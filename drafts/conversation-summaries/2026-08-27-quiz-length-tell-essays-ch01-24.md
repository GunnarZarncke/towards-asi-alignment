# 2026-08-27 — Quiz length tell (essays + ch01–ch24)

## Trigger
Length-tell fix for essay takeaways and `chapter()` entries ch01–ch24 only. Do not change ch25–ch48 in this pass.

## Done
- Rewrote options in `scripts/write_takeaway_quiz.py` for the 11 essay items and takeaway-ch01–ch24.
- Same grammatical frame per item; “— not only …” glosses moved into `explanation`; distractors are near-miss alignment claims.
- Per item, `max(len)-min(len)` of the four option strings is ≤ 12. Correct option ids unchanged.
- Regenerated `site/src/content/quiz/drafts/00-00-takeaways.yml`. Left ch25–ch48 as already rewritten in the sibling pass.

## Decisions
- Stricter band than the unique-longest gate: all four options within 12 characters of each other.

## Open / next
- Merge drafts if the live bank should pick this up; news takeaways and other sentence items still fail the bank gate.
- New blind solvers on rewritten packets.

## Key paths
- `scripts/write_takeaway_quiz.py`
- `site/src/content/quiz/LENGTH_TELL.md`

## Commits
- none
