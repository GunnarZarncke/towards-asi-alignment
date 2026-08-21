# 2026-08-20 — Housekeeping

## Trigger
User asked for general housekeeping.

## Done
- Ran `python3 scripts/archive_conversation_summaries.py` (15 active logs; prune dry-run found 0 superseded).
- Slimmed `HANDOFF.md` Open work: removed Done/Closed items that duplicated Recently shipped (field v2, consciousness, Krym, six-claims still listed as “Phase 3 next” despite Phases 0–6 shipped).
- Added Anthropic Risk Report news to Recently shipped; fixed Lean appendix letter I→G in the canonical-location table.
- Deleted untracked `experiments/__MACOSX/` (Apple zip sidecar, ~4.3 MB); gitignored `__MACOSX/`.

## Decisions
- Did not delete untracked working drafts (`drafts/anthropic-risk-report-aug-2026-analysis.md`, `drafts/lw-bridges-section.md`, etc.) or root `TSA.png`/`TSA.svg`.
- Did not compact `[x]` narratives in `metadata/TODO.md` (still deferred from `drafts/repo-cleanup-plan.md` Task 6).
- Did not commit.

## Open / next
- Untracked `experiments/value-detect-v1-master/` (and v2) look like unzipped experiment trees; decide keep vs attic vs sibling repo.
- Root `TSA.png` / `TSA.svg` — keep, move to `site/`/`figures/`, or drop.
- Optional: collapse closed TODO narratives (cleanup plan Task 6 leftover).

## Key paths
- `drafts/conversation-summaries/HANDOFF.md`
- `drafts/conversation-summaries/INDEX.md`
- `.gitignore`

## Commits
- none
