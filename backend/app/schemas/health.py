from datetime import datetime, timezone
from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    status: str = Field(default="ok", description="Current service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Current environment (development, staging, production)")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of the health check"
    )


class DatabaseHealthCheck(BaseModel):
    """Response model for the GET /health/db endpoint (Phase 3)."""

    status: str = Field(
        ...,
        description="'ok' when the database is reachable, 'unavailable' otherwise.",
    )
    database_url_prefix: str = Field(
        ...,
        description="Sanitized driver prefix of DATABASE_URL (no credentials).",
    )
    detail: str = Field(
        ...,
        description="Human-readable connectivity result or error summary.",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of this health check.",
    )
