# Lab 02 — SQL Filtering for Security Analysis

[Portfolio](../../README.md) / [Web Applications & SQL](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Evidence & Results](#evidence--results) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I completed SQL query exercises using login-attempt and employee tables in a simulated organization. I selected records relevant to an investigation and scoped employee/device groups for maintenance. This is database filtering for analysis; application protection against SQL injection is a separate topic.

## Objectives

- Combine conditions with `AND`, `OR`, and `NOT`.
- Filter dates, times, department values, and text patterns.
- Explain how each condition selects the records needed for a task.

## Environment & Tools

- MariaDB course environment
- `log_in_attempts` and `employees` tables
- `SELECT`, `WHERE`, `LIKE`, and Boolean conditions

## What I Did

### 1. Retrieve failed logins after hours

```sql
SELECT *
FROM log_in_attempts
WHERE login_time > '18:00' AND success = FALSE;
```

Both conditions must hold: the attempt is after the specified time and it failed.

### 2. Review the two dates in the scenario

```sql
SELECT *
FROM log_in_attempts
WHERE login_date = '2022-05-09' OR login_date = '2022-05-08';
```

These dates belong to the supplied dataset, rather than the date I performed the exercise.

### 3. Select login records outside the dataset's Mexico labels

```sql
SELECT *
FROM log_in_attempts
WHERE NOT country LIKE 'MEX%';
```

The wildcard matches the stored values beginning with `MEX`. A country value is an investigation filter, not proof that a login is unauthorized. Null or inconsistent country data would need separate handling in an operational query.

### 4. Scope employee groups for maintenance

```sql
SELECT *
FROM employees
WHERE department = 'Marketing' AND office LIKE 'East%';

SELECT *
FROM employees
WHERE department = 'Finance' OR department = 'Sales';

SELECT *
FROM employees
WHERE NOT department = 'Information Technology';
```

I used department and office criteria to select the relevant employee/device records. The Finance and Sales departments are part of the fictional exercise.

## Evidence & Results

The original [Apply filters to SQL queries report](Apply%20filters%20to%20SQL%20queries%20exemplar.pdf) contains my query explanations and embedded MariaDB results for all six tasks. Its workplace-style narrative describes the training scenario.

## Lessons Learned

- Match each business or investigation question to explicit selection conditions.
- Check Boolean grouping when combining `AND` and `OR` in a larger query.
- Understand the source data's naming, time representation, and missing values before interpreting the results.
- SQL result filtering selects records. Prepared statements protect application query structure from untrusted input; they solve a different problem.

## Practical Value

This work demonstrates query reasoning, investigation scoping, and the ability to identify employee/device groups for IT maintenance without changing the underlying data.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
