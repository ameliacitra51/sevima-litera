"""Unit tests for the Phase 3 course and lesson database foundation."""

from app.db.base import Base
from app.models import Category, Course, CourseLevel, CourseStatus, Lesson, Module


def test_catalog_tables_are_registered_in_metadata():
    assert {"categories", "courses", "modules", "lessons"}.issubset(
        Base.metadata.tables
    )


def test_catalog_relationships_are_configured():
    assert Category.courses.property.back_populates == "category"
    assert Course.category.property.back_populates == "courses"
    assert Course.modules.property.back_populates == "course"
    assert Module.course.property.back_populates == "modules"
    assert Module.lessons.property.back_populates == "module"
    assert Lesson.module.property.back_populates == "lessons"


def test_course_defaults_and_enums_are_defined():
    course = Course(
        category_id="00000000-0000-0000-0000-000000000001",
        title="Digital Safety",
        slug="digital-safety",
        description="Learn the basics of digital safety.",
    )
    assert course.level is None  # SQLAlchemy applies defaults during INSERT.
    assert CourseLevel.BEGINNER.value == "BEGINNER"
    assert CourseStatus.DRAFT.value == "DRAFT"


def test_ordering_and_slug_constraints_exist():
    module_constraints = {
        constraint.name for constraint in Module.__table__.constraints
    }
    lesson_constraints = {
        constraint.name for constraint in Lesson.__table__.constraints
    }
    assert "uq_modules_course_order" in module_constraints
    assert "uq_lessons_module_slug" in lesson_constraints
    assert "uq_lessons_module_order" in lesson_constraints
