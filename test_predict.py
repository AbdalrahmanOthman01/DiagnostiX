from fastapi_backend.model_loader import load_model, _models
from fastapi_backend.predictor import predict
import os

print("Loading models...")
load_model()

# We need a dummy image
from PIL import Image
img = Image.new('RGB', (100, 100), color = 'red')
os.makedirs('uploads', exist_ok=True)
img_path = 'uploads/test.png'
img.save(img_path)

print("Predicting Brain...")
print(predict('brain', file_path=img_path))

print("Predicting Breast...")
print(predict('breast', file_path=img_path))

print("Predicting XRay...")
print(predict('xray', file_path=img_path))

print("All predictions successful!")
