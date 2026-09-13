"""Create the tenant-scoped catalog and commercial schema for T05.

The price-offer exclusion constraint uses PostgreSQL's ``btree_gist`` extension so
that equality on tenant/variant/branch/price type and overlap on a ``tstzrange``
can be enforced by one database constraint. The migration creates the extension
when the migration role is permitted to do so; operators must pre-install or
allow ``btree_gist`` on PostgreSQL services that restrict ``CREATE EXTENSION``.
The downgrade intentionally leaves the shared extension installed.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260913_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


UTC_TIMESTAMP = sa.text("CURRENT_TIMESTAMP")


def upgrade() -> None:
    """Create all T05 tables, indexes, integrity constraints, and safe views."""

    # btree_gist supplies GiST operator classes for UUID and text equality in the
    # price-offer exclusion constraint below. It is deliberately not dropped on
    # downgrade because it may be shared by other application constraints.
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("brand_name", sa.String(length=200), nullable=False),
        sa.Column("default_locale", sa.String(length=16), nullable=False),
        sa.Column("currency", postgresql.CHAR(length=3), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="pk_tenants"),
        sa.CheckConstraint("char_length(trim(name)) > 0", name="ck_tenants_name_nonempty"),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_tenants_currency_format"),
        sa.CheckConstraint(
            "char_length(trim(default_locale)) > 0",
            name="ck_tenants_default_locale_nonempty",
        ),
        sa.CheckConstraint(
            "char_length(trim(timezone)) > 0",
            name="ck_tenants_timezone_nonempty",
        ),
    )

    op.create_table(
        "branches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("market_code", sa.String(length=16), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column(
            "hours_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("approved_phone", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_branches_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_branches"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_branches_tenant_id"),
        sa.UniqueConstraint("tenant_id", "code", name="uq_branches_tenant_code"),
        sa.CheckConstraint("char_length(trim(code)) > 0", name="ck_branches_code_nonempty"),
        sa.CheckConstraint("char_length(trim(name)) > 0", name="ck_branches_name_nonempty"),
        sa.CheckConstraint(
            "char_length(trim(market_code)) > 0",
            name="ck_branches_market_code_nonempty",
        ),
        sa.CheckConstraint("char_length(trim(timezone)) > 0", name="ck_branches_timezone_nonempty"),
    )
    op.create_index(
        "ix_branches_tenant_market_code",
        "branches",
        ["tenant_id", "market_code"],
    )

    op.create_table(
        "car_models",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("brand", sa.String(length=200), nullable=False),
        sa.Column("model_year", sa.Integer(), nullable=False),
        sa.Column("body_type", sa.String(length=64), nullable=False),
        sa.Column("market_code", sa.String(length=16), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_car_models_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_car_models"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_car_models_tenant_id"),
        sa.UniqueConstraint(
            "tenant_id",
            "code",
            "model_year",
            "market_code",
            name="uq_car_models_tenant_code_year_market",
        ),
        sa.CheckConstraint("char_length(trim(code)) > 0", name="ck_car_models_code_nonempty"),
        sa.CheckConstraint("char_length(trim(name)) > 0", name="ck_car_models_name_nonempty"),
        sa.CheckConstraint("char_length(trim(brand)) > 0", name="ck_car_models_brand_nonempty"),
        sa.CheckConstraint(
            "model_year BETWEEN 1886 AND 9999",
            name="ck_car_models_model_year_valid",
        ),
        sa.CheckConstraint(
            "char_length(trim(body_type)) > 0", name="ck_car_models_body_type_nonempty"
        ),
        sa.CheckConstraint(
            "char_length(trim(market_code)) > 0",
            name="ck_car_models_market_code_nonempty",
        ),
    )
    op.create_index(
        "ix_car_models_tenant_active_market",
        "car_models",
        ["tenant_id", "active", "market_code"],
    )

    op.create_table(
        "car_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("model_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("powertrain", sa.String(length=64), nullable=False),
        sa.Column("transmission", sa.String(length=64), nullable=False),
        sa.Column(
            "specs_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_car_variants_tenant",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "model_id"],
            ["car_models.tenant_id", "car_models.id"],
            name="fk_car_variants_model_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_car_variants"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_car_variants_tenant_id"),
        sa.UniqueConstraint("tenant_id", "code", name="uq_car_variants_tenant_code"),
        sa.CheckConstraint("char_length(trim(code)) > 0", name="ck_car_variants_code_nonempty"),
        sa.CheckConstraint("char_length(trim(name)) > 0", name="ck_car_variants_name_nonempty"),
        sa.CheckConstraint(
            "char_length(trim(powertrain)) > 0",
            name="ck_car_variants_powertrain_nonempty",
        ),
        sa.CheckConstraint(
            "char_length(trim(transmission)) > 0",
            name="ck_car_variants_transmission_nonempty",
        ),
    )
    op.create_index(
        "ix_car_variants_tenant_model",
        "car_variants",
        ["tenant_id", "model_id"],
    )

    op.create_table(
        "vehicle_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("approved_url", sa.Text(), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_vehicle_assets_tenant",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "variant_id"],
            ["car_variants.tenant_id", "car_variants.id"],
            name="fk_vehicle_assets_variant_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_vehicle_assets"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_vehicle_assets_tenant_id"),
        sa.CheckConstraint(
            "kind IN ('image', 'brochure', 'manual')",
            name="ck_vehicle_assets_kind",
        ),
        sa.CheckConstraint(
            (
                r"approved_url ~ '^https://(([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?[.])*"
                r"([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?))"
                r"(:([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|"
                r"65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?([/?#][^[:space:]]*)?$'"
            ),
            name="ck_vehicle_assets_approved_url_https",
        ),
        sa.CheckConstraint("char_length(trim(title)) > 0", name="ck_vehicle_assets_title_nonempty"),
        sa.CheckConstraint(
            "char_length(trim(locale)) > 0", name="ck_vehicle_assets_locale_nonempty"
        ),
    )
    op.create_index(
        "ix_vehicle_assets_tenant_variant_kind",
        "vehicle_assets",
        ["tenant_id", "variant_id", "kind"],
    )

    op.create_table(
        "vehicle_units",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("color_code", sa.String(length=64), nullable=True),
        sa.Column(
            "vin_encrypted",
            sa.LargeBinary(),
            nullable=True,
            comment="Opaque ciphertext boundary; T05 does not implement encryption.",
        ),
        sa.Column("vin_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_vehicle_units_tenant",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "variant_id"],
            ["car_variants.tenant_id", "car_variants.id"],
            name="fk_vehicle_units_variant_tenant",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_vehicle_units_branch_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_vehicle_units"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_vehicle_units_tenant_id"),
        sa.UniqueConstraint(
            "tenant_id",
            "vin_fingerprint",
            name="uq_vehicle_units_tenant_vin_fingerprint",
        ),
        sa.CheckConstraint(
            "status IN ('available', 'reserved', 'sold', 'in_transit', 'unavailable')",
            name="ck_vehicle_units_status",
        ),
        sa.CheckConstraint(
            "vin_fingerprint IS NULL OR vin_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_vehicle_units_vin_fingerprint_format",
        ),
        sa.CheckConstraint(
            "vin_encrypted IS NULL OR octet_length(vin_encrypted) > 0",
            name="ck_vehicle_units_encrypted_vin_nonempty",
        ),
    )
    op.create_index(
        "ix_vehicle_units_tenant_variant_branch_status",
        "vehicle_units",
        ["tenant_id", "variant_id", "branch_id", "status"],
    )

    op.create_table(
        "price_offers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("price_type", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", postgresql.CHAR(length=3), nullable=False),
        sa.Column("tax_basis", sa.String(length=32), nullable=False),
        sa.Column(
            "qualifiers_json",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_price_offers_tenant",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "variant_id"],
            ["car_variants.tenant_id", "car_variants.id"],
            name="fk_price_offers_variant_tenant",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_price_offers_branch_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_price_offers"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_price_offers_tenant_id"),
        sa.CheckConstraint(
            "price_type IN ('public_retail', 'promotional', 'finance', 'fleet')",
            name="ck_price_offers_price_type",
        ),
        sa.CheckConstraint(
            "amount >= 0 AND amount NOT IN "
            "('NaN'::numeric, 'Infinity'::numeric, '-Infinity'::numeric)",
            name="ck_price_offers_amount_nonnegative",
        ),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_price_offers_currency_format"),
        sa.CheckConstraint(
            "tax_basis IN ('tax_inclusive', 'tax_exclusive', 'unknown')",
            name="ck_price_offers_tax_basis",
        ),
        sa.CheckConstraint(
            "isfinite(valid_from)",
            name="ck_price_offers_valid_from_finite",
        ),
        sa.CheckConstraint(
            "valid_to IS NULL OR valid_to > valid_from",
            name="ck_price_offers_valid_window",
        ),
    )
    op.create_index(
        "ix_price_offers_tenant_variant_branch_validity",
        "price_offers",
        ["tenant_id", "variant_id", "branch_id", "valid_from", "valid_to"],
    )
    op.execute(
        """
        ALTER TABLE price_offers
        ADD CONSTRAINT excl_price_offers_no_overlap
        EXCLUDE USING gist (
            tenant_id WITH =,
            variant_id WITH =,
            branch_id WITH =,
            price_type WITH =,
            (tstzrange(valid_from, COALESCE(valid_to, 'infinity'::timestamptz), '[)'::text)) WITH &&
        )
        """
    )

    op.create_table(
        "integration_sync_state",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("integration", sa.String(length=64), nullable=False),
        sa.Column("resource_kind", sa.String(length=64), nullable=False),
        sa.Column("last_cursor", sa.Text(), nullable=True),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error_code", sa.String(length=128), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=UTC_TIMESTAMP, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name="fk_integration_sync_state_tenant",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_integration_sync_state"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_integration_sync_state_tenant_id"),
        sa.UniqueConstraint(
            "tenant_id",
            "integration",
            "resource_kind",
            name="uq_integration_sync_state_scope",
        ),
        sa.CheckConstraint(
            "char_length(trim(integration)) > 0",
            name="ck_integration_sync_state_integration_nonempty",
        ),
        sa.CheckConstraint(
            "char_length(trim(resource_kind)) > 0",
            name="ck_integration_sync_state_resource_kind_nonempty",
        ),
        sa.CheckConstraint(
            "last_error_code IS NULL OR char_length(trim(last_error_code)) > 0",
            name="ck_integration_sync_state_error_code_nonempty",
        ),
    )
    op.create_index(
        "ix_integration_sync_state_tenant_integration_success",
        "integration_sync_state",
        ["tenant_id", "integration", "last_success_at"],
    )

    # This is the only inventory surface intended for future availability tools:
    # it excludes all VIN fields and makes the available-only rule explicit.
    op.execute(
        """
        CREATE VIEW available_vehicle_units AS
        SELECT id, tenant_id, variant_id, branch_id, color_code, status, source_updated_at
        FROM vehicle_units
        WHERE status = 'available'
        """
    )
    op.execute(
        """
        COMMENT ON VIEW available_vehicle_units IS
        'Available units only; no VIN fields. Application authorization remains required.'
        """
    )
    op.execute(
        """
        COMMENT ON COLUMN vehicle_units.vin_fingerprint IS
        'One-way lookup fingerprint boundary; raw VIN values must never be stored or exposed here.'
        """
    )


def downgrade() -> None:
    """Remove T05 objects while retaining the shared btree_gist extension."""

    op.execute("DROP VIEW IF EXISTS available_vehicle_units")
    op.execute("ALTER TABLE price_offers DROP CONSTRAINT IF EXISTS excl_price_offers_no_overlap")
    op.drop_index(
        "ix_integration_sync_state_tenant_integration_success",
        table_name="integration_sync_state",
    )
    op.drop_table("integration_sync_state")
    op.drop_index("ix_price_offers_tenant_variant_branch_validity", table_name="price_offers")
    op.drop_table("price_offers")
    op.drop_index("ix_vehicle_units_tenant_variant_branch_status", table_name="vehicle_units")
    op.drop_table("vehicle_units")
    op.drop_index("ix_vehicle_assets_tenant_variant_kind", table_name="vehicle_assets")
    op.drop_table("vehicle_assets")
    op.drop_index("ix_car_variants_tenant_model", table_name="car_variants")
    op.drop_table("car_variants")
    op.drop_index("ix_car_models_tenant_active_market", table_name="car_models")
    op.drop_table("car_models")
    op.drop_index("ix_branches_tenant_market_code", table_name="branches")
    op.drop_table("branches")
    op.drop_table("tenants")
