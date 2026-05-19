# 🚀 DiagnostiX

**Enterprise-Grade AI-Powered Medical Diagnostics Platform**

Production-ready, scalable, and secure system for real-time brain tumor classification using deep learning.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Flask](https://img.shields.io/badge/Flask-3.0-red)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

DiagnostiX delivers hospital-grade accuracy for MRI brain tumor diagnosis using a modern microservices architecture:

- **Flask Frontend** – Beautiful, responsive UI with glassmorphism design
- **FastAPI Backend** – High-performance inference engine
- **PyTorch Model** – Loaded once at startup for maximum speed
- **Nginx Reverse Proxy** – Production traffic management

The system supports **PyTorch**, **TensorFlow**, **scikit-learn**, and is designed to easily accommodate future NLP, segmentation, and object detection models.

---

## 🏗️ Architecture Diagram

```
┌─────────────┐     HTTP      ┌──────────────┐     REST      ┌────────────────┐
│   User      │  ───────────▶ │   Flask      │  ───────────▶ │   FastAPI      │
│  Browser    │               │  Frontend    │               │   Backend      │
└─────────────┘               └──────────────┘               └────────────────┘
                                                                   │
                                                                   ▼
                                                            ┌────────────────┐
                                                            │  PyTorch Model │
                                                            │  (Loaded Once) │
                                                            └────────────────┘
```

**Key Design Decisions**
- Model loaded **once** on FastAPI startup (`@app.on_event("startup")`)
- Flask never performs inference — only proxies requests
- All responses validated with Pydantic schemas
- Comprehensive logging + global exception handling

---

## ✨ Features

- Drag & drop image upload with instant preview
- Real-time animated loading states
- Probability bar charts and clinical insights
- Dark / Light theme with localStorage persistence
- Fully responsive (mobile, tablet, desktop)
- Production Docker Compose stack (Flask + FastAPI + Nginx)
- Rate limiting, file validation, and security best practices
- Structured JSON logging with rotation

---

## 🚀 Quick Start

### Docker (Recommended for Production)

```bash
git clone https://github.com/your-org/diagnostix.git
cd diagnostix

# Add your trained model
cp /path/to/your/model.pt models/brain_tumor_model.pt

docker-compose up --build
```

Open **http://localhost** — fully production-ready.

### Development Mode

```bash
pip install -r requirements.txt

# Terminal 1
uvicorn fastapi_backend.api:app --reload --port 8000

# Terminal 2
python run.py
```

---

## 🔧 Configuration

All settings are managed via `.env`:

```env
FLASK_PORT=5000
FASTAPI_PORT=8000
MODEL_PATH=models/brain_tumor_model.pt
MODEL_TYPE=pytorch
NUM_CLASSES=3
CLASSES=Glioma,Meningioma,Pituitary
MAX_UPLOAD_SIZE=10485760
LOG_LEVEL=INFO
```

---

## 📡 API Reference

### `POST /predict`
Upload an MRI image and receive diagnosis.

**Request:**
```bash
curl -X POST http://localhost/api/predict \
  -F "file=@scan.jpg"
```

**Response:**
```json
{
  "prediction": "Glioma",
  "confidence": 0.9842,
  "class_probabilities": {
    "Glioma": 0.9842,
    "Meningioma": 0.0101,
    "Pituitary": 0.0057
  },
  "processing_time": "0.142 sec",
  "timestamp": "2026-05-19T00:12:31Z"
}
```

Other endpoints: `/health`, `/model-info`, `/status`, `/version`.

---

## 🧪 Testing

```bash
pytest tests/ -v
```

Includes tests for:
- Health checks
- Model loading
- Invalid file handling
- Prediction pipeline

---

## 🐳 Production Deployment

- Uses **Gunicorn** (Flask) + **Uvicorn** (FastAPI)
- Nginx for static files, rate limiting, and SSL termination
- Horizontal scaling ready via Docker Swarm / Kubernetes

---

## 👥 Core Contributors

<table>
<tr>
  <td align="center">
    <img src="https://avatars.githubusercontent.com/u/000?v=4" width="70"><br>
    <b>Abdalrahman Hossam Othman</b><br>
    <sub>Principal AI Engineer & System Architect</sub>
  </td>

</table>

---

## 🛣️ Roadmap

- [ ] PostgreSQL + Alembic integration
- [ ] WebSocket real-time progress
- [ ] Support for segmentation & object detection models
- [ ] Kubernetes manifests
- [ ] Prometheus + Grafana monitoring

---

## 📄 License

MIT License © 2026 DiagnostiX

---

<p align="center">
  <strong>Built for production. Designed for clinicians.</strong><br>
  <sub>DiagnostiX — AI that saves lives</sub>
</p>
