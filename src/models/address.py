# src/models/category.py
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Address(BaseModel):
    __tablename__ = "addresses"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_default = Column(Boolean, default=False)
    label = Column(String)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Cameroon")
    postal_code = Column(String)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="shipping_address")