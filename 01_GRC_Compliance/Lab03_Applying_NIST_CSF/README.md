# Lab03 — Applying the NIST CSF

## Scenario
In this lab I applied the NIST Cybersecurity Framework (CSF) to two real-world style incidents at a small retail company:  
1) a **credential-phishing data breach** that exposed and manipulated customer records, and  
2) a **DDoS (ICMP flood)** that took internal services offline.  
I used the CSF’s five functions—Identify, Protect, Detect, Respond, Recover—to analyze causes, select controls, and document playbooks the team can run next time.

## Objectives
- Map people, processes, technology, and data to CSF functions  
- Perform incident analysis for two cases and document control gaps  
- Propose high-impact mitigations and operating procedures  
- Produce short playbooks for response and recovery

## Files in this folder
- [`Applying the NIST CSF .pdf`](./Applying%20the%20NIST%20CSF%20.pdf) — framework guide and prompts  
- [`Completed Example of an Incident report analysis.pdf`](./Completed%20Example%20of%20an%20Incident%20report%20analysis.pdf) — credential-phishing incident write-up  
- [`Incident report analysis.pdf`](./Incident%20report%20analysis.pdf) — DDoS (ICMP flood) incident write-up

---

## What I did

### 1) Framed work with the NIST CSF
I structured all analysis and deliverables around the five CSF functions: **Identify**, **Protect**, **Detect**, **Respond**, and **Recover**. For each function I used the guide’s question prompts to drive evidence collection, gaps, and actions.

### 2) Incident A — Credential phishing → data exposure and tampering
**Summary:** An intern was phished and entered credentials into a fake site. The attacker used the account to access the customer database, exposing records and altering/deleting some entries.

**Identify**
- Mapped affected assets: intern account, IAM policy, customer DB, access logs  
- Confirmed compromise path and data integrity impact

**Protect**
- Enforced **MFA** on all user accounts  
- Limited login attempts to **three tries**  
- Launched awareness training on phishing and credential safety  
- Hardened the perimeter: updated firewall rules and added **IPS**

**Detect**
- Turned on firewall logging and added **IDS** coverage for unauthorized access attempts  
- Tuned monitoring to alert on anomalous DB reads/edits from user roles like “intern”

**Respond**
- Disabled the compromised account immediately  
- Notified leadership and customers; prepared notifications to regulators/law enforcement as required  
- Delivered targeted training to interns and staff

**Recover**
- Restored the customer DB from the **last full backup**  
- Instructed staff to re-enter changes made after the backup window

**Outputs**
- Updated access policy and training module  
- Firewall/IPS change ticket and evidence  
- Post-incident report with timeline, root cause, and corrective actions

### 3) Incident B — DDoS (ICMP flood) → service outage
**Summary:** Multiple sources sent high-volume ICMP packets that overwhelmed the network. Internal services were unusable for ~2 hours.

**Identify**
- Found a firewall configuration gap that allowed excessive inbound ICMP  
- Confirmed multi-source flooding pattern

**Protect**
- Added firewall **rate-limits** for ICMP  
- Enabled **source IP verification** to drop spoofed packets  
- Implemented continuous network monitoring  
- Deployed **IDS/IPS** with ICMP flood signatures

**Detect**
- Alerting via firewall logs, IDS/IPS, and traffic-pattern monitoring

**Respond**
- Blocked offending traffic at the edge  
- Took non-critical services offline to preserve core functions  
- Used IDS/IPS alerts to guide containment steps

**Recover**
- Brought services back online in a controlled sequence  
- Performed stability checks and a **lessons-learned** review

**Outputs**
- Network hardening changes and validation screenshots  
- DDoS response checklist and comms template  
- Monitoring thresholds and alert runbook

---

## Controls Implemented (roll-up)
- **Identity & Access:** MFA, login-attempt throttling, role reviews  
- **Perimeter & Network:** Updated firewall policy, ICMP rate-limit, source validation, WAF/IPS where applicable  
- **Monitoring & Detection:** Firewall logging, IDS/IPS rules, anomaly alerts for DB access  
- **Awareness & Training:** Phishing defense module for interns and employees  
- **Backup & Recovery:** Verified full backup restore for DB, service restart plan after outages

## Playbooks Produced
- **Phishing / Account Compromise:** isolate account → contain DB access → notify → restore → rotate secrets → train  
- **DDoS / ICMP Flood:** identify pattern → rate-limit/block → scale protections → comms to stakeholders → staged recovery → retrospective

## Lessons Learned
- Small configuration gaps create large blast radius. Guardrails like MFA, throttling, and least privilege shrink it.  
- Monitoring needs explicit signals for *integrity* events, not just availability.  
- Recovery plans must include **restore+re-entry** steps for data lost after the last backup.

## How this maps to the job
- **SOC Analyst:** write detections for anomalous DB edits by low-privilege roles; ICMP flood thresholds; failed-login + phishing correlation  
- **GRC Analyst:** map implemented controls to CSF categories; maintain evidence; schedule tabletop exercises and restore drills

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
