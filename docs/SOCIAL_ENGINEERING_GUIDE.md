# Educational Guide: How Oversharing Increases Social-Engineering Risk

## 1. Introduction: The Power of Context in Human Hacking
Social engineering is the psychological manipulation of people into performing actions or divulging confidential information. While traditional mass phishing relied on generic spam templates ("Click here to claim your prize"), modern threat actors leverage **Open Source Intelligence (OSINT)** gathered from social media profiles to construct high-trust, personalized communication.

Publicly available details do not automatically compromise an account, but they dramatically reduce the skepticism of the victim. When a message contains accurate, verifiable facts about someone's life, the human brain instinctively attributes legitimacy to the sender.

---

## 2. Exploited Information Categories & Attack Pretexting

### A. Current Employer & Workplace Context
* **Disclosed Facts:** Company name, job title, department, photos of corporate badge, attendance at company town halls, mentions of coworkers.
* **Adversary Pretexting Vector:** 
  - Attackers pose as the internal IT Helpdesk, HR department, or executive leadership.
  - An email or message stating: *"Hi [Name], regarding your role on the [Department] team, IT is migrating our Single Sign-On portal. Please verify your credentials at [phishing link]."*
  - The victim complies because the sender correctly named their specific role and department.

### B. Educational Institutions & Alumni Networks
* **Disclosed Facts:** High school, university graduation year, fraternity/sorority, campus societies.
* **Adversary Pretexting Vector:**
  - Scammers pose as the Alumni Association, student loan servicer, or reunion organizers.
  - Requests for "updated contact directories" or "urgent scholarship disbursements" trick users into submitting updated phone numbers, addresses, and employment data.

### C. Travel Schedules & Vacation Plans
* **Disclosed Facts:** Flight departure dates, hotel check-ins, countdown posts (*"Only 3 days until Rome!"*), out-of-office announcements.
* **Adversary Pretexting Vector:**
  - **Unoccupied Residence Exploitation:** Burglars know the exact window during which a home is empty.
  - **Emergency Impersonation Scams:** Attackers clone the traveler's account and message their elderly relatives or parents: *"I lost my phone and passport in Rome! Please wire emergency funds or send gift cards to this temporary contact."*

### D. Familial References & Relationships
* **Disclosed Facts:** Tagging children, spouses, siblings, parents, or pets; mentioning maiden names or childhood neighborhoods.
* **Adversary Pretexting Vector:**
  - **Knowledge-Based Authentication Bypass:** Many banking and email providers use security questions such as *"What was the name of your first pet?"*, *"What street did you grow up on?"*, or *"What is your mother's maiden name?"*. An OSINT scan often uncovers these answers within minutes.

### E. Niche Interests, Hobbies & Purchases
* **Disclosed Facts:** Specific camera equipment, marathon running events, crypto trading, vehicle purchases.
* **Adversary Pretexting Vector:**
  - Scammers send fraudulent warranty recall notices, fake race registration updates, or targeted spear-phishing tailored to specialized hobby communities.

### F. Attendance at Public Events & Conferences
* **Disclosed Facts:** Checking into industry summits, hackathons, concerts, or charity galas.
* **Adversary Pretexting Vector:**
  - Attackers circulate malicious PDF agendas or QR codes disguised as conference Wi-Fi portals or speaker slide downloads.

---

## 3. The Anatomy of a High-Trust Lure

```
[Public Fact on Social Media] ──► [Adversary Aggregates Context] ──► [High-Trust Communication Crafted]
           │                                                                    │
           ▼                                                                    ▼
"Just started as DevOps               Attacker references                 Target lowers guard &
at Acme Corp!"                        internal tools & boss               clicks credential harvest link
```

---

## 4. Defensive Countermeasures & Best Practices

1. **Decouple Identity from Public Broadcast:**
   - Keep professional accomplishments on professional networks (e.g., LinkedIn) and keep recreational and personal updates on strictly private accounts.
2. **Never Treat Outgoing Facts as Secrets:**
   - If a pet's name, school, or hometown is publicly visible on your profile, never select it as an authentication security question.
3. **Adopt Out-of-Band Verification:**
   - If a friend, colleague, or family member contacts you via DM asking for money, gift cards, or a verification code, immediately call them on their verified telephone number before acting.
4. **Retrospective Sharing Policy:**
   - Adopt the habit of posting vacation, concert, and travel photos *after* returning home safely.
5. **Periodic Account Pruning:**
   - Periodically remove old posts that contain outdated contact information, family tags, or unnecessary personal history.
