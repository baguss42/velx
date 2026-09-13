"""Idempotent, local-only seed data for the T05 catalog schema.

This module deliberately consumes ``app.services.dev_fixtures`` and refuses to be
called for staging or production-like settings. The VIN values are not real VINs;
the byte value is an opaque placeholder for the future encryption boundary, not an
encryption implementation.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from ipaddress import ip_address
from typing import Any, cast
from urllib.parse import urlsplit
from uuid import UUID

from sqlalchemy import Connection, Table, and_, func, select
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.engine import URL, Engine, make_url
from sqlalchemy.sql.selectable import FromClause

from app.config import Settings
from app.db.connection import normalize_postgresql_url
from app.services.dev_fixtures import (
    DEV_FIXTURE_BRANCH_ID,
    DevelopmentFixtures,
    get_development_fixtures,
)

from .models import (
    Branch,
    CarModel,
    CarVariant,
    IntegrationSyncState,
    PriceOffer,
    Tenant,
    VehicleAsset,
    VehicleUnit,
)

SEED_MODEL_ID = UUID("00000000-0000-0000-0000-000000000020")
SEED_ASSET_ID = UUID("00000000-0000-0000-0000-000000000030")
SEED_UNIT_ID = UUID("00000000-0000-0000-0000-000000000040")
SEED_PRICE_OFFER_ID = UUID("00000000-0000-0000-0000-000000000050")
SEED_SYNC_STATE_ID = UUID("00000000-0000-0000-0000-000000000060")
SEED_TIMESTAMP = datetime(2026, 1, 1, tzinfo=UTC)
SEED_FINGERPRINT = "f" * 64
_DEFAULT_POSTGRES_PORT = 5432


def _normalize_seed_host(host: str | None) -> str | None:
    """Normalize host spelling without treating distinct local hosts as equivalent."""

    if host is None:
        return None
    return host.lower().rstrip(".")


def _is_loopback_or_local_host(host: str) -> bool:
    """Return whether a database hostname is reserved for this machine."""

    normalized = _normalize_seed_host(host)
    if normalized is None:
        return False
    if normalized == "localhost" or normalized.endswith(".localhost"):
        return True
    try:
        address = ip_address(normalized)
    except ValueError:
        return False
    return address.version == 4 and address.is_loopback


def _seed_url_components(
    url: URL,
) -> tuple[str, str | None, str | None, str | None, int, str | None]:
    """Return connection target and credential components for exact seed binding."""

    port = _DEFAULT_POSTGRES_PORT if url.port is None else url.port
    return (
        url.drivername,
        url.username,
        url.password,
        _normalize_seed_host(url.host),
        port,
        url.database,
    )


def validate_seed_settings(settings: Settings) -> str:
    """Require explicit local fixture authorization and return its safe database URL."""

    if not settings.is_local:
        raise RuntimeError(
            "Fictional development fixtures are disabled outside development and test environments"
        )
    if not settings.dev_seed_enabled:
        raise RuntimeError("Set DEV_SEED_ENABLED=true to enable fictional development fixtures")

    configured_url = settings.migration_database_url
    if configured_url is None or not configured_url.strip():
        raise RuntimeError("Set MIGRATION_DATABASE_URL to a PostgreSQL URL before seeding")

    try:
        database_url = normalize_postgresql_url(configured_url)
        parsed = urlsplit(database_url)
        parsed_port = parsed.port
        host = parsed.hostname
    except ValueError as exc:
        raise RuntimeError(
            "MIGRATION_DATABASE_URL must be a valid PostgreSQL URL before seeding"
        ) from exc

    authority = parsed.netloc.rsplit("@", maxsplit=1)[-1]
    if authority.startswith("["):
        raise RuntimeError(
            "MIGRATION_DATABASE_URL must target localhost or a loopback IPv4 address; "
            "bracketed IPv6 authorities are not supported when seeding"
        )
    if ":" in authority:
        port_text = authority.rsplit(":", maxsplit=1)[-1]
        if not port_text.isascii() or not port_text.isdigit():
            raise RuntimeError(
                "MIGRATION_DATABASE_URL must use a valid PostgreSQL port when seeding"
            )
    if parsed_port is not None and not 1 <= parsed_port <= 65_535:
        raise RuntimeError(
            "MIGRATION_DATABASE_URL must use a PostgreSQL port between 1 and 65535 when seeding"
        )

    if parsed.query:
        raise RuntimeError("MIGRATION_DATABASE_URL must not include query parameters when seeding")
    if parsed.fragment:
        raise RuntimeError("MIGRATION_DATABASE_URL must not include fragment data when seeding")
    if not parsed.username:
        raise RuntimeError(
            "MIGRATION_DATABASE_URL must include a dedicated database role when seeding"
        )

    if host is None or not _is_loopback_or_local_host(host):
        raise RuntimeError(
            "MIGRATION_DATABASE_URL must target localhost or a loopback IPv4 address when seeding"
        )
    return database_url


@dataclass(frozen=True)
class SeedResult:
    """Identifiers written by the local fixture seed."""

    table_counts: dict[str, int]


def _upsert(connection: Connection, table: FromClause, values: Mapping[str, Any]) -> None:
    """Insert one fixture row or update it only when every fixture value matches."""

    typed_table = cast(Table, table)
    record_id = values["id"]
    statement = postgresql_insert(typed_table).values(dict(values))
    updates = {key: value for key, value in values.items() if key not in {"id", "created_at"}}
    updates["updated_at"] = func.current_timestamp()
    fixture_values_match = and_(
        *(
            typed_table.c[key].is_(None) if value is None else typed_table.c[key] == value
            for key, value in values.items()
        )
    )
    result = connection.execute(
        statement.on_conflict_do_update(
            index_elements=[typed_table.c.id],
            set_=updates,
            where=fixture_values_match,
        ).returning(typed_table.c.id)
    )
    if result.scalar_one_or_none() is not None:
        return

    existing = (
        connection.execute(select(typed_table).where(typed_table.c.id == record_id))
        .mappings()
        .one_or_none()
    )
    if existing is None:
        raise RuntimeError(
            f"Seed fixture collision in {typed_table.name} for id {record_id}; "
            "the existing row could not be read back"
        )

    mismatches = [key for key, value in values.items() if existing[key] != value]
    if not mismatches:
        mismatches = ["fixture values"]
    raise RuntimeError(
        f"Seed fixture collision in {typed_table.name} for id {record_id}; "
        f"existing row differs in {', '.join(mismatches)}"
    )


def _seed_row(
    connection: Connection,
    expected: dict[str, tuple[FromClause, Mapping[str, Any]]],
    label: str,
    table: FromClause,
    values: Mapping[str, Any],
) -> None:
    """Write one fixture row and retain its supplied values for read-back verification."""

    expected[label] = (table, dict(values))
    _upsert(connection, table, values)


def _verify_seeded_values(
    connection: Connection,
    expected: Mapping[str, tuple[FromClause, Mapping[str, Any]]],
) -> None:
    """Read back every seeded row and every fixture-supplied field before success."""

    for label, (table, expected_values) in expected.items():
        typed_table = cast(Table, table)
        record_id = expected_values["id"]
        existing = (
            connection.execute(select(typed_table).where(typed_table.c.id == record_id))
            .mappings()
            .one_or_none()
        )
        if existing is None:
            raise RuntimeError(f"Seed verification failed for {label}")
        mismatches = [key for key, value in expected_values.items() if existing[key] != value]
        if mismatches:
            raise RuntimeError(
                f"Seed verification failed for {label}; fields differ: {', '.join(mismatches)}"
            )


def seed_development_database(
    engine: Engine,
    fixtures: DevelopmentFixtures,
    *,
    settings: Settings,
) -> SeedResult:
    """Write the fictional catalog fixture in one transaction.

    Alembic owns table creation. This function assumes ``alembic upgrade head``
    has already run and never calls ``create_all`` or creates a SQLite substitute.
    """

    migration_url = validate_seed_settings(settings)
    try:
        migration_engine_url = make_url(migration_url)
    except ValueError as exc:
        raise RuntimeError(
            "MIGRATION_DATABASE_URL must be a valid PostgreSQL URL before seeding"
        ) from exc

    if engine.url.query:
        raise RuntimeError("Seed engine must not include query parameters when seeding")
    if engine.url.username != migration_engine_url.username:
        raise RuntimeError(
            "Seed engine must use the dedicated migration database role when seeding"
        )
    if _seed_url_components(engine.url) != _seed_url_components(migration_engine_url):
        raise RuntimeError(
            "Seed engine must match the validated MIGRATION_DATABASE_URL when seeding"
        )
    if fixtures.showroom.tenant_id != settings.tenant_id:
        raise RuntimeError(
            "Configured TENANT_ID must match the fictional fixture tenant before seeding"
        )

    showroom = fixtures.showroom
    car = fixtures.cars[0]
    price = fixtures.prices[0]
    if price.branch_id != DEV_FIXTURE_BRANCH_ID or price.variant_id != car.variant_id:
        raise RuntimeError("Development fixture relationships do not match the T05 seed boundary")

    expected: dict[str, tuple[FromClause, Mapping[str, Any]]] = {}

    with engine.begin() as connection:
        _seed_row(
            connection,
            expected,
            "tenant",
            Tenant.__table__,
            {
                "id": showroom.tenant_id,
                "name": showroom.name,
                "brand_name": showroom.brand_name,
                "default_locale": "id-ID",
                "currency": price.currency,
                "timezone": showroom.timezone,
            },
        )
        _seed_row(
            connection,
            expected,
            "branch",
            Branch.__table__,
            {
                "id": DEV_FIXTURE_BRANCH_ID,
                "tenant_id": showroom.tenant_id,
                "code": showroom.code,
                "name": showroom.name,
                "address": showroom.address,
                "market_code": "ID",
                "timezone": showroom.timezone,
                "hours_json": {
                    "mon-fri": "09:00-17:00",
                    "sat": "09:00-15:00",
                    "sun": "closed",
                    "fixture_label": fixtures.fixture_label,
                },
                "approved_phone": "+62-000-0000",
            },
        )
        _seed_row(
            connection,
            expected,
            "car_model",
            CarModel.__table__,
            {
                "id": SEED_MODEL_ID,
                "tenant_id": car.tenant_id,
                "code": car.model_code,
                "name": car.model_name,
                "brand": showroom.brand_name,
                "model_year": car.model_year,
                "body_type": car.body_type,
                "market_code": "ID",
                "active": True,
            },
        )
        _seed_row(
            connection,
            expected,
            "car_variant",
            CarVariant.__table__,
            {
                "id": car.variant_id,
                "tenant_id": car.tenant_id,
                "model_id": SEED_MODEL_ID,
                "code": f"{car.model_code}-CITYLINE",
                "name": car.variant_name,
                "powertrain": "electric",
                "transmission": "single-speed",
                "specs_json": {
                    "body_type": car.body_type,
                    "model_year": car.model_year,
                    "fixture_label": fixtures.fixture_label,
                },
                "active": True,
            },
        )
        _seed_row(
            connection,
            expected,
            "vehicle_asset",
            VehicleAsset.__table__,
            {
                "id": SEED_ASSET_ID,
                "tenant_id": car.tenant_id,
                "variant_id": car.variant_id,
                "kind": "brochure",
                "approved_url": "https://fictional.velx.invalid/assets/aurora-e2-cityline.pdf",
                "title": "Aurora E2 Cityline EV brochure (fictional)",
                "locale": "id-ID",
                "approved_at": SEED_TIMESTAMP,
            },
        )
        _seed_row(
            connection,
            expected,
            "vehicle_unit",
            VehicleUnit.__table__,
            {
                "id": SEED_UNIT_ID,
                "tenant_id": car.tenant_id,
                "variant_id": car.variant_id,
                "branch_id": DEV_FIXTURE_BRANCH_ID,
                "color_code": "fictional-blue",
                "vin_encrypted": b"fictional-dev-ciphertext-boundary",
                "vin_fingerprint": SEED_FINGERPRINT,
                "status": "available",
                "source_updated_at": SEED_TIMESTAMP,
            },
        )
        _seed_row(
            connection,
            expected,
            "price_offer",
            PriceOffer.__table__,
            {
                "id": SEED_PRICE_OFFER_ID,
                "tenant_id": car.tenant_id,
                "variant_id": price.variant_id,
                "branch_id": price.branch_id,
                "price_type": "public_retail",
                "amount": price.amount,
                "currency": price.currency,
                "tax_basis": "tax_inclusive",
                "qualifiers_json": {
                    "availability": price.availability,
                    "fixture_label": fixtures.fixture_label,
                    "note": "Fictional development offer; not a live quotation.",
                },
                "valid_from": SEED_TIMESTAMP,
                "valid_to": None,
                "source_updated_at": SEED_TIMESTAMP,
            },
        )
        _seed_row(
            connection,
            expected,
            "integration_sync_state",
            IntegrationSyncState.__table__,
            {
                "id": SEED_SYNC_STATE_ID,
                "tenant_id": car.tenant_id,
                "integration": "fictional_dms",
                "resource_kind": "catalog",
                "last_cursor": "fictional-seed-v1",
                "last_success_at": None,
                "last_error_code": None,
            },
        )

    with engine.connect() as connection:
        _verify_seeded_values(connection, expected)

    return SeedResult(table_counts={label: 1 for label in expected})


def seed_from_settings(engine: Engine, settings: Settings) -> SeedResult:
    """Load the guarded fixture bundle and seed it into an already-migrated database."""

    validate_seed_settings(settings)
    fixtures = get_development_fixtures(settings)
    return seed_development_database(engine, fixtures, settings=settings)
