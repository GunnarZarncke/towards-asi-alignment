#!/usr/bin/env python3
"""Lightweight narrative-voice lint for the LaTeX manuscript."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHAPTER_GLOB = "chapters/ch*.tex"
PARATEXT = {
    ROOT / "frontmatter" / "dedication.tex",
    ROOT / "frontmatter" / "acknowledgements.tex",
    ROOT / "frontmatter" / "preface.tex",
}

I_CLAIM = re.compile(r"\bI (?:argue|claim|contend|believe|think we|propose that)\b", re.I)
WE_ARGUE = re.compile(r"\bwe (?:argue|claim|contend)\b", re.I)
THESIS_BLOCK = re.compile(
    r"\\begin\{chapterthesis\}(.*?)\\end\{chapterthesis\}", re.S | re.I
)
THESIS_BAD = re.compile(r"\b(?:we\b|this chapter argues)\b", re.I)
WWCTV = re.compile(
    r"\\section\{What Would Change This View\}.*?(?=\\section|\Z)", re.S | re.I
)


def strip_comments(text: str) -> str:
    text = re.sub(r"(?m)^%.*$", "", text)
    text = re.sub(r"\\epigraph\{.*?\}\{.*?\}", "", text, flags=re.S)
    return text


def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    rel = path.relative_to(ROOT)

    if path.suffix == ".tex" and "chapters/ch" in str(path):
        if I_CLAIM.search(text):
            issues.append(f"{rel}: authorial I-claim in chapter body")
        if WE_ARGUE.search(text):
            issues.append(f"{rel}: 'we argue/claim' in chapter body (prefer direct claim)")

        thesis = THESIS_BLOCK.search(text)
        if thesis and THESIS_BAD.search(thesis.group(1)):
            issues.append(f"{rel}: chapterthesis uses 'we' or 'This chapter argues'")

        wwctv = WWCTV.search(text)
        if wwctv and re.search(r"\bwe argue\b", wwctv.group(0), re.I):
            issues.append(f"{rel}: WWCTV uses 'we argue' (use 'This chapter argues')")

    return issues


def main() -> int:
    paths = sorted(ROOT.glob(CHAPTER_GLOB))
    issues: list[str] = []
    for path in paths:
        issues.extend(check_file(path))

    if issues:
        print("Voice check failed:\n")
        for item in issues:
            print(f"  - {item}")
        return 1

    print(f"Voice check passed ({len(paths)} chapter files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
