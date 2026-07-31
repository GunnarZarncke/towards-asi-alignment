# 2026-07-31 — Conversation-summaries archive and slim index

## Trigger
User: `conversation-summaries` folder too crowded; simplify, remove, compress, or index.

## Done
- Added `scripts/archive_conversation_summaries.py`: moves logs before `2026-07-20` into `archive/YYYY-MM/`, rebuilds slim `INDEX.md`, writes monthly compressed indexes.
- Archived **414** logs (202 in `archive/2026-06/`, 212 in `archive/2026-07/`); **61** remain active in root.
- Replaced 487-line flat `INDEX.md` with ~83 lines (recent table + archive pointers).
- Added `archive/README.md`; updated `drafts/conversation-summaries/README.md` retention policy.
- Updated `AGENTS.md` handoff instructions for archive layout.
- Fixed 18 broken cross-repo path references to archived logs (`metadata/TODO.md`, experiment docs, etc.).

## Decisions
- Archive, do not delete: git has diffs; logs carry decisions git omits.
- Cutoff `2026-07-20` (~2 weeks active): balances resume surface vs folder noise.
- Monthly compressed indexes (one table row per session) instead of deleting old logs.

## Open / next
- Re-run `python3 scripts/archive_conversation_summaries.py` periodically (or after heavy session weeks).
- Optional: raise cutoff or add quarterly rollup if active folder grows past ~80 again.

## Key paths
- `scripts/archive_conversation_summaries.py`
- `drafts/conversation-summaries/INDEX.md`
- `drafts/conversation-summaries/archive/`

## Commits
- (pending)
