"""Reusable database and authenticated-user dependencies."""

from __future__ import annotations

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.db.deps import get_db
from app.models.user import User, UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve and validate the user represented by a bearer JWT."""
    try:
        user_id = decode_access_token(token)
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise UnauthorizedException()

    user = db.scalar(select(User).where(User.id == user_id))
    if user is None or not user.is_active:
        raise UnauthorizedException()
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Explicit dependency alias for routes requiring an active account."""
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Require an active authenticated account with the ADMIN role."""
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException("Admin privileges are required")
    return current_user
