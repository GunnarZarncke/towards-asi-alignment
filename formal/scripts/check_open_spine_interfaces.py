#!/usr/bin/env python3
"""Validate open-spine-interfaces YAML against Lean module files.

Usage (from repo root):
  python3 formal/scripts/check_open_spine_interfaces.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "reference" / "field-agendas" / "data" / "open-spine-interfaces.yml"
FORMAL = REPO / "formal"


def main() -> int:
    if not DATA.is_file():
        print(f"missing {DATA}", file=sys.stderr)
        return 1
    doc = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    interfaces = doc.get("openSpineInterfaces") or []
    errors: list[str] = []
    for iface in interfaces:
        iid = iface.get("id", "?")
        module = iface.get("leanModule")
        if not module:
            errors.append(f"{iid}: missing leanModule")
            continue
        lean_path = FORMAL / f"{module.removesuffix('.lean')}.lean"
        if not lean_path.is_file():
            errors.append(f"{iid}: Lean module not found: {lean_path}")
            continue
        text = lean_path.read_text(encoding="utf-8")
        for name in [iface.get("leanProp"), *iface.get("leanDefs", [])]:
            if not name:
                continue
            if not re.search(
                rf"\b(def|abbrev|structure|theorem|axiom|inductive)\s+{re.escape(name)}\b",
                text,
            ):
                errors.append(f"{iid}: `{name}` not found in {lean_path.name}")
    if errors:
        print("check_open_spine_interfaces: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"check_open_spine_interfaces: OK ({len(interfaces)} interface(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
