# src/schemas/auth.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    user_agent: Optional[str] = None
    ip: Optional[str] = None

class UserRegister(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    user_agent: Optional[str] = None
    ip: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class GoogleAuthRequest(BaseModel):
    token: str
    user_agent: Optional[str] = None
    ip: Optional[str] = None

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v