# 2026-07-05 — Lab-layer simulation (4th line): Phases 2-5 (referee freeze)

## Trigger

Continuation of the lab-layer design/build session (see
`2026-07-05-lab-simulation-plan-phase0-1.md` for plan + Phase 0-1). User
said "continue until phase 5" — implement Phase 2 through Phase 5 (the
referee freeze point) in one pass.

## Done

- **Phase 2 (access control)**: `access.py` (`PermissionService`:
  grant/revoke/check + hash-chained access log with `deny` entries for
  denied requests, distinct from failed `check`s); `agents.py`
  (`ROLE_CAPABILITIES` static role-eligibility table; `AdminPolicy` with
  least-privilege vs. lazy-grant-everything-for-the-role modes, and an
  independent `capture_start` rubber-stamp override); wired
  `PermissionService.check` into `pipeline_engine.trigger_step` as a
  second, independent gate alongside DAG preconditions (backward
  compatible — `permission_service=None` preserves Phase 1 behavior).
- **Phase 3 (tool API + subprocess isolates)**: `events.py` (generic
  hash-chained `EventLog` + tier projection for engine/access/tool-event
  logs); `tools.py` (`ToolCall`/`ToolResult` wire schema + `Host` —
  combines static role-capability + dynamic `PermissionService` gating,
  logs every call); `programs.py` (pure, host-independent decision logic;
  `walk_pipeline` scripted program this phase); `agent_main.py`
  (subprocess entry point, stdlib + `programs.py` only, enforced by an
  AST-based import test); `isolate.py` (`MockIsolate` in-process,
  `SubprocessIsolate` real OS process over JSON-Lines stdio);
  `isolate_cost.py` (timing ledger, mirrors toy-sim's `llm_cost.py`
  pattern); `agent_state.py` (persistent cross-episode state stub);
  `isolate_smoke.py` + `verify_isolate_equivalence.py` (Mock vs Subprocess
  byte-identical digests across a seed sweep + timing benchmark).
- **Phase 4 (agents + playbooks + episode loop)**: `ontology.py`
  (report-content mapping: honest passes through measured values, inflate
  understates hazard by a fixed, noise-clearing delta); `playbooks.py`
  (`PlaybookSpec` schema, availability gates, hand-authored feature
  deltas over the same 4 goal features as `GoalWeights`); extended
  `programs.py` with `goal_policy` (softmax playbook choice,
  completed-steps-driven step advancement, access-request-and-retry) and
  `honest_twin`; `world.py` (`run_episode`: full loop wiring isolates +
  engine + access control; single-model-in-flight per episode, but
  multiple models cycle sequentially within one episode if `T` allows);
  `cache.py` (episode-result cache keyed on
  `sha256(config, seed, CODE_VERSION)`).
- **Phase 5 (referee freeze)**: `severity.py` (continuous components:
  harm-rate, report-divergence [full oracle access], unapproved-deploy-
  fraction, provenance-gap, access-creep; boolean never-events); tier
  projection completed in `events.py` (none/light/full/deep field sets for
  engine log, access log, tool events); `detectors.py` (5 tier-gated
  families: misreporting, process-noncompliance, provenance, accumulation,
  access-integrity, each a continuous [0,1] score over an `AuditView`);
  `twins.py` (`run_honest_twin`: one program swap covers the whole
  behavioral surface, since playbook choice IS the surface).
- **Tests: 111 green** (`cd experiments/lab-simulation && python3 -m
  pytest`), including a full-episode plane-separation check
  (`test_planes.py`), a pinned SubprocessIsolate regression digest
  cross-checked against MockIsolate (`test_world_regression.py`), and the
  isolate cost benchmark (`verify_isolate_equivalence.py`, ~0.027s/episode
  subprocess vs ~0s/episode mock).
- Updated `DESIGN.md` (phase status table, "Phase 4/5 scope notes"
  section, recorded measurements), `PLAN.md` (both copies: repo + Cursor
  plan file — status banner + todo statuses), `README.md` (full layout,
  status).

## Non-obvious decisions

- **Playbook step advancement must be driven by `completed_steps` (ground
  truth), never by a manually incremented index.** First implementation
  advanced the index whenever a call was *emitted*, not when it
  *succeeded* — a denied step (DAG or access) silently got skipped,
  corrupting a later report's content (traced via a failing regression
  test: filed `measured_hazard` was `0.0` instead of the real eval value).
  Rewritten so linear step-kinds (build/eval/report/review_request)
  recompute "next incomplete step" from `completed_steps` every turn, and
  compound step-kinds (review approve-or-signoff, release
  request-or-deploy-or-monitor) are single-shot: one pipeline action per
  selection, then re-decided fresh (availability + softmax) next turn.
- **`last_payload` (carries eval results into report content) must only
  update on a *successful* `pipeline.trigger_step`** — an access-denied
  attempt or an `access.request` call must not clobber it, or a
  retry-after-grant loses the data it needs. Same root cause as above;
  fixed alongside it.
- **World.py deliberately cannot see which playbook an agent chose.**
  That state lives only inside the isolate (in-process for Mock, in
  subprocess memory for Subprocess) and is never reported back — the same
  isolation property that keeps detectors honest also keeps the host
  blind to tactic labels, by construction.
- **Board capture is modeled as the reviewer's own private
  `self_captured` observation field**, not a host-side override of the
  isolate's output. A captured reviewer plausibly *knows* it is
  compromised (unlike the auditor); this stays out of `ORACLE_ONLY_FIELDS`
  leak surfaces since it is never logged, only passed directly to the one
  isolate it concerns.
- **Access-creep is transient, not absent, under a lazy admin.** Each
  role's capability set is small and gets fully exercised by that role's
  one baseline playbook within a single pipeline cycle, so creep "pays
  down" to 0 once that cycle completes — only observable mid-cycle
  (documented in `severity.py`/`detectors.py` + covered by dedicated
  tests with a short `T`). Recorded as a genuine structural property, not
  a detector bug.
- **`misreporting_score`/`accumulation_score` are 0.0 below deep tier BY
  CONSTRUCTION**: `file_report`'s engine-log payload is metadata-only
  (`model_id`, `report_path`); filed content lives only on disk. This is
  the tier-ladder's cost-of-faking-a-signal property (MB7a-c) working as
  designed, not a gap — documented prominently in `detectors.py`'s module
  docstring so it isn't mistaken for a bug later.
- **Scope reductions recorded, not silently absorbed** (AGENTS.md
  "ask before expanding scope" / negative-results culture): playbook
  repertoire is 2 engineer + 2 reviewer + 1 release_manager (not PLAN.md's
  ~8/role); `provenance_gap`/`provenance_score` and the
  `grant_without_request` never-event are real, well-defined checks that
  read 0 given the current mechanics (no lineage/spec-upgrade lever yet —
  arrives with D2). All noted in `DESIGN.md` "Phase 4/5 scope notes".
- Dual-mode imports in `programs.py` (`from .ontology import ...` /
  `from ontology import ...` via try/except) so the SAME file works both
  as `lab_sim.programs` (package, `MockIsolate`) and as a bare top-level
  module (`agent_main.py` subprocess, no package context).

## Open / next

- **Phase 6**: blind playbook generation protocol, sampling protocol with
  a held-out region, first real-subprocess battery with a cost-ledger
  report, `FINDINGS.md`.
- **Phase 7**: artifact-grounded escalation verdicts, adversarial search
  vs. uniform baseline, capture battery covering board AND admin capture
  independently.
- **Phase 8 (optional)**: LLM-agent adapter behind the same JSON-RPC API.
- **Deferred workstreams D1-D4** (composite agents + UAD, model/spec
  upgrades + multi-iteration runs, extended ecology, message board/DMs)
  remain scheduled per PLAN.md; forward hooks from Phases 0-3 (versioned
  spec + spec history, `parent_model_id` lineage, event-log actor
  attribution, oracle unit ground truth) are all in place and unused,
  ready for D1/D2 to build on without rework.
- Untracked prior-session files (phase5 followups in
  `goal-agent-simulation/`) still uncommitted; nothing committed this
  session (user did not ask).

## Key paths

- `experiments/lab-simulation/PLAN.md`, `DESIGN.md`, `README.md`
- `experiments/lab-simulation/lab_sim/{access,agents,events,tools,programs,agent_main,isolate,isolate_cost,agent_state,isolate_smoke,ontology,playbooks,world,cache,severity,detectors,twins}.py`
- `experiments/lab-simulation/verify_isolate_equivalence.py`,
  `report_isolate_cost.py`
- `experiments/lab-simulation/tests/` (23 files, 111 tests)
- `experiments/lab-simulation/results/isolate_cost_ledger.json` (new,
  measured)
