#!/usr/bin/env python3
"""Verify the six-claim spine artifacts stay in sync."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INTRO = ROOT / "frontmatter" / "introduction.tex"
CONCEPTS = ROOT / "metadata" / "concepts.yml"

CLAIM_LABELS = [
    "claim:boundary",
    "claim:value-bundle",
    "claim:grounding",
    "claim:correction",
    "claim:successor",
    "claim:basin",
]

REQUIRED_TABLES = [
    "tables/claim-spine.tex",
    "tables/claim-layer-map.tex",
    "tables/claim-status-ch48.tex",
]

PART_CLAIM_RE = re.compile(
    r"(Claims?~\\ref\{claim:[^}]+\}|Section~\\ref\{sec:(?:how-claims-unfold|opening-claims-revisited-ch48)\})"
)


def main() -> int:
    errors: list[str] = []

    if not INTRO.exists():
        errors.append(f"Missing {INTRO.relative_to(ROOT)}")
    else:
        intro_text = INTRO.read_text(encoding="utf-8")
        for label in CLAIM_LABELS:
            if f"\\label{{{label}}}" not in intro_text:
                errors.append(f"Introduction missing \\label{{{label}}}")
        if "\\label{sec:how-claims-unfold}" not in intro_text:
            errors.append("Introduction missing \\label{sec:how-claims-unfold}")

    for rel in REQUIRED_TABLES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required table: {rel}")

    if not CONCEPTS.exists():
        errors.append(f"Missing {CONCEPTS.relative_to(ROOT)}")
    elif "slug: six-thesis-claims" not in CONCEPTS.read_text(encoding="utf-8"):
        errors.append("metadata/concepts.yml missing six-thesis-claims card")

    parts_dir = ROOT / "parts"
    if parts_dir.is_dir():
        for part_file in sorted(parts_dir.glob("part*.tex")):
            text = part_file.read_text(encoding="utf-8")
            if not PART_CLAIM_RE.search(text):
                errors.append(
                    f"{part_file.relative_to(ROOT)} does not reference an intro claim"
                )

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Claim spine check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
