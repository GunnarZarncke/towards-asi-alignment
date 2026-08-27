#!/usr/bin/env python3
"""Validate quiz question bank: schema, bridge coverage, unique ids."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_quiz_length_tell import MARGIN, classify, item_fail, lengths
QUESTIONS_PATH = ROOT / "site/src/content/quiz/questions.yml"
BRIDGE_IDS = [
    "MB1",
    "MB2",
    "MB3",
    "MB4",
    "MB4a",
    "MB5",
    "MB6",
    "MB7",
    "MB7a",
    "MB7b",
    "MB7c",
    "MB7d",
    "MB8",
    "MB9",
    "MB10",
    "MB11",
]
MIN_PER_BRIDGE = 2
MAX_PEOPLE_ORG_FRACTION = 0.20
MIN_MULTI_CORRECT_FRACTION = 0.05

PEOPLE_ORG_PROMPT = re.compile(
    r"^(Who |Which (author|economist|researcher|research group|organization|lab|conference|venue)\b|"
    r"Who (is|are|wrote|introduced|developed|authored|proposed|published|co-authored|popularized|led|maintains)\b)",
    re.I,
)


def main() -> int:
    raw = QUESTIONS_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    questions = data.get("questions") or []
    errors: list[str] = []
    ids: set[str] = set()

    for q in questions:
        qid = q.get("id")
        if not qid:
            errors.append("Question missing id")
            continue
        if qid in ids:
            errors.append(f"Duplicate id: {qid}")
        ids.add(qid)
        if not q.get("prompt"):
            errors.append(f"{qid}: missing prompt")
        if not q.get("options"):
            errors.append(f"{qid}: missing options")
        else:
            for opt in q["options"]:
                text = opt.get("text")
                if not isinstance(text, str) or not text.strip():
                    errors.append(f"{qid}: option {opt.get('id')!r} missing text (YAML comma/paren split?)")
                elif text.rstrip().endswith("("):
                    errors.append(f"{qid}: option text looks truncated: {text!r}")
                extra_keys = [k for k in opt.keys() if k not in {"id", "text", "correct"}]
                if extra_keys:
                    errors.append(f"{qid}: unexpected option keys {extra_keys} (unquoted YAML?)")
            correct = [o for o in q["options"] if o.get("correct")]
            if not correct:
                errors.append(f"{qid}: no correct option")
        topics = q.get("topics") or []
        if len(topics) != 1:
            errors.append(f"{qid}: expected exactly one primary topic, got {topics}")
        elif topics[0] not in BRIDGE_IDS:
            errors.append(f"{qid}: unknown topic {topics[0]}")

    bridge_counts = Counter()
    for q in questions:
        if q.get("topics"):
            bridge_counts[q["topics"][0]] += 1

    print(f"Questions: {len(questions)}")
    print("Bridge coverage:")
    for bridge in BRIDGE_IDS:
        count = bridge_counts.get(bridge, 0)
        flag = "OK" if count >= MIN_PER_BRIDGE else "LOW"
        print(f"  {bridge}: {count} [{flag}]")
        if count < MIN_PER_BRIDGE:
            errors.append(f"{bridge}: only {count} question(s), need {MIN_PER_BRIDGE}")

    people = [q for q in questions if PEOPLE_ORG_PROMPT.search((q.get("prompt") or "").lstrip())]
    frac = len(people) / max(len(questions), 1)
    print(f"People/org prompts: {len(people)} / {len(questions)} ({100 * frac:.0f}%; cap {int(MAX_PEOPLE_ORG_FRACTION * 100)}%)")
    if frac > MAX_PEOPLE_ORG_FRACTION + 1e-9:
        errors.append(
            f"people/org questions are {100 * frac:.0f}% of the bank; keep at most {int(MAX_PEOPLE_ORG_FRACTION * 100)}%"
        )

    multi = [
        q
        for q in questions
        if sum(1 for o in (q.get("options") or []) if o.get("correct")) > 1
    ]
    multi_frac = len(multi) / max(len(questions), 1)
    print(
        f"Multi-correct prompts: {len(multi)} / {len(questions)} "
        f"({100 * multi_frac:.1f}%; floor {int(MIN_MULTI_CORRECT_FRACTION * 100)}%)"
    )
    if multi_frac + 1e-9 < MIN_MULTI_CORRECT_FRACTION:
        errors.append(
            f"multi-correct questions are {100 * multi_frac:.1f}% of the bank; "
            f"need at least {int(MIN_MULTI_CORRECT_FRACTION * 100)}%"
        )

    sent = uniq = margin_fail = 0
    for q in questions:
        if classify(q) != "sentence":
            continue
        sent += 1
        lw = lengths(q)
        if not lw:
            continue
        c, w = lw
        if c > w:
            uniq += 1
        if item_fail(c, w):
            margin_fail += 1
    if sent:
        print(
            f"Length tell (sentence items): unique-longest {uniq}/{sent} "
            f"({100 * uniq / sent:.0f}%); margin>{MARGIN} {margin_fail}/{sent} "
            f"({100 * margin_fail / sent:.0f}%) — gate: python3 scripts/check_quiz_length_tell.py"
        )

    essay_slugs = [
        p.stem
        for p in (ROOT / "site/src/content/cards").glob("*.md")
        if re.search(r"^type:\s*essay\s*$", p.read_text(), re.M)
    ]
    takeaway_ids = {
        q["id"]
        for q in questions
        if "takeaway" in (q.get("tags") or [])
    }
    by_appear: dict[str, list] = {}
    for q in questions:
        for tag in q.get("appearOn") or []:
            by_appear.setdefault(tag, []).append(q)

    print("Takeaway-tagged questions:", len(takeaway_ids))
    for slug in sorted(essay_slugs):
        key = f"essay:{slug}"
        hits = by_appear.get(key, [])
        if not hits:
            errors.append(f"no quiz questions appearOn {key}")
        elif not any("takeaway" in (q.get("tags") or []) for q in hits):
            errors.append(f"{key}: has questions but none tagged takeaway")
    for i in range(1, 49):
        key = f"chapter:ch{i:02d}"
        hits = by_appear.get(key, [])
        if not hits:
            errors.append(f"no quiz questions appearOn {key}")
        elif not any("takeaway" in (q.get("tags") or []) for q in hits):
            errors.append(f"{key}: has questions but none tagged takeaway")

    news_yml = ROOT / "metadata/field-news.yml"
    news_data = yaml.safe_load(news_yml.read_text(encoding="utf-8"))
    news_slugs = [e["slug"] for e in (news_data.get("fieldNews") or [])]
    for slug in news_slugs:
        qid = "news-takeaway-" + slug.removeprefix("field-news-")
        match = next((q for q in questions if q.get("id") == qid), None)
        if not match:
            errors.append(f"missing news-takeaway question {qid}")
            continue
        appear = match.get("appearOn") or []
        if any(tag.startswith("news:") or tag.startswith("field-news") for tag in appear):
            errors.append(f"{qid}: must not appearOn a news card; use chapter:*")
        if not any(tag.startswith("chapter:") for tag in appear):
            errors.append(f"{qid}: needs appearOn chapter:* so it shows on the manuscript quiz block")

    if errors:
        print("\nErrors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
