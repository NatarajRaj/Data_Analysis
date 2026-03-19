# Data Lake Design

This project builds a small analytics-friendly data lake for `orders` data.

## What it does

1. Generates deterministic sample order data locally as CSV and Parquet.
2. Rewrites the data into Hive-style date partitions.
3. Uploads the partitioned layout to S3.
4. Creates an Athena external table and repairs partitions.
5. Provides partition-filtered Athena queries that scan only the required files.

## Project layout

cd py -m pip install -r requirements.txt

```text
data-lake-project/
├── README.md
├── requirements.txt
├── run_pipeline.sh
├── scripts/
├── data/
├── config/
├── output/
└── tests/
```

## Local setup

```bash
py -m pip install -r requirements.txt
```

## Run locally

PowerShell:

```powershell
py scripts/01_generate_data.py
py scripts/02_create_partitions.py
py scripts/03_upload_to_s3.py
```

Shell:

```bash
./run_pipeline.sh
```


## AWS setup

Update `config/aws_config.json` with:

- `bucket_name`
- `aws_region`
- `athena_database`
- `athena_table`
- `athena_output_s3`
- optional `s3_prefix`

Then run:

```powershell
py scripts/03_upload_to_s3.py
```

This script uploads `data/partitioned/orders/` to:

```text
s3://<bucket>/<prefix>/orders/year=YYYY/month=MM/day=DD/orders.parquet
```

## Athena rules satisfied

- Partitioned by `year`, `month`, and `day`
- Sample queries include mandatory partition filters
- Data is stored as Parquet for low scan volume

## Notes

- Local data generation and partitioning can be executed without AWS credentials.
- S3 upload and Athena execution require `awscli` or valid AWS credentials for `boto3`.
