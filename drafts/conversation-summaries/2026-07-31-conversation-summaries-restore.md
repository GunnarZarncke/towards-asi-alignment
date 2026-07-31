# 2026-07-31 — Restore conversation summaries; selective supersession prune

## Trigger
User: mass deletion of all 476 session logs was not intended (Cursor revert failed). Restore from git; prune only logs **superseded by later conversation logs**, not because work landed in code.

## Done
- Restored `drafts/conversation-summaries/` from git (`3b5c2ac0` state): ~460 session logs in root + archive.
- Replaced `scripts/compress_conversation_summaries.py` (delete-all) with:
  - `scripts/prune_superseded_conversation_logs.py` — conservative manual pairs + explicit supersession cues only.
  - `scripts/archive_conversation_summaries.py` — roll to `archive/YYYY-MM/`, keep 15 newest in root (no deletion).
  - `scripts/fix_conversation_log_references.py` — repair broken `RECOVERY.md (session …)` links.
- Pruned **11** superseded logs (field-news partials → tier A/B; ET-1 intermediates → lockstep conclusion; lab-sim freeze chain; graded-lab v4 plan → freeze log). New slim `RECOVERY.md` lists only these.
- Rewrote `HANDOFF.md`, `README.md`, `AGENTS.md` — per-session logs are normal handoff; RECOVERY is pruned-only.
- Fixed 41+ cross-refs in `metadata/TODO.md`, NEGATIVE_RESULTS, review docs, `PLAN_ET1.md`, `run_phase6.py`.

## Decisions
- **Keep** chapter-draft, session-end, and micro-logs even when integrated in repo — unless a later session explicitly supersedes.
- **Delete** only with curated pairs or auto-detect when a later log says "superseded" near a cite, or ET-1 "line stopped" closure cites earlier ET-1 logs.
- HANDOFF remains thematic rollup + open work; not a replacement for per-session logs.

## Open / next
- Optional: expand manual supersession pairs as patterns emerge (dry-run first).
- `2026-07-31-conversation-summaries-archive.md` describes the earlier (wrong) compression pass — keep as history.

## Commits
- (this session — see below)
