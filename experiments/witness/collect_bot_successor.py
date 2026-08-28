#!/usr/bin/env python3
"""Find a BRFA-approved bot with a later rights/block event (C-006)."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "mediawiki" / "bot_successor_v1.json"
UA = "towards-asi-alignment-witness/1.0 (https://github.com/GunnarZarncke/towards-asi-alignment; research)"
API = "https://en.wikipedia.org/w/api.php"

# Frozen candidates: historically flagged bots with public BRFA pages.
CANDIDATES = [
    "Cydebot",
    "BetacommandBot",
    "SoxBot",
    "AnomieBOT",
    "ClueBot NG",
    "Lowercase sigmabot III",
    "RussBot",
    "Xenobot Mk V",
]


def api(params: dict) -> dict:
    q = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def page_exists(title: str) -> bool:
    d = api({"action": "query", "titles": title})
    pages = d.get("query", {}).get("pages", {})
    return not any(int(k) < 0 for k in pages)


def collect(user: str) -> dict:
    brfa = f"Wikipedia:Bots/Requests for approval/{user}"
    row = {"user": user, "brfa_page": brfa, "brfa_exists": page_exists(brfa)}
    time.sleep(0.1)
    row["blocks"] = api(
        {
            "action": "query",
            "list": "logevents",
            "letype": "block",
            "letitle": f"User:{user}",
            "lelimit": "5",
        }
    ).get("query", {}).get("logevents", [])
    time.sleep(0.1)
    row["rights"] = api(
        {
            "action": "query",
            "list": "logevents",
            "letype": "rights",
            "letitle": f"User:{user}",
            "lelimit": "20",
        }
    ).get("query", {}).get("logevents", [])
    bot_removed = []
    for ev in row["rights"]:
        params = ev.get("params") or {}
        old = str(params.get("oldgroups", params.get("old", "")))
        new = str(params.get("newgroups", params.get("new", "")))
        blob = json.dumps(params).lower()
        if "bot" in blob and ("bot" in old.lower() or "'bot'" in old):
            if "bot" not in new.lower() or (isinstance(params.get("oldgroups"), list) and "bot" in params.get("oldgroups", []) and "bot" not in params.get("newgroups", [])):
                bot_removed.append(ev)
        if isinstance(params.get("oldgroups"), list) and "bot" in params["oldgroups"] and "bot" not in (params.get("newgroups") or []):
            bot_removed.append(ev)
    row["bot_flag_removed_events"] = bot_removed
    row["has_block_log"] = bool(row["blocks"])
    return row


def main() -> int:
    rows = []
    for i, u in enumerate(CANDIDATES, 1):
        print(f"[{i}/{len(CANDIDATES)}] {u}", flush=True)
        try:
            rows.append(collect(u))
        except Exception as e:
            rows.append({"user": u, "error": str(e)})
        time.sleep(0.15)
    hits = [r for r in rows if r.get("brfa_exists") and (r.get("bot_flag_removed_events") or r.get("has_block_log"))]
    payload = {"candidates": rows, "n_brfa_and_later_stop": len(hits), "hits": [h["user"] for h in hits]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {OUT} hits={payload['hits']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
