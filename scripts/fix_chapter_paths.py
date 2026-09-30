#!/usr/bin/env python3
"""Fix chained chapter-id replacements by matching file slugs to disk."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
SKIP_DIRS = {".git", ".lake", "dist", "node_modules", "__pycache__", ".biber-par-cache"}


def slug_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in CHAPTERS.glob("ch*.tex"):
        match = re.match(r"(ch\d+)-(.+)\.tex$", path.name)
        if not match:
            raise ValueError(path.name)
        prefix, slug = match.groups()
        mapping[slug] = prefix
    return mapping


def fix_chapter_paths(text: str, slugs: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        _old_prefix, slug = match.groups()
        new_prefix = slugs.get(slug)
        if new_prefix is None:
            return match.group(0)
        return f"chapters/{new_prefix}-{slug}"

    return re.sub(r"chapters/(ch\d+)-([\w-]+)", repl, text)


def main() -> None:
    slugs = slug_map()
    patterns = ("*.tex", "*.md", "*.yml", "*.py", "*.lean", "*.txt")
    changed = 0
    for pattern in patterns:
        for path in ROOT.rglob(pattern):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            try:
                original = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            updated = fix_chapter_paths(original, slugs)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                changed += 1
    print(f"Fixed chapter paths in {changed} files.")


if __name__ == "__main__":
    main()
