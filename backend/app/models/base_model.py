"""Shared ORM mixin classes for all LITERA models.

TimestampMixin adds created_at / updated_at columns (TIMESTAMPTZ) using
SQLAlchemy 2.x typed-mapping syntax (Mapped / mapped_column).
"""

from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class TimestampMixin:
    """Adds server-side created_at and updated_at TIMESTAMPTZ columns.

    Apply to any ORM model that needs automatic timestamp tracking:

        class MyModel(Base, TimestampMixin):
            __tablename__ = "my_table"
            ...
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
