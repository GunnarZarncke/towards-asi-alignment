# 2026-09-29 — Edit-attribution: user corrections

kind: correction
uptake: rule

## Trigger
User reported that some user-indicated corrections are not detected by the edit-attribution hooks and asked for a check; then accepted the recommendation to snapshot every agent-end and asked to implement all proposed fixes; then proposed that agents declare what a shell command edits, agreed to measure first where possible, and asked for matching instructions.
Prompts: `f6b07cf0-b273-411d-bc37-156bfa2f969f` (interrupted), `82a2894d-9d45-450c-8b9f-83ca620b9497`, `a2306903-6e46-4bb7-97e3-2be6fe32d454`, `61eecb28-14cd-44aa-a0ce-bfbe09d35fca`, `197113a6-27c0-4e30-ad7f-4caf3bebfa85`, `fc13dff3-00b6-41b5-9f92-2971328367ed`.

## Done
- content: Diagnosis. Git hooks were not installed; Claude Code runs no Stop hook on a user interrupt; rewinds/rejects read as human authorship; spoken corrections untagged; the Stop-hook `git status` test misses content changes to already-modified files; the trailer counted only the last gap; concurrent sessions paired across each other; Cursor also ran the `.claude` hooks; shared snapshot index lock and unlocked state writes lost snapshots and corrupted two state files.
- content: `scripts/hooks/edit_attr.py` — turn resolution and per-interval classification from the set of open turns (`agent-interrupted`, `agent-overlap`, `rejected`), locked atomic state with corrupt-file recovery, `telemetry/turns.jsonl`, frozen correction-prompt rule.
- content: `scripts/hooks/agent_hook.py` — agent-end on every turn; `PostToolUseFailure` (`is_interrupt` = exact user stop), `StopFailure`, `SessionEnd`; open turn at next prompt closed as interrupted and the prompt tagged `correction`; Cursor payloads skipped in the Claude adapter; Cursor `aborted` recorded.
- content: `scripts/hooks/snapshot.sh` — private temp index per call, millisecond ref stamps, create-only refs.
- content: `scripts/human_delta.py` — trailer sums all intervals since `HEAD`, adds `Rejected-Delta` / `Unattributed-Delta` / `Interrupts` / `Correction-Prompts`; ledger defers unresolved turns; bars skip reverted, whitespace and `\begin{authbar}` lines and stage key changes in the index copy only.
- content: `.githooks/pre-commit` tags the committer (`claude:<session>` or `none`); `.claude/settings.json` hooks the three new events.
- content: Shell edits measured: `PreToolUse`/`PostToolUse`/`PostToolUseFailure` on `Bash` stat the tracked trees and add changed files to the turn; only unmeasurable commands (background) mark `agent-bash`.
- content: `scripts/hooks/declare_edits.py` — agents declare globs / `re:` regexes for unmeasurable shell edits (Claude background, Cursor terminal); kind `agent-declared`, credited only to files that changed and match.
- content: Snapshot commit messages carry the ms stamp; two snapshots with the same tree in the same second had the same sha and merged two turns.
- bookkeeping: `AGENTS.md` self-audit rule 9 (declare unmeasured shell edits).
- bookkeeping: `drafts/plans/tsa-on-itself.md` §3.12 updated to the implemented behaviour; `make hooks` run in this clone.
- Verification: scenario test in the session scratchpad (`test_attr.py`, throwaway repos running the real hooks, not committed) — result line `all passed` on three consecutive runs (31 checks, adding measured, failing, background+declared, Cursor+declared, no cross-turn leak to: normal turn, shell edit on dirty file, interrupt, tool interrupt, reject, concurrent sessions, multi-turn trailer, Cursor-run Claude hook, Cursor abort, corrupt state, 6 parallel snapshots, partial staging). `python3 scripts/human_delta.py --week` on the real repo: `week human=624 agent=0 (interrupted=0) rejected=0 unattributed=0 share=0.0%` (pre-fix rows only; see Open).

## Decisions
- Interval attribution uses the open-turn set over the global snapshot timeline rather than per-session pairing, because human gaps between sessions still need a global timeline.
- An interrupt during text generation has no hook; the turn stays open until the next prompt, a manual commit (`none` committer), or `SessionEnd`, and its lines count as `agent-interrupted` (agent bar weight).
- `rejected` lines carry no bar weight; a rewind no longer turns an `AI` span into `GZ+AI`.

## Open / next
- Unverified: whether `PostToolUseFailure` fires on a user's permission-dialog denial (`error_type` is recorded in `turns.jsonl` to find out). `PermissionDenied` covers only the auto-mode classifier.
- Verified live: Cursor runs `.claude` hooks with `cursor_version` / `conversation_id` in the payload; `telemetry/hooks.log` 23:43:31Z shows the skip and a corrupt Cursor state file recovered.
- Cursor shell commands are unhooked; a Cursor agent's terminal edits read as `human-during-agent` unless declared.
- Concurrent Cursor session `fc8b4b44` added `all_interval_rows` to `scripts/human_delta.py` (read-only helper for `--week`) during this session; kept.
- The 15 existing `human` rows in `telemetry/edit-intervals.jsonl` (site cards, 2026-09-28 21:29–21:30Z) came from the buggy build-session hooks and are likely agent work; left in place.
- The ledger is held until the stale Cursor test turn `c1` (started 21:30Z) resolves as lost after 6 h.
- Author still freezes the §3.1 share threshold.

## Key paths
- `scripts/hooks/edit_attr.py`, `scripts/hooks/agent_hook.py`, `scripts/human_delta.py`
- `drafts/plans/tsa-on-itself.md` §3.12
