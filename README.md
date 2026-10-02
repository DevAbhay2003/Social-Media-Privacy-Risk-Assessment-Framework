# Social Media Privacy Risk Assessment Framework

[![Defensive Cybersecurity](https://img.shields.io/badge/Focus-Defensive%20Cybersecurity-blue.svg)](#cybersecurity-relevance)
[![Privacy by Design](https://img.shields.io/badge/Compliance-Privacy%20by%20Design-10B981.svg)](#privacy-by-design)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](#technology-stack)
[![Pytest Suite](https://img.shields.io/badge/Tests-34%20Passed%20%28100%25%29-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Ethical & Defensive Notice:**  
> This project is engineered exclusively for **defensive cybersecurity and privacy education**. It uses synthetic datasets or voluntarily supplied assessment responses and **does not scrape, track, or profile real social-media users**, nor does it harvest real personally identifiable information (PII).

---

## Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Cybersecurity Relevance](#cybersecurity-relevance)
- [Privacy vs. Security](#privacy-vs-security)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Privacy Questionnaire](#privacy-questionnaire)
- [Risk Categories](#risk-categories)
- [Risk Scoring](#risk-scoring)
- [Privacy Findings](#privacy-findings)
- [Recommendation Engine](#recommendation-engine)
- [Improvement Simulator](#improvement-simulator)
- [Digital Footprint](#digital-footprint)
- [Social Engineering Awareness](#social-engineering-awareness)
- [Account Security](#account-security)
- [Privacy Dashboard](#privacy-dashboard)
- [Privacy Report](#privacy-report)
- [Privacy by Design](#privacy-by-design)
- [Installation & Local Execution](#installation--local-execution)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Security & Privacy Testing](#security--privacy-testing)
- [Results](#results)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Screenshots & Proof Guide](#screenshots)
- [Learning Outcomes](#learning-outcomes)
- [Ethical Disclaimer](#ethical-disclaimer)
- [Author](#author)

---

## Overview
The **Social Media Privacy Risk Assessment Framework** is an industry-oriented defensive cybersecurity platform that evaluates an individual's or organization's social media exposure, account security posture, and digital footprint without scraping or storing private data. 

Through an interactive **44-question assessment across 10 defense-in-depth domains**, the framework calculates normalized category risk scores (0–100) and an overall weighted privacy risk score, mapping findings to actionable remediation roadmaps, an interactive **Privacy Improvement Simulator**, a safe in-memory **Photo EXIF Metadata Inspector**, and an aggregate **Cybersecurity Dashboard**.

---

## Problem Statement
While hiring teams, educational institutions, and adversaries evaluate online footprints with increasing sophistication, users frequently overshare sensitive identifiers:
1. **Unintentional OSINT Exposure:** Users post work badges, full birth dates, phone numbers, and travel schedules that enable spear-phishing, identity fraud, and physical stalking.
2. **False Sense of Security:** Many users believe that having a strong password means their privacy is protected, neglecting public profile visibility and data brokerage trails.
3. **Invasive Commercial Scanners:** Most commercial footprint auditing tools require users to submit sensitive real credentials or scrape private accounts, compounding the user's risk.
4. **Lack of Actionable Quantification:** Standard advice offers vague bullet points without quantifying exposure or showing how specific settings changes reduce risk.

---

## Objectives
* **Assess Without Invasiveness:** Formulate a structured, 44-question questionnaire evaluating configurations and behaviors rather than harvesting PII.
* **Quantify Exposure Mathematically:** Construct a 0–100 weighted risk engine (Low, Moderate, High, Critical) with explainable category contributions.
* **Prioritize Remediation:** Automatically generate prioritized security fixes (Immediate, Important, Good Practice).
* **Enable What-If Simulation:** Build an interactive simulator demonstrating live risk reduction when hardening specific settings.
* **Demonstrate In-Memory Media Auditing:** Provide a local EXIF inspector that flags GPS coordinates and strips metadata in RAM.
* **Comply with Privacy by Design:** Enforce zero raw PII storage in SQLite and support automated GDPR Right to Erasure.

---

## Cybersecurity Relevance
This project directly reflects workflows in:
* **SOC / Threat Intelligence:** Identifying open-source intelligence (OSINT) vectors used for initial reconnaissance.
* **Application Security & Privacy Engineering:** Designing software under Data Minimization, Purpose Limitation, and GDPR Article 25.
* **Governance, Risk & Compliance (GRC):** Formulating risk scoring rubrics, threat models, and policy compliance checklists.
* **Security Awareness Training:** Developing human-centric coaching tools that quantify risk and incentivize behavioral change.

Relevant career tracks: **Cybersecurity Analyst**, **Privacy Analyst**, **GRC Analyst**, **SOC Analyst**, **Security Consultant**, and **Security Awareness Specialist**.

---

## Privacy vs. Security

| Dimension | Privacy | Security |
| :--- | :--- | :--- |
| **Definition** | Controls how personal information is collected, exposed, shared, and utilized. | Protects systems, credentials, and assets against unauthorized access or misuse. |
| **Primary Goal** | Data minimization, confidentiality of identity, consent, and audience control. | Integrity, availability, and protection against unauthorized compromise. |
| **Common Tools** | Setting accounts to Private, disabling search indexing, hiding birth year, avoiding check-ins. | Strong passwords, MFA / FIDO2 tokens, login alerts, disk encryption. |
| **Failure Mode** | Doxxing, spear-phishing, physical stalking, unwanted profiling. | Credential theft, account takeover, session hijacking, malware injection. |

> [!IMPORTANT]
> **Strong Account Security ≠ Strong Privacy.**  
> A user can have a 30-character random password and a hardware security key (Strong Security), yet publicly post their personal cell number, birth year, and daily 7 AM running route (Weak Privacy).

---

## Features
- 📋 **44-Question Assessment Engine:** Evaluates 10 defense-in-depth categories with standardized options.
- ⚖️ **Normalized Risk Engine (0–100):** Weighted mathematical calculation with standard risk tiers.
- ⚡ **Privacy Improvement Simulator:** Interactive toggles showing real-time score reduction (e.g., 72 Critical ➔ 34 Moderate).
- 📸 **Safe In-Memory EXIF Inspector:** Reads JPEG/TIFF metadata in RAM, flags GPS tags, and provides one-click clean image download.
- 📊 **Analytics Dashboard:** Population distributions, radar profiles, and top systemic weaknesses benchmarked across 1,200 synthetic records.
- 📄 **Printable Privacy Audit Report:** Executive summary with PDF print export and GDPR cascade deletion.
- ☑️ **Defensive Action Checklist:** Interactive, printable 18-point privacy hardening checklist.
- 📁 **JSON File Ingestion Mode:** Dual support for `profile.json` and `posts.json` synthetic payloads.

---

## Architecture

```
User (Self-Reported / Demo Data)
               │
               ▼
   44-Question Stepper UI
               │
               ▼
   Input Validation & Sanitization (Zero Raw PII)
               │
               ▼
   Privacy Feature Extraction (extract_privacy_features)
               │
               ▼
┌────────────────────────────────────────────────────────┐
│               Category Risk Analyzers                  │
│ Profile • Personal Info • Location • Content • Network │
│ Tagging • Account Sec • OAuth Apps • Social Eng • Footprint │
└──────────────────────────────┬─────────────────────────┘
                               │ Normalized Scores (0-100)
                               ▼
               Overall Risk Scoring Engine
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
        Findings Engine              Recommendation Engine
       (Severity Ranked)              (Priority Ordered)
               │                               │
               └───────────────┬───────────────┘
                               ▼
             Executive Privacy Assessment Report
             + Interactive Improvement Simulator
                               │
                               ▼
        Privacy-Preserving SQLite Storage (No Raw PII)
```

---

## Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend API** | Python 3.10+ / Flask | Modular blueprints, lightweight execution, industry standard. |
| **Database** | SQLite3 | Local, privacy-preserving, zero external cloud dependency. |
| **Data Analysis** | Pandas & NumPy | Synthetic dataset modeling and population distribution analytics. |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | High-performance, zero build-step overhead, responsive cyber theme. |
| **Visualizations** | Chart.js 4.x | Radar, doughnut, and bar charts for risk distribution. |
| **Testing** | Pytest | 34 automated unit and integration tests. |

---

## Privacy Questionnaire
The framework includes 44 structured questions divided into 10 defense-in-depth categories:
- **CAT_A: Profile Visibility** (4 questions: visibility setting, search indexing, contact lookup, avatar context).
- **CAT_B: Personal Information** (5 questions: phone visibility, personal email, birth date, workplace, family info).
- **CAT_C: Location Privacy** (5 questions: real-time check-ins, geotagging, travel plans in advance, home exterior photos, routine schedules).
- **CAT_D: Posts & Content** (4 questions: default audience, badges/access cards, minors in photos, barcodes/tickets).
- **CAT_E: Friends & Followers** (4 questions: unknown connections, friends list visibility, follower approval, annual connection audits).
- **CAT_F: Tagging & Mentions** (4 questions: tag review enabled, stranger mentions, facial recognition auto-tags, tag removal familiarity).
- **CAT_G: Account Security & MFA** (5 questions: MFA status, MFA method [TOTP vs SMS], password reuse, login alerts, active sessions).
- **CAT_H: Third-Party Apps** (4 questions: connected OAuth apps, review frequency, permission inspection, viral quizzes).
- **CAT_I: Messaging & Social Engineering** (5 questions: open DMs, clicking DM links, OTP forwarding, fraudulent giveaways, emergency financial lures).
- **CAT_J: Digital Footprint** (4 questions: historical post auditing, abandoned accounts, defensive self-OSINT, biannual privacy checkups).

---

## Risk Categories & Weights

| Code | Domain | Weight | Focus |
| :---: | :--- | :---: | :--- |
| `CAT_A` | Profile Visibility | 10% | Discoverability, external search indexing, public avatars. |
| `CAT_B` | Personal Information | 15% | Phone numbers, personal emails, birth dates, family details. |
| `CAT_C` | Location Privacy | 15% | Live GPS check-ins, routine disclosures, vacation advance notices. |
| `CAT_D` | Posts & Content | 10% | Default audience, work badges, minors, tickets/barcodes. |
| `CAT_E` | Friends & Followers | 10% | Unknown requests, public friend lists, follower approval. |
| `CAT_F` | Tagging & Mentions | 5% | Tag review approval, mention controls, facial recognition. |
| `CAT_G` | Account Security & MFA | 15% | Multi-Factor Authentication, password reuse, login alerts. |
| `CAT_H` | Third-Party Apps | 5% | OAuth integrations, excessive scopes, regular app audits. |
| `CAT_I` | Social Engineering | 10% | Open DMs, suspicious link awareness, OTP forwarding scams. |
| `CAT_J` | Digital Footprint | 5% | Historical post auditing, abandoned accounts, self-OSINT searches. |

---

## Risk Scoring

* **Category Scores:** Each category calculates a normalized score from 0 (minimal exposure) to 100 (maximum risk).
* **Overall Score:** Weighted sum of all category scores:
  $$\text{Score} = \sum (\text{Category Score} \times \text{Weight})$$
* **Standard Risk Tiers:**
  - `0 – 20`: **LOW RISK** (Hardened perimeter, disciplined privacy hygiene)
  - `21 – 40`: **MODERATE RISK** (Standard exposure, minor configuration gaps)
  - `41 – 70`: **HIGH RISK** (Substantial exposure, potential vector for profiling/phishing)
  - `71 – 100`: **CRITICAL RISK** (Severe exposure, live GPS broadcasts, disabled MFA)

---

## Privacy Findings
The Findings Engine evaluates responses against threat heuristics and maps vulnerabilities to standardized severity ratings:
* **CRITICAL:** Direct immediate risk (Public phone in bio, live GPS sharing, disabled MFA, OTP forwarding susceptibility).
* **HIGH:** Major exposure vector (Public personal email, full birth date, unknown connections accepted, open DMs).
* **MEDIUM:** Moderate exposure (External search indexing enabled, predictable routine disclosures, stale OAuth apps).
* **LOW:** General hygiene gap (Unpruned friends list, missing self-OSINT search).

---

## Recommendation Engine
Remediations are automatically prioritized into an actionable roadmap:
1. **IMMEDIATE:** Actions required to halt active physical threats or credential compromise vectors.
2. **IMPORTANT:** Major attack surface reductions (hiding birth year, enabling tag review, upgrading to app-based MFA).
3. **GOOD PRACTICE:** Routine maintenance and defense-in-depth habits (biannual app audits, session reviews).

---

## Improvement Simulator
The **Privacy Improvement Simulator** answers the common user question: *"What happens if I improve my settings?"*  
Users toggle 14 defensive controls:
- **Baseline Profile:** Score **72 / 100 (CRITICAL RISK)**
- **Simulated Changes:** Hide phone + Disable live location + Enable MFA + Enable tag review
- **New Simulated Score:** **34 / 100 (MODERATE RISK)**
- **Net Attack Surface Reduction:** **38 Points (52.8% Risk Reduction)**

---

## Digital Footprint
The framework evaluates self-reported active and passive digital footprint practices:
* Historical timeline auditing and post purging (>12 months).
* Identification and deletion of abandoned/zombie platform accounts.
* Regular execution of defensive self-OSINT searches.
* Biannual execution of built-in platform privacy checkups.

---

## Social Engineering Awareness
Explains how threat actors aggregate public context (employer, college, vacation schedules, family references) to craft believable, high-trust phishing lures and pretexting attacks. The framework focuses strictly on defensive countermeasures and out-of-band verification.

---

## Account Security
Assesses the technical controls safeguarding private content:
* Multi-Factor Authentication (differentiating between vulnerable SMS and strong TOTP authenticator apps / FIDO2 keys).
* Unique password hygiene (preventing credential stuffing from third-party breach datasets).
* Real-time unrecognized login alerts and active session auditing.

---

## Privacy Dashboard
The Analytics Dashboard features:
* **Top Metric Cards:** Total records analyzed, population average risk, highest exposure domain, and MFA adoption rate.
* **10-Category Radar Chart:** Visual profile of domain risks.
* **Population Risk Doughnut Chart:** Breakdown of Low, Moderate, High, and Critical distribution.
* **Top Systemic Weaknesses Chart:** Horizontal bar chart showing weakness prevalence.
* **Security Controls Adoption Chart:** Adoption rates of MFA, login alerts, tag review, and checkups.
* **Recent Assessments Table:** Anonymized audit log with one-click report view.

---

## Privacy Report
Generates an executive privacy report featuring:
* Unique Assessment ID (`PRA-XXXX`) and Evaluation Timestamp.
* Visual Risk Gauge and Risk Tier Badge.
* Domain scores breakdown table and bar chart.
* Severity-ranked findings and priority-ordered remediation roadmap.
* Printable Privacy Checklist.
* One-click **Export to PDF / Print** functionality with print stylesheet formatting.
* GDPR Article 17 **Delete Record** button for instant cascade deletion.

---

## Privacy by Design
The project strictly implements all 7 foundational principles of Privacy by Design:
1. **Data Minimization:** No actual phone numbers, emails, passwords, or coordinates are collected.
2. **Purpose Limitation:** Data is processed exclusively for risk evaluation and immediate reporting.
3. **Least Privilege:** Components operate with minimal database and filesystem permissions.
4. **Privacy by Default:** Assessments recommend hardened privacy baselines.
5. **Transparency:** All formulas, weights, and finding triggers are open-source.
6. **User Control:** Right to Erasure cascade deletion available via UI or REST API.
7. **Secure Processing:** Input validation, parameterized queries, and in-memory image handling.

---

## Installation & Local Execution

### Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13 installed.
* Modern web browser (Chrome, Edge, Firefox, Safari).

### Step-by-Step Setup

```bash
# 1. Clone repository or navigate to project directory
cd "C:\Users\user\Desktop\IIP Projects\CS\p2"

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the 1,200 synthetic assessment dataset
python data/generate_dataset.py

# 5. Run the automated test suite to verify system integrity
pytest tests/test_privacy_framework.py -v

# 6. Start the local server
python backend/app.py
```

### Accessing the Interfaces
Once started, open your web browser to:
* **Homepage & Overview:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* **Privacy Questionnaire:** [http://127.0.0.1:5000/assessment](http://127.0.0.1:5000/assessment)
* **Analytics Dashboard:** [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)
* **Improvement Simulator:** [http://127.0.0.1:5000/simulator](http://127.0.0.1:5000/simulator)
* **Photo EXIF Inspector:** [http://127.0.0.1:5000/metadata](http://127.0.0.1:5000/metadata)
* **Privacy Checklist:** [http://127.0.0.1:5000/checklist](http://127.0.0.1:5000/checklist)

---

## Usage Guide
1. **Interactive Assessment:** Navigate to `/assessment`. Use the category tabs to complete the 44 questions, or click **"Load High Exposure Demo"** or **"Load Defensive Demo"** for instant 1-click evaluation.
2. **Reviewing Results:** Submit the assessment to generate the formal audit report at `/report?id=...`. Click **"Print / Save as PDF"** to export.
3. **Simulating Setting Changes:** Navigate to `/simulator` to toggle defensive configurations and observe real-time risk score reduction.
4. **Inspecting Photo EXIF:** Navigate to `/metadata` and upload an image or click **"Generate Demo Image with Embedded GPS"** to view camera tags and download an EXIF-stripped clean copy.

---

## API Documentation

| Method | Endpoint | Description | Request Payload | Response |
| :---: | :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Service health check & compliance declaration. | None | JSON status object |
| `GET` | `/api/questions` | Master catalog of 44 questions and categories. | None | Questions list |
| `POST` | `/api/assessment` | Submit answers and generate assessment record. | `{"answers": {...}, "platform": "..."}` | Assessment results |
| `GET` | `/api/assessment/{id}` | Retrieve existing assessment results by ID. | None | Full assessment JSON |
| `DELETE` | `/api/assessment/{id}` | GDPR Right to Erasure cascade deletion. | None | Confirmation message |
| `POST` | `/api/assessment/simulate-improvement` | Calculate simulated score reduction delta. | `{"answers": {...}, "selected_actions": [...]}` | Comparison delta JSON |
| `GET` | `/api/dashboard/stats` | Aggregate population analytics and benchmarks. | None | Population metrics |
| `POST` | `/api/analyze-json` | Ingest `profile.json` & `posts.json` files. | JSON payload or multipart | Assessment results |
| `POST` | `/api/metadata/extract` | In-memory EXIF metadata extraction. | Multipart `image` file | Parsed tags & hazards |
| `POST` | `/api/metadata/strip` | In-memory EXIF metadata scrubbing. | Multipart `image` file | Cleaned image download |
| `GET` | `/api/privacy-checklist` | Downloadable / printable checklist items. | None | Checklist items |

---

## Testing
The framework includes **34 automated tests** in `tests/test_privacy_framework.py`:
```bash
pytest tests/test_privacy_framework.py -v
```
All 34 tests execute and pass in under 1 second:
- Extreme profiles (fully private vs fully public).
- Specific risk triggers (public phone, missing MFA, live check-ins, travel posts, badge photos).
- Boundary score cutoffs (20, 40, 70).
- In-memory EXIF parsing and header stripping.
- SQLite data minimization schema inspection.
- REST API lifecycle (submission, retrieval, erasure).

---

## Security & Privacy Testing
- **Zero Raw PII Storage:** Programmatically confirmed via `test_29_data_minimization_sensitive_data_not_stored`.
- **Input Sanitization:** Enum-based validation rejecting unauthorized keys or malformed values.
- **In-Memory Buffer Safety:** EXIF parser strictly enforces byte offsets and skips external storage.
- **Cascade Deletion:** Verified complete erasure across all foreign-key tables upon deletion.

---

## Results
* **Deterministic Risk Scoring:** Clear differentiation between hardened profiles (scores < 15, Low Risk) and exposed profiles (scores > 75, Critical Risk).
* **Demonstrated Risk Reduction:** The Improvement Simulator consistently demonstrates a 40–55% drop in assessed risk when applying top defensive controls.
* **Population Benchmark:** The synthetic dataset of 1,200 records establishes a realistic population average risk of 48.9 (High Risk), highlighting systemic consumer vulnerabilities in MFA adoption (41% disabled) and tag review (44% disabled).

---

## Limitations
* **Self-Reported Behavioral Input:** The tool relies on user honesty in answering configuration questions. It deliberately avoids scraping live accounts to maintain an ethical posture.
* **Educational Calibration:** Weights and thresholds represent defense-in-depth rubric assumptions; they do not guarantee total immunity from cyber threats.

---

## Future Improvements
* Platform-specific guided interactive click-throughs for Instagram, LinkedIn, and X.
* Enterprise organizational policy templates for corporate employee awareness training.
* Client-side WebAssembly (Wasm) mode for 100% offline, air-gapped assessments.
* Longitudinal privacy score comparison over time.

---

## Screenshots
Refer to [`screenshots/README.md`](screenshots/README.md) for the 30-item screenshot checklist and standardized file naming guide.

---

## Learning Outcomes
By engineering this project, the author demonstrated mastery of:
- Defensive Threat Modeling and OSINT Attack Surface Reduction.
- Applying Privacy by Design (PbD) and Data Minimization under GDPR/CCPA.
- Full-stack Python/Flask REST API and responsive frontend engineering.
- Explainable mathematical risk modeling and what-if simulation engines.
- Test-Driven Development (TDD) using `pytest`.

---

## Ethical Disclaimer
This software is developed strictly for educational and defensive cybersecurity purposes. It does not perform account enumeration, does not bypass platform authentication, does not scrape private content, and does not profile real individuals.

---

## Author
- Developed as a **Cybersecurity Capstone Course Project** by a dedicated cybersecurity student and aspiring privacy engineer.  
- **Abhishek Basu — Embedded Systems Student GitHub: [DevAbhay2003](https://github.com/DevAbhay2003?tab=repositories) · LinkedIn: [Abhishek Basu](https://www.linkedin.com/in/abhishek-basu-68b1b1342/)**
*Feedback, contributions, and defensive security discussions are warmly welcomed.*
