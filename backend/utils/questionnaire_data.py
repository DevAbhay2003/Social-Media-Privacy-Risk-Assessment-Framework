"""
Social Media Privacy Risk Assessment Framework
Questionnaire Master Definitions & Security Rules
===================================================
Contains 44 structured questions divided into 10 defense-in-depth categories.
Strictly adheres to Privacy by Design and Data Minimization:
- No real PII is requested or collected.
- Assesses exposure configurations and behavioral patterns only.
"""

CATEGORY_DEFINITIONS = {
    "CAT_A": {
        "code": "CAT_A",
        "name": "Profile Visibility",
        "weight": 0.10,
        "description": "Evaluates public discoverability, search indexing, and profile footprint exposure."
    },
    "CAT_B": {
        "code": "CAT_B",
        "name": "Personal Information",
        "weight": 0.15,
        "description": "Assesses public exposure of contact details, birth date, education, and family information."
    },
    "CAT_C": {
        "code": "CAT_C",
        "name": "Location Privacy",
        "weight": 0.15,
        "description": "Analyzes real-time check-ins, routine disclosures, geotagging, and travel plan announcements."
    },
    "CAT_D": {
        "code": "CAT_D",
        "name": "Posts & Content",
        "weight": 0.10,
        "description": "Evaluates post default audiences, sensitive visual indicators (badges, screens), and minors."
    },
    "CAT_E": {
        "code": "CAT_E",
        "name": "Friends & Followers",
        "weight": 0.10,
        "description": "Reviews connection vetting practices, friends list visibility, and follower auditing."
    },
    "CAT_F": {
        "code": "CAT_F",
        "name": "Tagging & Mentions",
        "weight": 0.05,
        "description": "Evaluates tag approval workflows, unsolicited timeline mentions, and facial recognition tags."
    },
    "CAT_G": {
        "code": "CAT_G",
        "name": "Authentication & Account Security",
        "weight": 0.15,
        "description": "Assesses Multi-Factor Authentication (MFA), password hygiene, login alerts, and active sessions."
    },
    "CAT_H": {
        "code": "CAT_H",
        "name": "Third-Party Applications",
        "weight": 0.05,
        "description": "Evaluates OAuth integrations, app permissions, and periodic integration revocation."
    },
    "CAT_I": {
        "code": "CAT_I",
        "name": "Messaging & Social Engineering",
        "weight": 0.10,
        "description": "Measures susceptibility to unsolicited DMs, unexpected links, verification scams, and impersonation."
    },
    "CAT_J": {
        "code": "CAT_J",
        "name": "Digital Footprint",
        "weight": 0.05,
        "description": "Assesses historical post exposure, abandoned accounts, public comments, and privacy checkups."
    }
}

QUESTIONS = [
    # =========================================================================
    # CATEGORY A: Profile Visibility (4 Questions)
    # =========================================================================
    {
        "id": "Q_A1",
        "category_code": "CAT_A",
        "category_name": "Profile Visibility",
        "question": "What is the primary visibility setting of your main social media account?",
        "help_text": "Public accounts allow anyone on the internet, including automated scrapers, to view your content.",
        "options": [
            {"label": "Public (visible to anyone on or off the platform)", "value": "PUBLIC", "risk_points": 100},
            {"label": "Friends / Followers Only", "value": "FRIENDS", "risk_points": 30},
            {"label": "Private / Restricted to approved contacts", "value": "PRIVATE", "risk_points": 0}
        ],
        "risk_trigger": ["PUBLIC", "FRIENDS"],
        "finding_title": "Open Profile Visibility",
        "finding_desc": "Profile visibility is configured as open or broadly shared, increasing passive reconnaissance surface.",
        "severity": "HIGH",
        "recommendation_title": "Restrict Primary Profile Visibility",
        "recommendation_text": "Switch account visibility to Private or Friends Only to require authorization before viewing profile details.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_A2",
        "category_code": "CAT_A",
        "category_name": "Profile Visibility",
        "question": "Is your profile indexed by external search engines (e.g., Google, Bing)?",
        "help_text": "Search engine indexing makes your profile discoverable to anyone querying your name or aliases.",
        "options": [
            {"label": "Yes / Enabled", "value": "YES", "risk_points": 100},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 60},
            {"label": "No / Disabled in privacy settings", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "NOT_SURE"],
        "finding_title": "Search Engine Discoverability Enabled",
        "finding_desc": "External search engines can index your profile, linking your real identity to platform activity.",
        "severity": "MEDIUM",
        "recommendation_title": "Disable External Search Engine Indexing",
        "recommendation_text": "Navigate to Privacy Settings > Discoverability and disable 'Allow search engines outside of the platform to link to your profile'.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_A3",
        "category_code": "CAT_A",
        "category_name": "Profile Visibility",
        "question": "Can strangers look you up using your email address or phone number?",
        "help_text": "Lookups by contact info enable account correlation across different websites and leaked breach datasets.",
        "options": [
            {"label": "Yes, anyone can look me up", "value": "YES", "risk_points": 100},
            {"label": "Friends of friends / Limited", "value": "SOMETIMES", "risk_points": 50},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 70},
            {"label": "No, discoverability by contact info is disabled", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES", "NOT_SURE"],
        "finding_title": "Contact-Based Profile Discoverability",
        "finding_desc": "Strangers or threat actors can discover your profile by cross-referencing harvested phone numbers or emails.",
        "severity": "HIGH",
        "recommendation_title": "Disable Contact-Based Lookup",
        "recommendation_text": "Configure discoverability settings to 'Only Me' or 'Friends' for phone and email lookup.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_A4",
        "category_code": "CAT_A",
        "category_name": "Profile Visibility",
        "question": "Is your profile picture or bio accessible to the general public regardless of account privacy?",
        "help_text": "Many platforms keep avatars and bios public even when accounts are private, leaking visual and occupational context.",
        "options": [
            {"label": "Yes, avatar and detailed bio are public", "value": "YES", "risk_points": 100},
            {"label": "Avatar is public, but bio is minimal/empty", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, avatar and bio are restricted or completely generic", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Bio & Avatar Public Reconnaissance Context",
        "finding_desc": "Your public bio or avatar contains employer, university, or personal details readable without authorization.",
        "severity": "LOW",
        "recommendation_title": "Sanitize Public Profile Bio & Picture",
        "recommendation_text": "Remove specific workplace, educational, or contact references from your publicly visible bio.",
        "priority": "GOOD PRACTICE"
    },

    # =========================================================================
    # CATEGORY B: Personal Information (5 Questions)
    # =========================================================================
    {
        "id": "Q_B1",
        "category_code": "CAT_B",
        "category_name": "Personal Information",
        "question": "Is your phone number publicly visible anywhere on your profile or bio?",
        "help_text": "Exposed phone numbers lead directly to SMS phishing (smishing), SIM swapping, and telemarketing abuse.",
        "options": [
            {"label": "Yes, it is visible on my profile/contact card", "value": "YES", "risk_points": 100},
            {"label": "Visible only to connections/friends", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, it is hidden or not linked", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Public Phone Number Exposure",
        "finding_desc": "Your direct telephone number is publicly exposed, creating significant risk of SMS phishing, SIM hijacking, and identity theft.",
        "severity": "CRITICAL",
        "recommendation_title": "Hide Phone Number from Public Display",
        "recommendation_text": "Immediately set phone number visibility to 'Only Me' or remove it from public-facing bio fields.",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_B2",
        "category_code": "CAT_B",
        "category_name": "Personal Information",
        "question": "Is your personal email address publicly visible on your profile?",
        "help_text": "Public personal emails are harvested by automated bots for credential stuffing, spear-phishing, and spam lists.",
        "options": [
            {"label": "Yes, visible in my bio or about section", "value": "YES", "risk_points": 100},
            {"label": "Visible only to approved connections", "value": "SOMETIMES", "risk_points": 35},
            {"label": "No, hidden or masked", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Public Email Exposure",
        "finding_desc": "Personal email address is displayed publicly, exposing you to targeted spear-phishing and automated spam harvesting.",
        "severity": "HIGH",
        "recommendation_title": "Hide or Mask Personal Email",
        "recommendation_text": "Remove your personal email from public display. If business contact is required, use a disposable alias or contact form.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_B3",
        "category_code": "CAT_B",
        "category_name": "Personal Information",
        "question": "Do you publicly share your full birth date (day, month, and year)?",
        "help_text": "Full birth dates are critical verification tokens used by banks, utilities, and security question prompts.",
        "options": [
            {"label": "Yes, full day, month, and year are public", "value": "YES", "risk_points": 100},
            {"label": "Only day and month (year hidden)", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, birth date is completely private/hidden", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Birth Date Disclosure",
        "finding_desc": "Displaying full or partial birth dates supplies threat actors with high-value identity verification data for social engineering.",
        "severity": "HIGH",
        "recommendation_title": "Hide Birth Date & Year",
        "recommendation_text": "Adjust birthday privacy settings to hide the birth year, or set the entire date to 'Only Me'.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_B4",
        "category_code": "CAT_B",
        "category_name": "Personal Information",
        "question": "Is your specific current employer or educational institution publicly displayed?",
        "help_text": "Workplace context allows attackers to craft realistic business email compromise (BEC) and tailored workplace phishing.",
        "options": [
            {"label": "Yes, specific company and role are displayed", "value": "YES", "risk_points": 90},
            {"label": "General industry only, or visible only to friends", "value": "SOMETIMES", "risk_points": 30},
            {"label": "No, not disclosed on social media", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Employer / Educational Affiliation Exposure",
        "finding_desc": "Publicly linking specific employers or campuses increases vulnerability to spear-phishing disguised as colleagues or HR.",
        "severity": "MEDIUM",
        "recommendation_title": "Limit Workplace Specifics on Casual Profiles",
        "recommendation_text": "Reserve employer details for professional networks (LinkedIn) and limit exposure on recreational social media.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_B5",
        "category_code": "CAT_B",
        "category_name": "Personal Information",
        "question": "Do you publicly post details about your family members, children, or relationship status?",
        "help_text": "Family references (maiden names, kids' names) are standard answers to security verification questions.",
        "options": [
            {"label": "Yes, family members and relationships are tagged publicly", "value": "YES", "risk_points": 100},
            {"label": "Occasionally / Only general references", "value": "SOMETIMES", "risk_points": 45},
            {"label": "No, family and relationship details are kept private", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Family & Relationship Information Exposure",
        "finding_desc": "Disclosing familial relationships gives attackers clues for password recovery security questions (e.g., mother's maiden name).",
        "severity": "MEDIUM",
        "recommendation_title": "Protect Family & Relationship Information",
        "recommendation_text": "Avoid public relationship listings and never disclose details commonly utilized as account security questions.",
        "priority": "IMPORTANT"
    },

    # =========================================================================
    # CATEGORY C: Location Privacy (5 Questions)
    # =========================================================================
    {
        "id": "Q_C1",
        "category_code": "CAT_C",
        "category_name": "Location Privacy",
        "question": "Do you share your real-time or live location (e.g., check-ins, Snapchat Snap Map, live location)?",
        "help_text": "Broadcasting live locations informs observers exactly where you are and when you are away from home.",
        "options": [
            {"label": "Yes, regularly or enabled continuously", "value": "YES", "risk_points": 100},
            {"label": "Occasionally during special events", "value": "SOMETIMES", "risk_points": 60},
            {"label": "No, real-time location sharing is disabled", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Real-Time Location Broadcasting",
        "finding_desc": "Broadcasting real-time location creates acute physical security risks, stalking vectors, and confirms absence from residence.",
        "severity": "CRITICAL",
        "recommendation_title": "Disable Real-Time Location Sharing",
        "recommendation_text": "Turn off continuous location features like Snap Map (Ghost Mode) and avoid live check-ins at public venues.",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_C2",
        "category_code": "CAT_C",
        "category_name": "Location Privacy",
        "question": "Do you attach geotags (precise location tags) to photos and posts?",
        "help_text": "Geotags reveal exact geographic coordinates where photos or messages were created.",
        "options": [
            {"label": "Yes, most posts include location tags", "value": "YES", "risk_points": 90},
            {"label": "Sometimes / City level only", "value": "SOMETIMES", "risk_points": 45},
            {"label": "No, location tagging is turned off", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Precise Post Geotagging",
        "finding_desc": "Geotagging posts exposes regular hangout spots, residential areas, and daily routines to OSINT analysts.",
        "severity": "HIGH",
        "recommendation_title": "Disable Automatic Geotagging",
        "recommendation_text": "Revoke camera and social media app permissions to access precise GPS location on your smartphone.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_C3",
        "category_code": "CAT_C",
        "category_name": "Location Privacy",
        "question": "Do you post travel plans or vacation updates before or while you are away from home?",
        "help_text": "Announcing dates of absence publicly signals that your primary residence is currently unoccupied.",
        "options": [
            {"label": "Yes, I announce trips before or while traveling", "value": "YES", "risk_points": 100},
            {"label": "Sometimes while traveling, but not in advance", "value": "SOMETIMES", "risk_points": 50},
            {"label": "No, I only post photos after returning home", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Unoccupied Residence / Travel Exposure",
        "finding_desc": "Posting travel schedules or real-time vacation updates informs malicious actors that your home is vacant.",
        "severity": "HIGH",
        "recommendation_title": "Post Vacation Content Retrospectively",
        "recommendation_text": "Adopt the best practice of publishing vacation photos only after returning safely home.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_C4",
        "category_code": "CAT_C",
        "category_name": "Location Privacy",
        "question": "Have you ever posted photos containing your house number, street signs, or distinctive exterior views?",
        "help_text": "OSINT techniques (Google Street View matching) can pinpoint exact residential addresses from minor visual cues.",
        "options": [
            {"label": "Yes, house or street details are visible in posts", "value": "YES", "risk_points": 100},
            {"label": "Not sure / possibly in background", "value": "NOT_SURE", "risk_points": 60},
            {"label": "No, I intentionally blur or exclude home exteriors", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "NOT_SURE"],
        "finding_title": "Residential Environment Visual Clues",
        "finding_desc": "Street signs, house numbers, or identifiable architecture in photos permit geolocation of your exact home address.",
        "severity": "HIGH",
        "recommendation_title": "Audit Home Visuals and Blur Street Details",
        "recommendation_text": "Audit past photos for identifiable home markers, street names, or vehicle license plates, and delete or crop them.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_C5",
        "category_code": "CAT_C",
        "category_name": "Location Privacy",
        "question": "Do you regularly post about your recurring daily routines (e.g., 'Daily 7am gym workout' or daily commute route)?",
        "help_text": "Predictable schedule patterns allow adversaries to anticipate your physical movements.",
        "options": [
            {"label": "Yes, routine schedules are frequently shared", "value": "YES", "risk_points": 85},
            {"label": "Occasionally mention workout or commute times", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, I avoid posting predictable timing and routes", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Predictable Routine Pattern Disclosure",
        "finding_desc": "Recurring schedule disclosures establish predictable time-and-place patterns accessible to bad actors.",
        "severity": "MEDIUM",
        "recommendation_title": "Desynchronize Activity Posts",
        "recommendation_text": "Avoid posting timestamps or recurring gym/commute routes; share milestones retrospectively.",
        "priority": "GOOD PRACTICE"
    },

    # =========================================================================
    # CATEGORY D: Posts & Content (4 Questions)
    # =========================================================================
    {
        "id": "Q_D1",
        "category_code": "CAT_D",
        "category_name": "Posts & Content",
        "question": "What is the default audience configuration for new posts you publish?",
        "help_text": "Defaulting to public means every post is shared globally unless manually overridden every time.",
        "options": [
            {"label": "Public (anyone can view)", "value": "PUBLIC", "risk_points": 100},
            {"label": "Friends / Followers Only", "value": "FRIENDS", "risk_points": 25},
            {"label": "Custom Close Friends list / Private", "value": "PRIVATE", "risk_points": 0}
        ],
        "risk_trigger": ["PUBLIC"],
        "finding_title": "Public Default Post Audience",
        "finding_desc": "Your default post audience is set to Public, meaning all new content is broadcast globally by default.",
        "severity": "HIGH",
        "recommendation_title": "Change Default Post Audience to Friends",
        "recommendation_text": "Update default sharing audience in account settings to 'Friends' or 'Followers' instead of 'Public'.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_D2",
        "category_code": "CAT_D",
        "category_name": "Posts & Content",
        "question": "Have you posted photos displaying employee badges, conference badges, access cards, or office desk setups?",
        "help_text": "Badges often display bar codes, company logos, and access tiers used to clone credentials or bypass physical security.",
        "options": [
            {"label": "Yes, new job/badge celebration photos are posted", "value": "YES", "risk_points": 90},
            {"label": "Possibly in the background of office photos", "value": "SOMETIMES", "risk_points": 50},
            {"label": "No, I never post credentials or workplace keys", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Physical Security Credential / Badge Exposure",
        "finding_desc": "Displaying corporate badges, building passes, or internal computer screens facilitates corporate espionage and badge cloning.",
        "severity": "HIGH",
        "recommendation_title": "Remove or Blur Corporate Badges",
        "recommendation_text": "Review and delete photos showing company ID badges, internal monitors, desks, or access control passes.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_D3",
        "category_code": "CAT_D",
        "category_name": "Posts & Content",
        "question": "Do you post photos of children, minor family members, or school uniforms on public accounts?",
        "help_text": "Children cannot provide legal consent; public photos risk unwanted scraping, school identification, and exploitation.",
        "options": [
            {"label": "Yes, photos of minors/school uniforms are public", "value": "YES", "risk_points": 100},
            {"label": "Shared only with close, approved family/friends", "value": "FRIENDS", "risk_points": 30},
            {"label": "No, I never share photos of minors on social media", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Minors & School Uniform Exposure",
        "finding_desc": "Posting images of minors or recognizable school crests on public platforms risks child safety and identity profiling.",
        "severity": "CRITICAL",
        "recommendation_title": "Restrict Children's Images & Obscure School Uniforms",
        "recommendation_text": "Make accounts strictly private, blur faces of minors, and never reveal school logos or schedules.",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_D4",
        "category_code": "CAT_D",
        "category_name": "Posts & Content",
        "question": "Do you post photos displaying vehicle license plates, boarding passes, or event tickets?",
        "help_text": "Boarding pass barcodes contain passenger name records (PNRs), frequent flyer numbers, and passport metadata.",
        "options": [
            {"label": "Yes, have posted boarding passes or car photos without blurring", "value": "YES", "risk_points": 95},
            {"label": "Sometimes blur parts of it", "value": "SOMETIMES", "risk_points": 45},
            {"label": "No, I strictly avoid posting tickets or license plates", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Barcodes / Boarding Passes / Vehicle Registration Exposure",
        "finding_desc": "Posting boarding pass barcodes or vehicle plates permits unauthorized itinerary modification or driver registration lookup.",
        "severity": "HIGH",
        "recommendation_title": "Never Post Travel Tickets or Barcodes",
        "recommendation_text": "Never upload photos of concert tickets, boarding passes, or clear car license plates.",
        "priority": "IMPORTANT"
    },

    # =========================================================================
    # CATEGORY E: Friends / Followers (4 Questions)
    # =========================================================================
    {
        "id": "Q_E1",
        "category_code": "CAT_E",
        "category_name": "Friends & Followers",
        "question": "How do you handle connection or follow requests from people you do not recognize?",
        "help_text": "Fake profiles are commonly used by OSINT investigators and social engineers to bypass friends-only privacy walls.",
        "options": [
            {"label": "I frequently accept requests to grow my network", "value": "YES", "risk_points": 100},
            {"label": "I sometimes accept if we have mutual connections", "value": "SOMETIMES", "risk_points": 60},
            {"label": "I only accept people I know and have verified in real life", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Unvetted Connection Acceptance",
        "finding_desc": "Accepting unknown or unverified profiles bypasses your friends-only privacy perimeter, exposing private posts.",
        "severity": "HIGH",
        "recommendation_title": "Verify Connections Before Accepting",
        "recommendation_text": "Vet unknown connection requests via independent channels before accepting; maintain a strict boundary.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_E2",
        "category_code": "CAT_E",
        "category_name": "Friends & Followers",
        "question": "Is your friends list or follower list visible to the public or strangers?",
        "help_text": "Public friend lists enable attackers to identify your close confidants and mount spear-phishing or impersonation scams.",
        "options": [
            {"label": "Yes, anyone can see my entire friends/followers list", "value": "YES", "risk_points": 90},
            {"label": "Visible only to mutual friends", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, set to 'Only Me' or hidden", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Public Friends & Followers List",
        "finding_desc": "Publicly exposing your social graph enables adversary mapping of relationships for targeted pretexting.",
        "severity": "MEDIUM",
        "recommendation_title": "Hide Friends / Follower List",
        "recommendation_text": "Set 'Who can see your friends list?' to 'Only Me' to shield your contacts from profiling.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_E3",
        "category_code": "CAT_E",
        "category_name": "Friends & Followers",
        "question": "Do you require approval for new followers, or can anyone follow your account automatically?",
        "help_text": "Requiring approval ensures nobody gains access to your posts without explicit permission.",
        "options": [
            {"label": "Anyone can follow automatically without approval", "value": "YES", "risk_points": 90},
            {"label": "Approval is required for all new followers", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Automatic Follower Ingestion Without Review",
        "finding_desc": "Allowing automatic follows enables bots and adversaries to subscribe to your feed without gatekeeping.",
        "severity": "MEDIUM",
        "recommendation_title": "Enable Follower Approval Requirement",
        "recommendation_text": "Enable 'Private Account' or 'Require Follow Approval' in your profile settings.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_E4",
        "category_code": "CAT_E",
        "category_name": "Friends & Followers",
        "question": "Do you periodically audit your friends or followers to remove inactive or unfamiliar accounts?",
        "help_text": "Over time, accounts of former contacts may be hacked, abandoned, or repurposed by threat actors.",
        "options": [
            {"label": "No, I never remove or audit old connections", "value": "NO", "risk_points": 80},
            {"label": "Rarely / Every few years", "value": "SOMETIMES", "risk_points": 40},
            {"label": "Yes, I conduct periodic reviews (at least once a year)", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "SOMETIMES"],
        "finding_title": "Absence of Periodic Connection Hygiene Audits",
        "finding_desc": "Accumulating stale connections over years leaves dormant or potentially compromised accounts inside your private circle.",
        "severity": "LOW",
        "recommendation_title": "Schedule Annual Connection Audits",
        "recommendation_text": "Dedicate time annually to prune unfamiliar followers, inactive accounts, and ex-acquaintances.",
        "priority": "GOOD PRACTICE"
    },

    # =========================================================================
    # CATEGORY F: Tagging & Mentions (4 Questions)
    # =========================================================================
    {
        "id": "Q_F1",
        "category_code": "CAT_F",
        "category_name": "Tagging & Mentions",
        "question": "Is Tag Review enabled (requiring your explicit approval before tagged posts appear on your profile)?",
        "help_text": "Other people can tag you in photos or check-ins that expose your location and activities without your knowledge.",
        "options": [
            {"label": "No, tags appear automatically on my profile", "value": "NO", "risk_points": 100},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 65},
            {"label": "Yes, Tag Review is turned on and I approve each post", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "NOT_SURE"],
        "finding_title": "Tag Review Disabled",
        "finding_desc": "Third parties can tag you in locations or contexts that automatically attach to your profile without prior consent.",
        "severity": "HIGH",
        "recommendation_title": "Enable Tag Review & Timeline Approval",
        "recommendation_text": "Turn on 'Review posts you are tagged in before the post appears on your profile'.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_F2",
        "category_code": "CAT_F",
        "category_name": "Tagging & Mentions",
        "question": "Can strangers or people you do not follow tag or mention your username in public posts?",
        "help_text": "Spammers and cryptocurrency scammers tag random users in malicious comment threads to deliver malicious links.",
        "options": [
            {"label": "Yes, anyone can tag or mention me", "value": "YES", "risk_points": 85},
            {"label": "Only people I follow or mutual connections", "value": "NO", "risk_points": 0},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 50}
        ],
        "risk_trigger": ["YES", "NOT_SURE"],
        "finding_title": "Unrestricted Mentions & Tagging by Strangers",
        "finding_desc": "Permitting anyone to mention you exposes your profile to mass phishing tags, harassment, and crypto spam schemes.",
        "severity": "MEDIUM",
        "recommendation_title": "Restrict Mentions to Approved Connections",
        "recommendation_text": "Configure 'Who can @mention you' to 'People You Follow' or 'No One'.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_F3",
        "category_code": "CAT_F",
        "category_name": "Tagging & Mentions",
        "question": "Do you permit platforms to automatically identify your face in photos uploaded by others (facial recognition)?",
        "help_text": "Facial recognition systems build biometric templates linking your offline face to your digital social identity.",
        "options": [
            {"label": "Yes / Enabled", "value": "YES", "risk_points": 90},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 55},
            {"label": "No / Disabled facial recognition features", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "NOT_SURE"],
        "finding_title": "Biometric Facial Recognition Auto-Tagging Enabled",
        "finding_desc": "Automatic facial recognition creates biometric vectors linking your physical image to uploaded photos across the platform.",
        "severity": "MEDIUM",
        "recommendation_title": "Opt-Out of Platform Facial Recognition",
        "recommendation_text": "Locate Face Recognition settings and toggle off automatic face suggestion and recognition features.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_F4",
        "category_code": "CAT_F",
        "category_name": "Tagging & Mentions",
        "question": "When others tag you in an embarrassing or location-sensitive post, do you know how to remove the tag?",
        "help_text": "Untagging yourself dissociates your profile from undesirable or compromising content posted by others.",
        "options": [
            {"label": "No / Never had to do it", "value": "NO", "risk_points": 70},
            {"label": "Yes, I actively untag myself from risky posts", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO"],
        "finding_title": "Lack of Tag Removal Familiarity",
        "finding_desc": "Inability to untag yourself limits your remediation capability when acquaintances publish sensitive content.",
        "severity": "LOW",
        "recommendation_title": "Practice Post Untagging & Audience Removal",
        "recommendation_text": "Familiarize yourself with the 'Remove Tag' and 'Hide from Profile' options on each active platform.",
        "priority": "GOOD PRACTICE"
    },

    # =========================================================================
    # CATEGORY G: Authentication & Account Security (5 Questions)
    # =========================================================================
    {
        "id": "Q_G1",
        "category_code": "CAT_G",
        "category_name": "Authentication & Account Security",
        "question": "Do you have Multi-Factor Authentication (MFA / 2FA) enabled on your social media accounts?",
        "help_text": "MFA blocks up to 99% of bulk automated credential attacks by requiring a second verification factor.",
        "options": [
            {"label": "No, MFA is disabled", "value": "NO", "risk_points": 100},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 70},
            {"label": "Yes, MFA is enabled", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "NOT_SURE"],
        "finding_title": "Multi-Factor Authentication (MFA) Inactive",
        "finding_desc": "Account relies solely on a single password, leaving it exposed to credential stuffing, dictionary attacks, and data leaks.",
        "severity": "CRITICAL",
        "recommendation_title": "Enable Multi-Factor Authentication Immediately",
        "recommendation_text": "Enable MFA under Security Settings using an Authenticator App (Google Authenticator, Bitwarden, or hardware security key).",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_G2",
        "category_code": "CAT_G",
        "category_name": "Authentication & Account Security",
        "question": "What primary method do you use for Multi-Factor Authentication?",
        "help_text": "Hardware keys and authenticator apps are significantly more secure than SMS text codes, which can be intercepted or SIM-swapped.",
        "options": [
            {"label": "I do not use MFA", "value": "NONE", "risk_points": 100},
            {"label": "SMS Text Message (OTP)", "value": "SMS", "risk_points": 45},
            {"label": "Authenticator App (TOTP) or Hardware Security Key (FIDO2)", "value": "APP_KEY", "risk_points": 0}
        ],
        "risk_trigger": ["NONE", "SMS"],
        "finding_title": "Weak or Absent MFA Method (SMS Vulnerability)",
        "finding_desc": "SMS-based MFA is susceptible to SIM-swapping, SS7 telecom vulnerabilities, and automated phishing proxies.",
        "severity": "HIGH",
        "recommendation_title": "Upgrade from SMS to Authenticator App or FIDO Key",
        "recommendation_text": "Transition from SMS verification to an app-based TOTP generator or hardware security key (YubiKey).",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_G3",
        "category_code": "CAT_G",
        "category_name": "Authentication & Account Security",
        "question": "Do you reuse the same password across multiple online accounts or social platforms?",
        "help_text": "If a reused password is breached on any minor website, attackers will test it against all your major accounts.",
        "options": [
            {"label": "Yes, I use the same or very similar passwords everywhere", "value": "YES", "risk_points": 100},
            {"label": "I have 2 or 3 passwords I rotate between accounts", "value": "SOMETIMES", "risk_points": 65},
            {"label": "No, I use unique, strong passwords (or a password manager)", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Password Reuse / Credential Stuffing Vulnerability",
        "finding_desc": "Password repetition enables credential stuffing; a single compromised database can compromise your social profiles.",
        "severity": "CRITICAL",
        "recommendation_title": "Deploy a Password Manager with Unique Passwords",
        "recommendation_text": "Adopt a password manager (e.g., Bitwarden, 1Password) to generate and store 16+ character unique passwords.",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_G4",
        "category_code": "CAT_G",
        "category_name": "Authentication & Account Security",
        "question": "Do you have Unrecognized Login Alerts enabled (notifications when your account is accessed from a new device/browser)?",
        "help_text": "Login alerts provide immediate warning of unauthorized sessions, allowing quick password resets.",
        "options": [
            {"label": "No / Disabled", "value": "NO", "risk_points": 85},
            {"label": "Not Sure", "value": "NOT_SURE", "risk_points": 50},
            {"label": "Yes, enabled via email or push notifications", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "NOT_SURE"],
        "finding_title": "Login Alerts Disabled",
        "finding_desc": "Absence of real-time login alerts delays discovery if a threat actor gains unauthorized session access.",
        "severity": "HIGH",
        "recommendation_title": "Turn On Unrecognized Login Alerts",
        "recommendation_text": "Enable 'Get alerts about unrecognized logins' to receive instant notifications of novel devices or IP addresses.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_G5",
        "category_code": "CAT_G",
        "category_name": "Authentication & Account Security",
        "question": "Do you regularly review active login sessions and terminate unrecognized devices?",
        "help_text": "Old phones, public computers, or compromised browser cookies can maintain active sessions indefinitely.",
        "options": [
            {"label": "No, I never check active sessions", "value": "NO", "risk_points": 80},
            {"label": "Rarely / Only when problems arise", "value": "SOMETIMES", "risk_points": 40},
            {"label": "Yes, I regularly inspect and terminate stale sessions", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "SOMETIMES"],
        "finding_title": "Stale Session Retention",
        "finding_desc": "Neglecting active session logs allows lingering sessions on shared or obsolete devices to remain authenticated.",
        "severity": "MEDIUM",
        "recommendation_title": "Review Where You're Logged In",
        "recommendation_text": "Visit Security > 'Where You're Logged In' and log out of all devices you do not currently operate.",
        "priority": "GOOD PRACTICE"
    },

    # =========================================================================
    # CATEGORY H: Third-Party Apps (4 Questions)
    # =========================================================================
    {
        "id": "Q_H1",
        "category_code": "CAT_H",
        "category_name": "Third-Party Applications",
        "question": "Have you used 'Sign in with Facebook / Google / Apple' or connected quizzes, games, or analytics tools to your account?",
        "help_text": "Connected apps often retain API access tokens granting permissions to read profiles, contacts, or posts.",
        "options": [
            {"label": "Yes, I have connected numerous third-party apps and quizzes", "value": "YES", "risk_points": 85},
            {"label": "Only a few critical services", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, I avoid third-party social logins and quizzes", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Extensive Third-Party OAuth App Exposure",
        "finding_desc": "Granting tokens to third-party tools (quizzes, analytics, games) creates supply chain exposure if those vendors suffer a breach.",
        "severity": "HIGH",
        "recommendation_title": "Audit and Prune Connected OAuth Apps",
        "recommendation_text": "Navigate to Settings > Apps & Websites and revoke access for any applications you do not use on a daily basis.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_H2",
        "category_code": "CAT_H",
        "category_name": "Third-Party Applications",
        "question": "How often do you review and revoke permissions for connected third-party applications?",
        "help_text": "Applying the Principle of Least Privilege requires removing integrations as soon as they are no longer actively required.",
        "options": [
            {"label": "Never / I didn't know I could do that", "value": "NO", "risk_points": 90},
            {"label": "Once every couple of years", "value": "SOMETIMES", "risk_points": 45},
            {"label": "Regularly (at least every 6 months)", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "SOMETIMES"],
        "finding_title": "Lack of Periodic Third-Party App Audits",
        "finding_desc": "Dormant integrations retain granted permissions indefinitely, violating the Principle of Least Privilege.",
        "severity": "MEDIUM",
        "recommendation_title": "Establish Biannual App Revocation Reviews",
        "recommendation_text": "Set a recurring calendar reminder every 6 months to review and disconnect third-party integrations.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_H3",
        "category_code": "CAT_H",
        "category_name": "Third-Party Applications",
        "question": "Do you check what specific permissions (e.g., read DMs, post on your behalf, access friends list) an app requests before authorizing?",
        "help_text": "Many malicious apps disguise themselves as fun quizzes while requesting excessive scopes.",
        "options": [
            {"label": "No, I usually click 'Accept' immediately", "value": "NO", "risk_points": 90},
            {"label": "Sometimes glance at the screen", "value": "SOMETIMES", "risk_points": 45},
            {"label": "Yes, I inspect permissions and decline overreaching scopes", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "SOMETIMES"],
        "finding_title": "Unvetted OAuth Permission Grants",
        "finding_desc": "Authorizing application permissions without scrutiny can grant read access to private messages, contacts, or photos.",
        "severity": "HIGH",
        "recommendation_title": "Scrutinize OAuth Scopes Before Authorizing",
        "recommendation_text": "Deny apps that request write permissions, message reading, or access to your friends list.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_H4",
        "category_code": "CAT_H",
        "category_name": "Third-Party Applications",
        "question": "Have you ever participated in viral social media quizzes (e.g., 'What celebrity do you look like?' or 'What does your name mean?')?",
        "help_text": "Viral quizzes are notorious front-ends used to harvest psychological profiles and personal behavioral data.",
        "options": [
            {"label": "Yes, I have completed viral quizzes on social platforms", "value": "YES", "risk_points": 80},
            {"label": "No, I strictly avoid viral interactive quizzes", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Participation in Data-Harvesting Quizzes",
        "finding_desc": "Interactive social quizzes frequently harvest profile details, connection graphs, and personal metadata.",
        "severity": "MEDIUM",
        "recommendation_title": "Revoke Legacy Quiz Permissions",
        "recommendation_text": "Check your connected apps list and immediately delete all quiz, game, or astrology integrations.",
        "priority": "GOOD PRACTICE"
    },

    # =========================================================================
    # CATEGORY I: Messaging & Social Engineering (5 Questions)
    # =========================================================================
    {
        "id": "Q_I1",
        "category_code": "CAT_I",
        "category_name": "Messaging & Social Engineering",
        "question": "Can anyone send you direct messages (DMs), or are messages restricted to approved connections?",
        "help_text": "Open message requests allow attackers to initiate phishing, fake prize lures, and malicious file drops directly into your inbox.",
        "options": [
            {"label": "Anyone can message me directly", "value": "YES", "risk_points": 90},
            {"label": "Filtered into a message requests folder", "value": "SOMETIMES", "risk_points": 45},
            {"label": "Strictly restricted to people I follow/friends", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Unrestricted Direct Messaging Channel",
        "finding_desc": "Leaving DMs open to anyone invites targeted social engineering, harassment, and phishing attempts.",
        "severity": "HIGH",
        "recommendation_title": "Restrict Direct Message Reception",
        "recommendation_text": "Adjust message controls so only followed accounts or friends can message you directly.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_I2",
        "category_code": "CAT_I",
        "category_name": "Messaging & Social Engineering",
        "question": "Have you ever clicked on unexpected links sent via direct message from friends or strangers (e.g., 'Is this video you?')?",
        "help_text": "'Is this video of you?' is the classic social engineering lure used to hijack accounts via credential harvesting landing pages.",
        "options": [
            {"label": "Yes, I have clicked such links in the past", "value": "YES", "risk_points": 100},
            {"label": "Only if it appeared to come from a close contact", "value": "SOMETIMES", "risk_points": 65},
            {"label": "No, I never click unexpected links in messages", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Susceptibility to DM Phishing Lures",
        "finding_desc": "Clicking unexpected links in private messages exposes credentials and authentication cookies to harvesting pages.",
        "severity": "CRITICAL",
        "recommendation_title": "Verify Links Out-of-Band Before Clicking",
        "recommendation_text": "Never click sensationalized links in messages. Contact the sender on an alternative channel to verify their identity.",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_I3",
        "category_code": "CAT_I",
        "category_name": "Messaging & Social Engineering",
        "question": "Would you ever share a 6-digit verification code or SMS OTP with someone messaging you asking for help recovering their account?",
        "help_text": "Attackers initiate password resets or register WhatsApp on their own device, then trick victims into forwarding the code.",
        "options": [
            {"label": "I have done this or might if it's a friend in need", "value": "YES", "risk_points": 100},
            {"label": "Unsure / Depends on the context", "value": "NOT_SURE", "risk_points": 75},
            {"label": "Never. Verification codes are strictly confidential", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "NOT_SURE"],
        "finding_title": "Vulnerability to Verification Code Forwarding Scams",
        "finding_desc": "Willingness to forward one-time passcodes allows attackers to finalize account takeovers or SIM swaps.",
        "severity": "CRITICAL",
        "recommendation_title": "Never Forward Verification Passcodes",
        "recommendation_text": "Security codes are for your eyes only. Legitimate platforms and genuine friends will never ask you to forward an OTP.",
        "priority": "IMMEDIATE"
    },
    {
        "id": "Q_I4",
        "category_code": "CAT_I",
        "category_name": "Messaging & Social Engineering",
        "question": "Do you interact with unsolicited giveaway promotions, crypto offers, or brand ambassador messages?",
        "help_text": "Brand ambassador and crypto DM campaigns are mass-market financial fraud schemes targeting social media users.",
        "options": [
            {"label": "Yes, I occasionally reply or look into them", "value": "YES", "risk_points": 90},
            {"label": "Rarely", "value": "SOMETIMES", "risk_points": 40},
            {"label": "No, I immediately report and block them as spam", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES"],
        "finding_title": "Interaction with Fraudulent Giveaways / Ambassador Lures",
        "finding_desc": "Engaging with unsolicited commercial or giveaway messages marks your account as an active target for secondary fraud.",
        "severity": "HIGH",
        "recommendation_title": "Block and Report Unsolicited Promotional DMs",
        "recommendation_text": "Block unsolicited offers and brand ambassador pitches immediately without responding.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_I5",
        "category_code": "CAT_I",
        "category_name": "Messaging & Social Engineering",
        "question": "If a friend's profile sends you an urgent message requesting emergency funds or gift cards, what is your reaction?",
        "help_text": "Impersonated and compromised accounts regularly plead for urgent financial assistance through gift cards or crypto transfers.",
        "options": [
            {"label": "I would consider helping or ask how to transfer money", "value": "YES", "risk_points": 100},
            {"label": "I would be suspicious but might converse with them", "value": "SOMETIMES", "risk_points": 50},
            {"label": "I would call them immediately on their real phone number to verify", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Susceptibility to Friend Impersonation Emergency Scams",
        "finding_desc": "Responding to emergency financial pleas in DMs without telephone verification risks falling victim to account takeover scams.",
        "severity": "HIGH",
        "recommendation_title": "Mandate Out-of-Band Voice Confirmation for Financial Requests",
        "recommendation_text": "Always call the friend over phone or in-person before taking any action when urgent money is requested.",
        "priority": "IMPORTANT"
    },

    # =========================================================================
    # CATEGORY J: Digital Footprint (4 Questions)
    # =========================================================================
    {
        "id": "Q_J1",
        "category_code": "CAT_J",
        "category_name": "Digital Footprint",
        "question": "Do you regularly audit or delete old social media posts, comments, and photos from years ago?",
        "help_text": "Historical posts from high school or past years may contain outdated views, old locations, or abandoned email addresses.",
        "options": [
            {"label": "No, my entire posting history remains permanently visible", "value": "NO", "risk_points": 85},
            {"label": "Occasionally / Rarely", "value": "SOMETIMES", "risk_points": 45},
            {"label": "Yes, I regularly purge or archive posts older than 12 months", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "SOMETIMES"],
        "finding_title": "Unmanaged Historical Digital Footprint",
        "finding_desc": "Leaving years of historical posts online provides a deep timeline for OSINT profiling, doxxing, and contextual scraping.",
        "severity": "MEDIUM",
        "recommendation_title": "Audit and Archive Historical Timeline Posts",
        "recommendation_text": "Use platform archive tools to hide or delete posts, comments, and photos older than 1-2 years.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_J2",
        "category_code": "CAT_J",
        "category_name": "Digital Footprint",
        "question": "Do you have abandoned or unused social media accounts that you haven't logged into for years?",
        "help_text": "Unmonitored zombie accounts are prime targets for silent takeover, password spraying, and impersonation.",
        "options": [
            {"label": "Yes, multiple old accounts (Tumblr, Ask.fm, old Twitter, MySpace)", "value": "YES", "risk_points": 90},
            {"label": "Maybe 1 or 2 old accounts", "value": "SOMETIMES", "risk_points": 50},
            {"label": "No, I permanently delete accounts when I stop using them", "value": "NO", "risk_points": 0}
        ],
        "risk_trigger": ["YES", "SOMETIMES"],
        "finding_title": "Abandoned Zombie Accounts",
        "finding_desc": "Dormant accounts with unmaintained passwords remain vulnerable to silent takeover and brand impersonation.",
        "severity": "HIGH",
        "recommendation_title": "Locate and Permanently Delete Dormant Accounts",
        "recommendation_text": "Search your password manager and email history for old platform accounts and execute permanent deletion requests.",
        "priority": "IMPORTANT"
    },
    {
        "id": "Q_J3",
        "category_code": "CAT_J",
        "category_name": "Digital Footprint",
        "question": "Have you ever searched your own name or username on Google or DuckDuckGo to inspect your public footprint?",
        "help_text": "Performing a defensive self-OSINT check reveals what prospective employers, stalkers, or scammers can find without effort.",
        "options": [
            {"label": "No, I have never self-searched", "value": "NO", "risk_points": 75},
            {"label": "Yes, I conduct periodic defensive self-searches", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO"],
        "finding_title": "Absence of Defensive Self-OSINT Monitoring",
        "finding_desc": "Failing to conduct self-searches prevents you from discovering exposed data broker listings, pasted records, or cached posts.",
        "severity": "LOW",
        "recommendation_title": "Conduct Quarterly Defensive Self-Searches",
        "recommendation_text": "Search your full name and common usernames in incognito mode quarterly to monitor your public search presence.",
        "priority": "GOOD PRACTICE"
    },
    {
        "id": "Q_J4",
        "category_code": "CAT_J",
        "category_name": "Digital Footprint",
        "question": "How often do you complete a formal privacy checkup on your active social media accounts?",
        "help_text": "Platforms frequently update privacy options, terms, and default settings after major feature rollouts.",
        "options": [
            {"label": "Never / Only when creating the account", "value": "NO", "risk_points": 85},
            {"label": "Every couple of years", "value": "SOMETIMES", "risk_points": 45},
            {"label": "Regularly (at least every 6 months)", "value": "YES", "risk_points": 0}
        ],
        "risk_trigger": ["NO", "SOMETIMES"],
        "finding_title": "Irregular Privacy Settings Maintenance",
        "finding_desc": "Platform privacy policies and default settings evolve continuously; neglecting checkups leaves new exposure toggles active.",
        "severity": "MEDIUM",
        "recommendation_title": "Run Built-In Platform Privacy Checkups",
        "recommendation_text": "Execute the built-in 'Privacy Checkup' wizard on your platforms every 6 months to review newly added toggles.",
        "priority": "GOOD PRACTICE"
    }
]

# Quick lookup dictionary by Question ID
QUESTION_MAP = {q["id"]: q for q in QUESTIONS}
