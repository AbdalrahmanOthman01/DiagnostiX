import torch
import sys

paths = [
    "models/best_BrainTumor.pth",
    "models/Breast_Cancer.pth",
    "models/pneumonia_model.pth"
]

for p in paths:
    try:
        data = torch.load(p, map_location="cpu", weights_only=False)
        print(f"{p}: type={type(data)}")
        if isinstance(data, dict):
            print(f"  keys: {list(data.keys())}")
    except Exception as e:
        print(f"{p} failed: {e}")
