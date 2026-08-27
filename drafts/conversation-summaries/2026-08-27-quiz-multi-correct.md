# 2026-08-27 — Quiz multi-correct floor

## Trigger
The bank keyed lists of people as a single option; readers never saw more than one correct checkbox. Target ≥5% multi-correct.

## Done
- Split bundled keys in drafts (`01`–`04`) into separate `correct: true` options; added “(Select all that apply.)”.
- `check_quiz_bank.py` now fails if multi-correct share is under 5%. Merged bank: **12 / 211 (5.7%)**.

## Decisions
Natural splits only: coauthor lists, HELM metrics vs scenarios, Christiano two failure shapes, GSAI spec + world model, RSP thresholds + commitments, Goodhart three types, Hendrycks four areas, MIRI pause + off-switch. Did not mark extra authors on lead-author prompts.

## Open / next
Harder distractors / re-blind still on the site board.

## Key paths
- `site/src/content/quiz/drafts/`
- `scripts/check_quiz_bank.py`

## Commits
- (pending)
