"""
Flask Routes - Frontend only
Handles page rendering and proxying requests to FastAPI backend.
Never performs model inference.
"""
from flask import Blueprint, render_template, request, jsonify, current_app
import requests
import os

main_bp = Blueprint("main", __name__)
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

@main_bp.route("/")
def landing():
    return render_template("index.html")

@main_bp.route("/home")
def home():
    return render_template("index.html")

@main_bp.route("/predict")
def predict_page():
    return render_template("predict.html")

@main_bp.route("/results")
def results():
    return render_template("results.html")

@main_bp.route("/history")
def history():
    return render_template("history.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/api/predict", methods=["POST"])
def proxy_predict():
    """Proxy prediction request to FastAPI backend"""
    try:
        disease = request.form.get("disease", "brain")
        
        if "file" in request.files:
            # Image upload (brain tumor etc.)
            files = {
                "file": (
                    request.files["file"].filename,
                    request.files["file"].stream,
                    request.files["file"].content_type
                )
            }
            data = {"disease": disease}
            response = requests.post(
                f"{FASTAPI_URL}/predict",
                files=files,
                data=data,
                timeout=30
            )
        else:
            # Tabular / questionnaire data
            data = request.form.to_dict()
            data["disease"] = disease
            response = requests.post(
                f"{FASTAPI_URL}/predict",
                data=data,
                timeout=30
            )
        
        return jsonify(response.json()), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Prediction service timeout"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "FastAPI backend unavailable (503). Make sure uvicorn is running on port 8000."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/api/health")
def proxy_health():
    try:
        response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503