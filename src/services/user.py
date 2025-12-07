# src/services/user.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .base import BaseService
from ..models.user import User
from ..schema.user import UserCreate, UserUpdate, User as UserSchema
from ..core.security import get_password_hash

class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def create(self, obj_in: UserCreate) -> User:
        """Create user with password hashing"""
        obj_in_data = obj_in.dict(exclude_unset=True)

        # Hash password if provided
        if "password" in obj_in_data:
            obj_in_data["hashed_password"] = get_password_hash(obj_in_data.pop("password"))

        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_google_id(self, google_id: str) -> Optional[User]:
        """Get user by Google ID"""
        return self.db.query(User).filter(User.google_id == google_id).first()

    def search_users(self, query: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name or email"""
        return self.db.query(User).filter(
            or_(
                User.email.ilike(f"%{query}%"),
                User.first_name.ilike(f"%{query}%"),
                User.last_name.ilike(f"%{query}%"),
                User.display_name.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()

    def update_profile(self, user: User, update_data: UserUpdate) -> User:
        """Update user profile"""
        return self.update(user, update_data)