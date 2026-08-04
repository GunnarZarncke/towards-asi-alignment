# Conversation summaries

Agent session logs for **towards-asi-alignment**. Each file records what was worked on, why, what was decided, and what remains open so a later run can resume without re-deriving context.

## Picking up work

1. Read **[HANDOFF.md](HANDOFF.md)** (aggregated themes and open work).
2. Skim **[INDEX.md](INDEX.md)** for recent sessions; dig into relevant logs or **[archive/](archive/README.md)**.
3. Check `metadata/book.yml` for chapter status.
4. Read `AGENTS.md` and the relevant `INSTRUCTIONS.md` section for the task at hand.

Do not treat chat history as durable; **this folder is the handoff record**.

## When to write a log

At the **end of every agent conversation** that changes the repo, drafts manuscript text, or makes project decisions — even if the user does not ask explicitly.

## Filename convention

```text
YYYY-MM-DD-short-topic.md
```

Use a short kebab-case topic (e.g. `init-scaffold`, `ch01-draft`, `build-fix`). If two sessions share a day, append `-2`, `-3`, etc.

## Log template

```markdown
# YYYY-MM-DD — Short topic

## Trigger
What the user asked for (one or two sentences).

## Done
- Bullet list of concrete changes (files, commits, builds).

## Decisions
- Choices made and rationale (only non-obvious ones).

## Open / next
- Unfinished work, blockers, and the recommended next step.

## Key paths
- Files or dirs the next agent should read first.

## Commits
- `hash` message (if any)
```

## Retention

- **Active folder:** the **15 most recent** session logs (burst-day cap).
- **Archive:** older logs in `archive/YYYY-MM/`; monthly indexes at `archive/YYYY-MM-INDEX.md`.
- **Prune:** remove logs **superseded by a later session** only — not because work shipped. Script: `scripts/prune_superseded_conversation_logs.py`; one-line index in `RECOVERY.md`.
- **Roll to archive:** `python3 scripts/archive_conversation_summaries.py` from repo root.

Git history remains the source of truth for file-level diffs; logs carry decisions and open items git does not.
