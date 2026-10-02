# Social Media Privacy Risk Matrix

## 1. Risk Matrix Overview
Risk is evaluated as a function of **Likelihood** (the probability of observation, scraping, or exploitation) and **Impact** (the potential severity of physical, financial, psychological, or organizational harm).

```
   ▲ HIGH     [ Moderate Risk ]    [ High Risk ]        [ CRITICAL RISK ]
 I │
 M │ MEDIUM   [ Low Risk ]         [ Moderate Risk ]    [ High Risk ]
 P │
 A │ LOW      [ Low Risk ]         [ Low Risk ]         [ Moderate Risk ]
 C │
 T ┼──────────────────────────────────────────────────────────────────────►
              LOW                  MEDIUM               HIGH
                              L I K E L I H O O D
```

---

## 2. Risk Evaluation Table

| Privacy / Security Exposure Vector | Likelihood | Impact | Combined Risk Rating | Attack Vectors / Operational Consequences |
| :--- | :--- | :--- | :--- | :--- |
| **Real-Time Location Broadcasting (Snap Map / Check-in)** | **Medium** | **High** | **CRITICAL** | Stalking, physical confrontation, residential burglary during scheduled absences. |
| **Multi-Factor Authentication (MFA) Inactive** | **Medium** | **High** | **CRITICAL** | Account takeover via credential stuffing; loss of private messaging confidentiality. |
| **Sharing One-Time Passcodes (OTP) in DMs** | **Low** | **High** | **CRITICAL** | Immediate account hijacking, WhatsApp account theft, SIM-swap finalization. |
| **Posting Uncensored Images of Minors / School Crests** | **High** | **High** | **CRITICAL** | Child safety hazards, automated image harvesting, school routine tracking. |
| **Public Direct Phone Number in Bio** | **High** | **Medium** | **HIGH** | Smishing, unsolicited cold calling, telemarketing databases, SIM-swap targeting. |
| **Announcing Vacations / Travel Before Return** | **Medium** | **High** | **HIGH** | Verifiable signal of unoccupied residence, enabling burglary and property theft. |
| **Public Full Birth Date (Day, Month, Year)** | **High** | **Medium** | **HIGH** | Knowledge-based security question bypass, identity profiling, synthetic ID fraud. |
| **Clicking Unverified DM Links ('Is this you in video?')**| **Medium** | **High** | **HIGH** | Credential harvesting landing pages, session hijacking via cookie grabbers. |
| **Accepting Connection Requests from Unknown Profiles** | **High** | **Medium** | **HIGH** | Circumvention of friends-only privacy perimeter by sockpuppets and OSINT scrapers. |
| **Tag Review Disabled (Automatic Timeline Posting)** | **High** | **Medium** | **HIGH** | Third-party parties expose user's location, alcohol consumption, or sensitive contexts. |
| **Corporate ID Badges / Desk Monitors Displayed** | **Medium** | **High** | **HIGH** | Social engineering pretexting (BEC), badge replication, visual credential exposure. |
| **Password Reuse Across Multiple Services** | **High** | **High** | **CRITICAL** | Credential stuffing from unrelated third-party breach datasets. |
| **Public Personal Email Address** | **High** | **Low** | **MODERATE** | Mass spam lists, targeted spear-phishing campaigns, credential dictionary attacks. |
| **Unvetted Third-Party OAuth Apps Active** | **Medium** | **Medium** | **MODERATE** | Supply-chain data exposure if third-party app developer suffers database breach. |
| **External Search Engine Indexing Enabled** | **High** | **Low** | **MODERATE** | Uncontrolled discoverability, background check harvesting, cross-site identity linkage. |
| **Predictable Commute / Daily Routine Disclosures** | **Medium** | **Medium** | **MODERATE** | Pattern-of-life analysis allowing physical prediction of movements. |
| **Unrestricted Follower Ingestion** | **High** | **Low** | **MODERATE** | Passive bot subscription, automated scraping of newly published timeline updates. |
| **Dormant / Abandoned Social Accounts Left Active** | **Medium** | **Medium** | **MODERATE** | Silent takeover of stale handles for malicious impersonation. |
| **Facial Recognition Auto-Tagging Enabled** | **High** | **Low** | **LOW** | Platform biometric model training and automated relationship graph mapping. |
| **Unsanitized Bio / Public Avatar Context** | **High** | **Low** | **LOW** | Minor contextual hints (alma mater, industry) aiding passive OSINT profiling. |

---

## 3. Contextual Variance
> [!IMPORTANT]
> A risk matrix represents baseline probability assumptions. **Actual real-world risk depends directly on threat model context.** For example:
> - For a public creator or marketing influencer, a public email is necessary for business, while personal address exposure remains catastrophic.
> - For an enterprise executive, school administrator, or law enforcement officer, even minor workplace or schedule hints represent High or Critical severity.
