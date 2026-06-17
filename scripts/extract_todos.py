#!/usr/bin/env python3
"""Extract TODO and STUB markers from LaTeX and markdown files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER_RE = re.compile(r"\[STUB\]|TODO|FIXME", re.IGNORECASE)


def main() -> None:
    count = 0
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in {".tex", ".md"}:
            continue
        if any(p.startswith(".") or p == ".venv" for p in path.relative_to(ROOT).parts):
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if MARKER_RE.search(line):
                print(f"{path.relative_to(ROOT)}:{i}: {line.strip()}")
                count += 1
    print(f"\nTotal markers: {count}")


if __name__ == "__main__":
    main()
