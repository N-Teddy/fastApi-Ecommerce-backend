# src/models/order.py
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from ..enums.order import OrderStatus
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID


# Create PostgreSQL ENUM type
order_status_enum = ENUM(
    OrderStatus,
    name="order_status",
    create_type=True
)

class Order(BaseModel):
    __tablename__ = "orders"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"))
    order_number = Column(String, unique=True, index=True)
    status = Column(order_status_enum, default=OrderStatus.PENDING)
    total_amount = Column(Numeric(12, 2))
    shipping_fee = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    notes = Column(Text)

    user = relationship("User", back_populates="orders")
    shipping_address = relationship("Address", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='total_amount_non_negative'),
    )