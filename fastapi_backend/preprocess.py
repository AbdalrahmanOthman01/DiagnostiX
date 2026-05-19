"""
Preprocessing Pipeline
Handles image resizing, normalization, tensor conversion.
Reusable for multiple model types.
"""
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
from fastapi_backend.config import settings

def preprocess_image(image_path: str, disease: str = "brain"):
    """Standard preprocessing for different diseases"""
    if disease == "breast":
        transform = transforms.Compose([
            transforms.Resize((50, 50)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        image = Image.open(image_path).convert("RGB")
    elif disease == "xray":
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])
        image = Image.open(image_path).convert("L")
    else: # brain and default
        transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
        ])
        image = Image.open(image_path).convert("RGB")
        
    tensor = transform(image).unsqueeze(0)
    return tensor.to("cuda" if torch.cuda.is_available() else "cpu")

import pandas as pd

def preprocess_tabular(form_data: dict, file_path: str = None):
    """Process tabular data from form or csv file"""
    if file_path and file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        return df.iloc[0:1] # Return first row as dataframe
        
    if form_data:
        disease = form_data.get('disease', '')
        
        feature_values = []
        for key, val in form_data.items():
            if key != 'disease' and val is not None and str(val).strip() != '':
                try:
                    feature_values.append(float(val))
                except ValueError:
                    pass
                    
        # Pad with 0s if features are missing
        if disease == 'heart' and len(feature_values) < 21:
            feature_values += [0.0] * (21 - len(feature_values))
        elif disease == 'diabetes' and len(feature_values) < 65:
            feature_values += [0.0] * (65 - len(feature_values))
            
        return np.array([feature_values])
        
    raise ValueError("No tabular data provided")