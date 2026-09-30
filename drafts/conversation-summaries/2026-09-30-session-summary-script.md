# 2026-09-30 — Session summary script

kind: new-work
uptake: local

## Trigger
User asked for a script to recap user vs agent actions from recorded session logs; then useful defaults when run with no parameters; then end-of-session commit.
Prompts: paraphrase-only (telemetry prompt ids not copied this turn).

## Done
- content: `scripts/session_summary.py` — read-only recap from `telemetry/prompts`, `telemetry/turns`, git log, optional Cursor transcript merge; `--session`, `--since`/`--until`, `--commit`, `--format json`; no-arg defaults = latest telemetry session + auto transcript + commits in window.
- Verification: `python3 scripts/session_summary.py` exit 0; stderr `latest telemetry session \`9d8fadfc\``; markdown lists user requests, agent turns, commits.

## Decisions
- Defaults are read-only; script never appends ledger rows or session logs.
- Transcript merge is on by default when a session is known; `--no-transcript` opts out.

## Open / next
- None for this script; optional future: `--compare-log` against an existing session log file.

## Key paths
- `scripts/session_summary.py`
- `scripts/human_delta.py` (sibling edit-attribution tooling)

## Commits
- _(this session)_
