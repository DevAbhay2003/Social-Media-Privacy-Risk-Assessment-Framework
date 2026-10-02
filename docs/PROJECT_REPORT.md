# Comprehensive Academic & Industry Technical Report

**Project Title:** Social Media Privacy Risk Assessment Framework  
**Course:** Advanced Cybersecurity & Privacy Engineering  
**Focus:** Defensive Security, Privacy by Design, OSINT Attack Surface Reduction, Risk Scoring  

---

## 1. Abstract
The proliferation of social media platforms has transformed online communication into a continuous broadcast of personal behavioral context. Individuals and organizational employees routinely expose sensitive information—such as direct contact numbers, precise residential locations, travel itineraries, access badges, and familial relationships—without recognizing the aggregated risk surface they create. Malicious threat actors exploit this Open Source Intelligence (OSINT) to orchestrate spear-phishing, business email compromise (BEC), credential stuffing, and social-engineering attacks. 

This project presents the **Social Media Privacy Risk Assessment Framework**, a full-stack, defensive cybersecurity platform designed to evaluate privacy configurations and digital footprint hygiene without scraping, profiling, or harvesting real user data. Utilizing a structured 44-question assessment across 10 defense-in-depth domains, the framework computes normalized category risk metrics (0–100) and an overall weighted privacy risk score. Key engineering contributions include an interactive **Privacy Improvement Simulator** that visualizes projected risk reduction, an in-memory **Photo EXIF Metadata Inspector and Scrubber**, an aggregate population analytics dashboard benchmarked across 1,200 synthetic records, and full adherence to **Privacy by Design (PbD)** principles under GDPR and CCPA. The implementation is thoroughly verified by an automated 34-test suite in `pytest` achieving 100% test pass fidelity.

---

## 2. Introduction & Background
Modern society relies on social networks for professional networking, personal relationships, and public expression. However, the commercial architecture of social media incentivizes broad visibility and engagement over data minimization. Consequently, users frequently mistake account authentication controls (such as having a password) for personal data privacy. 

This framework was developed as a cybersecurity course capstone project to bridge the gap between technical risk analysis and human privacy behavior. It provides individuals, students, job-seekers, and enterprise employees with a defensible, non-invasive mechanism to assess and remediate their online footprint.

---

## 3. Problem Statement
Traditional privacy and security tools suffer from significant shortcomings:
1. **Invasive Data Harvesting:** Many commercial footprint scanners require users to supply real email addresses, phone numbers, or social passwords, creating substantial new privacy risks.
2. **Conflation of Security and Privacy:** Users assume that having a strong password means their privacy is safe, disregarding the risks of publicly visible phone numbers or live location broadcasts.
3. **Static, Unactionable Advice:** Standard awareness checklists provide generic bullet points without quantifying exposure or showing the mathematical impact of hardening settings.
4. **Lack of Explainability:** Proprietary risk scores function as black boxes, failing to educate users on how specific configurations contribute to their exposure.

---

## 4. Project Objectives
* **Objective 1:** Build a modular, defense-in-depth questionnaire (44 questions across 10 categories) that assesses exposure without asking users to reveal their actual PII.
* **Objective 2:** Design a normalized risk-scoring engine (0–100 scale; Low, Moderate, High, Critical) with configurable domain weightings.
* **Objective 3:** Implement an automated Findings Engine and Recommendation Engine that generates prioritized, actionable remediation steps.
* **Objective 4:** Develop an interactive Privacy Improvement Simulator demonstrating real-time what-if mitigation modeling.
* **Objective 5:** Provide a safe, in-memory image EXIF metadata inspector that detects GPS leaks and strips metadata from photos without storing files on disk.
* **Objective 6:** Build a population analytics dashboard benchmarked against 1,200 synthetic assessment records.
* **Objective 7:** Enforce strict Privacy by Design compliance with verifiable zero-PII database storage and automated GDPR Right to Erasure support.

---

## 5. Conceptual Foundations

### 5.1 Privacy vs. Security
* **Privacy:** Dictates how personal information is collected, exposed, shared, and utilized. It concerns data minimization, consent, and audience restriction.
* **Security:** Protects systems, networks, and data from unauthorized access, modification, or destruction (confidentiality, integrity, availability).
* **The Intersecting Reality:** A user may possess military-grade authentication security (a 32-character random passphrase and a YubiKey hardware token) while simultaneously maintaining zero privacy by publicly posting their home address, child's school uniform, and daily workout route. **Strong Account Security ≠ Strong Privacy.**

### 5.2 Digital Footprint Dynamics
* **Active Digital Footprint:** Deliberate data releases—posts, photo uploads, profile bios, comments on public forums, and tagged relationships.
* **Passive Digital Footprint:** Involuntary or background data trails—search engine cache archives, web scraping by commercial data brokers, and location metadata embedded in image files.

### 5.3 Social Engineering & OSINT Aggregation
Threat actors rarely hack accounts by brute-forcing high-entropy passwords. Instead, they aggregate contextual fragments from disparate public posts:
1. Employer and job title from a LinkedIn profile.
2. Coworker names and badge designs from Instagram celebration posts.
3. Travel dates from an X post.
By synthesizing these data points, the attacker crafts a personalized spear-phishing email masquerading as corporate IT, inducing the victim to disclose credentials or authorize malicious transactions.

---

## 6. Proposed System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Client Web Interface                       │
│  (Modern Responsive HTML5 / CSS3 Cyber UI / Chart.js Displays)   │
└────────────────────────────────┬────────────────────────────────┘
                                 │ HTTP / JSON REST
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask REST API Server                      │
│                                                                 │
│  ┌──────────────────────────┐    ┌───────────────────────────┐  │
│  │   Assessment Blueprints  │    │   Dashboard & Analytics   │  │
│  └─────────────┬────────────┘    └─────────────┬─────────────┘  │
│                │                               │                │
│                ▼                               ▼                │
│  ┌──────────────────────────┐    ┌───────────────────────────┐  │
│  │ Input Validation Module  │    │ In-Memory EXIF Inspector  │  │
│  │  (Zero PII Enforcement)  │    │  (RAM-Only Parsing/Strip) │  │
│  └─────────────┬────────────┘    └───────────────────────────┘  │
│                │                                                │
│                ▼                                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Privacy Risk Engine Pipeline                 │  │
│  │                                                           │  │
│  │  1. Feature Extraction (extract_privacy_features)         │  │
│  │  2. Category Scoring (10 Normalized Domains, 0-100)       │  │
│  │  3. Weighted Overall Scoring (calculate_privacy_risk)     │  │
│  │  4. Findings Generation (generate_privacy_findings)       │  │
│  │  5. Security Recommendations (Priority Sorting)          │  │
│  │  6. Improvement Simulator (Dynamic Recalculation)         │  │
│  └─────────────────────────────┬─────────────────────────────┘  │
└────────────────────────────────┼────────────────────────────────┘
                                 │ Parameterized SQL
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              Privacy-Preserving SQLite Storage                  │
│       (Stores ONLY assessment IDs, scores, and findings;         │
│          Zero telephone numbers, emails, or coordinates)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Questionnaire & Risk Rubric Design

The assessment is divided into 10 defense-in-depth categories encompassing 44 targeted questions:

| Category Code | Domain Name | Weight | Primary Risk Focus |
| :---: | :--- | :---: | :--- |
| **CAT_A** | Profile Visibility | 10% | Public discoverability, external search indexing, public avatars. |
| **CAT_B** | Personal Information | 15% | Public telephone numbers, personal emails, birth dates, employers. |
| **CAT_C** | Location Privacy | 15% | Live GPS check-ins, routine disclosures, vacation advance notices. |
| **CAT_D** | Posts & Content | 10% | Default post audiences, corporate badges in photos, minors. |
| **CAT_E** | Friends & Followers | 10% | Vetting unknown connections, public friend lists, follower approval. |
| **CAT_F** | Tagging & Mentions | 5% | Tag Review enabled, stranger mentions, facial recognition. |
| **CAT_G** | Account Security & MFA | 15% | Multi-Factor Authentication (TOTP vs SMS), password reuse, login alerts. |
| **CAT_H** | Third-Party Apps | 5% | OAuth integrations, excessive scopes, regular app revocation. |
| **CAT_I** | Social Engineering | 10% | Open DMs, suspicious link awareness, OTP forwarding scams. |
| **CAT_J** | Digital Footprint | 5% | Historical post auditing, abandoned accounts, self-OSINT searches. |

---

## 8. Feature Engineering & Risk Scoring Methodology

### 8.1 Category Score Normalization
Each question $q \in \text{Category}_c$ provides structured options mapped to calibrated risk contributions ($P_q \in [0, 100]$). The normalized category score $S_c$ is computed as:
$$S_c = \text{round}\left(\frac{\sum_{q \in \text{Category}_c} P_q}{|\text{Category}_c|}\right)$$

### 8.2 Overall Weighted Privacy Risk Score
The overall privacy risk score $R \in [0, 100]$ combines all 10 domain scores weighted by threat severity:
$$R = \text{round}\left(\frac{\sum_{c=1}^{10} S_c \times W_c}{\sum_{c=1}^{10} W_c}\right)$$
Where $\sum W_c = 1.0$.

### 8.3 Risk Tier Classification
* **0 – 20: LOW RISK** (Minimal public exposure, proactive security controls, disciplined sharing habits).
* **21 – 40: MODERATE RISK** (Typical consumer exposure, minor configuration gaps, manageable footprint).
* **41 – 70: HIGH RISK** (Substantial attack surface, multiple sensitive identifiers exposed, prime target for OSINT).
* **71 – 100: CRITICAL RISK** (Severe exposure, live GPS broadcasts, disabled MFA, acute risk of takeover/stalking).

---

## 9. Core Engineering Innovations

### 9.1 Privacy Improvement Simulator
The simulator allows users to test the impact of hardening their settings before making changes on live platforms. By selecting from 14 actionable improvements (e.g., hiding phone number, enabling TOTP MFA, turning on tag review), the simulator creates a deep copy of the baseline answers, applies the hardened values, recalculates all category scores, and reports the net score delta (e.g., from 72 Critical down to 34 Moderate, representing a 38-point reduction).

### 9.2 Safe In-Memory Photo EXIF Metadata Inspector
Many users upload photos unaware that smartphones embed GPS coordinates, camera hardware identifiers, and timestamps in JPEG/TIFF headers. To demonstrate this risk without creating privacy vulnerabilities:
- The backend parses JPEG APP1 EXIF markers **strictly in memory**.
- Extracted tags (Camera Make/Model, Creation Time, GPS Latitude/Longitude) are evaluated for privacy risk.
- A one-click sanitizer strips all EXIF segments in memory and returns a clean, sanitized JPEG byte stream for download.
- Zero raw image files or GPS coordinates are written to persistent storage.

### 9.3 Population Analytics & Synthetic Dataset
To provide meaningful organizational context, the framework includes a synthetic dataset generator (`data/generate_dataset.py`) producing 1,200 fictional assessment records modeling four realistic personas (Privacy Conscious, Average User, Casual Oversharer, High Exposure). The analytics dashboard visualizes population distributions, systemic weaknesses, and control adoption benchmarks using interactive Chart.js visualizations.

---

## 10. Verification, Testing & Quality Assurance
The system was validated using an automated test suite of **34 comprehensive unit and integration tests** in `pytest`:
- **Functional Tests:** Extreme profiles (fully private vs fully public), specific risk triggers (public phone, missing MFA, live check-ins, travel posts, badge photos).
- **Boundary Tests:** Verified mathematical transitions at scores 20 (Low/Moderate), 40 (Moderate/High), and 70 (High/Critical).
- **Security & PbD Tests:** Verified that database table schemas contain zero sensitive PII columns.
- **REST API Tests:** Tested `/api/health`, `/api/assessment` submission, and GDPR Article 17 `/api/assessment/{id}` erasure.
- **Result:** **34 passed in 0.50 seconds with 100% pass fidelity and zero warnings.**

---

## 11. Limitations & Ethical Safeguards
* **Self-Reported Data:** As a defensive tool, the framework relies on user honesty in answering configuration questions. It intentionally does not scrape or verify live account status to prevent invasive surveillance.
* **Educational Calibration:** Weights and thresholds represent defense-in-depth rubric assumptions; they do not guarantee that an account will never be compromised.
* **Consent-Driven Only:** The framework operates solely on self-owned accounts or voluntary demo inputs.

---

## 12. Conclusion
The **Social Media Privacy Risk Assessment Framework** demonstrates that effective cybersecurity risk assessment can be achieved without compromising user privacy. By coupling rigorous defense-in-depth principles, explainable scoring rubrics, interactive what-if simulation, and strict Privacy by Design compliance, this project provides a model for modern, human-centric privacy engineering.
