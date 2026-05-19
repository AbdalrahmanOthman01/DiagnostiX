"""
Post-processing Module
Formats output, adds medical insights, validates results.
"""
from fastapi_backend.schemas import PredictionResponse
from datetime import datetime

def format_prediction(raw_result: dict) -> PredictionResponse:
    """Clean JSON response formatting"""
    return PredictionResponse(
        prediction=raw_result["prediction"],
        confidence=round(raw_result["confidence"], 4),
        class_probabilities={k: round(v, 4) for k, v in raw_result["class_probabilities"].items()},
        processing_time=raw_result["processing_time"],
        timestamp=datetime.utcnow()
    )

def add_insights(prediction: str) -> str:
    """Medical domain insights (example)"""
    insights = {
        "Glioma": "High-grade glioma detected. Recommend urgent MRI follow-up.",
        "Meningioma": "Benign meningioma likely. Monitor with regular scans.",
        "Pituitary": "Pituitary adenoma. Endocrine evaluation advised."
    }
    return insights.get(prediction, "Consult specialist for diagnosis.")