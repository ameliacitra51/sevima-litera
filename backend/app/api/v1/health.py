from datetime import datetime, timezone
from fastapi import APIRouter
from app.config import settings
from app.schemas.health import HealthCheck

router = APIRouter()


@router.get("/health", response_model=HealthCheck, summary="Health Check")
async def health_check() -> HealthCheck:
    """Return backend health status, metadata, and current UTC timestamp."""
    return HealthCheck(
        status="ok",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc),
    )
