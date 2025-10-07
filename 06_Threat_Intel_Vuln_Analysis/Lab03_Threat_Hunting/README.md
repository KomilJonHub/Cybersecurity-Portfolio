# Lab03 – Threat Hunting Investigation

## Introduction
This lab simulates a **real-world threat hunting scenario** where a security analyst investigates suspicious activity across multiple data sources. The exercise demonstrates how to uncover evidence of intrusion, persistence mechanisms, and **data exfiltration** by correlating logs, host-based artifacts, and network traffic.  

Threat hunting goes beyond waiting for automated alerts — it requires **active hypothesis-driven investigation** to detect Indicators of Compromise (IoCs) that adversaries attempt to conceal.  

By completing this lab, I demonstrated the ability to:  
- Analyze **Windows Event Viewer logs** for DNS anomalies.  
- Investigate **PowerShell execution and persistence mechanisms**.  
- Use **Linux tools** to analyze attacker scripts and outbound connections.  
- Review **firewall logs** to confirm data exfiltration attempts.  
- Correlate host- and network-based artifacts to reconstruct the attack chain.  

---

## Objectives
The investigation was structured around four main objectives:  

1. **Identify suspicious DNS activity** pointing to possible command-and-control (C2) communication.  
2. **Examine PowerShell activity** on endpoints for evidence of execution and persistence.  
3. **Analyze Linux netstat results and attacker scripts** to confirm malicious connectivity.  
4. **Correlate findings with firewall logs** to confirm data exfiltration and the responsible internal IP.  

---

## Lab Environment
The lab was conducted in a controlled training environment that mirrored a realistic SOC investigation.  

- **Windows 10 Endpoint**  
  - Tools: Event Viewer, PowerShell  
  - Focus: DNS logs, script execution, scheduled tasks  

- **Linux (Kali) Environment**  
  - Tools: `netstat`, script inspection  
  - Focus: Malicious connectivity and exfiltration scripts  

- **Firewall Logs**  
  - Focus: Detection of outbound data exfiltration  

---

## Tools & Techniques
- **Windows Event Viewer** (Event IDs: 1001 – DNS assignment, 3010 – DNS queries)  
- **PowerShell Analysis** (script execution, scheduled task persistence)  
- **Linux Command-Line** (`netstat`, reviewing malicious `.sh` scripts)  
- **Firewall Log Review** (traffic correlation with suspected exfiltration host)  
- **Threat Hunting Process**  
  - Hypothesis → Investigation → Correlation → Confirmation  

---

## Investigation Walkthrough

The threat hunting process was conducted in a structured sequence, guided by the lab instructions. Each stage provided key insights into attacker behavior.  

---

###  Step 1 – Firewall Reconnaissance Detection  
- **Action**: Reviewed firewall logs for scanning attempts from a suspected attacker machine (Kali).  
- **Finding**: Evidence of network scans targeting multiple internal systems was logged, confirming reconnaissance activity from an external adversary.  
- **Screenshot 1**: Firewall log entries showing packet captures from the scanning host.  

---

###  Step 2 – Windows DNS Client Events (Event ID 1001 & 3010)  
- **Action**: Investigated **DNS Client logs** in Windows Event Viewer.  
  - Event ID **1001** showed assignment of DNS servers.  
  - Event ID **3010** revealed DNS queries made by the host.  
- **Finding**: Queries to suspicious domains such as `badsite.ru` were uncovered.  
- **Screenshot 2**: Event Viewer filtered to Event ID 3010.  
- **Screenshot 3**: Event ID 1001 showing assigned DNS server (10.1.16.1).  
- **Screenshot 4**: Query to malicious domain `badsite.ru`.  

---

###  Step 3 – PowerShell Execution Analysis  
- **Action**: Executed suspicious PowerShell scripts provided in the environment (`lab04demo2.ps1`, `lab04demo3.ps1`).  
- **Finding**:  
  - Script `lab04demo2.ps1` repeatedly attempted connections until termination.  
  - Script `lab04demo3.ps1` demonstrated persistence behavior by scheduling tasks.  
- **Screenshot 5**: Execution of `lab04demo2.ps1` showing connection attempts.  
- **Screenshot 6**: Evidence of malicious PowerShell activity from scheduled tasks (`lab04demo3.ps1`).  

---

###  Step 4 – Linux Network Forensics (Kali)  
- **Action**: On the Linux machine, used `netstat -np` to identify live malicious connections.  
- **Finding**: Multiple connections to external IPs (`10.1.16.1:443`, `10.1.16.11:37622`) confirmed command-and-control (C2) channels.  
- **Screenshot 7**: Netstat output showing persistent established connections.  
- **Screenshot 8**: Review of `Lab04demo4.sh` script revealing automated outbound exfiltration to `ca.ad.structurereality.com` over port 443.  

---

###  Step 5 – Firewall Exfiltration Logs  
- **Action**: Correlated host findings with **firewall logs** to confirm large-scale data exfiltration.  
- **Finding**: IP `10.1.16.2` was identified as the primary source of exfiltration traffic, transferring large amounts of data out of the network.  
- **Screenshot 9**: Firewall log snippet highlighting outbound transfer from `10.1.16.2`.  
- **Screenshot 10**: Analyst confirmation question identifying `10.1.16.2` as the IoC for exfiltration.  

---

###  Step 6 – Consolidation of Indicators of Compromise (IoCs)  
By the end of the investigation, multiple IoCs were identified across host and network layers:  
- Suspicious DNS queries: `badsite.ru`  
- Malicious PowerShell scripts: `lab04demo2.ps1`, `lab04demo3.ps1`  
- Attacker persistence: Scheduled tasks via PowerShell  
- Malicious Linux script: `Lab04demo4.sh`  
- Malicious outbound host: `10.1.16.2` (responsible for exfiltration)  

**Screenshots 11–16** provide supporting evidence of IoCs and analyst validation steps.  


---

---

## MITRE ATT&CK Mapping
- [T1059.001: PowerShell](https://attack.mitre.org/techniques/T1059/001/)

## Findings & Lessons Learned

This investigation demonstrated how **threat hunting connects scattered evidence into a clear attack story**.  
Key takeaways:  
- **DNS monitoring matters** – unusual queries can reveal command-and-control channels long before exfiltration happens.  
- **PowerShell is both a tool and a weapon** – persistence through scheduled tasks is one of the most common attacker tactics.  
- **Linux visibility is critical** – simple commands like `netstat` or inspecting bash scripts can uncover data exfiltration attempts.  
- **Network correlation closes the loop** – only by combining host forensics with firewall logs was the exfiltrating host confirmed.  
- **IoCs are the bridge between incident and defense** – by documenting domains, IPs, and malicious scripts, the organization can harden defenses and feed intelligence into SIEM/SOAR.  

This exercise showed the importance of **proactive hunting**: you don’t wait for an alert, you dig into the data until the attacker’s path is exposed.  

---

## Investigation Screenshots

The following screenshots capture the key steps of the hunt — from DNS anomalies, to PowerShell persistence, Linux attacker scripts, and final exfiltration evidence in the firewall logs. Together, they illustrate how the investigation unfolded:  

![](screenshots/1.png)  
![](screenshots/2.png)  
![](screenshots/3.png)  
![](screenshots/4.png)  
![](screenshots/5.png)  
![](screenshots/6.png)  
![](screenshots/7.png)  
![](screenshots/8.png)  
![](screenshots/9.png)  
![](screenshots/10.png)  
![](screenshots/11.png)  
![](screenshots/12.png)  
![](screenshots/13.png)  
![](screenshots/14.png)  
![](screenshots/15.png)  
![](screenshots/16.png)  

---

## Final Summary

By walking through this lab, I was able to simulate a **full threat hunt lifecycle**:  
1. Start from suspicious DNS traffic.  
2. Pivot into PowerShell logs to uncover persistence.  
3. Confirm attacker activity in Linux and firewall logs.  
4. Document the full kill chain and IoCs.  

This mirrors the daily work of SOC analysts and threat hunters: piecing together fragmented events into a coherent narrative that explains **who the attacker was, how they persisted, and what data they tried to steal**.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
