# Lab 04 — Linux File Permissions and Access Control

[Portfolio](../../README.md) / [Linux & Windows Security](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Evidence & Results](#evidence--results) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I completed a course-based permissions exercise for a fictional research team. I inspected project files, including a hidden archive, then changed file and directory modes to match the scenario's authorization requirements.

## Objectives

- Read owner, group, and other permission bits using a detailed listing.
- Remove inappropriate write access and preserve required read access.
- Verify directory traversal permissions after a targeted change.

## Environment & Tools

- Linux course environment using the `researcher2` account and `research_team` group
- `ls -la` and symbolic-mode `chmod`

## What I Did

```bash
ls -la
chmod o-w project_k.txt
chmod u-w,g-w,g+r .project_x.txt
chmod g-x drafts
ls -la
```

- I removed **other write** access from `project_k.txt`.
- I removed owner/group write and added group read for `.project_x.txt`. The resulting listing shows `r--r-----`: owner and group can read, while others have no access.
- I removed group execute/search permission from `drafts`. Its existing owner permissions and lack of other permissions combine with that change to produce `drwx------` in the captured listing, leaving ordinary traversal access with `researcher2`.

For a directory, execute permission controls searching/traversing it. The command `chmod g-x` changes only the group execute bit; the complete final listing establishes the resulting access rather than the command alone.

## Evidence & Results

The original [File permissions in Linux report](File%20permissions%20in%20Linux.pdf) contains my commands, captured listings, permission-string explanation, and summary. Pages 3–4 show the hidden-file and directory results. Its organizational language belongs to the course scenario.

## Lessons Learned

- A leading dot hides a filename from a default listing; it does not protect the file's contents.
- Use a full listing to check the existing state before and after each change.
- File read/write permissions and directory traversal permissions serve different purposes.
- Least privilege requires checking all applicable access classes and relevant parent directories, with ACLs and privileged access considered where present.

## Practical Value

This exercise demonstrates methodical local access review and the ability to explain a permissions change in terms another technician can verify.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
