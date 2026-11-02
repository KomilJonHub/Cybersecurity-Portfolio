# Lab: Splunk — Scheduling Reports & Alerts (Failed Root Logins)

[Portfolio](../../README.md) / [SIEM & Log Analysis](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Lessons Learned](#lessons-learned) · [Evidence & Results](#evidence--results)

## Overview
I completed this Splunk Education exercise using the fictional **Buttercup Games** authentication dataset. I saved a failed-root-login report, configured a daily 06:00 schedule and email action, then created a real-time alert for failed-password events excluding invalid usernames. I checked its trigger history and saved results for follow-up.

---

## Objectives
- Detect and report on **failed root logins** in the last 24 hours.
- Operationalize the search as a **scheduled report** with email delivery.
- Build a **real-time alert** for targeted failed logins with sensible throttling.
- Verify alert firings and preserve evidence as a saved report for handoff.

---

## Environment & Tools
- **Platform:** Splunk Enterprise 9.x (Search & Reporting)
- **Indexes / sourcetypes:**  
  - `index=security` `sourcetype=linux_secure` (Linux auth)  
  - (Other lab data available: `index=web` `sourcetype=access_combined`)
- **Role:** poweruser
- **Time ranges used:** Last 24 hours, Last 60 minutes, Real-time

---

## What I Did

### 1) Baseline search: failed root logins (Last 24 hours)
```spl
index=security sourcetype=linux_secure password fail* root
```
Result view and field discovery:
![Failed root logins — baseline](./screenshots/Screenshot%202025-09-26%20142146.png)

**Why this matters:** Focuses on high-risk attempts specifically targeting `root`. Uses prefix matching `fail*` to include “Failed”.

---

### 2) Save as report and keep it analyst-friendly
Saved as: **analyst_report_FailedRootLoginsLast24Hours**, then re-saved as **L1S1** for my handoff naming convention.
![Reports list](./screenshots/Screenshot%202025-09-26%20142528.png)

**Takeaway:** Stable names like `L1S1` make it easy for teammates to reference during shift change.

---

### 3) Schedule the report and notify stakeholders
Schedule: **Run every day at 06:00**, **Time Range = Last 24 hours**, with **Send email → `admin@buttercupgames.com`**, the address supplied by the lab. The screenshots verify the configured action and schedule, rather than inbox delivery.

Screens:
- Open schedule editor  
  ![Edit schedule](./screenshots/Screenshot%202025-09-26%20142650.png)
- Next scheduled time confirmed  
  ![Next scheduled time](./screenshots/Screenshot%202025-09-26%20142747.png)

**Takeaway:** A scheduled report with email delivery eliminates “did anyone run the search?” during morning briefings.

---

### 4) Hunt noisy patterns and refine: failed password NOT invalid
I changed the search to exclude messages containing `invalid`:
```spl
index=security sourcetype=linux_secure failed password NOT invalid
```
![Tuned search and Save As Alert menu](./screenshots/Screenshot%202025-09-26%20142935.png)

**Why this matters:** This search is broader than the root-only report and can include failures for several usernames. Excluding invalid-user messages changes coverage; it can also hide relevant username-guessing activity, so I would review that activity separately.

---

### 5) Turn the tuned search into a **real-time alert**
Save As → **Alert**
- **Title:** `Komiljon-Login attempts`  
- **Type:** Real-time  
- **Trigger:** Number of Results **> 0 in 1 minute**  
- **Mode:** **For each result**  
- **Throttle:** Suppress by field `host` for **60 seconds**  
- **Action:** Add to Triggered Alerts, **Severity: High**

Configuration flow:
![Alert configuration form including per-result mode and host throttling](./screenshots/Screenshot%202025-09-26%20143134.png)

**Takeaway:** Host-based suppression limits repeated notifications from one host. Its grouping and 60-second window also affect which events create separate alerts, so they need tuning to the intended monitoring coverage.

---

### 6) Validate firings and preserve evidence
- Alert overview with history:  
  ![Alert overview and trigger history](./screenshots/Screenshot%202025-09-26%20143209.png)
- Triggered Alerts view:  
  ![Triggered Alerts list](./screenshots/Screenshot%202025-09-26%20143338.png)

From a fired alert, I used **View results** to inspect the exact events and confirmed they matched intent.

---

### 7) Save alert results as a handoff report (L1S2)
From a fired alert → **Save As → Report → Title: L1S2**.  
Now both **L1S1** (daily) and **L1S2** (alert evidence) are discoverable under Reports for the next analyst.

---

## SPL Cheatsheet
```spl
# Baseline report (Last 24 hours)
index=security sourcetype=linux_secure password fail* root

# Alert logic: reduce noise from invalid users
index=security sourcetype=linux_secure failed password NOT invalid
```

---

## Lessons Learned
- Scheduled reports create dependable cadence for leadership without manual effort.
- Real-time alerts must include **noise controls** (scope, keywords, throttling) to stay actionable.
- Keeping **L1S1** and **L1S2** as named artifacts makes shift handoffs faster and cleaner.

---

## MITRE ATT&CK Mapping
- **T1110 — Brute Force:** repeated failed authentication events are relevant investigation leads. The lab verifies search and alert behavior, rather than proving malicious intent or successful account access.

---

## Evidence & Results
- Lab guide PDF: [`The lab content`](./artifacts/Splunk%20lab3%20-%20Copy.pdf)

---

## Personal Reflection
Saving a search, scheduling it, and checking an alert trigger taught me to validate each stage separately. I would also review delivery, monitoring coverage, resource use, and suppression behavior before relying on the configuration operationally.

![Saved alert and Edit menu](./screenshots/Screenshot%202025-09-26%20143618.png)

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
