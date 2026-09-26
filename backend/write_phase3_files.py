"""One-shot script to write all Phase 3 backend modules with correct UTF-8 (no BOM).
Run from D:\\litera\\backend with the venv active.
"""
import pathlib

files = {}

files["app/db/base.py"] = (
    '"""SQLAlchemy 2.x Declarative Base for all LITERA ORM models.\n\n'
    "All ORM model classes MUST inherit from this Base so that their table\n"
    "metadata is registered for Alembic autogenerate and schema creation.\n"
    '"""\n\n'
    "from sqlalchemy.orm import DeclarativeBase\n\n\n"
    "class Base(DeclarativeBase):\n"
    '    """Project-wide SQLAlchemy declarative base class."""\n'
    "    pass\n"
)

files["app/db/session.py"] = (
    '"""SQLAlchemy engine and session factory.\n\n'
    "The engine is created once at module import time using DATABASE_URL from\n"
    "app.config.settings. All credentials are sourced from the .env file --\n"
    "never hardcoded here.\n"
    '"""\n\n'
    "from sqlalchemy import create_engine\n"
    "from sqlalchemy.orm import sessionmaker\n\n"
    "from app.config import settings\n\n"
    "# Engine -- pool_pre_ping tests connections before reuse.\n"
    "engine = create_engine(\n"
    "    settings.DATABASE_URL,\n"
    "    pool_pre_ping=True,\n"
    "    echo=settings.DEBUG,\n"
    ")\n\n"
    "# Session factory -- explicit transaction management.\n"
    "SessionLocal = sessionmaker(\n"
    "    autocommit=False,\n"
    "    autoflush=False,\n"
    "    bind=engine,\n"
    ")\n"
)

files["app/db/deps.py"] = (
    '"""FastAPI dependency that provides a per-request SQLAlchemy Session.\n\n'
    "Inject this via Depends(get_db) in any route that needs database access.\n"
    "The generator pattern guarantees the session is always closed, preventing\n"
    "connection leaks even when unhandled exceptions occur inside the route.\n"
    '"""\n\n'
    "from typing import Generator\n\n"
    "from sqlalchemy.orm import Session\n\n"
    "from app.db.session import SessionLocal\n\n\n"
    "def get_db() -> Generator[Session, None, None]:\n"
    '    """Yield a database session and ensure it is closed after the request."""\n'
    "    db: Session = SessionLocal()\n"
    "    try:\n"
    "        yield db\n"
    "    finally:\n"
    "        db.close()\n"
)

files["app/models/__init__.py"] = (
    '"""LITERA Database Models.\n\n'
    "Re-exports Base and all model classes so that Alembic autogenerate\n"
    "discovers every mapped table via Base.metadata.\n"
    '"""\n\n'
    "from app.db.base import Base  # noqa: F401\n"
    "from app.models.base_model import TimestampMixin  # noqa: F401\n\n"
    '__all__ = ["Base", "TimestampMixin"]\n'
)

files["app/models/base_model.py"] = (
    '"""Shared ORM mixin classes for all LITERA models.\n\n'
    "TimestampMixin adds created_at / updated_at columns (TIMESTAMPTZ) using\n"
    "SQLAlchemy 2.x typed-mapping syntax (Mapped / mapped_column).\n"
    '"""\n\n'
    "from datetime import datetime\n"
    "from sqlalchemy import DateTime\n"
    "from sqlalchemy.orm import Mapped, mapped_column\n"
    "from sqlalchemy.sql import func\n\n\n"
    "class TimestampMixin:\n"
    '    """Adds server-side created_at and updated_at TIMESTAMPTZ columns.\n\n'
    "    Apply to any ORM model that needs automatic timestamp tracking:\n\n"
    "        class MyModel(Base, TimestampMixin):\n"
    '            __tablename__ = "my_table"\n'
    "            ...\n"
    '    """\n\n'
    "    created_at: Mapped[datetime] = mapped_column(\n"
    "        DateTime(timezone=True),\n"
    "        server_default=func.now(),\n"
    "        nullable=False,\n"
    "    )\n"
    "    updated_at: Mapped[datetime] = mapped_column(\n"
    "        DateTime(timezone=True),\n"
    "        server_default=func.now(),\n"
    "        onupdate=func.now(),\n"
    "        nullable=False,\n"
    "    )\n"
)

# alembic/env.py (long -- built line-by-line)
env_lines = [
    '"""Alembic environment configuration for LITERA.\n\n',
    "This module is invoked by Alembic whenever a migration command is run.\n\n",
    "Key responsibilities:\n",
    "  - Override sqlalchemy.url with the value from pydantic-settings so that\n",
    "    credentials come from the .env file, never from alembic.ini.\n",
    "  - Import all ORM models via app.models so Base.metadata is fully\n",
    "    populated before autogenerate compares it to the live schema.\n",
    "  - Run migrations in offline mode (SQL output) or online mode (live DB).\n",
    '"""\n\n',
    "import sys\n",
    "import os\n\n",
    "# Ensure backend/ is on sys.path so 'from app.xxx import ...' works.\n",
    "# __file__ resolves to backend/alembic/env.py; two dirname() calls -> backend/.\n",
    "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n\n",
    "from logging.config import fileConfig\n\n",
    "from sqlalchemy import engine_from_config, pool\n",
    "from alembic import context\n\n",
    "# Load pydantic-settings (reads .env automatically).\n",
    "from app.config import settings\n\n",
    "# Import ALL ORM models so their tables register on Base.metadata.\n",
    "import app.models  # noqa: F401\n",
    "from app.db.base import Base\n\n",
    "# Alembic Config object.\n",
    "config = context.config\n\n",
    "# Override sqlalchemy.url -- real credentials come from .env, not alembic.ini.\n",
    'config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)\n\n',
    "if config.config_file_name is not None:\n",
    "    fileConfig(config.config_file_name)\n\n",
    "target_metadata = Base.metadata\n\n\n",
    "def run_migrations_offline() -> None:\n",
    '    """Run migrations in offline mode (emit SQL without a live connection)."""\n',
    '    url = config.get_main_option("sqlalchemy.url")\n',
    "    context.configure(\n",
    "        url=url,\n",
    "        target_metadata=target_metadata,\n",
    "        literal_binds=True,\n",
    '        dialect_opts={"paramstyle": "named"},\n',
    "        compare_type=True,\n",
    "        compare_server_default=True,\n",
    "    )\n",
    "    with context.begin_transaction():\n",
    "        context.run_migrations()\n\n\n",
    "def run_migrations_online() -> None:\n",
    '    """Run migrations in online mode (connect to live database)."""\n',
    "    connectable = engine_from_config(\n",
    "        config.get_section(config.config_ini_section, {}),\n",
    '        prefix="sqlalchemy.",\n',
    "        poolclass=pool.NullPool,\n",
    "    )\n",
    "    with connectable.connect() as connection:\n",
    "        context.configure(\n",
    "            connection=connection,\n",
    "            target_metadata=target_metadata,\n",
    "            compare_type=True,\n",
    "            compare_server_default=True,\n",
    "        )\n",
    "        with context.begin_transaction():\n",
    "            context.run_migrations()\n\n\n",
    "if context.is_offline_mode():\n",
    "    run_migrations_offline()\n",
    "else:\n",
    "    run_migrations_online()\n",
]
files["alembic/env.py"] = "".join(env_lines)

# tests/test_database.py
test_lines = [
    '"""Phase 3 -- Database Foundation Tests.\n\n',
    "This suite verifies:\n",
    "  1. DATABASE_URL is properly configured via pydantic-settings.\n",
    "  2. SQLAlchemy engine and SessionLocal factory are correctly created.\n",
    "  3. The declarative Base exposes metadata.\n",
    "  4. The get_db() dependency yields a valid SQLAlchemy Session instance.\n",
    "  5. A real round-trip to PostgreSQL succeeds (SELECT 1).\n",
    "  6. The GET /api/v1/health/db endpoint returns a well-formed response.\n\n",
    "Tests 5 and 6 REQUIRE a running PostgreSQL instance.\n",
    "If PostgreSQL is not available they WILL FAIL and state why clearly --\n",
    "per project policy, database tests must not be silently skipped or faked.\n",
    '"""\n\n',
    "import pytest\n",
    "from fastapi.testclient import TestClient\n",
    "from sqlalchemy import text\n",
    "from sqlalchemy.exc import OperationalError\n",
    "from sqlalchemy.orm import Session\n\n",
    "from app.config import settings\n",
    "from app.db.base import Base\n",
    "from app.db.deps import get_db\n",
    "from app.db.session import SessionLocal, engine\n",
    "from app.main import app\n\n",
    "client = TestClient(app)\n\n\n",
    "# ---------------------------------------------------------------------------\n",
    "# 1. Configuration tests (no live DB required)\n",
    "# ---------------------------------------------------------------------------\n\n\n",
    "def test_database_url_is_configured():\n",
    '    """DATABASE_URL must be a non-empty PostgreSQL connection string."""\n',
    '    assert settings.DATABASE_URL, "DATABASE_URL must not be empty."\n',
    "    assert \"postgresql\" in settings.DATABASE_URL.lower(), (\n",
    "        f\"DATABASE_URL must reference PostgreSQL. Got: {settings.DATABASE_URL!r}\"\n",
    "    )\n\n\n",
    "def test_database_url_has_no_placeholder():\n",
    '    """DATABASE_URL must not still be the literal .env.example placeholder."""\n',
    "    url = settings.DATABASE_URL.lower()\n",
    "    assert \"example\" not in url, \"DATABASE_URL still contains a placeholder value.\"\n\n\n",
    "# ---------------------------------------------------------------------------\n",
    "# 2. Engine and session factory tests (no live DB required)\n",
    "# ---------------------------------------------------------------------------\n\n\n",
    "def test_engine_is_created():\n",
    '    """SQLAlchemy engine must exist and have a PostgreSQL dialect."""\n',
    "    assert engine is not None\n",
    "    assert engine.dialect.name == \"postgresql\", (\n",
    "        f\"Expected postgresql dialect, got: {engine.dialect.name}\"\n",
    "    )\n\n\n",
    "def test_session_local_factory_is_callable():\n",
    '    """SessionLocal must produce a Session object (lazy -- no connection yet)."""\n',
    "    db = SessionLocal()\n",
    "    try:\n",
    "        assert isinstance(db, Session)\n",
    "    finally:\n",
    "        db.close()\n\n\n",
    "# ---------------------------------------------------------------------------\n",
    "# 3. Declarative Base tests (no live DB required)\n",
    "# ---------------------------------------------------------------------------\n\n\n",
    "def test_base_metadata_is_accessible():\n",
    '    """Base.metadata must be a SQLAlchemy MetaData object."""\n',
    "    from sqlalchemy import MetaData\n",
    "    assert isinstance(Base.metadata, MetaData)\n\n\n",
    "# ---------------------------------------------------------------------------\n",
    "# 4. get_db dependency test (no live DB -- Session is lazy)\n",
    "# ---------------------------------------------------------------------------\n\n\n",
    "def test_get_db_dependency_yields_session():\n",
    '    """get_db() generator must yield a SQLAlchemy Session instance."""\n',
    "    gen = get_db()\n",
    "    try:\n",
    "        db = next(gen)\n",
    "        assert isinstance(db, Session), f\"Expected Session, got {type(db)}\"\n",
    "    finally:\n",
    "        try:\n",
    "            next(gen)\n",
    "        except StopIteration:\n",
    "            pass\n\n\n",
    "# ---------------------------------------------------------------------------\n",
    "# 5. Live database connectivity test (REQUIRES running PostgreSQL)\n",
    "# ---------------------------------------------------------------------------\n\n\n",
    "def test_database_connection_live():\n",
    '    """Execute SELECT 1 -- FAILS if PostgreSQL is not running (by design)."""\n',
    "    try:\n",
    "        with engine.connect() as conn:\n",
    "            result = conn.execute(text(\"SELECT 1\"))\n",
    "            row = result.fetchone()\n",
    "            assert row is not None\n",
    "            assert row[0] == 1\n",
    "    except OperationalError as exc:\n",
    "        pytest.fail(\n",
    "            \"\\n\"\n",
    "            \"================================================================\\n\"\n",
    "            \"  PostgreSQL connectivity FAILED                                \\n\"\n",
    "            \"================================================================\\n\"\n",
    "            f\"  DATABASE_URL : {settings.DATABASE_URL}\\n\"\n",
    "            f\"  Error        : {exc}\\n\"\n",
    "            \"\\n\"\n",
    "            \"  Ensure PostgreSQL is running and DATABASE_URL in .env is     \\n\"\n",
    "            \"  correct, then re-run: pytest tests/test_database.py          \\n\"\n",
    "            \"================================================================\"\n",
    "        )\n\n\n",
    "# ---------------------------------------------------------------------------\n",
    "# 6. GET /api/v1/health/db endpoint tests\n",
    "# ---------------------------------------------------------------------------\n\n\n",
    "def test_db_health_endpoint_returns_200():\n",
    '    """GET /api/v1/health/db must always return HTTP 200."""\n',
    "    response = client.get(\"/api/v1/health/db\")\n",
    "    assert response.status_code == 200, (\n",
    "        f\"Expected 200, got {response.status_code}. Body: {response.text}\"\n",
    "    )\n\n\n",
    "def test_db_health_endpoint_response_schema():\n",
    '    """Response body must contain status, database_url_prefix, detail, timestamp."""\n',
    "    response = client.get(\"/api/v1/health/db\")\n",
    "    data = response.json()\n",
    "    assert \"status\" in data\n",
    "    assert \"database_url_prefix\" in data\n",
    "    assert \"detail\" in data\n",
    "    assert \"timestamp\" in data\n",
    "    assert data[\"status\"] in (\"ok\", \"unavailable\"), (\n",
    "        f\"'status' must be 'ok' or 'unavailable', got: {data['status']!r}\"\n",
    "    )\n\n\n",
    "def test_db_health_endpoint_credentials_not_leaked():\n",
    '    """database_url_prefix must not expose the database password."""\n',
    "    response = client.get(\"/api/v1/health/db\")\n",
    "    data = response.json()\n",
    "    prefix = data.get(\"database_url_prefix\", \"\")\n",
    "    assert \"postgres:\" not in prefix, \"database_url_prefix must not leak the password.\"\n\n\n",
    "def test_db_health_endpoint_connected():\n",
    '    """GET /api/v1/health/db must return status="ok" (REQUIRES PostgreSQL)."""\n',
    "    response = client.get(\"/api/v1/health/db\")\n",
    "    data = response.json()\n",
    "    if data[\"status\"] != \"ok\":\n",
    "        pytest.fail(\n",
    "            \"\\n\"\n",
    "            \"================================================================\\n\"\n",
    "            \"  /api/v1/health/db reported PostgreSQL as UNAVAILABLE         \\n\"\n",
    "            \"================================================================\\n\"\n",
    "            f\"  detail     : {data.get('detail')}\\n\"\n",
    "            f\"  url_prefix : {data.get('database_url_prefix')}\\n\"\n",
    "            \"================================================================\"\n",
    "        )\n",
]
files["tests/test_database.py"] = "".join(test_lines)

for path, content in files.items():
    p = pathlib.Path(path)
    p.write_text(content, encoding="utf-8")
    print(f"Written (utf-8): {path}")

print("All files written.")
