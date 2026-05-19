"""
Flask Application Configuration
Production-ready settings with environment variable support.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "production-secret-key-change-me")
    FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png").split(","))

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}