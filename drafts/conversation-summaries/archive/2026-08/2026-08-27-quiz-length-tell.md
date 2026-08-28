# 2026-08-27 — Quiz length-tell implementation

## Trigger
User: implement the length-tell check/fix.

## Done
- Rewrote sentence-item options (generators + drafts 01–04) so keyed lines are not uniquely longest by >12 characters.
- `scripts/check_quiz_length_tell.py` now in `make check`.
- Generators assert option length bands on write.
- Gate: 0% margin-fail; unique-longest 44% of sentence items (within 12 chars). Name-like 49.

## Decisions
- Strong authoring: all options in a 12-char band on sentence items; gate remains C vs longest wrong +12.
- Blind 211/211 from before this rewrite is void; re-solve not run in this pass.

## Open / next
- New blind solver round on the rewritten bank (`BLIND_EVAL.md`).

## Key paths
- `site/src/content/quiz/LENGTH_TELL.md`

## Commits
- `bfaa4ceb` Ship the companion-site field quiz with a 5% multi-correct floor.
