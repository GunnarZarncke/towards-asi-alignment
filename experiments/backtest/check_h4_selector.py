#!/usr/bin/env python3
"""Check frozen H4 selector protocol h4-selector-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h4-selector-v1.json"
PROTOCOL = "h4-selector-v1.0.0"


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print("[1/4] load", FIXTURE.name)
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    ok_n = data.get("n_joined", 0) >= 8
    print(f"[2/4] {'PASS' if ok_n else 'FAIL'} n_joined ≥ 8")
    rho_h = data.get("spearman_elo_honest")
    rho_a = data.get("spearman_elo_accuracy")
    ok_rho = rho_h is not None and rho_a is not None and rho_h <= 0 and rho_a > 0
    print(f"[3/4] {'PASS' if ok_rho else 'FAIL'} Spearman Elo×honest ≤ 0 and Elo×acc > 0")
    ok_st = data.get("status") == "layer_fail"
    print(f"[4/4] {'PASS' if ok_st else 'FAIL'} C-007 layer fail")
    if not (ok_n and ok_rho and ok_st):
        return 1
    print("OUTCOME C-007 layer_fail")
    return 0


if __name__ == "__main__":
    sys.exit(main())
