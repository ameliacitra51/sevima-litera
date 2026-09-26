"""FastAPI dependency that provides a per-request SQLAlchemy Session.

Inject this via Depends(get_db) in any route that needs database access.
The generator pattern guarantees the session is always closed, preventing
connection leaks even when unhandled exceptions occur inside the route.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after the request."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
