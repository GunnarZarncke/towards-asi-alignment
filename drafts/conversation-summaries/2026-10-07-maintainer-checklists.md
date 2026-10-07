# 2026-10-07 — Maintainer checklists + quiz CI fix

kind: new-work
uptake: rule

## Trigger
User: build failed (`make check`, quiz bank); then asked for maintainer doc listing action→follow-up rules from conversation logs; end of session commit.
Prompts: paraphrase (no telemetry id in this session)

## Done
- content: **`news-takeaway-ward-monitoring-oct-2026`** in quiz bank; generator updated (`scripts/attic/write_news_takeaway_quiz.py`). Verified `make check` pass.
- content: Added [`docs/MAINTAINER.md`](../../docs/MAINTAINER.md) — field news→quiz, symbols→graphs, predictions, bibliography, cards, chapters, experiments, releases, field hub, quiz constraints, `make check` gate map, CI failure quick reference.
- housekeeping: Linked from [`docs/BUILD.md`](../../docs/BUILD.md), [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md) (human docs + field-news card table); header comment on [`metadata/field-news.yml`](../../metadata/field-news.yml).

## Decisions
- Consolidate in `docs/MAINTAINER.md` — pointers to deep docs, no lane-plan duplication.
- Field news→quiz called out first (highest-frequency CI miss in logs since 2026-09-19).

## Open / next
- Tag `v1.7.0` and fill `RELEASE_NOTES.md` commit hash when author approves notes (see `2026-10-07-v1-7-0-release-notes.md`).

## Key paths
- `docs/MAINTAINER.md`
- `scripts/check_quiz_bank.py`
- `scripts/attic/write_news_takeaway_quiz.py`

## Commits
- `eb6bf89de` Add quiz takeaway for Ward monitoring field news so make check passes.
- (pending) Add maintainer checklists (`RELEASE_NOTES.md` left unstaged — still in author edit).
