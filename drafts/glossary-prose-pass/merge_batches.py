#!/usr/bin/env python3
"""Merge glossary-prose-pass batch files into inter-agenda-term-glossary.md.

Usage (from repo root):
  python3 drafts/glossary-prose-pass/merge_batches.py --dry-run
  python3 drafts/glossary-prose-pass/merge_batches.py --apply
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GLOSSARY = REPO / "reference/field-agendas/inter-agenda-term-glossary.md"
BATCH_DIR = Path(__file__).resolve().parent
BATCH_FILES = [
    "batch-A-C.md",
    "batch-D-I.md",
    "batch-K-R.md",
    "batch-S-W.md",
]

HEAD_RE = re.compile(r"^#### (.+)$", re.M)
ENTRY_RE = re.compile(
    r"^(#### .+?\n\n\| \| \|\n\|---\|---\|\n(?:\| \*\*[^*]+\*\* \| .*?\n)+)",
    re.M,
)


def extract_entries(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    # Split on #### headings; keep only blocks that look like glossary tables
    parts = re.split(r"(?=^#### )", text, flags=re.M)
    for part in parts:
        m = HEAD_RE.match(part.strip())
        if not m:
            continue
        title = m.group(1).strip()
        if "| **Sources** |" not in part:
            continue
        # Trim trailing blank lines / following section junk
        block = part.strip() + "\n"
        entries[title] = block
    return entries


def replace_entries(glossary: str, replacements: dict[str, str]) -> tuple[str, list[str], list[str]]:
    missing: list[str] = []
    applied: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        title = match.group(1)
        if title in replacements:
            applied.append(title)
            return replacements[title].rstrip() + "\n"
        return match.group(0)

    # Match from #### title through next #### or ### or EOF
    pattern = re.compile(
        r"^#### (.+?)\n(?:.*?)(?=^#### |^### |\Z)",
        re.M | re.S,
    )
    new_text, n = pattern.subn(replacer, glossary)
    for title in replacements:
        if title not in applied:
            missing.append(title)
    return new_text, applied, missing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    replacements: dict[str, str] = {}
    for name in BATCH_FILES:
        path = BATCH_DIR / name
        if not path.exists():
            print(f"MISSING batch: {path}")
            continue
        found = extract_entries(path.read_text())
        print(f"{name}: {len(found)} entries")
        overlap = set(replacements) & set(found)
        if overlap:
            print(f"  WARNING overlap: {sorted(overlap)[:5]}...")
        replacements.update(found)

    glossary = GLOSSARY.read_text()
    new_text, applied, missing = replace_entries(glossary, replacements)
    print(f"Would apply: {len(applied)}; missing in glossary: {len(missing)}")
    if missing:
        print("  missing titles:", ", ".join(missing[:20]), ("..." if len(missing) > 20 else ""))
    if args.apply:
        GLOSSARY.write_text(new_text)
        print(f"Wrote {GLOSSARY}")
    else:
        print("Dry run only; pass --apply to write.")


if __name__ == "__main__":
    main()
