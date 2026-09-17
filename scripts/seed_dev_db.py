"""Seed the fictional VelX catalog into an already-migrated local PostgreSQL database."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from argparse import ArgumentParser

from sqlalchemy import create_engine

from app.config import Settings
from app.db.seed import seed_from_settings, validate_seed_settings


def main() -> int:
    """Run the guarded idempotent development seed."""

    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="apply Alembic migrations before seeding",
    )
    args = parser.parse_args()

    settings = Settings()
    try:
        database_url = validate_seed_settings(settings)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    if args.upgrade:
        migration_environment = os.environ.copy()
        migration_environment["MIGRATION_DATABASE_URL"] = database_url
        try:
            subprocess.run(
                [sys.executable, "-m", "alembic", "upgrade", "head"],
                check=True,
                env=migration_environment,
            )
        except subprocess.CalledProcessError as exc:
            raise SystemExit(f"Alembic upgrade failed with exit code {exc.returncode}") from exc

    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        result = seed_from_settings(engine, settings)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    finally:
        engine.dispose()

    print(json.dumps({"seeded": result.table_counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
