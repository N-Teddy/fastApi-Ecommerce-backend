# src/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from ...deps import get_db, get_current_user
from ....services.auth import AuthService
from ....schema.auth import (
    UserLogin,
    UserRegister,
    GoogleAuthRequest,
    PasswordResetRequest,
    PasswordResetConfirm
)
from ....schema.token import Token
from ....schema.user import User as UserSchema
from ....models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    """User login with email/password"""
    # Add user agent and IP if not provided
    if not login_data.user_agent:
        login_data.user_agent = user_agent
    if not login_data.ip:
        login_data.ip = x_forwarded_for

    auth_service = AuthService(db)
    user, token = auth_service.login(login_data)
    return token

@router.post("/register", response_model=Token)
def register(
    register_data: UserRegister,
    db: Session = Depends(get_db),
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    """Register new user"""
    # Add user agent and IP if not provided
    if not register_data.user_agent:
        register_data.user_agent = user_agent
    if not register_data.ip:
        register_data.ip = x_forwarded_for

    auth_service = AuthService(db)
    user, token = auth_service.register(register_data)
    return token

@router.post("/google", response_model=Token)
def google_auth(
    auth_data: GoogleAuthRequest,
    db: Session = Depends(get_db),
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    """Authenticate with Google OAuth"""
    # Add user agent and IP if not provided
    if not auth_data.user_agent:
        auth_data.user_agent = user_agent
    if not auth_data.ip:
        auth_data.ip = x_forwarded_for

    auth_service = AuthService(db)
    user, token = auth_service.google_auth(auth_data)
    return token

@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str
):
    """Refresh access token"""
    # Note: This would typically accept refresh token in body
    # You might want to adjust based on your frontend needs
    pass

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    session_id: Optional[str] = None
):
    """Logout user"""
    auth_service = AuthService(db)
    auth_service.logout(current_user.id, session_id)
    return {"message": "Successfully logged out"}

@router.post("/password/reset-request")
def request_password_reset(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset email"""
    auth_service = AuthService(db)
    return auth_service.request_password_reset(reset_request.email)

@router.post("/password/reset")
def reset_password(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Reset password with token"""
    auth_service = AuthService(db)
    auth_service.reset_password(reset_data)
    return {"message": "Password reset successful"}

@router.get("/me", response_model=UserSchema)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user