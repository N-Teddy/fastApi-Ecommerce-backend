# src/models/review.py
from sqlalchemy import Column, String, Text, SmallInteger, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Review(BaseModel):
    __tablename__ = "reviews"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    rating = Column(SmallInteger)
    title = Column(String)
    body = Column(Text)

    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='rating_range'),
    )