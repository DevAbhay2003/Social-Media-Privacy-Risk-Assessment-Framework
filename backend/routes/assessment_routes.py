"""
Social Media Privacy Risk Assessment Framework
Assessment API Routes
===================================================
RESTful endpoints for running assessments, retrieving findings,
simulating setting improvements, and enforcing data minimization.
"""

from flask import Blueprint, request, jsonify
from backend.utils.validators import validate_questionnaire_submission, validate_profile_payload, validate_posts_payload
from backend.utils.questionnaire_data import QUESTIONS, CATEGORY_DEFINITIONS
from backend.services.assessment_engine import process_questionnaire_assessment, process_json_profile_assessment
from backend.services.improvement_simulator import simulate_privacy_improvements, IMPROVEMENT_ACTION_MAP
from backend.database import get_assessment_by_id, delete_assessment_by_id

assessment_bp = Blueprint("assessment", __name__, url_prefix="/api")

@assessment_bp.route("/questions", methods=["GET"])
def get_questions():
    """Returns the full master questionnaire definitions with categories."""
    return jsonify({
        "status": "success",
        "total_questions": len(QUESTIONS),
        "categories": CATEGORY_DEFINITIONS,
        "questions": QUESTIONS
    }), 200

@assessment_bp.route("/assessment", methods=["POST"])
def create_assessment():
    """
    Submits user questionnaire responses, computes risk metrics,
    and stores an anonymized, privacy-safe record.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Missing JSON request body."}), 400

    answers = data.get("answers", {})
    platform = data.get("platform", "Cross-Platform")

    # Defensive validation
    is_valid, err_msg, sanitized_answers = validate_questionnaire_submission(answers)
    if not is_valid:
        return jsonify({"status": "error", "message": err_msg}), 422

    result = process_questionnaire_assessment(sanitized_answers, platform=platform)
    return jsonify({
        "status": "success",
        "data": result
    }), 201

@assessment_bp.route("/assessment/<assessment_id>", methods=["GET"])
def get_assessment(assessment_id):
    """Retrieves assessment results by ID without exposing sensitive PII."""
    record = get_assessment_by_id(assessment_id)
    if not record:
        return jsonify({"status": "error", "message": f"Assessment '{assessment_id}' not found."}), 404

    return jsonify({
        "status": "success",
        "data": record
    }), 200

@assessment_bp.route("/assessment/<assessment_id>/recommendations", methods=["GET"])
def get_recommendations(assessment_id):
    """Retrieves prioritized security recommendations for an assessment."""
    record = get_assessment_by_id(assessment_id)
    if not record:
        return jsonify({"status": "error", "message": "Assessment not found."}), 404

    return jsonify({
        "status": "success",
        "assessment_id": assessment_id,
        "recommendations": record["recommendations"]
    }), 200

@assessment_bp.route("/assessment/simulate-improvement", methods=["POST"])
def simulate_improvement():
    """
    Simulates setting changes and calculates projected risk score reduction.
    """
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", {})
    selected_actions = data.get("selected_actions", [])

    if not isinstance(selected_actions, list):
        return jsonify({"status": "error", "message": "selected_actions must be an array of action keys."}), 400

    simulation = simulate_privacy_improvements(answers, selected_actions)
    return jsonify({
        "status": "success",
        "data": simulation
    }), 200

@assessment_bp.route("/assessment/available-improvements", methods=["GET"])
def get_available_improvements():
    """Returns catalog of configurable improvement actions."""
    return jsonify({
        "status": "success",
        "actions": IMPROVEMENT_ACTION_MAP
    }), 200

@assessment_bp.route("/analyze-json", methods=["POST"])
def analyze_json():
    """
    Ingests profile.json and posts.json synthetic payloads.
    Supports either direct JSON body or multipart file upload.
    """
    if request.is_json:
        data = request.get_json()
        profile_raw = data.get("profile", {})
        posts_raw = data.get("posts", [])
    elif "profile" in request.files and "posts" in request.files:
        import json
        try:
            profile_raw = json.loads(request.files["profile"].read().decode("utf-8"))
            posts_raw = json.loads(request.files["posts"].read().decode("utf-8"))
        except Exception as e:
            return jsonify({"status": "error", "message": f"Malformed uploaded JSON files: {str(e)}"}), 400
    else:
        return jsonify({"status": "error", "message": "Expected JSON payload or 'profile' & 'posts' files."}), 400

    _, _, valid_profile = validate_profile_payload(profile_raw)
    _, _, valid_posts = validate_posts_payload(posts_raw)

    result = process_json_profile_assessment(valid_profile, valid_posts)
    return jsonify({
        "status": "success",
        "data": result
    }), 201

@assessment_bp.route("/privacy-checklist", methods=["GET"])
def get_privacy_checklist():
    """Returns downloadable / printable privacy audit checklist."""
    checklist = [
        {"item": "Review profile visibility; set account to Private or Friends Only where feasible.", "category": "Profile Visibility", "tier": "Essential"},
        {"item": "Remove direct phone number from bio, contact cards, and search lookup.", "category": "Personal Info", "tier": "Critical"},
        {"item": "Remove or mask personal email address; use aliases for business inquiries.", "category": "Personal Info", "tier": "Critical"},
        {"item": "Hide full birth year; limit birthday visibility to Day and Month or Only Me.", "category": "Personal Info", "tier": "High"},
        {"item": "Turn off continuous real-time location broadcasting (e.g., Snap Map Ghost Mode).", "category": "Location", "tier": "Critical"},
        {"item": "Avoid posting vacation or travel schedules until you have returned safely home.", "category": "Location", "tier": "High"},
        {"item": "Never post images showing corporate ID badges, building keys, or monitor screens.", "category": "Posts & Content", "tier": "Critical"},
        {"item": "Protect minors: restrict photos of children and obscure school badges.", "category": "Posts & Content", "tier": "Critical"},
        {"item": "Enable Tag Review so tagged photos and check-ins require your explicit approval.", "category": "Tagging", "tier": "High"},
        {"item": "Decline connection requests from unfamiliar profiles or verify them out-of-band.", "category": "Friends", "tier": "High"},
        {"item": "Enable Multi-Factor Authentication (MFA) using an Authenticator App (TOTP).", "category": "Account Security", "tier": "Critical"},
        {"item": "Use unique passwords generated and stored in a secure password manager.", "category": "Account Security", "tier": "Critical"},
        {"item": "Enable unrecognized login alerts via email or push notifications.", "category": "Account Security", "tier": "High"},
        {"item": "Audit and terminate stale active login sessions across devices biannually.", "category": "Account Security", "tier": "Medium"},
        {"item": "Review third-party app permissions; revoke access for unused apps and quizzes.", "category": "Third-Party Apps", "tier": "High"},
        {"item": "Never forward 6-digit verification codes or OTPs to anyone via direct message.", "category": "Social Engineering", "tier": "Critical"},
        {"item": "Conduct defensive self-OSINT searches to monitor publicly cached footprint data.", "category": "Digital Footprint", "tier": "Medium"},
        {"item": "Run platform-native Privacy Checkups every 6 months to audit new settings.", "category": "Digital Footprint", "tier": "Medium"}
    ]
    return jsonify({
        "status": "success",
        "checklist": checklist
    }), 200

@assessment_bp.route("/assessment/<assessment_id>", methods=["DELETE"])
def delete_assessment(assessment_id):
    """Enforces Right to Erasure / GDPR Article 17 by deleting assessment records."""
    success = delete_assessment_by_id(assessment_id)
    if not success:
        return jsonify({"status": "error", "message": "Assessment ID not found or already deleted."}), 404

    return jsonify({
        "status": "success",
        "message": f"Assessment '{assessment_id}' and all associated records have been permanently erased."
    }), 200
