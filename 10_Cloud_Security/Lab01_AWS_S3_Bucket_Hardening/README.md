# Lab01 - AWS S3 Bucket Hardening

## Objective
Secure a public S3 bucket by enforcing least privilege, encryption, and logging controls.

## Tools Used
- AWS Console & CLI
- AWS CloudTrail
- AWS Config

## Steps
1. Created an S3 bucket and enabled server-side encryption with SSE-S3.
2. Configured bucket policies to allow only specific IAM roles.
3. Enabled access logging and versioning for auditability.
4. Validated compliance with AWS Config rules.

## Findings
- Misconfigured public access settings expose data if not restricted.
- Centralized logging and versioning support incident investigations.

## References
- [AWS S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
