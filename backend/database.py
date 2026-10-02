"""
Social Media Privacy Risk Assessment Framework
Database Layer (Privacy-Preserving SQLite Storage)
===================================================
Adheres to Privacy by Design & Data Minimization:
- Stores ONLY calculated scores, risk levels, findings, and remediation guidance.
- NEVER stores phone numbers, email addresses, birthdays, coordinates, or passwords.
- Supports complete right-to-erasure (data deletion).
"""

import os
import sqlite3
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

DB_FILE = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "privacy_risk.db"))

def get_db_connection() -> sqlite3.Connection:
    """Creates a connection with row factory for dictionary-like access."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes normalized database schema with privacy-by-design constraints."""
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id TEXT PRIMARY KEY,
                overall_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                platform TEXT NOT NULL,
                source_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS category_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id TEXT NOT NULL,
                category_code TEXT NOT NULL,
                category_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                weight REAL NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id TEXT NOT NULL,
                category_code TEXT NOT NULL,
                finding_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id TEXT NOT NULL,
                category_code TEXT NOT NULL,
                priority TEXT NOT NULL,
                title TEXT NOT NULL,
                action_steps TEXT NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
            );
        """)
    conn.close()

def save_assessment_record(
    assessment_id: str,
    overall_score: int,
    risk_level: str,
    platform: str,
    source_type: str,
    category_scores: List[Dict[str, Any]],
    findings: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]]
) -> str:
    """
    Saves an assessment in the database.
    Guarantees no raw personal identifying information is stored.
    """
    conn = get_db_connection()
    now_iso = datetime.now(timezone.utc).isoformat()

    with conn:
        conn.execute(
            """INSERT INTO assessments 
               (assessment_id, overall_score, risk_level, platform, source_type, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (assessment_id, overall_score, risk_level, platform, source_type, now_iso)
        )

        for cat in category_scores:
            conn.execute(
                """INSERT INTO category_scores 
                   (assessment_id, category_code, category_name, score, weight)
                   VALUES (?, ?, ?, ?, ?)""",
                (assessment_id, cat["category_code"], cat["category_name"], cat["score"], cat["weight"])
            )

        for f in findings:
            conn.execute(
                """INSERT INTO findings 
                   (assessment_id, category_code, finding_type, severity, title, description)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (assessment_id, f["category_code"], f.get("finding_type", "EXPOSURE"), f["severity"], f["title"], f["description"])
            )

        for r in recommendations:
            conn.execute(
                """INSERT INTO recommendations 
                   (assessment_id, category_code, priority, title, action_steps)
                   VALUES (?, ?, ?, ?, ?)""",
                (assessment_id, r["category_code"], r["priority"], r["title"], r["action_steps"])
            )

    conn.close()
    return assessment_id

def get_assessment_by_id(assessment_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves full assessment record with categories, findings, and recommendations."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM assessments WHERE assessment_id = ?", (assessment_id,))
    assessment_row = cur.fetchone()
    if not assessment_row:
        conn.close()
        return None

    cur.execute("SELECT * FROM category_scores WHERE assessment_id = ?", (assessment_id,))
    cat_rows = cur.fetchall()

    cur.execute("SELECT * FROM findings WHERE assessment_id = ? ORDER BY id ASC", (assessment_id,))
    find_rows = cur.fetchall()

    cur.execute("SELECT * FROM recommendations WHERE assessment_id = ? ORDER BY id ASC", (assessment_id,))
    rec_rows = cur.fetchall()

    conn.close()

    return {
        "assessment_id": assessment_row["assessment_id"],
        "overall_score": assessment_row["overall_score"],
        "risk_level": assessment_row["risk_level"],
        "platform": assessment_row["platform"],
        "source_type": assessment_row["source_type"],
        "created_at": assessment_row["created_at"],
        "category_scores": [dict(r) for r in cat_rows],
        "findings": [dict(r) for r in find_rows],
        "recommendations": [dict(r) for r in rec_rows]
    }

def delete_assessment_by_id(assessment_id: str) -> bool:
    """Enforces Right-to-Erasure (GDPR Art. 17 / CCPA) by deleting all associated records."""
    conn = get_db_connection()
    with conn:
        cur = conn.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
        rows_deleted = cur.rowcount
    conn.close()
    return rows_deleted > 0

def get_all_recent_assessments(limit: int = 15) -> List[Dict[str, Any]]:
    """Retrieves recent assessment records without sensitive data."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT assessment_id, overall_score, risk_level, platform, source_type, created_at "
        "FROM assessments ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Initialize DB upon module load
init_db()
