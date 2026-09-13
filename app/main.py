"""FastAPI application entry point for the VelX backend."""

from fastapi import FastAPI

from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="VelX API",
    version=settings.app_version,
    description=f"{settings.showroom_name} API.",
)


@app.get("/health/live", tags=["health"])
async def health_live() -> dict[str, str]:
    """Report that the API process is running."""

    return {"status": "ok", "service": "velx-api"}


@app.get("/health/ready", tags=["health"])
async def health_ready() -> dict[str, str]:
    """Report that the foundation service is ready for local traffic."""

    return {"status": "ok", "service": "velx-api"}
