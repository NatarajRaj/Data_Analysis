from __future__ import annotations

from pathlib import Path
import json

import boto3
from botocore.exceptions import ClientError


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "aws_config.json"
PARTITION_ROOT = ROOT / "data" / "partitioned" / "orders"


def load_config() -> dict[str, str]:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    required = [
        "bucket_name",
        "aws_region",
        "athena_database",
        "athena_table",
        "athena_output_s3",
    ]
    missing = [key for key in required if not config.get(key) or str(config[key]).startswith("<")]
    if missing:
        raise ValueError(f"Update config/aws_config.json before upload. Missing: {', '.join(missing)}")
    config.setdefault("s3_prefix", "datalake")
    return config


def ensure_bucket_exists(config: dict[str, str]) -> None:
    s3 = boto3.client("s3", region_name=config["aws_region"])
    bucket = config["bucket_name"]
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "Unknown")
        message = error.get("Message", str(exc))
        if code in {"404", "NoSuchBucket", "NotFound"}:
            raise RuntimeError(
                f"S3 bucket '{bucket}' does not exist. Create it first or update config/aws_config.json."
            ) from exc
        if code in {"403", "AccessDenied"}:
            raise RuntimeError(
                f"S3 bucket '{bucket}' exists but is not accessible with the current AWS credentials."
            ) from exc
        raise RuntimeError(f"S3 bucket check failed for '{bucket}': [{code}] {message}") from exc


def upload_partitions(config: dict[str, str]) -> str:
    s3 = boto3.client("s3", region_name=config["aws_region"])
    bucket = config["bucket_name"]
    prefix = f"{config['s3_prefix'].strip('/')}/orders"
    uploaded_files = 0

    for local_path in PARTITION_ROOT.rglob("*.parquet"):
        relative_path = local_path.relative_to(PARTITION_ROOT).as_posix()
        s3_key = f"{prefix}/{relative_path}"
        try:
            s3.upload_file(str(local_path), bucket, s3_key)
            print(f"Uploaded s3://{bucket}/{s3_key}")
            uploaded_files += 1
        except ClientError as exc:
            error = exc.response.get("Error", {})
            code = error.get("Code", "Unknown")
            message = error.get("Message", str(exc))
            raise RuntimeError(f"Upload failed for s3://{bucket}/{s3_key}: [{code}] {message}") from exc

    print(f"Uploaded {uploaded_files} parquet files to s3://{bucket}/{prefix}/")

    return f"s3://{bucket}/{prefix}/"


def main() -> None:
    try:
        if not PARTITION_ROOT.exists():
            raise FileNotFoundError(f"Partitioned data not found: {PARTITION_ROOT}")

        config = load_config()
        ensure_bucket_exists(config)
        table_location = upload_partitions(config)
        print(f"S3 upload completed successfully at {table_location}")
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
