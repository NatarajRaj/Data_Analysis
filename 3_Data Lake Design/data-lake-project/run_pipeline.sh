#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
STEPS = [
    "scripts/01_generate_data.py",
    "scripts/02_create_partitions.py",
    "scripts/03_upload_to_s3.py",
]


def main() -> int:
    for step in STEPS:
        print(f"Running {step}...")
        subprocess.run([sys.executable, step], cwd=ROOT, check=True)
    print("Pipeline completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
