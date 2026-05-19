from fastapi_backend.model_loader import load_model, _models
import sys

print("Loading models...")
load_model()
print("Loaded models:", list(_models.keys()))
