#!/usr/bin/env python3
"""Validate metadata/claim-extracts/*.jsonl against the manuscript and the Lean spine.

Checks per record:
  - JSON parses, required keys present, ids unique
  - `quote` occurs verbatim (whitespace-normalised) inside `lines` of the chapter file
  - every `lean:<name>` ref and every `lean.sym` entry names a symbol that occurs
    as a whole word in formal/**/*.lean (last dotted component)
  - every `ref` has a known prefix (lean|label|cite|concept|?)

Stop rule: any failure means the extract is stale or wrong. Fix the record or delete
it; do not edit the chapter to fit the extract. Prints a flag histogram (informational).

Usage: python3 scripts/check_claim_extract.py [metadata/claim-extracts/ch42.jsonl ...]
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACT_DIR = ROOT / "metadata" / "claim-extracts"
REQUIRED = {"id", "lines", "sec", "quote", "role", "load", "rule", "form", "refs", "lean", "flags"}
PREFIXES = ("lean:", "label:", "cite:", "concept:", "?:")
CHAPTER_FILES = {"ch42": "chapters/ch42-safety-case.tex"}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def lean_corpus() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "formal").rglob("*.lean"))


def check_file(path: Path, lean: str) -> tuple[list[str], Counter]:
    errors: list[str] = []
    flags: Counter = Counter()
    chapter = CHAPTER_FILES.get(path.stem)
    if chapter is None:
        return [f"{path.name}: no chapter mapping in CHAPTER_FILES"], flags
    tex_lines = (ROOT / chapter).read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            r = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}:{n}: bad JSON: {e}")
            continue
        rid = r.get("id", f"<line {n}>")
        missing = REQUIRED - r.keys()
        if missing:
            errors.append(f"{rid}: missing keys {sorted(missing)}")
            continue
        if rid in seen:
            errors.append(f"{rid}: duplicate id")
        seen.add(rid)
        a, b = r["lines"]
        window = norm(" ".join(tex_lines[a - 1 : b]))
        if norm(r["quote"]) not in window:
            errors.append(f"{rid}: quote not found in {chapter}:{a}-{b}")
        syms = [x[5:] for x in r["refs"] if x.startswith("lean:")] + list(r["lean"].get("sym", []))
        for s in syms:
            name = s.split(".")[-1]
            if not re.search(rf"(?<![\w']){re.escape(name)}(?![\w'])", lean):
                errors.append(f"{rid}: Lean symbol not found: {s}")
        for x in r["refs"]:
            if not x.startswith(PREFIXES):
                errors.append(f"{rid}: ref without known prefix: {x}")
        flags.update(r["flags"])
    return errors, flags


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or sorted(EXTRACT_DIR.glob("*.jsonl"))
    lean = lean_corpus()
    total_errors: list[str] = []
    for p in paths:
        errs, flags = check_file(p, lean)
        total_errors += errs
        print(f"{p.name}: {len(errs)} error(s)")
        for tag, c in flags.most_common():
            print(f"  {c:3d}  {tag}")
    for e in total_errors:
        print("ERROR", e)
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
