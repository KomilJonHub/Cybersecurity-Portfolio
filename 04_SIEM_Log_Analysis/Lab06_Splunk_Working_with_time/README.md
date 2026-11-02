# Lab: Splunk — Working With Time

[Portfolio](../../README.md) / [SIEM & Log Analysis](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [Evidence & Results](#evidence--results) · [Lessons Learned](#lessons-learned)

## Overview
I ran this lab to practice **time-aware analysis** in Splunk. Acting as a SOC analyst at **Buttercup Games**, I turned raw badge, proxy, and web logs into reports that answer specific time-based questions for Facilities, Network, and Sales teams. I used time pickers, `earliest`/`latest` modifiers, `bin`, `timechart`, and date functions to produce concise, handoff-ready visuals and tables.

## Objectives
- Group events by hour and day with `bin` and `timechart`.
- Compare current vs. prior periods using `relative_time`, `if()`, and trend summaries.
- Format time for humans with `strftime`, totals with `addtotals`, and currency with `foreach`.
- Save each task as a named report (L1S1, L1X, L2S1–L2S3) for repeatable ops.

## Environment & Tools
- **App:** Search & Reporting (Splunk Enterprise 9.x)
- **Indexes & sourcetypes:**  
  - `index=security sourcetype=history_access` (badge reader)  
  - `index=network sourcetype=cisco_wsa_squid` (web security appliance)  
  - `index=web sourcetype=access_combined` (online sales)

---

## Lab Exercise 1 — Searching with Time

### L1S1 — Hourly Badge Events by Department
**Scenario:** Facilities wants hourly counts of badge swipes by department. The screenshot records a Last 24 hours view.<br>
**SPL:**
```spl
index=security sourcetype=history_access
| bin span=1h _time
| stats count by Department, _time
| stats list(Department), list(count) by _time
```
**Notes:** `bin` snaps timestamps to the hour. Second `stats` pivots to one row per hour with department lists and counts.  
**Saved report:** L1S1  
**Screenshot:**  
![L1S1 — Hourly badge-ins by department](./screenshots/Screenshot%202025-09-30%20192313.png)

---

### L1X (Challenge) — Previous business week, grouped into ranges of 100
**Scenario:** Facilities wants last business week’s badge “Access” events per department, bucketed by 100s.  
**SPL:**
```spl
index=security sourcetype=history_access Event_Description="Access"
| stats count as events by Department
| sort -events
| bin events span=100
| stats list(Department) as Department by events
| sort events
```
**Notes:** Buckets show volume tiers; listing departments per bucket keeps it readable.  
**Saved report:** L1X  
**Screenshot:**  
![L1X — Events bucketed by 100](./screenshots/Screenshot%202025-09-30%20193648.png)

---

## Lab Exercise 2 — Formatting Time & Using Time Commands

### L2S1 — Non-business web usage by day (previous business week)
**Scenario:** Network wants non-business categories in one-day bins with human-readable day labels. The captured search uses `earliest=-1w@w1 latest=@w1`, a Monday-to-Monday week.<br>
**SPL:**
```spl
index=network sourcetype=cisco_wsa_squid usage!=Business earliest=-1w@w1 latest=@w1
| timechart span=1d count by usage
| eval Day=strftime(_time,"%a %d")
| table Day Borderline Personal Unknown Violation
```
**Notes:** `timechart` handles daily grouping; `strftime` formats `_time` for a clear table and chart.  
**Saved report:** L2S1  
**Screenshots:**  
Table view  
![L2S1 — Daily table](./screenshots/Screenshot%202025-09-30%20202636.png)  
Line chart  
![L2S1 — Daily line chart](./screenshots/Screenshot%202025-09-30%20202916.png)

---

### L2S2 — Server errors: this week vs. prior-month average
**Scenario:** Compare the **last 7 days** of server errors to the **average** from one month ago up to yesterday.  
**SPL:**
```spl
index=network sourcetype=cisco_wsa_squid sc_http_status>=500 earliest=-1mon@m latest=@d
| eval StartTime=relative_time(now(),"-7d@d")
| eval Series=if(_time>=StartTime,"this_week","prior")
| timechart span=1d count by Series
| eval Day=strftime(_time,"%A")
| eval Day_Num=strftime(_time,"%w")
| stats avg(prior) as Average, sum(this_week) as "This Week", values(Day) as Day by Day_Num
| eval Average=round(Average,2)
| table Day Average "This Week"
```
**Notes:** `relative_time` defines the split point; `stats` summarizes the earlier-period daily counts and recent totals by weekday. In `-1mon@m`, `mon` is one month while the `@m` snap is to a minute, not the start of a month. Recording the resolved time boundaries makes the comparison easier to audit.<br>
**Saved report:** L2S2  
**Screenshot:**  
![L2S2 — This week vs prior average](./screenshots/Screenshot%202025-09-30%20204736.png)

---

### L2S3 — Web sales report with totals, units, and average sale amount
**Scenario:** Sales wants the previous business week’s successful purchase records within the lab's hour filter, with totals and formatted currency. `date_hour>=9 AND date_hour<=17` includes the entire 17:00 hour, through 17:59; a strict 09:00–17:00 boundary would use `<17`.<br>
**SPL:**
```spl
index=web sourcetype=access_combined status=200 productId=* date_hour>=9 AND date_hour<=17
| timechart sum(price) as DailySales count as UnitsSold
| eval AvgSaleAmt=if(UnitsSold>0, DailySales/UnitsSold, null())
| eval Day=strftime(_time,"%a")
| addtotals col=t row=f label=TOTALS labelfield=Day DailySales, UnitsSold
| foreach Daily*, Avg* [ eval <<FIELD>>="$".tostring(<<FIELD>>,"commas") ]
| table Day DailySales UnitsSold AvgSaleAmt
```
**Notes:** `addtotals` produces totals row; `foreach` formats currency consistently.  
**Saved report:** L2S3  
**Screenshot:**  
![L2S3 — Sales table with totals](./screenshots/Screenshot%202025-09-30%20211406.png)

---

## SPL Cheatsheet (used here)
```spl
# Snap time to bins
| bin span=1h _time

# Daily time series by field(s)
| timechart span=1d count by usage

# Prior vs this-week split
| eval StartTime=relative_time(now(),"-7d@d")
| eval Series=if(_time>=StartTime,"this_week","prior")

# Human-readable day labels
| eval Day=strftime(_time,"%a %d")  # or "%A" for full name

# Totals and currency formatting
| addtotals col=t row=f label=TOTALS labelfield=Day DailySales, UnitsSold
| foreach Daily*, Avg* [ eval <<FIELD>>="$".tostring(<<FIELD>>,"commas") ]
```

## Evidence & Results

The screenshots preserve the completed reports and resolved time windows. The guide supplies the exercise scenarios.

- Lab guide PDF: [`Lab Content`](./artifacts/Splunk%20lab5.pdf)

## Lessons Learned
- Time functions (`bin`, `timechart`, `strftime`) turn raw logs into clear, time-based insights.  
- `relative_time` enables quick current vs. prior comparisons without joins.  
- Formatting with totals, currency, and day labels makes reports readable for non-technical teams.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
