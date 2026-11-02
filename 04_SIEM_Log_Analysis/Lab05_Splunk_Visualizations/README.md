# Lab: Splunk Visualizations — Turning Data into Insight

[Portfolio](../../README.md) / [SIEM & Log Analysis](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Lessons Learned](#lessons-learned) · [Evidence & Results](#evidence--results) · [Practical Value](#practical-value)

## Overview
I worked on this visualization lab as part of my Splunk Power User certification prep to gain hands-on experience turning raw log data into actionable insights. The scenario placed me in the role of a SOC analyst at **Buttercup Games**, responsible for making complex datasets readable and usable during a high-traffic sales period.

In this setup, I had to compare e-commerce web sales against vendor transactions, track failed login trends across Linux servers, and highlight risky network activity in proxy and access logs. The goal was to practice building timecharts, single-value panels, and geographic maps that transform noise into clear visuals. These visualizations allow different teams—business, operations, and security—to understand key patterns at a glance and review results with clear context.

---

## Objectives
- Practice visualizing **sales and security data** with Splunk’s built-in tools.  
- Combine multiple datasets into one chart.  
- Apply formatting, renaming, and trendlines for clarity.  
- Use maps (choropleth and cluster) to display geographic insights.  
- Create **challenge visualizations** using trellis, gauges, and maps.  

---

## Environment & Tools
- **Platform:** Splunk Enterprise 9.x (Search & Reporting app)  
- **Indexes used:**  
  - `index=web` (`sourcetype=access_combined`)  
  - `index=sales` (`sourcetype=vendor_sales`)  
  - `index=security` (`sourcetype=linux_secure`, `sourcetype=history_access`)  
  - `index=network` (`sourcetype=cisco_wsa_squid`)  
  - `index=games` (`sourcetype=SimCubeBeta`)  
- **Roles:** poweruser  
- **Time ranges:** Last 24h, Last 7d, Last 30d, Previous week  

---

## What I Did

### L1S1 — Compare web vs. vendor sales
```spl
(index=web sourcetype=access_combined action=purchase status=200) 
OR (index=sales sourcetype=vendor_sales)
| timechart span=1h count by sourcetype
```
Result: hourly counts of purchases per sourcetype.  
![L1S1](./screenshots/Screenshot%202025-09-27%20125429.png)

---

### L1S2 — Rename fields for clarity
```spl
... 
| rename vendor_sales as retailSales, access_combined as webSales
```
Displayed in a column chart. Clearer naming: *webSales vs. retailSales*.  
![L1S2](./screenshots/Screenshot%202025-09-27%20130350.png)

---

### L1S3 — Linux login failures trend
```spl
index=security sourcetype=linux_secure fail*
| timechart count as failures span=1d
| trendline sma2(failures) as trend
```
Line chart with 7 days of login failures plus a smoothed trendline.  
![L1S3](./screenshots/Screenshot%202025-09-27%20133900.png)

---

### L1S4 — Strategy category sales
```spl
index=sales sourcetype=vendor_sales categoryId="STRATEGY"
| timechart count span=1d
```
Daily sales trend for strategy games.  
![L1S4](./screenshots/Screenshot%202025-09-27%20135447.png)

---

### L1S5 — Single value visualization
Same data as L1S4 but displayed as **Single Value** with delta from previous day.  
![L1S5](./screenshots/Screenshot%202025-09-27%20140003.png)

---

### L1S6 — Geo distribution of products sold
```spl
index=web sourcetype=access_combined action=purchase status=200 sale_price=*
| iplocation clientip
| geostats count by product_name globallimit=0
```
Cluster map showing purchases by geolocation.  
![L1S6](./screenshots/Screenshot%202025-09-27%20143752.png)

---

### L1S7 — Retail sales by country with totals
```spl
index=sales sourcetype=vendor_sales
| stats count as "Retail Events" by VendorCountry
| appendpipe [ stats sum("Retail Events") as "Retail Events" | eval VendorCountry="Total" ]
```
Added a total row at the bottom.  
![L1S7](./screenshots/Screenshot%202025-09-27%20150723.png)

---

## Challenge Exercises

### LX1 — Trellis pie charts for proxy usage
```spl
index=network sourcetype=cisco_wsa_squid usage!=Business
| chart count over location by usage
```
Split by location → trellis pie charts (Boston, London, San Francisco).  
![LX1](./screenshots/Screenshot%202025-09-27%20151659.png)

---

### LX2 — Gauge visualization
```spl
index=security sourcetype=history_access Address_Description="San Francisco"
| dedup rfid
| stats count
```
Displayed as a filler gauge showing count of distinct RFID badges used.  
![LX2](./screenshots/Screenshot%202025-09-27%20152958.png)

---

### LX3 — Global gaming events map
```spl
index=games sourcetype=SimCubeBeta earliest=-30d@d latest=now
| iplocation user_ip
| stats count as Events by Country
| geom geo_countries featureIdField=Country
```
Choropleth map showing worldwide distribution of game events.  
![LX3](./screenshots/Screenshot%202025-09-27%20154212.png)

---

## Lessons Learned

- **Field renaming** makes chart series and tables easier to understand.
- **Trendlines** help summarize changes while the underlying counts remain available for review.
- **Single values and gauges** need a labelled metric, time range, and useful comparison.
- **Trellis layouts** make regional category distributions easier to compare.
- **Maps** add geographic context, but an IP-derived location is an approximation.
- Choosing a visualization starts with the question: a count of purchase events, revenue, and distinct users are different measures.

## MITRE ATT&CK Mapping

These are visualization and analysis exercises. Authentication trends and proxy patterns can support a later investigation, but the displayed sales, geographic, and usage charts do not establish an ATT&CK technique by themselves.

## Evidence & Results

The [lab guide](artifacts/Splunk%20lab4.pdf) supplies the scenarios and dataset. The task screenshots above document the completed visualizations. Additional original evidence shows the intermediate table views, US-state map exercise, and saved reports:

<details>
<summary>Open intermediate tables, map exercise, and report index</summary>

![Linux authentication failure counts before adding the trendline](screenshots/Screenshot%202025-09-27%20133437.png)
![US state geometry table](screenshots/Screenshot%202025-09-27%20141935.png)
![US state choropleth map](screenshots/Screenshot%202025-09-27%20142413.png)
![Saved reports including completed exercises](screenshots/Screenshot%202025-09-27%20154607.png)

</details>

## Practical Value

I practiced selecting and labelling visualizations so another person can inspect the underlying data, compare periods or locations, and understand the measure being presented.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
