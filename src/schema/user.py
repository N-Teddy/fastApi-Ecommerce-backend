# src/schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from ..enums.user import AuthProvider


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    email: EmailStr
    password: Optional[str] = None
    auth_provider: AuthProvider = AuthProvider.EMAIL
    google_id: Optional[str] = None

    @validator('password', pre=True, always=True)
    def validate_password(cls, v, values):
        if values.get('auth_provider') == AuthProvider.EMAIL and not v:
            raise ValueError('Password is required for email authentication')
        return v

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    email_verified: bool
    auth_provider: AuthProvider
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserInDB):
    pass