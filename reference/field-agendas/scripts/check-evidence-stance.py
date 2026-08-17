#!/usr/bin/env python3
"""Validate direction/weight fields on reference/field-agendas/data/evidence.yml.

Usage:
  python3 reference/field-agendas/scripts/check-evidence-stance.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EVIDENCE_YML = REPO / "reference" / "field-agendas" / "data" / "evidence.yml"

# Entries with id <= this value may omit direction (legacy backfill pass).
STANCE_REQUIRED_AFTER_ID = 157

VALID_DIRECTIONS = frozenset({"support", "challenge", "unclear"})

DOT = "\u00b7"
CIRCUMFLEX = "\u0302"
CARON_BELOW = "\u032c"

EXPECTED_MARKS = {
    ("support", 1): DOT + CIRCUMFLEX,
    ("support", 2): DOT + CIRCUMFLEX * 2,
    ("support", 3): DOT + CIRCUMFLEX * 3,
    ("challenge", 1): DOT + CARON_BELOW,
    ("challenge", 2): DOT + CARON_BELOW * 2,
    ("challenge", 3): DOT + CARON_BELOW * 3,
    ("unclear", None): DOT,
}


def stance_mark(direction: str | None, weight: int | None = 1) -> str:
    if not direction:
        return ""
    if direction == "support":
        return DOT + CIRCUMFLEX * int(weight or 1)
    if direction == "challenge":
        return DOT + CARON_BELOW * weight
    if direction == "unclear":
        return DOT
    return ""


def check_mark_encoding() -> list[str]:
    errors: list[str] = []
    for (direction, weight), expected in EXPECTED_MARKS.items():
        got = stance_mark(direction, weight or 1) if direction != "unclear" else stance_mark("unclear")
        if got != expected:
            errors.append(f"stance mark mismatch {direction}/{weight}: {got!r} != {expected!r}")
    return errors


def self_test() -> list[str]:
    """Fast smoke cases for validator logic (no evidence.yml I/O)."""
    errors: list[str] = []
    errors.extend(check_mark_encoding())

    sample = [
        {"id": 1, "direction": "support", "weight": 2},
        {"id": 2, "direction": "unclear"},
        {"id": 3, "direction": "challenge", "weight": 3},
    ]
    for entry in sample:
        direction = entry.get("direction")
        weight = entry.get("weight")
        if direction == "unclear" and weight is not None:
            errors.append("self_test: unclear must not carry weight")
        if direction in ("support", "challenge") and weight not in (1, 2, 3):
            errors.append(f"self_test: bad weight on ev-{entry['id']}")

    bad = {"id": 999, "weight": 2}
    if bad.get("direction") is None and bad.get("weight") is not None:
        pass  # rule exercised in main(); self_test documents expectation

    if stance_mark("support", 1) != DOT + CIRCUMFLEX:
        errors.append("self_test: support mark encoding")
    if stance_mark(None) != "":
        errors.append("self_test: empty direction mark")
    return errors


def main() -> int:
    errors = self_test()
    if errors:
        print("evidence-stance self_test FAILED")
        for e in errors:
            print(f"  {e}")
        return 1

    data = yaml.safe_load(EVIDENCE_YML.read_text())
    entries = data.get("evidence") or []

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[int] = set()

    for entry in entries:
        eid = entry.get("id")
        if eid is None:
            errors.append("evidence entry missing id")
            continue
        if eid in seen_ids:
            errors.append(f"ev-{eid}: duplicate id")
        seen_ids.add(eid)

        direction = entry.get("direction")
        weight = entry.get("weight")

        if direction is not None and direction not in VALID_DIRECTIONS:
            errors.append(f"ev-{eid}: invalid direction {direction!r} (expected support|challenge|unclear)")

        if weight is not None:
            if not isinstance(weight, int) or weight not in (1, 2, 3):
                errors.append(f"ev-{eid}: weight must be 1, 2, or 3 (got {weight!r})")

        if direction in ("support", "challenge"):
            if weight is None:
                warnings.append(f"ev-{eid}: direction={direction} without weight (defaults to 1 at render)")
        elif direction == "unclear" and weight is not None:
            errors.append(f"ev-{eid}: weight must not be set when direction is unclear")

        if direction is None and weight is not None:
            errors.append(f"ev-{eid}: weight set without direction")

        if eid > STANCE_REQUIRED_AFTER_ID and direction is None:
            errors.append(
                f"ev-{eid}: direction required on new entries (id > {STANCE_REQUIRED_AFTER_ID})"
            )

    tagged = sum(1 for e in entries if e.get("direction"))
    print(
        f"evidence-stance: {len(entries)} entries, {tagged} tagged, "
        f"require direction on id > {STANCE_REQUIRED_AFTER_ID}"
    )

    if warnings:
        print(f"\n## WARN ({len(warnings)})")
        for w in warnings[:20]:
            print(f"  {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")

    if errors:
        print(f"\n## ERROR ({len(errors)})")
        for e in errors:
            print(f"  {e}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
