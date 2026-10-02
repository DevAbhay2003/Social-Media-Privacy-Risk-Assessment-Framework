"""
Social Media Privacy Risk Assessment Framework
Privacy Improvement Simulator
===================================================
Simulates the impact of applying targeted privacy and security controls.
Demonstrates risk reduction math, illustrating how simple defensive hygiene
significantly diminishes exposure metrics.

Disclaimer:
This calculation represents a mathematical framework simulation for educational
guidance, not a guarantee of absolute security or immunity from cyber threats.
"""

from typing import Dict, Any, List
from backend.services.scoring_engine import calculate_category_scores, calculate_privacy_risk, classify_risk_level

# Standard simulated improvement controls mapped to question IDs and ideal safe answers
IMPROVEMENT_ACTION_MAP = {
    "make_phone_private": {
        "label": "Hide phone number from public bio/profile",
        "question_id": "Q_B1",
        "target_value": "NO",
        "category": "CAT_B"
    },
    "hide_email": {
        "label": "Hide personal email address from public bio",
        "question_id": "Q_B2",
        "target_value": "NO",
        "category": "CAT_B"
    },
    "hide_birth_date": {
        "label": "Hide birth year and set birthday to private",
        "question_id": "Q_B3",
        "target_value": "NO",
        "category": "CAT_B"
    },
    "disable_live_location": {
        "label": "Disable real-time location sharing and Snap Map",
        "question_id": "Q_C1",
        "target_value": "NO",
        "category": "CAT_C"
    },
    "stop_posting_travel": {
        "label": "Post vacation and travel updates only after returning",
        "question_id": "Q_C3",
        "target_value": "NO",
        "category": "CAT_C"
    },
    "make_profile_private": {
        "label": "Set profile visibility to Private / Approved Friends Only",
        "question_id": "Q_A1",
        "target_value": "PRIVATE",
        "category": "CAT_A"
    },
    "enable_tag_review": {
        "label": "Enable Tag Review before tagged posts appear on profile",
        "question_id": "Q_F1",
        "target_value": "YES",
        "category": "CAT_F"
    },
    "reject_unknown_connections": {
        "label": "Vet and decline connection requests from strangers",
        "question_id": "Q_E1",
        "target_value": "NO",
        "category": "CAT_E"
    },
    "enable_mfa": {
        "label": "Enable Multi-Factor Authentication with Authenticator App",
        "question_id": "Q_G1",
        "target_value": "YES",
        "category": "CAT_G",
        "secondary_override": {"Q_G2": "APP_KEY"}
    },
    "stop_password_reuse": {
        "label": "Use unique passwords with a password manager",
        "question_id": "Q_G3",
        "target_value": "NO",
        "category": "CAT_G"
    },
    "enable_login_alerts": {
        "label": "Enable unrecognized login notifications",
        "question_id": "Q_G4",
        "target_value": "YES",
        "category": "CAT_G"
    },
    "review_third_party_apps": {
        "label": "Revoke permissions for unused third-party OAuth apps",
        "question_id": "Q_H2",
        "target_value": "YES",
        "category": "CAT_H"
    },
    "restrict_direct_messages": {
        "label": "Restrict incoming DMs to followed friends only",
        "question_id": "Q_I1",
        "target_value": "NO",
        "category": "CAT_I"
    },
    "audit_historical_posts": {
        "label": "Purge or archive old posts older than 12 months",
        "question_id": "Q_J1",
        "target_value": "YES",
        "category": "CAT_J"
    }
}

def simulate_privacy_improvements(
    current_answers: Dict[str, str],
    selected_actions: List[str]
) -> Dict[str, Any]:
    """
    Applies simulated setting improvements to a copy of current answers
    and recalculates category and overall scores.
    """
    # 1. Calculate baseline current score
    orig_cat_scores = calculate_category_scores(current_answers)
    orig_overall, orig_level = calculate_privacy_risk(orig_cat_scores)

    # 2. Clone answers and apply selected improvements
    simulated_answers = dict(current_answers)
    applied_changes = []

    for action_key in selected_actions:
        if action_key not in IMPROVEMENT_ACTION_MAP:
            continue

        meta = IMPROVEMENT_ACTION_MAP[action_key]
        qid = meta["question_id"]
        target = meta["target_value"]

        # Only count if the setting is actually changing
        current_val = simulated_answers.get(qid)
        if current_val != target:
            simulated_answers[qid] = target
            applied_changes.append(meta["label"])

            # Handle secondary overrides (e.g., Q_G2 when Q_G1 is enabled)
            if "secondary_override" in meta:
                for sqid, sval in meta["secondary_override"].items():
                    simulated_answers[sqid] = sval

    # 3. Recalculate simulated scores
    sim_cat_scores = calculate_category_scores(simulated_answers)
    sim_overall, sim_level = calculate_privacy_risk(sim_cat_scores)

    # 4. Compute delta
    points_reduced = max(0, orig_overall - sim_overall)
    percent_reduction = round((points_reduced / orig_overall * 100) if orig_overall > 0 else 0, 1)

    return {
        "original_score": orig_overall,
        "original_risk_level": orig_level,
        "simulated_score": sim_overall,
        "simulated_risk_level": sim_level,
        "points_reduced": points_reduced,
        "percent_reduction": percent_reduction,
        "applied_improvements_count": len(applied_changes),
        "applied_improvements": applied_changes,
        "category_comparison": [
            {
                "category_code": o["category_code"],
                "category_name": o["category_name"],
                "original_score": o["score"],
                "simulated_score": s["score"],
                "delta": o["score"] - s["score"]
            }
            for o, s in zip(orig_cat_scores, sim_cat_scores)
        ],
        "disclaimer": "This is an educational risk framework simulation. Real-world security involves multiple defense-in-depth layers beyond platform configuration."
    }
