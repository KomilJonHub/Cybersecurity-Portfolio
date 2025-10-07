# Lab04_File_Permissions

> Update Linux file and directory permissions to enforce proper access controls.

## Objective
Ensure project files and directories have appropriate permissions to match organizational authorization policies.

## Commands Used
```bash
ls -la
chmod o-w project_k.txt
chmod u-w,g-w,g+r .project_x.txt
chmod g-x drafts
```

## Security Outcomes
- Reviewed existing permissions to understand user, group, and other access.
- Removed write access from `project_k.txt` for unauthorized users.
- Adjusted `.project_x.txt` so only user and group have read permissions.
- Restricted execute access on the `drafts/` directory to `researcher2`.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
