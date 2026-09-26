"""Public response schemas for lesson endpoints."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.course import CourseListItem


class LessonDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    slug: str
    content: str
    order_index: int
    duration_minutes: int
    is_published: bool
    module_id: uuid.UUID
    course: CourseListItem

