# 2026-09-29 — Edit-attribution usage and read-only week

kind: notes
uptake: local

## Trigger
Cursor session `fc8b4b44` (the one that built the tooling, `2026-09-28-edit-attribution-build.md`) asked for walkthrough examples of an edit turn vs a no-edit turn, whether prompt intent or correction is detectable, a command to summarise what the hooks recorded, and a `--week` that does not write the ledger. Its closing turn ran 23:43:31–23:44:23Z while the Claude Code session `6b376df9` was fixing correction attribution (`2026-09-29-edit-attribution-corrections.md`); this log states the joint result.
Prompts: `806f5a3d-e84c-4b8e-b67d-27fc4274f631` (closing turn). Earlier turns of this session are paraphrase-only: its hooks failed on a corrupt state file and recorded no prompts.

## Done
- notes: Edit turn vs no-edit turn, as the hooks now behave. Both get an `agent-start` snapshot at the prompt and an `agent-end` snapshot at Stop; a no-edit turn's end has the same tree as its start and yields no ledger row, but it bounds the following gap so hand edits after the reply are `human`, not `unattributed`. An edit turn yields `agent` rows for files in its edit list; Claude Code shell commands are measured per command; unmeasurable shell edits are `agent-bash` unless declared (`agent-declared`).
- notes: Prompt intent. Every prompt is stored with `kind: correction | request` by the frozen rule in `scripts/hooks/edit_attr.py` (after an interrupt, or matching the correction patterns); interrupts, rejects, and correction prompts appear as commit trailers. Finer speech-act classification stays with §3.14 of `drafts/plans/tsa-on-itself.md`.
- notes: Summary commands:
  ```sh
  python3 scripts/human_delta.py --week                  # print-only tally
  git for-each-ref refs/snapshots --format='%(refname:short)'
  python3 scripts/export_prompts.py --month 2026-09      # redacted prompt digest
  ```
- content: `scripts/human_delta.py` — `all_interval_rows()`; `--week` reads persisted rows plus final pairs not yet appended, and writes nothing.
- Verification: `python3 scripts/human_delta.py --week` on the joint code → `week human=624 agent=0 (interrupted=0) rejected=0 unattributed=0 share=0.0%`, exit 0 (the 624 human lines are the pre-fix rows the corrections log flags as likely agent work).

## Decisions
- Weekly inspection is read-only; ledger rows are appended by `post-commit`, `pre-commit`, `--month`, and `--derive-bars`.
- Snapshot-time tree dedup is not needed: identical trees are one git object already, and snapshot commits are made unique by their millisecond stamp.

## Open / next
- Open items are tracked in `2026-09-29-edit-attribution-corrections.md`.

## Key paths
- `scripts/human_delta.py` (`--week`, `all_interval_rows`)
- `drafts/plans/tsa-on-itself.md` §3.12–§3.14
