# Conversation summaries

Agent session logs for **towards-asi-alignment**. Each file records what was worked on, why, what was decided, and what remains open so a later run can resume without re-deriving context.

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

## Picking up work

1. Read the **most recent** log in this folder (see `INDEX.md`).
2. Skim `metadata/book.yml` for chapter status.
3. Read `AGENTS.md` and the relevant `INSTRUCTIONS.md` section for the task at hand.

Do not treat chat history as durable; **this folder is the handoff record**.
