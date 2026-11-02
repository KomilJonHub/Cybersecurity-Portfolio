# Lab 01 — Linux Filesystem Permissions

[Portfolio](../../README.md) / [Linux & Windows Security](../README.md)

[Overview](#overview) · [Objectives](#objectives) · [Environment & Tools](#environment--tools) · [What I Did](#what-i-did) · [Evidence & Results](#evidence--results) · [Lessons Learned](#lessons-learned) · [Practical Value](#practical-value)

## Overview

I used an Ubuntu VM to investigate mounted storage, diagnose a permission error, change file ownership and mode bits, and compare symbolic and hard links. The exercise connects everyday filesystem troubleshooting with appropriate access.

## Objectives

- Check block devices and mounts before working with their contents.
- Explain access using ownership, directory permissions, and file mode bits.
- Verify how different link types behave when a target is renamed.

## Environment & Tools

- Ubuntu virtual machine
- `lsblk`, `mount`, `umount`, `ls`, `chmod`, `chown`, `ln`, and `mv`

## What I Did

1. **Enumerated devices and mounted filesystems.**
   ```bash
   lsblk
   mount | grep sda2
   ```
   I identified the root filesystem and the additional `/dev/sdb1` device in the lab.

2. **Mounted and unmounted the additional filesystem.**
   ```bash
   sudo mount /dev/sdb1 ~/second_drive/
   ls -l ~/second_drive/
   sudo umount /dev/sdb1
   ls -l ~/second_drive/
   ```
   The listing showed the mounted filesystem's contents, then an empty mount-point directory after unmounting. The lab's `second_drive` directory was already present.

3. **Investigated a permission error.**
   Creating `/mnt/myNewFile.txt` failed. I used `ls -ld /mnt` to check the root-owned directory and its mode before deciding what access was appropriate.

4. **Changed file permissions and ownership.**
   ```bash
   sudo chmod 665 myFile.txt
   sudo chown analyst myFile.txt
   ```
   The screenshots show mode `665` (`rw-rw-r-x`), followed by an ownership change and a successful append/read check. This was a permission-bit exercise; granting others execute access is not a suitable default for a text file. Ownership and the applicable permission class need to be considered together.

5. **Compared symbolic and hard links.**
   ```bash
   ln -s file1.txt file1symbolic
   ln file2.txt file2hard
   mv file1.txt file1new.txt
   mv file2.txt file2new.txt
   ```
   Renaming the symbolic link's target left its stored path unresolved. The hard link still accessed its inode after the other filename was changed. Renaming a symbolic link itself does not necessarily break it; the path it contains and its location determine resolution.

## Evidence & Results

| Evidence | What it shows |
|---|---|
| [Images 1–2](screenshots/image1.png) | Device and root-filesystem checks; [root directory listing](screenshots/image2.png) |
| [Images 3–4](screenshots/image3.png) | Mounted contents and [empty mount point after unmounting](screenshots/image4.png) |
| [Image 5](screenshots/image5.png) | Permission denied when creating a file in `/mnt`, followed by a directory-permission check |
| [Images 6–7](screenshots/image6.png) | Mode-bit change and [ownership/append verification](screenshots/image7.png) |
| [Images 8–9](screenshots/image8.png) | Link creation and [behavior after target renames](screenshots/image9.png) |

The complete original sequence remains in [`screenshots/`](screenshots/).

## Lessons Learned

- Confirm the filesystem mounted at a path before interpreting an empty directory as lost data.
- Diagnose access from the directory, owner/group membership, and applicable mode bits rather than guessing from a failed command.
- Hard links reference an inode; symbolic links store a path that can become stale when its target moves.

## Practical Value

This exercise demonstrates storage checks, permission troubleshooting, and verification of file operations—useful habits in desktop support and Linux administration.

## MITRE ATT&CK Context

[T1222 — File and Directory Permissions Modification](https://attack.mitre.org/techniques/T1222/) provides adversarial context for reviewing unexpected permission changes. My work here was authorized administration in a lab.

<p align="center"><img src="../../divider_wave.svg" alt="" width="100%" /></p>

> **Author:** Komiljon Karimov<br>
> **Mission:** Reliable technology and informed security decisions

[Back to portfolio](../../README.md) · [Domain index](../README.md)
