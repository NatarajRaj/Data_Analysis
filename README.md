# Data Engineering Assignment

This repository contains all four parts of the assignment:

1. Cost analysis and decision-making
2. Backup automation with PostgreSQL and S3
3. Data lake design with partitioned data and Athena
4. Cleanup proof and billing proof

## Repository Structure

### Part 1: Cost Analysis

Folder: `1_Cost Analysis`

Contents:

- backup strategy comparison
- retention and restore options
- recommendation based on cost, speed, and operational complexity

Main file:

- `1_Cost Analysis/README.md`

### Part 2: Backup Automation

Folder: `2_Backup_Automation`

Contents:

- `generate_retail_data.py` to create sample retail data in PostgreSQL
- `backup.sh` to take a PostgreSQL backup, compress it, and upload it to S3
- documentation for execution, retention, and cost considerations

Main file:

- `2_Backup_Automation/README.md`

Example command:

```powershell
& "C:\Program Files\Git\bin\bash.exe" .\2_Backup_Automation\backup.sh
```

### Part 3: Data Lake Design

Folder: `3_Data Lake Design/data-lake-project`

Contents:

- local sample data generation
- partitioned Parquet dataset
- S3 upload
- Athena-ready table and queries

Main file:

- `3_Data Lake Design/data-lake-project/README.md`

### Part 4: Cleanup Process

Folder: `4_Cleanup Process`

Contents:

- AWS CLI cleanup proof
- AWS billing screenshot showing zero cost

Main file:

- `4_Cleanup Process/README.md`

## Submission Checklist

- `README.md` at repository root
- Part 1 cost analysis
- Part 2 backup automation scripts and documentation
- Part 3 data lake scripts and Athena proof
- Part 4 cleanup proof and billing screenshot

## Notes

- Local config files, logs, installers, and other machine-specific artifacts should not be committed.
- AWS credentials are expected to be configured locally and are not stored in this repository.
