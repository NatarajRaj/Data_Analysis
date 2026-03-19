# 📦 Data Engineering Assignment – Backup Automation

## 🧠 Overview

This project implements a **cost-efficient and automated backup pipeline** for a PostgreSQL database using local execution and AWS S3.

The solution focuses on:

* Low-cost design (no paid AWS services)
* Automation of backup process
* Organized storage in S3
* Email alerts for backup success and failure
* Retention using lifecycle policies

---

## ⚙️ Architecture

```text
Local PostgreSQL → pg_dump → gzip → AWS S3 → Lifecycle Retention(30 days)
```

---

## 🔄 Workflow

### 1. Data Generation (10:00 PM Daily)

* A Python script (`generate_retail_data.py`) generates ~100,000 records daily.
* Simulates real-time data ingestion into PostgreSQL.

### 2. Backup Process (2:00 AM Daily)

* A Bash script (`backup.sh`) performs:

  * Full database backup using `pg_dump`
  * Compression using `gzip`
* Upload to AWS S3
* Sends a status email after the run completes or fails

---

## 🗂️ S3 Storage Structure

Backups are organized using a date-based structure:

```
s3://natarajan-de-2026-bucket-1/backups/postgres/YYYY/MM/DD/backup_timestamp.sql.gz
```

Example:

```
s3://natarajan-de-2026-bucket-1/backups/postgres/2026/03/18/backup_175916.sql.gz
```

---

## 🛠️ Technologies Used

* PostgreSQL (Local database)
* Python (Data generation)
* Bash (Backup automation)
* AWS S3 (Storage)
* AWS CLI (Upload)
* Windows Task Scheduler (Automation)

---

## 🚀 How It Runs

### Step 1: Configure Environment

Create a `config.env` file:

```
DB_HOST=localhost
DB_NAME=data_analytics
DB_USER=postgres
DB_PASSWORD=******
S3_BUCKET=natarajan-de-2026-bucket-1
AWS_REGION=ap-south-2
EMAIL=alerts@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=alerts@example.com
SMTP_PASSWORD=app-password
SMTP_FROM=alerts@example.com
SMTP_USE_TLS=true
```

`EMAIL` is the alert recipient. The SMTP settings are used by `send_email.py` to send success and failure notifications.

---

### Step 2: Run Full Automation (Recommended)

Run the shell script to create and upload the backup:

```bash
& "C:\Program Files\Git\bin\bash.exe" .\backup.sh
# ./backup.sh
```

---

### Step 3: Run Data Generation Only (Optional)

```bash
py generate_retail_data.py
```

---

### Step 4: Run Backup Script Only (Optional)

```bash
& "C:\Program Files\Git\bin\bash.exe" .\backup.sh
# ./backup.sh
```

---

### Step 5: Automation

Using Windows Task Scheduler:

| Task            | Time     |
| --------------- | -------- |
| Data Generation | 10:00 PM |
| Backup Job      | 2:00 AM  |

---

## 🧹 Retention Strategy

Retention is implemented using **S3 Lifecycle Policy**:

* Backups older than **30 days are automatically deleted**
* No manual cleanup required

This ensures:

* Cost optimization
* Compliance with data retention requirements

### Lifecycle Rule Proof

Example lifecycle configuration for deleting old backups after 30 days:

```json
{
  "Rules": [
    {
      "ID": "DeleteOldBackupsAfter30Days",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "backups/postgres/"
      },
      "Expiration": {
        "Days": 30
      }
    }
  ]
}
```

Example AWS CLI command used to apply the rule:

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket natarajan-de-2026-bucket-1 \
  --lifecycle-configuration file://lifecycle.json
```

---

## 💰 Cost Considerations

The solution is designed to minimize AWS costs:

* Uses only **S3 (≤100 MB)** → within free tier
* No EC2, RDS, or Glue jobs used
* Athena not used in this part
* Compression reduces storage size
* Lifecycle policy prevents storage accumulation

---

## 🔐 Security Best Practices

* No credentials hardcoded in scripts
* AWS access managed via `aws configure`
* Config stored in environment file (`config.env`)
* Sensitive data excluded from version control

---

## 📌 Key Design Decisions

| Feature     | Decision               |
| ----------- | ---------------------- |
| Backup Type | Full backup (pg_dump)  |
| Compression | gzip                   |
| Storage     | AWS S3                 |
| Retention   | S3 Lifecycle           |
| Automation  | Task Scheduler         |
| Data Volume | Simulated (cost-aware) |

---

## ✅ Outcome

* Fully automated backup pipeline
* Organized and query-ready storage
* Zero-cost AWS usage
* Production-like design

---

## 📎 Future Enhancements

* Incremental backups
* Monitoring & alerting (SNS/Email)
* Data lake + Athena integration
* CI/CD pipeline integration

---

## 🎯 Conclusion

This solution demonstrates a **scalable, cost-efficient, and production-ready backup system**, aligning with modern data engineering best practices while adhering strictly to zero-cost constraints.
