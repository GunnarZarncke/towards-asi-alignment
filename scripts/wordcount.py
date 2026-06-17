#!/usr/bin/env python3
"""Approximate word count for chapter LaTeX files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRIP_RE = re.compile(r"\\[a-zA-Z@]+(\[[^\]]*\])?(\{[^}]*\})?|[{}%]|\\.")


def count_words(text: str) -> int:
    text = re.sub(r"%.*", "", text)
    text = STRIP_RE.sub(" ", text)
    return len(text.split())


def main() -> None:
    total = 0
    for path in sorted((ROOT / "chapters").glob("ch*.tex")):
        n = count_words(path.read_text(encoding="utf-8"))
        total += n
        print(f"{path.name}: {n}")
    print(f"Total (chapters): {total}")


if __name__ == "__main__":
    main()
