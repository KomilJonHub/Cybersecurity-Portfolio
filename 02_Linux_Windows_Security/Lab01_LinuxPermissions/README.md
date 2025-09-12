 Filesystem Permissions Lab

Lab Name: Navigating the Linux Filesystem and Permission SettingsModule: 154  Lab ID: GLAB 154.8.6Platform: Ubuntu VM (VirtualBox)Date Completed: August 3, 2025

 Objective

Gain hands-on experience navigating Linux filesystems, mounting/unmounting partitions, modifying file permissions and ownership, and creating symbolic and hard links. These skills are essential for system administrators, cybersecurity analysts, and penetration testers.

 Tools & Commands Used

lsblk, mount, umount

mkdir, ls -l, cd

chmod, chown, touch, echo, cat

ln, ln -s, mv

 Lab Walkthrough

 1. Checking Available Block Devices

I began by inspecting the available block devices on my VM using:

lsblk

This showed the disk layout of my system, including sda1, sda2, and an unmounted external partition /dev/sdb1.

To confirm the filesystem and mount points, I ran:

mount | grep /dev/sd

This helped ensure I was working with the correct partition before mounting.

 2. Navigating the Filesystem

To explore the root directory structure, I used:

cd /
ls -l

This displayed all directories and their permissions, owners, and groups—helpful for understanding default access settings.

 3. Mounting a Partition

I created a new mount point:

mkdir ~/second_drive

Then I mounted /dev/sdb1 into that directory:

sudo mount /dev/sdb1 ~/second_drive/

After mounting, I listed the contents of the folder and confirmed that a file named myFile.txt existed.

To confirm the mount:

mount | grep /dev/sdb1

 4. Unmounting the Partition

To remove the mounted partition, I ran:

sudo umount /dev/sdb1

Then I verified the contents of ~/second_drive again, which were now empty—confirming a successful unmount.

 5. Permission Denied Test

I attempted to create a file in /mnt:

touch /mnt/myNewFile.txt

This returned a "Permission denied" error. I used:

ls -ld /mnt

to inspect the directory permissions. The issue was due to lack of write permission for my user in /mnt.

 6. Changing Permissions with chmod

I attempted to change the permissions of myFile.txt to rw-rw-r-- using:

sudo chmod 665 myFile.txt

However, the change didn’t reflect properly—likely due to the file being on a mounted filesystem with specific mount options.

 7. Changing Ownership with chown

Next, I changed ownership of the file to my user account:

sudo chown analyst myFile.txt

Then I successfully appended content using:

echo "test" >> myFile.txt

And verified it with:

cat myFile.txt

This reinforced that file ownership is more critical than permission bits in some mount scenarios.

 8. Creating Symbolic and Hard Links

I created two types of links to test the differences:

ln -s file1.txt file1symbolic
ln file2.txt file2hard

Then, I renamed the original files:

mv file1.txt file1new.txt

Attempting to open the symbolic link failed:

cat file1symbolic  # Error

But the hard link worked:

cat file2hard  # Success

This illustrated that symbolic links point to filenames (and break if renamed), while hard links point to actual data blocks and remain functional.

 Screenshots

Screenshots for each step are available in the screenshots/ folder. Each demonstrates the terminal output of the commands listed above.

 Key Takeaways

lsblk and mount are essential for identifying disks and mount points.

File permissions (chmod) and ownership (chown) must be managed carefully, especially on mounted filesystems.

Symbolic links break if the original file is renamed; hard links don’t.

Linux access control combines directory permissions, ownership, and user roles.


Lab Source: Per Scholas Cybersecurity ProgramLab Reference: GLAB 154.8.6
