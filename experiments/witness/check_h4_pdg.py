#!/usr/bin/env python3
"""Check frozen H4 PDG protocol h4-pdg-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h4-pdg-v1.json"
PROTOCOL = "h4-pdg-v1.0.0"
MARGIN = 0.25
MIN_INCLUDED = 50


def classify(mae_g: float, mae_1d: float, mae_i: float) -> str:
    beat_1d = mae_g <= mae_1d - MARGIN
    beat_i = mae_g <= mae_i - MARGIN
    if beat_1d and beat_i:
        return "layer_fail_and_detection_pass"
    if beat_1d or beat_i:
        return "ambig"
    return "null"


def main() -> int:
    print("[1/3] load", FIXTURE.name)
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    status = data.get("status")
    print("[2/3] status", status)
    if status == "refuse":
        reason = data.get("reason") or ""
        low = reason.lower()
        ok = "refuse" == status and (
            "10–20" in reason or "10-20" in low or "adolescent" in low or "prereg" in low
        )
        print("[3/3]", "PASS" if ok else "FAIL", "refuse reason recorded")
        print("OUTCOME refuse:", reason[:400])
        return 0 if ok else 1
    n = data.get("n_units_included", 0)
    ok_n = n >= MIN_INCLUDED
    print(f"  n_units_included={n} ≥ {MIN_INCLUDED}: {ok_n}")
    mae = data["heldout_mae"]
    expected = classify(mae["geometry"], mae["oned_generosity"], mae["intercept"])
    ok_st = status == expected
    print(
        f"[3/3] {'PASS' if ok_st else 'FAIL'} status={status} "
        f"geom={mae['geometry']} 1-D={mae['oned_generosity']} intercept={mae['intercept']}"
    )
    if not (ok_n and ok_st):
        return 1
    print("OUTCOME", status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
