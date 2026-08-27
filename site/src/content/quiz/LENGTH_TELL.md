# Quiz length tell

The keyed option must not be findable by picking the longest line.

Blind solvers already do that when distractors are jokes. Length is a second, independent leak.

## Metric

For each question:

- `C` = character length of the longest **correct** option (Unicode length of `text`, no YAML escapes).
- `W` = character length of the longest **incorrect** option.
- **Unique-longest tell:** `C > W`.
- **Margin:** `C - W`.
- **Name-like item:** every option is shorter than 48 characters (person, paper, org). Length among names is ignored; do not pad names with epithets.

**Sentence items** are the rest. Those are the gate.

Report:

```bash
python3 scripts/check_quiz_length_tell.py
```

## Gate (sentence items)

An item **fails** if `C > W + 12` (more than 12 characters uniquely longest).

The **bank** fails if more than **25%** of sentence items fail, or if any item has `C > 1.5 W` with `W ≥ 40`.

`make check` includes `python3 scripts/check_quiz_length_tell.py`.

## Fix (rewrite, do not pad)

Work in the **draft** YAML (or the takeaway generators), then `python3 scripts/merge_quiz_drafts.py`.

Per failing item, in order:

1. **Same frame.** Every option uses the same opener and grammar as the keyed line (`Whether…`, `Treat… as…`, a full sentence). Mixed fragments vs paragraphs is itself a tell.
2. **Move glosses off the keyed line.** Clauses like “— not only X” belong in `explanation`, not in the option. Shorten the keyed claim to one sentence.
3. **Near-miss distractors at keyed length.** Each wrong option is a real competing view (wrong object, wrong checkpoint, wrong evidence type), written to within **12 characters** of `C`. Prefer matching `C` by adding a false mechanism, not adjectives.
4. **Forbidden padding.** Do not append “in this particular case”, “from a certain point of view”, or repeated hedges to make the count.
5. **Forbidden jokes** as the only short lines (font, dark theme, prime numbers). A joke may exist only if it is as long as the others and still clearly wrong.

Stop when `check_quiz_length_tell.py` exits 0.

## Verify after a rewrite batch

1. Length gate green on the touched ids.
2. **New** blind solvers on those packets only (`site/src/content/quiz/BLIND_EVAL.md`). Old 211/211 does not carry over: it was partly a length/joke solve.
3. Spot-check that a distractor is not accidentally true (multi-key).

## Authoring default

When writing a new item, draft **four options of one length band** before marking which is correct. If the keyed line is still uniquely longest, the item is not done.
