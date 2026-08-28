#!/usr/bin/env python3
"""Join SNAP wiki-RfA candidates to later MediaWiki traces (blocks / rights / contribs)."""

from __future__ import annotations

import gzip
import json
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAP = ROOT / "data" / "snap" / "wiki-RfA.txt.gz"
OUT = ROOT / "data" / "mediawiki" / "rfa_followup_v1.json"
UA = "towards-asi-alignment-witness/1.0 (https://github.com/GunnarZarncke/towards-asi-alignment; research)"
API = "https://en.wikipedia.org/w/api.php"
SAMPLE_N = 40
YEAR = 2012


def _add_vote(elections: dict, rec: dict) -> None:
    if not rec.get("TGT"):
        return
    key = (rec["TGT"], rec.get("YEA", ""))
    e = elections.setdefault(
        key,
        {
            "tgt": rec["TGT"],
            "yea": rec.get("YEA"),
            "res": rec.get("RES"),
            "dat": rec.get("DAT"),
            "oppose": 0,
            "support": 0,
            "neutral": 0,
        },
    )
    vot = rec.get("VOT")
    if vot == "-1":
        e["oppose"] += 1
    elif vot == "1":
        e["support"] += 1
    else:
        e["neutral"] += 1


def parse_snap(path: Path) -> list[dict]:
    rec: dict = {}
    elections: dict[tuple[str, str], dict] = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("SRC:"):
                _add_vote(elections, rec)
                rec = {"SRC": line[4:]}
                continue
            if ":" in line:
                k, _, v = line.partition(":")
                rec[k] = v
        _add_vote(elections, rec)
    return list(elections.values())


def api(params: dict) -> dict:
    q = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def later_traces(user: str) -> dict:
    out = {"user": user, "block": None, "rights_events": [], "contribs_after_2013": None}
    b = api(
        {
            "action": "query",
            "list": "blocks",
            "bkusers": user,
            "bklimit": "5",
            "bkprop": "user|timestamp|expiry|reason",
        }
    )
    blocks = b.get("query", {}).get("blocks", [])
    if blocks:
        out["block"] = blocks[0]
    lg = api(
        {
            "action": "query",
            "list": "logevents",
            "letype": "rights",
            "letitle": f"User:{user}",
            "lelimit": "10",
        }
    )
    out["rights_events"] = lg.get("query", {}).get("logevents", [])
    uc = api(
        {
            "action": "query",
            "list": "usercontribs",
            "ucuser": user,
            "ucstart": "2014-01-01T00:00:00Z",
            "uclimit": "1",
            "ucdir": "newer",
        }
    )
    contribs = uc.get("query", {}).get("usercontribs", [])
    out["contribs_after_2013"] = bool(contribs)
    if contribs:
        out["first_contrib_after_2013"] = contribs[0].get("timestamp")
    return out


def main() -> int:
    print("[1/4] parse SNAP", SNAP.name, flush=True)
    elections = parse_snap(SNAP)
    year = [e for e in elections if e.get("yea") == str(YEAR) and e["oppose"] > 0]
    year.sort(key=lambda e: (-e["oppose"], e["tgt"]))
    sample = year[:SAMPLE_N]
    print(f"[2/4] elections={len(elections)} year{YEAR}_with_oppose={len(year)} sample={len(sample)}", flush=True)
    traces = []
    for i, e in enumerate(sample, 1):
        print(f"  [{i}/{len(sample)}] {e['tgt']} oppose={e['oppose']} res={e['res']}", flush=True)
        try:
            t = later_traces(e["tgt"])
        except Exception as ex:
            t = {"user": e["tgt"], "error": str(ex)}
        traces.append({**e, "later": t})
        time.sleep(0.15)
    n_block = sum(1 for t in traces if t.get("later", {}).get("block"))
    n_rights = sum(1 for t in traces if t.get("later", {}).get("rights_events"))
    n_later_edits = sum(1 for t in traces if t.get("later", {}).get("contribs_after_2013"))
    payload = {
        "source": "SNAP wiki-RfA + MediaWiki API",
        "sample_year": YEAR,
        "sample_n": len(sample),
        "n_with_block_record": n_block,
        "n_with_rights_log": n_rights,
        "n_with_contribs_after_2013": n_later_edits,
        "traces": traces,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[3/4] wrote {OUT} blocks={n_block} rights={n_rights} later_edits={n_later_edits}", flush=True)
    print("[4/4] done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
