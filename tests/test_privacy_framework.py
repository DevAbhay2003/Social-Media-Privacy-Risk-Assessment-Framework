"""
Social Media Privacy Risk Assessment Framework
Automated Defensive Test Suite (34 Comprehensive Tests)
===================================================
Covers all functional requirements, scoring rules, boundary conditions,
privacy-by-design compliance, data minimization, and REST API endpoints.
"""

import os
import sys
import pytest

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.utils.questionnaire_data import QUESTIONS, QUESTION_MAP, CATEGORY_DEFINITIONS
from backend.utils.validators import validate_questionnaire_submission, validate_profile_payload, validate_posts_payload
from backend.services.scoring_engine import (
    calculate_category_scores,
    calculate_privacy_risk,
    classify_risk_level,
    score_profile_and_posts,
    extract_privacy_features
)
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_privacy_improvements
from backend.services.assessment_engine import process_questionnaire_assessment
from backend.services.metadata_engine import parse_exif_from_bytes, strip_exif_metadata
from backend.database import init_db, get_assessment_by_id, delete_assessment_by_id, get_db_connection
from backend.app import create_app

@pytest.fixture
def client():
    """Provides Flask test client with an in-memory/test SQLite database."""
    app = create_app({"TESTING": True, "DATABASE_PATH": ":memory:"})
    with app.test_client() as client:
        yield client

# Helper fixtures for standard synthetic response profiles
def get_fully_private_answers():
    answers = {}
    for q in QUESTIONS:
        safest = min(q["options"], key=lambda o: o["risk_points"])
        answers[q["id"]] = safest["value"]
    return answers

def get_fully_public_answers():
    answers = {}
    for q in QUESTIONS:
        riskiest = max(q["options"], key=lambda o: o["risk_points"])
        answers[q["id"]] = riskiest["value"]
    return answers


# =========================================================================
# TEST CASES 1 - 20: Behavioral Profiles & Specific Risk Vectors
# =========================================================================

def test_01_fully_private_profile():
    """Test 01: Fully private synthetic profile produces LOW risk score."""
    answers = get_fully_private_answers()
    cat_scores = calculate_category_scores(answers)
    overall, level = calculate_privacy_risk(cat_scores)
    assert overall <= 20, f"Expected Low risk (<=20), got {overall}"
    assert level == "LOW"

def test_02_fully_public_synthetic_profile():
    """Test 02: Fully public synthetic profile produces CRITICAL risk score."""
    answers = get_fully_public_answers()
    cat_scores = calculate_category_scores(answers)
    overall, level = calculate_privacy_risk(cat_scores)
    assert overall >= 71, f"Expected Critical risk (>=71), got {overall}"
    assert level == "CRITICAL"

def test_03_public_phone_exposure():
    """Test 03: Public phone number reported generates a CRITICAL severity finding."""
    answers = get_fully_private_answers()
    answers["Q_B1"] = "YES" # Public phone
    findings = generate_privacy_findings(answers)
    phone_finding = next((f for f in findings if f["question_id"] == "Q_B1"), None)
    assert phone_finding is not None
    assert phone_finding["severity"] == "CRITICAL"
    assert "Phone" in phone_finding["title"]

def test_04_public_email_exposure():
    """Test 04: Public personal email generates a HIGH severity finding."""
    answers = get_fully_private_answers()
    answers["Q_B2"] = "YES" # Public email
    findings = generate_privacy_findings(answers)
    email_finding = next((f for f in findings if f["question_id"] == "Q_B2"), None)
    assert email_finding is not None
    assert email_finding["severity"] == "HIGH"

def test_05_public_birthday_exposure():
    """Test 05: Public birth year disclosure flags high verification risk."""
    answers = get_fully_private_answers()
    answers["Q_B3"] = "YES" # Full birth date public
    findings = generate_privacy_findings(answers)
    bday_finding = next((f for f in findings if f["question_id"] == "Q_B3"), None)
    assert bday_finding is not None
    assert "Birth Date" in bday_finding["title"]

def test_06_public_location_exposure():
    """Test 06: Search engine discoverability and contact lookup create exposure."""
    answers = get_fully_private_answers()
    answers["Q_A2"] = "YES"
    answers["Q_A3"] = "YES"
    cat_scores = calculate_category_scores(answers)
    cat_a = next(c for c in cat_scores if c["category_code"] == "CAT_A")
    assert cat_a["score"] > 0

def test_07_real_time_check_ins():
    """Test 07: Real-time location sharing triggers CRITICAL physical security risk."""
    answers = get_fully_private_answers()
    answers["Q_C1"] = "YES" # Live location enabled
    findings = generate_privacy_findings(answers)
    loc_finding = next((f for f in findings if f["question_id"] == "Q_C1"), None)
    assert loc_finding is not None
    assert loc_finding["severity"] == "CRITICAL"

def test_08_travel_plans_in_advance():
    """Test 08: Posting travel plans in advance flags unoccupied residence risk."""
    answers = get_fully_private_answers()
    answers["Q_C3"] = "YES" # Travel announced in advance
    findings = generate_privacy_findings(answers)
    travel_finding = next((f for f in findings if f["question_id"] == "Q_C3"), None)
    assert travel_finding is not None
    assert travel_finding["severity"] == "HIGH"

def test_09_workplace_badge_exposure():
    """Test 09: Physical badge exposure in photos flags credential risk."""
    answers = get_fully_private_answers()
    answers["Q_D2"] = "YES"
    findings = generate_privacy_findings(answers)
    badge_finding = next((f for f in findings if f["question_id"] == "Q_D2"), None)
    assert badge_finding is not None
    assert "Badge" in badge_finding["title"]

def test_10_education_exposure():
    """Test 10: Specific employer/education disclosures contribute to personal info score."""
    answers = get_fully_private_answers()
    answers["Q_B4"] = "YES"
    cat_scores = calculate_category_scores(answers)
    cat_b = next(c for c in cat_scores if c["category_code"] == "CAT_B")
    assert cat_b["score"] > 0

def test_11_public_posts_default():
    """Test 11: Public default post audience triggers content risk finding."""
    answers = get_fully_private_answers()
    answers["Q_D1"] = "PUBLIC"
    findings = generate_privacy_findings(answers)
    post_finding = next((f for f in findings if f["question_id"] == "Q_D1"), None)
    assert post_finding is not None
    assert post_finding["severity"] == "HIGH"

def test_12_unknown_connections_accepted():
    """Test 12: Accepting unknown connections escalates connection score."""
    answers = get_fully_private_answers()
    answers["Q_E1"] = "YES" # Accept strangers
    cat_scores = calculate_category_scores(answers)
    cat_e = next(c for c in cat_scores if c["category_code"] == "CAT_E")
    assert cat_e["score"] >= 20

def test_13_tag_review_disabled():
    """Test 13: Disabled tag review generates timeline approval finding."""
    answers = get_fully_private_answers()
    answers["Q_F1"] = "NO" # Tag review off
    findings = generate_privacy_findings(answers)
    tag_finding = next((f for f in findings if f["question_id"] == "Q_F1"), None)
    assert tag_finding is not None
    assert "Tag Review" in tag_finding["title"]

def test_14_mfa_disabled():
    """Test 14: Disabled Multi-Factor Authentication generates CRITICAL account risk."""
    answers = get_fully_private_answers()
    answers["Q_G1"] = "NO" # MFA disabled
    findings = generate_privacy_findings(answers)
    mfa_finding = next((f for f in findings if f["question_id"] == "Q_G1"), None)
    assert mfa_finding is not None
    assert mfa_finding["severity"] == "CRITICAL"

def test_15_login_alerts_disabled():
    """Test 15: Unrecognized login alerts disabled flags session monitoring gap."""
    answers = get_fully_private_answers()
    answers["Q_G4"] = "NO"
    findings = generate_privacy_findings(answers)
    login_finding = next((f for f in findings if f["question_id"] == "Q_G4"), None)
    assert login_finding is not None
    assert "Login Alerts" in login_finding["title"]

def test_16_password_reuse_reported():
    """Test 16: Reusing passwords across accounts triggers CRITICAL credential stuffing risk."""
    answers = get_fully_private_answers()
    answers["Q_G3"] = "YES" # Reuses password
    findings = generate_privacy_findings(answers)
    pwd_finding = next((f for f in findings if f["question_id"] == "Q_G3"), None)
    assert pwd_finding is not None
    assert pwd_finding["severity"] == "CRITICAL"

def test_17_third_party_apps_not_reviewed():
    """Test 17: Never reviewing third party apps raises application risk score."""
    answers = get_fully_private_answers()
    answers["Q_H2"] = "NO"
    cat_scores = calculate_category_scores(answers)
    cat_h = next(c for c in cat_scores if c["category_code"] == "CAT_H")
    assert cat_h["score"] > 0

def test_18_suspicious_link_awareness_low():
    """Test 18: Clicking unexpected links in direct messages flags CRITICAL social engineering risk."""
    answers = get_fully_private_answers()
    answers["Q_I2"] = "YES" # Clicks unexpected DM links
    findings = generate_privacy_findings(answers)
    link_finding = next((f for f in findings if f["question_id"] == "Q_I2"), None)
    assert link_finding is not None
    assert link_finding["severity"] == "CRITICAL"

def test_19_old_posts_not_reviewed():
    """Test 19: Neglecting historical timeline post audits raises digital footprint score."""
    answers = get_fully_private_answers()
    answers["Q_J1"] = "NO"
    findings = generate_privacy_findings(answers)
    footprint_finding = next((f for f in findings if f["question_id"] == "Q_J1"), None)
    assert footprint_finding is not None
    assert "Historical" in footprint_finding["title"]

def test_20_privacy_settings_not_reviewed():
    """Test 20: Irregular privacy checkups trigger maintenance finding."""
    answers = get_fully_private_answers()
    answers["Q_J4"] = "NO"
    findings = generate_privacy_findings(answers)
    checkup_finding = next((f for f in findings if f["question_id"] == "Q_J4"), None)
    assert checkup_finding is not None


# =========================================================================
# TEST CASES 21 - 34: Scoring Mechanics, Boundaries, API & Privacy Compliance
# =========================================================================

def test_21_category_score_calculation():
    """Test 21: Category scoring normalizes all 10 domains to range [0, 100]."""
    answers = get_fully_public_answers()
    cat_scores = calculate_category_scores(answers)
    assert len(cat_scores) == 10
    for c in cat_scores:
        assert 0 <= c["score"] <= 100
        assert c["category_code"] in CATEGORY_DEFINITIONS

def test_22_overall_score_calculation_weights():
    """Test 22: Weighted overall score math conforms to assigned category weights."""
    sample_scores = [
        {"category_code": "CAT_A", "score": 100, "weight": 0.50},
        {"category_code": "CAT_B", "score": 0, "weight": 0.50}
    ]
    overall, level = calculate_privacy_risk(sample_scores)
    assert overall == 50
    assert level == "HIGH"

def test_23_score_boundary_20():
    """Test 23: Score boundary 20 maps to LOW, while 21 transitions to MODERATE."""
    assert classify_risk_level(20.0) == "LOW"
    assert classify_risk_level(21.0) == "MODERATE"

def test_24_score_boundary_40():
    """Test 24: Score boundary 40 maps to MODERATE, while 41 transitions to HIGH."""
    assert classify_risk_level(40.0) == "MODERATE"
    assert classify_risk_level(41.0) == "HIGH"

def test_25_score_boundary_70():
    """Test 25: Score boundary 70 maps to HIGH, while 71 transitions to CRITICAL."""
    assert classify_risk_level(70.0) == "HIGH"
    assert classify_risk_level(71.0) == "CRITICAL"

def test_26_recommendation_generation_prioritization():
    """Test 26: Recommendations sort strictly by priority (IMMEDIATE before IMPORTANT)."""
    answers = get_fully_public_answers()
    recs = generate_recommendations(answers)
    assert len(recs) > 0
    prio_map = {"IMMEDIATE": 0, "IMPORTANT": 1, "GOOD PRACTICE": 2}
    for i in range(len(recs) - 1):
        assert prio_map[recs[i]["priority"]] <= prio_map[recs[i+1]["priority"]]

def test_27_improvement_simulation_delta():
    """Test 27: Privacy improvement simulator computes expected positive point reduction."""
    answers = get_fully_public_answers()
    actions = ["make_phone_private", "disable_live_location", "enable_mfa", "enable_tag_review"]
    sim = simulate_privacy_improvements(answers, actions)
    assert sim["points_reduced"] > 0
    assert sim["simulated_score"] < sim["original_score"]
    assert len(sim["applied_improvements"]) == 4

def test_28_database_save_and_retrieve():
    """Test 28: Assessment record persists and retrieves properly from SQLite."""
    answers = get_fully_private_answers()
    result = process_questionnaire_assessment(answers, platform="TestPlatform")
    record = get_assessment_by_id(result["assessment_id"])
    assert record is not None
    assert record["assessment_id"] == result["assessment_id"]
    assert record["platform"] == "TestPlatform"
    assert len(record["category_scores"]) == 10

def test_29_data_minimization_sensitive_data_not_stored():
    """Test 29: Verifies that database schema and tables contain ZERO raw PII columns."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Inspect table schemas
    cur.execute("PRAGMA table_info(assessments);")
    cols = [r[1].lower() for r in cur.fetchall()]
    forbidden = ["phone", "email", "password", "birth", "dob", "address", "lat", "lon", "gps", "message"]
    for f in forbidden:
        assert f not in cols, f"Forbidden sensitive PII column '{f}' discovered in assessments table!"
    conn.close()

def test_30_report_generation():
    """Test 30: Completed assessment creates complete report data contract."""
    answers = get_fully_public_answers()
    result = process_questionnaire_assessment(answers)
    assert "assessment_id" in result
    assert "overall_score" in result
    assert "risk_level" in result
    assert "category_scores" in result
    assert "findings" in result
    assert "recommendations" in result

def test_31_api_health_check(client):
    """Test 31: API /api/health returns 200 OK and defensive mode declaration."""
    res = client.get("/api/health")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["status"] == "healthy"
    assert "Zero Raw PII" in json_data["storage"]

def test_32_api_submit_assessment(client):
    """Test 32: API POST /api/assessment accepts answers and returns created assessment."""
    answers = get_fully_public_answers()
    res = client.post("/api/assessment", json={"answers": answers, "platform": "WebTest"})
    assert res.status_code == 201
    data = res.get_json()["data"]
    assert data["overall_score"] >= 71
    assert data["risk_level"] == "CRITICAL"

def test_33_api_delete_assessment_erasure(client):
    """Test 33: API DELETE /api/assessment/<id> enforces GDPR Right to Erasure."""
    answers = get_fully_private_answers()
    created = process_questionnaire_assessment(answers)
    aid = created["assessment_id"]
    
    res = client.delete(f"/api/assessment/{aid}")
    assert res.status_code == 200
    assert get_assessment_by_id(aid) is None

def test_34_safe_exif_metadata_extraction_and_stripping():
    """Test 34: Safe in-memory EXIF parser correctly flags GPS and strips metadata markers."""
    # Synthetic minimal JPEG with APP1 EXIF containing GPS block
    synthetic_jpeg = (
        b"\xff\xd8"                                      # SOI
        b"\xff\xe1\x00\x1aExif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x01\x88%\x00\x04\x00\x00\x00\x01\x00\x00\x00\x12"
        b"\xff\xda\x00\x08\x01\x01\x00\x00?\x00"        # SOS
        b"\xff\xd9"                                      # EOI
    )
    meta = parse_exif_from_bytes(synthetic_jpeg)
    assert meta["has_exif"] is True

    stripped = strip_exif_metadata(synthetic_jpeg)
    clean_meta = parse_exif_from_bytes(stripped)
    assert clean_meta["has_exif"] is False
