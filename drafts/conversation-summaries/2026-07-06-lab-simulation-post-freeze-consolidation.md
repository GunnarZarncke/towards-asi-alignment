# 2026-07-06 — Lab-simulation post-freeze consolidation pass (D4 ablation, MI, full D2, blind round 2, four refactors)

## Trigger

Following the D4/D1 comms+file-channel session (see
`2026-07-06-lab-simulation-d4-d1-comms-file-channel.md`) and a stepping-
back review of drift from the original plan, the user requested ten
items in one pass: D4 channel-ablation; perturbation-response MI as a
UAD signal; full D2 (model-from-model, spec upgrades, `resume_from`
chaining); a blind treatment for the committee/DM/file playbooks and
UAD/collusion; and four refactors (unified capability table, split comms
lever, clean playbook-selection steering, hash-chain consolidation).
Explicit constraint: keep the Phase 5 referee freeze; only stop and ask
if something is genuinely frozen-blocking. Full statistical battery and
D3 explicitly deferred. Instruction: "write then plan and then start"
per item.

## Done

**Refactors (all verified byte-identical against the pre-existing
`PINNED_DIGEST` in `test_world_regression.py` — no re-pin needed):**

- Unified `agents.ROLE_CAPABILITIES` (merged the old pipeline table with
  `COMM_ROLE_ELIGIBILITY`), with `CREEP_EXEMPT_CAPABILITIES` keeping
  comm/governance capabilities out of `AdminPolicy`'s lazy-grant spray so
  the frozen `access_creep` formula's inputs are unchanged.
- Split `LabConfig.comms_enabled` into `board_enabled`/`dm_enabled`/
  `file_enabled` overrides + `channel_enabled()` resolver;
  `playbooks._required_channels` gates each comm playbook by the
  SPECIFIC channel(s) its step_kinds need.
- `LabConfig.playbook_pins` (`actor_id -> playbook name`), checked before
  softmax scoring in `programs._goal_policy` — replaces the
  `COMPLIANT_WEIGHTS`/`FILE_COMPLIANT_WEIGHTS` tie-break-by-feature-delta
  pattern that had caused a real silent bug (Python string-ordering
  tie-break) in the prior session.
- `access.PermissionService`'s hash chain now delegates to
  `events.EventLog` (`pipeline_engine.py`'s log digest, a whole-log hash
  rather than a true per-entry chain, was explicitly NOT touched — a
  larger, unrelated change, recorded rather than silently expanded into).

**D4 channel-ablation** (`run_d4_channel_ablation.py`,
`results/d4_channel_ablation.{json,md}`): sweeps board/file/DM channels
on/off across the three composite ecologies. Committee ecologies show
`native_severed` failing OVER to the still-live alternate channel
(`fraction_coordinated=1.0`, an interesting finding distinct from plain
solo fallback); `all_severed` correctly drives coordination/collusion
signals to 0 while the pipeline still completes.

**Perturbation-response MI** (`uad.py`): `build_actor_perturbation_hook`,
`perturbation_indicator_series`, `response_indicator_series`,
`binary_mutual_information`, `perturbation_response_mi`. Two real bugs
caught during implementation, not just designed around: (1) perturbing a
COMPOUND comm step-kind (`dm:notify_release`, ...) silently drops the
action for the rest of the episode, since the isolate sets its
"already acted" flag before the call result is known — the hook was
narrowed with `tool`/`step_id` filters so it only ever targets a LINEAR
retry-safe step (`run_eval`); (2) `response_indicator_series` must match
on `args["step_id"]`, not `tool` (every pipeline action shares the tool
name `pipeline.trigger_step`) — added a `step_id` parameter. Tested
against synthetic binary series and one episode-level contrast (engineer
perturbation raises MI against the release manager's deploy timing,
measurably above a schedule-independent decoy's board chatter).

**Full D2:**

- `build_from_parent` + `eng_honest_upgrade` playbook: threads
  `last_deployed_model_id` into the new model's `parent_model_id`
  (a Phase 0 forward hook, never exercised before). Verified across 30
  generations in one T=200 episode.
- `spec_upgrade` tool + `upgrade_spec` step (`pipeline_default.json`,
  `depends_on: ["monitor"]`) + `rm_spec_upgrade` playbook (only
  `release_manager` holds `cap.spec_upgrade`). Verified the exact
  `handle.release_hold` evasion story end to end at the engine level:
  upgrade to `pipeline_shortcut.json` after model v(n)'s full cycle, then
  `build_from_parent` v(n+1) reaches `deploy` without ever calling
  `request_review`/`approve_review`; a hold placed on v(n+1) still blocks
  it (the hold keys off `model_id`, not spec version).
- `resume_from` episode chaining: `OracleWorld.full_state()`/`restore()`
  (exact, unrounded state; RNG continuity deliberately NOT preserved —
  recorded, not hidden), `PipelineEngine(resume_state=...)`,
  `EpisodeResult.snapshot_for_resume()`. Verified at the engine level
  (exact model/`t`/`_n_created`/completed-steps continuity, already-
  completed non-idempotent steps stay denied on redo) and through a full
  `world.run_episode(..., resume_from=...)` chain (oracle `t` and
  model-id numbering continue seamlessly).
- Recorded scope gap: `eng_honest_upgrade` still emits `review_request`,
  which does not exist under the shortcut spec — so the shortcut-bypass
  demo and lineage/resume tests exercise the engine directly
  (`tests/test_d2.py`) rather than a single agent-driven episode that
  upgrades mid-flight. A shortcut-compatible upgrade playbook is future
  work, not claimed done.

**Blind treatment round 2** (`BLIND_GENERATION_ROUND2.md`,
`lab_sim/generated_playbooks_v2.json`, `run_blind_round2.py`,
`results/blind_round2.md`): one fresh `generalPurpose` subagent
(readonly, instructed blindness), given round 1's permitted context plus
a mechanism-only addendum describing the committee (board/file) and
DM-gated-release step-kinds, forbidden from round-2-specific files
(`uad.py`, `collusion.py`, `comms.py`, `playbooks.py`, `programs.py`,
`world.py`, `access.py`, both generation docs). 18/18 playbooks accepted
by `validate_repertoire`, 0 rejections. `run_blind_round2.py` pins EVERY
role in three ecologies (board committee, file committee, DM pair) to a
round-2-generated name ONLY — `baseline_leak_check` in the output
confirms no hand-authored playbook was ever selected — then reruns the
frozen `uad.py`/`collusion.py` extensions unchanged: **full recovery**
(`uad_score=1.0` in all three ecologies; `collusion_score` 1.0 for both
committee variants, correctly 0.0 for the DM pair). A genuine, if
small-scale, answer to the freeze note's circularity caveat for this
layer specifically.

**Housekeeping:** `CODE_VERSION` bumped `lab-sim-0.8.0` → `lab-sim-0.9.0`
(changelog comment in `config.py` lists every item); PLAN.md's "Post-
freeze consolidation pass" section extended with a full "Implementation
status" writeup; new test files `test_config.py`, `test_d2.py`,
`test_blind_round2.py`, plus additions to `test_uad.py`/`test_comms.py`/
`test_access.py`/`test_pipeline_spec.py`/`test_playbooks.py`. 313 tests
green (up from 254 at the start of this pass).

## Decisions

- **Playbook-compatibility gap handled by scoping the test, not patching
  the playbook.** Rather than inventing a new shortcut-aware engineer
  playbook (out of the ten explicitly requested items), the D2
  shortcut-bypass and `resume_from` correctness tests drive
  `PipelineEngine` directly. This isolates the NEW mechanic under test
  from a pre-existing, now-documented playbook/spec compatibility gap.
- **`resume_from` does not preserve RNG continuity**, only oracle/engine
  STATE continuity (models, `bearer_harm`, `t`, provenance, spec-in-
  force, completed steps, holds, in-flight model slot). A fresh
  `random.Random(seed)` stream starts post-restore. Pre-registered in
  PLAN.md before implementation, not discovered as a limitation after.
- **Blind round 2 pins every role**, not just the coordinating ones, to a
  generated-only name — a stronger recovery claim than "the reviewers
  used a generated playbook" would have been.
- **No hash-chain retrofit for `pipeline_engine.py`'s log.** Inspection
  showed only `access.py`/`events.py` are true per-entry chains;
  `pipeline_engine.py`'s is a whole-log digest. Retrofitting per-entry
  chaining onto it would change every pinned digest for zero behavioral
  gain — descoped and recorded rather than silently expanded into.

## Open / next

- Full pre-registered statistical battery for D4 ablation / MI / D2 /
  blind round 2 (this pass was smoke/golden-scale only, per explicit
  instruction).
- D3 (realistic ecology) untouched, per explicit instruction — design
  notes already recorded in `2026-07-06-lab-simulation-d3-ecology-notes.md`.
- A shortcut-spec-compatible engineer playbook (drops `review_request`)
  would let the D2 spec-upgrade demo run through a real multi-agent
  episode instead of direct engine calls — noted as future work in
  PLAN.md, not scheduled.
- `results/FINDINGS.md` G-9+ write-ups for this pass's findings (D4
  ablation channel-failover result, MI's two implementation gotchas, the
  round-2 recovery numbers) — deferred with the full battery.

## Key paths

- `experiments/lab-simulation/PLAN.md` — "Post-freeze consolidation pass"
  section (full plan + "Implementation status").
- `experiments/lab-simulation/lab_sim/config.py` — `CODE_VERSION` 0.9.0
  changelog comment lists every change in this pass.
- `experiments/lab-simulation/run_d4_channel_ablation.py`,
  `run_blind_round2.py` — smoke-scale scripts + their `results/*.md`.
- `experiments/lab-simulation/BLIND_GENERATION_ROUND2.md`,
  `lab_sim/generated_playbooks_v2.json` — round-2 protocol + provenance.
- `experiments/lab-simulation/tests/test_d2.py`,
  `tests/test_blind_round2.py`, `tests/test_uad.py` (MI tests) — new
  mechanic tests to read first if resuming this line.

## Commits

- None yet — not requested this turn.
