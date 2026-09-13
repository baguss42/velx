"""Database URL helpers shared by Alembic and local seed tooling."""

from __future__ import annotations


def normalize_postgresql_url(url: str) -> str:
    """Return a SQLAlchemy URL that explicitly selects the psycopg 3 driver."""

    normalized_url = url.strip()
    if normalized_url.startswith("postgresql://"):
        return "postgresql+psycopg://" + normalized_url.removeprefix("postgresql://")
    if normalized_url.startswith("postgresql+psycopg://"):
        return normalized_url
    raise ValueError("Expected a postgresql:// or postgresql+psycopg:// URL")


__all__ = ["normalize_postgresql_url"]
