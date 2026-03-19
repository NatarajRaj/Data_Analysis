from __future__ import annotations

from pathlib import Path
import shutil

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PARQUET = ROOT / "data" / "raw" / "sample_orders.parquet"
PARTITION_ROOT = ROOT / "data" / "partitioned" / "orders"


def main() -> None:
    if not RAW_PARQUET.exists():
        raise FileNotFoundError(f"Missing raw parquet file: {RAW_PARQUET}")

    df = pd.read_parquet(RAW_PARQUET)
    df["order_ts"] = pd.to_datetime(df["order_ts"])
    df["year"] = df["order_ts"].dt.strftime("%Y")
    df["month"] = df["order_ts"].dt.strftime("%m")
    df["day"] = df["order_ts"].dt.strftime("%d")

    if PARTITION_ROOT.exists():
        shutil.rmtree(PARTITION_ROOT)
    PARTITION_ROOT.mkdir(parents=True, exist_ok=True)

    for (year, month, day), frame in df.groupby(["year", "month", "day"], sort=True):
        partition_dir = PARTITION_ROOT / f"year={year}" / f"month={month}" / f"day={day}"
        partition_dir.mkdir(parents=True, exist_ok=True)
        output_path = partition_dir / "orders.parquet"
        frame.drop(columns=["year", "month", "day"]).to_parquet(output_path, index=False)

    print(f"Created {df.groupby(['year', 'month', 'day']).ngroups} partitions under {PARTITION_ROOT}")


if __name__ == "__main__":
    main()
