"""Request and response schemas for administrator catalog management."""

from __future__ import annotations

import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.course import CourseLevel, CourseStatus
from app.schemas.course import CategorySummary, CourseDetail, CourseListItem, ModuleSummary
from app.schemas.lesson import LessonDetail


class CategoryCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    slug: Annotated[str, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=100)]
    description: str | None = None
    order_index: Annotated[int, Field(ge=0)] = 0


class CategoryUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=2, max_length=100)] = None
    slug: Annotated[str | None, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=100)] = None
    description: str | None = None
    order_index: Annotated[int | None, Field(ge=0)] = None


class CategoryListResponse(BaseModel):
    items: list[CategorySummary]


class CourseCreate(BaseModel):
    category_id: uuid.UUID
    title: Annotated[str, Field(min_length=2, max_length=200)]
    slug: Annotated[str, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=200)]
    description: Annotated[str, Field(min_length=10)]
    thumbnail_url: str | None = None
    level: CourseLevel = CourseLevel.BEGINNER
    status: CourseStatus = CourseStatus.DRAFT


class CourseUpdate(BaseModel):
    category_id: uuid.UUID | None = None
    title: Annotated[str | None, Field(min_length=2, max_length=200)] = None
    slug: Annotated[str | None, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=200)] = None
    description: Annotated[str | None, Field(min_length=10)] = None
    thumbnail_url: str | None = None
    level: CourseLevel | None = None
    status: CourseStatus | None = None


class AdminCourseListResponse(BaseModel):
    items: list[CourseListItem]
    total: int


class ModuleCreate(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=200)]
    description: str | None = None
    order_index: Annotated[int, Field(ge=1)]


class ModuleUpdate(BaseModel):
    title: Annotated[str | None, Field(min_length=2, max_length=200)] = None
    description: str | None = None
    order_index: Annotated[int | None, Field(ge=1)] = None


class LessonCreate(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=200)]
    slug: Annotated[str, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=200)]
    content: Annotated[str, Field(min_length=1)]
    order_index: Annotated[int, Field(ge=1)]
    duration_minutes: Annotated[int, Field(ge=1, le=600)] = 5
    is_published: bool = False


class LessonUpdate(BaseModel):
    title: Annotated[str | None, Field(min_length=2, max_length=200)] = None
    slug: Annotated[str | None, Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=200)] = None
    content: Annotated[str | None, Field(min_length=1)] = None
    order_index: Annotated[int | None, Field(ge=1)] = None
    duration_minutes: Annotated[int | None, Field(ge=1, le=600)] = None
    is_published: bool | None = None


class DeleteResponse(BaseModel):
    id: uuid.UUID
    message: str
