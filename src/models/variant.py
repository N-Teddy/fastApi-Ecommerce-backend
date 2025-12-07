# src/models/variant.py
from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class ProductVariant(BaseModel):
    __tablename__ = "product_variants"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Numeric(10, 2))
    compare_at_price = Column(Numeric(10, 2))
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    images = relationship("Image",
                primaryjoin="and_(ProductVariant.id==foreign(Image.imageable_id), "
                "Image.imageable_type=='product_variant')",
                backref="product_variant",
                cascade="all, delete-orphan")

    product = relationship("Product", back_populates="variants")
    order_items = relationship("OrderItem", back_populates="variant")

    __table_args__ = (
        CheckConstraint('stock >= 0', name='stock_non_negative'),
    )