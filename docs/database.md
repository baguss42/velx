# VelX database schema and local seed

T05 owns the PostgreSQL catalog/commercial tables:

- `tenants` and `branches`
- `car_models` and `car_variants`
- approved `vehicle_assets`
- `vehicle_units` inventory
- time-bounded `price_offers`
- `integration_sync_state` cursors and sync health

All child records carry `tenant_id`. Tenant-bound relationships use composite foreign
keys such as `(tenant_id, variant_id)`, backed by tenant-scoped unique keys. Monetary
values use `numeric(18,2)` and three-letter uppercase currency codes. Timestamps are
PostgreSQL `timestamptz` values; presentation code is responsible for localization.

## Offer validity and PostgreSQL extension

`price_offers` rejects negative and non-finite amounts (`NaN`, `Infinity`, and
`-Infinity`) as well as invalid currency/status/tax values. It also rejects
`valid_to <= valid_from`. The `excl_price_offers_no_overlap` exclusion
constraint prevents overlapping `[valid_from, valid_to)` ranges for the same tenant,
variant, branch, and price type. A null `valid_to` is converted to PostgreSQL
`infinity`, so an open-ended offer overlaps every later offer in that scope.

The migration runs `CREATE EXTENSION IF NOT EXISTS btree_gist` because the exclusion
constraint combines GiST range overlap with equality on UUID/text columns. If a managed
PostgreSQL service does not allow the migration role to create extensions, an operator
must pre-install/enable `btree_gist` before `alembic upgrade head`. The downgrade removes
the T05 constraint and tables but intentionally leaves this shared extension installed.

The `available_vehicle_units` view is the safe availability surface for future tools. It
contains only `status = 'available'` rows and omits `vin_encrypted` and
`vin_fingerprint`. Those columns are opaque storage boundaries only; T05 does not
implement encryption and no real VIN is present in the development fixture.

## Empty-database development path

Use a disposable local PostgreSQL database and a dedicated migration role. Do not use
these fictional fixtures in staging or production-like environments.

```sh
cp .env.example .env
# Start the local-only database service:
docker compose up -d postgres
# Set APP_ENV=development or test, DEV_SEED_ENABLED=true, and MIGRATION_DATABASE_URL:
# MIGRATION_DATABASE_URL=postgresql+psycopg://migrator:velx-local-only@localhost:5432/velx_dev
make db-seed
```

The Compose service binds PostgreSQL to `127.0.0.1` and persists data in the
`velx-postgres-data` named volume. `docker compose down` stops the service without
deleting local data; use `docker compose down -v` only when a fresh empty database is
needed. The Compose password is a disposable development value and must never be
reused outside local development.

`make db-seed` is fail-closed. It requires the explicit `DEV_SEED_ENABLED=true` opt-in,
uses only the dedicated `MIGRATION_DATABASE_URL`, and accepts only `localhost`, a
`*.localhost` name, or a loopback IPv4 address as the seed target. Bracketed IPv6
authorities are rejected. `DATABASE_URL` is never a fallback for seeding. Keep the
setting false unless the database is disposable local/test PostgreSQL;
`APP_ENV=staging` and `APP_ENV=production` are always rejected.

`make db-seed` runs `alembic upgrade head` and then
`scripts/seed_dev_db.py` in one explicit sequence. The seed reads the existing,
clearly labeled fixtures from `app/services/dev_fixtures.py`, writes all eight T05
record types, verifies the deterministic UUIDs by reading them back, and is safe to
rerun when the explicit local/test opt-in is enabled. A deterministic-ID collision with
any differing fixture value raises an error instead of overwriting the existing row.

For migrations without data, run `make db-upgrade`. To remove the T05 schema from a
disposable database, run `.venv/bin/alembic downgrade base`; this does not remove the
shared `btree_gist` extension.
