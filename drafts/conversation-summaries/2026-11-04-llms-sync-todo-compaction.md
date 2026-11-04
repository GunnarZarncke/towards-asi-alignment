# llms anti-pattern sync + TODO narrative compaction

**kind:** housekeeping · **uptake:** local

## Trigger

User: fix llms.txt sync; run narrative compaction steps.

## Done

- **content:** Matched `llms.txt` and `REVIEWING_FOR_AGENTS.md` Anti-Patterns (nine bullets; cross-ref note; book vs project on first bullet only). Ran `site/scripts/sync-bot-orientation.mjs` → `site/public/llms.txt`, `reviewing-for-agents.md`, `llms-full.txt`.
- **bookkeeping:** `metadata/TODO.md` — removed long `[x]` narratives from Site/Housekeeping boards; rolled 2026-09-23 batch + site quiz/hub/tour into **Closed (one-liners)**; split quiz residual into open **Quiz — chapter-end blocks**; ch46 follow-up as open **Claims-ledger bare-number chapters (S)**.
- **bookkeeping:** `drafts/attic/repo-cleanup-plan.md` — Task 6 llms sync + TODO compaction marked done.

## Verification

- `node site/scripts/sync-bot-orientation.mjs` → wrote public bot-orientation files.
