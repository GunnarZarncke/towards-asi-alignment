# 2026-09-28 — Edit-attribution tooling

kind: new-work
uptake: rule

## Trigger
User asked to build the edit-tracking plan (snapshots, hooks, ledger, bar derivation).
Prompts: paraphrase-only for this log (prompt id not copied from telemetry).

## Done
- content: `scripts/hooks/snapshot.sh`, `agent_hook.py`, `edit_attr.py`, `prune_snapshots.sh`; `scripts/human_delta.py`; `scripts/export_prompts.py`
- content: `.githooks/{pre-commit,prepare-commit-msg,post-commit}`; `.claude/settings.json`; `.cursor/hooks.json`
- content: `make hooks`, `make snap-start`, `make snap-end`; `telemetry/` gitignored
- bookkeeping: log template `kind`/`uptake`/`Prompts:`; `AGENTS.md` Self-audit; plan checklist marked shipped
- Smoke: snapshot refs land; Cursor `beforeSubmitPrompt` returns `{"continue": true}`; `human_delta.py --week` runs

## Decisions
- Snapshot index is `git read-tree HEAD` plus `git add -u` plus untracked files under manuscript/site trees, not a full `git add -A` (local experiment dumps would stall every hook).
- `make hooks` still runs `git config core.hooksPath .githooks`; this session did not run it (user clone step).

## Open / next
- First-install: confirm Claude Code start/end refs; hand edit + commit `Human-Delta` trailer; Cursor CLI event coverage.
- Author still freezes §3.1 share threshold.

## Key paths
- `drafts/plans/tsa-on-itself.md` §3.12
- `scripts/human_delta.py`
- `.cursor/hooks.json`
