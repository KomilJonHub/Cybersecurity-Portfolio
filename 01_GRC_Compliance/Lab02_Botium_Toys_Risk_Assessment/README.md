# Lab02 — Botium Toys Risk Assessment (GRC & Compliance)

[Portfolio](../../README.md) / [GRC & Compliance](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Lessons and Practical Value](#lessons-and-practical-value)

## Overview

I completed this Google Cybersecurity course assessment for **Botium Toys**, a fictional retailer. I reviewed the supplied asset inventory and risk assessment, completed the controls and compliance checklist, and wrote recommendations for the IT manager. My work connects access, data protection, detection, and recovery gaps to business risk.

The scenario supplies the business facts and an **8/10 risk score**. I used those inputs to assess control coverage and prioritize improvements; the score is not a risk model I independently calculated.

## Objectives

- Review the scope and assets of the retailer's security program
- Evaluate administrative, technical, and physical controls
- Compare the scenario with PCI DSS, GDPR, and SOC reporting criteria covered in the course
- Explain control gaps and recommend a practical sequence of improvements

## Artifacts and Attribution

| File | Role in the exercise |
|---|---|
| [Botium Toys: Scope, goals, and risk assessment report](./Botium%20Toys_%20Scope,%20goals,%20and%20risk%20assessment%20report.pdf) | Supplied course scenario, inventory, control facts, and risk score |
| [Control categories](./Control%20categories.pdf) | Supplied reference explaining control categories and purposes |
| [Controls and compliance checklist](./Controls%20and%20compliance%20checklist.pdf) | My completed assessment and written recommendations, using the course template |
| [Cybersecurity incident report](./Cybersecurity%20incident%20report.pdf) | My separate course analysis of a supplied TCP/HTTP denial-of-service scenario; not an observed Botium Toys incident |

The original documents remain unchanged. The checklist records that a password policy exists; the source explains why that policy is weak. Legacy-system monitoring exists but has no regular schedule or clear intervention process, which explains the qualified coverage in my assessment.

## Scope and Method

The supplied scope covers the entire security program: employee devices, internal networking, business systems and services, data storage, storefront and warehouse assets, and legacy systems.

1. I reviewed the inventory and existing controls in the supplied report.
2. I compared that evidence with the checklist's control and compliance questions.
3. I distinguished controls that were present from those that were absent or inadequate.
4. I wrote recommendations covering sensitive-data access, backups, passwords, intrusion alerts, encryption, classification, and user roles.

## Key Findings from the Scenario

- All employees have access to internally stored data and may be able to access cardholder data and PII/SPII.
- The report says credit card information is not encrypted across its local processing, transmission, and storage touchpoints; it does not describe a measured TLS configuration.
- Least privilege and separation of duties are missing.
- There is no IDS, no backup of critical data, and no disaster recovery plan.
- Password requirements are weak, and there is no centralized password manager.
- Legacy maintenance lacks a regular schedule and clear procedures.
- Existing protections include a firewall, monitored antivirus, locks, CCTV, and fire protection. The report also describes availability and integrity controls and established privacy/notification procedures.

The supplied **high risk rating of 8/10** is consistent with the combination of broad data access, missing encryption, and recovery gaps. Antivirus is documented; an EDR deployment is not.

## Control Mapping

| Category | Improvements I recommended or developed from the assessment |
|---|---|
| **Administrative** | Least-privilege access policy, separation of duties, clear user roles, account lifecycle responsibilities, data classification, and a disaster recovery plan |
| **Technical** | Encryption, password management, intrusion alerts, backups and restore tests; MFA as an additional access safeguard |
| **Physical** | Maintain and review the existing locks, CCTV, and fire protection alongside the digital controls |

## Compliance Snapshot

- **PCI DSS:** The scenario shows excessive access to cardholder information, insecure data handling, missing encryption, and weak password management.
- **GDPR:** Privacy and notification procedures are described as present, while confidentiality and data classification still need work. The course checklist's 72-hour notification wording is scenario material, not a complete legal compliance determination.
- **SOC reporting criteria:** Access policy and confidentiality need improvement. The supplied report describes integrity and availability controls as present; I retained that distinction rather than marking every area as deficient.

## Recommended Priorities

The following is my suggested **30–60 day planning sequence**, not an implementation record or a promised delivery schedule:

1. Restrict sensitive-data access using appropriate roles and least privilege; define who can view and change each data set.
2. Improve password policy and management, and evaluate MFA for account protection.
3. Establish critical-data backups, test restores, and document recovery responsibilities.
4. Encrypt cardholder information and assess separation of card-processing systems from other workloads.
5. Add intrusion detection and define who reviews alerts and follows up.
6. Classify data, assign owners, and establish a regular legacy-system maintenance process.

A WAF or CDN may help protect a web application, but it does not replace network detection or a backup and recovery process.

## Separate Incident Analysis: TCP Denial of Service

In the attached incident report, I analyzed a supplied TCP/HTTP scenario involving repeated SYN requests and website disruption. I explained the handshake and connected the traffic pattern with denial of service. This was a completed analysis exercise, separate from the Botium Toys controls assessment.

A SYN flood can exhaust connection resources and prevent legitimate access; it does not necessarily shut down the operating system. Repeated SYNs alone also require context before attributing malicious intent. Possible responses include SYN cookies, connection or rate limits, upstream filtering, and detection tuned to the observed traffic. Those are response options, not controls I deployed in this assessment.

## Lessons and Practical Value

- An inventory is the basis for decisions about identities, data, and recovery priorities.
- A control can exist and still be inadequate: password policy and irregular legacy maintenance are useful examples.
- Access restrictions, encryption, detection, and tested recovery address different risks and need to work together.
- Clear attribution makes an assessment useful: supplied facts, my conclusions, and recommended actions should be easy to distinguish.

This work demonstrates control review, written risk analysis, and practical recommendations relevant to IT support, access administration, and junior risk or GRC work.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
