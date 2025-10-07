# Lab02 — Incident Handler Journal

## Why this lab matters
This journal is the backbone of my incident response practice. It turns every lab and project into evidence: what happened, how I analyzed it, which controls I applied, and what I learned. Hiring managers can see how I think, not just what tools I used.

## What this is
A living log I updated after each exercise using a consistent structure:
- **Date and entry ID**
- **Short description**
- **Tool(s) used**
- **The 5 W’s** (Who, What, Where, When, Why)
- **Phase** of the NIST incident lifecycle
- **Notes** with actions and follow-ups

> Artifact: [`Incident handler’s journal.pdf`](./Incident%20handler%27s%20journal.pdf)

---

## Highlights from my entries

### 1) Ransomware in healthcare — detection and first analysis
- **Focus:** Phishing-led ransomware that encrypted critical data in a healthcare environment  
- **Phase:** Detection & Analysis  
- **Actions:** Captured indicators, scoped impact, and documented immediate hardening ideas for email and endpoints  
- **Outcome:** Clear next steps for awareness training and layered email/endpoint defenses

### 2) Phishing alert with malware — tool-assisted validation
- **Focus:** Suspicious attachment delivered via phishing  
- **Tool:** VirusTotal to analyze the file and enrich indicators  
- **Phase:** Detection & Analysis  
- **Outcome:** Confirmed malicious file, refined user training, and raised the bar on mail filtering

### 3) Confirmed compromise — escalation and containment planning
- **Focus:** User executed a malicious download; workstation showed unauthorized installs  
- **Phase:** Detection & Analysis → handoff to Level-2 for **Containment** planning  
- **Outcome:** Documented escalation, reinforced phishing controls, and captured gaps for response playbooks

### 4) Forced browsing + data exfiltration in retail — integrity and confidentiality hit
- **Focus:** Unauthorized URL enumeration exposed customer orders and transactions  
- **Phase:** Detection & Analysis **and** Containment/Eradication/Recovery  
- **Actions:** Recommend allowlisting, stronger authZ around sensitive paths, and routine web app testing  
- **Outcome:** Concrete web app control improvements and monitoring cues for future detections

---

## Timeline snapshot

| Date       | Entry | Incident Type                              | Phase                           | Key Tool(s)  | Outcomes |
|------------|------:|--------------------------------------------|---------------------------------|--------------|----------|
| 2025-06-11 | 1     | Phishing → **Ransomware** in healthcare    | Detection & Analysis             | —            | User training, email and endpoint hardening |
| 2025-06-15 | 2     | **Phishing** with malicious attachment     | Detection & Analysis             | VirusTotal   | IOC validation, improved filtering and awareness |
| 2025-06-16 | 3     | **Phishing** → unauthorized software       | Detection & Analysis → Escalate | —            | Level-2 containment plan, reinforce controls |
| 2025-06-17 | 4     | **Forced browsing** → data exfiltration    | Detection & Analysis; C/E/R      | —            | URL allowlisting, stronger authZ, periodic testing |

*C/E/R = Containment, Eradication, and Recovery.*

---

## How I use this journal
- **IR discipline:** Enforce a repeatable structure so nothing is missed under pressure.  
- **Control evidence:** Each entry links to specific controls and follow-ups.  
- **Detection tuning:** Indicators and root causes feed SIEM/IDS rules and playbooks.  
- **Growth loop:** Reflections convert mistakes into checklists and training content.

## Reflections
- Interpreting subtle phishing indicators and correlating logs was hardest early on. Repetition built speed and accuracy.  
- Incident response is a lifecycle. Preparation, detection, containment, and recovery are connected.  
- Lightweight intel tools like VirusTotal accelerate triage and keep analysis grounded.

## Reuse
- Use this journal format for on-call rotations and table-tops.  
- Convert repeated fixes into **runbooks** and **detections**.  
- Bring selected entries to interviews to demonstrate method, not just results.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
