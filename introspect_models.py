from fastapi_backend.model_loader import load_model, _models
import joblib

load_model()
heart_model = _models['heart']
diabetes_model = _models['diabetes']

print("Heart Model Type:", type(heart_model))
if hasattr(heart_model, 'feature_names_in_'):
    print("Heart Expected Features:", list(heart_model.feature_names_in_))
elif hasattr(heart_model, 'get_booster'):
    print("Heart Expected Features:", heart_model.get_booster().feature_names)

print("Diabetes Model Type:", type(diabetes_model))
if hasattr(diabetes_model, 'feature_names_in_'):
    print("Diabetes Expected Features:", list(diabetes_model.feature_names_in_))
elif hasattr(diabetes_model, 'get_booster'):
    print("Diabetes Expected Features:", diabetes_model.get_booster().feature_names)

