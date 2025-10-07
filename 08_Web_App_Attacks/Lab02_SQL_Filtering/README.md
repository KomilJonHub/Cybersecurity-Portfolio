# Lab 02: SQL Filtering

> Apply input filtering to block SQL injection attempts.

## Objective
Understand how filtering controls such as validation, whitelisting, and parameterization neutralize malicious SQL payloads.

## Filtering Techniques
- **Input Validation:** Enforce expected data types and lengths before processing.
- **Whitelisting:** Accept only known-good characters or patterns.
- **Parameterized Queries:** Use placeholders so user data is never executed as SQL code.
- **Escaping/Encoding:** Properly encode special characters to prevent them from altering query structure.

## Role in Preventing SQL Injection
Filtering treats user input as data, not executable commands. By sanitizing or isolating untrusted values, it becomes significantly harder for attackers to modify queries, exfiltrate data, or escalate privileges.

## MITRE ATT&CK Mapping
- [T1190: Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)

## Lessons Learned
Consistent filtering, combined with least privilege and monitoring, forms a strong defense-in-depth strategy against SQL injection.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
