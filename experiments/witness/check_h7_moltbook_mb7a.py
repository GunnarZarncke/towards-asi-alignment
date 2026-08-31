#!/usr/bin/env python3
"""Check frozen H7 Moltbook MB7a protocol h7-moltbook-mb7a-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h7-moltbook-mb7a-v1.json"
PREREG = Path(__file__).resolve().parent / "fixtures" / "h7-moltbook-mb7a-v1.preregistration.json"
PROTOCOL = "h7-moltbook-mb7a-v1.0.0"
ALLOWED = {"pass", "fail", "structure_stop", "ambig", "refuse", "null"}
BROADCAST_STOP = 0.95


def expected_status(data: dict) -> str | None:
    """Recompute outcome from frozen metrics when tier_a block present."""
    ta = data.get("tier_a")
    if not ta:
        return None
    n_found = len(ta.get("author_ids_found") or [])
    if n_found < 2:
        return "refuse"
    if not ta.get("joined"):
        return "refuse"
    bf = float(ta.get("broadcast_fraction_jan31", 0))
    if (
        bf >= BROADCAST_STOP
        and not ta.get("thread_edge_jan31")
        and not ta.get("merged")
    ):
        return "structure_stop"
    if ta.get("merged") and int(ta.get("over_merge", 0)) == 0:
        return "pass"
    if ta.get("merged") and int(ta.get("over_merge", 0)) > 0:
        return "ambig"
    if ta.get("coactivity_jan31") and not ta.get("merged"):
        return "fail"
    return "null"


def main() -> int:
    print("[1/5] load preregistration", PREREG.name)
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg.get("protocol_version") != PROTOCOL:
        print("FAIL prereg protocol")
        return 1

    print("[2/5] load", FIXTURE.name)
    if not FIXTURE.exists():
        print("FAIL missing fixture — run collect_h7_moltbook_mb7a.py")
        return 1
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1

    status = data.get("status")
    print("[3/5] status", status)
    if status not in ALLOWED:
        print("FAIL unknown status")
        return 1
    if status == "refuse":
        print("OUTCOME refuse:", data.get("reason", data.get("tier_a")))
        return 0

    exp = expected_status(data)
    ok_st = exp is None or status == exp
    print(f"[4/5] {'PASS' if ok_st else 'FAIL'} expected={exp} reported={status}")
    ta = data.get("tier_a", {})
    print(
        "  tier_a merged=", ta.get("merged"),
        "over_merge=", ta.get("over_merge"),
        "coactivity=", ta.get("coactivity_jan31"),
    )

    ok_thr = data.get("thresholds", {}).get("specificity_ratio") == 1.25
    print(f"[5/5] {'PASS' if ok_thr else 'FAIL'} frozen thresholds present")
    if not (ok_st and ok_thr):
        return 1
    print("OUTCOME", status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
