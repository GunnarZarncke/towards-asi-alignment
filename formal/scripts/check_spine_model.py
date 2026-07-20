#!/usr/bin/env python3
"""Verify SpineModel bridge-independence checklist completeness.

Ensures `AlignmentProofSpine/SpineModel.lean` exports exactly one
`*_independently_load_bearing` theorem per labeled bridge in the credibility
plan (P3), plus `spine_axioms_consistent` and `spine_axioms_nontrivial`.

Usage (from repo root or formal/):
    python3 scripts/check_spine_model.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FORMAL_ROOT = Path(__file__).resolve().parent.parent
SPINE_MODEL = FORMAL_ROOT / "AlignmentProofSpine" / "SpineModel.lean"

REQUIRED_INDEPENDENCE = [
    "MB1_independently_load_bearing",
    "MB2_independently_load_bearing",
    "MB3_independently_load_bearing",
    "MB4_independently_load_bearing",
    "MB4a_independently_load_bearing",
    "MB5_independently_load_bearing",
    "MB6a_independently_load_bearing",
    "MB6b_independently_load_bearing",
    "MB7a_independently_load_bearing",
    "MB7b_independently_load_bearing",
    "MB7c_independently_load_bearing",
    "MB7d_independently_load_bearing",
    "MB8_independently_load_bearing",
    "MB9_independently_load_bearing",
    "MB10_independently_load_bearing",
    "MB11_independently_load_bearing",
    "s10_blanket_coherence_independently_load_bearing",
    "within_deployment_risk_tolerance_independently_load_bearing",
]

REQUIRED_CONSISTENCY = [
    "spine_axioms_consistent",
    "spine_axioms_nontrivial",
]

THEOREM_RE = re.compile(r"^\s*theorem\s+(\w+)", re.MULTILINE)


def main() -> int:
    if not SPINE_MODEL.is_file():
        print(f"ERROR: missing {SPINE_MODEL}", file=sys.stderr)
        return 1

    text = SPINE_MODEL.read_text(encoding="utf-8")
    found = set(THEOREM_RE.findall(text))

    missing_indep = [n for n in REQUIRED_INDEPENDENCE if n not in found]
    missing_cons = [n for n in REQUIRED_CONSISTENCY if n not in found]

    if missing_indep or missing_cons:
        if missing_indep:
            print("Missing bridge independence theorems:", file=sys.stderr)
            for n in missing_indep:
                print(f"  - {n}", file=sys.stderr)
        if missing_cons:
            print("Missing consistency/export theorems:", file=sys.stderr)
            for n in missing_cons:
                print(f"  - {n}", file=sys.stderr)
        return 1

    print(
        f"SpineModel check passed ({len(REQUIRED_INDEPENDENCE)} bridge independence "
        f"theorems + {len(REQUIRED_CONSISTENCY)} consistency exports)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
