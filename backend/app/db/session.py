"""SQLAlchemy engine and session factory.

The engine is created once at module import time using DATABASE_URL from
app.config.settings. All credentials are sourced from the .env file --
never hardcoded here.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Engine -- pool_pre_ping tests connections before reuse.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Session factory -- explicit transaction management.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
