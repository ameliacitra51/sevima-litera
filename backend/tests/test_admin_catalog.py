"""Tests for administrator catalog authorization and contracts."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.api.v1.admin_catalog import list_categories
from app.core.dependencies import get_current_admin_user
from app.core.exceptions import ForbiddenException
from app.main import app
from app.models.course import Category
from app.models.user import User, UserRole
from app.schemas.admin_catalog import CourseCreate, LessonCreate, ModuleCreate


class _FakeSession:
    def __init__(self, rows=()):
        self.rows = rows

    def scalars(self, _statement):
        class _Rows:
            def __init__(self, values):
                self.values = values

            def all(self):
                return self.values

        return _Rows(self.rows)


def _user(role: UserRole) -> User:
    now = datetime.now(timezone.utc)
    return User(
        id=uuid.uuid4(),
        email=f"{role.value.lower()}@example.com",
        username=f"{role.value.lower()}_one",
        full_name=role.value,
        hashed_password="not-used-in-this-test",
        role=role,
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def test_student_is_forbidden_from_admin_dependency():
    with pytest.raises(ForbiddenException) as error:
        get_current_admin_user(_user(UserRole.STUDENT))
    assert error.value.status_code == 403
    assert error.value.error_code == "FORBIDDEN"


def test_admin_is_allowed_by_admin_dependency():
    admin = _user(UserRole.ADMIN)
    assert get_current_admin_user(admin) is admin


def test_admin_payloads_require_valid_relationship_fields():
    category_id = uuid.uuid4()
    course = CourseCreate(
        category_id=category_id,
        title="Digital Safety",
        slug="digital-safety",
        description="Learn safe digital habits for everyday life.",
    )
    module = ModuleCreate(title="Foundations", order_index=1)
    lesson = LessonCreate(
        title="Strong passwords",
        slug="strong-passwords",
        content="# Strong passwords",
        order_index=1,
    )
    assert course.category_id == category_id
    assert module.order_index == 1
    assert lesson.duration_minutes == 5

    with pytest.raises(ValidationError):
        CourseCreate(
            category_id=category_id,
            title="Bad slug",
            slug="Bad Slug",
            description="This payload must reject invalid slug format.",
        )


def test_admin_categories_returns_category_summary():
    category = Category(id=uuid.uuid4(), name="Digital Literacy", slug="digital-literacy")
    response = list_categories(_FakeSession(rows=(category,)))
    assert response.items[0].slug == "digital-literacy"


def test_admin_routes_are_registered():
    paths = {route.path for route in app.routes}
    assert "/api/v1/admin/categories" in paths
    assert "/api/v1/admin/courses" in paths
    assert "/api/v1/admin/courses/{course_id}/modules" in paths
    assert "/api/v1/admin/modules/{module_id}/lessons" in paths
    assert "/api/v1/admin/lessons/{lesson_id}" in paths
