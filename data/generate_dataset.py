"""
Social Media Privacy Risk Assessment Framework
Synthetic Dataset Generator
===================================================
Generates a realistic, statistically sound synthetic dataset of 1,200 fictional
privacy assessment records for educational analysis, risk distribution modeling,
and dashboard reporting.

Complies strictly with Privacy by Design:
- Contains 100% synthetic fictional records.
- No real social media accounts, handles, or individuals are targeted or profiled.
- Demonstrates privacy risk correlations and mathematical scoring distributions.
"""

import os
import csv
import random

def calculate_synthetic_score(row: dict) -> tuple[int, str]:
    """
    Computes a deterministic, defensible risk score (0-100) based on simulated answers.
    Higher score indicates higher privacy risk / exposure.
    """
    score = 0

    # Profile Visibility (Weight: 10)
    if row["profile_visibility"] == "PUBLIC":
        score += 10
    elif row["profile_visibility"] == "FRIENDS_ONLY":
        score += 3
    # PRIVATE = 0

    # Personal Information Exposure (Weight: 15)
    if row["phone_public"] == "YES":
        score += 4
    if row["email_public"] == "YES":
        score += 3
    if row["birthday_public"] == "YES":
        score += 3
    if row["workplace_public"] == "YES":
        score += 3
    if row["relationship_public"] == "YES":
        score += 2

    # Location Privacy (Weight: 15)
    if row["location_public"] == "YES":
        score += 5
    if row["location_tagging"] == "YES":
        score += 5
    elif row["location_tagging"] == "SOMETIMES":
        score += 2
    if row["travel_posts"] == "YES":
        score += 5
    elif row["travel_posts"] == "SOMETIMES":
        score += 2

    # Posts & Content (Weight: 10)
    if row["posts_public"] == "PUBLIC":
        score += 7
    elif row["posts_public"] == "FRIENDS":
        score += 2
    if row["education_public"] == "YES":
        score += 3

    # Connections & Followers (Weight: 10)
    if row["unknown_connections"] == "YES":
        score += 10
    elif row["unknown_connections"] == "SOMETIMES":
        score += 5

    # Tagging Permissions (Weight: 5)
    if row["tag_review_enabled"] == "NO":
        score += 5
    elif row["tag_review_enabled"] == "NOT_SURE":
        score += 3

    # Authentication & Account Security (Weight: 15)
    if row["mfa_enabled"] == "NO":
        score += 8
    elif row["mfa_enabled"] == "NOT_SURE":
        score += 4
    if row["login_alerts_enabled"] == "NO":
        score += 4
    if row["password_reuse_reported"] == "YES":
        score += 3

    # Third-Party Apps (Weight: 5)
    if row["third_party_apps_reviewed"] == "NO":
        score += 5
    elif row["third_party_apps_reviewed"] == "NOT_SURE":
        score += 3

    # Social Engineering Susceptibility (Weight: 10)
    if row["suspicious_link_awareness"] == "LOW":
        score += 10
    elif row["suspicious_link_awareness"] == "MEDIUM":
        score += 5

    # Digital Footprint Management (Weight: 5)
    if row["old_posts_reviewed"] == "NO":
        score += 3
    if row["privacy_settings_reviewed"] == "NO":
        score += 2

    # Clamp score to [0, 100]
    final_score = max(0, min(100, score))

    if final_score <= 20:
        level = "LOW"
    elif final_score <= 40:
        level = "MODERATE"
    elif final_score <= 70:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return final_score, level

def generate_synthetic_dataset(num_records: int = 1200, output_path: str = None) -> str:
    """
    Generates fictional privacy assessments with correlated behavioral archetypes.
    Archetypes represent realistic user personas (Privacy Conscious, Average User, Casual Oversharer, High Exposure).
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "social_media_privacy_assessments.csv")

    random.seed(42)  # Deterministic seed for reproducibility

    records = []
    
    # Archetype distribution:
    # 25% Privacy Conscious, 40% Average User, 25% Casual Oversharer, 10% High Exposure
    personas = [
        {"name": "Conscious", "weight": 0.25},
        {"name": "Average", "weight": 0.40},
        {"name": "Oversharer", "weight": 0.25},
        {"name": "HighRisk", "weight": 0.10}
    ]

    for i in range(1, num_records + 1):
        pid = f"SYNTH-{i:05d}"
        persona_choice = random.choices(
            [p["name"] for p in personas],
            weights=[p["weight"] for p in personas]
        )[0]

        if persona_choice == "Conscious":
            # Low exposure settings
            profile_vis = random.choices(["PRIVATE", "FRIENDS_ONLY", "PUBLIC"], weights=[0.75, 0.20, 0.05])[0]
            phone_pub = "NO" if random.random() > 0.02 else "YES"
            email_pub = "NO" if random.random() > 0.08 else "YES"
            bday_pub = "NO" if random.random() > 0.10 else "YES"
            loc_pub = "NO" if random.random() > 0.05 else "YES"
            work_pub = "NO" if random.random() > 0.15 else "YES"
            edu_pub = "NO" if random.random() > 0.20 else "YES"
            rel_pub = "NO" if random.random() > 0.15 else "YES"
            posts_pub = "PRIVATE" if random.random() > 0.3 else "FRIENDS"
            loc_tag = "NO" if random.random() > 0.1 else "SOMETIMES"
            travel = "NO" if random.random() > 0.05 else "SOMETIMES"
            unknown_conn = "NO" if random.random() > 0.05 else "SOMETIMES"
            tag_rev = "YES" if random.random() > 0.1 else "NO"
            app_rev = "YES" if random.random() > 0.15 else "NO"
            mfa = "YES" if random.random() > 0.05 else "NO"
            login_alerts = "YES" if random.random() > 0.1 else "NO"
            pwd_reuse = "NO" if random.random() > 0.1 else "YES"
            link_aware = "HIGH" if random.random() > 0.1 else "MEDIUM"
            old_posts = "YES" if random.random() > 0.2 else "NO"
            priv_rev = "YES" if random.random() > 0.15 else "NO"

        elif persona_choice == "Average":
            # Moderate settings
            profile_vis = random.choices(["FRIENDS_ONLY", "PUBLIC", "PRIVATE"], weights=[0.60, 0.25, 0.15])[0]
            phone_pub = "NO" if random.random() > 0.15 else "YES"
            email_pub = "NO" if random.random() > 0.35 else "YES"
            bday_pub = "YES" if random.random() > 0.40 else "NO"
            loc_pub = "NO" if random.random() > 0.30 else "YES"
            work_pub = "YES" if random.random() > 0.40 else "NO"
            edu_pub = "YES" if random.random() > 0.35 else "NO"
            rel_pub = "YES" if random.random() > 0.45 else "NO"
            posts_pub = random.choices(["FRIENDS", "PUBLIC", "PRIVATE"], weights=[0.65, 0.25, 0.10])[0]
            loc_tag = random.choices(["SOMETIMES", "NO", "YES"], weights=[0.55, 0.30, 0.15])[0]
            travel = random.choices(["SOMETIMES", "NO", "YES"], weights=[0.50, 0.35, 0.15])[0]
            unknown_conn = random.choices(["SOMETIMES", "NO", "YES"], weights=[0.45, 0.45, 0.10])[0]
            tag_rev = random.choices(["YES", "NO", "NOT_SURE"], weights=[0.45, 0.40, 0.15])[0]
            app_rev = random.choices(["NO", "YES", "NOT_SURE"], weights=[0.50, 0.30, 0.20])[0]
            mfa = random.choices(["YES", "NO"], weights=[0.60, 0.40])[0]
            login_alerts = random.choices(["YES", "NO"], weights=[0.50, 0.50])[0]
            pwd_reuse = random.choices(["YES", "NO"], weights=[0.45, 0.55])[0]
            link_aware = random.choices(["MEDIUM", "HIGH", "LOW"], weights=[0.55, 0.30, 0.15])[0]
            old_posts = random.choices(["NO", "YES"], weights=[0.60, 0.40])[0]
            priv_rev = random.choices(["NO", "YES"], weights=[0.55, 0.45])[0]

        elif persona_choice == "Oversharer":
            # Higher exposure
            profile_vis = random.choices(["PUBLIC", "FRIENDS_ONLY"], weights=[0.80, 0.20])[0]
            phone_pub = "YES" if random.random() > 0.45 else "NO"
            email_pub = "YES" if random.random() > 0.25 else "NO"
            bday_pub = "YES" if random.random() > 0.15 else "NO"
            loc_pub = "YES" if random.random() > 0.25 else "NO"
            work_pub = "YES" if random.random() > 0.15 else "NO"
            edu_pub = "YES" if random.random() > 0.15 else "NO"
            rel_pub = "YES" if random.random() > 0.20 else "NO"
            posts_pub = "PUBLIC" if random.random() > 0.2 else "FRIENDS"
            loc_tag = "YES" if random.random() > 0.3 else "SOMETIMES"
            travel = "YES" if random.random() > 0.25 else "SOMETIMES"
            unknown_conn = "YES" if random.random() > 0.30 else "SOMETIMES"
            tag_rev = "NO" if random.random() > 0.25 else "YES"
            app_rev = "NO" if random.random() > 0.15 else "NOT_SURE"
            mfa = "NO" if random.random() > 0.35 else "YES"
            login_alerts = "NO" if random.random() > 0.30 else "YES"
            pwd_reuse = "YES" if random.random() > 0.25 else "NO"
            link_aware = "LOW" if random.random() > 0.40 else "MEDIUM"
            old_posts = "NO" if random.random() > 0.15 else "YES"
            priv_rev = "NO" if random.random() > 0.20 else "YES"

        else: # HighRisk
            # Extreme exposure profile
            profile_vis = "PUBLIC"
            phone_pub = "YES"
            email_pub = "YES"
            bday_pub = "YES"
            loc_pub = "YES"
            work_pub = "YES"
            edu_pub = "YES"
            rel_pub = "YES"
            posts_pub = "PUBLIC"
            loc_tag = "YES"
            travel = "YES"
            unknown_conn = "YES"
            tag_rev = "NO"
            app_rev = "NO"
            mfa = "NO"
            login_alerts = "NO"
            pwd_reuse = "YES"
            link_aware = "LOW"
            old_posts = "NO"
            priv_rev = "NO"

        row = {
            "profile_id": pid,
            "profile_visibility": profile_vis,
            "phone_public": phone_pub,
            "email_public": email_pub,
            "birthday_public": bday_pub,
            "location_public": loc_pub,
            "workplace_public": work_pub,
            "education_public": edu_pub,
            "relationship_public": rel_pub,
            "posts_public": posts_pub,
            "location_tagging": loc_tag,
            "travel_posts": travel,
            "unknown_connections": unknown_conn,
            "tag_review_enabled": tag_rev,
            "third_party_apps_reviewed": app_rev,
            "mfa_enabled": mfa,
            "login_alerts_enabled": login_alerts,
            "password_reuse_reported": pwd_reuse,
            "suspicious_link_awareness": link_aware,
            "old_posts_reviewed": old_posts,
            "privacy_settings_reviewed": priv_rev
        }

        score, level = calculate_synthetic_score(row)
        row["risk_score"] = score
        row["risk_level"] = level
        records.append(row)

    # Write to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = list(records[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Print summary statistics
    low_count = sum(1 for r in records if r["risk_level"] == "LOW")
    mod_count = sum(1 for r in records if r["risk_level"] == "MODERATE")
    high_count = sum(1 for r in records if r["risk_level"] == "HIGH")
    crit_count = sum(1 for r in records if r["risk_level"] == "CRITICAL")
    avg_score = sum(r["risk_score"] for r in records) / len(records)

    print(f"Generated {len(records)} synthetic privacy assessment records at: {output_path}")
    print(f"Summary: Average Score = {avg_score:.1f}")
    print(f"  - LOW (0-20):       {low_count} ({low_count/len(records)*100:.1f}%)")
    print(f"  - MODERATE (21-40): {mod_count} ({mod_count/len(records)*100:.1f}%)")
    print(f"  - HIGH (41-70):     {high_count} ({high_count/len(records)*100:.1f}%)")
    print(f"  - CRITICAL (71-100):{crit_count} ({crit_count/len(records)*100:.1f}%)")

    return output_path

if __name__ == "__main__":
    generate_synthetic_dataset()
