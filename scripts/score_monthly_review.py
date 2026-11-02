#!/usr/bin/env python3
"""Score a monthly section-vintage review (§3.16).

Each excerpt starts with four label lines: TOP, TOP_OLD, RANDOM, RANDOM_OLD.
The author deletes all but the one that matches the excerpt. Excerpt order in
the file is shuffled and does not indicate priority. The sibling `.key.json`
holds the true label per id.

Stop (frozen 2026-11-02): every excerpt whose true label is TOP or TOP_OLD
must have that single label left. RANDOM and RANDOM_OLD are printed and do not
change the exit code.

Exit 0: all top excerpts labeled correctly.
Exit 1: stop — human pass on the missed top paths before the next feature lane.
Exit 2: any excerpt does not have exactly one label line left.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOP_LABELS = {"TOP", "TOP_OLD"}
LABEL_LINE = re.compile(r"^(TOP_OLD|TOP|RANDOM_OLD|RANDOM)\s*$")


def parse_marks(text: str) -> dict[str, list[str]]:
    parts = re.split(r"(?=^## E\d+\s*$)", text, flags=re.M)
    marks: dict[str, list[str]] = {}
    for part in parts:
        header = re.match(r"## (E\d+)\s*\n", part)
        if not header:
            continue
        rest = part[header.end() :]
        heading = rest.find("\n### ")
        block = rest[:heading] if heading >= 0 else rest
        found = [m.group(1) for line in block.splitlines() if (m := LABEL_LINE.match(line.strip()))]
        marks[header.group(1)] = found
    return marks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path, help="monthly review markdown")
    parser.add_argument("--key", type=Path, default=None)
    args = parser.parse_args()
    review = args.review
    key_path = args.key or review.with_suffix(".key.json")
    if not review.is_file():
        raise SystemExit(f"missing review file: {review}")
    if not key_path.is_file():
        raise SystemExit(f"missing key: {key_path}")
    key = json.loads(key_path.read_text(encoding="utf-8"))
    marks = parse_marks(review.read_text(encoding="utf-8"))

    top_wrong: list[str] = []
    bad_count: list[str] = []
    rows = []
    for row in key["excerpts"]:
        kept = marks.get(row["id"], [])
        if len(kept) == 1:
            guessed = kept[0]
        else:
            guessed = None
        ok = guessed == row["label"]
        scope = "top" if row["label"] in TOP_LABELS else "random"
        if len(kept) != 1:
            bad_count.append(row["id"])
        elif scope == "top" and not ok:
            top_wrong.append(row["id"])
        rows.append((row, guessed, ok, scope, len(kept)))

    print(f"month {key.get('month', '?')}  words {key.get('words', '?')}")
    if bad_count:
        print("INCOMPLETE: each excerpt must keep exactly one of TOP, TOP_OLD, RANDOM, RANDOM_OLD.")
        for row, _g, _ok, _scope, n in rows:
            if n != 1:
                print(f"  {row['id']} has {n} label line(s) left (need 1)")
        sys.exit(2)

    for row, guessed, ok, scope, _n in rows:
        status = "ok" if ok else "miss"
        print(
            f"  {row['id']}  {scope:6}  said {guessed or '(none)':10}  true {row['label']:10}  {status}"
            f"  {row['path']}"
        )

    n_top = sum(1 for _r, _g, _ok, scope, _n in rows if scope == "top")
    n_top_ok = sum(1 for _r, _g, ok, scope, _n in rows if scope == "top" and ok)
    n_rand = sum(1 for _r, _g, _ok, scope, _n in rows if scope == "random")
    n_rand_ok = sum(1 for _r, _g, ok, scope, _n in rows if scope == "random" and ok)
    print(f"top {n_top_ok}/{n_top}  random {n_rand_ok}/{n_rand} (informational)")

    if top_wrong:
        missed = [row["path"] for row, _g, ok, scope, _n in rows if scope == "top" and not ok]
        print("STOP: top label miss. Human pass on: " + ", ".join(missed))
        sys.exit(1)
    print("PASS: top excerpts labeled correctly.")


if __name__ == "__main__":
    main()
