## Scenario Overview
I worked on this simulated real-world lab project as part of my Splunk Power User certification prep to gain hands-on experience with the Splunk SIEM tool. The scenario put me in the role of a SOC analyst at Buttercup Games, responsible for monitoring customer activity, employee access, and network traffic during a high-profile sales promotion.  

In this setup, I had to validate e-commerce actions from the web servers, track authentication attempts on the Linux bastion hosts, and monitor email, proxy, and firewall logs for suspicious behavior. The goal was to practice using Splunk fields to separate normal activity from threats, build searches that could evolve into detections, and deliver clear reports that other analysts could rely on in a real shift handoff.


Key telemetry I focused on:
- **Online Sales (`index=web`, `sourcetype=access_combined`)** – tracked cart activity, HTTP codes, and product details.
- **Web Server Security (`index=security`, `sourcetype=linux_secure`)** – monitored shell access and privileged logons.
- **Email Security (`index=security`, `sourcetype=cisco_esa`)** – cross-checked senders and recipients for phishing.
- **Web Proxy (`index=security`, `sourcetype=cisco_wsa_squid`)** – flagged odd destinations and malware verdicts.
- **Firewall (`index=security`, `sourcetype=cisco_firewall`)** – mapped usernames to network paths and policy hits.

Throughout the lab I stuck to three habits: pivot on fields, build searches that double as detections, and turn quick findings into repeatable knowledge.


> 📄 **Lab Playbook:** [Splunk 1 – Using Fields Lab Instructions](artifacts/Splunk%201%20lab%20instructions.pdf)

## Lab Outcomes at a Glance
Here’s how each saved search (L1S1 – L2S2) paid off for the SOC mission.

| Exercise | What I Focused On | SPL Snapshot | Why It Mattered |
| --- | --- | --- | --- |
| L1S1 | Validating web purchase actions against promo traffic | `index=web sourcetype=access_combined action=*` | Confirmed we capture both purchase and non-purchase activity before locking in cart monitoring. |
| L1S2 | Hunting invalid admin logons in real time | `index=security sourcetype=linux_secure failed invalid admin* \| fields user src_ip app` | Surfaced brute-force patterns against admin aliases so IAM could respond quickly. |
| L1S3 | Packaging checkout errors for partners | `... \| table clientip host status \| rename ...` | Delivered a human-friendly error report for incident responders and web ops. |
| L2S1 | Trialing `erex` for quick authentication labels | `... \| erex event_description examples="Accepted password ","Failed password" \| stats ...` | Fast-tracked triage by tagging outcomes without waiting on formal regex. |
| L2S2 | Locking in `rex` for dependable enrichment | `... \| rex field=_raw "(?<event_description>...)" \| rex ...` | Produced repeatable port attribution that stands up in dashboards and alerts. |

---

### L1S1 – Using Fields to Validate E-commerce Activity
- **Objective:** Make sure Buttercup’s promo purchases are accounted for and expose any missing `action` values before an alert goes live.
- **Representative SPL:**
  ```spl
  index=web sourcetype=access_combined earliest=-1d@d latest=@d
  | search action=*
  | stats count by action
  ```
  I iterated with `action=purchase`, `action!=purchase`, and `action=*` to confirm which events carried the field before saving the search.
- **Evidence:**
  - [Lab Report PDF](artifacts/L1S1-2025-09-23.pdf)
  - ![Search Walkthrough Screenshot](screenshots/Screenshot%202025-09-23%20152641.png)

### L1S2 – Hunting Invalid Admin Logons
- **Objective:** Keep a rolling, last-60-minute view of failed admin authentications so brute-force attempts can be squashed quickly.
- **Representative SPL:**
  ```spl
  index=security sourcetype=linux_secure earliest=-60m@m latest=now
  "failed" "invalid"
  | search user=admin*
  | fields user src_ip app
  ```
- **What stood out to me:**

- **Evidence:**
  - [Lab Report PDF](artifacts/L1S2-2025-09-23.pdf)
  - ![Execution Screenshot](screenshots/Screenshot%202025-09-23%20154425.png)

### L1S3 – Reporting Web Checkout Errors with Friendly Labels
- **Objective:** Hand web operations a report they can act on immediately when checkout errors spike.
- **Representative SPL:**
  ```spl
  index=web sourcetype=access_combined action=purchase status>399 earliest=-4h@h latest=now
  | table clientip host status
  | rename clientip AS "Customer IP" host AS "Web Server" status AS "HTTP Status"
  ```

- **Evidence:**
  - [Lab Report PDF](artifacts/L1S3-2025-09-23.pdf)
  - ![Formatted Results Screenshot](screenshots/Screenshot%202025-09-23%20153647.png)

### L2S1 – Building Temporary Fields with `erex`
- **Objective:** Experiment with `erex` so I could label authentication outcomes on the fly while deciding whether a regex investment was worth it.
- **Representative SPL:**
  ```spl
  index=security sourcetype=linux_secure earliest=-7d@d latest=@d "port"
  | erex field=_raw mode=examples event_description examples="Accepted password ","Failed password"
  | erex field=_raw mode=examples port examples="22","2222","443"
  | stats count(port) AS port_count by event_description
  ```

- **Evidence:**
  - [Lab Report PDF](artifacts/L2S1-2025-09-23.pdf)
  - ![erex Results Screenshot](screenshots/Screenshot%202025-09-23%20162114.png)

### L2S2 – Operationalizing Regex-Based Field Extractions
- **Objective:** Graduate the `erex` experiment into production-ready `rex` commands that my teammates can trust in dashboards.
- **Representative SPL:**
  ```spl
  index=security sourcetype=linux_secure earliest=-7d@d latest=@d "port"
  | rex field=_raw "(?<event_description>(Accepted|Failed) password)"
  | rex field=_raw "port (?<port>\d+)"
  | stats count(port) AS port_count by event_description port
  | sort - port_count
  ```
- **Evidence:**
  - [Lab Report PDF](artifacts/L2S2-2025-09-23.pdf)
  - ![Regex Extraction Screenshot](screenshots/Screenshot%202025-09-23%20162644.png)

## Additional Visual References
![Search Progression Screenshot – Job Inspector tip nudging me from `erex` to `rex`.](screenshots/Screenshot%202025-09-23%20162114.png)
![Fields Sidebar Snapshot – The fields I leaned on when slicing product metadata.](screenshots/Screenshot%202025-09-23%20162130.png)

## Lessons Learned
Working through this lab gave me more than just practice with SPL syntax—it showed me how Splunk can be used as a real SOC tool under pressure. I learned how to:

- Validate business-critical activity (like purchases) against raw telemetry to detect fraud or broken workflows.  
- Surface brute-force attempts and privileged account misuse in near real time.  
- Translate raw logs into human-friendly reports that other teams can act on immediately.  
- Use quick field extractions (`erex`) to move fast, then solidify them with regex (`rex`) for lasting detections.  
- Balance speed and accuracy—sometimes the fast answer buys time, while the durable one builds trust for future shifts.  

**Takeaway:** This lab reinforced that effective SOC work isn’t about chasing perfect queries—it’s about using fields smartly, validating results, and leaving behind reliable searches that teammates can depend on.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
