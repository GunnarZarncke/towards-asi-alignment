#!/usr/bin/env python3
"""Check frozen H4 SCOTUS protocol h4-scotus-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h4-scotus-v1.json"
PROTOCOL = "h4-scotus-v1.0.0"
MARGIN = 0.05
MIN_INCLUDED = 9


def classify(acc_g: float, acc_1d: float, acc_i: float) -> str:
    beat_1d = acc_g >= acc_1d + MARGIN
    beat_i = acc_g >= acc_i + MARGIN
    if beat_1d and beat_i:
        return "layer_fail_and_detection_pass"
    if beat_1d or beat_i:
        return "ambig"
    return "null"


def main() -> int:
    print("[1/4] load", FIXTURE.name)
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    status = data.get("status")
    print("[2/4] status", status)
    if status == "refuse":
        print("OUTCOME refuse:", data.get("reason"))
        return 0
    n = data.get("n_units_included", 0)
    ok_n = n >= MIN_INCLUDED
    print(f"[3/4] {'PASS' if ok_n else 'FAIL'} n={n} ≥ {MIN_INCLUDED}")
    acc = data["heldout_accuracy"]
    expected = classify(acc["geometry"], acc["oned_issue_area"], acc["intercept"])
    ok_st = status == expected
    print(
        f"[4/4] {'PASS' if ok_st else 'FAIL'} status={status} "
        f"geom={acc['geometry']} 1-D={acc['oned_issue_area']} intercept={acc['intercept']}"
    )
    print(
        "  margins",
        data.get("margin_geometry_minus_oned"),
        data.get("margin_geometry_minus_intercept"),
    )
    if not (ok_n and ok_st):
        return 1
    print("OUTCOME", status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
