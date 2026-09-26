"""Phase 3 -- Database Foundation Tests.

This suite verifies:
  1. DATABASE_URL is properly configured via pydantic-settings.
  2. SQLAlchemy engine and SessionLocal factory are correctly created.
  3. The declarative Base exposes metadata.
  4. The get_db() dependency yields a valid SQLAlchemy Session instance.
  5. A real round-trip to PostgreSQL succeeds (SELECT 1).
  6. The GET /api/v1/health/db endpoint returns a well-formed response.

Tests 5 and 6 REQUIRE a running PostgreSQL instance.
If PostgreSQL is not available they WILL FAIL and state why clearly --
per project policy, database tests must not be silently skipped or faked.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.config import settings
from app.db.base import Base
from app.db.deps import get_db
from app.db.session import SessionLocal, engine
from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# 1. Configuration tests (no live DB required)
# ---------------------------------------------------------------------------


def test_database_url_is_configured():
    """DATABASE_URL must be a non-empty PostgreSQL connection string."""
    assert settings.DATABASE_URL, "DATABASE_URL must not be empty."
    assert "postgresql" in settings.DATABASE_URL.lower(), (
        f"DATABASE_URL must reference PostgreSQL. Got: {settings.DATABASE_URL!r}"
    )


def test_database_url_has_no_placeholder():
    """DATABASE_URL must not still be the literal .env.example placeholder."""
    url = settings.DATABASE_URL.lower()
    assert "example" not in url, "DATABASE_URL still contains a placeholder value."


# ---------------------------------------------------------------------------
# 2. Engine and session factory tests (no live DB required)
# ---------------------------------------------------------------------------


def test_engine_is_created():
    """SQLAlchemy engine must exist and have a PostgreSQL dialect."""
    assert engine is not None
    assert engine.dialect.name == "postgresql", (
        f"Expected postgresql dialect, got: {engine.dialect.name}"
    )


def test_session_local_factory_is_callable():
    """SessionLocal must produce a Session object (lazy -- no connection yet)."""
    db = SessionLocal()
    try:
        assert isinstance(db, Session)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# 3. Declarative Base tests (no live DB required)
# ---------------------------------------------------------------------------


def test_base_metadata_is_accessible():
    """Base.metadata must be a SQLAlchemy MetaData object."""
    from sqlalchemy import MetaData
    assert isinstance(Base.metadata, MetaData)


# ---------------------------------------------------------------------------
# 4. get_db dependency test (no live DB -- Session is lazy)
# ---------------------------------------------------------------------------


def test_get_db_dependency_yields_session():
    """get_db() generator must yield a SQLAlchemy Session instance."""
    gen = get_db()
    try:
        db = next(gen)
        assert isinstance(db, Session), f"Expected Session, got {type(db)}"
    finally:
        try:
            next(gen)
        except StopIteration:
            pass


# ---------------------------------------------------------------------------
# 5. Live database connectivity test (REQUIRES running PostgreSQL)
# ---------------------------------------------------------------------------


def test_database_connection_live():
    """Execute SELECT 1 -- FAILS if PostgreSQL is not running (by design)."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 1
    except OperationalError as exc:
        pytest.fail(
            "\n"
            "================================================================\n"
            "  PostgreSQL connectivity FAILED                                \n"
            "================================================================\n"
            f"  DATABASE_URL : {settings.DATABASE_URL}\n"
            f"  Error        : {exc}\n"
            "\n"
            "  Ensure PostgreSQL is running and DATABASE_URL in .env is     \n"
            "  correct, then re-run: pytest tests/test_database.py          \n"
            "================================================================"
        )


# ---------------------------------------------------------------------------
# 6. GET /api/v1/health/db endpoint tests
# ---------------------------------------------------------------------------


def test_db_health_endpoint_returns_200():
    """GET /api/v1/health/db must always return HTTP 200."""
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. Body: {response.text}"
    )


def test_db_health_endpoint_response_schema():
    """Response body must contain status, database_url_prefix, detail, timestamp."""
    response = client.get("/api/v1/health/db")
    data = response.json()
    assert "status" in data
    assert "database_url_prefix" in data
    assert "detail" in data
    assert "timestamp" in data
    assert data["status"] in ("ok", "unavailable"), (
        f"'status' must be 'ok' or 'unavailable', got: {data['status']!r}"
    )


def test_db_health_endpoint_credentials_not_leaked():
    """database_url_prefix must not expose the database password."""
    response = client.get("/api/v1/health/db")
    data = response.json()
    prefix = data.get("database_url_prefix", "")
    assert "postgres:" not in prefix, "database_url_prefix must not leak the password."


def test_db_health_endpoint_connected():
    """GET /api/v1/health/db must return status="ok" (REQUIRES PostgreSQL)."""
    response = client.get("/api/v1/health/db")
    data = response.json()
    if data["status"] != "ok":
        pytest.fail(
            "\n"
            "================================================================\n"
            "  /api/v1/health/db reported PostgreSQL as UNAVAILABLE         \n"
            "================================================================\n"
            f"  detail     : {data.get('detail')}\n"
            f"  url_prefix : {data.get('database_url_prefix')}\n"
            "================================================================"
        )
