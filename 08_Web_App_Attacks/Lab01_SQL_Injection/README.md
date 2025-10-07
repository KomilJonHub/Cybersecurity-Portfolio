# Lab 01: SQL Injection Discovery

> Explore how unsanitized input can lead to authentication bypass and data leakage.

## Objective
Deploy DVWA, discover an injectable parameter, and exploit it with manual techniques and `sqlmap`. Demonstrate mitigations.

## Environment
- DVWA running in Docker
- Tools: Burp Suite, `sqlmap`

## Procedure
1. **Setup DVWA**
   ```bash
   docker build -t dvwa-lab .
   docker run -d -p 8080:80 dvwa-lab
   ```
   Browse to `http://localhost:8080` and log in with `admin` / `password`.

2. **Manual probing**
   - Intercepted the login request with Burp Suite.
   - Tested `' or '1'='1` in the username field to bypass authentication.

3. **Automated exploitation**
   - Used `sqlmap` to enumerate the `users` table:
     ```bash
     sqlmap -u "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=<id>; security=low" --dump
     ```

4. **Mitigation**
   - Enabled prepared statements and strict input validation to block injection attempts.

## Findings
- Unsanitized `id` parameter allowed data extraction and login bypass.
- Parameterized queries and least privilege reduce exposure.

## MITRE ATT&CK Mapping
- [T1190: Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)

## Lessons Learned
Understanding both offensive and defensive techniques is crucial when assessing web applications.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
