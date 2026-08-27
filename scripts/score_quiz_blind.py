#!/usr/bin/env python3
"""Score solver answers against keys. Usage: score_quiz_blind.py answers.json"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYS = ROOT / "drafts/quiz-blind-packets/.keys.json"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: score_quiz_blind.py answers.json [answers2.json ...]", file=sys.stderr)
        return 2
    keys = json.loads(KEYS.read_text(encoding="utf-8"))
    answers: dict[str, list[str]] = {}
    for arg in sys.argv[1:]:
        data = json.loads(Path(arg).read_text(encoding="utf-8"))
        if isinstance(data, dict) and "answers" in data:
            data = data["answers"]
        for row in data:
            answers[row["id"]] = list(row["selected"])

    missing_key = [i for i in answers if i not in keys]
    missing_ans = [i for i in keys if i not in answers]
    fail = []
    pass_ids = []
    for qid, selected in answers.items():
        if qid not in keys:
            continue
        want = set(keys[qid])
        got = set(selected)
        if want == got:
            pass_ids.append(qid)
        else:
            fail.append({"id": qid, "expected": sorted(want), "got": sorted(got)})

    print(f"Scored {len(answers)} answers against {len(keys)} keys")
    print(f"PASS {len(pass_ids)}")
    print(f"FAIL {len(fail)}")
    if missing_ans:
        print(f"UNANSWERED {len(missing_ans)}")
    if missing_key:
        print(f"UNKNOWN IDS {missing_key}")
    for row in fail:
        print(f"  FAIL {row['id']}: expected {row['expected']} got {row['got']}")
    if missing_ans:
        print("Unanswered ids:")
        for qid in missing_ans:
            print(f"  {qid}")
    out = ROOT / "drafts/quiz-blind-packets/last-score.json"
    out.write_text(
        json.dumps({"pass": pass_ids, "fail": fail, "unanswered": missing_ans}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 1 if fail or missing_ans or missing_key else 0


if __name__ == "__main__":
    raise SystemExit(main())
