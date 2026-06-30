#!/usr/bin/env python3
"""Ensure every references/*.bib entry has a one-line summary in bibliography-summaries.tex."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARIES_PATH = ROOT / "references" / "bibliography-summaries.tex"
KEY_RE = re.compile(r"@\w+\{([^,]+),")
SUMMARY_RE = re.compile(r"\\bibsummary\{([^}]+)\}\{([^}]*)\}")


def load_bib_keys() -> set[str]:
    keys: set[str] = set()
    for bib in (ROOT / "references").glob("*.bib"):
        keys.update(KEY_RE.findall(bib.read_text(encoding="utf-8", errors="replace")))
    return keys


def load_summaries() -> dict[str, str]:
    text = SUMMARIES_PATH.read_text(encoding="utf-8")
    return {key: body for key, body in SUMMARY_RE.findall(text)}


def main() -> int:
    if not SUMMARIES_PATH.is_file():
        print(f"Missing {SUMMARIES_PATH}", file=sys.stderr)
        return 1

    keys = load_bib_keys()
    summaries = load_summaries()
    missing = sorted(keys - summaries.keys())
    orphan = sorted(summaries.keys() - keys)

    if missing:
        print("Bibliography keys without a \\bibsummary line:", file=sys.stderr)
        for key in missing:
            print(f"  - {key}", file=sys.stderr)
    if orphan:
        print("Orphan \\bibsummary keys (no matching .bib entry):", file=sys.stderr)
        for key in orphan:
            print(f"  - {key}", file=sys.stderr)

    if missing or orphan:
        print(
            "\nAdd or fix entries in references/bibliography-summaries.tex "
            "(see references/README.md and AGENTS.md).",
            file=sys.stderr,
        )
        return 1

    print(
        f"Bibliography summary check passed ({len(summaries)} summaries for {len(keys)} bib keys)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
