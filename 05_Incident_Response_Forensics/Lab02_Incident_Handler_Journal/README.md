# Lab02 — Incident Handler Journal

[Portfolio](../../README.md) / [Incident Response & Forensics](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [What I Did](#what-i-did) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I completed this incident-handler journal as part of my cybersecurity coursework. It records analysis of supplied ransomware, phishing, and web-application scenarios, with the 5 W’s, response phases, and recommendations. The healthcare, financial-services, and retail organizations belong to those scenarios.

## Objectives

- Organize incident facts and distinguish them from recommendations
- Document the response phase, investigation reasoning, and next steps
- Use a consistent format that another reader can follow

## What I Did

A living log I updated after each exercise using a consistent structure:
- **Date and entry ID**
- **Short description**
- **Tool(s) used**
- **The 5 W’s** (Who, What, Where, When, Why)
- **Phase** of the NIST incident lifecycle
- **Notes** with actions and follow-ups

> Evidence: [`Incident handler’s journal.pdf`](./Incident%20handler%27s%20journal.pdf)

---

## Analysis & Results

### 1) Ransomware in healthcare — detection and first analysis
- **Focus:** Phishing-led ransomware that encrypted critical data in a healthcare environment  
- **Phase:** Detection & Analysis  
- **Actions:** Captured indicators, scoped impact, and documented immediate hardening ideas for email and endpoints  
- **Outcome:** Written recommendations for awareness training and layered email/endpoint defenses

### 2) Phishing alert with malware — tool-assisted validation
- **Focus:** Suspicious attachment delivered via phishing  
- **Tool:** VirusTotal to analyze the file and enrich indicators  
- **Phase:** Detection & Analysis  
- **Outcome:** Documented the malicious-file finding and recommended improvements to training and mail filtering

### 3) Confirmed compromise — escalation and containment planning
- **Focus:** User executed a malicious download; workstation showed unauthorized installs  
- **Phase:** Detection & Analysis → handoff to Level-2 for **Containment** planning  
- **Outcome:** Documented escalation, reinforced phishing controls, and captured gaps for response playbooks

### 4) Forced browsing + data exfiltration in retail — integrity and confidentiality hit
- **Focus:** Unauthorized URL enumeration exposed customer orders and transactions  
- **Phase:** Detection & Analysis **and** Containment/Eradication/Recovery  
- **Actions:** Recommend allowlisting, stronger authZ around sensitive paths, and routine web app testing  
- **Outcome:** Recommendations for web-app authorization checks and monitoring cues

---

## Journal Timeline

These are journal-entry dates. The underlying scenario events may have different dates, including the retail case from December 2022. The table summarizes recommendations and documented response steps.

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
- **Control evidence:** Entries connect incident facts with recommended controls and follow-ups.
- **Detection tuning:** Recorded indicators and causes can inform future SIEM/IDS rules and response procedures.
- **Growth loop:** Reflections convert mistakes into checklists and training content.

## Lessons Learned
- Interpreting subtle phishing indicators and correlating logs was hardest early on. Repetition built speed and accuracy.  
- Incident response is a lifecycle. Preparation, detection, containment, and recovery are connected.  
- Lightweight intel tools like VirusTotal accelerate triage and keep analysis grounded.

## Practical Value
- Use this journal format for on-call rotations and table-tops.  
- Convert repeated fixes into **runbooks** and **detections**.  
- Bring selected entries to interviews to demonstrate method, not just results.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
