Objective:
This assessment is designed to evaluate your practical data engineering skills, specifically:

Cost-aware decision making
Backup automation
Data lake design for analytics
Ability to execute safely on AWS without incurring cost
Important Rules (Read Carefully)
You must use AWS, but must not incur any cost
Any billable AWS resource = automatic rejection

Not Allowed
RDS
EC2
DMS
Glue Jobs
NAT Gateway
QuickSight

Any managed database or compute service
Allowed (Safe / Near-Zero Cost)
S3 (≤ 100 MB total data)
IAM
Athena (queries must scan only KBs/MBs)
AWS CLI
Local execution (Postgres / Python / Bash)
Scenario
You are working on a SaaS platform with:
A production PostgreSQL database
Reporting and analytics needs
Compliance requirement to retain data for 30–90 days
Strong pressure to minimise cloud cost
Your task is to design and execute a cost-efficient backup and data lake solution.
Part 1 – Cost Analysis (Decision Making)
Task
Assume:
Database size: 100 GB
Growth: 2 GB per day
Explain (in Markdown or PDF):
At least 2 different approaches for:
Backups
Retention
Restore
Compare them on:
Cost
Restore speed
Operational complexity
Clearly state:
Which approach is cheapest long-term
Which is fastest to restore
Which you recommend and why
No calculations need to be perfect — reasoning matters.
Part 2 – Backup Automation (Execution Required)
Task
Implement a real automated backup flow.
Requirements
Use a local PostgreSQL or SQLite database
Take a backup (e.g. pg_dump)
Compress it
Upload it to S3
Organise backups by date
Implement a retention policy (delete or archive old backups)
Example S3 structure:
s3://<your-bucket>/backups/postgres/2025/01/10/backup.sql.gz
Deliverables
Script (Bash / Python)
README explaining:
How it runs
How retention works
Cost considerations
Part 3 – Data Lake Design (Execution Required)
Task
Design and execute a simple data lake.
Requirements
Generate sample data locally (CSV or Parquet)
Upload to S3 using an analytics-friendly structure
Use partitions (date-based preferred)
Make it queryable via Athena
Example:
s3://<your-bucket>/datalake/orders/year=2025/month=01/day=10/
Athena Rules
Queries must scan only KBs or MBs
Partition filters are mandatory
Mandatory Cleanup (CRITICAL)
You must delete everything after execution.
Required proof:
AWS CLI cleanup commands
Screenshot of AWS Billing page showing $0 cost
Example:
aws s3 rm s3://<your-bucket> --recursive
aws s3 rb s3://<your-bucket>
Missing cleanup proof = submission rejected.
Submission Requirements
Submit one ZIP or GitHub repo containing:
README.md (mandatory)
Cost analysis document
Scripts used
Screenshots (Athena, S3, billing)
Optional: diagram