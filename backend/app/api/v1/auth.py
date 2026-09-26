"""Authentication endpoints for user registration and JWT sessions."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_active_user
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.db.deps import get_db
from app.models.user import User, UserRole
from app.schemas.auth import (
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a student account",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    """Create a student account with a one-way Argon2 password hash."""
    email = str(payload.email).lower()
    username = payload.username.strip()
    existing = db.scalar(
        select(User).where(or_(User.email == email, User.username == username))
    )
    if existing is not None:
        if existing.email == email:
            raise ConflictException("Email is already registered")
        raise ConflictException("Username is already taken")

    user = User(
        email=email,
        username=username,
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
        role=UserRole.STUDENT,
        is_active=True,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise ConflictException("Email or username is already registered")
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse, summary="Login with email and password")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Validate credentials and issue a short-lived JWT bearer token."""
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")
    if not user.is_active:
        raise UnauthorizedException("User account is inactive")

    return TokenResponse(
        access_token=create_access_token(user.id),
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse, summary="Get current user")
def me(current_user: User = Depends(get_current_active_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=LogoutResponse, summary="Logout current user")
def logout(
    current_user: User = Depends(get_current_active_user),
) -> LogoutResponse:
    """End a stateless client session.

    JWTs are stateless; the client must discard its token. Server-side token
    revocation will be introduced only if a token blacklist is required.
    """
    return LogoutResponse(message="Logged out successfully")
