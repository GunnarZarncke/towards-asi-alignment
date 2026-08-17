#!/usr/bin/env python3
"""Validate specify-construct-instances YAML against Lean names in AlignmentConstruction.lean.

Usage (from repo root):
  python3 formal/scripts/check_specify_construct_instances.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "reference" / "field-agendas" / "data" / "specify-construct-instances.yml"
LEAN = REPO / "formal" / "AlignmentProofSpine" / "AlignmentConstruction.lean"


def lean_names(text: str) -> set[str]:
    pattern = re.compile(
        r"\b(?:def|abbrev|structure|theorem|axiom)\s+([A-Za-z_][A-Za-z0-9_]*)"
    )
    return set(pattern.findall(text))


def main() -> int:
    if not DATA.is_file():
        print(f"missing {DATA}", file=sys.stderr)
        return 1
    if not LEAN.is_file():
        print(f"missing {LEAN}", file=sys.stderr)
        return 1

    doc = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    known = lean_names(LEAN.read_text(encoding="utf-8"))
    agenda_dir = REPO / "reference" / "field-agendas" / "data" / "agendas"
    agenda_slugs = {p.stem for p in agenda_dir.glob("*.yml")}
    errors: list[str] = []

    for row in doc.get("instances") or []:
        rid = row.get("id", "?")
        for slug in row.get("agendaSlugs") or []:
            if slug not in agenda_slugs:
                errors.append(f"{rid}.agendaSlugs: `{slug}` not in reference/field-agendas/data/agendas/")
        for side in ("specify", "construct"):
            block = row.get(side) or {}
            for key in ("lean", "pair"):
                name = block.get(key)
                if name and name not in known:
                    errors.append(f"{rid}.{side}.{key}: `{name}` not in AlignmentConstruction.lean")

    for row in doc.get("peerRows") or []:
        rid = row.get("id", "?")
        for slug in row.get("agendaSlugs") or []:
            if slug not in agenda_slugs:
                errors.append(f"peer {rid}.agendaSlugs: `{slug}` not in reference/field-agendas/data/agendas/")
        # peer rows are catalog-only; no Lean binding required

    if errors:
        print("check_specify_construct_instances: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    n = len(doc.get("instances") or [])
    print(f"check_specify_construct_instances: OK ({n} instance(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
