# Defensive Threat Model: Social Media User Footprint

## 1. Overview & Objectives
This threat model assesses the attack surface of an individual or enterprise employee maintaining personal or professional social media profiles. The analysis adopts an adversarial perspective (OSINT and threat reconnaissance) to formulate actionable, defense-in-depth countermeasures without engaging in offensive exploitation.

---

## 2. Threat Analysis Matrix

| Asset | Threat | Exposure Vector | Potential Impact | Existing Common Controls | Recommended Hardened Controls |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **User Account & Session** | **Account Takeover (ATO)** | Password reuse across breached external sites; absence of MFA; SMS OTP interception. | Unauthorized profile control, malicious posting, reputational damage, pivot into connected business tools. | Single password authentication; SMS 2FA. | Deploy hardware FIDO2 keys or app-based TOTP (RFC 6238); generate unique 16+ char passwords with a manager. |
| **Contact Identity Information** | **Smishing, SIM-Swapping & Targeted Phishing** | Direct phone number and personal email publicly listed in bio or contact fields. | Automated credential phishing, SIM hijack to bypass SMS OTP, telemarketing extortion. | Platform default visibility (often public). | Set phone and email visibility to **"Only Me"**; use masked email aliases for public correspondence. |
| **Location & Physical Safety** | **Physical Stalking & Unoccupied Burglary** | Real-time GPS check-ins; live Snap Map; posting vacation schedules in advance. | Physical confrontation, stalking, theft during known residential absence. | Manual location toggles. | Disable background geotagging; activate Snap Map **Ghost Mode**; publish travel photos retrospectively after returning home. |
| **Identity Verification Data** | **Identity Theft & Security Question Bypass** | Full birth date (day, month, year); mother's maiden name; high school or childhood pet references. | Resetting banking or email credentials by answering knowledge-based authentication questions. | Birthday displayed to friends or public. | Restrict birth date to Day and Month (hide year) or set to "Only Me"; never answer security questions with truthful social facts. |
| **Organizational Context & Badges** | **Business Email Compromise (BEC) & Spear-Phishing** | Photos displaying corporate ID badges, building floor plans, access tiers, and desk monitors. | Adversaries craft tailored pretexting emails posing as internal IT or executives; physical badge cloning. | Corporate social media guidelines. | Strict prohibition on photographing corporate credentials, badges, monitors, or access control doors. |
| **Social Graph & Relationships** | **Pretexting & Friend Impersonation Scams** | Public friends/followers list; tagging close family relations publicly. | Attackers clone friend profiles and send emergency pleas for money, gift cards, or OTP forwarding. | Default public follower visibility. | Set "Who can see your friends list?" to **"Only Me"**; mandate out-of-band telephone verification for financial requests. |
| **Application Ecosystem** | **Supply Chain & Third-Party App Compromise** | Legacy OAuth tokens granted to interactive viral quizzes, games, and unmaintained analytics tools. | Silent API data harvesting; unauthorized profile reading or token leakage during third-party breaches. | OAuth consent screen. | Apply the **Principle of Least Privilege**: audit connected apps biannually and revoke inactive integrations immediately. |
| **Historical Digital Footprint** | **Doxxing & Contextual OSINT Scraping** | 5-10 years of unpruned timeline posts, old comments, and dormant secondary accounts. | Attackers reconstruct a complete lifetime biography, mapping addresses, previous affiliations, and opinions. | None (permanent timeline). | Conduct annual timeline audits; purge posts older than 12-24 months; permanently delete abandoned platform accounts. |

---

## 3. Threat Actor Profiles & Capabilities
1. **Automated Scraping Bots:** Harvest public emails, phone numbers, and handles from public bios to populate mass spam, credential-stuffing, and telemarketing databases.
2. **Social Engineers & Pretexters:** Investigate publicly disclosed employers, colleges, and hobbies to establish rapport and trick victims into clicking malicious links or forwarding OTP codes.
3. **Opportunistic Criminals:** Monitor vacation announcements and check-in geotags to verify vacant residences.
4. **Credential Stuffing Networks:** Correlate public emails with leaked third-party database breaches, testing passwords against social logins where MFA is inactive.

---

## 4. Defensive Posture Summary
Defending online privacy requires treating social media as an untrusted public broadcast network. Privacy hygiene is achieved through:
- **Data Minimization:** Refusing to publish non-essential identifiers.
- **Access Control:** Enforcing Private or Friends-Only visibility walls.
- **Verification Decoupling:** Never using public biographical facts as authentication secrets.
