"""Unit tests for User authentication flows without a live database."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import jwt
import pytest

from app.api.v1.auth import login, me, register
from app.config import settings
from app.core.dependencies import get_current_user
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest


class _FakeSession:
    def __init__(self, user=None):
        self.user = user
        self.added = None
        self.rolled_back = False

    def scalar(self, _statement):
        return self.user

    def add(self, value):
        self.added = value

    def commit(self):
        if self.added is not None:
            self.user = self.added

    def refresh(self, value):
        value.id = value.id or uuid.uuid4()
        value.created_at = datetime.now(timezone.utc)
        value.updated_at = value.created_at

    def rollback(self):
        self.rolled_back = True


def _user(password: str = "SecurePassword123!") -> User:
    now = datetime.now(timezone.utc)
    return User(
        id=uuid.uuid4(),
        email="student@example.com",
        username="student_one",
        full_name="Student One",
        hashed_password=hash_password(password),
        role=UserRole.STUDENT,
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def test_password_is_argon2_hash_and_round_trips():
    hashed = hash_password("SecurePassword123!")
    assert hashed.startswith("$argon2")
    assert verify_password("SecurePassword123!", hashed)
    assert not verify_password("wrong-password", hashed)


def test_register_creates_student_without_exposing_password():
    response = register(
        RegisterRequest(
            email="student@example.com",
            username="student_one",
            full_name="Student One",
            password="SecurePassword123!",
        ),
        _FakeSession(),
    )
    assert response.email == "student@example.com"
    assert response.role == UserRole.STUDENT
    assert not hasattr(response, "password")


def test_register_rejects_duplicate_email():
    with pytest.raises(ConflictException) as error:
        register(
            RegisterRequest(
                email="student@example.com",
                username="other_user",
                full_name="Student One",
                password="SecurePassword123!",
            ),
            _FakeSession(_user()),
        )
    assert error.value.status_code == 409
    assert error.value.error_code == "RESOURCE_CONFLICT"


def test_login_returns_bearer_token_and_user():
    user = _user()
    response = login(
        LoginRequest(email=user.email, password="SecurePassword123!"),
        _FakeSession(user),
    )
    assert response.token_type == "bearer"
    assert response.user.id == user.id
    payload = jwt.decode(
        response.access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    assert payload["sub"] == str(user.id)


def test_login_rejects_invalid_password():
    with pytest.raises(UnauthorizedException) as error:
        login(
            LoginRequest(email="student@example.com", password="wrong"),
            _FakeSession(_user()),
        )
    assert error.value.status_code == 401


def test_current_user_dependency_rejects_invalid_token():
    with pytest.raises(UnauthorizedException):
        get_current_user("not-a-jwt", _FakeSession())


def test_me_returns_safe_user_profile():
    user = _user()
    response = me(user)
    assert response.username == user.username
    assert not hasattr(response, "hashed_password")
