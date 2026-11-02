# Lab 03 — Splunk Data Models, `tstats`, and Report Acceleration

[Portfolio](../../README.md) / [SIEM & Log Analysis](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [Lessons Learned](#lessons-learned) · [Evidence & Results](#evidence--results)

## Overview

I used **data models**, **`tstats`**, and **report acceleration** in the Buttercup Games training environment. I built a monthly revenue report, enabled acceleration, inspected search jobs, and produced an APAC vendor rollup. The saved outputs show the work; the timings below are observations from individual runs.

---

## Objectives

- Query **data models** via `datamodel` and their **accelerated summaries**.
- Use **`tstats`** for fast, schema-aware aggregations.
- Build, save, and **accelerate** a monthly revenue report.
- Validate the performance delta with **Job Inspector**.
- Present results stakeholders can use without translation.

---

## Environment & Tools

- **Splunk Enterprise** → *Search & Reporting*
- **Data models**: `vsales.apac` and `AccButtercup_Games_Online_Sales` in the course environment
- **Sources**: Buttercup Games online store logs (`access_combined`)
- **Time ranges**: *Year to date*, *Previous week*, *Last 30 days*, *Last 5 minutes*

---

## Task 1 — Build the Monthly Online Sales Revenue report

**Scenario.** Sales wants a sortable table of revenue per `productId` for the last 30 days. First run on raw events, then save and accelerate.

**SPL (raw events)**
```spl
index=web sourcetype=access_combined action=purchase status=200
| fields price, productId
| stats sum(price) as revenue by productId
| eval revenue="$".tostring(revenue,"commas")
```

**Result.** Table by product with formatted currency. For a numeric revenue ranking, sort before converting the amount to a currency string.
![Monthly revenue table](./screenshots/Screenshot%202025-09-25%20174641.png)

**Saved reports.**
- `allStudents_Sales_Report_MonthlyOnlineSalesRevenue` (baseline)
- `Karimov_Sales_Report_MonthlyOnlineSalesRevenue` (my copy)

![Reports list](./screenshots/Screenshot%202025-09-25%20201155.png)

---

## Task 2 — Enable Report Acceleration and verify

**Scenario.** Make the monthly revenue report fast for ad-hoc use and dashboards.

**Steps.**
1. Open the saved report → **Edit → Acceleration** → enable.
2. Confirm summary under **Settings → Report Acceleration Summaries**.
3. Re-run the report and confirm the job banner shows **Using summaries for search**.

**Evidence.**
- Job using summaries (hover):  
  ![Job using summaries](./screenshots/Screenshot%202025-09-25%20175318.png)
- Acceleration infrastructure pages:  
  ![Report acceleration list](./screenshots/Screenshot%202025-09-25%20174947.png)  
  ![My saved report with acceleration enabled](./screenshots/Screenshot%202025-09-25%20174853.png)

**Performance check (Job Inspector).**
- Run A: scanned **12,530** events in **0.363s**.  
  ![Inspector A](./screenshots/Screenshot%202025-09-25%20175348.png)
- Run B: scanned **10,874** events in **0.448s**.  
  ![Inspector B](./screenshots/Screenshot%202025-09-25%20174649.png)

*Takeaway:* The summary-use message confirms that the accelerated report used summaries. These runs scanned different event counts and were taken at different times, so they are not a controlled speedup benchmark. A fair comparison would hold the search, time range, dataset, and cache conditions constant across repeated runs.

---

## Task 3 — Compare data model events vs. summaries

**Scenario.** Compare events from **AccButtercup_Games_Online_Sales** with and without summaries, checking both output fields and coverage.

**Events (no summaries)**
```spl
| datamodel AccButtercup_Games_Online_Sales search summariesonly=false
```

**Summaries**
```spl
| datamodel AccButtercup_Games_Online_Sales search summariesonly=true
```

**Result.** Both views expose the model fields, but the captured relative windows differ and show different event counts. Summary availability and time boundaries need checking before treating outputs as equivalent.<br>
![Events view](./screenshots/Screenshot%202025-09-25%20190231.png)  
![Summaries view](./screenshots/Screenshot%202025-09-25%20190238.png)

---

## Task 4 — Year-to-date monthly volume with `tstats`

**Scenario.** Leadership wants YTD activity by month.

**SPL**
```spl
| tstats count as events where index=* by _time span=1mon
| eval Month=strftime(_time,"%B %Y"), events=tostring(events,"commas")
| table Month events
```

**Result.** Month-by-month volume with friendly labels and comma formatting.  
![YTD monthly volume](./screenshots/Screenshot%202025-09-25%20191624.png)

---

## Task 5 — APAC vendor sales rollup from the `vsales` data model

### 5A. Stakeholder table via `datamodel` + `stats`
```spl
| datamodel vsales apac flat
| stats sum(price) as Sales by Vendor, VendorCountry, VendorCity
| search Sales > 200
```
**Result.** APAC list filtered to meaningful sales only.  
![APAC via datamodel](./screenshots/Screenshot%202025-09-25%20185456.png)

### 5B. Same ask, optimized with `tstats`
```spl
| tstats sum(apac.price) as Sales from datamodel=vsales.apac by apac.Vendor apac.VendorCountry apac.VendorCity
| search Sales > 200
| rename apac.Vendor as "Vendor", apac.VendorCountry as "Country", apac.VendorCity as "City"
| sort Country Vendor City
| eval Sales="$".tostring(Sales,"commas")
| table Vendor Country City Sales
```
**Result.** APAC aggregates with readable labels through `tstats`; the screenshot records the resulting table.<br>
![APAC via tstats](./screenshots/Screenshot%202025-09-25%20194440.png)

---

## Lessons Learned

- **`tstats`** can query indexed fields and accelerated data-model summaries efficiently; field availability and acceleration coverage determine whether it fits the question.
- **Acceleration** needs time to build, and summary coverage affects the result.
- **Name the output for humans** (`rename`, `tostring`) to reduce friction.
- **Compare carefully:** Job Inspector metrics are useful only with the search context and workload recorded.

---

## Personal Reflection

I built the raw query first, then inspected acceleration and the search jobs. Switching between `datamodel … search` and `tstats` clarified the difference between reviewing events and requesting aggregates. I also learned to separate a successful configuration check from a controlled performance comparison.

## Evidence & Results

The original [course guide](artifacts/Splunk%20Lab2%20content.pdf), [report exports](artifacts/), and [screenshots](screenshots/) retain the searches, output, and Job Inspector observations.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
