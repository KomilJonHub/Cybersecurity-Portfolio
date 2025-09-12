# Lab01 - SQL Injection Discovery

## Objective
Identify and exploit a basic SQL injection vulnerability within a deliberately vulnerable web application and document mitigation strategies.

## Tools Used
- DVWA (Damn Vulnerable Web Application)
- sqlmap
- Burp Suite

## Steps
1. Enumerated the login form and intercepted requests with Burp Suite.
2. Used `sqlmap` to automate detection and extraction of user credentials.
3. Demonstrated how parameterized queries prevent injection attacks.

## Findings
- The application accepted unsanitized input, allowing authentication bypass and data exfiltration.
- Implementing prepared statements and input validation mitigated the issue.

## References
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
