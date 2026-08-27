#!/usr/bin/env python3
"""Merge quiz draft YAML batches into site/src/content/quiz/questions.yml."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "site/src/content/quiz/drafts"
OUT = ROOT / "site/src/content/quiz/questions.yml"

# Drop near-duplicates; primary id kept elsewhere.
SKIP_IDS = {
    "embedded-agency-sequence",
    "embedded-agency-paper-year",
    "mesa-optimizer-coiner",
    "hubinger-mesa-optimizer",
    "off-switch-game-venue",
    "cirl-venue-authors",
    "debate-paper-authors",
    "irving-debate-2018",
    "elk-arc-report",
    "yudkowsky-cev-2004",
    "amodei-concrete-problems",
    "alignment-faking-authors",
    "constitutional-ai-mechanism",
    "tiling-agents-author",
    "dalrymple-gsai-components",
    "kelly-goal-structuring",
    "goodhart-monetary-origin",
    "goodhart-law-statement",
    "hubinger-mesa-optimizer",
    "dennett-intentional-stance-book",
}

# Append appearOn from secondary id onto primary, then drop secondary.
MERGE_APPEAR_ON: dict[str, str] = {
    "off-switch-game-venue": "off-switch-game-authors",
    "cirl-venue-authors": "cirl-framework-authors",
    "debate-paper-authors": "debate-oversight-paper",
    "irving-debate-2018": "debate-oversight-paper",
    "elk-arc-report": "elk-problem-arc",
    "yudkowsky-cev-2004": "cev-author-year",
    "amodei-concrete-problems": "concrete-problems-paper",
    "tiling-agents-author": "yudkowsky-tiling-agents",
    "dalrymple-gsai-components": "gsai-core-triple",
    "kelly-goal-structuring": "kelly-gsn-purpose",
    "embedded-agency-paper-year": "embedded-agency-lead-author",
    "embedded-agency-sequence": "embedded-agency-lead-author",
    "mesa-optimizer-coiner": "mesa-optimizer-paper",
    "hubinger-mesa-optimizer": "mesa-optimizer-paper",
    "constitutional-ai-mechanism": "bai-constitutional-ai",
    "alignment-faking-authors": "greenblatt-alignment-faking",
    "goodhart-monetary-origin": "goodhart-law-namesake",
    "goodhart-law-statement": "goodhart-law-namesake",
}


def _str_representer(dumper: yaml.Dumper, data: str):
    if any(ch in data for ch in ",:{}[]#&*!|>'\"%@`") or data.strip() != data or "\n" in data:
        style = "|" if "\n" in data else '"'
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, _str_representer)


def _dump_questions(questions: list[dict]) -> str:
    return yaml.dump({"questions": questions}, sort_keys=False, allow_unicode=True, width=100)


def load_questions(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return data.get("questions") or []


def main() -> int:
    by_id: dict[str, dict] = {}
    order: list[str] = []

    for path in sorted(DRAFTS.glob("*.yml")):
        for q in load_questions(path):
            qid = q["id"]
            if qid in SKIP_IDS:
                continue
            if qid not in by_id:
                by_id[qid] = q
                order.append(qid)
            else:
                existing = by_id[qid]
                for tag in q.get("appearOn") or []:
                    tags = existing.setdefault("appearOn", [])
                    if tag not in tags:
                        tags.append(tag)

    for secondary, primary in MERGE_APPEAR_ON.items():
        if secondary not in by_id or primary not in by_id:
            continue
        sec = by_id.pop(secondary)
        order.remove(secondary)
        primary_q = by_id[primary]
        for tag in sec.get("appearOn") or []:
            tags = primary_q.setdefault("appearOn", [])
            if tag not in tags:
                tags.append(tag)

    questions = [by_id[qid] for qid in order]
    OUT.write_text(_dump_questions(questions), encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
