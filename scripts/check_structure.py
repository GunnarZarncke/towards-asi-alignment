#!/usr/bin/env python3
"""Verify the LaTeX book scaffold structure."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "book.tex",
    "build.sh",
    "clean.sh",
    "Makefile",
    "latexmkrc",
    "metadata/book.yml",
    "metadata/preamble.tex",
    "frontmatter/titlepage.tex",
    "frontmatter/executive-overview.tex",
    "tables/chapter-map.tex",
    "tables/part-roadmap.tex",
    "tables/part-roadmap-overview.tex",
    "references/main.bib",
]

PARTS = [f"parts/part{i:02d}-" for i in range(1, 11)]
CHAPTER_COUNT = 45
APPENDIX_COUNT = 9


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    chapters = sorted((ROOT / "chapters").glob("ch*.tex"))
    if len(chapters) != CHAPTER_COUNT:
        errors.append(f"Expected {CHAPTER_COUNT} chapter files, found {len(chapters)}")

    appendices = sorted((ROOT / "appendices").glob("app*.tex"))
    if len(appendices) != APPENDIX_COUNT:
        errors.append(f"Expected {APPENDIX_COUNT} appendix files, found {len(appendices)}")

    parts = sorted((ROOT / "parts").glob("part*.tex"))
    if len(parts) != 10:
        errors.append(f"Expected 10 part files, found {len(parts)}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
