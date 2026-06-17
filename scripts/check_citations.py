#!/usr/bin/env python3
"""Check that chapter citation keys exist in bibliography files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CITE_RE = re.compile(r"\\(?:parencite|textcite|cite|autocite|footcite)\{([^}]+)\}")
KEY_RE = re.compile(r"@\w+\{([^,]+),")


def load_bib_keys() -> set[str]:
    keys: set[str] = set()
    for bib in (ROOT / "references").glob("*.bib"):
        text = bib.read_text(encoding="utf-8", errors="replace")
        keys.update(KEY_RE.findall(text))
    return keys


def find_citations() -> set[str]:
    cites: set[str] = set()
    for tex in ROOT.rglob("*.tex"):
        if ".venv" in tex.parts:
            continue
        text = tex.read_text(encoding="utf-8", errors="replace")
        for match in CITE_RE.findall(text):
            for key in match.split(","):
                cites.add(key.strip())
    return cites


def main() -> int:
    keys = load_bib_keys()
    cites = find_citations()
    missing = sorted(c for c in cites if c not in keys)
    if missing:
        print("Missing bibliography keys:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print(f"Citation check passed ({len(cites)} keys cited, {len(keys)} keys in bib).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
