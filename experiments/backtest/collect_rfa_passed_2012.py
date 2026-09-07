#!/usr/bin/env python3
"""All 2012 successful SNAP RfAs with oppose>0 → later MediaWiki traces."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_rfa_followup import SNAP, later_traces, parse_snap  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "mediawiki" / "rfa_followup_passed_2012.json"


def main() -> int:
    elections = parse_snap(SNAP)
    passed = [e for e in elections if e.get("yea") == "2012" and e.get("res") == "1" and e["oppose"] > 0]
    print(f"[1/3] passed_2012_with_oppose={len(passed)}", flush=True)
    traces = []
    for i, e in enumerate(passed, 1):
        print(f"  [{i}/{len(passed)}] {e['tgt']} oppose={e['oppose']}", flush=True)
        try:
            t = later_traces(e["tgt"])
        except Exception as ex:
            t = {"user": e["tgt"], "error": str(ex)}
        traces.append({**e, "later": t})
        time.sleep(0.15)
    n_block = sum(1 for t in traces if t.get("later", {}).get("block"))
    desysop_users = []
    for t in traces:
        for ev in t.get("later", {}).get("rights_events") or []:
            params = ev.get("params") or {}
            old = params.get("oldgroups") or []
            new = params.get("newgroups") or []
            if isinstance(old, list) and "sysop" in old and "sysop" not in (new or []):
                desysop_users.append({"tgt": t["tgt"], "ts": ev.get("timestamp"), "oppose": t["oppose"]})
                break
    payload = {
        "sample": "all 2012 SNAP RfA with RES=1 and oppose>0",
        "n": len(traces),
        "n_block": n_block,
        "n_later_edits": sum(1 for t in traces if t.get("later", {}).get("contribs_after_2013")),
        "n_sysop_removed": len(desysop_users),
        "desysop": desysop_users,
        "traces": traces,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[2/3] wrote {OUT} block={n_block} desysop={len(desysop_users)} later={payload['n_later_edits']}", flush=True)
    print("[3/3] done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
