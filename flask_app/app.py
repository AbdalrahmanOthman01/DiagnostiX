"""
Flask Application Factory
Main entry point for the frontend. Handles blueprints, config, and error pages.
"""
from flask import Flask
from flask_cors import CORS
from flask_app.config import config
import os

def create_app(config_name="production"):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config[config_name])
    CORS(app)

    # Register routes
    from flask_app.routes import main_bp
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error="404 - Page Not Found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", error="500 - Internal Server Error"), 500

    return app

from flask import render_template