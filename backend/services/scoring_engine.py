"""
Social Media Privacy Risk Assessment Framework
Privacy Feature Extraction and Risk Scoring Engine
===================================================
Converts self-reported privacy questionnaire responses or synthetic JSON profile data
into normalized numerical privacy risk metrics (0-100).

Scale:
  0 - 20:   LOW RISK (Minimal exposure, strong defensive hygiene)
  21 - 40:  MODERATE RISK (Standard exposure, minor configuration gaps)
  41 - 70:  HIGH RISK (Substantial exposure, potential vector for profiling/phishing)
  71 - 100: CRITICAL RISK (Acute exposure, immediate risk of takeover/stalking/doxxing)

Note: Weights and thresholds are educational defense-in-depth assumptions.
"""

import re
from typing import Dict, Any, List, Tuple
from backend.utils.questionnaire_data import CATEGORY_DEFINITIONS, QUESTION_MAP, QUESTIONS

# Configurable Category Weights (Sum to 1.0)
DEFAULT_CATEGORY_WEIGHTS = {
    "CAT_A": 0.10,  # Profile Visibility
    "CAT_B": 0.15,  # Personal Information
    "CAT_C": 0.15,  # Location Privacy
    "CAT_D": 0.10,  # Posts & Content
    "CAT_E": 0.10,  # Friends & Followers
    "CAT_F": 0.05,  # Tagging & Mentions
    "CAT_G": 0.15,  # Account Security & MFA
    "CAT_H": 0.05,  # Third-Party Applications
    "CAT_I": 0.10,  # Messaging & Social Engineering
    "CAT_J": 0.05   # Digital Footprint
}

def classify_risk_level(score: float) -> str:
    """Classifies risk score into standard risk tier."""
    if score <= 20.0:
        return "LOW"
    elif score <= 40.0:
        return "MODERATE"
    elif score <= 70.0:
        return "HIGH"
    else:
        return "CRITICAL"

def extract_privacy_features(answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Transforms questionnaire answers into structured numeric privacy-risk features.
    Returns:
      Dictionary containing raw feature values, risk weights, and category mappings.
    """
    features = {}

    for qid, qdef in QUESTION_MAP.items():
        user_val = answers.get(qid, "NO")
        # Lookup assigned risk points for option
        matched_opt = next((opt for opt in qdef["options"] if opt["value"] == user_val), None)
        points = matched_opt["risk_points"] if matched_opt else 0

        features[qid] = {
            "value": user_val,
            "risk_points": points,
            "category": qdef["category_code"],
            "severity": qdef.get("severity", "LOW")
        }

    return features

def calculate_category_scores(answers: Dict[str, str], custom_weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
    """
    Calculates 0-100 risk score for each of the 10 privacy categories.
    Each category score represents the normalized risk (0 = lowest risk, 100 = highest risk).
    """
    weights = custom_weights or DEFAULT_CATEGORY_WEIGHTS
    category_buckets: Dict[str, List[int]] = {cat_code: [] for cat_code in CATEGORY_DEFINITIONS}

    for qid, qdef in QUESTION_MAP.items():
        cat_code = qdef["category_code"]
        user_val = answers.get(qid)
        if not user_val:
            continue

        matched_opt = next((opt for opt in qdef["options"] if opt["value"] == user_val), None)
        points = matched_opt["risk_points"] if matched_opt else 0
        category_buckets[cat_code].append(points)

    category_results = []
    for cat_code, cat_info in CATEGORY_DEFINITIONS.items():
        points_list = category_buckets.get(cat_code, [])
        if points_list:
            cat_score = round(sum(points_list) / len(points_list))
        else:
            cat_score = 0

        cat_weight = weights.get(cat_code, cat_info["weight"])

        category_results.append({
            "category_code": cat_code,
            "category_name": cat_info["name"],
            "score": min(100, max(0, cat_score)),
            "weight": cat_weight,
            "risk_level": classify_risk_level(cat_score),
            "description": cat_info["description"]
        })

    return category_results

def calculate_privacy_risk(category_scores: List[Dict[str, Any]]) -> Tuple[int, str]:
    """
    Combines individual category scores into an overall privacy risk score (0-100)
    using normalized weights.
    Returns: (overall_score, risk_level)
    """
    total_weighted_score = 0.0
    total_weight = 0.0

    for cat in category_scores:
        score = cat["score"]
        weight = cat["weight"]
        total_weighted_score += score * weight
        total_weight += weight

    if total_weight > 0:
        overall = round(total_weighted_score / total_weight)
    else:
        overall = 0

    overall = max(0, min(100, overall))
    level = classify_risk_level(overall)
    return overall, level

# =========================================================================
# JSON Profile & Posts Risk Engine (For file-based input / Step 1-9 schema)
# =========================================================================

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\s-]?){9,}")
WORK_KEYWORDS = {"badge", "id card", "hq", "office", "3rd floor", "4th floor", "desk", "shift", "cubicle"}
CHILD_HINTS = {"my kid", "my child", "daughter", "son", "#kids", "#school", "kindergarten"}
ROUTINE_HINTS = {"every day", "daily", "7am run", "morning commute", "school drop", "every morning"}

def score_profile_and_posts(profile: Dict[str, Any], posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates synthetic profile and posts JSON payloads against privacy heuristics.
    Returns calculated score, category breakdown, and findings list.
    """
    findings = []
    
    # 1. PII Exposure (Max 25 pts)
    pii_points = 0
    text_corpus = f"{profile.get('bio', '')} {profile.get('email', '')} {profile.get('phone', '')}"
    if EMAIL_RE.search(text_corpus):
        pii_points += 10
        findings.append({
            "category_code": "CAT_B",
            "category_name": "Personal Information",
            "finding_type": "EXPOSURE",
            "severity": "HIGH",
            "title": "Email Address Publicly Visible",
            "description": "Email found in profile bio or contact fields. Enables phishing and credential stuffing.",
            "fix": "Remove personal email from public view; use a platform contact button or alias."
        })
    if PHONE_RE.search(text_corpus):
        pii_points += 12
        findings.append({
            "category_code": "CAT_B",
            "category_name": "Personal Information",
            "finding_type": "EXPOSURE",
            "severity": "CRITICAL",
            "title": "Phone Number Exposed in Profile",
            "description": "Phone number is discoverable in profile bio, facilitating smishing, SIM-swapping, and harassment.",
            "fix": "Remove phone number immediately from public bio; set visibility to private."
        })
    if profile.get("location"):
        pii_points += 5
        findings.append({
            "category_code": "CAT_B",
            "category_name": "Personal Information",
            "finding_type": "EXPOSURE",
            "severity": "MEDIUM",
            "title": "City-Level Location Exposed",
            "description": "Residential city is publicly declared on profile.",
            "fix": "Broaden location to country-level or remove location string entirely."
        })
    cat_b_score = min(100, round((min(25, pii_points) / 25) * 100))

    # 2. Geolocation & Routine Trails (Max 20 pts)
    geo_points = 0
    for p in posts:
        pid = p.get("id", "post")
        if p.get("geo"):
            geo_points += 6
            findings.append({
                "category_code": "CAT_C",
                "category_name": "Location Privacy",
                "finding_type": "LOCATION_LEAK",
                "severity": "HIGH",
                "title": f"Precise Geotag in {pid}",
                "description": f"Post {pid} includes latitude/longitude coordinates or specific venue tags.",
                "fix": "Turn off location tagging when posting; strip historical geotags."
            })
        if p.get("media", {}).get("exif", {}).get("created_local"):
            geo_points += 4
            findings.append({
                "category_code": "CAT_C",
                "category_name": "Location Privacy",
                "finding_type": "METADATA_LEAK",
                "severity": "MEDIUM",
                "title": f"EXIF Timestamp / Device Metadata in {pid}",
                "description": f"Image file contains camera make/model and creation timestamp in post {pid}.",
                "fix": "Strip EXIF metadata using privacy tools prior to uploading."
            })
        ptext = (p.get("text") or "").lower()
        if any(h in ptext for h in ROUTINE_HINTS):
            geo_points += 5
            findings.append({
                "category_code": "CAT_C",
                "category_name": "Location Privacy",
                "finding_type": "ROUTINE_LEAK",
                "severity": "MEDIUM",
                "title": f"Daily Routine Pattern Disclosed in {pid}",
                "description": f"Text in post {pid} reveals recurring schedule, workout route, or commute timing.",
                "fix": "Avoid posting predictable daily time/place patterns."
            })
    cat_c_score = min(100, round((min(20, geo_points) / 20) * 100))

    # 3. Children / Minors & Workplace (Max 25 pts)
    content_points = 0
    for p in posts:
        pid = p.get("id", "post")
        if p.get("media", {}).get("is_child_present"):
            content_points += 15
            findings.append({
                "category_code": "CAT_D",
                "category_name": "Posts & Content",
                "finding_type": "MINOR_EXPOSURE",
                "severity": "CRITICAL",
                "title": f"Minor / Child Present in {pid}",
                "description": f"Public post {pid} contains imagery of children, posing sharenting and safety concerns.",
                "fix": "Switch post to close friends only, or blur faces of minors."
            })
        ptext = (p.get("text") or "").lower()
        if any(w in ptext for w in WORK_KEYWORDS):
            content_points += 8
            findings.append({
                "category_code": "CAT_D",
                "category_name": "Posts & Content",
                "finding_type": "WORK_LEAK",
                "severity": "HIGH",
                "title": f"Workplace / Access Badge Detail in {pid}",
                "description": f"Post {pid} reveals company office floor, access badges, or internal desk setups.",
                "fix": "Avoid posting employee ID badges, floor plans, or internal monitor screens."
            })
    cat_d_score = min(100, round((min(25, content_points) / 25) * 100))

    # 4. Privacy Settings (Max 20 pts)
    priv = profile.get("privacy", {})
    priv_points = 0
    if not priv.get("account_private", False):
        priv_points += 10
        findings.append({
            "category_code": "CAT_A",
            "category_name": "Profile Visibility",
            "finding_type": "OPEN_PROFILE",
            "severity": "HIGH",
            "title": "Account is Publicly Accessible",
            "description": "Account is not set to Private; posts and profile details are viewable by any internet user.",
            "fix": "Set account to Private to require follow requests before viewing content."
        })
    if priv.get("show_activity", True):
        priv_points += 5
        findings.append({
            "category_code": "CAT_A",
            "category_name": "Profile Visibility",
            "finding_type": "ACTIVITY_STATUS",
            "severity": "LOW",
            "title": "Activity / Last-Seen Status Enabled",
            "description": "Active status reveals when you are online to contacts and strangers.",
            "fix": "Disable 'Show Activity Status' in privacy options."
        })
    if priv.get("allow_message_requests", True):
        priv_points += 5
        findings.append({
            "category_code": "CAT_I",
            "category_name": "Messaging & Social Engineering",
            "finding_type": "OPEN_DM",
            "severity": "MEDIUM",
            "title": "Open Message Requests from Strangers",
            "description": "Anyone can send message requests, creating susceptibility to DM phishing and scams.",
            "fix": "Limit message requests to friends of friends or close contacts."
        })
    cat_a_score = min(100, round((min(15, priv_points) / 15) * 100))

    # 5. Linkage & External Footprint (Max 10 pts)
    link_points = 0
    for url in profile.get("links", []):
        if "linktr.ee" in url or "pastebin" in url:
            link_points += 6
            findings.append({
                "category_code": "CAT_J",
                "category_name": "Digital Footprint",
                "finding_type": "LINKAGE_RISK",
                "severity": "MEDIUM",
                "title": f"Link Aggregator / Pastebin Linked: {url}",
                "description": "Link-in-bio aggregators frequently point to external unvetted contact lists and documents.",
                "fix": "Audit bio link destinations to ensure they do not expose sensitive resumes or spreadsheets."
            })
        if "github.com" in url:
            link_points += 4
            findings.append({
                "category_code": "CAT_J",
                "category_name": "Digital Footprint",
                "finding_type": "CORRELATION_RISK",
                "severity": "LOW",
                "title": "Developer Profile Cross-Linked",
                "description": "Public GitHub account linked to personal profile allows code and commit correlation.",
                "fix": "Ensure linked developer repositories contain no accidentally committed secrets or API tokens."
            })
    cat_j_score = min(100, round((min(10, link_points) / 10) * 100))

    # Compile category structures
    category_scores = [
        {"category_code": "CAT_A", "category_name": "Profile Visibility", "score": cat_a_score, "weight": 0.20, "risk_level": classify_risk_level(cat_a_score)},
        {"category_code": "CAT_B", "category_name": "Personal Information", "score": cat_b_score, "weight": 0.25, "risk_level": classify_risk_level(cat_b_score)},
        {"category_code": "CAT_C", "category_name": "Location Privacy", "score": cat_c_score, "weight": 0.25, "risk_level": classify_risk_level(cat_c_score)},
        {"category_code": "CAT_D", "category_name": "Posts & Content", "score": cat_d_score, "weight": 0.20, "risk_level": classify_risk_level(cat_d_score)},
        {"category_code": "CAT_J", "category_name": "Digital Footprint", "score": cat_j_score, "weight": 0.10, "risk_level": classify_risk_level(cat_j_score)}
    ]

    overall_score, risk_level = calculate_privacy_risk(category_scores)

    return {
        "overall_score": overall_score,
        "risk_level": risk_level,
        "category_scores": category_scores,
        "findings": findings
    }
