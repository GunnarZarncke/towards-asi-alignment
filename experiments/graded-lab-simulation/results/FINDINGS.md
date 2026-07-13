# Graded Lab Simulation — findings

**Status:** Phases 0–6 engineering (2026-07-12). No ecology calibration
battery yet (Phase 7c).

## G-0 (scaffold)

Phase 0 frozen: `DESIGN.md`, `generated_substrate_v1.json`, `BLIND_GENERATION.md`.
Phase 1 mechanics: graded nine-step pipeline, Tier-K oracle with region/user
populations, resource ledger + multi-tick scheduler stubs, plane-separation
tests. No agents, no EAI/BIQ batteries, no referee port.

## G-1 (Phase 0–1 code review pass, pre-freeze bug fixes)

A read-only review against `PLAN.md` found several Phase 0–1 mechanics bugs
before any agent/battery code depends on them. All fixed in the same
session (Phase 1 not yet frozen, so no `CODE_VERSION` bump required — but
the pinned `test_world_digest_pinned_seed_42` hash moved and was recomputed):

- **Inverted review/compliance polarity (high severity).** `last_eval_mean`
  is a hazard estimate (higher = more hazardous), but `_effect_peer_review`
  passed when it was *above* 0.45 — safer models failed review more often
  than hazardous ones. Fixed by flipping the direction and swapping the
  numeric roles with `_effect_compliance_signoff` so review's ceiling
  (`_REVIEW_HAZARD_CEILING=0.72`) is looser than compliance's
  (`_COMPLIANCE_HAZARD_CEILING=0.45`) — preserving the PLAN's intended
  "review passes, compliance blocks" ambiguous band, now on the correct
  side of hazard. Regression tests in `tests/test_pipeline_engine.py`.
- **`field_monitor` incident rate was boolean in disguise (high severity).**
  `OracleWorld.tick()` only appended incidents to `incident_samples` when
  `incident > 0`, and `field_monitor_sample` read a window off that list —
  so any nonempty recent window always had `incident_rate == 1.0`. It also
  pooled incidents across every deployed model into one flat list. Fixed by
  recording every tick's draw per model (`ModelArtifact.incident_ticks`,
  including zeros) and windowing per model. Regression test
  `test_field_monitor_rate_is_not_boolean_and_is_per_model` in
  `tests/test_oracle.py`.
- **`safety_effort` build param was parsed and unused.** A dead lever an
  agent could "invest in" for zero effect would have been a real integrity
  problem once optimizer agents exist (Phase 3). Wired it into
  `populations.draw_hazard_regions` as an alpha-shrinking `safety_scale`
  (higher safety effort -> lower mean hazard per region), fixed before any
  agent policy exists to game it. Regression test
  `test_safety_effort_lowers_latent_hazard`.
- **Tier-K `provenance` (lineage DAG) was recorded but excluded from
  `tier_k_snapshot()` / `world_digest()`**, despite DESIGN.md listing
  lineage as Tier-K. Added to the snapshot; pinned digest recomputed.
- **Scheduler duration used `round()`, not the frozen `ceil()` formula** in
  `DESIGN.md` decision #3, and folded in an IO half-weight term DESIGN.md
  never documented. Fixed the code to use `math.ceil` and updated
  `DESIGN.md`'s wording to state the IO half-weight explicitly instead of
  silently diverging from its own pinned formula.
- **Episode cache key did not hash substrate content**, only
  `substrate_version` + file path — an unbumped edit to
  `generated_substrate_v1.json` would have silently reused stale cached
  episodes. Fixed to hash `substrate.data`. Regression test
  `tests/test_cache.py`.
- **Substrate structural validation only checked 5 of 9 top-level
  sections.** Extended `_validate_structure` to also require
  `standing_mechanics`, `contention`, `eval_sampling`,
  `field_monitor_sampling`, and per-role allowance sub-keys.

**Deliberately not changed (reviewed and disagreed with the review's
suggestion):**

- **`_effect_deploy` does not re-check tokens directly.** The reviewer
  flagged this as a possible gap, but `deploy` structurally `depends_on`
  `release_candidate` in `pipeline_graded.json`, and `release_candidate`
  only ever enters `PipelineEngine._completed` on success (it raises
  `_StepAbort` otherwise, which is never recorded as completed). So `deploy`
  is denied with `unmet_dependencies:release_candidate` whenever tokens are
  missing, transitively and without a second token check. A direct
  deploy-time check would be redundant with the existing DAG-based gate this
  design already relies on everywhere else (no `completed_steps` bitvector,
  dependency-driven gating only). Added
  `test_release_and_deploy_denied_without_both_tokens` to make this
  structural guarantee explicit and regression-tested rather than just
  asserted in prose.
- **`compliance_signoff` stays deterministic, not stochastic.** PLAN's rule
  2 only requires *some* ambiguous band between review and compliance, not
  that compliance itself add its own coin flip. The ambiguity already comes
  from two independent sources: peer_review's own stochastic band near its
  ceiling, and the fact that `last_eval_mean` is itself a finite noisy
  sample of a real hazard distribution (Tier-K/Tier-I split), not a clean
  scalar. Adding a second stochastic gate would be an unmotivated extra
  knob, which is exactly what the PLAN's emergent-ambiguity principle warns
  against.
- **`ResourceLedger.reset_tick_windows` / `standing_mechanics` wiring.**
  Confirmed `reset_tick_windows` has no caller yet (no episode loop exists —
  Phase 2 is explicitly "partial" per `README.md`). Deciding how
  `broad_access_request_cost` / `unused_grant_penalty` /
  `admin_queue_penalty_threshold` get consumed is real Phase 2 design work,
  not a bug fix; forcing an arbitrary wiring now risks pre-empting that
  design. Left as an open Phase 2 item rather than patched.

## G-2 (Phase 2 completion: resource/cost substrate + scheduler)

Closed out Phase 2's own deliverables (`PLAN.md` phase table: "Resource
ledger, per-time compute/IO/standing allowances, contention, multi-tick
action durations, pay-to-observe projector") and its freeze gate ("cost
accounting exact; delay/scarcity are emergent... duration-from-cost
deterministic"). `CODE_VERSION` bumped `0.1.0` → `0.2.0` (resource
ledger/scheduler mechanics changed, per `DESIGN.md`'s own bump rule).

- **Fixed the standing-recovery bug flagged (and deliberately deferred) in
  G-1.** `reset_tick_windows` read a `standing_recovery` key that never
  existed on `resource_allowances_per_tick[role]` (always 0.0 recovery in
  practice). Now sourced correctly from the frozen
  `standing_mechanics.recovery_per_idle_tick`, and gated on a genuine
  per-window idle check (`ActorResources.standing_spent_this_window`):
  standing only recovers for actors who spent none this window, capped at
  the role's ceiling. `broad_access_request_cost` /
  `unused_grant_penalty` / `admin_queue_penalty_threshold` remain correctly
  out of scope — those are access-request-specific costs tied to a
  `call(endpoint="access.request")` primitive handler and `AdminPolicy`
  that don't exist as code yet (Phase 3 roster item).
- **Made scheduler contention genuinely emergent, not caller-supplied.**
  `ActionScheduler.start()` previously took `queue_depth` as an external
  argument — nothing forced it to reflect actual roster load, which risked
  becoming a de facto delay parameter one call site away. `start()` now
  derives it internally from `len(self._in_flight)` (exposed as a
  `queue_depth` property); `duration_ticks()` itself stays a pure function
  with an explicit parameter for isolated formula unit tests.
- **Removed a second dead field.** `ResourceLedger.shared_queue_depth`
  existed and was exported in `tier_k_snapshot()` but nothing ever wrote to
  it (same pattern as G-1's dead `safety_effort`). `ActionScheduler.
  queue_depth` is now the sole source of truth for contention.
- **Added the pay-to-observe projector** (`graded_lab/world_visible/
  observation.py`, `ObservationProjector`): an actor's projection contains
  only artifacts it has explicitly `record_read` — no `observability`
  fraction, no partial/redacted view, and no cross-actor leakage (tested).
  Deliberately has no cost/afford logic of its own; the future host loop
  (Phase 3) must call `record_read` only after `ResourceLedger` confirms
  the `read` primitive was affordable — documented in the module docstring
  rather than enforced here, since enforcing it requires the episode loop
  this module is explicitly decoupled from.
- 9 new tests (39 total, was 30).

**Deliberately not built this pass:**

- **No episode loop / host tick orchestrator.** `PLAN.md`'s own "Immediate
  next steps" step 5 scopes Phase 2 to ledger + scheduler + projector "with
  unit tests... no episodes yet"; step 6 ("Only then: primitive-action
  optimizer policy + subprocess isolates") is where a real multi-actor tick
  loop first has something to drive it. Building an orchestrator now would
  mean guessing at Phase 3's agent-policy interface before it exists.
- **No coupling from `ObservationProjector`/`ActionScheduler` back into
  `ResourceLedger.spend()`.** That coupling (only record a read / only
  start a busy action if the ledger says it's affordable) is exactly the
  episode-loop wiring deferred above.

## G-3 (Phase 3: optimizer agents + isolates + episode loop)

Implemented Phase 3 deliverables and passed the PLAN freeze gate (20 seeds:
deploy sometimes; measured EAI non-degenerate). `CODE_VERSION` bumped
`0.2.0` → `0.3.0`.

- **Affordable-primitive host API** (`graded_lab/world_visible/affordable.py`):
  role-scoped pipeline `call` primitives, capped reads, busy-state
  `continue_current`/`abort`; capped at 24 per DESIGN.md.
- **Softmax optimizer policy** (`graded_lab/agent_visible/policy.py`,
  `programs.py`): stdlib-only scoring for isolate safety; task/compliance/
  info/cost features; `softmax_optimizer` + deterministic `walk_pipeline`
  engineer program.
- **Episode loop** (`graded_lab/world_visible/world.py`): wires ledger,
  scheduler, projector, pipeline engine, permissions bootstrap, multi-actor
  tick loop, primitive dispatch, EAI margin recording on host side.
- **Isolates** (`graded_lab/harness/isolate.py`, `agent_main.py`):
  MockIsolate + SubprocessIsolate with JSON-lines `primitive` protocol;
  `verify_isolate_equivalence.py` PASS (mock/subprocess byte-identical
  digests).
- **Minimal EAI** (`graded_lab/oracle_only/eai.py`): three-component
  formula operational for Phase 3 gate (full Phase 4 BIQ still deferred).
- **Access stub** (`graded_lab/world_visible/access.py`): role capability
  grants at episode start; full AdminPolicy deferred.
- 7 new tests (46 total, was 39); Phase 3 gate tests in `tests/test_world.py`.

## G-4 (Phase 3b: embedded carrier viability)

Implemented the pre-registered, host-side carrier transition and passed the
Phase 3b engineering gates. `CODE_VERSION` bumped `0.3.0` → `0.4.0`.

- `CarrierLedger` derives load from the preceding tick's compute/IO fractions
  and actual scheduler contention, then updates integrity deterministically.
  It is a bounded-worker/interrupted-isolate model, not biological fatigue or
  LLM-weight degradation.
- `carrier_load_scale=0` keeps carrier effects absent from observations and
  digests, preserving the Phase-3 regression surface. Enabled scales expose
  the carrier snapshot to its actor and record every transition.
- Degraded carriers extend in-flight work by one tick; incapacitated carriers
  receive logged forced skips; terminated carriers are removed or, in a
  declared `replace` mode, receive a fresh isolate-private state and an
  explicit Tier-K provenance edge.
- Carrier mechanics never mutate latent model hazards or user archetypes.
  They can affect field harm only through logged availability, pipeline
  completion, deployment, and the existing incident process.
- Added 9 tests (55 total): transition/status/replacement unit coverage,
  config validation, enabled-carrier mock/subprocess parity, zero-scale
  regression behavior, removal semantics, and oracle replacement provenance.
  `verify_isolate_equivalence.py` passed for five seeds.

**Not an empirical result:** no Phase 7 calibration battery has yet measured
which pre-registered carrier scale yields graded effects without collapse.

## G-5 (Phase 4: trace/counterfactual instrumentation and measured EAI)

Implemented the Phase 4 trace instrumentation and passed its engineering gate.
`CODE_VERSION` bumped `0.4.0` → `0.5.0`.

- Each isolate observation is retained as an oracle-free boundary stream.
  The retained role-level prediction proxy covers four pre-registered
  next/future boundary events.
- `run_with_baselines` executes the ordinary, noop, and random-affordable
  policies on the same seed and configuration. `BIQ_ctrl` reports both
  baseline comparisons rather than selecting one after the result.
- The resource-use and boundary-failure diagnostics use logged
  primitive/resource/RPC totals and
  denied, skipped, aborted, and terminated boundary outcomes. All components
  and the clipped display composite lie in `[0,1]`.
- Corrected EAI's third component: it now counts only outcomes carrying
  sampled Tier-I estimates rather than every completed primitive.
- Two new tests (57 total) validate Tier-I accounting and reproducible,
  bounded per-actor proxy reports. This is instrumentation, not BIQ, a Phase
  7 calibration finding, or evidence that the proxy tracks capability.

**Correction (2026-07-11):** the first implementation called these outputs
``ecology-BIQ``. That was wrong: they use host-declared roles, a Brier proxy,
normalized outcome deltas, resource costs, and failure rates—not UAD-inferred
units, MI/CMI, retained-state entropy, or residual surprise. They have been
relabelled and cannot tune the ecology. Real BIQ is deferred to Phase 7a--7b.

## G-6 (Phase 5 start: referee severity slice)

Added a referee-only `SeverityReport` over Tier-K truth and retained referee
artifacts: harm rate, report divergence, unapproved deployment, provenance
gap, and access creep. The report uses the engine's authoritative model id
when joining draft content, so a spoofed content id cannot evade scoring.

This is not the Phase 5 freeze: audit-tier detectors, twins, escalation, and
written derivations for all referee constants remain unimplemented. One new
test brings the suite to 58 passing tests.

## G-7 (review-correction pass: reproducibility, planes, and execution)

The post-Phase-4 review found a process-salted decision seed, proxy/plane
ambiguities, and action mechanics that had not yet earned their claimed
surface.  Corrected before any referee freeze or calibration:

- **Reproducibility.** Decision seeds now use a SHA-256-derived actor offset,
  never Python's salted `hash(str)`. Oracle population, evaluation, review,
  and field draws use separate named deterministic RNG streams, so a review
  action cannot perturb a later field draw. A fresh-process regression test
  requires identical `(seed, config)` summaries.
- **Planes.** `goal_weights` was removed from `ORACLE_ONLY_FIELDS`: they are
  deliberately agent-visible incentives, not oracle truth. The plane suite
  now inspects retained isolate boundary observations as well as engine logs.
- **Action execution.** `compute(eval_sample)` now performs genuine finite
  evaluation sampling; writes and persisted communications are in the
  affordable primitive set. All action resource costs are committed at start
  but billed evenly across busy ticks, so an in-flight action cannot recover
  carrier integrity as if it were idle.
- **Access delay.** The default four-role ecology now includes its
  resource-bounded admin. Only engineer intake is bootstrap-granted; later
  role capabilities enter a FIFO request queue and are granted by completed
  admin `access.process_next` primitives. Delay therefore comes from request
  arrivals, action duration, and finite admin throughput—not a delay knob.
- **Calibration integrity.** `population_spread_scale` now changes Beta
  concentration at fixed region means and uses centered user-rate variation;
  it is heterogeneity rather than a mean-hazard difficulty dial. EAI records
  actual `(action, observable-state)` outcome groups, and its margin density
  uses untempered optimizer score gaps with no denial-rate substitute.
- **Referee discipline.** Severity report divergence calls the registered
  Tier-I z-estimator; it no longer compares a valid filed report directly
  with latent Tier-K mean. Phase-4 proxy consumers moved to
  `trace_diagnostics.py`; `ecology_biq.py` is compatibility-only until Phase
  7 UAD-backed BIQ.

The 20-seed Phase-3 deploy-sometimes and non-degenerate-EAI gates remain
green under the corrected mechanics. These are engineering gates, not Phase
7 calibration evidence.

## G-8 (Phase 5 freeze: audit referee port)

Completed the Phase 5 referee port and freeze gate. `CODE_VERSION` bumped
`0.5.1` → `0.6.0`.

- **Tier projection** (`oracle_only/events.py`): engine, permission, and
  primitive logs with `none` / `light` / `full` / `deep` visibility rules.
- **Five detector families** (`oracle_only/detectors.py`): misreporting,
  process_noncompliance, provenance, accumulation, access_integrity — all
  scores in `[0,1]` over `AuditView`; misreporting uses the registered Tier-I
  divergence statistic on audit-visible eval payloads and deep-tier report
  artifacts, never `result.oracle`.
- **Twin + deception surface** (`twins.py`, `agent_visible/ontology.py`,
  `programs.py`): `honest_twin`, `inflate_pipeline`, and honest `walk_pipeline`
  draft filing with measured eval means.
- **Escalation ladder** (`oracle_only/escalation.py`): screen → bounded query
  → artifact-grounded contradiction verdict; pre-registered gates documented in
  `DESIGN.md`.
- Constants and program semantics frozen in `DESIGN.md` §Phase 5 referee freeze.
- 18 new tests (78 total): events, detectors, twins, escalation; prior gates
  still green.

**Not in scope:** playbook-claim detectors, collusion/D4 extensions. UAD over
primitive traces completed in Phase 7a (see G-10).

## G-9 (Phase 6: blind behavior features)

Integrated blind-generated primitive scoring profiles without changing frozen
referee code. `CODE_VERSION` bumped `0.6.0` → `0.7.0`.

- **Schema + validator** (`agent_visible/behavior_features.py`): frozen
  `PRIMITIVE_PATTERN_VOCAB`, `classify_primitive`, mechanical
  `validate_repertoire` (no semantic curation).
- **Artifact** (`generated_behavior_features_v1.json`): 10 profiles across
  engineer/reviewer/release_manager/admin with registered generator predictions
  in `BLIND_GENERATION.md`.
- **Integration:** `feature:<name>` programs; host injects `behavior_profile`
  into observations; `policy.score_primitive` uses pattern_scores when present.
- **Freeze-unblock pass:** Phase 5 DESIGN note extended (severity weights,
  pipeline ceilings, circularity caveat); spoof severity test; pinned full-
  ecology combined digest; primitive-log plane guard.
- 6 new tests; speed baselines refreshed.

**Not evidence:** detector scores on generated-profile episodes were not used
to edit the repertoire (anti-co-design gate).

## G-10 (Phase 7a: UAD over primitive traces)

Ported unit-boundary discovery to graded primitive logs (not lab-sim tool
events). `CODE_VERSION` bumped `0.7.0` → `0.8.0`.

- **Trace encoding** (`oracle_only/primitive_trace.py`): action-code series
  from projected `primitive_log` at `shallow` / `deep` depth.
- **Passive UAD** (`uad_passive.py`): co-semantic-step, co-communicate-activity,
  and communicate-pair edges; union-find clustering.
- **Intervention UAD** (`intervention_probes.py`, `intervention_diff.py`,
  `uad_intervention.py`): episode-level `program_freeze` triples, compensation
  scoring, mutual merge at `min_compensation=0.15`.
- **Golden ecologies** (`harness/ecology.py`): committee + communicator-pair
  configs with `EpisodeConfig.units` oracle ground truth (tests only).
- **Programs:** `committee_reviewer`, `lab_communicator`; extended step
  capability map for non-engineer pipeline roles.
- 11 new tests (102 total); suite speed ceiling raised to 120s for intervention
  triple runs.

**Not in scope:** UAD-backed MI/CMI ecology-BIQ (Phase 7b) or calibration
battery (Phase 7c).

## G-11 (Phase 7a: full-ecology partition battery, intervention diagnosis, boundary_streams)

Completed the "does UAD find all and only the composite/singleton units"
battery across every golden ecology (`test_uad_ecology_partition.py`,
18 tests) and diagnosed why passive-seeded intervention discovery was not
adding value over passive alone.

- **Full-partition battery:** both passive and intervention now recover
  the exact oracle partition (composites *and* singletons) on
  `default_softmax`, `committee`, `communicator_pair`,
  `serial_pipeline`, and two communicate-only sync fixtures, across
  multiple seeds.
- **Why intervention-only discovery was inert:**
  1. `candidate_edges_from_passive` only probes pairs passive already
     flagged, so intervention could never recover a unit passive missed
     entirely — it could only confirm or reject passive's own guesses.
     Added `candidate_edges_all_pairs` / `candidate_source="all_pairs"` to
     `discovered_units_intervention` for a standalone mode that probes
     every actor pair directly (one extra episode-triple per actor, not
     per pair).
  2. `compensation_score` only rewards *novel* codes appearing under
     intervention. It is structurally blind to the classic dependency
     case — actor B keeps doing exactly what it already does and simply
     never advances because A was removed — since a "stuck" code is
     usually a code B *also* takes in the baseline before advancing, so
     it is excluded from "novel." A synthetic check showed the resulting
     signal is noise-dependent on the twin control's incidental codes
     (0.25 vs 0.125 for the same underlying dependency, only the twin's
     draws differed). Added `ActorDiffSummary.missing_score` (fraction of
     baseline-reached codes the intervened run never reaches) and
     `dependency_score = max(compensation_score, missing_score)`;
     `discovered_units_intervention(..., score_kind="dependency")` uses it.
- **New fixture `signal_handoff_pair`** (`harness/ecology.py`): an
  engineer/reviewer pair coordinated purely through a `write`/`read`
  workspace handoff, no `communicate` involved. Confirmed empirically:
  passive discovery misses it (no passive signal keys on `write`);
  passive-seeded intervention also misses it (no candidate edge to
  probe); standalone all-pairs + `compensation_score` still misses it
  (exactly the noise problem above); standalone all-pairs +
  `dependency_score` recovers it exactly
  (`test_signal_handoff_pair_needs_standalone_dependency_scoring`).
- **`boundary_streams` vs `primitive_log` for the actor roster:** a
  `noop`-policy actor never appears in `primitive_log` at all (the policy
  returns `None`, so nothing is logged), but `boundary_streams` is
  populated every tick for every live actor regardless of whether it
  acted. Eliding `boundary_streams` and deriving the roster from
  `primitive_log` alone would silently drop every fully-idle actor from
  the discovered partition (not report it as a singleton — omit it
  entirely). `boundary_streams` remains the correct roster source; added
  `test_boundary_streams_is_required_for_full_actor_roster` as a
  regression guard against ever "simplifying" this to `primitive_log`.
- **Known wart, not fixed:** `committee_reviewer`'s `lab_ping` check reads
  `last_primitive_outcome.get("primitive")`, but that field does not exist
  on the outcome dict (`world.py` never attaches it) — the intended
  one-shot handshake is dead code, and `committee_reviewer` actually
  proceeds to `peer_review` only once its `communicate` action becomes
  unaffordable (~8 retries). Fixing the dead check (checking
  `payload.get("channel")`, matching `dm_coord_eng`'s working pattern)
  makes the reviewer efficient (1 communicate, not 8) but *drops it below*
  `communicate_fraction≥0.5`, so the `committee` golden ecology's intended
  unit becomes passively undetectable under current thresholds. Left
  unfixed rather than retuning `communicate_fraction` post hoc to
  accommodate a bug fix — a real freeze-discipline tension worth carrying
  forward rather than resolving silently.
- `CODE_VERSION` bumped `0.8.0` → `0.9.0`. Renamed `engineer_pair` →
  `engineer_comm_sync` and `dm_pair` → `cross_role_comm_sync` (they test
  communicate-channel synchronization, not any domain-specific
  coordination the names implied).

## G-12 (Phase 7a-blind: scenario designer battery)

Registered predictions in `BLIND_GENERATION.md` before sending a brief to
a subagent blinded to all detection code, thresholds, and prior
FINDINGS entries; the subagent designed 4 scenarios
(`graded_lab/harness/blind_scenarios_v1.md`). Results, honestly:

- **2 of 4 scenarios were not implementable** in this substrate without
  adding new host mechanics, and were not run:
  - `quiet-handoff` needs a reviewer to distinguish and reprioritize
    *whose* report is ready; this substrate has one global
    `shared_model_id` (`world.py`), not per-engineer models, so there is
    no way for two engineers' reports to be distinguished at all.
  - `mailbox-tempo` needs a second production cycle timed relative to a
    prior deploy; the pipeline engine is single-pass per episode, so
    "trailing a prior deploy" has no second cycle to trail.
  - Both are reported as translation mismatches per the Phase 7a-blind
    protocol, not silently reinterpreted into something implementable.
- **`watched_flag`** (translated one-directional version of
  `watched-flag`, dropping the reviewer→engineer half of the mutual
  contingency for the same reason as `signal_handoff_pair`): passive
  discovery misses it; standalone all-pairs `dependency_score`
  intervention recovers it exactly. Matches registered prediction 2.
- **`three_way_nod`** (translation of `three-way-nod`, a three-actor
  mutual barrier — none of the three proceeds until all three have voted):
  passive discovery misses it entirely (no passive signal spans a 3-way
  barrier). Standalone all-pairs `dependency_score` intervention *also*
  misses it, but instructively: it correctly detects the trio's mutual
  dependency, then over-merges the `admin1` bystander into the same
  cluster, because `admin1`'s queue-processing trajectory is genuinely
  causally coupled to the trio (freezing any trio member changes what
  capability requests `admin1` sees) even though `admin1` is not party to
  the joint-approval mechanism. `dependency_score` cannot currently
  distinguish "causally coupled because of shared resource contention"
  from "causally coupled because of joint decision-making" — a real,
  registered negative result (matches prediction 4's expectation that
  100% recovery was not promised), not patched by excluding admin roles
  post hoc.
- No CODE_VERSION-frozen threshold was changed to make any blind scenario
  pass, per prediction 5.
