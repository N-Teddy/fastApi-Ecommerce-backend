# src/models/category.py
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

       # Image relationships
    images = relationship("Image",
                primaryjoin="and_(Category.id==foreign(Image.imageable_id), "
                "Image.imageable_type=='category')",
                backref="category",
                cascade="all, delete-orphan")

    # Property to get primary image
    @property
    def primary_image(self):
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0] if self.images else None

    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category")