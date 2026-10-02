"""
Social Media Privacy Risk Assessment Framework
Security Recommendation Engine
===================================================
Produces personalized, prioritized, and actionable privacy recommendations
aligned with defense-in-depth principles.

Priorities:
  - IMMEDIATE: Stop acute active exposure (Phone in bio, live GPS, disabled MFA, OTP sharing).
  - IMPORTANT: Critical attack surface reduction (Public birth year, unvetted connections, tag review).
  - GOOD PRACTICE: Continuous hygiene (Biannual audits, search indexing, session cleanups).
"""

from typing import Dict, Any, List
from backend.utils.questionnaire_data import QUESTION_MAP

PRIORITY_ORDER = {
    "IMMEDIATE": 0,
    "IMPORTANT": 1,
    "GOOD PRACTICE": 2
}

def generate_recommendations(answers: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Translates triggered risk findings into personalized remediation actions.
    Returns: List of recommendations ordered by priority.
    """
    recommendations = []
    seen_titles = set()

    for qid, user_val in answers.items():
        if qid not in QUESTION_MAP:
            continue

        qdef = QUESTION_MAP[qid]
        risk_triggers = qdef.get("risk_trigger", [])

        if user_val in risk_triggers:
            rec_title = qdef.get("recommendation_title", "Review Privacy Setting")
            if rec_title in seen_titles:
                continue
            seen_titles.add(rec_title)

            recommendations.append({
                "question_id": qid,
                "category_code": qdef["category_code"],
                "category_name": qdef["category_name"],
                "priority": qdef.get("priority", "GOOD PRACTICE"),
                "title": rec_title,
                "action_steps": qdef.get("recommendation_text", "Update privacy options in account settings."),
                "impact_estimate": "High reduction in attack surface" if qdef.get("priority") == "IMMEDIATE" else "Substantial defense enhancement"
            })

    # Sort by priority
    recommendations.sort(key=lambda x: PRIORITY_ORDER.get(x["priority"], 99))
    return recommendations
