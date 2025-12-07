# src/utils/image_helper.py
from sqlalchemy.orm import Session
from models.image import Image, ImageType

def get_images_for_entity(db: Session, imageable_type: ImageType, imageable_id: int):
    """Get all images for a specific entity"""
    return db.query(Image).filter(
        Image.imageable_type == imageable_type,
        Image.imageable_id == imageable_id
    ).order_by(Image.position).all()

def get_primary_image_for_entity(db: Session, imageable_type: ImageType, imageable_id: int):
    """Get the primary image for an entity"""
    return db.query(Image).filter(
        Image.imageable_type == imageable_type,
        Image.imageable_id == imageable_id,
        Image.is_primary == True
    ).first()

def set_primary_image(db: Session, image_id: int):
    """Set an image as primary and unset others for the same entity"""
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        return None

    # Unset primary for all other images of the same entity
    db.query(Image).filter(
        Image.imageable_type == image.imageable_type,
        Image.imageable_id == image.imageable_id,
        Image.id != image_id
    ).update({Image.is_primary: False})

    # Set this image as primary
    image.is_primary = True
    db.commit()
    return image

def add_image_to_entity(db: Session, imageable_type: ImageType, imageable_id: int,
                       url: str, alt_text: str = None, is_primary: bool = False):
    """Add an image to an entity"""
    if is_primary:
        # Unset existing primary image
        db.query(Image).filter(
            Image.imageable_type == imageable_type,
            Image.imageable_id == imageable_id,
            Image.is_primary == True
        ).update({Image.is_primary: False})

    # Get next position
    last_image = db.query(Image).filter(
        Image.imageable_type == imageable_type,
        Image.imageable_id == imageable_id
    ).order_by(Image.position.desc()).first()

    position = last_image.position + 1 if last_image else 0

    image = Image(
        imageable_type=imageable_type,
        imageable_id=imageable_id,
        url=url,
        alt_text=alt_text,
        is_primary=is_primary,
        position=position
    )

    db.add(image)
    db.commit()
    db.refresh(image)
    return image