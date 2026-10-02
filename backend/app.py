"""
Social Media Privacy Risk Assessment Framework
Master Application Server (Flask REST API & Web UI)
===================================================
A defensive cybersecurity framework evaluating digital footprints,
social-engineering exposure, location leaks, and authentication hygiene.

Strictly follows Privacy by Design:
- Zero scraping of real profiles.
- Zero collection of actual PII.
- 100% defensive educational modeling.
"""

import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.database import init_db
from backend.routes.assessment_routes import assessment_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.metadata_routes import metadata_bp

def create_app(test_config=None) -> Flask:
    """Application factory for the privacy risk assessment platform."""
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
    
    # Enable CORS for defensive API access
    CORS(app)

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "defensive-privacy-framework-secret-key-2026")
    app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB max upload

    if test_config:
        app.config.update(test_config)

    # Initialize Database Schema
    init_db()

    # Register API Blueprints
    app.register_blueprint(assessment_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(metadata_bp)

    # Health Check Endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "Social Media Privacy Risk Assessment Framework",
            "version": "1.0.0",
            "mode": "Defensive Privacy Engineering",
            "storage": "Privacy-Preserving SQLite (Zero Raw PII)"
        }), 200

    # Frontend Navigation Routes
    @app.route("/")
    def index_page():
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/assessment")
    def assessment_page():
        return send_from_directory(frontend_dir, "assessment.html")

    @app.route("/dashboard")
    def dashboard_page():
        return send_from_directory(frontend_dir, "dashboard.html")

    @app.route("/simulator")
    def simulator_page():
        return send_from_directory(frontend_dir, "simulator.html")

    @app.route("/report")
    def report_page():
        return send_from_directory(frontend_dir, "report.html")

    @app.route("/metadata")
    def metadata_page():
        return send_from_directory(frontend_dir, "metadata.html")

    @app.route("/checklist")
    def checklist_page():
        return send_from_directory(frontend_dir, "checklist.html")

    # Static Assets Handler (CSS, JS)
    @app.route("/css/<path:filename>")
    def serve_css(filename):
        return send_from_directory(os.path.join(frontend_dir, "css"), filename)

    @app.route("/js/<path:filename>")
    def serve_js(filename):
        return send_from_directory(os.path.join(frontend_dir, "js"), filename)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print("  SOCIAL MEDIA PRIVACY RISK ASSESSMENT FRAMEWORK")
    print("  Defensive Cybersecurity & Privacy by Design")
    print(f"  Starting local server on: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=True)
