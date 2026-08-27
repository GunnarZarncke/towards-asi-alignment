# Blind quiz evaluation

How to check that keyed answers are recoverable **without** the book and **without** seeing the key.

**Void:** reviewing items while `correct: true` is visible. **Void:** packets that keep author option ids such as `take` vs `d0`.

## Roles

- **Solver (subagent):** sees prompt + option id/text only. Chooses one or more option ids. Does **not** see `correct`, explanations, source labels, or any TSA manuscript / `context/` / keyed quiz YAML / field-news bodies / `.keys.json`.
- **Scorer (superagent):** does not ask the solver to check a keyed option. After the solver returns, compare selected ids to the key with `scripts/score_quiz_blind.py`. Match = pass. Mismatch = fail (ambiguous item, wrong key, or TSA-private claim).

## Protocol

1. Export blinded packets. Option ids are **opaque and shuffled** (`o0`…`oN`):

   ```bash
   python3 scripts/export_quiz_blind_packets.py
   ```

2. Give **each** solver **one** packet. Solver instructions:

   - Read only that packet file. Do not grep the repo. Do not open `questions.yml` or `.keys.json`.
   - Use general AI-safety / CS / economics knowledge.
   - For each question, list the option **id**(s) you would select. Multi-select only if several look required.
   - Return only `id` + `selected`. Do not assume `o0` is correct.

3. Score (superagent only):

   ```bash
   python3 scripts/score_quiz_blind.py drafts/quiz-blind-packets/answers-batch-*.json
   ```

   Each answers file is a list of `{ "id": "...", "selected": ["oN", ...] }`.
   Keys are in `drafts/quiz-blind-packets/.keys.json` (gitignored).

4. On **fail**, fix the item, then re-blind that item with a **new** solver. Do not show the previous solver the key.

5. Record PASS/FAIL counts in the session log.

Length / joke tells: fix first with [`LENGTH_TELL.md`](LENGTH_TELL.md). A blind pass on uniquely-long keyed lines does not count.

## What this does not replace

- Schema checks (`check_quiz_bank.py`).
- Length-tell gate (`scripts/check_quiz_length_tell.py`, [`LENGTH_TELL.md`](LENGTH_TELL.md)).
- Gunnar wording review vs theses.
- **Harder distractors** — Site board in `metadata/TODO.md` (quiz distractors too easy). Revalidate with a new blind solver round after that rewrite.
