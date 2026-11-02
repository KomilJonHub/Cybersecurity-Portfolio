# Contributing

This is a **personal IT and cybersecurity portfolio**. External contributions are **not accepted**.

## How to Provide Feedback
- Open a GitHub **Issue** with:
  - File/section (path)
  - What is inaccurate or risky
  - Proposed fix (one sentence)
  - Links/evidence

Or contact me on **LinkedIn**: https://www.linkedin.com/in/komiljon-karimov

## Pull Requests
PRs from non-invited contributors will be **closed**. If I invite a PR, you agree that:
- You wrote the content or have rights to it.
- Your contribution is licensed under the repository **Portfolio License**.
- No sensitive or proprietary data.

## Style (for invited edits)

Use the [lab README guide](.github/LAB_README_TEMPLATE.md) and preserve the existing visual identity.
- Use clear, active sentences. Include the detail needed to explain the work.
- Each lab README: overview • objectives • environment • actions • evidence/results • lessons and practical value. Adapt the sections to the actual work.
- Filenames: `LabXX_Title/README.md` with a `screenshots/` subfolder.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity

## Validation

From the repository root, run `python scripts/check_portfolio.py` to check local links, anchors, README reachability, titles, and standard footers. Then run the safe project tests:

```bash
cd 07_Scripting_Automation/Python/Keylogger
python -m unittest discover -s tests -v
```

GitHub Actions runs both checks on pushes and pull requests. External credential verification remains separate because blocked access is not proof of a broken destination.
