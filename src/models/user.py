# src/models/user.model.py
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from ..enums.user import AuthProvider
from .base import BaseModel

auth_provider_enum = ENUM(
    AuthProvider,
    name="auth_provider",
    create_type=True,
)

class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    phone = Column(String)
    auth_provider = Column(auth_provider_enum, default=AuthProvider.EMAIL)
    google_id = Column(String, unique=True, index=True)
    email_verified = Column(Boolean, default=False)

    # Image relationships
    images = relationship("Image",
                primaryjoin="and_(User.id==foreign(Image.imageable_id), "
                "Image.imageable_type=='user_profile')",
                backref="user_profile",
                cascade="all, delete-orphan")

    # Property to get primary profile image
    @property
    def profile_image(self):
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0] if self.images else None

    orders = relationship("Order", back_populates="user")
    addresses = relationship("Address", back_populates="user")
    wishlists = relationship("Wishlist", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    product_views = relationship("ProductView", back_populates="user")