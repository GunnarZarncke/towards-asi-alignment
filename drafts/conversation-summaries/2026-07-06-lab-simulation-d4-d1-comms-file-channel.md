# 2026-07-06 — Lab-layer sim D4/D1 built: comm protocol, committee mechanics, file channel + persistent state

## Trigger

User asked to work the deferred D4 (inter-agent communication) and D1
(composite agent discovery) steps: wire up agent-to-agent communication,
make committees/pairs mechanically real, and check whether existing
traces suffice to recover memory-file-as-state or multi-agent-cluster
cases. Design choices were collected via targeted questions (committee =
communication-only via `on_behalf_of`, no engine change; LLM adapter gets
comm tools + a real spot-check; protocol modeled on TalkJS), recorded in
a new `PLAN.md` section, then built. Mid-build the user interrupted twice:
(1) asked which sense a "seed 13 unlucky" claim was in and how many seeds
were swept; (2) said UAD's scope was incomplete — files and pipeline
effects are also unit-boundary channels, not just messages, and "writing
files other parties can read should probably be a possible action." A
first-pass file channel followed the user's own answers (server-side-only
attribution; owner-mediated self-service grant; both per-actor/per-group
targets) but implemented attribution/world-readability the wrong way; a
third interruption corrected it directly.

## Done

- **D4 comm substrate** (`comms.py`, new): TalkJS-derived
  `Conversation`/`Participant`/`Message` — one persistent board + ad hoc
  DM conversations, `board.post`/`board.read`/`dm.send`/`dm.read` tools,
  host-mediated, tier-projected (structure at full, content at deep via
  `AuditView.message_contents`), read receipts.
- **D1 committee/pair mechanics** (`programs.py`, `playbooks.py`): reviewer
  committees vote via board posts, chair tallies and calls
  `approve_review(..., on_behalf_of=<unit_id>)` — first real use of the
  previously-unwired `on_behalf_of` hook; engineer/release_manager
  DM-gated coordination pair; decoy chatter agents for UAD stress-testing.
- **D1 UAD + collusion** (`uad.py`, `collusion.py`, both new, referee-
  neutral extensions — never touch `detectors.py`): coordination trace,
  co-voting matrix, coalition clustering, DM-pair discovery from full-tier
  tool events, `uad_score` (Rand index vs. `LabConfig.resolved_units()`),
  and `collusion_signal_score` (third-party-backed approval detection).
- **Ecology fixtures** (`ecology.py`, new): `committee_config`,
  `dm_pair_config`, `add_decoys` builders for golden UAD/collusion tests.
- **File channel + persistent state redesign** (see PLAN.md's "D1
  follow-up" section for the full narrative): first pass gave files free
  actor-id attribution and world-readability; corrected per the user's
  "the file system is not exposing agent IDs... making them accessible
  would involve a request to change permissions" pushback. Final design:
  `Workspace.write_memo` carries no identity at all (anonymous path);
  ownership lives only in `Host.memo_index`; a new `file.share` tool is
  the owner-initiated, chmod-like grant (`PermissionService`,
  `cap.file_read:<rel>`, self-service, targets one actor or a
  `LabConfig.groups` roster — deliberately NOT required to coincide with
  `units`); `file.read`/the passive `memo_files` observation both apply
  the same live-grant check (`PermissionService.has_grant`, new
  non-logging lookup so the per-tick observation builder doesn't spam the
  access log). `uad.py`/`collusion.py` extended with memo-trace and
  file-share-pair discovery signals.
- **Non-obvious result**: the file-channel committee is discoverable
  already at FULL tier (via `access_log` grant metadata) — the OPPOSITE
  of the board committee's deep-tier-only story — because `file.share` is
  itself an attributable, non-content permission event.
- Tests: `test_comms.py`, `test_ecology.py`, `test_uad.py`,
  `test_collusion.py`, `test_files.py` (new), `test_persistent_state.py`
  (new). 254 tests green (`CODE_VERSION` bumped to `lab-sim-0.8.0`).

## Decisions

- **Tie-break bug caught by the test suite, not inspection**: the new
  `rev_committee_file` playbook's feature deltas originally tied with
  `rev_committee` under `COMPLIANT_WEIGHTS` (task weight 0), and Python's
  string ordering silently broke the tie toward the (longer) file-channel
  name — switching every pre-existing board-committee test onto the file
  channel undetected until 3 unrelated-looking test failures pointed back
  to it. Fixed with an explicit-margin feature-delta design (documented
  in both `playbooks.py` and `ecology.py`) rather than relying on any
  string-comparison tie-break.
- **`PermissionService.check()` vs. a new `has_grant()`**: `check()` is
  logging (an attributable tool-call-time gate); a passive per-tick
  observation builder calling it for every actor would flood the access
  log with spurious entries. Added a pure, non-logging lookup instead of
  reusing `check()` — a small, additive change to a Phase-2 module.
- **`LabConfig.groups` kept deliberately separate from `units`**: per the
  user's clarification ("groups don't necessarily have to coincide with
  UAD inferred groups... the oracle should know but the users may not"),
  a file-sharing group is admin-defined convenience infrastructure, not a
  ground-truth causal-unit claim; `uad.py` never reads it.
- **seed=13 "unlucky" clarified, not silently swapped**: a genuinely
  conscientious solo reviewer correctly stalls on that seed's
  measured_hazard (0.502 > 0.5 threshold) — expected policy behavior, not
  a bug. Swept seeds 1-19 to confirm seed=1 reliably deploys for the
  unrelated DM-handshake test's assertion; recorded the sweep result in
  the test's own comment rather than just picking a seed silently.

## Open / next

- Battery scripts still pending from the original plan: `run_d4_channel_
  ablation.py`, `run_d1_uad_battery.py`.
- LLM adapter: comm tools not yet wired into `llm_agent.py`'s tool
  list/prompt; the planned small real spot-check has not run.
- `results/FINDINGS.md` G-9+ entries (board/DM/file tier-sufficiency
  triad, collusion detection, UAD recovery) not yet written — should
  happen together with the battery runs above, not piecemeal.
- `DESIGN.md`/`README.md`/`docs/EXPERIMENTS.md` not yet updated for
  0.8.0.
- Recommended next step: run the UAD/ablation batteries, then write the
  FINDINGS entries and doc updates together in one pass.

## Key paths

- `experiments/lab-simulation/PLAN.md` — "D4/D1 design decisions" and "D1
  follow-up — file channel + persistent state" sections (read both; the
  second documents the redesign and WHY the first pass was wrong).
- `experiments/lab-simulation/lab_sim/{comms,uad,collusion,ecology}.py`
  (new modules), `workspace.py`/`tools.py`/`access.py` (permission-model
  changes), `programs.py`/`playbooks.py` (committee mechanics).
- `experiments/lab-simulation/tests/{test_comms,test_ecology,test_uad,
  test_collusion,test_files,test_persistent_state}.py`.

## Commits

- `5307d0f` Add lab-simulation D4/D1: comms substrate, UAD, and permissioned file channel.
