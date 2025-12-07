# src/services/auth.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests

from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)
from ..core.config import settings
from ..services.base import BaseService
from ..services.user import UserService
from ..services.email import EmailService
from ..models.user import User
from ..models.session import Session as SessionModel
from ..schema.auth import (
    UserLogin,
    UserRegister,

    GoogleAuthRequest,
    PasswordResetRequest,
    PasswordResetConfirm
)
from ..schema.token import Token, TokenPayload
from ..schema.user import UserCreate, UserUpdate
from ..core.exceptions import (
    BadRequestException,
    UnauthorizedException,
    NotFoundException,
    ValidationException
)

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.email_service = EmailService(db)

    def login(self, login_data: UserLogin) -> Tuple[User, Token]:
        """Authenticate user with email/password"""
        user = self.db.query(User).filter(
            User.email == login_data.email
        ).first()

        if not user:
            raise UnauthorizedException("Incorrect email or password")

        if not user.is_active:
            raise BadRequestException("Account is deactivated")

        if not verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedException("Incorrect email or password")

        # Create tokens
        access_token = self._create_user_tokens(user.id)

        # Create session
        self._create_session(user.id, login_data.user_agent, login_data.ip)

        return user, access_token

    def register(self, register_data: UserRegister) -> Tuple[User, Token]:
        """Register new user"""
        # Check if user exists
        existing_user = self.db.query(User).filter(
            User.email == register_data.email
        ).first()

        if existing_user:
            raise BadRequestException("User with this email already exists")

        # Create user
        user_create = UserCreate(
            email=register_data.email,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            password=register_data.password,
            is_active=True,
            auth_provider="email"
        )

        user = self.user_service.create(user_create)

        # Create tokens
        access_token = self._create_user_tokens(user.id)

        # Create session
        self._create_session(user.id, register_data.user_agent, register_data.ip)

        # Send welcome email
        # self.email_service.send_welcome_email(user.email, user.first_name)

        return user, access_token

    def google_auth(self, auth_data: GoogleAuthRequest) -> Tuple[User, Token]:
        """Authenticate with Google OAuth"""
        # Verify Google token
        user_info = self._verify_google_token(auth_data.token)

        if not user_info:
            raise UnauthorizedException("Invalid Google token")

        # Check if user exists by Google ID
        user = self.db.query(User).filter(
            User.google_id == user_info["sub"]
        ).first()

        if not user:
            # Check if user exists by email
            user = self.db.query(User).filter(
                User.email == user_info["email"]
            ).first()

            if user:
                # Link Google account to existing user
                user.google_id = user_info["sub"]
                user.email_verified = True
                self.db.commit()
            else:
                # Create new user
                user_create = UserCreate(
                    email=user_info["email"],
                    first_name=user_info.get("given_name", ""),
                    last_name=user_info.get("family_name", ""),
                    display_name=user_info.get("name", ""),
                    google_id=user_info["sub"],
                    email_verified=True,
                    is_active=True,
                    auth_provider="google"
                )
                user = self.user_service.create(user_create)

        # Create tokens
        access_token = self._create_user_tokens(user.id)

        # Create session
        self._create_session(user.id, auth_data.user_agent, auth_data.ip)

        return user, access_token

    def refresh_token(self, refresh_token: str) -> Token:
        """Refresh access token using refresh token"""
        payload = verify_token(refresh_token)

        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token payload")

        user = self.user_service.get(int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        return self._create_access_token(user.id)

    def logout(self, user_id: int, session_id: Optional[str] = None):
        """Logout user (remove specific session or all sessions)"""
        if session_id:
            # Remove specific session
            session = self.db.query(SessionModel).filter(
                SessionModel.id == session_id,
                SessionModel.user_id == user_id
            ).first()
            if session:
                self.db.delete(session)
        else:
            # Remove all user sessions (optional)
            sessions = self.db.query(SessionModel).filter(
                SessionModel.user_id == user_id
            ).all()
            for session in sessions:
                self.db.delete(session)

        self.db.commit()

    def request_password_reset(self, email: str):
        """Request password reset email"""
        user = self.db.query(User).filter(User.email == email).first()

        if user:
            # Generate reset token
            reset_token = create_access_token(
                subject=user.id,
                expires_delta=timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS),
                token_type="reset"
            )

            # Send reset email
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
            self.email_service.send_password_reset_email(
                email=user.email,
                name=user.first_name or user.email,
                reset_url=reset_url
            )

        # Always return success to prevent email enumeration
        return {"message": "Password reset email sent if account exists"}

    def reset_password(self, reset_data: PasswordResetConfirm) -> bool:
        """Reset password with token"""
        payload = verify_token(reset_data.token)

        if not payload or payload.get("type") != "reset":
            raise ValidationException("Invalid or expired reset token")

        user_id = payload.get("sub")
        if not user_id:
            raise ValidationException("Invalid token payload")

        user = self.user_service.get(int(user_id))
        if not user:
            raise NotFoundException("User not found")

        # Update password
        user_update = UserUpdate(hashed_password=get_password_hash(reset_data.new_password))
        self.user_service.update(user, user_update)

        # Invalidate all sessions for security
        self._invalidate_user_sessions(user.id)

        return True

    def _create_user_tokens(self, user_id: int) -> Token:
        """Create access and refresh tokens"""
        access_token = create_access_token(
            subject=user_id,
            token_type="access"
        )

        refresh_token = create_access_token(
            subject=user_id,
            token_type="refresh"
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    def _create_access_token(self, user_id: int) -> Token:
        """Create only access token"""
        access_token = create_access_token(
            subject=user_id,
            token_type="access"
        )

        return Token(
            access_token=access_token,
            token_type="bearer"
        )

    def _create_session(self, user_id: int, user_agent: Optional[str], ip: Optional[str]):
        """Create user session"""
        session = SessionModel(
            user_id=user_id,
            user_agent=user_agent,
            ip=ip
        )
        self.db.add(session)
        self.db.commit()
        return session

    def _verify_google_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify Google OAuth token"""
        try:
            # Verify token with Google
            response = requests.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            )

            if response.status_code == 200:
                user_info = response.json()

                # Verify audience
                if user_info.get("aud") != settings.GOOGLE_CLIENT_ID:
                    return None

                return user_info

            return None
        except Exception:
            return None

    def _invalidate_user_sessions(self, user_id: int):
        """Invalidate all user sessions"""
        sessions = self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id
        ).all()

        for session in sessions:
            self.db.delete(session)

        self.db.commit()