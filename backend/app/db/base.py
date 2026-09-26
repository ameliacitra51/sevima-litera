"""SQLAlchemy 2.x Declarative Base for all LITERA ORM models.

All ORM model classes MUST inherit from this Base so that their table
metadata is registered for Alembic autogenerate and schema creation.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Project-wide SQLAlchemy declarative base class."""
    pass
