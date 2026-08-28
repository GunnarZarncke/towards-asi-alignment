#!/usr/bin/env python3
"""Summarize wiki-socks: labeled socks vs matched non-socks (Exp. 3 instrument, not κ*)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATS = ROOT / "data" / "wiki-socks" / "repo" / "stats.csv"
OUT = ROOT / "data" / "wiki-socks" / "spi_instrument_v1.json"


def main() -> int:
    n = 0
    pos = 0
    neg = 0
    with STATS.open(encoding="utf-8", errors="replace", newline="") as f:
        for row in csv.DictReader(f):
            n += 1
            pos += int(float(row["num_positives"]))
            neg += int(float(row["num_negatives"]))
            if n % 5000 == 0:
                print(f"  [{n}] investigations", flush=True)
    payload = {
        "source": "lraszewski/wiki-socks stats.csv",
        "investigations": n,
        "positive_contrib_rows": pos,
        "negative_twin_contrib_rows": neg,
        "has_labeled_socks_and_twins": n > 0 and pos > 0 and neg > 0,
        "kappa_star": None,
        "note": "Labels and twins exist; CheckUser private; no cost-of-faking bound.",
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
