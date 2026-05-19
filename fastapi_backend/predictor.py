"""
Core Prediction Engine
Performs inference using cached model. Never reloads.
"""
import time
import torch
import numpy as np
from fastapi_backend.model_loader import get_model, get_device
from fastapi_backend.preprocess import preprocess_image, preprocess_tabular
from fastapi_backend.config import settings
from fastapi_backend.logger import logger

def predict(disease: str, file_path: str = None, form_data: dict = None) -> dict:
    """Main prediction function"""
    start = time.time()
    
    # Get model and configuration
    model = get_model(disease)
    config = settings.MODELS[disease]
    model_type = config["type"]
    classes = config["classes"]

    if model_type == "pytorch":
        if not file_path:
            raise ValueError(f"Image file required for {disease}")
            
        input_tensor = preprocess_image(file_path, disease)
        with torch.no_grad():
            outputs = model(input_tensor)
            
            if outputs.shape[1] == 1:
                # Binary classification with a single output node (e.g., Pneumonia)
                prob_positive = torch.sigmoid(outputs).item()
                prob_negative = 1.0 - prob_positive
                
                class_probs = {
                    classes[0]: prob_negative,
                    classes[1]: prob_positive
                }
                conf_val = prob_positive if prob_positive >= 0.5 else prob_negative
                pred_label = classes[1] if prob_positive >= 0.5 else classes[0]
            else:
                # Multi-class or binary with multiple output nodes (e.g., Brain Tumor, Breast Cancer)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)

                class_probs = {classes[i]: float(probabilities[0][i]) for i in range(len(classes))}
                pred_label = classes[predicted.item()]
                conf_val = float(confidence.item())

    elif model_type == "xgboost":
        # Process tabular data
        df = preprocess_tabular(form_data, file_path)
        
        # Handle cases where model was saved as a dict (e.g. diabetes)
        actual_model = model['model'] if isinstance(model, dict) else model
        
        # XGBoost/Joblib models expect standard arrays or dataframes
        probabilities = actual_model.predict_proba(df)[0]
        predicted_idx = np.argmax(probabilities)
        
        class_probs = {classes[i]: float(probabilities[i]) for i in range(len(classes))}
        pred_label = classes[predicted_idx]
        conf_val = float(probabilities[predicted_idx])
        
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    processing_time = f"{(time.time() - start):.3f} sec"

    result = {
        "prediction": pred_label,
        "confidence": conf_val,
        "class_probabilities": class_probs,
        "processing_time": processing_time
    }
    logger.info(f"Prediction completed for {disease}: {result['prediction']} ({result['confidence']:.2f})")
    return result