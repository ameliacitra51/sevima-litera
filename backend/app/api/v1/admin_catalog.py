"""Administrator catalog management endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, selectinload

from app.core.dependencies import get_current_admin_user
from app.core.exceptions import ConflictException, NotFoundException
from app.db.deps import get_db
from app.models.course import Category, Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import User
from app.schemas.admin_catalog import (
    AdminCourseListResponse,
    CategoryCreate,
    CategoryListResponse,
    CategoryUpdate,
    CourseCreate,
    CourseUpdate,
    DeleteResponse,
    LessonCreate,
    LessonUpdate,
    ModuleCreate,
    ModuleUpdate,
)
from app.schemas.course import CategorySummary, CourseDetail, CourseListItem, LessonSummary, ModuleSummary

router = APIRouter(
    prefix="/admin",
    tags=["Admin Catalog"],
    dependencies=[Depends(get_current_admin_user)],
)


def _course_query(course_id: uuid.UUID):
    return (
        select(Course)
        .where(Course.id == course_id)
        .options(
            joinedload(Course.category),
            selectinload(Course.modules).selectinload(Module.lessons),
        )
    )


def _module_query(module_id: uuid.UUID):
    return select(Module).where(Module.id == module_id).options(selectinload(Module.lessons))


def _lesson_query(lesson_id: uuid.UUID):
    return select(Lesson).where(Lesson.id == lesson_id)


def _commit_or_conflict(db: Session, message: str) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictException(message)


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(db: Session = Depends(get_db)) -> CategoryListResponse:
    categories = db.scalars(select(Category).order_by(Category.order_index, Category.name)).all()
    return CategoryListResponse(items=[CategorySummary.model_validate(item) for item in categories])


@router.post("/categories", response_model=CategorySummary, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> CategorySummary:
    category = Category(**payload.model_dump())
    db.add(category)
    _commit_or_conflict(db, "Category name or slug is already in use")
    db.refresh(category)
    return CategorySummary.model_validate(category)


@router.patch("/categories/{category_id}", response_model=CategorySummary)
def update_category(category_id: uuid.UUID, payload: CategoryUpdate, db: Session = Depends(get_db)) -> CategorySummary:
    category = db.get(Category, category_id)
    if category is None:
        raise NotFoundException("Category not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    _commit_or_conflict(db, "Category name or slug is already in use")
    db.refresh(category)
    return CategorySummary.model_validate(category)


@router.get("/courses", response_model=AdminCourseListResponse)
def list_admin_courses(db: Session = Depends(get_db)) -> AdminCourseListResponse:
    courses = db.scalars(select(Course).options(joinedload(Course.category)).order_by(Course.updated_at.desc())).all()
    return AdminCourseListResponse(
        items=[CourseListItem.model_validate(course) for course in courses],
        total=len(courses),
    )


@router.post("/courses", response_model=CourseDetail, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> CourseDetail:
    category = db.get(Category, payload.category_id)
    if category is None:
        raise NotFoundException("Category not found")
    course = Course(**payload.model_dump(), creator_id=current_admin.id)
    db.add(course)
    _commit_or_conflict(db, "Course slug is already in use")
    db.refresh(course)
    course = db.scalar(_course_query(course.id))
    return CourseDetail.model_validate(course)


@router.get("/courses/{course_id}", response_model=CourseDetail)
def get_admin_course(course_id: uuid.UUID, db: Session = Depends(get_db)) -> CourseDetail:
    """Return a course including draft content for the admin workspace."""
    course = db.scalar(_course_query(course_id))
    if course is None:
        raise NotFoundException("Course not found")
    return CourseDetail.model_validate(course)


@router.patch("/courses/{course_id}", response_model=CourseDetail)
def update_course(
    course_id: uuid.UUID,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
) -> CourseDetail:
    course = db.scalar(_course_query(course_id))
    if course is None:
        raise NotFoundException("Course not found")
    values = payload.model_dump(exclude_unset=True)
    if "category_id" in values:
        if db.get(Category, values["category_id"]) is None:
            raise NotFoundException("Category not found")
    for key, value in values.items():
        setattr(course, key, value)
    _commit_or_conflict(db, "Course slug is already in use")
    course = db.scalar(_course_query(course_id))
    return CourseDetail.model_validate(course)


@router.delete("/courses/{course_id}", response_model=DeleteResponse)
def delete_course(course_id: uuid.UUID, db: Session = Depends(get_db)) -> DeleteResponse:
    course = db.get(Course, course_id)
    if course is None:
        raise NotFoundException("Course not found")
    db.delete(course)
    db.commit()
    return DeleteResponse(id=course_id, message="Course deleted successfully")


@router.post("/courses/{course_id}/modules", response_model=ModuleSummary, status_code=status.HTTP_201_CREATED)
def create_module(course_id: uuid.UUID, payload: ModuleCreate, db: Session = Depends(get_db)) -> ModuleSummary:
    if db.get(Course, course_id) is None:
        raise NotFoundException("Course not found")
    module = Module(course_id=course_id, **payload.model_dump())
    db.add(module)
    _commit_or_conflict(db, "Module order is already used in this course")
    db.refresh(module)
    module = db.scalar(_module_query(module.id))
    return ModuleSummary.model_validate(module)


@router.patch("/modules/{module_id}", response_model=ModuleSummary)
def update_module(module_id: uuid.UUID, payload: ModuleUpdate, db: Session = Depends(get_db)) -> ModuleSummary:
    module = db.scalar(_module_query(module_id))
    if module is None:
        raise NotFoundException("Module not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(module, key, value)
    _commit_or_conflict(db, "Module order is already used in this course")
    module = db.scalar(_module_query(module_id))
    return ModuleSummary.model_validate(module)


@router.delete("/modules/{module_id}", response_model=DeleteResponse)
def delete_module(module_id: uuid.UUID, db: Session = Depends(get_db)) -> DeleteResponse:
    module = db.get(Module, module_id)
    if module is None:
        raise NotFoundException("Module not found")
    db.delete(module)
    db.commit()
    return DeleteResponse(id=module_id, message="Module deleted successfully")


@router.post("/modules/{module_id}/lessons", response_model=LessonSummary, status_code=status.HTTP_201_CREATED)
def create_lesson(module_id: uuid.UUID, payload: LessonCreate, db: Session = Depends(get_db)) -> LessonSummary:
    if db.get(Module, module_id) is None:
        raise NotFoundException("Module not found")
    lesson = Lesson(module_id=module_id, **payload.model_dump())
    db.add(lesson)
    _commit_or_conflict(db, "Lesson slug or order is already used in this module")
    db.refresh(lesson)
    return LessonSummary.model_validate(lesson)


@router.patch("/lessons/{lesson_id}", response_model=LessonSummary)
def update_lesson(lesson_id: uuid.UUID, payload: LessonUpdate, db: Session = Depends(get_db)) -> LessonSummary:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise NotFoundException("Lesson not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(lesson, key, value)
    _commit_or_conflict(db, "Lesson slug or order is already used in this module")
    db.refresh(lesson)
    return LessonSummary.model_validate(lesson)


@router.delete("/lessons/{lesson_id}", response_model=DeleteResponse)
def delete_lesson(lesson_id: uuid.UUID, db: Session = Depends(get_db)) -> DeleteResponse:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise NotFoundException("Lesson not found")
    db.delete(lesson)
    db.commit()
    return DeleteResponse(id=lesson_id, message="Lesson deleted successfully")
