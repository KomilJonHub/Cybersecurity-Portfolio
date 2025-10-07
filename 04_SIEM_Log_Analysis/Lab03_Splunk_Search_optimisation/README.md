# Lab 02 — Splunk Data Models, `tstats`, and Report Acceleration

This lab focuses on speed and clarity. I used **data models**, **`tstats`**, and **report acceleration** to turn a heavy monthly revenue query into a fast, production-ready report, then verified gains with **Job Inspector**. I also built stakeholder-style tables on the *sales* data model, including an APAC vendor rollup.

---

## Objectives

- Query **data models** via `datamodel` and their **accelerated summaries**.
- Use **`tstats`** for fast, schema-aware aggregations.
- Build, save, and **accelerate** a monthly revenue report.
- Validate the performance delta with **Job Inspector**.
- Present results stakeholders can use without translation.

---

## Environment & Datasets

- **Splunk Enterprise** → *Search & Reporting*
- **Data Model**: `sales` (e.g., `sales.apac`, `AccButtercup_Games_Online_Sales`)
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
| sort - revenue
```

**Result.** Clean table by product with formatted currency.  
![Monthly revenue table](./screenshots/Screenshot%202025-09-25%20174853.png)

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
  ![Job using summaries](./screenshots/Screenshot%202025-09-25%20174853.png)
- Acceleration infrastructure pages:  
  ![Report acceleration list](./screenshots/Screenshot%202025-09-25%20174947.png)  
  ![Acceleration summaries](./screenshots/Screenshot%202025-09-25%20175318.png)

**Performance check (Job Inspector).**
- Run A: scanned **12,530** events in **0.363s**.  
  ![Inspector A](./screenshots/Screenshot%202025-09-25%20175348.png)
- Run B: scanned **10,874** events in **0.448s**.  
  ![Inspector B](./screenshots/Screenshot%202025-09-25%20174649.png)

*Takeaway:* Once summaries build, subsequent executions read from summary buckets. Less scan, faster dashboards.

---

## Task 3 — Compare data model events vs. summaries

**Scenario.** Validate **AccButtercup_Games_Online_Sales** returns the same fields whether pulling events or summaries.

**Events (no summaries)**
```spl
| datamodel AccButtercup_Games_Online_Sales search summariesonly=false
```

**Summaries**
```spl
| datamodel AccButtercup_Games_Online_Sales search summariesonly=true
```

**Result.** Same schema; summaries reduce work.  
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

## Task 5 — APAC vendor sales rollup from the `sales` data model

### 5A. Stakeholder table via `datamodel` + `stats`
```spl
| datamodel v=sales apac flat
| stats sum(price) as Sales by Vendor, VendorCountry, VendorCity
| search Sales > 200
```
**Result.** APAC list filtered to meaningful sales only.  
![APAC via datamodel](./screenshots/Screenshot%202025-09-25%20185456.png)

### 5B. Same ask, optimized with `tstats`
```spl
| tstats sum(apac.price) as Sales from datamodel=v:sales.apac by apac.Vendor apac.VendorCountry apac.VendorCity
| search Sales > 200
| rename apac.Vendor as "Vendor", apac.VendorCountry as "Country", apac.VendorCity as "City"
| sort Country Vendor City
| eval Sales="$".tostring(Sales,"commas")
| table Vendor Country City Sales
```
**Result.** Same story, faster path; business-ready labels.  
![APAC via tstats](./screenshots/Screenshot%202025-09-25%20194440.png)

---

## Lessons Learned

- **`tstats` over data models** is the default for speed when you need aggregates.
- **Acceleration** needs time to build, then delivers interactive performance.
- **Name the output for humans** (`rename`, `tostring`) to reduce friction.
- **Prove value** with Job Inspector metrics, not vibes.

---

## Personal Reflection

I built the raw query first, then accelerated it and proved the gain with hard numbers. Switching between `datamodel … search` and `tstats` clarified when I want rows versus speed. The final tables are readable in a meeting without me narrating.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
