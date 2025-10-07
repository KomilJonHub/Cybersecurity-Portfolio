
# Lab: Splunk Visualizations — Turning Data into Insight

## Scenario Overview
I worked on this visualization lab as part of my Splunk Power User certification prep to gain hands-on experience turning raw log data into actionable insights. The scenario placed me in the role of a SOC analyst at **Buttercup Games**, responsible for making complex datasets readable and usable during a high-traffic sales period.

In this setup, I had to compare e-commerce web sales against vendor transactions, track failed login trends across Linux servers, and highlight risky network activity in proxy and access logs. The goal was to practice building timecharts, single-value panels, and geographic maps that transform noise into clear visuals. These visualizations allow different teams—business, operations, and security—to understand key patterns at a glance and respond quickly.y city. The goal was simple: build visuals that carry their own context so the next analyst can open the report, glance, and act.

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
![L1S3](./screenshots/Screenshot%202025-09-27%20133437.png)

---

### L1S4 — Strategy category sales
```spl
index=sales sourcetype=vendor_sales categoryId="STRATEGY"
| timechart count span=1d
```
Daily sales trend for strategy games.  
![L1S4](./screenshots/Screenshot%202025-09-27%20133900.png)

---

### L1S5 — Single value visualization
Same data as L1S4 but displayed as **Single Value** with delta from previous day.  
![L1S5](./screenshots/Screenshot%202025-09-27%20135447.png)

---

### L1S6 — Geo distribution of products sold
```spl
index=web sourcetype=access_combined action=purchase status=200 sale_price=*
| iplocation clientip
| geostats count by product_name globallimit=0
```
Cluster map showing purchases by geolocation.  
![L1S6](./screenshots/Screenshot%202025-09-27%20140003.png)

---

### L1S7 — Retail sales by country with totals
```spl
index=sales sourcetype=vendor_sales
| stats count as "Retail Events" by VendorCountry
| appendpipe [ stats sum("Retail Events") as "Retail Events" | eval VendorCountry="Total" ]
```
Added a total row at the bottom.  
![L1S7](./screenshots/Screenshot%202025-09-27%20143752.png)

---

## Challenge Exercises

### LX1 — Trellis pie charts for proxy usage
```spl
index=network sourcetype=cisco_wsa_squid usage!=Business
| chart count over location by usage
```
Split by location → trellis pie charts (Boston, London, San Francisco).  
![LX1](./screenshots/Screenshot%202025-09-27%20142413.png)

---

### LX2 — Gauge visualization
```spl
index=security sourcetype=history_access Address_Description="San Francisco"
| dedup rfid
| stats count
```
Displayed as a filler gauge showing count of distinct RFID badges used.  
![LX2](./screenshots/Screenshot%202025-09-27%20150723.png)

---

### LX3 — Global gaming events map
```spl
index=games sourcetype=SimCubeBeta earliest=-30d@d latest=now
| iplocation user_ip
| stats count as Events by Country
| geom geo_countries featureIdField=Country
```
Choropleth map showing worldwide distribution of game events.  
![LX3](./screenshots/Screenshot%202025-09-27%20151659.png)

---

## Artifacts
- [Lab Guide PDF](./artifacts/Splunk%20lab4.pdf)  

---

## Lessons Learned
- **Field renaming** (e.g., retailSales vs. webSales) improves readability in charts.  
- **Trendlines** quickly show direction of metrics without overloading managers.  
- **Single Value & Gauge visualizations** highlight key figures at a glance.  
- **Maps** provide immediate context for geographic patterns of users or sales.  
- Trellis layouts are powerful for side-by-side regional comparisons.  

---

## Lessons Learned
This lab reinforced how visualization amplifies the value of search results. I learned how to:

- Use `timechart`, `trendline`, and `single-value` panels to highlight shifts and anomalies over time.  
- Rename technical fields into business-friendly labels so reports make sense outside the SOC.  
- Apply Trellis layouts and pie charts to split data by location or category for faster pattern recognition.  
- Leverage `iplocation`, `geostats`, and `geom` for mapping, turning raw IPs into geographic insights.  
- Balance detail and clarity—too much data confuses, but the right visualization points to action immediately.  

**Takeaway:** Effective SOC visualizations aren’t about fancy charts—they’re about making data readable in seconds. A good panel answers the core question fast, helps non-technical teams act, and leaves behind a reliable report for the next analyst on shift.  ---

## MITRE ATT&CK Mapping
These visualizations support detections in:  
- **T1078 – Valid Accounts**: Monitoring login failures over time (L1S3).  
- **T1190 – Exploit Public-Facing Application**: Purchase events could highlight abuse patterns in retail (L1S1–L1S2).  
- **T1071.001 – Application Layer Protocol: Web Protocols**: Web and proxy usage patterns (LX1).  
- **T1036 – Masquerading**: Geographic distribution checks can reveal anomalies in user logins (LX3).

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
