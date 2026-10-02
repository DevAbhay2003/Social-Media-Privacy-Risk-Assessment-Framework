"""
Social Media Privacy Risk Assessment Framework
Assessment Coordination Engine
===================================================
Coordinates the full defensive privacy risk evaluation pipeline:
Input Validation -> Feature Extraction -> Category Scoring -> Overall Scoring
-> Findings Generation -> Recommendation Engine -> Privacy-Preserving Persistence.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from backend.services.scoring_engine import (
    calculate_category_scores,
    calculate_privacy_risk,
    score_profile_and_posts,
    DEFAULT_CATEGORY_WEIGHTS
)
from backend.services.findings_engine import generate_privacy_findings, get_top_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.database import save_assessment_record, get_assessment_by_id

def process_questionnaire_assessment(
    answers: Dict[str, str],
    platform: str = "Cross-Platform",
    custom_weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Executes full assessment pipeline from questionnaire responses.
    """
    assessment_id = f"PRA-{uuid.uuid4().hex[:8].upper()}"

    # 1. Compute Category Scores
    cat_scores = calculate_category_scores(answers, custom_weights)

    # 2. Compute Overall Privacy Risk Score
    overall_score, risk_level = calculate_privacy_risk(cat_scores)

    # 3. Generate Findings
    findings = generate_privacy_findings(answers)

    # 4. Generate Actionable Recommendations
    recommendations = generate_recommendations(answers)

    # 5. Save to Database (Privacy by Design - NO raw PII stored)
    save_assessment_record(
        assessment_id=assessment_id,
        overall_score=overall_score,
        risk_level=risk_level,
        platform=platform,
        source_type="QUESTIONNAIRE",
        category_scores=cat_scores,
        findings=findings,
        recommendations=recommendations
    )

    return {
        "assessment_id": assessment_id,
        "overall_score": overall_score,
        "risk_level": risk_level,
        "platform": platform,
        "source_type": "QUESTIONNAIRE",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "category_scores": cat_scores,
        "findings": findings,
        "top_findings": get_top_findings(findings, 5),
        "recommendations": recommendations,
        "total_findings_count": len(findings),
        "total_recommendations_count": len(recommendations)
    }

def process_json_profile_assessment(
    profile: Dict[str, Any],
    posts: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Executes evaluation from synthetic profile and posts JSON payloads.
    """
    assessment_id = f"PRA-JSON-{uuid.uuid4().hex[:8].upper()}"
    res = score_profile_and_posts(profile, posts)

    # Map findings into recommendations
    recs = []
    for f in res["findings"]:
        recs.append({
            "category_code": f["category_code"],
            "priority": "IMMEDIATE" if f["severity"] == "CRITICAL" else ("IMPORTANT" if f["severity"] == "HIGH" else "GOOD PRACTICE"),
            "title": f"Remediate: {f['title']}",
            "action_steps": f.get("fix", "Review privacy settings.")
        })

    platform = profile.get("platform", "generic").capitalize()

    save_assessment_record(
        assessment_id=assessment_id,
        overall_score=res["overall_score"],
        risk_level=res["risk_level"],
        platform=platform,
        source_type="JSON_INGESTION",
        category_scores=res["category_scores"],
        findings=res["findings"],
        recommendations=recs
    )

    return {
        "assessment_id": assessment_id,
        "overall_score": res["overall_score"],
        "risk_level": res["risk_level"],
        "platform": platform,
        "source_type": "JSON_INGESTION",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "category_scores": res["category_scores"],
        "findings": res["findings"],
        "top_findings": res["findings"][:5],
        "recommendations": recs,
        "total_findings_count": len(res["findings"]),
        "total_recommendations_count": len(recs)
    }
