#!/usr/bin/env python3
"""Stream concatenated Perceval JSON objects; join Reviewed-by onto BIC hashes."""

from __future__ import annotations

import csv
import gzip
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GZ = ROOT / "data" / "zenodo" / "linux-commits-2023-11-12.json.gz"
CSV = ROOT / "data" / "zenodo" / "bfc_bic.csv"
OUT = ROOT / "data" / "zenodo" / "bic_review_tags_v1.json"

TAG_RE = re.compile(
    r"^(Reviewed-by|Acked-by|Tested-by|Reported-by|Fixes):\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)


def extract_hash_message(obj: dict) -> tuple[str | None, str]:
    data = obj.get("data") if isinstance(obj.get("data"), dict) else obj
    h = data.get("commit") or data.get("hash") or data.get("Commit")
    msg = data.get("message") or data.get("Message") or ""
    if isinstance(h, dict):
        h = h.get("hash") or h.get("commit")
    if not msg and isinstance(data.get("Commit"), dict):
        msg = data["Commit"].get("message") or ""
        h = h or data["Commit"].get("hash") or data["Commit"].get("commit")
    return (str(h).lower() if h else None), str(msg)


def main() -> int:
    if not GZ.exists():
        print("MISSING", GZ, file=sys.stderr)
        return 1
    print("[1/4] load BIC hashes", flush=True)
    bic: set[str] = set()
    bfc: set[str] = set()
    with CSV.open(encoding="utf-8", errors="replace", newline="") as f:
        for row in csv.DictReader(f):
            bic.add(row["BIC_hash"].lower())
            bfc.add(row["BFC_hash"].lower())
    want = bic | bfc
    print(f"[2/4] want={len(want)} bic={len(bic)} stream concatenated JSON", flush=True)
    found: dict[str, dict] = {}
    n = 0
    decoder = json.JSONDecoder()
    buf = ""
    with gzip.open(GZ, "rt", encoding="utf-8", errors="replace") as f:
        while True:
            chunk = f.read(1024 * 512)
            if chunk:
                buf += chunk
            while True:
                s = buf.lstrip()
                if not s:
                    buf = s
                    break
                try:
                    obj, idx = decoder.raw_decode(s)
                except json.JSONDecodeError:
                    buf = s
                    break
                buf = s[idx:]
                n += 1
                if n == 1:
                    data = obj.get("data") if isinstance(obj.get("data"), dict) else obj
                    print("  first keys", list(obj)[:8], "data keys", list(data)[:12] if isinstance(data, dict) else type(data), flush=True)
                    h0, m0 = extract_hash_message(obj)
                    print("  first hash", h0, "msg_len", len(m0), flush=True)
                if n % 25000 == 0:
                    print(f"  [{n}] scanned matched={len(found)} buf={len(buf)}", flush=True)
                h, msg = extract_hash_message(obj)
                if not h or h not in want:
                    continue
                tags = {m.group(1).lower(): True for m in TAG_RE.finditer(msg)}
                found[h] = {
                    "reviewed_by": bool(tags.get("reviewed-by")),
                    "acked_by": bool(tags.get("acked-by")),
                    "tested_by": bool(tags.get("tested-by")),
                    "fixes": bool(tags.get("fixes")),
                    "msg_len": len(msg),
                }
            if not chunk:
                break
    bic_rows = [found[h] for h in bic if h in found]
    n_rb = sum(1 for r in bic_rows if r["reviewed_by"])
    payload = {
        "commits_scanned": n,
        "wanted": len(want),
        "matched": len(found),
        "bic_matched": len(bic_rows),
        "bic_with_reviewed_by": n_rb,
        "bic_with_reviewed_by_frac": (n_rb / len(bic_rows)) if bic_rows else None,
        "sample_bic_with_rb": [h for h, r in found.items() if h in bic and r["reviewed_by"]][:20],
        "sample_bic_without_rb": [h for h, r in found.items() if h in bic and not r["reviewed_by"]][:20],
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[3/4] wrote {OUT}", flush=True)
    print(f"[4/4] scanned={n} matched={len(found)} bic_rb={n_rb}/{len(bic_rows)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
