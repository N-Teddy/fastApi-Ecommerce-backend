# src/enums/user.py
from enum import Enum

class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"