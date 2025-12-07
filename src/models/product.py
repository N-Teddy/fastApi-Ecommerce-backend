# src/models/product.py
from sqlalchemy import Column, String, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from ..enums.product import ProductStatus
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

product_status_enum = ENUM(
    ProductStatus,
    name="product_status",
    create_type=True,
)

class Product(BaseModel):
    __tablename__ = "products"

    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    description = Column(Text)
    base_price = Column(Numeric(10, 2))
    status = Column(product_status_enum, default=ProductStatus.DRAFT)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    featured_image_url = Column(String)

     # Image relationships
    images = relationship("Image",
                primaryjoin="and_(Product.id==foreign(Image.imageable_id), "
                "Image.imageable_type=='product')",
                backref="product",
                cascade="all, delete-orphan")

    # Property to get primary image
    @property
    def primary_image(self):
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0] if self.images else None

    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    wishlists = relationship("Wishlist", back_populates="product")
    reviews = relationship("Review", back_populates="product")