# Conversation summaries

Agent handoff for **towards-asi-alignment**. Durable state lives in `metadata/TODO.md`, experiment `FINDINGS.md`, and git — not in per-session files.

## Picking up work

1. Read **[HANDOFF.md](HANDOFF.md)** (aggregated open work and recent themes).
2. Skim `metadata/book.yml` and `metadata/TODO.md`.
3. Read `AGENTS.md` for task-specific rules.

Past sessions: one-line index in **[RECOVERY.md](RECOVERY.md); full text via git history.

## After a session

Update **HANDOFF.md** (Open work / Recently shipped). Add a one-line entry to **RECOVERY.md** only if you created a standalone log file to delete later.

Do **not** recreate the old pattern of hundreds of per-session `.md` files.

## Optional bulk compress

If standalone log files accumulate again:

```bash
python3 scripts/compress_conversation_summaries.py --delete
```

Regenerates RECOVERY one-liners and removes individual logs. Does not overwrite HANDOFF.md.

## Old log template (deprecated)

Per-session files are retired. If you must scratch-pad a multi-day thread, use `drafts/<topic>.md` outside this folder and merge into HANDOFF when done.
