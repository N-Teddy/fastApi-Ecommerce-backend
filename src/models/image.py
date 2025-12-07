# src/models/image.py
from sqlalchemy import Column, String, Integer, Boolean, Index
from sqlalchemy.dialects.postgresql import ENUM
from .base import BaseModel
from ..enums.image import ImageType
from sqlalchemy.dialects.postgresql import UUID

image_type_enum = ENUM(
    ImageType,
    name="image_type",
    create_type=True,
)


class Image(BaseModel):
    __tablename__ = "images"

    # Polymorphic columns
    imageable_type = Column(image_type_enum, nullable=False)
    imageable_id = Column(UUID(as_uuid=True), nullable=False)

    # Image data
    url = Column(String, nullable=False)
    alt_text = Column(String)
    caption = Column(String)
    is_primary = Column(Boolean, default=False)
    position = Column(Integer, default=0)  # For ordering images
    image_metadata = Column(String)  # JSON string for additional data (size, dimensions, etc.)

    # Add indexes for polymorphic queries
    __table_args__ = (
        Index('idx_imageable', 'imageable_type', 'imageable_id'),
    )

    # Helper property to get the associated object
    @property
    def imageable(self):
        """Get the associated object based on imageable_type and imageable_id"""
        # This would typically be implemented in your service layer
        # For SQLAlchemy relationships, you'd use a different pattern
        pass