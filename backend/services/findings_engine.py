"""
Social Media Privacy Risk Assessment Framework
Privacy Findings Engine
===================================================
Identifies specific privacy weaknesses, misconfigurations, and oversharing
patterns from questionnaire responses or synthetic profile analyses.

Severities:
  - CRITICAL: Immediate direct threat (public phone, disabled MFA, live location, OTP sharing)
  - HIGH: Major exposure vector (public email, birth date, unknown connections, open DMs)
  - MEDIUM: Moderate exposure (search indexing, stale app access, workplace details)
  - LOW: Hygiene gap (avatar context, missing quarterly audits)
"""

from typing import Dict, Any, List
from backend.utils.questionnaire_data import QUESTION_MAP

SEVERITY_ORDER = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}

def generate_privacy_findings(answers: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Evaluates questionnaire answers and generates structured findings for detected gaps.
    Returns: List of findings sorted by severity.
    """
    findings = []

    for qid, user_val in answers.items():
        if qid not in QUESTION_MAP:
            continue

        qdef = QUESTION_MAP[qid]
        risk_triggers = qdef.get("risk_trigger", [])

        # Check if the user's answer triggers a vulnerability finding
        if user_val in risk_triggers:
            findings.append({
                "question_id": qid,
                "category_code": qdef["category_code"],
                "category_name": qdef["category_name"],
                "finding_type": "WEAK_CONFIGURATION",
                "severity": qdef.get("severity", "LOW"),
                "title": qdef.get("finding_title", "Privacy Weakness Detected"),
                "description": qdef.get("finding_desc", "Configured option creates unneeded privacy exposure."),
                "user_response": user_val
            })

    # Sort findings by severity (Critical first, then High, Medium, Low)
    findings.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 99))
    return findings

def get_top_findings(findings: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
    """Returns the top N most severe findings."""
    return findings[:limit]
