"""Public course catalogue endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.v1.pagination import total_pages
from app.core.exceptions import NotFoundException
from app.db.deps import get_db
from app.models import Category, Course, CourseLevel, CourseStatus, Module
from app.schemas.course import (
    CategorySummary,
    CourseDetail,
    CourseListItem,
    CourseListResponse,
    LessonSummary,
    ModuleSummary,
)

router = APIRouter(prefix="/courses", tags=["Courses"])


PageQuery = Annotated[int, Query(ge=1, description="1-based page number")]
PageSizeQuery = Annotated[int, Query(ge=1, le=100, description="Items per page")]
CategoryQuery = Annotated[str | None, Query(min_length=1, max_length=100)]
SearchQuery = Annotated[str | None, Query(min_length=1, max_length=100)]


def _course_list_item(course: Course) -> CourseListItem:
    return CourseListItem.model_validate(course)


def _course_detail(course: Course) -> CourseDetail:
    """Build a public course detail and hide unpublished lessons."""
    data = _course_list_item(course).model_dump()
    data["modules"] = [
        ModuleSummary(
            id=module.id,
            title=module.title,
            description=module.description,
            order_index=module.order_index,
            lessons=[
                LessonSummary.model_validate(lesson)
                for lesson in module.lessons
                if lesson.is_published
            ],
        )
        for module in course.modules
    ]
    return CourseDetail.model_validate(data)


@router.get("", response_model=CourseListResponse, summary="List published courses")
def list_courses(
    db: Session = Depends(get_db),
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
    category: CategoryQuery = None,
    level: CourseLevel | None = None,
    search: SearchQuery = None,
) -> CourseListResponse:
    """Return published courses with optional category, level, and title search."""
    filters = [Course.status == CourseStatus.PUBLISHED]
    if category:
        filters.append(Category.slug == category.strip().lower())
    if level:
        filters.append(Course.level == level)
    if search:
        filters.append(Course.title.ilike(f"%{search.strip()}%"))

    count_statement = select(func.count(Course.id)).join(Course.category).where(*filters)
    total = db.scalar(count_statement) or 0

    statement = (
        select(Course)
        .join(Course.category)
        .where(*filters)
        .options(selectinload(Course.category))
        .order_by(Course.created_at.desc(), Course.title.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    courses = db.scalars(statement).all()

    return CourseListResponse(
        items=[_course_list_item(course) for course in courses],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages(total, page_size),
    )


@router.get("/{slug}", response_model=CourseDetail, summary="Get course detail")
def get_course(slug: str, db: Session = Depends(get_db)) -> CourseDetail:
    """Return a published course with its ordered modules and published lessons."""
    statement = (
        select(Course)
        .where(Course.slug == slug, Course.status == CourseStatus.PUBLISHED)
        .options(
            selectinload(Course.category),
            selectinload(Course.modules).selectinload(Module.lessons),
        )
    )
    course = db.scalar(statement)
    if course is None:
        raise NotFoundException(f"Published course with slug '{slug}' was not found")
    return _course_detail(course)
