# 2026-08-27 — Blind quiz solver protocol

## Trigger
User: prior “blind” check was not blinded. Solver must **choose** answers without knowing the key and without TSA material; superagent only scores match vs expectation. Document protocol; rerun all evaluations.

## Done
- Protocol: [`site/src/content/quiz/BLIND_EVAL.md`](../../site/src/content/quiz/BLIND_EVAL.md).
- Export/score: `scripts/export_quiz_blind_packets.py`, `scripts/score_quiz_blind.py`. Packets under `drafts/quiz-blind-packets/` (opaque shuffled `o0`… ids). `.keys.json` gitignored.
- First solver round **voided**: packets still used author ids `take`/`d0` (key leak).
- Second round: eight solvers, one packet each, TSA files forbidden; scorer compared to keys only after answers were written.
- Result: **211 / 211 PASS**, 0 FAIL. Selected-id histogram roughly uniform (`o0`–`o3`), so solvers were not always picking `o0`.

## Decisions
- Looking at `correct: true` and asking “is this keyed option sound?” is **not** this protocol.
- A pass here does **not** mean distractors are good; many items are still non-joke vs joke, which a field-literate solver will always hit.

## Open / next
- Near-miss distractor rewrite, then a **new** solver round on changed items only.

## Key paths
- `site/src/content/quiz/BLIND_EVAL.md`

## Commits
- none
