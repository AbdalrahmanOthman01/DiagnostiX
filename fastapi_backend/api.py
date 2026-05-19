"""
FastAPI Backend - Production API Server
Handles model inference, validation, error handling, logging.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import time
from fastapi_backend.model_loader import load_model
from fastapi_backend.predictor import predict
from fastapi_backend.postprocess import format_prediction
from fastapi_backend.schemas import PredictionResponse, HealthResponse, ModelInfo
from fastapi_backend.logger import logger
from fastapi_backend.config import settings

app = FastAPI(title="DiagnostiX ML API", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.on_event("startup")
async def startup_event():
    """Load model once at startup"""
    logger.info("Starting FastAPI backend...")
    load_model()
    logger.info("Model loaded successfully. API ready.")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", model_loaded=True, uptime=time.time(), version="1.0.0")

@app.get("/model-info", response_model=ModelInfo)
async def model_info():
    return ModelInfo(
        model_name=settings.MODEL_NAME if hasattr(settings, 'MODEL_NAME') else "BrainTumorClassifier",
        model_type=settings.MODEL_TYPE,
        num_classes=settings.NUM_CLASSES,
        classes=settings.CLASSES,
        input_shape="224x224x3",
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(request: Request):
    """Main prediction endpoint - supports image and tabular data"""
    
    form = await request.form()
    disease = form.get("disease", "brain")
    
    file = form.get("file")
    file_path = None
    
    if file and hasattr(file, "filename") and file.filename:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
    # For tabular data from questions, we pass the form dict
    # For CSV or Image, we pass the file_path
    
    # We will pass everything to predictor.py
    try:
        raw_result = predict(disease=disease, file_path=file_path, form_data=form)
        return format_prediction(raw_result)
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(500, f"Model inference failed: {str(e)}")

@app.get("/version")
async def version():
    return {"version": "1.0.0", "framework": "FastAPI + PyTorch"}

@app.get("/status")
async def status():
    return {"status": "operational", "model": "loaded"}