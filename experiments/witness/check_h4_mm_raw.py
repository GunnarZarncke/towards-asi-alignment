#!/usr/bin/env python3
"""Check frozen H4 raw MM protocol h4-mm-raw-v1.0.0 plus validation block."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h4-mm-raw-v1.json"
PROTOCOL = "h4-mm-raw-v1.0.0"
MARGIN = 0.05
MIN_INCLUDED = 500


def classify(acc_g: float, acc_1d: float, acc_i: float) -> str:
    beat_1d = acc_g >= acc_1d + MARGIN
    beat_i = acc_g >= acc_i + MARGIN
    if beat_1d and beat_i:
        return "layer_fail_and_detection_pass"
    if beat_1d or beat_i:
        return "ambig"
    return "null"


def main() -> int:
    print("[1/5] load", FIXTURE.name)
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    status = data.get("status")
    print("[2/5] unit_key", data.get("unit_key"), "status", status)
    if status == "refuse":
        print("OUTCOME refuse:", data.get("reason"))
        return 0
    n = data.get("n_units_included", 0)
    ok_n = n >= MIN_INCLUDED
    print(f"[3/5] {'PASS' if ok_n else 'FAIL'} n_units_included={n} ≥ {MIN_INCLUDED}")
    acc = data["heldout_accuracy"]
    expected = classify(acc["geometry"], acc["oned_number"], acc["intercept"])
    ok_st = status == expected
    print(
        f"[4/5] {'PASS' if ok_st else 'FAIL'} status={status} "
        f"geom={acc['geometry']} 1-D={acc['oned_number']} intercept={acc['intercept']}"
    )
    print(
        "  margins",
        data.get("margin_geometry_minus_oned"),
        data.get("margin_geometry_minus_intercept"),
    )
    val = data.get("validation") or {}
    ok_val = bool(val)
    print(f"[5/5] {'PASS' if ok_val else 'FAIL'} validation block present")
    if val:
        conv = val.get("converged")
        boot = val.get("unit_bootstrap") or {}
        col = val.get("collinearity") or {}
        print("  converged", conv)
        print(
            "  bootstrap vs 1-D",
            boot.get("margin_vs_oned_p025"),
            boot.get("margin_vs_oned_p975"),
            "vs intercept",
            boot.get("margin_vs_intercept_p025"),
            boot.get("margin_vs_intercept_p975"),
        )
        print(
            "  collinear Number=Σ types",
            col.get("number_equals_sum_of_type_deltas"),
            col.get("max_abs_number_minus_type_sum"),
        )
        print(
            "  geom without Number acc",
            val.get("geometry_without_number_heldout_accuracy"),
        )
        if conv is False:
            print("  WARN not fully converged (does not change frozen pass/fail)")
    if not (ok_n and ok_st and ok_val):
        return 1
    print("OUTCOME", status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
