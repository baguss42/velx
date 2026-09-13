"""Clearly fictional showroom data for local development and contract work."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from app.config import Settings, get_settings

FICTIONAL_FIXTURE_LABEL = "FICTIONAL DEVELOPMENT FIXTURE - NOT REAL SHOWROOM DATA"
DEV_FIXTURE_TENANT_ID = UUID("00000000-0000-0000-0000-000000000001")
DEV_FIXTURE_SHOWROOM_ID = UUID("00000000-0000-0000-0000-000000000010")
DEV_FIXTURE_BRANCH_ID = UUID("00000000-0000-0000-0000-000000000011")
DEV_FIXTURE_VARIANT_ID = UUID("00000000-0000-0000-0000-000000000021")


@dataclass(frozen=True)
class DevelopmentShowroom:
    """Fictional showroom record with a visible non-production marker."""

    id: UUID
    tenant_id: UUID
    code: str
    name: str
    brand_name: str
    address: str
    timezone: str
    fixture_label: str = FICTIONAL_FIXTURE_LABEL
    is_fictional: bool = True


@dataclass(frozen=True)
class DevelopmentCar:
    """Fictional catalog variant for local tool and UI development."""

    variant_id: UUID
    tenant_id: UUID
    model_code: str
    model_name: str
    variant_name: str
    model_year: int
    body_type: str
    fixture_label: str = FICTIONAL_FIXTURE_LABEL
    is_fictional: bool = True


@dataclass(frozen=True)
class DevelopmentPrice:
    """Fictional price snapshot; it must never be presented as a live offer."""

    variant_id: UUID
    branch_id: UUID
    amount: Decimal
    currency: str
    availability: str
    fixture_label: str = FICTIONAL_FIXTURE_LABEL
    is_fictional: bool = True


@dataclass(frozen=True)
class DevelopmentFixtures:
    """Bundle of local-only fictional records used by later repository slices."""

    fixture_label: str
    showroom: DevelopmentShowroom
    cars: tuple[DevelopmentCar, ...]
    prices: tuple[DevelopmentPrice, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize fixture values into JSON-safe primitives for local tooling."""

        return {
            "fixture_label": self.fixture_label,
            "showroom": {
                "id": str(self.showroom.id),
                "tenant_id": str(self.showroom.tenant_id),
                "code": self.showroom.code,
                "name": self.showroom.name,
                "brand_name": self.showroom.brand_name,
                "address": self.showroom.address,
                "timezone": self.showroom.timezone,
                "fixture_label": self.showroom.fixture_label,
                "is_fictional": self.showroom.is_fictional,
            },
            "cars": [
                {
                    "variant_id": str(car.variant_id),
                    "tenant_id": str(car.tenant_id),
                    "model_code": car.model_code,
                    "model_name": car.model_name,
                    "variant_name": car.variant_name,
                    "model_year": car.model_year,
                    "body_type": car.body_type,
                    "fixture_label": car.fixture_label,
                    "is_fictional": car.is_fictional,
                }
                for car in self.cars
            ],
            "prices": [
                {
                    "variant_id": str(price.variant_id),
                    "branch_id": str(price.branch_id),
                    "amount": str(price.amount),
                    "currency": price.currency,
                    "availability": price.availability,
                    "fixture_label": price.fixture_label,
                    "is_fictional": price.is_fictional,
                }
                for price in self.prices
            ],
        }


DEVELOPMENT_FIXTURES = DevelopmentFixtures(
    fixture_label=FICTIONAL_FIXTURE_LABEL,
    showroom=DevelopmentShowroom(
        id=DEV_FIXTURE_SHOWROOM_ID,
        tenant_id=DEV_FIXTURE_TENANT_ID,
        code="DEMO-JKT",
        name="VelX Fiksi Motors - Development Showroom",
        brand_name="VelX Fiksi Motors",
        address="Jl. Contoh No. 1, Jakarta (fictional)",
        timezone="Asia/Jakarta",
    ),
    cars=(
        DevelopmentCar(
            variant_id=DEV_FIXTURE_VARIANT_ID,
            tenant_id=DEV_FIXTURE_TENANT_ID,
            model_code="AURORA-E2",
            model_name="Aurora E2",
            variant_name="Cityline EV",
            model_year=2026,
            body_type="hatchback",
        ),
    ),
    prices=(
        DevelopmentPrice(
            variant_id=DEV_FIXTURE_VARIANT_ID,
            branch_id=DEV_FIXTURE_BRANCH_ID,
            amount=Decimal("425000000.00"),
            currency="IDR",
            availability="available",
        ),
    ),
)

# Short alias for seed and local-tool callers.
DEV_FIXTURES = DEVELOPMENT_FIXTURES


def get_development_fixtures(settings: Settings | None = None) -> DevelopmentFixtures:
    """Return fixtures only when the explicit local/test mode is active."""

    active_settings = settings or get_settings()
    if not active_settings.is_local:
        raise RuntimeError(
            "Development fixtures are disabled outside development and test environments"
        )
    return DEVELOPMENT_FIXTURES
