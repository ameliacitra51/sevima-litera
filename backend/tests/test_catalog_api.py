"""Unit tests for public Course and Lesson API handlers."""

from __future__ import annotations

import uuid

import pytest

from app.api.v1.courses import get_course, list_courses
from app.api.v1.lessons import get_lesson
from app.core.exceptions import NotFoundException
from app.main import app
from app.models import Category, Course, CourseLevel, CourseStatus, Lesson, Module


class _ScalarRows:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _FakeSession:
    def __init__(self, *, scalar_values=(), rows=()):
        self._scalar_values = iter(scalar_values)
        self._rows = rows

    def scalar(self, _statement):
        return next(self._scalar_values)

    def scalars(self, _statement):
        return _ScalarRows(self._rows)


def _catalog_fixture():
    category = Category(
        id=uuid.uuid4(), name="Digital Literacy", slug="digital-literacy"
    )
    course = Course(
        id=uuid.uuid4(),
        category_id=category.id,
        title="Digital Safety",
        slug="digital-safety",
        description="Learn safe digital habits.",
        level=CourseLevel.BEGINNER,
        status=CourseStatus.PUBLISHED,
        category=category,
    )
    module = Module(
        id=uuid.uuid4(), course_id=course.id, title="Foundations", order_index=1
    )
    lesson = Lesson(
        id=uuid.uuid4(),
        module_id=module.id,
        title="Strong Passwords",
        slug="strong-passwords",
        content="# Strong passwords\n\nUse a password manager.",
        order_index=1,
        duration_minutes=6,
        is_published=True,
        module=module,
    )
    course.modules = [module]
    module.lessons = [lesson]
    return category, course, module, lesson


def test_course_list_returns_paginated_published_items():
    _, course, _, _ = _catalog_fixture()
    response = list_courses(
        db=_FakeSession(scalar_values=(1,), rows=(course,)),
        page=1,
        page_size=20,
    )

    assert response.total == 1
    assert response.total_pages == 1
    assert response.items[0].slug == "digital-safety"
    assert response.items[0].category.slug == "digital-literacy"


def test_course_detail_returns_ordered_modules_and_published_lessons():
    _, course, _, _ = _catalog_fixture()
    response = get_course(course.slug, _FakeSession(scalar_values=(course,)))

    assert response.slug == course.slug
    assert response.modules[0].order_index == 1
    assert response.modules[0].lessons[0].slug == "strong-passwords"


def test_lesson_detail_returns_markdown_and_course_context():
    _, course, _, lesson = _catalog_fixture()
    response = get_lesson(lesson.id, _FakeSession(scalar_values=(lesson,)))

    assert response.content.startswith("# Strong passwords")
    assert response.course.slug == course.slug
    assert response.module_id == lesson.module_id


def test_missing_course_and_lesson_raise_standard_not_found_error():
    with pytest.raises(NotFoundException) as missing_course:
        get_course("missing", _FakeSession(scalar_values=(None,)))
    assert missing_course.value.status_code == 404
    assert missing_course.value.error_code == "RESOURCE_NOT_FOUND"

    with pytest.raises(NotFoundException) as missing_lesson:
        get_lesson(uuid.uuid4(), _FakeSession(scalar_values=(None,)))
    assert missing_lesson.value.status_code == 404


def test_catalog_routes_are_registered():
    paths = {route.path for route in app.routes}
    assert "/api/v1/courses" in paths
    assert "/api/v1/courses/{slug}" in paths
    assert "/api/v1/lessons/{lesson_id}" in paths
