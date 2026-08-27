#!/usr/bin/env python3
"""Fail if keyed quiz options are uniquely longest (length tell)."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "site/src/content/quiz/questions.yml"

NAME_LIKE_MAX = 48
MARGIN = 12
MAX_FAIL_FRACTION = 0.25
RATIO_FAIL = 1.5
RATIO_MIN_W = 40


def opt_len(text: str) -> int:
    return len(text or "")


def classify(q: dict) -> str:
    opts = q.get("options") or []
    if not opts:
        return "empty"
    if all(opt_len(o.get("text") or "") < NAME_LIKE_MAX for o in opts):
        return "name-like"
    return "sentence"


def lengths(q: dict) -> tuple[int, int] | None:
    corr = [o for o in (q.get("options") or []) if o.get("correct")]
    wrong = [o for o in (q.get("options") or []) if not o.get("correct")]
    if not corr or not wrong:
        return None
    c = max(opt_len(o.get("text") or "") for o in corr)
    w = max(opt_len(o.get("text") or "") for o in wrong)
    return c, w


def item_fail(c: int, w: int) -> bool:
    return c > w + MARGIN


def ratio_fail(c: int, w: int) -> bool:
    return w >= RATIO_MIN_W and c > RATIO_FAIL * w


def main() -> int:
    questions = yaml.safe_load(QUESTIONS_PATH.read_text(encoding="utf-8")).get("questions") or []
    sentence = []
    name_like = 0
    fails: list[tuple[int, str, int, int]] = []
    ratio_hits: list[str] = []
    unique_longest = 0

    for q in questions:
        kind = classify(q)
        if kind == "name-like":
            name_like += 1
            continue
        if kind != "sentence":
            continue
        lw = lengths(q)
        if not lw:
            continue
        c, w = lw
        sentence.append(q["id"])
        if c > w:
            unique_longest += 1
        if item_fail(c, w):
            fails.append((c - w, q["id"], c, w))
        if ratio_fail(c, w):
            ratio_hits.append(q["id"])

    fails.sort(reverse=True)
    n = max(len(sentence), 1)
    frac = len(fails) / n
    print(f"Questions: {len(questions)}")
    print(f"Name-like (ignored): {name_like}")
    print(f"Sentence items: {len(sentence)}")
    print(f"Unique-longest correct: {unique_longest} ({100 * unique_longest / n:.0f}% of sentence)")
    print(f"Fail margin > {MARGIN} chars: {len(fails)} ({100 * frac:.0f}%; cap {int(MAX_FAIL_FRACTION * 100)}%)")
    print(f"Fail C > {RATIO_FAIL} W (W≥{RATIO_MIN_W}): {len(ratio_hits)}")
    for margin, qid, c, w in fails[:25]:
        print(f"  +{margin}c  {qid}  C={c} W={w}")
    if len(fails) > 25:
        print(f"  ... {len(fails) - 25} more")

    errors = []
    if frac > MAX_FAIL_FRACTION + 1e-9:
        errors.append(
            f"{100 * frac:.0f}% of sentence items have keyed option uniquely longest by >{MARGIN} chars "
            f"(cap {int(MAX_FAIL_FRACTION * 100)}%)"
        )
    if ratio_hits:
        errors.append(f"{len(ratio_hits)} item(s) have C > {RATIO_FAIL}× longest distractor")
    if errors:
        print("\nErrors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("\nLength-tell checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
