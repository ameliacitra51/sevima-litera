"""Alembic environment configuration for LITERA.

This module is invoked by Alembic whenever a migration command is run.

Key responsibilities:
  - Override sqlalchemy.url with the value from pydantic-settings so that
    credentials come from the .env file, never from alembic.ini.
  - Import all ORM models via app.models so Base.metadata is fully
    populated before autogenerate compares it to the live schema.
  - Run migrations in offline mode (SQL output) or online mode (live DB).
"""

import sys
import os

# Ensure backend/ is on sys.path so 'from app.xxx import ...' works.
# __file__ resolves to backend/alembic/env.py; two dirname() calls -> backend/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Load pydantic-settings (reads .env automatically).
from app.config import settings

# Import ALL ORM models so their tables register on Base.metadata.
import app.models  # noqa: F401
from app.db.base import Base

# Alembic Config object.
config = context.config

# Override sqlalchemy.url -- real credentials come from .env, not alembic.ini.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode (emit SQL without a live connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode (connect to live database)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
