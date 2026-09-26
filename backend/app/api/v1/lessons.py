"""Public lesson content endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import NotFoundException
from app.db.deps import get_db
from app.models import Course, CourseStatus, Lesson, Module
from app.schemas.lesson import LessonDetail

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("/{lesson_id}", response_model=LessonDetail, summary="Get lesson detail")
def get_lesson(lesson_id: uuid.UUID, db: Session = Depends(get_db)) -> LessonDetail:
    """Return published lesson content with its parent course context."""
    statement = (
        select(Lesson)
        .join(Lesson.module)
        .join(Module.course)
        .where(
            Lesson.id == lesson_id,
            Lesson.is_published.is_(True),
            Course.status == CourseStatus.PUBLISHED,
        )
        .options(
            selectinload(Lesson.module)
            .selectinload(Module.course)
            .selectinload(Course.category)
        )
    )
    lesson = db.scalar(statement)
    if lesson is None:
        raise NotFoundException(f"Published lesson '{lesson_id}' was not found")

    return LessonDetail(
        id=lesson.id,
        title=lesson.title,
        slug=lesson.slug,
        content=lesson.content,
        order_index=lesson.order_index,
        duration_minutes=lesson.duration_minutes,
        is_published=lesson.is_published,
        module_id=lesson.module_id,
        course=lesson.module.course,
    )
