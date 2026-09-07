#!/usr/bin/env python3
"""Check frozen H4 bundle protocol h4-bundle-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h4-bundle-v1.json"
PROTOCOL = "h4-bundle-v1.0.0"


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print("[1/3] load", FIXTURE.name)
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    ok_n = data.get("n_countries", 0) >= 20
    print(f"[2/3] {'PASS' if ok_n else 'FAIL'} n_countries ≥ 20")
    ok = data.get("status") == "layer_fail" and data.get("n_nonimplication_pairs", 0) > 0
    print(f"[3/3] {'PASS' if ok else 'FAIL'} C-004 non-implication layer fail")
    if not (ok_n and ok):
        return 1
    print("OUTCOME C-004 layer_fail")
    return 0


if __name__ == "__main__":
    sys.exit(main())
