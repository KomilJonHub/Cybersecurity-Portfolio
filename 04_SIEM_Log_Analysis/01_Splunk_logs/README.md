# Lab 01 — Splunk: Using Fields and Search-Time Extractions

[Portfolio](../../README.md) / [SIEM & Log Analysis](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Evidence & Results](#evidence--results) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I completed this Splunk Education lab using the fictional **Buttercup Games** dataset. I explored web-event fields, searched Linux authentication failures, formatted a checkout-error report, and compared example-driven extraction with explicit regular expressions. The work demonstrates how I check field coverage and turn raw events into readable reports.

The lab environment also supplies email, proxy, and firewall data. The completed tasks below focus on web and Linux authentication events.

## Objectives

- Compare field presence, missing values, and purchase/non-purchase searches.
- Find failed authentication events associated with admin usernames.
- Format checkout errors with readable field labels.
- Compare `erex` and `rex` extractions and validate the resulting counts.

## Environment & Tools

- **Splunk Enterprise** — Search & Reporting in the education lab
- **Web data:** `index=web sourcetype=access_combined`
- **Authentication data:** `index=security sourcetype=linux_secure`
- **Course guide:** [Using Fields lab instructions](artifacts/Splunk%201%20lab%20instructions.pdf)

## What I Did

The SPL snippets describe the method. The original PDF exports and screenshots retain the actual historical results and selected time windows.

### L1S1 — Compare Field Values and Field Presence

I explored `action`, `sale_price`, and `categoryId` in web events. I compared events with and without an `action` value and tested purchase/non-purchase conditions before saving the report.

```spl
index=web sourcetype=access_combined earliest=-1d@d latest=@d
| stats count by action
```

This summary counts events with an `action` value. To check missing values separately, I used `NOT action=*`; `action!=purchase` only returns events where `action` exists with another value.

- [Original L1S1 report export](artifacts/L1S1-2025-09-23.pdf)
- Purchase search and field exploration:

![Purchase-event search with the fields sidebar](screenshots/Screenshot%202025-09-23%20153647.png)
![categoryId values inspected during purchase-event exploration](screenshots/Screenshot%202025-09-23%20154425.png)

### L1S2 — Find Failed Admin Authentication Events

I searched a last-60-minute window for failed logins involving invalid admin usernames, then retained fields useful for reviewing the user and source.

```spl
index=security sourcetype=linux_secure earliest=-60m@m latest=now
failed invalid user=admin*
| fields user src_ip app
```

The saved report contains repeated failed authentication events from several sources. Those events are investigation leads; a count of failures alone does not establish a successful compromise.

- [Original L1S2 report export](artifacts/L1S2-2025-09-23.pdf)

![Saved L1S2 authentication-failure report](screenshots/Screenshot%202025-09-23%20162114.png)
![L1S2 search and selected authentication fields](screenshots/Screenshot%202025-09-23%20162130.png)

### L1S3 — Format Checkout Errors for Review

I filtered purchase events with HTTP status codes above 399, selected the fields needed for follow-up, and renamed the columns.

```spl
index=web sourcetype=access_combined action=purchase status>399
| table clientip host status
| rename clientip AS "Customer IP" host AS "Web Server" status AS "HTTP Status"
```

The guide requests a last-four-hour window; the screenshot records a last-60-minute view, while the later PDF export contains a different result count. Keeping the time window visible helps explain why the outputs differ.

- [Original L1S3 report export](artifacts/L1S3-2025-09-23.pdf)

![L1S3 checkout-error table with renamed columns](screenshots/Screenshot%202025-09-23%20162644.png)

The historical output labels the client address **Customer ID**; the clarified example above uses **Customer IP** to describe the field precisely.

### L2S1 — Explore Example-Driven Extraction with `erex`

I extracted `event_description` from authentication messages using example phrases and compared the resulting counts. A representative search is:

```spl
index=security sourcetype=linux_secure port
| erex event_description examples="Accepted password,Failed password"
| stats count(src_port) by event_description
```

The [original L2S1 report](artifacts/L2S1-2025-09-23.pdf) records accepted/failed password counts and zero `src_port` counts for two other message categories. That prompted a closer look at which fields were actually available in those events.

### L2S2 — Review and Use Explicit Extraction with `rex`

I added a `port` extraction, reviewed Splunk's generated regular expression through the Job messages, and used `rex` for the follow-up report. The [original L2S2 report](artifacts/L2S2-2025-09-23.pdf) retains counts for all four message categories, including **Received disconnect** and **Server listening**.

A simplified extraction pattern illustrates the approach:

```spl
index=security sourcetype=linux_secure port
| rex field=_raw "(?<event_description>Accepted password|Failed password|Received disconnect|Server listening)"
| rex field=_raw "port (?<port>\d+)"
| stats count(port) by event_description
```

The course guide explains the extraction progression. [Splunk's `erex` reference](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/erex) documents the command syntax and how to review the generated regex. A `rex` command inside a search remains search-time extraction; reusable automatic field extraction requires a saved knowledge-object configuration.

## Evidence & Results

| Exercise | Published result |
|---|---|
| L1S1 | Original event export plus purchase/field-exploration screenshots |
| L1S2 | Authentication-failure report and matching search/report screenshots |
| L1S3 | Checkout-error report and matching renamed-column screenshot |
| L2S1 | PDF export of counts using the initial extraction |
| L2S2 | PDF export showing the revised port counts |

## Lessons Learned

- Field presence, `!=`, and `NOT` have different effects on missing values.
- Inspecting raw events helps explain a missing or zero field count.
- Time windows must be recorded when comparing saved output with screenshots.
- Readable labels make a report more useful for technical follow-up.
- Example-driven extraction is a starting point; explicit regex and result checks make its behavior easier to explain.

## Practical Value

This lab gave me practice troubleshooting data coverage, reviewing authentication activity, and documenting searches another person can understand and repeat in the same lab environment.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
