"""
Social Media Privacy Risk Assessment Framework
Input Validation and Defensive Sanitization
===================================================
Provides defensive input validation to prevent injection, malformed payloads,
and excessive data ingestion, adhering strictly to Data Minimization.
"""

import re
from typing import Dict, Any, List, Tuple
from backend.utils.questionnaire_data import QUESTION_MAP, QUESTIONS

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
URL_REGEX = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

def validate_questionnaire_submission(answers: Dict[str, Any]) -> Tuple[bool, str, Dict[str, str]]:
    """
    Validates questionnaire answers submitted by user.
    Ensures:
    1. Answers is a dictionary.
    2. Minimum threshold of answered questions is met.
    3. All question keys are valid known question IDs.
    4. Selected option values are legal choices for the question.
    Returns: (is_valid, error_message, sanitized_answers)
    """
    if not isinstance(answers, dict):
        return False, "Payload must be a JSON object of question answers.", {}

    sanitized = {}
    valid_ids = set(QUESTION_MAP.keys())

    for qid, val in answers.items():
        if qid not in valid_ids:
            continue # Ignore unknown keys safely

        # Convert to string and sanitize
        clean_val = str(val).strip().upper()
        q_def = QUESTION_MAP[qid]
        allowed_values = {opt["value"] for opt in q_def["options"]}

        if clean_val not in allowed_values:
            return False, f"Invalid response value '{clean_val}' for question {qid}.", {}

        sanitized[qid] = clean_val

    # Ensure at least 50% of the questions are answered for a meaningful assessment
    if len(sanitized) < 20:
        return False, f"At least 20 questions must be answered for a reliable assessment (received {len(sanitized)}).", {}

    return True, "", sanitized

def validate_profile_payload(profile: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates synthetic or demo profile JSON structure.
    Does NOT store raw sensitive PII; only validates schema structure.
    """
    if not isinstance(profile, dict):
        return False, "Profile must be a JSON object.", {}

    sanitized = {
        "platform": str(profile.get("platform", "generic")).strip().lower()[:30],
        "username": str(profile.get("username", "anonymous_user")).strip()[:50],
        "display_name": str(profile.get("display_name", "")).strip()[:100],
        "bio": str(profile.get("bio", "")).strip()[:500],
        "website": str(profile.get("website", "")).strip()[:200],
        "email": str(profile.get("email", "")).strip()[:100] if profile.get("email") else "",
        "phone": str(profile.get("phone", "")).strip()[:30] if profile.get("phone") else "",
        "location": str(profile.get("location", "")).strip()[:100] if profile.get("location") else "",
        "privacy": profile.get("privacy", {}),
        "links": [str(l)[:200] for l in profile.get("links", []) if isinstance(l, str)][:20]
    }

    if not isinstance(sanitized["privacy"], dict):
        sanitized["privacy"] = {}

    return True, "", sanitized

def validate_posts_payload(posts: Any) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Validates synthetic posts array. Caps processing to 100 posts to prevent DoS.
    """
    if not isinstance(posts, list):
        return False, "Posts must be a JSON list.", []

    sanitized_posts = []
    for p in posts[:100]:
        if not isinstance(p, dict):
            continue
        sanitized_posts.append({
            "id": str(p.get("id", f"post_{len(sanitized_posts)+1}"))[:50],
            "text": str(p.get("text", ""))[:1000],
            "created_at": str(p.get("created_at", ""))[:50],
            "hashtags": [str(h)[:50] for h in p.get("hashtags", []) if isinstance(h, str)][:20],
            "mentions": [str(m)[:50] for m in p.get("mentions", []) if isinstance(m, str)][:20],
            "geo": p.get("geo") if isinstance(p.get("geo"), dict) else None,
            "media": p.get("media") if isinstance(p.get("media"), dict) else {}
        })

    return True, "", sanitized_posts
