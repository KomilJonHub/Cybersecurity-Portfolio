# Lab03 — Applying the NIST CSF

[Portfolio](../../README.md) / [GRC & Compliance](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I completed a Google Cybersecurity course incident-analysis exercise using the NIST Cybersecurity Framework. I used the supplied guide and phishing example to organize my own written analysis of a **simulated ICMP-flood denial-of-service incident**. The work connects a configuration gap, business disruption, protective controls, response, and recovery.

The course material uses the original **five-function CSF structure**: Identify, Protect, Detect, Respond, and Recover. This exercise follows that pre-CSF 2.0 structure.

## Objectives

- Structure incident analysis around the framework's functions
- Connect affected services and configuration gaps with business impact
- Explain protective and detective controls in the scenario
- Organize response and recovery actions into a usable written plan

## Files and Attribution

| File | Role in the exercise |
|---|---|
| [Applying the NIST CSF](./Applying%20the%20NIST%20CSF%20.pdf) | Supplied framework guide and analysis prompts |
| [Completed Example of an Incident report analysis](./Completed%20Example%20of%20an%20Incident%20report%20analysis.pdf) | Supplied model answer about credential phishing, used as a reference |
| [Incident report analysis](./Incident%20report%20analysis.pdf) | My completed ICMP-flood analysis and reflections, using the course template |

I completed the written analysis in the course template. The tables and sections below distinguish supplied scenario actions, my analysis, and recommendations.

## How I Applied the Framework

### 1. Use the Guide to Ask Specific Questions

I used each function to move from the incident description to a structured assessment: what was affected, which safeguards were missing, what signals would help detection, how the team should respond, and how normal service could be restored.

### 2. Learn from the Supplied Credential-Phishing Example

The model answer describes an intern entering credentials on a fake website. Access logs suggest an attacker used the account to access customer records, and employees report missing or altered records.

| Function | What the supplied example describes |
|---|---|
| **Identify** | Review affected systems, access policies, compromised credentials, and possible data deletion |
| **Protect** | The fictional team has added MFA and a three-attempt login limit; a protective firewall configuration and IPS investment are future actions |
| **Detect** | Planned firewall logging and IDS monitoring |
| **Respond** | Account disabled, employee training, leadership informed, and planned customer/other required notifications |
| **Recover** | Planned restoration from the previous night's backup, followed by re-entry of newer customer changes |

This supplied example helped me separate confidentiality and integrity impacts from recovery needs. A specific login-attempt limit also needs context because an overly rigid lockout can disrupt legitimate users.

### 3. Complete My ICMP-Flood Incident Analysis

**Scenario facts:** The supplied case describes a large volume of ICMP traffic, an inadequately configured firewall, and internal services unavailable for about two hours. The response team blocks incoming ICMP, takes noncritical services offline, and restores essential services.

**Identify — connect cause and impact**

I explained how the firewall configuration allowed the flood to disrupt normal traffic. I connected that technical gap with service availability and the need to review the network's protective configuration.

**Protect — map safeguards to the gap**

My report describes the scenario team's ICMP rate limiting, source-address verification, monitoring, and IDS/IPS measures. I used these controls to explain how to reduce the chance and impact of a similar event.

**Detect — define useful signals**

I connected firewall events, IDS/IPS alerts, and unusual traffic patterns with earlier recognition of a flood. Detection needs thresholds and a person or team responsible for acting on the signal.

**Respond — organize future actions**

I described blocking or filtering attack traffic, using detection alerts to guide containment, and training staff on the response process. Filtering requires care: source addresses can be spoofed, and local controls alone may not prevent an upstream link from saturating.

**Recover — restore service carefully**

I outlined a controlled restart of network services, stability checks, review for remaining vulnerabilities, and sharing lessons learned. These steps form the recovery section of my written analysis.

## Response and Recovery Outline

I condensed the framework analysis into these documentation sequences:

- **Credential phishing, based on the model case:** review account activity → contain compromised access → coordinate notifications → restore affected data → reconcile changes after the backup → improve authentication and awareness.
- **ICMP flood, based on my analysis:** recognize abnormal traffic → filter or rate-limit within the response plan → protect essential services → communicate impact → restore in stages → review configuration and monitoring.

These outlines summarize the response and recovery reasoning in the written work.

## Lessons Learned

- Framework functions help keep a technical incident connected to people, services, and business impact.
- Proposed safeguards, scenario actions, and actions I actually performed must be distinguished in a report.
- Restoring a backup is only one part of recovery; newer changes and communications also need attention.
- A configuration change should be followed by a defined validation step and a review of the remaining risks.

## Practical Value

This completed analysis demonstrates structured technical writing, control selection, risk reasoning, and response planning. These skills support troubleshooting and service continuity work as well as junior GRC, risk, and security-analysis responsibilities.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
