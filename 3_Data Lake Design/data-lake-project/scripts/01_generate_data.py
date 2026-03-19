from __future__ import annotations

from pathlib import Path
import random

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CSV_PATH = RAW_DIR / "sample_orders.csv"
PARQUET_PATH = RAW_DIR / "sample_orders.parquet"


def build_orders() -> pd.DataFrame:
    random.seed(42)
    dates = pd.date_range("2025-01-01", "2026-03-15", freq="D")
    regions = ["north", "south", "east", "west"]
    statuses = ["created", "shipped", "delivered", "returned"]
    rows: list[dict[str, object]] = []

    order_counter = 1
    for order_date in dates:
        orders_today = random.randint(4, 12)
        for _ in range(orders_today):
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(15, 250), 2)
            discount = round(random.choice([0, 0, 0, 5, 10, 15]), 2)
            gross_amount = round(quantity * unit_price, 2)
            net_amount = round(gross_amount - discount, 2)
            rows.append(
                {
                    "order_id": f"ORD-{order_counter:06d}",
                    "customer_id": f"CUST-{random.randint(1000, 9999)}",
                    "order_ts": order_date + pd.to_timedelta(random.randint(0, 86399), unit="s"),
                    "region": random.choice(regions),
                    "status": random.choice(statuses),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": discount,
                    "net_amount": net_amount,
                }
            )
            order_counter += 1

    df = pd.DataFrame(rows).sort_values("order_ts").reset_index(drop=True)
    return df


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = build_orders()
    df.to_csv(CSV_PATH, index=False)
    df.to_parquet(PARQUET_PATH, index=False)
    print(f"Wrote {len(df)} rows to {CSV_PATH}")
    print(f"Wrote {len(df)} rows to {PARQUET_PATH}")


if __name__ == "__main__":
    main()
