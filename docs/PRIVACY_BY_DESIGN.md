# Privacy by Design Architecture & Implementation

## 1. Executive Summary
The **Social Media Privacy Risk Assessment Framework** was designed from inception to embody the foundational principles of **Privacy by Design (PbD)** established by Dr. Ann Cavoukian and codified under GDPR (Article 25) and CCPA. Unlike conventional risk assessment tools that harvest sensitive information to analyze exposure, our framework calculates risk metrics while strictly avoiding the collection or storage of personal identifying information (PII).

---

## 2. Implementation of Core Privacy by Design Principles

### 1. Data Minimization (GDPR Art. 5(1)(c))
* **Principle:** Collect and process only the minimum data strictly necessary to fulfill the intended purpose.
* **Framework Implementation:**
  - The assessment **never asks users to enter their actual phone numbers, email addresses, passwords, home addresses, or dates of birth**.
  - Instead, the system asks binary and configuration questions: *"Is your phone number visible on your profile? (YES/NO)"*.
  - This allows accurate exposure modeling without generating an attractive database target for adversaries.

### 2. Purpose Limitation (GDPR Art. 5(1)(b))
* **Principle:** Data must be collected for specified, explicit, and legitimate purposes and not further processed in a manner incompatible with those purposes.
* **Framework Implementation:**
  - Questionnaire answers are processed solely to compute the immediate privacy risk score and generate remediation guidance.
  - The platform does not cross-reference data across external advertising networks, data brokers, or profiling algorithms.

### 3. Principle of Least Privilege (PoLP)
* **Principle:** Software components and users must operate using only the minimal permissions required.
* **Framework Implementation:**
  - The web application operates without root/admin database privileges.
  - The EXIF metadata extraction service operates entirely in memory; it possesses no persistent disk write capabilities for uploaded images.

### 4. Privacy by Default (GDPR Art. 25(2))
* **Principle:** The strictest privacy settings must apply automatically without requiring proactive user intervention.
* **Framework Implementation:**
  - In our benchmark evaluations and recommendations, the framework advocates for "Private Account", "Tag Review: Enabled", and "Search Indexing: Disabled" as the baseline posture for users.
  - The assessment storage defaults to anonymized IDs (`PRA-XXXX`) rather than user-identifiable handles.

### 5. Transparency & Openness (GDPR Art. 12)
* **Principle:** Operations and algorithms must remain explainable, predictable, and open to scrutiny.
* **Framework Implementation:**
  - Every calculation, category weight, and risk threshold is open-source and explainable.
  - The assessment report explicitly discloses the formula, category contributions, and specific findings that contributed to the final score.
  - Ethical and educational disclaimers are prominently displayed across every interface.

### 6. User Control & Right to Erasure (GDPR Art. 17 / CCPA)
* **Principle:** Users must retain full sovereignty over their data, including the right to delete records permanently.
* **Framework Implementation:**
  - The framework provides an automated **Right to Erasure** endpoint (`DELETE /api/assessment/{id}`) and a visible *"Delete Record"* button on the report page.
  - Triggering deletion executes an immediate cascade delete across the `assessments`, `category_scores`, `findings`, and `recommendations` tables.

### 7. Retention Limitation (GDPR Art. 5(1)(e))
* **Principle:** Personal data must be kept in a form that permits identification for no longer than is necessary.
* **Framework Implementation:**
  - Assessment records persist only derived metadata (scores, timestamps, finding categories).
  - The safe photo EXIF viewer holds image bytes in memory buffer only during active request processing; bytes are automatically discarded by garbage collection immediately upon response transmission.

### 8. Secure Processing & Defensive Architecture (GDPR Art. 32)
* **Principle:** Implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk.
* **Framework Implementation:**
  - Input validation strictly enforces allowed enum values and question mappings, preventing SQL injection and payload tampering.
  - Database interactions utilize parameterized queries via Python's standard `sqlite3` driver.
  - Rate limiting parameters and upload size ceilings (20MB) prevent denial-of-service abuse.

---

## 3. Database Schema Verification: Zero Raw PII Storage

```sql
-- Schema strictly excludes PII fields:
CREATE TABLE assessments (
    assessment_id TEXT PRIMARY KEY,
    overall_score INTEGER NOT NULL,
    risk_level TEXT NOT NULL,
    platform TEXT NOT NULL,
    source_type TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

Automated verification test `test_29_data_minimization_sensitive_data_not_stored` programmatically inspects the SQLite table definitions to guarantee that columns matching `phone`, `email`, `password`, `dob`, `address`, or `gps` are non-existent.
