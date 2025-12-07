# src/enums/image.py
from enum import Enum

class ImageType(str, Enum):
    PRODUCT = "product"
    CATEGORY = "category"
    USER_PROFILE = "user_profile"
    PRODUCT_VARIANT = "product_variant"