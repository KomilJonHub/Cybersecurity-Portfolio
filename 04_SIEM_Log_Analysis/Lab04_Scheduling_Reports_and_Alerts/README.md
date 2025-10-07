# Lab: Splunk — Scheduling Reports & Alerts (Failed Root Logins)

## Scenario
I acted as a SOC analyst at **Buttercup Games** during a high-traffic promotion. My job was to keep a tight watch on Linux bastion hosts for risky authentication patterns while giving leadership a clean, repeatable snapshot of failed root logins they could rely on during morning standups. I built a baseline search, saved it as a report, scheduled it to email the admin team daily at 06:00, and then created a **real-time alert** for specific failed-password activity with throttling to avoid noise. I documented performance and outcomes so another analyst could take over mid-shift without losing context.

---

## Objectives
- Detect and report on **failed root logins** in the last 24 hours.
- Operationalize the search as a **scheduled report** with email delivery.
- Build a **real-time alert** for targeted failed logins with sensible throttling.
- Verify alert firings and preserve evidence as a saved report for handoff.

---

## Environment & Data
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
Schedule: **Run every day at 06:00**, **Time Range = Last 24 hours**, with **Send email → admin@buttercupgames.com**.

Screens:
- Open schedule editor  
  ![Edit schedule](./screenshots/Screenshot%202025-09-26%20142935.png)
- Next scheduled time confirmed  
  ![Next scheduled time](./screenshots/Screenshot%202025-09-26%20143134.png)

**Takeaway:** A scheduled report with email delivery eliminates “did anyone run the search?” during morning briefings.

---

### 4) Hunt noisy patterns and refine: failed password NOT invalid
To separate real failures from “invalid user” noise, I tightened the query:
```spl
index=security sourcetype=linux_secure failed password NOT invalid
```
![Tuned search for alert logic](./screenshots/Screenshot%202025-09-26%20142650.png)

**Why this matters:** Targets legitimate user accounts failing authentication and avoids predictable bot noise.

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
![Save as Alert](./screenshots/Screenshot%202025-09-26%20142747.png)
![Alert form](./screenshots/Screenshot%202025-09-26%20143209.png)

**Takeaway:** Throttling by `host` avoids alert storms from the same machine while still catching multi-host spray.

---

### 6) Validate firings and preserve evidence
- Alert overview with history:  
  ![Alert overview](./screenshots/Screenshot%202025-09-26%20143338.png)
- Triggered Alerts view:  
  ![Triggered Alerts list](./screenshots/Screenshot%202025-09-26%20143618.png)

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

## Takeaways
- Scheduled reports create dependable cadence for leadership without manual effort.
- Real-time alerts must include **noise controls** (scope, keywords, throttling) to stay actionable.
- Keeping **L1S1** and **L1S2** as named artifacts makes shift handoffs faster and cleaner.

---

## MITRE ATT&CK Mapping
- **T1110 – Brute Force:** Repeated failed authentication attempts against Linux bastions.  
- **T1078 – Valid Accounts (monitoring):** Follow-on detections often pair with successful logins from unusual sources.

---

## Artifacts
- Lab guide PDF: [`The lab content`](./artifacts/Splunk%20lab3%20-%20Copy.pdf)

---

## Personal Reflection
This lab was about discipline. A clean search is good; an automated, scheduled report that lands in an inbox before the standup is better. Adding a real-time alert with sane throttling turned the same logic into something the on-call can trust at 2 a.m. That’s the difference between “I ran a search” and “our process catches this every time.”

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
