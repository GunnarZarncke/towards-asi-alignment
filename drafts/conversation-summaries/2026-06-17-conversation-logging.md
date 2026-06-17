# 2026-06-17 — Conversation logging

## Trigger

User requested a **durable record of what was worked on and why** from each agent conversation, logged in a project folder and referenced from `AGENTS.md` so later runs can resume where a previous session stopped.

## Done

- Established `drafts/conversation-summaries/` as the conversation log folder (matches `INSTRUCTIONS.md` §8 layout).
- Added `README.md` (format, template, handoff rules) and `INDEX.md` (chronological index).
- Backfilled log for the scaffold session: `2026-06-17-init-scaffold.md`.
- Added this log for the logging setup itself.
- Updated `AGENTS.md` with a **Conversation continuity** section (read latest log before work; append log before ending).

## Decisions

- **Location:** `drafts/conversation-summaries/` — already in the prescribed repo structure; avoids a parallel folder name.
- **Handoff source of truth:** Logs supersede chat history for resume context; `INDEX.md` points to the latest entry.
- **When to log:** End of every session that changes the repo or makes drafting/project decisions, even if the user does not ask.

## Open / next

- Second milestone drafting (see `2026-06-17-init-scaffold.md`).
- Future agents should append a new dated log and update `INDEX.md` at session end.
- User may want this commit pushed or the logging rule mirrored in `INSTRUCTIONS.md` (not done unless asked).

## Key paths

- `drafts/conversation-summaries/INDEX.md` — start here when resuming
- `AGENTS.md` — conversation continuity rules
- `metadata/book.yml` — manuscript progress

## Commits

- Folded into `init: create full book scaffold` on `main` (use `git log -1` for hash)
