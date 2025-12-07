# src/models/order_item.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.id"))
    product_title_snapshot = Column(String, nullable=False)
    sku_snapshot = Column(String)
    unit_price = Column(Numeric(12, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    line_total = Column(Numeric(12, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    variant = relationship("ProductVariant", back_populates="order_items")

    __table_args__ = (
        CheckConstraint('quantity > 0', name='quantity_positive'),
        CheckConstraint('line_total >= 0', name='line_total_non_negative'),
    )