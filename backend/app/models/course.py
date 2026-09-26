"""Course catalogue models for the Phase 3 database foundation."""

from __future__ import annotations

import uuid
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_model import TimestampMixin

if TYPE_CHECKING:
    from app.models.module import Module
    from app.models.user import User


class CourseLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class CourseStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(nullable=False, default=0, server_default="0")
    courses: Mapped[list[Course]] = relationship(back_populates="category", passive_deletes=True)


class Course(TimestampMixin, Base):
    __tablename__ = "courses"
    __table_args__ = (Index("ix_courses_status_level", "status", "level"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    creator_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    level: Mapped[CourseLevel] = mapped_column(SqlEnum(CourseLevel, name="course_level", native_enum=False, length=20), nullable=False, default=CourseLevel.BEGINNER, server_default=CourseLevel.BEGINNER.value)
    status: Mapped[CourseStatus] = mapped_column(SqlEnum(CourseStatus, name="course_status", native_enum=False, length=20), nullable=False, default=CourseStatus.DRAFT, server_default=CourseStatus.DRAFT.value)
    category: Mapped[Category] = relationship(back_populates="courses")
    creator: Mapped[User | None] = relationship(back_populates="created_courses")
    modules: Mapped[list[Module]] = relationship(back_populates="course", cascade="all, delete-orphan", order_by="Module.order_index")
