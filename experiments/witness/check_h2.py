#!/usr/bin/env python3
"""Check frozen H2 Linux protocol fixture h2-v1.2.0 (richer sources)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h2-linux-v1.json"
PROTOCOL = "h2-v1.2.0"


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print("[1/5] load", FIXTURE.name)
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    c4 = data["c004a"]
    ok4 = (
        c4.get("status") == "layer_fail"
        and c4.get("instrument_has_both") is True
        and c4.get("bic_with_reviewed_by", 0) >= 17000
    )
    print(f"[2/5] {'PASS' if ok4 else 'FAIL'} C-004a Reviewed-by×BIC layer fail")
    c5 = data["c005_nak_reentry"]
    ep = c5.get("episode") or {}
    ok5 = c5.get("status") == "layer_fail" and ep.get("revert") and ep.get("reentry")
    print(f"[3/5] {'PASS' if ok5 else 'FAIL'} C-005 revert then same-title re-entry")
    c6 = data["c006_stable_option3"]
    ok6 = c6.get("status") == "layer_fail" and c6.get("unlisted_fails") is True
    print(f"[4/5] {'PASS' if ok6 else 'FAIL'} C-006 adjusted -stable hunk ≠ upstream")
    rb = data["reviewed_by_as_M"].get("status") == "refuse"
    print(f"[5/5] {'PASS' if rb else 'FAIL'} Reviewed-by M refuse")
    if not (ok4 and ok5 and ok6 and rb):
        return 1
    print("OUTCOME C-004a/C-005/C-006 layer_fail; Exp3 Reviewed-by refuse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
