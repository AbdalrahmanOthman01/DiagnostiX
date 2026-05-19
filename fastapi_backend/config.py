"""
FastAPI Backend Configuration
Centralized settings for model, logging, and production.
"""
import os

class Settings:
    # Model configurations for all supported diseases
    MODELS: dict = {
        "brain": {
            "path": os.getenv("MODEL_PATH_BRAIN", "models/best_BrainTumor.pth"),
            "type": "pytorch",
            "classes": ["Glioma", "Meningioma", "Pituitary"]
        },
        "breast": {
            "path": os.getenv("MODEL_PATH_BREAST", "models/Breast_Cancer.pth"),
            "type": "pytorch",
            "classes": ["Benign", "Malignant"]
        },
        "xray": {
            "path": os.getenv("MODEL_PATH_XRAY", "models/pneumonia_model.pth"),
            "type": "pytorch",
            "classes": ["Normal", "Pneumonia"]
        },
        "heart": {
            "path": os.getenv("MODEL_PATH_HEART", "models/heart_xgboost.pkl"),
            "type": "xgboost",
            "classes": ["Low Risk", "High Risk"]
        },
        "diabetes": {
            "path": os.getenv("MODEL_PATH_DIABETES", "models/diabetes_xgboost_pipeline.pkl"),
            "type": "xgboost",
            "classes": ["Negative", "Positive"]
        }
    }
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./prediction_history.db")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))

settings = Settings()