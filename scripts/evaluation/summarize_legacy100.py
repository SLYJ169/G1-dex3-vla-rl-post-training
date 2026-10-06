#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    with args.csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    success = sum(int(r["success"]) for r in rows)
    total = sum(int(r["total"]) for r in rows)
    print(f"Legacy100 success: {success}/{total} ({100.0 * success / total:.1f}%)")


if __name__ == "__main__":
    main()