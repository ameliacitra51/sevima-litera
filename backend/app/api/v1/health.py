from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.db.deps import get_db
from app.schemas.health import DatabaseHealthCheck, HealthCheck

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


@router.get(
    "/health/db",
    response_model=DatabaseHealthCheck,
    summary="Database Health Check",
    tags=["Health"],
)
def db_health_check(db: Session = Depends(get_db)) -> DatabaseHealthCheck:
    """Check live PostgreSQL connectivity by executing a lightweight SELECT 1.

    Always returns HTTP 200 — the `status` field indicates actual DB health:
    - ``"ok"``          — database is reachable and responding.
    - ``"unavailable"`` — connection failed; `detail` contains the error.

    This endpoint deliberately never raises HTTP 5xx so that monitoring
    infrastructure can always read the status payload.
    """
    # Build a sanitised URL prefix for display (strip user/password)
    raw_url: str = settings.DATABASE_URL
    url_prefix = raw_url.split("@")[-1] if "@" in raw_url else raw_url.split("://")[0]

    try:
        db.execute(text("SELECT 1"))
        return DatabaseHealthCheck(
            status="ok",
            database_url_prefix=url_prefix,
            detail="PostgreSQL is reachable. SELECT 1 succeeded.",
            timestamp=datetime.now(timezone.utc),
        )
    except OperationalError as exc:
        return DatabaseHealthCheck(
            status="unavailable",
            database_url_prefix=url_prefix,
            detail=f"OperationalError — cannot connect to PostgreSQL: {exc.orig}",
            timestamp=datetime.now(timezone.utc),
        )
    except SQLAlchemyError as exc:
        return DatabaseHealthCheck(
            status="unavailable",
            database_url_prefix=url_prefix,
            detail=f"SQLAlchemyError: {exc}",
            timestamp=datetime.now(timezone.utc),
        )

