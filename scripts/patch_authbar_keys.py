#!/usr/bin/env python3
"""Set authbar keys for epistemic status, Summary, and Chapter References."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = sorted((ROOT / "chapters").glob("ch*.tex")) + sorted(
    (ROOT / "appendices").glob("app*.tex")
)

EPISTEMIC_RE = re.compile(
    r"\\begin\{authbar\}\{[^}]+\}(\s*\n\\begin\{epistemicstatus\})"
)
SUMMARY_RE = re.compile(
    r"(\\section\{Summary\}(?:\s*\n(?:\\label\{[^}]+\}|%[^\n]*|\s*))*)"
    r"\\begin\{authbar\}\{[^}]+\}"
)
CHAPTER_REFS_RE = re.compile(
    r"(\\section\*\{Chapter References\}(?:\s*\n(?:\\label\{[^}]+\}|%[^\n]*|\s*))*)"
    r"\\begin\{authbar\}\{[^}]+\}"
)


def patch(text: str) -> str:
    text = EPISTEMIC_RE.sub(r"\\begin{authbar}{GZ+AI}\1", text)
    text = SUMMARY_RE.sub(r"\1\\begin{authbar}{AI}", text)
    text = CHAPTER_REFS_RE.sub(r"\1\\begin{authbar}{AI}", text)
    return text


def main() -> int:
    changed = 0
    for path in TARGETS:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = patch(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"patched: {path.relative_to(ROOT)}")
            changed += 1
    print(f"Done. Patched {changed} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
