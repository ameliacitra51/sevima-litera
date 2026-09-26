"""Public response schemas for course catalogue endpoints."""

from __future__ import annotations

import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.course import CourseLevel, CourseStatus


class CategorySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str


class LessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    slug: str
    order_index: int
    duration_minutes: int
    is_published: bool


class ModuleSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    order_index: int
    lessons: list[LessonSummary] = Field(default_factory=list)


class CourseListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    slug: str
    description: str
    thumbnail_url: str | None
    level: CourseLevel
    status: CourseStatus
    category: CategorySummary


class CourseDetail(CourseListItem):
    modules: list[ModuleSummary] = Field(default_factory=list)


class CourseListResponse(BaseModel):
    items: list[CourseListItem]
    total: int
    page: Annotated[int, Field(ge=1)]
    page_size: Annotated[int, Field(ge=1, le=100)]
    total_pages: int
