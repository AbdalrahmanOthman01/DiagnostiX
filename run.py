#!/usr/bin/env python3
"""
Production Run Script for Flask Frontend
Handles Gunicorn/Flask startup with proper config loading.
"""
import os
from flask_app.app import create_app

flask_app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    flask_app.run(host=host, port=port, debug=debug)