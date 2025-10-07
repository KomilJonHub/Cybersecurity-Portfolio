# Lab 08 — Splunk: Leveraging Lookups and Subsearches

In this lab I used **lookups** and **subsearches** to enrich raw logs, tighten my searches, and ship results that non-technical teams can act on. I verified lookup contents, joined context into events, saved a curated dataset back to a CSV lookup, drew a revenue map, and filtered product activity with a lookup-driven subsearch.


## Objectives

- Validate and use file-based lookups with `inputlookup` and `lookup`.
- Normalize field names during joins (`AS`, `OUTPUT`) and keep output readable with `table`.
- Persist results with `outputlookup` for dashboards and follow-on hunts.
- Use subsearches to **constrain** the outer search to a business list (e.g., multiplayer titles).
- Present answers in the shortest possible path for Security, Sales, and IT Ops.

---

## Environment & Data

- **Splunk Enterprise** → *Search & Reporting*
- **Indexes:** `web`, `network`, `sales`
- **Lookups:**  
  - `status_definitions.csv` — HTTP status → description, type  
  - `knownusers.csv` — username → user, dept  
  - `mp_products.csv` — multiplayer product list  
  - `canada_prov` — province geometry for choropleth

---

## What I Did

### L1S1 — Sanity-check the HTTP status dictionary

**Scenario.** Before enriching logs, I verified the `status_definitions.csv` contents.

**SPL**
```spl
| inputlookup status_definitions.csv
```

**Result.** Full dictionary of `status`, `status_description`, `status_type`.  
![L1S1](./screenshots/Screenshot%202025-10-04%20214841.png)

**Why it matters.** Trust the lookup first, then depend on it in joins.

---

### L1S2 — Enrich non-200 responses with readable status and type

**Scenario.** Ops wanted a breakdown of **client vs server errors** per web host.

**SPL**
```spl
index=web sourcetype=access_* status!=200
| lookup status_definitions.csv status OUTPUT status_description status_type
| stats count by host status_description status_type
```

**Result.** Clear counts per `host`, with human-readable reasons.  
![L1S2](./screenshots/Screenshot%202025-10-04%20220234.png)

**Takeaways.**
- Enrichment turns cryptic codes into categories teams can act on.
- Keep the table simple: `host`, `status_description`, `status_type`, `count`.

---

### L1S3 — Who accessed “Uncategorized URLs” on the proxy?

**Scenario.** SecOps asked for users and departments hitting **Uncategorized URLs** in the last 24h, with HTTP context.

**SPL**
```spl
index=network sourcetype=cisco_wsa_squid x_webcat_code_full="Uncategorized URLs"
| lookup knownusers.csv user AS username OUTPUT user dept
| lookup status_definitions.csv status OUTPUT status_description
| search user=*
| table user dept cs_url status status_description
```

**Result.** Named users, their departments, the URLs, and status.  
![L1S3](./screenshots/Screenshot%202025-10-04%20233931.png)

**Takeaways.**
- Use `AS` to align mismatched keys (`username` → `user`) during the join.
- Chain lookups safely; keep the final projection tight with `table`.

---

### L1S4 — Map Canadian revenue by province in CAD

**Scenario.** Sales wanted a **map** of last week’s Canadian revenue in **CAD**.

**SPL**
```spl
index=sales sourcetype=vendor_sales VendorCountry=Canada
| stats sum(price) AS USDollars BY VendorStateProvince
| eval CDNDollars=round(USDollars*1.31,2)
| fields - USDollars
| geom canada_prov featureIdField=VendorStateProvince
```

**Result.** Choropleth showing provincial revenue; Ontario dominates.  
![L1S4](./screenshots/Screenshot%202025-10-04%20234813.png)

**Takeaways.**
- `geom … featureIdField=` binds your stats to a geography lookup.
- Convert currency before drawing so legends match business units.

---

### L1S5 — Curate recent web errors into a reusable lookup

**Scenario.** Create a lightweight evidence set of **erroring clients** and associated hosts/statuses, and save it for dashboards.

**SPL**
```spl
index=web sourcetype=access_combined status!=200 referer_domain="http://www.buttercupgames.com"
| lookup status_definitions.csv status OUTPUT status_description status_type
| stats count by clientip host status_description status_type
| stats list(status_description) AS status_description list(status_type) AS status_type \
        list(host) AS host sum(count) AS count BY clientip
| outputlookup BCG_web_server_errors.csv
```

**Result.** New lookup `BCG_web_server_errors.csv` written to app context.  
![L1S5](./screenshots/Screenshot%202025-10-04%20235149.png)

**Takeaways.**
- `outputlookup` converts a one-off hunt into a data asset other teams can reuse.
- Rolling this into a dashboard panel is a trivial next step.

---

### L2S1 — Subsearch: only multiplayer titles during the event window

**Scenario.** Marketing asked, “Which **multiplayer** games were viewed most during the weekend promo?”

**Idea.** Use a subsearch to produce a product allow-list; the outer search counts views only for those titles in the target window.

**SPL**
```spl
index=web sourcetype=access_combined action="view" earliest=@w6 latest=@w7
    [ | inputlookup mp_products.csv
      | fields product_name
      | format ]
| stats count(action) AS viewed BY product_name
| sort -viewed
```

**Result.** Ranked list of multiplayer titles by views.  
![L2S1](./screenshots/Screenshot%202025-10-05%20152145.png)

**Takeaways.**
- `format` turns rows into a valid OR-filter block for the outer search.
- Keep the subsearch small and surgical; let the outer search do the work.

---

## Saved Reports Index

| ID   | Purpose                                                     | Screenshot |
|------|-------------------------------------------------------------|------------|
| L1S1 | Inspect HTTP status lookup contents                         | `Screenshot 2025-10-04 214841.png` |
| L1S2 | Enrich non-200 responses and count by host + type           | `Screenshot 2025-10-04 220234.png` |
| L1S3 | Known users hitting Uncategorized URLs (user + dept + URL)  | `Screenshot 2025-10-04 233931.png` |
| L1S4 | Choropleth map of Canada revenue in CAD                     | `Screenshot 2025-10-04 234813.png` |
| L1S5 | Persist curated web error dataset via `outputlookup`        | `Screenshot 2025-10-04 235149.png` |
| L2S1 | Subsearch-filtered multiplayer views during event window    | `Screenshot 2025-10-05 152145.png` |

---

## Lessons Learned

- **Trust, then join.** `inputlookup` first; never assume lookup shape.
- **Align names early.** `AS` and `OUTPUT` avoid messy downstream renames.
- **Persist value.** `outputlookup` is the fastest path from hunt → dashboard.
- **Subsearch = scope.** Use it to define *who/what*, then measure in the outer search.
- **Table the story.** `table` and concise labels reduce cognitive load for stakeholders.

---

## Personal Reflection

Lookups felt like bridges—connecting logs to the language teams already use. I kept joins explicit, fixed field names at the edge, and saved good slices as reusable CSVs. Subsearches acted like a scalpel: small, precise, and perfect for scoping the audience before counting anything. If Sales or Security can answer their question from a single table or map without extra explanation, I did my job well.

---

## MITRE ATT&CK Mapping

This lab builds **enrichment and scoping** capabilities that support detections rather than targeting a single technique. Relevant surfaces:

- **Data Sources:** Web server, Web proxy, Application, Authentication
- **Supports work against:** Initial Access, Command and Control, Exfiltration patterns via web activity baselining and error analysis

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
