# src/models/analytics.py
from sqlalchemy import Column, DateTime, ForeignKey
from datetime import datetime
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class ProductView(BaseModel):
    __tablename__ = "product_views"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    viewed_at = Column(DateTime, default=datetime.utcnow)