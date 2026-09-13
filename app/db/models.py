"""SQLAlchemy 2 metadata for the catalog and commercial schema slice.

The Alembic migration is the authoritative DDL. These models provide typed SQLAlchemy
boundaries for seed code and the repositories implemented by later tasks. VIN columns are
opaque storage boundaries; application services must never include them in customer/tool DTOs.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    LargeBinary,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import (
    CHAR,
    JSONB,
    ExcludeConstraint,
)
from sqlalchemy.dialects.postgresql import (
    UUID as PostgreSQLUUID,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

APPROVED_ASSET_URL_REGEX = (
    r"^https://(([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?[.])*"
    r"([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?))"
    r"(:([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|"
    r"65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?([/?#][^[:space:]]*)?$"
)


class Base(DeclarativeBase):
    """Base metadata for VelX application-owned tables."""


class TimestampColumnsMixin:
    """UTC-aware timestamp columns shared by catalog and sync records."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Tenant(TimestampColumnsMixin, Base):
    """Tenant root for all catalog and commercial records."""

    __tablename__ = "tenants"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brand_name: Mapped[str] = mapped_column(String(200), nullable=False)
    default_locale: Mapped[str] = mapped_column(String(16), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="ck_tenants_name_nonempty"),
        CheckConstraint(
            "currency ~ '^[A-Z]{3}$'",
            name="ck_tenants_currency_format",
        ),
        CheckConstraint(
            "char_length(trim(default_locale)) > 0",
            name="ck_tenants_default_locale_nonempty",
        ),
        CheckConstraint(
            "char_length(trim(timezone)) > 0",
            name="ck_tenants_timezone_nonempty",
        ),
    )


class Branch(TimestampColumnsMixin, Base):
    """Tenant-owned showroom branch."""

    __tablename__ = "branches"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    market_code: Mapped[str] = mapped_column(String(16), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    hours_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    approved_phone: Mapped[str | None] = mapped_column(String(64), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_branches_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_branches_tenant_id"),
        UniqueConstraint("tenant_id", "code", name="uq_branches_tenant_code"),
        Index("ix_branches_tenant_market_code", "tenant_id", "market_code"),
        CheckConstraint("char_length(trim(code)) > 0", name="ck_branches_code_nonempty"),
        CheckConstraint("char_length(trim(name)) > 0", name="ck_branches_name_nonempty"),
        CheckConstraint(
            "char_length(trim(market_code)) > 0",
            name="ck_branches_market_code_nonempty",
        ),
        CheckConstraint("char_length(trim(timezone)) > 0", name="ck_branches_timezone_nonempty"),
    )


class CarModel(TimestampColumnsMixin, Base):
    """Tenant-owned model-year catalog entry."""

    __tablename__ = "car_models"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brand: Mapped[str] = mapped_column(String(200), nullable=False)
    model_year: Mapped[int] = mapped_column(Integer, nullable=False)
    body_type: Mapped[str] = mapped_column(String(64), nullable=False)
    market_code: Mapped[str] = mapped_column(String(16), nullable=False)
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_car_models_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_car_models_tenant_id"),
        UniqueConstraint(
            "tenant_id",
            "code",
            "model_year",
            "market_code",
            name="uq_car_models_tenant_code_year_market",
        ),
        Index("ix_car_models_tenant_active_market", "tenant_id", "active", "market_code"),
        CheckConstraint("char_length(trim(code)) > 0", name="ck_car_models_code_nonempty"),
        CheckConstraint("char_length(trim(name)) > 0", name="ck_car_models_name_nonempty"),
        CheckConstraint("char_length(trim(brand)) > 0", name="ck_car_models_brand_nonempty"),
        CheckConstraint(
            "model_year BETWEEN 1886 AND 9999",
            name="ck_car_models_model_year_valid",
        ),
        CheckConstraint(
            "char_length(trim(body_type)) > 0", name="ck_car_models_body_type_nonempty"
        ),
        CheckConstraint(
            "char_length(trim(market_code)) > 0",
            name="ck_car_models_market_code_nonempty",
        ),
    )


class CarVariant(TimestampColumnsMixin, Base):
    """Tenant-owned model variant with searchable specifications."""

    __tablename__ = "car_variants"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    model_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    powertrain: Mapped[str] = mapped_column(String(64), nullable=False)
    transmission: Mapped[str] = mapped_column(String(64), nullable=False)
    specs_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_car_variants_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ("tenant_id", "model_id"),
            ("car_models.tenant_id", "car_models.id"),
            name="fk_car_variants_model_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_car_variants_tenant_id"),
        UniqueConstraint("tenant_id", "code", name="uq_car_variants_tenant_code"),
        Index("ix_car_variants_tenant_model", "tenant_id", "model_id"),
        CheckConstraint("char_length(trim(code)) > 0", name="ck_car_variants_code_nonempty"),
        CheckConstraint("char_length(trim(name)) > 0", name="ck_car_variants_name_nonempty"),
        CheckConstraint(
            "char_length(trim(powertrain)) > 0",
            name="ck_car_variants_powertrain_nonempty",
        ),
        CheckConstraint(
            "char_length(trim(transmission)) > 0",
            name="ck_car_variants_transmission_nonempty",
        ),
    )


class VehicleAsset(TimestampColumnsMixin, Base):
    """Approved variant media/document metadata."""

    __tablename__ = "vehicle_assets"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    variant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    approved_url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    locale: Mapped[str] = mapped_column(String(16), nullable=False)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_vehicle_assets_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ("tenant_id", "variant_id"),
            ("car_variants.tenant_id", "car_variants.id"),
            name="fk_vehicle_assets_variant_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_vehicle_assets_tenant_id"),
        Index("ix_vehicle_assets_tenant_variant_kind", "tenant_id", "variant_id", "kind"),
        CheckConstraint(
            "kind IN ('image', 'brochure', 'manual')",
            name="ck_vehicle_assets_kind",
        ),
        CheckConstraint(
            f"approved_url ~ '{APPROVED_ASSET_URL_REGEX}'",
            name="ck_vehicle_assets_approved_url_https",
        ),
        CheckConstraint("char_length(trim(title)) > 0", name="ck_vehicle_assets_title_nonempty"),
        CheckConstraint("char_length(trim(locale)) > 0", name="ck_vehicle_assets_locale_nonempty"),
    )


class VehicleUnit(TimestampColumnsMixin, Base):
    """Branch inventory unit with opaque VIN storage boundaries."""

    __tablename__ = "vehicle_units"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    variant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    color_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    vin_encrypted: Mapped[bytes | None] = mapped_column(
        LargeBinary,
        nullable=True,
        comment="Opaque ciphertext boundary; T05 does not implement encryption.",
    )
    vin_fingerprint: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment=(
            "One-way lookup fingerprint boundary; raw VIN values must never be stored "
            "or exposed here."
        ),
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    source_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_vehicle_units_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ("tenant_id", "variant_id"),
            ("car_variants.tenant_id", "car_variants.id"),
            name="fk_vehicle_units_variant_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ("tenant_id", "branch_id"),
            ("branches.tenant_id", "branches.id"),
            name="fk_vehicle_units_branch_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_vehicle_units_tenant_id"),
        UniqueConstraint(
            "tenant_id",
            "vin_fingerprint",
            name="uq_vehicle_units_tenant_vin_fingerprint",
        ),
        Index(
            "ix_vehicle_units_tenant_variant_branch_status",
            "tenant_id",
            "variant_id",
            "branch_id",
            "status",
        ),
        CheckConstraint(
            "status IN ('available', 'reserved', 'sold', 'in_transit', 'unavailable')",
            name="ck_vehicle_units_status",
        ),
        CheckConstraint(
            "vin_fingerprint IS NULL OR vin_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_vehicle_units_vin_fingerprint_format",
        ),
        CheckConstraint(
            "vin_encrypted IS NULL OR octet_length(vin_encrypted) > 0",
            name="ck_vehicle_units_encrypted_vin_nonempty",
        ),
    )


class PriceOffer(TimestampColumnsMixin, Base):
    """Time-bounded, branch-specific commercial offer."""

    __tablename__ = "price_offers"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    variant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    price_type: Mapped[str] = mapped_column(String(32), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    tax_basis: Mapped[str] = mapped_column(String(32), nullable=False)
    qualifiers_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_price_offers_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ("tenant_id", "variant_id"),
            ("car_variants.tenant_id", "car_variants.id"),
            name="fk_price_offers_variant_tenant",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ("tenant_id", "branch_id"),
            ("branches.tenant_id", "branches.id"),
            name="fk_price_offers_branch_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_price_offers_tenant_id"),
        Index(
            "ix_price_offers_tenant_variant_branch_validity",
            "tenant_id",
            "variant_id",
            "branch_id",
            "valid_from",
            "valid_to",
        ),
        CheckConstraint(
            "price_type IN ('public_retail', 'promotional', 'finance', 'fleet')",
            name="ck_price_offers_price_type",
        ),
        CheckConstraint(
            "amount >= 0 AND amount NOT IN "
            "('NaN'::numeric, 'Infinity'::numeric, '-Infinity'::numeric)",
            name="ck_price_offers_amount_nonnegative",
        ),
        CheckConstraint(
            "currency ~ '^[A-Z]{3}$'",
            name="ck_price_offers_currency_format",
        ),
        CheckConstraint(
            "tax_basis IN ('tax_inclusive', 'tax_exclusive', 'unknown')",
            name="ck_price_offers_tax_basis",
        ),
        CheckConstraint(
            "isfinite(valid_from)",
            name="ck_price_offers_valid_from_finite",
        ),
        CheckConstraint(
            "valid_to IS NULL OR valid_to > valid_from",
            name="ck_price_offers_valid_window",
        ),
        ExcludeConstraint(
            ("tenant_id", "="),
            ("variant_id", "="),
            ("branch_id", "="),
            ("price_type", "="),
            (
                text(
                    "tstzrange(valid_from, COALESCE(valid_to, 'infinity'::timestamptz), '[)'::text)"
                ),
                "&&",
            ),
            name="excl_price_offers_no_overlap",
            using="gist",
        ),
    )


class IntegrationSyncState(TimestampColumnsMixin, Base):
    """Cursor and health state for tenant-scoped imported business resources."""

    __tablename__ = "integration_sync_state"

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False)
    integration: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    last_cursor: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_code: Mapped[str | None] = mapped_column(String(128), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ("tenant_id",),
            ("tenants.id",),
            name="fk_integration_sync_state_tenant",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_integration_sync_state_tenant_id"),
        UniqueConstraint(
            "tenant_id",
            "integration",
            "resource_kind",
            name="uq_integration_sync_state_scope",
        ),
        Index(
            "ix_integration_sync_state_tenant_integration_success",
            "tenant_id",
            "integration",
            "last_success_at",
        ),
        CheckConstraint(
            "char_length(trim(integration)) > 0",
            name="ck_integration_sync_state_integration_nonempty",
        ),
        CheckConstraint(
            "char_length(trim(resource_kind)) > 0",
            name="ck_integration_sync_state_resource_kind_nonempty",
        ),
        CheckConstraint(
            "last_error_code IS NULL OR char_length(trim(last_error_code)) > 0",
            name="ck_integration_sync_state_error_code_nonempty",
        ),
    )


__all__ = [
    "Base",
    "Branch",
    "CarModel",
    "CarVariant",
    "IntegrationSyncState",
    "PriceOffer",
    "Tenant",
    "VehicleAsset",
    "VehicleUnit",
]
