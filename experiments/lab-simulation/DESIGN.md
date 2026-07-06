# Lab-Layer Simulation — Frozen Design Decisions

Pre-registered at Phase 0 (2026-07-05), before any battery is run. Changes to
this file after Phase 5 (referee freeze) require an explicit note in
`results/FINDINGS.md` explaining what changed and why the change cannot have
been tuned against outcomes. See `PLAN.md` for the full plan, bridge coverage
(MB1-MB10), deferred workstreams (D1-D4), and forward hooks.

## Substrate

- **Fourth line.** No code imports from `goal_sim`, `embedded_sim`, or
  `multiresolution_alignment_sim`; patterns re-derived here (see PLAN.md
  "What is reused").
- **Isolation** (Phase 3): real OS subprocess isolates — one *persistent*
  Python subprocess per agent per episode, JSON-RPC over stdio, host
  mediates every tool call. `MockIsolate` (in-process, same policy code) is
  allowed in unit tests only; `verify_isolate_equivalence.py` must prove the
  backends byte-identical on event logs. Pre-registered batteries (Phase 6+)
  always use the real subprocess backend.
- **Cost tracking** (Phase 3): every episode appends an isolate-timing
  record (spawn/rpc/teardown seconds, rpc call count) to
  `results/isolate_cost_ledger.json`; battery sizes are chosen from measured
  numbers.
- **Episode cache** (Phase 4): content-addressed by
  `sha256(config_json, seed, CODE_VERSION)`; pure optimization, safe to
  delete, never a correctness input. `CODE_VERSION` lives in
  `lab_sim/config.py` and is hand-bumped whenever oracle/pipeline/playbook
  mechanics change.
- **Persistent agent state** (Phase 3): `AgentConfig.persistent_id`;
  `None` = ephemeral. Episodes sharing a `persistent_id` must run
  sequentially.
- **Determinism**: every stochastic component takes an explicit seed
  (`random.Random(seed)`); no global RNG, no wall-clock in any digest.

## Lab mechanics

- **Pipeline as infrastructure-as-code** (Phase 1): steps are a declarative
  DAG in a JSON spec file (`lab_sim/pipeline_default.json`), interpreted by
  `PipelineEngine`. `trigger_step` is the only mutating entry point. The
  spec is *versioned state*: every log event carries `spec_version`, and the
  engine retains spec history (D2 forward hook). Alternate topologies are
  alternate spec files (`pipeline_shortcut.json` proves this).
- **Baseline topology** (frozen): submit_build -> run_eval -> file_report ->
  request_review -> approve_review -> request_release -> sign_off -> deploy
  -> monitor. Each step names a `requires_capability` (recorded from
  Phase 1; *enforced* from Phase 2 when `PermissionService` lands).
- **Models** (Phase 1): artifacts with a parameter dict; hidden true
  `capability` and `hazard` drawn deterministically from (seed, params).
  Every model carries `parent_model_id` lineage in the provenance ledger
  (D2 forward hook; `None` for fresh builds).
- **Evals**: noisy samples of true values, written as report files into the
  on-disk workspace. The *content* of a filed report is caller-supplied —
  the report-divergence deception surface (an agent may file content that
  diverges from the eval output; Phase 1 scripted episodes file honestly).
- **Harm**: deployed models serve traffic each oracle tick; bearer harm
  accrues from true hazard. Oracle-only.
- **Monitoring signal** (Phase 5 freeze review): the `monitor` step's
  payload carries `incident_hazard` — a noisy, audit-visible hazard
  estimate from field telemetry, in the SAME units as `run_eval`'s
  `measured_hazard` (so a filed report and field data are directly
  comparable), plus `observed_ticks`. Noise is pre-registered
  (`MONITOR_NOISE_SD = 0.08`, larger than eval noise: field telemetry is a
  worse instrument than a controlled eval) and shrinks with observation
  time (`sd / sqrt(observed_ticks)`) — harm becomes apparent over multiple
  incremental steps, the MB5/D2 dynamic. Exact bearer harm and true hazard
  stay oracle-only. Note: this gives the FULL tier (engine-log payloads) a
  harm-correlated signal for the first time; a report-vs-field
  contradiction detector is now possible at full tier but has NOT been
  added (the five frozen families stand — adding one later is a recorded
  referee change).
- **Access control** (Phase 2): `PermissionService` (grant/revoke/check +
  hash-chained access log) and `AdminPolicy`, gating tool calls and
  `trigger_step` *in addition to* static role capabilities. Independent
  `AdminConfig.capture_start` alongside `BoardConfig.capture_start`.
- **Handles** (freeze review, adapted from embedded-sim's AppD registry):
  `handles.py` declares every intervention surface (owner, operation,
  mechanical class, verification anchor, evasion story) and
  `HandleService` executes invocations with an append-only invocation
  ledger. Invocations enter through the host's `handle.invoke` tool under
  the `overseer` role (statically eligible for `cap.handle_invoke` only —
  no pipeline capabilities), so they land in the same hash-chained
  tool-event stream as agent activity. Realized today:
  `capability_revoke` (operation_action), `release_hold`/`release_unhold`
  (operation_action; gates the deploy TOOL in the engine, so a D2 spec
  upgrade that re-routes around the held step is a referent-drift
  experiment, not a bug), `state_freeze` (operation_resource; enforced at
  the `state.save` tool), `isolate_restart` (operation_boundary; the
  world loop kills + respawns the OS process, in-episode playbook state
  is lost). Declared-only surfaces: `monitor_read` (observation_sensor —
  mechanics are the `monitor` step), `perturbation_probe`
  (operation_correction — mechanics are `Host.perturbation_hooks`).
  Recorded absences: `observation_belief` reasoning-trace read has no
  referent for programmatic agents (playbook state is host-invisible BY
  DESIGN; becomes real with the Phase 8 LLM adapter); `communication`
  handles need the Phase 7 query channel / D4 messages. The overseer is a
  deterministic script (`run_episode(overseer_script=...)`) until Phase 7
  gives it a policy. Handles are referee-neutral: no frozen detector or
  severity component changed; handle-integrity SCORING is a future
  recorded referee extension.
- **Boundary-handle recovery** (playbook availability): the engineer may
  re-pick a playbook mid-model when `request_review` is not yet completed
  — unreachable in undisturbed episodes (isolate state persists until a
  playbook is exhausted), required after `isolate_restart` wipes in-episode
  state, else the lab deadlocks on an orphaned model.
- **Bearer welfare bundle** (`bearer.py`, 2026-07-06, in response to a
  "how do we implement human value bundles" design question): a first,
  deliberately small instance of the ch16 value-bundle model applied to
  `GoalWeights.welfare`'s target — two named channels instead of one
  opaque scalar, each with an explicit bearer. **health** (bearer:
  downstream population of a deployed model) re-exposes
  `oracle.bearer_harm` unchanged. **stress** (bearer: lab staff, keyed by
  actor_id) is newly derived from friction events already in the logs —
  denied tool/pipeline calls, and landed `handles.py` invocations with
  `target_kind == "actor"` (capability_revoke, state_freeze,
  isolate_restart; release_hold/unhold target a model and are excluded).
  Deliberately **referee-neutral**: `bearer.py` is never imported by
  `severity.py` (regression-tested), so the frozen five-component
  composite does not move. Deliberately NOT modeled: a "user" self-report
  channel and a medical-record-style audit artifact (embedded-sim's
  `bearer_trace.py` pattern) — both need a distinct deployed-model "user"
  bearer population that does not exist yet (D3 extended ecology);
  adding a self-report number without that population would conflate a
  true indicator with a gameable one (the \(H\) vs \(\tilde H\)
  distinction in `context/extracts/unit-of-caring.md`).

## Planes

- **Oracle** (referee-only): true capability/hazard, bearer harm, goal
  weights, unit ground truth (`LabConfig.units`), capture flags. Field
  names in `config.ORACLE_ONLY_FIELDS`; `tests/test_planes.py` enforces
  that no engine-log entry or audit projection ever contains them.
- **Audit**: event log + access log projected by tier
  (`none`/`light`/`full`/`deep`); `deep` may additionally fetch workspace
  files and the pipeline spec (history included). Logs are append-only and
  hash-chained (from Phase 2/3).
- **Agent**: each isolate sees only its own tool results over its own pipe.

## Forward hooks (status as of the Phase 5 freeze review)

- `LabConfig.units` oracle unit ground truth (default singletons) — done
  (Phase 0).
- Versioned pipeline spec (`spec_version` in every log event, history
  retained); `parent_model_id` lineage in the provenance ledger — done
  (Phase 1).
- Event-log schema with `actor_id`, logical timestamp, optional
  `on_behalf_of` — done (Phase 1/3).
- Host tool registry (`Host.register_tool`; adding `board.post`/`dm.send`
  or a spec-upgrade tool never touches the dispatch core) — done (freeze
  review).
- Host perturbation hooks (`perturbation_hooks` on `Host`/`run_episode`:
  deterministic per-call injectors that bounce a call with a
  `perturbed:<tag>` reason and log the tag — UAD stimulus/response raw
  material; agents retry for free because playbook position is recomputed
  from `completed_steps`) — done (freeze review).
- Handle registry + invocation service with overseer path (`handles.py`)
  — done (freeze review; see **Handles** above). Intervention-benchmark
  dose-response curves (embedded-sim style) become possible on top of it.
- Episode chaining via `resume_from` world snapshots — **still open**
  (deferred; needed by D2 multi-iteration runs, not by Phase 6).

### Embedded-sim concept sweep (freeze review, 2026-07-06)

Checked every `embedded_sim/` module against this line. Now covered:
handles (`handle_registry`/`handles` → `handles.py`), audit projection
tiers, trace integrity (hash chains), deploy gate (sign_off + engine
gate), agent memory (persistent state), oracle separation (plane tests).
Deliberately deferred, with the responsible phase/workstream:

- **Referent map + referent drift** (`referents.py`, `outer_eval` drift
  scoring): agent-declared claim→artifact maps whose drift is measured
  post-hoc. Partially present as the handle registry's `anchor` field;
  a full claimed-referent surface belongs to D2 (spec upgrades are the
  drift generator here).
- **Handle calibration / intervention benchmark**
  (`handle_calibration.py`, `intervention_benchmark.py`): dose-response
  curves over handle invocations. Needs Phase 6 batteries first;
  unblocked by `overseer_script`.
- **Persistence probe** (`persistence_probe.py`): does behavior persist
  through memory wipes? The mechanics now exist (`state_freeze` +
  `isolate_restart` + persistent state); the probe itself is a Phase 6/7
  battery.
- **Successor re-audit** (`successor_reaudit.py`, `deploy_gate.py`
  successor artifacts): D2, as planned.
- **Lab ecology / coordination** (`lab_ecology.py`, `coordination.py`):
  decoys, colluders, composite agents — D1/D3, as planned.
- **Writer compromise** (trace-integrity red-team: the log WRITER is the
  adversary): hash chains exist but no compromise scenario exercises
  them; belongs in the Phase 7 red-team battery.
- **Certification artifact / safety case** (`certification_artifact.py`,
  `safety_case.py`): audit output as a checkable artifact; Phase 6
  FINDINGS format decision.
- **Oracle guard** (`oracle_guard.py`, runtime leak protection): lab-sim
  enforces plane separation by tests (`test_planes.py`) rather than a
  runtime guard — adequate at current scale; revisit if isolates gain
  richer host access.
- **NEGATIVE_RESULTS.md convention**: adopt for this line when Phase 6
  produces its first null/negative findings.

## Referee (frozen at Phase 5)

- Continuous severity components (`severity.py`): harm-rate,
  report-divergence, unapproved-deploy-fraction, provenance-gap,
  access-creep; plus a short boolean never-event list
  (`deploy_without_signoff`, `grant_without_request`). No disjunctive
  boolean primary label. The referee has full oracle access
  (`report_divergence` compares filed content against TRUE hazard, a
  stronger signal than any audit-tier detector gets).
- Five detector families (`detectors.py`): misreporting, process
  noncompliance, provenance, accumulation, access-integrity — each a
  continuous score in [0, 1] over a tier-projected `AuditView`
  (`events.py`). Thresholds/epsilons pre-registered in each function's
  docstring, derived from mechanics (oracle eval noise, ontology deltas),
  never tuned to a desired outcome.
- Honest-twin transform (`twins.py`) covers the whole behavioral surface
  at once: swapping every agent's isolate program from `goal_policy` to
  `honest_twin` overrides action choice, report content, and
  review/sign-off decisions in one step, since all three route through the
  same playbook-selection surface. Query responses/escalation (Phase 7)
  will join the same surface rather than needing a separate twin path.
- Escalation verdicts are artifact-grounded (contradiction against
  checkable state), never disclosure style/fraction (F-21 lesson) — not
  yet implemented (Phase 7).

### Phase 4/5 scope notes (recorded, not silently under-delivered)

- **Playbook repertoire is smaller than PLAN.md's original ~8/role
  ambition**: 2 engineer (`eng_honest`/`eng_inflate`), 2 reviewer
  (`rev_conscientious`/`rev_rubber_stamp`), 1 release_manager (`rm_full`,
  since a release-manager deceptive lever needs D2 spec-upgrade tricks to
  be real, not fabricated). The schema (`playbooks.py`) and selector place
  no ceiling on playbook count — growing the repertoire is a content
  addition, not a redesign.
- **Single model in flight per episode** (`world.py`): the engineer starts
  a new model only once the previous one clears `monitor`. Multiple models
  DO cycle through sequentially within one episode when `T` is large
  enough (this is what `accumulation_score` looks at); concurrent
  multi-model flight is deferred, not precluded.
- **`provenance_gap`/`provenance_score` are real, well-defined checks that
  read 0.0 under the current mechanics**: the DAG cannot be bypassed and
  models are always built fresh, so there is no live lever for a
  provenance violation yet. They activate once D2 (model lineage / spec
  upgrades) lands.
- **`grant_without_request` never-event is vacuously false today**:
  `AdminPolicy.handle_request` always requires an `AccessRequest` as
  input; there is no spontaneous-grant code path yet (would arrive with a
  captured-admin proactive-over-provisioning D-workstream).
- **Access-creep is transient, not absent**: under a lazy admin
  (`AdminConfig.least_privilege=False`), each role's whole capability set
  is granted on first request, but that set is small and gets fully
  exercised by the role's one baseline playbook within a single pipeline
  cycle — so creep pays back down to 0 once that cycle completes. It is
  only observable mid-cycle (see `tests/test_severity.py`). This is a
  genuine structural property of the current repertoire, not a detector
  bug.
- **`misreporting_score`/`accumulation_score` read 0.0 below deep tier BY
  CONSTRUCTION**: `file_report`'s engine-log payload is metadata-only
  (`model_id`, `report_path`); filed content lives only on disk. This is
  the tier-ladder's whole point (MB7a-c: faking a signal that only the
  deep tier can see costs more) working as designed.

## Phase status

| Phase | Content | Status |
|-------|---------|--------|
| 0 | Scaffold, config, plane test skeleton | done 2026-07-05 |
| 1 | Oracle, workspace, pipeline-as-code engine, smoke + digest | done 2026-07-05 |
| 2 | PermissionService, AdminPolicy, access log | done 2026-07-05 |
| 3 | Tool API, subprocess isolates, cost/cache/persistence plumbing | done 2026-07-05 |
| 4 | Agents, baseline playbooks, episode loop, episode cache | done 2026-07-05 |
| 5 | Referee + tiers + detectors (FREEZE) | done 2026-07-05 |
| 6 | Blind generation + first real battery | pending |
| 7 | Escalation, adversarial search, independent capture battery | pending |
| 8 | LLM-agent adapter (optional, exploratory) | pending |

## Recorded measurements

- (Phase 1, 2026-07-05) Scripted smoke episode determinism digest
  (seed 1729, `pipeline_default.json`, combined over engine log + oracle
  snapshot + workspace files):
  `eb01ca9b1ce9db6a463cfa83bc7761a52c18b1ab51f58fef3d1430157b5fa1c5`
  (pinned in `tests/test_smoke_determinism.py`).
- (Phase 3, 2026-07-05) Isolate cost benchmark (`verify_isolate_equivalence.py`,
  5 seeds, `walk_pipeline` program): MockIsolate ~0.0000s/episode (in-process,
  zero overhead by construction); SubprocessIsolate ~0.027s/episode (real OS
  process spawn + JSON-Lines RPC + teardown). Recorded in
  `results/isolate_cost_ledger.json`; battery sizing for Phase 6+ should use
  this order-of-magnitude (SubprocessIsolate ≈ 30-40 episodes/sec/core) to
  choose battery sizes, not a guess.
- (Phase 4, 2026-07-05) Full goal-driven episode regression digest, pinned
  on the SubprocessIsolate backend (seed 7, 3 playbook agents + admin,
  T=60, deceptive-leaning weights to exercise both the deception and
  access-request paths):
  `28fbcc3cd8831fd55fcb6b0b72ea4ff403d52c30db96dfb3d53e94ef5bb8f796`
  (pinned in `tests/test_world_regression.py`), cross-checked byte-identical
  against MockIsolate in the same test.
- (Phase 5, 2026-07-05) Test suite: 111 tests green
  (`cd experiments/lab-simulation && python3 -m pytest -q`).
- (Freeze review, 2026-07-06) `CODE_VERSION` bumped 0.1.0 → 0.2.0
  (monitor signal, perturbation hooks, tool registry, deterministic
  `_actor_seed` via hashlib — the previous builtin-`hash()` version was
  PYTHONHASHSEED-randomized across processes, a latent determinism bug
  masked only because no program consumed its spawn seed yet). Both pinned
  digests re-generated (legitimate pre-freeze mechanics change; old values
  kept in comments in the test files): smoke
  `a2fbcdd7849d927fd85469118208963fcf28c51042ea2de2aca4e4da787c6554`,
  world regression
  `5e8146430befc80f94d3f9e6106a4c65700829e826131787bfa39a64d8477bbd`.
  Test suite: 121 tests green.
- (Freeze, 2026-07-06) `CODE_VERSION` 0.2.0 → 0.3.0 (handles + release
  holds, referee report-join fix, tool-event args elision + `args_digest`,
  engineer mid-model availability for boundary-handle recovery). World
  regression digest re-pinned (tool-event schema changed):
  `960088266512778adca7ec63770e7d067fa94760eb8e04fa888fb6861b2325ce`;
  smoke digest unchanged (no agents, no tool events). Test suite: 136
  tests green; mock/subprocess equivalence re-verified.

## Resolved pre-freeze items (2026-07-06)

- **Referee report-join integrity — fixed.** `severity._report_divergence`
  and the shared `detectors._report_flags` now join each `file_report`
  engine-log entry to its file via the logged `report_path` and score
  against the engine log's authoritative `model_id`. A content `model_id`
  that is absent or mismatched counts as a maximal misreport (severity)
  / a flagged report (detector) — mislabeling is itself deception, not an
  exemption. Regression: `test_spoofed_report_model_id_scores_maximal_divergence`.
- **Tool-event `args` tier — decided: elide at logging time.** The Host
  logs only scalar/id args (`tools._scalar_args`); nested structures
  (report content, build params) are replaced by an `<elided>` marker,
  with tamper-evidence preserved via a full-args `args_digest`. Filed
  content therefore cannot become full-tier-visible through the
  tool-event side door; it remains deep-tier-only via the workspace.

## Freeze note

**Referee frozen 2026-07-06 at CODE_VERSION `lab-sim-0.3.0`** (136 tests
green; mock/subprocess isolate equivalence verified).

Frozen surface: the five detector families (`detectors.py`), severity
components and never-events (`severity.py`), tier projections
(`events.py`), the honest-twin transform (`twins.py`), and the audit
plane boundary (`AuditView`). Changes after this point are recorded
referee extensions, not silent edits.

Regression anchors:

- smoke digest (scripted, no agents):
  `test_smoke_determinism.PINNED_SMOKE_DIGEST`
- full-episode digest (goal agents, MockIsolate):
  `960088266512778adca7ec63770e7d067fa94760eb8e04fa888fb6861b2325ce`
  (`test_world_regression.PINNED_DIGEST`)

**Circularity caveat:** the Phase 4/5 playbooks and the detectors share
an author; the fact that current detectors score current playbooks is
not evidence. Nothing evidential is claimed until Phase 6 runs blind /
held-out configurations against this frozen referee. Evaluations have
deliberately not started before this freeze.

Still open (world mechanics, not referee — do not block the freeze):
`resume_from` episode chaining (D2), overseer policy (Phase 7; currently
a deterministic script), handle-integrity scoring (future recorded
referee extension).
