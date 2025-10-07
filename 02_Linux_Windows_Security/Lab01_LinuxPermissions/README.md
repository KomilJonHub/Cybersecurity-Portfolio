# Lab 01: Linux Filesystem Permissions

> Practical exploration of mounting devices, adjusting permissions and ownership, and working with links on Ubuntu.

## Objective
Gain hands-on experience navigating the Linux filesystem, managing mounts, and modifying permissions and ownership.

## Environment
- Ubuntu virtual machine
- Commands: `lsblk`, `mount`, `umount`, `chmod`, `chown`, `ln`

## Key Steps
1. **Enumerate block devices**
   ```bash
   lsblk
   mount | grep /dev/sd
   ```
   Confirmed `/dev/sdb1` was available for mounting.

2. **Mount and unmount a partition**
   ```bash
   mkdir ~/second_drive
   sudo mount /dev/sdb1 ~/second_drive
   sudo umount /dev/sdb1
   ```
   Verified file availability before and after unmounting.

3. **Investigate permission issues**
   - Attempted to create a file in `/mnt` and received a permission error.
   - Used `ls -ld /mnt` to review directory permissions.

4. **Modify permissions and ownership**
   ```bash
   sudo chmod 664 myFile.txt
   sudo chown analyst myFile.txt
   ```
   Demonstrated the effect of permission bits versus ownership.

5. **Create symbolic and hard links**
   ```bash
   ln -s file1.txt file1symbolic
   ln file2.txt file2hard
   mv file1.txt file1new.txt
   ```
   Observed that renaming broke the symbolic link but the hard link remained functional.

## Screenshots
Reference images in the [`screenshots/`](./screenshots/) directory.

## MITRE ATT&CK Mapping
- [T1222: File and Directory Permissions Modification](https://attack.mitre.org/techniques/T1222/)

## Lessons Learned
- Block devices and mount points must be verified before use.
- Ownership often determines access more than raw permission bits.
- Hard links survive file renames; symbolic links do not.

---

> **Author:** Komiljon Karimov  
> **Mission:** Upskilling into Cybersecurity
