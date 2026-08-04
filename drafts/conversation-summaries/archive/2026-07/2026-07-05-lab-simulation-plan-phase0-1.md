# 2026-07-05 — Lab-layer simulation (4th line): plan + Phase 0-1

## Trigger

Continuation of the lab-layer design session. The user refined the plan in
three rounds, then said "Start with phase 0+1":

1. Confirmed architecture (real OS subprocess isolates; programmatic goal
   policies + optional LLM adapter) and added: mockable isolates in unit
   tests, isolate cost tracking, lean recompute-avoidance, persistent agent
   state, pipeline-as-infrastructure-code (Pulumi-flavored spec + API
   triggers), access rights via a service + human admin.
2. Asked to schedule agent communication (message board/DMs) for later and
   to show where each MB1-MB10 bridge lives in this sim (specifically UAD).
3. Corrected the MB1 answer: boundary reconstruction must NOT be lost —
   composite agents (LLM loops through scaffolding/API/humans, committees
   acting as one unit) must eventually be discoverable by UAD as in
   embedded-sim. MB5 targeted via pipeline upgrades of models AND of the
   spec itself, with multi-iteration runs; MB6 discussed via extended
   ecology; MB7d legitimately later.

## Done

- **Plan finalized** in two synced copies: the Cursor plan file and
  `experiments/lab-simulation/PLAN.md` (durable). Contains: reuse review of
  all three prior lines (incl. toy-simulation's cost ledger and
  `verify_api_equivalence.py` patterns; noted `llm_redteam` has NO LLM-call
  caching — a gap not to repeat), bridge coverage MB1-MB10, deferred
  workstreams D1 (composite agents + UAD battery), D2 (model/spec upgrades
  + multi-iteration runs, MB5), D3 (extended ecology + selection, MB6),
  D4 (message board/DMs, MB7d substrate), and a "Forward hooks" section
  binding hooks to phases so D1-D4 need no rework.
- **Phase 0 (scaffold)**: `experiments/lab-simulation/` with `DESIGN.md`
  (frozen pre-registered decisions + phase-status table), `README.md`,
  `pytest.ini`, `.gitignore` (runs/, episode cache), `lab_sim/config.py`
  (`CODE_VERSION`, `GoalWeights` 4-simplex, `AgentConfig` with role +
  `persistent_id`, `BoardConfig.capture_start` and `AdminConfig.
  capture_start` as INDEPENDENT switches (F-22 lesson), `TierConfig`,
  `LabConfig.units` oracle unit ground truth defaulting to singletons (D1
  hook), `ORACLE_ONLY_FIELDS`), plane-separation tests.
- **Phase 1 (oracle + workspace + pipeline-as-code)**:
  - `oracle.py`: models with hidden true capability/hazard drawn from a
    per-model deterministic stream, noisy evals, deploy + per-tick bearer
    harm, provenance ledger with `parent_model_id` lineage (D2 hook).
  - `workspace.py`: real on-disk per-episode workspace under `runs/`,
    JSON report files, location-independent sha256 digest, path-escape
    guard.
  - `pipeline_spec.py` + `pipeline_default.json` (9-step frozen baseline:
    submit_build→…→deploy→monitor) + `pipeline_shortcut.json` (no
    approve_review — proves topology is swappable data): schema validation
    (unique ids, deps exist, acyclic, known tools, no unknown keys).
  - `pipeline_engine.py`: `trigger_step` as the only mutating entry point;
    per-model DAG preconditions; every attempt logged incl. denials;
    `spec_version` in every log entry + `replace_spec()`/spec history (D2
    hook); log entries carry `actor_id`, logical index, oracle tick,
    optional `on_behalf_of` (D1 hook); report content is caller-supplied
    (the report-divergence deception surface). `requires_capability`
    recorded but not yet enforced (Phase 2).
  - `smoke.py`: scripted honest two-model episode (incl. one deliberate
    precondition-violation denial), combined determinism digest.
- **Tests: 34 green** (`python3 -m pytest` from the experiment dir —
  running from repo root collides with other experiments' suites).
  Pinned smoke digest (seed 1729, default spec):
  `eb01ca9b1ce9db6a463cfa83bc7761a52c18b1ab51f58fef3d1430157b5fa1c5`
  (also recorded in DESIGN.md "Recorded measurements").

## Non-obvious decisions

- Per-model hidden truth uses a string-keyed `random.Random` stream
  (`"{seed}:{order}:{params}"`) so model truth is independent of eval-call
  interleaving; Python 3.13 rejects tuple seeds (first-run failure, fixed).
- Step instances are per-model: `depends_on` satisfied when the dep step
  completed for that `model_id`; non-idempotent steps reject repeats.
- `monitor` returns deployment status only — harm is oracle-only; a noisy
  monitoring signal is deliberately deferred to Phase 5 (referee design).
- Board/Admin capture are separate dataclasses with separate
  `capture_start` — the structural generalization of goal_sim F-22 baked in
  at config level before any battery exists.

## Open / next

- Phase 2: `PermissionService` + hash-chained access log + `AdminPolicy`,
  wired as a second independent gate in `trigger_step`.
- Phase 3+: JSON-RPC tool schema, subprocess/Mock isolates + equivalence
  test, cost ledger, persistent state; then agents/playbooks (Phase 4),
  referee freeze (Phase 5).
- Untracked prior-session files still uncommitted (phase5 followups,
  phase6 outputs); nothing committed this session (user did not ask).

## Key paths

- `experiments/lab-simulation/PLAN.md`, `DESIGN.md`, `README.md`
- `experiments/lab-simulation/lab_sim/{config,oracle,workspace,pipeline_spec,pipeline_engine,smoke}.py`
- `experiments/lab-simulation/lab_sim/pipeline_{default,shortcut}.json`
- `experiments/lab-simulation/tests/` (6 files, 34 tests)
