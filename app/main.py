"""FastAPI application entry point for the VelX backend."""

from fastapi import FastAPI

app = FastAPI(
    title="VelX API",
    version="0.1.0",
    description="Local foundation API for the VelX showroom chatbot.",
)


@app.get("/health/live", tags=["health"])
async def health_live() -> dict[str, str]:
    """Report that the API process is running."""

    return {"status": "ok", "service": "velx-api"}


@app.get("/health/ready", tags=["health"])
async def health_ready() -> dict[str, str]:
    """Report that the foundation service is ready for local traffic."""

    return {"status": "ok", "service": "velx-api"}
