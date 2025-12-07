# src/models/session.py
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Session(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_agent = Column(Text)
    ip = Column(String)
    last_seen = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")