#!/usr/bin/env python3
"""Moral Machine country AMCE non-implication; write bundle fixture."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "moral-machine" / "CountriesChangePr.csv"
OUT = ROOT / "fixtures" / "h4-bundle-v1.json"

NUMBER_COL = "No. Characters [Less -> More]: Estimates"
GEOM_COLS = [
    "[Omission -> Commission]: Estimates",
    "[Passengers -> Pedestrians]: Estimates",
    "Law [Illegal -> Legal]: Estimates",
    "Gender [Male -> Female]: Estimates",
    "Fitness [Large -> Fit]: Estimates",
    "Social Status [Low -> High]: Estimates",
    "Age [Elderly -> Young]: Estimates",
    "Species [Pets -> Humans]: Estimates",
]


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return float("nan")
    k = (len(sorted_vals) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


def main() -> int:
    print("[1/4] load", CSV_PATH.name)
    if not CSV_PATH.exists():
        print("FAIL missing", CSV_PATH)
        return 1
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    countries = []
    for row in rows:
        iso = row[""]
        try:
            number = float(row[NUMBER_COL])
            geom = [float(row[c]) for c in GEOM_COLS]
        except (KeyError, ValueError):
            print("FAIL missing AMCE columns")
            return 1
        countries.append({"iso": iso, "number": number, "geom": geom})
    n = len(countries)
    print(f"[2/4] {n} countries; pairwise distances")
    if n < 20:
        payload = {
            "protocol_version": "h4-bundle-v1.0.0",
            "status": "refuse",
            "reason": f"n={n} < 20",
            "n_countries": n,
        }
        OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print("OUTCOME refuse")
        return 0

    geom_d: list[float] = []
    d1: list[float] = []
    pairs: list[tuple[float, float, str, str]] = []
    total = n * (n - 1) // 2
    done = 0
    for i in range(n):
        for j in range(i + 1, n):
            g = math.sqrt(
                sum((a - b) ** 2 for a, b in zip(countries[i]["geom"], countries[j]["geom"]))
            )
            d = abs(countries[i]["number"] - countries[j]["number"])
            geom_d.append(g)
            d1.append(d)
            pairs.append((g, d, countries[i]["iso"], countries[j]["iso"]))
            done += 1
        if (i + 1) % 20 == 0 or i == n - 1:
            print(f"  [{done}/{total}] pairs after country {i + 1}/{n}")

    print("[3/4] thresholds")
    geom_sorted = sorted(geom_d)
    d1_sorted = sorted(d1)
    med_g = percentile(geom_sorted, 0.5)
    p25_d = percentile(d1_sorted, 0.25)
    hits = [(g, d, a, b) for g, d, a, b in pairs if g >= med_g and d <= p25_d]
    example = min(hits, key=lambda t: t[1]) if hits else None

    status = "layer_fail" if hits else "refuse"
    reason = (
        f"{len(hits)} pairs with geometry ≥ median ({med_g:.4f}) and "
        f"|Δ Number| ≤ 25th percentile ({p25_d:.4f})"
        if hits
        else "no non-implication pairs under frozen thresholds"
    )

    print("[4/4] write fixture")
    payload = {
        "protocol_version": "h4-bundle-v1.0.0",
        "frozen": "2026-08-28",
        "host": "H4",
        "source": "OSF 3hvt2 CountriesChangePr.csv (Awad et al. Nature 2018)",
        "n_countries": n,
        "n_pairs": total,
        "median_geometry": round(med_g, 6),
        "p25_abs_delta_number": round(p25_d, 6),
        "n_nonimplication_pairs": len(hits),
        "example_pair": None
        if example is None
        else {
            "a": example[2],
            "b": example[3],
            "geometry": round(example[0], 6),
            "abs_delta_number": round(example[1], 6),
        },
        "oned_column": NUMBER_COL,
        "geometry_columns": GEOM_COLS,
        "status": status,
        "reason": reason,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("OUTCOME", status, reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
