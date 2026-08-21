#!/usr/bin/env python3
"""Remove empty \\begin{authbar}...\\end{authbar} blocks (section shells with no body)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = sorted((ROOT / "chapters").glob("ch*.tex")) + sorted(
    (ROOT / "appendices").glob("app*.tex")
)

# authbar open, optional blank/comment-only lines, authbar close
EMPTY_AUTHBAR_RE = re.compile(
    r"^\\begin\{authbar\}\{[^}]+\}\n(?:[ \t]*(?:%[^\n]*)?\n)*\\end\{authbar\}\n",
    re.MULTILINE,
)


def strip_empty_authbars(text: str) -> tuple[str, int]:
    return EMPTY_AUTHBAR_RE.subn("", text)


def main() -> int:
    total = 0
    for path in TARGETS:
        original = path.read_text(encoding="utf-8")
        updated, n = strip_empty_authbars(original)
        if n:
            path.write_text(updated, encoding="utf-8")
            print(f"removed {n} empty authbar(s): {path.relative_to(ROOT)}")
            total += n
    print(f"Done. Removed {total} empty authbar block(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
