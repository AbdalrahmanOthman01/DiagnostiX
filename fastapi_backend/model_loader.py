"""
Production Model Loader
Loads PyTorch/TensorFlow/Sklearn models ONLY ONCE at startup.
Supports .pt, .h5, .pkl, .joblib.
"""
import torch
import joblib
import os
import __main__
from fastapi_backend.config import settings
from fastapi_backend.logger import logger
from fastapi_backend.models import BrainEfficientNet, SimpleCNN, PneumoniaCNN

# Inject classes into __main__ for torch.load to find them if they were saved whole
setattr(__main__, 'BrainEfficientNet', BrainEfficientNet)
setattr(__main__, 'SimpleCNN', SimpleCNN)
setattr(__main__, 'PneumoniaCNN', PneumoniaCNN)

_models = {}
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    """Startup model loading - called once"""
    global _models
    
    for disease, config in settings.MODELS.items():
        model_path = config["path"]
        
        # In a real environment, you might want to log a warning instead of crashing 
        # if one model is missing, allowing the rest of the API to function.
        if not os.path.exists(model_path):
            logger.warning(f"Model not found at {model_path} for {disease}")
            continue

        try:
            if config["type"] == "pytorch":
                import __main__
                from fastapi_backend.models import BrainEfficientNet, SimpleCNN, PneumoniaCNN
                setattr(__main__, 'PneumoniaCNN', PneumoniaCNN)
                setattr(__main__, 'BrainEfficientNet', BrainEfficientNet)
                setattr(__main__, 'SimpleCNN', SimpleCNN)

                checkpoint = torch.load(model_path, map_location=_device, weights_only=False)
                
                # Unwrap if checkpoint is a dict wrapping another dict or model
                if isinstance(checkpoint, dict) and "model" in checkpoint:
                    checkpoint = checkpoint["model"]
                
                # If checkpoint is a state_dict (OrderedDict or dict), instantiate the model
                if isinstance(checkpoint, dict):
                    if disease == "breast":
                        model = SimpleCNN()
                        model.load_state_dict(checkpoint)
                    elif disease == "brain":
                        model = BrainEfficientNet()
                        model.load_state_dict(checkpoint)
                    elif disease == "xray":
                        model = PneumoniaCNN()
                        model.load_state_dict(checkpoint)
                    else:
                        raise ValueError(f"Unknown pytorch dict format for {disease}")
                else:
                    # Checkpoint is the full model object
                    model = checkpoint
                
                model = model.to(_device)
                model.eval()
                _models[disease] = model
                logger.info(f"PyTorch model loaded successfully for {disease} on {_device}")
            elif config["type"] == "xgboost":
                model = joblib.load(model_path)
                _models[disease] = model
                logger.info(f"Sklearn/Joblib model loaded for {disease}")
            else:
                logger.error(f"Unsupported model format for {disease}")
        except Exception as e:
            logger.error(f"Model load failed for {disease}: {e}")

    if not _models:
        logger.error("No models were successfully loaded!")

def get_model(disease: str):
    """Return cached model instance for a disease"""
    if disease not in _models:
        # Try loading lazily if not found (in case file was added later)
        if disease in settings.MODELS and os.path.exists(settings.MODELS[disease]["path"]):
            load_model()
        if disease not in _models:
            raise ValueError(f"Model for {disease} is not loaded or missing.")
    return _models[disease]

def get_device():
    return _device