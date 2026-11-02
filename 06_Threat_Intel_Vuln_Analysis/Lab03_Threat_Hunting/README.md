# Lab03 — Threat Hunting Investigation

[Portfolio](../../README.md) / [Threat & Vulnerability Analysis](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I completed this threat-hunting lab in a controlled training environment. I examined Linux firewall events, Windows connections and processes, PowerShell scripts and scheduled tasks, DNS Client events, and a supplied firewall-log exercise. My screenshots record both the investigation steps and the demonstration activity provided by the lab.

The aim was to build an explanation from several sources: which host made a connection, which process owned it, what the script did, and what deserved further investigation. I learned to distinguish an observation from a conclusion about compromise, persistence, or data loss.

## Objectives

1. Enable and review host firewall logging to recognize a controlled scan.
2. Map Windows connections to process IDs and command lines.
3. Inspect repeated connection behavior and a running scheduled task.
4. Use Linux connection information and script contents to explain activity.
5. Review DNS events and prioritize unusual traffic in a supplied incident scenario.

## Environment & Tools

| Environment | Tools and evidence |
|---|---|
| **Ubuntu LAMP host** | `iptables`, saved rule listing, `/var/log/kern.log` |
| **Kali Linux** | Interface address checks, inspection of the lab Nmap script, `netstat`, shell script review |
| **Windows lab hosts** | CMD `netstat` and `tasklist`, PowerShell process queries, script and scheduled-task inspection |
| **Windows DNS Client events** | Event Viewer, provider-specific event IDs 1001 and 3010 |
| **Supplied firewall-log question** | Traffic/volume comparison and selection of an address for further investigation |

The private addresses and lab domains below belong to the training scenario. Their appearance in a connection table is not, by itself, evidence of a malicious external host.

---

## Investigation Walkthrough

### Step 1 — Enable Logging and Recognize the Controlled Scan

I enabled an `iptables` input logging rule on the Ubuntu host, saved the rules, and reviewed the kernel log. The first attempt lacked sufficient permission; I switched to a privileged session before applying the rule. On Kali I checked the interface address and examined the supplied `lab04demo1.sh` Nmap command.

- **Screenshot 1:** Ubuntu session, initial permission error, privileged logging setup, rule export, and log-following command.
- **Screenshot 2:** Kali interface address after starting the lab demonstration script.
- **Screenshot 3:** Kernel log traffic providing a baseline for comparison.
- **Screenshot 4:** TCP SYN entries from `172.16.0.100` with sequential destination ports, consistent with the controlled scan.
- **Screenshot 5:** Kali address and script contents showing the Nmap target `172.16.0.201` and port range 1–100.

Correlating the script with the logged traffic explained the scan pattern. The host firewall logs and demonstration script provide the context for this controlled scan.

### Step 2 — Connect Windows Sockets with Processes

I used `netstat -nop tcp` to inspect connections and their process IDs, then used `tasklist` to identify the corresponding executables.

- **Screenshot 6:** Windows TCP connections and process IDs, followed by the `tasklist` command.
- **Screenshot 7:** Windows process listing and a filtered query identifying PID 4 as `System`.
- **Screenshot 8:** Another Windows host's connection table and a filtered PID query identifying `powershell.exe` for a connection to `10.1.16.1:443`.

A connection and a process name provide a starting point. I needed the command line, script, and task context to explain why PowerShell was making the connection.

### Step 3 — Inspect PowerShell Execution and Scheduled-Task Context

I queried `Win32_Process` and inspected the command line for a PowerShell process. I then read the script and listed running scheduled tasks under `SYSTEM`.

- **Screenshot 9:** Process properties show PowerShell launched with `-File` and a path to `lab04demo3.ps1`.
- **Screenshot 10:** Script contents, the command-line search, and a running scheduled task named `Lab04Demo3.ps1`.
- **Screenshot 14:** A separate execution of `lab04demo2.ps1` prints its attempt counter and terminates after the displayed maximum.

In `lab04demo3.ps1`, the counter increment is commented out, so the loop continues making requests with a sleep interval. The running scheduled task provides the task context for that behavior. A scheduled task can support persistence, but the screenshot alone does not establish its trigger, how it was registered, or whether it survives a reboot.

### Step 4 — Explain Linux Connections Using the Script

I reviewed Linux connection tables and read `/root/lab04demo4.sh`.

- **Screenshot 11:** `netstat -np --protocol=inet` shows multiple `nc` connections from the Kali host to `10.1.16.1:443`, alongside SSH and network-management traffic. The same screenshot includes the script contents.

The script adds a hosts-file mapping for `ca.ad.structureality.com`, then repeatedly opens an `nc` connection to port 443 with a sleep interval. This explains the repeated connections in the demonstration. Port 443 and an established socket do not prove TLS, command-and-control, or data exfiltration; the visible script does not show a data source being uploaded. The separate SSH connections should not automatically be treated as malicious activity.

### Step 5 — Evaluate the Supplied Firewall-Log Exercise

**Screenshot 12** is a course question about possible exfiltration. It contains a supplied log excerpt and my original selection of `10.1.16.2`; it does not show a scored result.

On review, the strongest volume anomaly in the displayed excerpt is **`10.1.24.101` → `220.181.38.251:53`**, with a permitted entry labelled **`1029M BYTES`**. The same internal host also has a denied connection to destination port 7777. That makes `10.1.24.101` a priority for further investigation. The visible `10.1.16.2` entries show a smaller internal web connection and a denied FTP connection, which do not support the earlier README's claim of confirmed large-scale exfiltration from that host.

I preserved the original screenshot and selection. The revised assessment follows the visible log: investigate the unusual source, destination, protocol, and volume, then seek endpoint and traffic evidence before deciding whether sensitive data actually left the environment. The exercise's byte count is supplied data, not a measurement I collected.

### Step 6 — Examine DNS Client Events

I reviewed the Windows DNS Client Events Operational channel and filtered/searched its records.

- **Screenshot 13:** Event ID 1001 reports DNS server information, including `10.1.16.1`.
- **Screenshot 15:** Event ID 3010 and a search for `badsite.ru`; the displayed message records a query for the lab domain.
- **Screenshot 16:** The DNS event's Details view, including process/thread identifiers and event metadata.

Event IDs must be interpreted with their provider and channel, not treated as universal Windows meanings. The DNS query is a lead in this lab context; the domain string alone does not prove a successful connection or command-and-control.

---

## Findings and Investigation Leads

| Evidence | What I established | What would resolve the next question |
|---|---|---|
| Sequential SYN log entries and the Nmap script | The controlled scan generated a recognizable host firewall pattern | Compare timestamps, source/target, and authorized scan scope |
| Windows sockets and process queries | Process IDs connect network activity to `System` or PowerShell | Inspect command line, parent process, and expected host role |
| PowerShell script and running task | A nonincrementing loop explains repeated requests; a named task is running | Inspect the task definition, trigger, principal, and registration history |
| Linux `nc` sockets and script | The script explains repeated port-443 connections | Inspect payloads and endpoints before assigning C2 or exfiltration intent |
| Supplied firewall excerpt | `10.1.24.101` has the standout permitted-volume entry | Correlate endpoint activity and traffic contents with the incident timeline |
| DNS Client event | A query for the lab's suspicious domain is present | Correlate process context, response, connections, and other host evidence |

## Lessons Learned

- Process IDs are useful pivots between a network table and the executable responsible for activity.
- Reading a script can explain repeated connections more precisely than classifying traffic by port alone.
- Scheduled-task context matters, but a running task is not a complete persistence investigation.
- A firewall log can identify a priority lead without confirming what data was transferred.
- Revisiting an initial answer against the evidence is part of a sound investigation.

## MITRE ATT&CK Mapping

- [T1059.001 — PowerShell](https://attack.mitre.org/techniques/T1059/001/): the lab demonstrates PowerShell script execution and process inspection.
- [T1053.005 — Scheduled Task](https://attack.mitre.org/techniques/T1053/005/): the running task provides a relevant investigation example; its full persistence properties require the task definition.

---

## Investigation Screenshots

<details>
<summary><b>Open the complete original screenshot sequence</b></summary>

### Linux logging and controlled scan

![1 — Ubuntu firewall logging setup and privilege correction](screenshots/1.png)
![2 — Kali interface address for the demonstration](screenshots/2.png)
![3 — Ubuntu kernel firewall log baseline](screenshots/3.png)
![4 — Sequential destination ports in TCP SYN log entries](screenshots/4.png)
![5 — Nmap demonstration script and Kali address](screenshots/5.png)

### Windows connections, processes, and task analysis

![6 — Windows TCP connections and process IDs](screenshots/6.png)
![7 — Windows tasklist and filtered System process](screenshots/7.png)
![8 — Connection PID correlated with powershell.exe](screenshots/8.png)
![9 — PowerShell process command line and properties](screenshots/9.png)
![10 — PowerShell loop contents and running scheduled task](screenshots/10.png)

### Linux connections and supplied firewall exercise

![11 — Linux netstat output and repeated nc connection script](screenshots/11.png)
![12 — Supplied firewall log and original unscored quiz selection](screenshots/12.png)

### DNS events and bounded PowerShell demonstration

![13 — DNS Client event 1001 with server information](screenshots/13.png)
![14 — PowerShell demo2 counter and termination message](screenshots/14.png)
![15 — DNS Client event 3010 query and domain search](screenshots/15.png)
![16 — DNS Client event Details view](screenshots/16.png)

</details>

## Practical Value

This lab gave me practice moving between command output, script behavior, event details, and written findings. The same habits help with troubleshooting, network support, incident analysis, and documenting when a result needs further investigation.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
