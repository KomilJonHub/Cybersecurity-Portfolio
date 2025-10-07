# Lab02 — Botium Toys Risk Assessment (GRC & Compliance)

## Scenario
I stepped in as the security analyst for a fast-growing toy retailer with a small IT team and aging systems. The goal was to baseline risk, map controls to compliance, and give the business a short, prioritized plan to reduce risk fast.

## Objectives
- Define scope and critical assets
- Evaluate current controls across admin, technical, and physical families
- Map to PCI DSS, GDPR, and SOC Trust Services
- Score risk and deliver a 30–60 day remediation plan

## Artifacts (this folder)
- [`Botium Toys_ Scope, goals, and risk assessment report.pdf`](./Botium%20Toys_%20Scope,%20goals,%20and%20risk%20assessment%20report.pdf)
- [`Control categories.pdf`](./Control%20categories.pdf)
- [`Controls and compliance checklist.pdf`](./Controls%20and%20compliance%20checklist.pdf)
- [`Cybersecurity incident report.pdf`](./Cybersecurity%20incident%20report.pdf)

## Scope
People, process, tech, and facilities: employee devices, internal network, servers and SaaS, data stores, internet edge, and legacy platforms.

## Method
1. Asset and process review  
2. Control gap analysis (admin/technical/physical)  
3. Compliance checklist (PCI, GDPR, SOC)  
4. Risk scoring and prioritized remediation

## Key Findings
- Excess access to internal data, including PII and cardholder data
- No encryption for card data at rest; weak TLS coverage in transit
- Missing least-privilege and separation of duties
- No IDS/IPS; limited anomaly detection
- No tested backups and no disaster recovery runbook
- Weak password policy; no centralized password manager
- Legacy systems monitored ad hoc; no schedule or ownership
- Present controls: perimeter firewall, AV/EDR, basic physical security, GDPR 72-hour notification plan

## Risk Rating
**High (8/10)** due to access, encryption, detection, and recovery gaps.

## Control Mapping (sample)
- **Administrative**: Access control policy, RBAC/least-privilege, SoD, account lifecycle, DR plan, data classification
- **Technical**: Firewall, IDS/IPS, AV/EDR, encryption in transit/at rest, password manager, MFA, backups with restore tests
- **Physical**: Locks, CCTV, fire detection, secure storage, lighting, alarms/signage

## Compliance Snapshot
- **PCI DSS**: Gaps in network segmentation, access to CHD, encryption, and credential policy
- **GDPR**: Breach notification flow exists; needs stronger data inventory, classification, and retention controls
- **SOC Trust Services**: Access control, confidentiality, integrity checks, and availability planning need uplift

## Quick Wins (30–60 days)
1. Enforce **least privilege** with role-based groups; remove shared and broad access  
2. Roll out a **password manager** + policy update; require length and **MFA**  
3. Enable **backups** for critical systems and **test restores**; publish a DR runbook  
4. **Encrypt cardholder data** at rest and in transit; **segment** card-processing systems  
5. Add **network detection** (IDS/IPS or WAF fronting); alert on anomalies  
6. **Label and inventory data** with owners, sensitivity, and retention

## Incident Vignette: DoS (SYN Flood)
Observed rapid SYN packets causing service disruption. Mitigations: enable SYN cookies, rate-limit at edge, place site behind WAF/CDN, and add IDS rules for flood patterns. Treat as a detection/response tuning exercise.

## Lessons Learned
- You can’t manage what you haven’t inventoried: identities, access, and data first
- Backups are useless without **tested restores**
- RBAC + encryption + detection + backups remove most practical SMB risk

## How this maps to roles
- **SOC Analyst**: write alerts for unauthorized data access, SYN-flood signatures, and failed backup restores  
- **GRC Analyst**: maintain PCI/GDPR evidence, track control owners/dates, and drive DR tabletop tests

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
