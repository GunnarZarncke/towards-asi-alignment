#!/usr/bin/env python3
"""Verify the LaTeX book scaffold structure."""

from __future__ import annotations

import re
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
    "tables/part-roadmap.tex",
    "references/main.bib",
]

PARTS = [f"parts/part{i:02d}-" for i in range(1, 11)]
CHAPTER_COUNT = 48
APPENDIX_COUNT = 13
PART_I = {f"ch{i:02d}" for i in range(1, 6)}
EQREF = re.compile(r"\\(?:eqref|ref)\{(eq:[^}]+)\}")
LABEL_EQ = re.compile(r"\\label\{(eq:[^}]+)\}")


def check_part_i_eqref_homes() -> list[str]:
    """Part I (ch01–ch05) may \\eqref only equations defined in Part I."""

    eq_home: dict[str, str] = {}
    chapters_dir = ROOT / "chapters"
    for path in sorted(chapters_dir.glob("ch*.tex")):
        ch = path.stem.split("-")[0]
        for m in LABEL_EQ.finditer(path.read_text(encoding="utf-8")):
            eq_home[m.group(1)] = ch
    errors: list[str] = []
    for path in sorted(chapters_dir.glob("ch*.tex")):
        ch = path.stem.split("-")[0]
        if ch not in PART_I:
            continue
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("%"):
                continue
            for m in EQREF.finditer(line):
                lab = m.group(1)
                home = eq_home.get(lab)
                if home is None:
                    errors.append(f"{path.name}:{i} \\eqref{{{lab}}} has no defining \\label")
                elif home not in PART_I:
                    errors.append(
                        f"{path.name}:{i} Part I \\eqref{{{lab}}} homes in {home}; "
                        "use \\ref{{ch:…}} / \\ref{{sec:…}} so Part I reads without later equations"
                    )
    return errors


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

    errors.extend(check_part_i_eqref_homes())

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
