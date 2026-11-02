# Lab 01 — SQL Injection Discovery

[Portfolio](../../README.md) / [Web Applications & SQL](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Evidence & Results](#evidence--results) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I practiced SQL injection analysis against DVWA, an intentionally vulnerable training application. The exercise connects manual probing and database enumeration with the defensive reason for separating query structure from user-supplied data.

## Objectives

- Run an isolated vulnerable application for authorized practice.
- Investigate an injectable parameter manually and with `sqlmap`.
- Explain parameterized queries, validation, and database least privilege as mitigations.

## Environment & Tools

- DVWA in Docker using the repository's [Dockerfile](Dockerfile)
- Burp Suite and `sqlmap`
- Local training accounts and data only

## What I Did

### 1. Set up the local application

```bash
docker build -t dvwa-lab .
docker run -d -p 127.0.0.1:8080:80 dvwa-lab
```

I used the DVWA interface at `http://localhost:8080`. The image's initial database setup must be completed before using its training modules. Its `admin` / `password` login is a classroom default. Binding the published port to loopback keeps this deliberately vulnerable service on the local host.

### 2. Probe the vulnerable page

I used the authenticated SQL Injection module at low security to examine how the `id` parameter changes a database query. Burp Suite helped inspect requests and compare normal input with quote/Boolean test payloads. This module's parameter is distinct from the application's login form.

### 3. Enumerate the lab database with sqlmap

```bash
sqlmap -u "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=<id>; security=low" --dump
```

The session cookie must come from the local authorized lab session. The intentionally vulnerable parameter allowed data extraction from the exercise database.

### 4. Examine defensive controls

I connected the vulnerable behavior with prepared statements, input validation, and least-privilege database access. Bound parameters keep values separate from SQL structure. Allowlist validation supports expected types and ranges; escaping alone is database/context dependent and is not a replacement for parameterization.

## Evidence & Results

The [Dockerfile](Dockerfile) records the DVWA environment. The walkthrough preserves the manual and automated work completed in the training application. The currently published files do not include an application-source patch or before/after captures of the mitigation step; those would make that part of the demonstration easier to reproduce and assess.

## Lessons Learned

- Keep intentionally vulnerable applications isolated and use only authorized targets.
- Distinguish authentication prerequisites from the vulnerable endpoint being tested.
- Explain the unsafe query construction and the corresponding defensive change, rather than treating a successful tool run as the whole assessment.

## Practical Value

This lab demonstrates web-request analysis and the reasoning behind a common application-security control. A useful follow-up is to document a vulnerable query beside its parameterized version, with synthetic before/after requests.

## MITRE ATT&CK Context

[T1190 — Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/) describes relevant adversarial behavior. DVWA is an authorized local training target.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
