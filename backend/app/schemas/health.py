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
