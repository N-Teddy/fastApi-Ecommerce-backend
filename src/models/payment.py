# src/models/payment.py
from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import relationship
from ..enums.payment import PaymentMethod, PaymentStatus
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

# Create PostgreSQL ENUM types
payment_method_enum = ENUM(
    PaymentMethod,
    name="payment_method",
    create_type=True
)

payment_status_enum = ENUM(
    PaymentStatus,
    name="payment_status",
    create_type=True
)

class Payment(BaseModel):
    __tablename__ = "payments"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    method = Column(payment_method_enum, nullable=False)
    gateway_payment_id = Column(String)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(payment_status_enum, default=PaymentStatus.PENDING)
    raw_response = Column(JSONB)

    order = relationship("Order", back_populates="payments")