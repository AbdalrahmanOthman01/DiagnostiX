"""
Pydantic Schemas for Request/Response Validation
Production-grade validation for all API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

class PredictionRequest(BaseModel):
    filename: str = Field(..., min_length=1)

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float = Field(..., ge=0, le=1)
    class_probabilities: Dict[str, float]
    processing_time: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ModelInfo(BaseModel):
    model_name: str
    model_type: str
    num_classes: int
    classes: List[str]
    input_shape: str
    version: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    uptime: float
    version: str

class PredictionHistory(BaseModel):
    id: int
    filename: str
    prediction: str
    confidence: float
    timestamp: datetime