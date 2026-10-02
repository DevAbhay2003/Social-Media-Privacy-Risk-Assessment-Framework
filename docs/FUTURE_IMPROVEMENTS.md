# Defensive Roadmap: Future Framework Improvements

The **Social Media Privacy Risk Assessment Framework** is committed to defensive, consent-driven privacy engineering. The following roadmap outlines architectural enhancements designed to expand educational impact, enterprise maturity, and technical security without ever incorporating invasive surveillance, user scraping, or unauthorized tracking.

---

## 1. Planned Defensive Enhancements

### A. Platform-Specific Guided Walkthroughs
* **Concept:** Interactive step-by-step click-through guides for major ecosystems (Instagram, LinkedIn, X, TikTok, Facebook, Discord, GitHub).
* **Defensive Value:** Instead of generic advice, provide direct deeplinks and screenshot references guiding users directly to the specific toggle on each mobile OS (iOS/Android) and desktop interface.

### B. Enterprise & Organizational Policy Benchmarking
* **Concept:** Allow corporate security teams and university CISOs to define custom privacy compliance baselines (e.g., "Corporate Badge Photos = Forbidden", "MFA = Mandatory TOTP").
* **Defensive Value:** Tailors risk scoring to organization-specific threat models without inspecting private employee accounts.

### C. Gamified Security Awareness & Micro-Quizzes
* **Concept:** Embedded 60-second scenario quizzes illustrating real-world social engineering pretexts (e.g., spotting an emergency money transfer scam or detecting an impersonated LinkedIn recruiter).
* **Defensive Value:** Reinforces positive behavioral changes through scenario-based learning.

### D. Privacy Maturity Model (PMM) Scoring
* **Concept:** Implement a maturity scale (Tier 1: Ad-hoc / Exposed ➔ Tier 2: Reactive ➔ Tier 3: Hardened ➔ Tier 4: Zero-Footprint Pro) modeled after the NIST Cybersecurity Framework (CSF) and CIS Controls.
* **Defensive Value:** Provides progressive milestones for personal and corporate digital hygiene.

### E. Family & Teen Digital Safety Module
* **Concept:** Specialized rubric weighting for minors, focusing on school uniform obfuscation, location tagging around sports grounds, and cyberbullying perimeter defenses.
* **Defensive Value:** Empowers parents and educators to coach teenagers on responsible social media boundaries.

### F. Longitudinal Privacy Progress Tracking (Delta Over Time)
* **Concept:** Enable users to import past anonymized assessment JSONs to visualize their privacy score trend over 6, 12, and 24 months.
* **Defensive Value:** Visualizes sustained improvement and encourages periodic 6-month checkups.

### G. Client-Side WebAssembly (Wasm) / Pure Offline Local Mode
* **Concept:** Compile scoring logic and EXIF inspection into client-side WebAssembly or offline Progressive Web App (PWA).
* **Defensive Value:** Eliminates client-server communication completely, allowing high-risk journalists, activists, or executives to run assessments on isolated, air-gapped devices.

### H. Internationalization & Accessibility (i18n & a11y)
* **Concept:** Multilingual support (Spanish, French, German, Hindi, Japanese) and WCAG 2.1 AA compliant screen-reader accessibility.
* **Defensive Value:** Democratizes privacy defense education across global, non-technical demographics.

---

## 2. Explicit Anti-Goals (Features Strictly Prohibited)
To maintain our core ethical commitment, the framework will **never** incorporate:
- ❌ Automated profile scraping or web crawlers.
- ❌ Account enumeration or password brute-forcing utilities.
- ❌ Dark pattern surveillance or behavioral telemetry tracking.
- ❌ Harvesting of actual phone numbers, email addresses, or coordinates.
