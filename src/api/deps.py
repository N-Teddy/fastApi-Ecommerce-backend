# src/api/deps.py
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Generator
from sqlalchemy.orm import Session

from ..core.security import verify_token
from ..core.exceptions import UnauthorizedException, ForbiddenException
from ..services.user import UserService
from ..models.user import User
from ..config.database import SessionLocal


def get_db() -> Generator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login"))
) -> User:
    """Get current authenticated user"""
    payload = verify_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException("Invalid authentication token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    user_service = UserService(db)
    user = user_service.get(int(user_id))
    if not user:
        raise UnauthorizedException("User not found")

    if not user.is_active:
        raise UnauthorizedException("Inactive user")

    return user

def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Check if current user is superuser"""
    if not current_user.is_admin:
        raise ForbiddenException("Not enough permissions")
    return current_user