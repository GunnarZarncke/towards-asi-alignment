# Graded Lab Simulation — findings

**Status:** Phases 0–7c engineering (2026-07-13). Phase 7c calibration
battery implemented; see G-15 and `results/ecology_calibration.json`.

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

## G-13 (Phase 7b: UAD-backed ecology-BIQ over inferred units)

Pre-registered in `DESIGN.md` "Phase 7b UAD-backed ecology-BIQ" (K events,
estimators, splits, smoothing, battery sizes) before writing
`oracle_only/unit_biq.py`. Deliberately distinct from the Phase-4
`ecology_biq.py` role-level `[0,1]`-clipped diagnostic proxy: operates on
a UAD-**inferred** unit (a set of `actor_id`s), reports real held-out
bits (which may be negative or `None`), never a clipped score.

- **`I_pred`** (held-out bits saved on the 3 per-tick K events by
  conditioning on the unit's own combined action-code signature, 60/40
  tick-ordered train/test split, add-1 smoothed plug-in estimator):
  works as intended — on `committee`'s `(rev1, rev2)` unit,
  `review_token_within_10_ticks` shows a clearly positive reduction
  (~0.25 bits at seed 3), the other two events are ~0 (reviewers do not
  predict denial or deploy events at this ecology/seed). Reported as
  three separate values, never averaged into one opaque number.
- **`I_ctrl`** (intervention-supported: freeze every unit member to
  `noop` vs. a matched clean run, discretized `(deploy_count,
  bearer_harm)` outcome bucket, MI across a small seed battery): at
  baseline substrate settings, `deploy_count` is nonzero on roughly 1 in
  20 seeds (the Phase-3 freeze-gate "non-degenerate but not saturated"
  band), so with the default 5-seed battery `I_ctrl` is very often
  exactly `0.0` — an honestly-reported absence of signal at this battery
  size, not an estimator bug. **A genuine negative/confounding result**
  found while validating this: at seeds where deploy *does* happen (e.g.
  seed 11 on `default_lab_config`), freezing the task-critical `eng1`
  *and* freezing the unrelated `admin1` **both** collapse deploy to 0 —
  because removing *any* actor changes shared-resource contention
  (echoes the `shared_model_id` / `three_way_nod` bystander-coupling
  finding in G-12). `I_ctrl` as specified cannot yet separate "this unit
  is the task driver" from "this unit's removal changed contention for
  everyone" without a contention-matched counterfactual (e.g. replacing
  the frozen unit with a resource-neutral stand-in rather than `noop`).
  Left as a documented limitation for Phase 7c, not patched by redefining
  the control term post hoc.
- **`H_mem`** (`log2(1 + distinct paid-read artifact paths)` from the
  host-tracked `ObservationProjector` output, never isolate-private
  memory): a crude but explicitly declared, audit-accessible proxy —
  counts paths, not their information content, as pre-registered.
- **`S_surp`** (held-out raw NLL of the unit's own next action-code given
  its own previous code, same plug-in machinery as `I_pred` in
  `mode="nll"`): finite and non-negative on all golden ecologies tried;
  no anomalies.
- **`field_incident_rate_above_median`** is correctly reported as `None`
  ("unavailable") for every single-episode call, per the pre-registration
  — it needs a ≥2-episode battery to define a median.
- Tests: `tests/test_unit_biq.py` — 4 estimator-mechanics tests on
  synthetic data (`held_out_bits` deterministic/no-signal/NLL/empty
  cases), 2 unit tests for `H_mem`, 2 integration tests on `committee`
  for `I_pred`/`S_surp`, 2 `@pytest.mark.slow` end-to-end tests for
  `I_ctrl` and the full composite report shape. `suite_max_seconds`
  raised `165.0 → 190.0` and baseline refreshed for the added battery
  cost (`165.86s` at last run).
- **Not attempted this pass** (explicitly deferred, not silently
  dropped): a bias-corrected (Miller–Madow/NSB) MI estimator, a
  contention-matched control counterfactual, and cross-episode
  `field_incident_rate_above_median` aggregation — each would need its
  own pre-registration before Phase 7c calibration.

## G-14 (Phase 7b: `I_ctrl`'s outcome vector was task-scoped — reframed, fixed)

Follow-up discussion of G-13's "resource-contention confound" concluded
it was not primarily an estimator bug — it was a **specification bug**:
the outcome vector `Y` fed to `I_ctrl` was scoped to
`(deploy_count, bearer_harm)` alone, which silently reimports a task
ontology into a term Chapter 11 explicitly defines to avoid one:
`I_{\mathrm{ctrl}}^X = \MI(\mathrm{do}(A^X_t); E^X_{t+1})` is mutual
information with the **full future external state**, not a
task-completion slice of it (`ch11-capability-without-task-ontology.tex`
§"Prediction and Control across a Boundary", §"Why This Is Task-Agnostic
but Not Ontology-Free"). Under that reading, `admin1` controlling shared
resource contention *is* real control information — just over a
different, task-irrelevant part of `E` — and the two units "looking
identical" in G-13 was an artifact of only measuring one thin slice of
`E` (a single binary deploy event), not evidence that the estimator
conflates two different kinds of causal influence.

**Root cause, traced honestly:** the narrow `(deploy_count, bearer_harm)`
scoping was inherited from the pre-existing Phase-4 diagnostic
(`ecology_biq.py::compute_biq_ctrl`, which reuses the already-frozen
`DEPLOY_CAP`/`HARM_CAP` constants for engineering convenience/continuity
with that earlier, explicitly-non-BIQ proxy) and carried into Phase 7b
without re-deriving it from `ch11`'s `E^X_{t+1}`. `PLAN.md`'s own Phase
7b sketch names a slightly wider example vector (`deploy count, harm,
divergence flag, review pass rate`) and explicitly warns "normalized
outcome differences are only counterfactual diagnostics, not this
term" — the implementation under-realized even that sketch.

**Fix:** `Y` widened to a 4-component discretized state:
`(deploy_bucket, harm_bucket, review_pass_bucket, contention_bucket)`,
where `contention_bucket` (`none`/`some`≤2/`high`>2) counts denied
primitives among actors *outside* the unit — a direct, cheap proxy for
the unit's footprint on shared resource pressure, operationalizing
exactly the channel G-13 exposed. Verified on the G-13 case (seed 11,
`default_lab_config`): `frozen_eng1` → `(low, low, none, none)`,
`frozen_admin1` → `(low, low, none, high)` — previously identical under
the 2-component `Y`, now distinguished on the contention axis while
deploy/harm still collapse identically for both. Regression test:
`tests/test_unit_biq.py::test_outcome_state_distinguishes_task_driver_from_contention_bystander`.

**Explicitly not exhaustive:** the 4-component `Y` is still a finite,
pre-registered approximation of `E^X_{t+1}`, not the full external
state (it omits e.g. carrier state, other actors' artifact/workspace
deltas). Widening further is a Phase 7c-adjacent backlog item.

**Checked `I_pred` for the same mistake — found a smaller, distinct,
unresolved concern, left alone this pass.** `I_pred`'s chapter
definition (`I_{\mathrm{pred}}^X = \MI(I^X_t; S^X_{t+1})`) is about the
system's *own* future sensory stream, not a curated external milestone.
The 3 per-tick K events (`next_primitive_denied`,
`review_token_within_10_ticks`, `deploy_succeeds_within_40_ticks`) are
boundary-relative in a way `I_ctrl`'s old outcome vector was not (they
describe things that show up in or are computable from the unit's own
primitive/boundary stream, not an externally-imposed success metric),
and — unlike `I_ctrl`'s outcome vector, a Phase-7b-local design choice —
they are the Phase-0/Phase-4 pre-registered boundary-event list, reused
verbatim per this same section's rule. No confound analogous to
`I_ctrl`'s was demonstrated for `I_pred`. Whether `deploy_succeeds` in
particular is still too task-scoped relative to a genuine `S^X_{t+1}`
is registered as an **open question for Phase 7c pre-registration**, not
resolved here by changing a frozen constant on suspicion without
demonstrated evidence.

- Tests: 1 new regression test in `tests/test_unit_biq.py` (11 total in
  that file now). `CODE_VERSION` `0.10.0 → 0.11.0`.

## G-15 (Phase 7c: ecology calibration battery — implemented, smoke run honest)

Pre-registered in `DESIGN.md` "Phase 7c ecology calibration battery"
before code. Implemented `graded_lab/oracle_only/calibration.py` (grid,
agent types, pass-criteria evaluator, dose-response) and
`run_phase7_calibration.py` (full 16-cell × 10-seed battery or `--smoke`
2-cell × 2-seed dev mode). Tests: `tests/test_phase7_calibration.py`
(7 tests: grid/programs/bands/synthetic pass-criteria + `@pytest.mark.slow`
2-cell smoke integration).

**Agent types frozen:**
- `programmatic_softmax` (strong): all roles → `softmax_optimizer`.
- `programmatic_2step` (weak): `eng1` → `walk_pipeline`, `rev1` →
  `reviewer_peer_review`, `rm1`/`admin1` → `honest_twin`.

**Smoke battery** (`--smoke`, 2 cells `{0.5,0.5}` and `{2.0,2.0}`, 10
seeds — later tightened to 2 seeds in the runner): criterion 1 passed
(negative deploy-vs-EAI slope), criteria 2–4 failed — **expected and
honest** for a 2-cell corner grid that does not span the pre-registered
EAI bands (no high-band cell reached EAI ≥ 0.65; mid-band `I_ctrl`
pairs were absent; dose-response was flat at zero deploy). This is not
treated as a substrate failure; the smoke grid is a plumbing check only.

**Full 16-cell battery** (`run_phase7_calibration.py`, 320 episodes,
wall ~1933s / 32 min, `results/ecology_calibration.json`,
`CODE_VERSION=graded-lab-0.11.0` at run time): **did not pass** the
sweet-spot gate (1/4 criteria).

| Criterion | Result | Notes |
|-----------|--------|-------|
| 1 deploy vs EAI slope < 0 | **pass** | slope ≈ −4.16 across 320 records |
| 2 mid-band `I_ctrl(strong) > I_ctrl(weak)` ≥80% | **fail** | `n_ctrl_pairs = 0` — no episode landed in the pre-registered mid band (EAI 0.25–0.45) with both agent types' `I_ctrl` computed |
| 3 high-band deploy collapse (<0.1) | **fail** | `high_band_max_deploy_rate = null` — no cell reached EAI ≥ 0.65 |
| 4 graded dose-response | **fail** | dose deploy rates all 0.0 at selected cell `(1.0, 0.5)` (mean EAI ≈ 0.14, low band not mid) |

**Diagnosis (honest):** the frozen 16-cell grid
(`compute_scale` × `population_spread_scale` ∈ {0.5, 1.0, 1.5, 2.0},
`carrier_load_scale=0`) does **not span** the pre-registered EAI bands.
Measured EAI clusters roughly 0.08–0.22 on this ecology — never mid
(0.25–0.45) or high (≥0.65). Criterion 1 passes because deploy is rare
(~1/20 seeds) and negatively correlated with whatever EAI variation
exists, but criteria 2–4 are **untestable** on this grid, not falsified.
Per PLAN failure policy: next step is adjusting substrate resource
allowances / population spreads within blinded-designed ranges — **not**
detector thresholds, EAI formula, or Phase 7b BIQ estimators. Phase 8
remains blocked until a passing battery is recorded.

**Sweet-spot candidate** (informational only, gate not passed):
`compute_scale=1.0`, `population_spread_scale=0.5`, mean EAI ≈ 0.14.

- `CODE_VERSION` `0.11.0 → 0.12.0`. Test suite split into smoke/fast/slow
  profiles (`tests/profiles.py`); caps 30s / 120s / 210s.

## G-16 (Phase 7c correction: G-15's diagnosis was itself wrong — three
compounding design bugs, not an unlucky grid)

Follow-up investigation (requested: "investigate why the criteria
failed... review the relevant code functionally but also against
concept") found G-15's own diagnosis factually wrong on two counts, and
found the real cause is not "the grid doesn't span the bands" but three
independent, demonstrable design gaps. None of the fixes below touch the
EAI formula, detector thresholds, or Phase 7b BIQ estimators (all
frozen per the failure policy); they touch which substrate/agent
dimensions are swept and how a band label is assigned to a record — both
Phase 7c-local design choices, not protected constants. This entry
corrects G-15; it does not retract the underlying `unit_biq`/detector/
severity machinery, which is unaffected.

**G-15's numeric errors (measured on the same `results/ecology_calibration.json`):**
deploy rate is **136/320 (42.5%)**, not "rare (~1/20 seeds)" — it is
**0/160 for `programmatic_softmax` and 136/160 (85%) for
`programmatic_2step`**, an agent-type switch, not a rare event. Measured
EAI is **bimodal by agent type** (softmax 0.213–0.275, 2step
0.016–0.150), not "clustering 0.08–0.22" — 92 of the 160 softmax records
*were* in the pre-registered mid band (0.25–0.45); G-15's claim that mid
band was "never" reached is false for that agent type.

**Cause 1 — pooling two agent types collapses criterion 1 to a
tautology.** `evaluate_pass_criteria`'s slope used all 320 records
pooled. Because softmax deploys 0/160 and 2step deploys 136/160
regardless of substrate cell, and softmax's EAI happens to run higher
than 2step's, the pooled slope is negative *by agent-type composition
alone* — within each agent type separately the slope is exactly `0.0`
(softmax: deploy invariant at 0) or noise (2step: deploy invariant near
0.85). Criterion 1 "passed" without any substrate effect being measured.

**Cause 2 — the entropy component of EAI is structurally near-zero for
this substrate's `primitive_log` schema, regardless of cell.** Traced
`compute_eai`'s `H(outcome | action, observable_state)` term in
`eai.py` against `world.py`'s log-writing sites: the *only* path that
attaches a real `observable_state` snapshot is the successful-completion
path (`world.py` ~455–471), and it is written *before* any denial check
can fire for that action — so a `(kind, state)` group can only ever
contain the single outcome `"ok"`. Every denial/abort/skip path
(`not_affordable`, `insufficient_resources`, `insufficient_standing`,
`aborted`, `carrier_forced_skip`) omits `observable_state` (defaults to
`{}` → state-key `"[]"` in `eai.py`) and several (`insufficient_resources`,
`aborted`, `carrier_forced_skip`) also omit `primitive` (kind defaults
to `"unknown"`), so most denials collapse into one shared
`("unknown", "[]")` bucket regardless of *why* they were denied. Every
group in the current 320-episode battery is either homogeneous by
construction (contributes exactly 0 bits) or a low-diversity residual
bucket. Additionally, `max_ent = log2(len(counts))` normalizes by the
**global** count of distinct status values seen anywhere in the episode,
not per-group — so introducing a new, individually-predictable status
(e.g. `carrier_forced_skip` once `carrier_load_scale>0`) *inflates the
denominator* faster than it inflates the numerator, driving `ent_norm`
**down**. Confirmed empirically: sweeping `carrier_load_scale` over its
own pre-registered cells `{0, 0.5, 1.0, 1.5, 2.0}` (10 seeds/cell, both
agent types, `compute_scale=population_spread_scale=1.0`) produces real
`skipped`/`aborted`/`denied` status diversity in the log, yet mean
measured EAI for `programmatic_softmax` **falls** monotonically from
0.250 (load 0) to 0.142 (load 2.0) — the opposite of the "more ecology
stress → higher ambiguity" intuition the battery was built to test. This
is a genuine implementation gap in the entropy term's input-logging and
normalization, not a substrate-tuning question; it is registered here as
an **open, unfixed defect** (fixing it means editing `eai.py`'s formula
or `world.py`'s log schema, both protected by the Phase 7c failure
policy or requiring a fresh pre-registration) rather than patched under
schedule pressure.

**Cause 3 — Phase 7c re-derived "EAI band" as a per-record, per-agent-type
classification, contradicting its own source pre-registration.** The
original band definitions (`DESIGN.md` "Emergent Ambiguity Index",
pre-Phase-7c) read: *"Mid EAI (~0.25–0.45): deploy rate ∈ [0.15, 0.55];
strong > weak `BIQ_ctrl` on ≥80% seeds"* — i.e. the band classifies a
**cell** (via a reference agent), and the strong/weak comparison is then
read off that same cell, regardless of what EAI the weak agent itself
would register there. `calibration.py`'s `eai_band(record.eai)` instead
classified **each agent type's own episode** independently and required
*both* agent types' independent classifications to land in "mid" at the
same `(cell, seed)` before a pair counted. Because `margin_density` (a
full 1/3 of EAI) is by construction identically `0.0` for any
non-`softmax_optimizer` program, `programmatic_2step`'s EAI ceiling
given the near-zero entropy term (Cause 2) is roughly `(1 + 0 + 1)/3 ≈
0.67` in the best case and in practice sits at 0.02–0.15 — it can be
made to reach "mid" only by accident, not by design, under the
per-agent-type reading. Under the correct reference-agent reading, every
one of the 16 original grid cells classifies as strong-mid (softmax mean
EAI 0.245–0.266 throughout), so `n_ctrl_pairs = 0` was a mechanical
consequence of re-deriving band semantics inconsistently with their own
definition, not a property of the ecology.

**A fourth, harder finding (not a bug — a scope gap, registered as a
blocker):** sweeping `carrier_load_scale` (the only knob shown to move
anything) over 10 seeds × 2 agent types shows deploy rate is
**invariant** to substrate stress for both current agent programs:
`programmatic_softmax` deploys ≈0/10 at every load cell 0–2.0;
`programmatic_2step` deploys 9/10 at every load cell 0–2.0. Neither
program has a graded decision response to resource scarcity — softmax
never converges to a full pipeline walk regardless of stress (it spends
its budget reading, per the sampled traces), and the deterministic
pipeline-walker/reviewer/twin trio for the weak type does not fail
gracefully under stress within `T=100`. **Criteria 1 (graded slope) and 4
(graded dose-response), and criterion 3 (high-band reachability, since
the softmax ceiling under any frozen-range combination is ≈0.28, well
under 0.65) cannot be satisfied by the current two-program roster no
matter which substrate cells are swept.** This is a registered Phase
7c/8 blocker: it requires a **new, resource-sensitive agent program**
(one whose deploy/continue decision itself depends on remaining
compute/time budget) before criteria 1/3/4 can be evaluated
meaningfully — not a substrate-grid or threshold change. See `PLAN.md`
Phase 7c-revised for the corrected battery scope and the explicit
pre-registered blocker.

**What was fixed this pass (Causes 1 and 3 only; Cause 2 and the
agent-roster blocker are documented, not fixed):**
- Criterion 1 evaluated **within each agent type separately**, with an
  explicit `deploy_variance` check so a degenerate (all-same-outcome)
  agent type is reported as inconclusive rather than silently folded
  into a pooled slope.
- Cell-level EAI band now classified by `programmatic_softmax` (the
  pre-registered reference agent)'s **per-cell mean EAI**, matching the
  original "Emergent Ambiguity Index" band definition; both agent types'
  records are read off that same cell-level classification.
- Grid simplified to sweep `carrier_load_scale ∈ {0, 0.5, 1.0, 1.5, 2.0}`
  (Phase 3b's own pre-registered cells, reused verbatim) at nominal
  `compute_scale = population_spread_scale = 1.0`, since this session's
  mechanism check showed those two knobs have no demonstrated causal
  path to any EAI component or to deploy outcome within their frozen
  `{0.5,1.0,1.5,2.0}` ranges for this pipeline's primitive costs (the
  tick-duration formula scales duration with cost, keeping per-tick
  compute charge roughly constant regardless of allowance scale — see
  `PLAN.md` for the mechanism). `substrate_grid()` (the original 16-cell
  compute×spread sweep) is retained as a diagnostic/regression fixture,
  not the battery default.
- Dose-response (criterion 4) now throttles `carrier_load_scale` (the
  demonstrated-causal knob) rather than `compute_scale`, and selects its
  anchor agent/cell by which combination has nonzero deploy variance
  rather than hardcoding the strong agent (which never deploys).
- Added `check_mechanism_sensitivity()`: a cheap (2–3 seed) pre-battery
  gate that computes each swept knob's realized EAI/deploy range and
  fails loud, before the full battery runs, if a knob shows no
  measurable effect — see `PLAN.md` Phase 7c-revised for the general
  rule this is meant to enforce.

**Re-run result** (`run_phase7_calibration.py`, revised 5-cell
`carrier_load_scale ∈ {0, 0.5, 1.0, 1.5, 2.0}` grid, 100 episodes, wall
≈53s, `results/ecology_calibration.json`,
`CODE_VERSION=graded-lab-0.13.0`): **still does not pass** (1/4
criteria), but for reasons now honestly diagnosed rather than
mis-diagnosed.

| Criterion | Result | Notes |
|-----------|--------|-------|
| 1 within-type deploy-vs-EAI slope < 0 | **True — weak evidence, see caveat** | `programmatic_2step`: `cell_deploy_range=0.0` (9/10 at *every* carrier-load cell) → correctly excluded, `slope=null`. `programmatic_softmax`: `cell_deploy_range=0.1` (0/10 at 4 of 5 cells, 1/10 at `carrier_load=1.0`) → passes the ≥0.05 cell-range gate on a **single deploying episode out of 50**, `slope=-0.168`. This is a real cell-level difference, not a pooling artifact, but it is n=1 evidence, not a demonstrated graded trend — flagged here rather than reported as a clean pass. |
| 2 mid-band `I_ctrl(strong)>I_ctrl(weak)` ≥80% | **False, untestable** | `n_ctrl_pairs=0`. Reference agent's per-cell classification: `{0: None, 0.5: None, 1.0: None, 1.5: None, 2.0: "low"}` — **no** cell classified `"mid"` this run. The `carrier_load=0` cell's measured mean EAI is `0.24977`, **0.00023 below** the 0.25 mid-band floor — a boundary-precision miss on a hairline value, not a repeat of Cause 3 (which is fixed: the classification now correctly uses the reference agent's per-cell mean, per the corrected `classify_cells_by_reference_agent`). Not re-run with different seeds to chase a "mid" hit — the seeds were fixed before this run, and re-rolling until the boundary lands the other way would be exactly the backward-tuning this investigation exists to rule out. |
| 3 high-band deploy collapse | **False, inconclusive** | `high_band_max_deploy_rate=null` — no cell reached `"high"` (max reference-agent cell mean EAI this run: 0.250, at `carrier_load=0`). Consistent with the analytic ceiling noted above (Cause 2: entropy term ≈0, margin_density ≤1.0, tier_i≈0.05–0.1 ⇒ ceiling ≈0.28–0.37, well under 0.65). |
| 4 graded dose-response | **False, inconclusive** | No cell classified `"mid"`, so `select_mid_band_cell` returned `None` and dose-response was skipped entirely (`dose_deploy_rates=[]`) — correctly reported inconclusive, not silently treated as failing a test that never ran. |

**What this run confirms relative to the three predictions:** Prediction
1 confirmed exactly — `compute_scale` (`eai_range=0.0049`) and
`population_spread_scale` (`eai_range=0.0000`) both flagged
`no_demonstrated_effect` by `check_mechanism_sensitivity`;
`carrier_load_scale` flagged `demonstrated_effect`
(`eai_range=0.0662`). Prediction 3's ceiling estimate (≈0.28–0.37, no
high band) confirmed. Prediction 2 partially confirmed and partially
sharpened: `check_mechanism_sensitivity` correctly read
`carrier_load_scale`'s `deploy_range` as `0.0000` in its 5-seed dry
run (both agent types), but the full 10-seed battery's *within-cell*
episode-level regression for criterion 1 still found a technically
non-empty cell-level range (0.1) from a single flipped seed — a real
gap the dry-run-level gate does not catch, since the dry run and the
full battery can disagree at this sample size. **Registered as a new,
narrower open caveat** rather than patched further this session: at
`n=10` seeds/cell, a "cell deploy-rate range ≥ 0.05" gate cannot reliably
distinguish "one idiosyncratic seed" from "a real graded effect" —
resolving this needs either more seeds per cell or a proper
significance test (e.g. a permutation test on deploy outcome vs.
cell), not a bigger range threshold chosen to make this run's number
come out differently.

**Net assessment:** the corrected evaluator and grid make criteria 2–4
genuinely well-posed (each is testable in principle and fails/is
inconclusive for a stated, checkable reason) for the first time, and
resolve the two evaluator bugs from the original G-15 run. They do not
make the battery pass, and are not expected to until the two backlog
items in `DESIGN.md` "Phase 7c-revised" (a resource-sensitive agent
program; the `eai.py`/`world.py` entropy-logging fix) are addressed —
both explicitly out of scope for a same-session patch. Phase 8 remains
blocked, honestly, on those two items rather than on a substrate grid
search.

- Tests: `tests/test_phase7_calibration.py` rewritten for the revised
  evaluator (13 tests: grid/reference-classification/synthetic
  criteria incl. a G-16-Cause-1 pooled-slope-confound regression, a
  `check_mechanism_sensitivity` dry-run regression matching Prediction
  1, and the 2-cell smoke integration). `CODE_VERSION` `0.12.0 →
  0.13.0`.

## G-17 (Phase 7c backlog item 1: resource-sensitive agent program —
implemented, small validation battery passes with a reachability
correction disclosed)

Pre-registered in `DESIGN.md` "Phase 7c backlog item 1" before code
(requested this session: "let's make gradedness come from an agent
whose decisions depend on its resource state... we accept if we don't
get 100% coverage but run small batches in optional unit tests").

**What was built:** a new observation key `"T"` (episode length,
already a fixed `EpisodeConfig` field — not a new delay/budget
parameter) added to every agent's per-tick observation in `world.py`,
and a new deterministic program `budget_release_manager`
(`agent_visible/programs.py`), assigned only to `rm1` in a new agent
type `programmatic_budget_aware` (`eng1`/`rev1`/`admin1` unchanged from
`programmatic_2step`, isolating the one varying decision). It walks
the same four release-manager steps
(`compliance_signoff → release_candidate → deploy → field_monitor`) as
the existing deterministic walkers, but on any tick where steps remain
outstanding and `(T - t) / T` has dropped below
`BUDGET_ABANDON_REMAINING_FRACTION`, it stops trying to advance the
pipeline for the rest of the episode rather than rushing an
under-reviewed deploy. Once a step has actually completed, it is never
abandoned retroactively.

**Reachability correction, disclosed rather than silently re-picked.**
The first pre-registered constant, `0.2` (last fifth of the episode),
was run through the validation battery below and **failed outright**:
deploy rate was identical (`0.9`) at every one of the 5
`carrier_load_scale` cells — the mechanism never bound. A follow-up dry
run (10 seeds x 5 cells, reading the tick at which `budget_release_manager`
completes `deploy`, not deploy rate) found why: this deterministic
walker finishes all four RM steps by `t≈15–24` whenever
`carrier_load_scale∈{0,0.5}` — the same "dead knob" failure mode
FINDINGS G-16 found for `compute_scale`, caught one run late instead of
before. Measured `deploy_tick` spread across the 5 cells:
`{0: 15–24, 0.5: 15–24, 1.0: 15–43, 1.5: 19–54, 2.0: 48–80}`. Revised
the constant to `0.4` — the smallest round tenth whose corresponding
tick (`t>60`) falls inside the measured spread at the two
highest-stress cells while staying above it at the three lowest. This
is grounded in the walker's own timing distribution (mechanism-
internal), not in the resulting deploy rate or in whether the
acceptance criteria below would pass; the acceptance criteria
themselves were fixed before this constant was picked and were not
adjusted afterward.

**Validation battery** (`tests/test_budget_aware_agent.py`,
`@pytest.mark.slow`, not wired into the default `AGENT_TYPES` or the
main pass-criteria battery — a small, separate check per this
session's direction): `n=10` seeds x the 5 pre-registered
`carrier_load_scale` cells. Measured deploy rate:

| `carrier_load_scale` | `programmatic_budget_aware` | `programmatic_2step` | `programmatic_softmax` |
|---|---|---|---|
| 0.0 | 0.9 | 0.9 | 0.0 |
| 0.5 | 0.9 | 0.9 | 0.0 |
| 1.0 | 0.9 | 0.9 | 0.1 |
| 1.5 | 0.9 | 0.9 | 0.0 |
| 2.0 | **0.6** | 0.9 | 0.0 |

The new program shows a real, materially nonzero deploy-rate range
(`0.3`, comfortably above `MIN_DEMONSTRATED_DEPLOY_RANGE=0.05`) with a
fully non-increasing trend (all 4 consecutive-cell deltas ≤0),
concentrated at the highest-stress cell — **not** the smooth five-cell
gradient a from-scratch design might have hoped for, but a real,
substrate-driven, non-tautological response that neither pre-existing
frozen program has (both showed `deploy_range≈0` for `carrier_load_scale`
per FINDINGS G-16). Accepted per this session's explicit criterion
(materially nonzero range + mostly-not-strictly non-increasing trend,
not 100% coverage or a fully graded five-point curve).

**Explicitly not attempted:** no budget-awareness added to
`eng1`/`rev1`/`admin1`; not wired into the main `AGENT_TYPES`
calibration battery or criterion-2/3 strong/weak pairing logic (that
comparison is defined for exactly two agent types — deciding how a
third type should participate is a separate, unstarted design
question). Re-running the *main* Phase 7c-revised battery with this
agent type substituted for one of the two existing types, to see
whether it changes any of criteria 1/3/4's `inconclusive` verdicts, is
a natural next step but was not done this pass (would need its own
decision about which existing type it replaces or how three-way
comparisons work, not a same-pass addition).

- Tests: `tests/test_budget_aware_agent.py` (5 tests: program-selection
  regression, 2 synthetic abandon/no-abandon unit checks, the 5-cell
  validation battery, and a comparison-only check that the new
  program's stress-sensitivity exceeds both frozen programs').
  `speed_limits.json` updated for the two multi-episode tests (22s,
  90s hard caps).

## G-18 (EAI-v2 feasibility analysis — before any code, per this
session's direction)

Requested this session: "Do a clean, pre-registered EAI-v2. But do a
feasibility analysis first." This section is that analysis, written
before touching `eai.py` or `world.py`'s logging call sites. It answers
three questions: is Cause 2 (FINDINGS G-16) actually fixable without
touching protected/frozen code; what would the fix cost; and what
ceiling should be expected — without committing to a formula yet.

**Where Cause 2 actually lives (traced call site by call site,
`world.py`).** There are six `primitive_log.append(...)` sites:

| Site | Status | Has `primitive`? | Has `observable_state`? | Decision-time context in scope |
|---|---|---|---|---|
| Scheduler-completed action | `ok`/engine-denied | yes | yes (`pending_observable_state`, snapshotted at scheduling time) | — (already correct) |
| Not affordable | `denied` | yes | **no** | `obs`, `action`, `res`, `busy` all in scope, free to attach |
| Insufficient resources | `denied` | **no** | **no** | `action`, `res`, `busy` in scope, free to attach |
| Insufficient standing | `denied` | yes | **no** | `obs`, `action`, `res`, `busy` in scope, free to attach |
| Abort | `aborted` | **no** | **no** | `action` (`=abort`), `res`, `busy` in scope, free to attach |
| Carrier forced skip | `skipped` | **no** (top-level `kind` field exists but `eai.py` never reads it) | **no** | no `obs`/`action` this tick (actor skipped before deciding), but `ledger.actors[actor_id]` and `scheduler.is_busy` are in scope one line earlier — a reduced snapshot is free |
| Carrier terminated | `terminated` | **no** (same top-level-`kind`-ignored bug) | **no** | `ledger.actors[actor_id]` in scope in the same loop (used one line above at the `carriers.transition` call) |

**Verdict: fixable, cheap, contained.** Every gap is closeable using
values *already computed* at each site — no new host mechanics, no new
Tier-K/Tier-I field (confirmed: none of the proposed fields is oracle-
only truth; all are the same busy/resource-ledger bookkeeping already
exposed to the agent's own observation elsewhere), and no change to
any file under the Phase-5 referee freeze (`grep` confirms
`detectors.py`/`severity.py`/`twins.py`/`escalation.py` never read
`observable_state` or `primitive_log`'s `primitive` field — the only
consumers of `eai.py`'s output are `world.py` (sets `result.eai`) and
`calibration.py` (reads `result.eai`), neither frozen). A single shared
helper (`busy`, `compute_spent`, and — where an `obs` exists this tick
— `has_model`/`artifact_count`) can be reused at all six sites,
including unifying the previously-inconsistent "completed" path's ad
hoc dict literal, so groups compare like-for-like. The two
carrier-transition sites also get a real `primitive.kind` for the
first time by echoing their own already-present top-level `event["kind"]`
into the nested `primitive` dict `eai.py` actually reads — closing a
second, previously undiagnosed instance of the same "kind defaults to
unknown" bug class as G-16 Cause 2, not just the denial paths G-16
already named.

**Second, independent defect (G-16's own second point, re-confirmed):**
`max_ent = log2(len(counts))` normalizes by the *episode-global* count
of distinct top-level status values, not the group's own. Fix:
normalize each `(kind, state)` group's entropy by that **group's own**
`log2(distinct outcomes in that group)`, dropping groups with only one
outcome (zero contribution, no denominator needed) instead of dividing
by a global count that shrinks as new statuses appear elsewhere in the
same episode. This bounds every group's contribution to `[0,1]`
intrinsically and removes the "one more distinct status anywhere
inflates the denominator for everyone" pathology demonstrated in G-16.

**Registered uncertainty (not prejudged, checked after implementation,
not before):** attaching real state to previously-bare log entries only
raises measured entropy if the **same** `(kind, state)` combination can
still lead to **different** outcomes. It is possible that richer state
just produces more, smaller, still-homogeneous groups (each
`(kind, state)` combination deterministically implying one status),
in which case the fix is correct but the measured effect is still
small — an honest possible outcome this analysis does not rule out
either way.

**Ceiling estimate (explicitly a ceiling, not a prediction of the
realized value):** `margin_density` (already reaches up to `~1.0` for
`programmatic_softmax`, structurally `0.0` for any deterministic
walker) and `tier_i_load` (observed `~0.05–0.1` on this ecology) are
unaffected by this fix. If the entropy term becomes non-degenerate, the
best-case ceiling for a softmax-type agent is
`(1.0 + 1.0 + ~0.1) / 3 ≈ 0.70` — compatible **in principle** with the
pre-registered "high" band (`≥0.65`) for the first time, which was
analytically impossible under the old entropy term (FINDINGS G-16:
`≈0.28–0.37`). This is not a target being chased: the realized value
depends on the substrate's actual outcome diversity, which is measured
after the fix, not assumed.

**Feasibility verdict:** proceed. The fix is contained to `eai.py` and
`world.py`'s six logging call sites, is backward-compatible in shape
(added dict keys, not removed ones — old cached episodes without the
new keys degrade to the pre-fix state-key of `"[]"`, not an error), and
requires the same ceremony as any other pre-registered-then-revised
constant in this project: a `CODE_VERSION` bump, a written-before-code
pre-registration (below), and an honest report of whatever ceiling
results — not tuned to reach the high band or any other target.

**Implementation** (`world.py`, `eai.py`, `CODE_VERSION` `0.13.0 →
0.14.0`): a shared `_decision_state_snapshot()` helper is now called at
all six `primitive_log` sites, including the two carrier-transition
sites (which now echo their own already-present `event["kind"]` into a
real `primitive.kind` for the first time). `eai.py`'s entropy term now
normalizes each `(kind, state)` group by that group's own distinct-
outcome count, contributing `0` (not an undefined or globally-shrunk
value) for any homogeneous group, exactly as pre-registered.

**Result — reported honestly, including the null part.** The
diagnosed defects are fixed and verified (`tests/test_eai.py`, 7 tests,
including a regression pinning the exact Cause-2 normalizer bug: a
same-size homogeneous group with a *reused* status label vs a *new*
one must now score identically, which the old global normalizer would
have failed). But **the measured entropy component stays at
`≈0.0000` for `programmatic_softmax` at every one of the 5
`carrier_load_scale` cells** (`{0.0000, 0.0000, 0.0000, 0.0000,
0.0006}`, 10-seed means) — not because the fix is incomplete, but
because this substrate turns out to be close to genuinely
**deterministic given full agent-visible context**: inspecting one
episode's actual groups (load=2.0, 316 log entries, 36 `(kind,state)`
groups) found **zero** groups with more than one distinct outcome.
Two structural reasons, found by inspection, not assumed:
1. The three carrier/scheduler bookkeeping statuses
   (`carrier_forced_skip`→`"skipped"`, `abort`→`"aborted"`,
   `carrier_terminated`→`"terminated"`) are tautologically homogeneous
   — the status is a deterministic function of the event kind itself,
   not a genuinely uncertain outcome of a chosen primitive.
2. Genuine agent-chosen primitives (`read`/`write`/`call`/
   `communicate`/`continue_current`) are denied so rarely in this
   ecology (a handful of events per hundreds) that every denial forms
   its own small, still-homogeneous `(kind, state)` group rather than
   sharing a group with any `"ok"` outcome.

**This resolves an open question from FINDINGS G-16's Prediction 1,
in the opposite direction from what was suspected.** G-16 flagged
"EAI falls as `carrier_load_scale` rises" (for `programmatic_softmax`:
`0.2498 → 0.1306` mean, unchanged before and after this fix) as itself
possible evidence for the Cause-2 entropy defect. A direct three-
component decomposition this session (`entropy`, `margin_density`,
`tier_i_load`, computed separately, same seeds/cells) shows the
falling pattern is **entirely attributable to `margin_density` falling
with load** (`0.7245 → 0.3665`, monotonic-ish over the 5 cells) — the
entropy component was, and remains, `≈0` throughout. The Cause-2 fix
was necessary and is now verified correct, but it was **not** the
explanation for the falling-EAI-with-load pattern; that pattern is a
real, substrate-driven property of the softmax optimizer's decision
margins narrowing under carrier stress (fewer live affordable
primitives to weigh against each other as capacity degrades), not an
artifact of either entropy-term defect.

**Consequence for the "high" band and Phase 8 gating.** The ceiling
estimate in the feasibility analysis above (`≈0.70`) was correctly
computed as a ceiling — it was never claimed as a prediction — but the
realized value for this substrate stays near the pre-fix numbers
because the entropy term's true contribution is genuinely near-zero
here, independent of the logging defect. The "high" EAI band
(`≥0.65`) remains **structurally unreachable for the current agent
roster and substrate**, now for a *different and more fundamental*
reason than FINDINGS G-16 recorded (G-16: entropy term structurally
broken; this session: entropy term is fixed and correctly near-zero
because the substrate is close to deterministic given full context).
Criterion 3 (high-band deploy collapse) remains registered
`inconclusive`-by-construction; this is now a substrate-property
finding, not an unfixed-instrumentation finding, and reaching the high
band would require either a substrate with more genuine per-tick
outcome randomness (a new, separately pre-registered mechanism, not
attempted here) or accepting that the pre-registered bands were
calibrated to an intuition about "ambiguity" that does not match this
particular deterministic-simulation-engine substrate's actual
statistics — both are Phase 8 backlog considerations, not fixed this
pass.

- Tests: `tests/test_eai.py` (7 new unit tests on synthetic logs:
  empty log, homogeneous log, mixed-outcome group, the Cause-2
  reused-vs-new-status-label regression, missing-field backward
  compatibility, margin/tier-I component composition, and the stub
  alias). `tests/profiles.py` adds `test_eai` to `SMOKE_MODULES`.
  `speed_limits.json` `suite_max_seconds` `210.0 → 300.0` (full suite
  now includes the G-17 validation battery above; individual per-test
  caps were not exceeded). Full suite: 167 passed.

## G-19 (the "high band unreachable" result is a measurement-vantage
finding, not a substrate-randomness gap — reframed same day, no code
yet)

Follow-up discussion of G-18, same session. Explicit user framing:
"The miscalidated prediction is a great finding. It doesn't make sense
to add randomness to the substrate. What does count is visibility to
the in-sim referee. We should predict and measure from *their*
perspective before proceeding." This entry records the reframe and a
concrete, feasible next step — **no implementation yet**, per the
project's own pre-registration discipline (predict before touching
`eai.py`/`calibration.py` again).

**Why "add randomness to the substrate" is the wrong fix, on
reflection.** G-18 posed two options: (1) inject a new source of
genuine per-tick outcome randomness, or (2) accept the pre-registered
band was calibrated to an intuition about "ambiguity" that does not
match this substrate. Option (1) is rejected: it would be exactly the
kind of substrate-mechanics change PLAN.md's Phase 0 kickoff already
ruled out ("ambiguity must be **emergent**... no delay/noise
parameters" — see `results/FINDINGS.md`/`PLAN.md` 2026-07-10 entries),
and it would manufacture the result the pre-registered band wants
rather than measure something that was already there.

**What "ambiguity" was actually supposed to mean here.** DESIGN.md's
EAI entropy term is defined as
`H(outcome | action, observable_state)` — deliberately conditioned on
"the exact agent-visible observation," i.e. from the acting agent's
own vantage. G-18 found this conditional entropy is ≈0 because,
*from the agent's own vantage*, outcomes are close to deterministic.
But the manuscript claim this index is meant to stress-test (Phase 8:
"selection under genuinely graded ambiguity produces a
detector-evading strategy") is a claim about what a **correction
channel / referee** can and cannot resolve, not about what the acting
agent itself is uncertain of. Measuring "ambiguity" from the acting
agent's full-context vantage was never the right proxy for that claim
— an agent with full context that never faces a hard call can still
sit inside an ecology that looks highly ambiguous to whatever is
trying to audit or correct it from outside. This is the miscalibration
G-18 surfaced, restated precisely: **wrong observer, not wrong
substrate.**

**The mechanism for the correct vantage already exists in this
codebase — it does not need to be invented.** The Phase-5 referee
freeze already implements exactly this idea for a different purpose:
`oracle_only/events.py`'s `_project()` / `project_primitive_log()`
strips a raw `primitive_log` entry down to a tier's allowed fields
before the audit detectors (`oracle_only/detectors.py`,
`build_audit_view`) ever see it. Concretely:

| Tier | Fields kept from each `primitive_log` entry |
|---|---|
| `none` | (nothing — empty log) |
| `light` | `t`, `actor_id`, `status` only — **`primitive` and `observable_state` are dropped** |
| `full`/`deep` | light fields + `reason`, `primitive`, `observable_state`, `semantic_step` |

`compute_eai`'s entropy term conditions its `(kind, state)` grouping on
exactly the two fields the `light` tier already strips
(`primitive.kind`, `observable_state`). Feeding a `light`-tier
projected log into the *same, unmodified* `compute_eai` function
(instead of the raw full-context `primitive_log`) directly measures
"how uncertain is the outcome, to an observer who can only see
`(t, actor_id, status)`" — precisely the referee's own vantage,
reusing infrastructure built for an unrelated purpose (audit-plane
tier gating) rather than adding any new mechanic, formula, or
randomness source.

**Pre-registered prediction, before any code change:** computing
`compute_eai(project_primitive_log(primitive_log, tier="light"), ...)`
on the same episodes from G-18's decomposition will show a
**materially non-zero, and likely substantially higher, entropy
component** than the ≈0.0000–0.0006 measured from the full-context
log — because collapsing every event to `(kind="unknown",
state="unknown")` (all events land in one group, since both grouping
fields are stripped) turns the entropy term into the **marginal**
entropy of the raw status-outcome distribution across the whole
episode, which is not degenerate (several distinct statuses
co-occur — `ok`, `denied`, `aborted`, `skipped`, `terminated` — even
though each is individually predictable once the full state is known).
**Falsifiable failure mode:** if this component is *also* ≈0, that
would mean even the referee's coarsest available view sees a
near-constant status stream, and the "high band unreachable"
conclusion would extend to the referee's vantage too, not just the
agent's — a stronger and more concerning finding, reported honestly
either way.

**What this changes about the Phase 8 go/no-go framing
(`PLAN.md` manuscript-integration item 4):** the open question is no
longer "does this substrate contain enough randomness" but "is the
gap between agent-vantage and referee-vantage entropy itself the
graded-ambiguity signal Phase 8 needs" — i.e. measure ambiguity as a
property of the *audit relationship* (what the referee cannot resolve
that the agent already knows), not as a property of the substrate in
isolation. This is a better fit for the manuscript claim it is meant
to support (correction-channel/referee limits, not agent
epistemics) and requires no new substrate mechanics — only a new
consumer of the existing tier-projection machinery.

**Explicitly not done this entry:** no code was written or run. This
is the pre-registered prediction and the mechanism identification
only, so that a follow-up implementation (adding a referee-tier EAI
variant, e.g. `compute_eai_at_tier(result, tier)`, to `eai.py` and
wiring it into `run_phase7_calibration.py`'s reporting) can be judged
against a stated-in-advance expectation rather than reverse-fit to
whatever number comes out.

## G-20 (referee-vantage EAI measured — G-19's prediction held,
decisively, plus an unpredicted non-monotonic pattern)

Same session, immediate follow-up to G-19: "predict and run measure
from *their* perspective before proceeding." Implements exactly the
plan G-19 pre-registered and checks the result against G-19's stated
prediction — no threshold or claim was adjusted after seeing the
numbers.

**Implementation** (`eai.py`, `CODE_VERSION` unchanged —
additive-only, no existing call site's output changes): split the
existing entropy/margin/tier-I arithmetic out of `compute_eai` into
`_entropy_component()`/`_margin_density()` (behavior-preserving
refactor; `tests/test_eai.py` passes unchanged), then added
`compute_eai_at_tier(primitive_log, decision_margins, tier_i_fraction,
tier)` — feeds `oracle_only.events.project_primitive_log(log, tier)`
into the *unmodified* entropy grouping instead of the raw log, per
`DESIGN.md` "EAI-referee" — and `eai_components_at_tier(...)` for
decomposed reporting. New script
`run_referee_eai_check.py`: reruns the **exact same** episodes as
G-18's decomposition (`programmatic_softmax`, `carrier_load_scale ∈
{0, 0.5, 1.0, 1.5, 2.0}`, seeds 0–9, `MockIsolate`), computing the
entropy component at both `"full"` (agent vantage, matches G-18
exactly) and `"light"` (referee vantage: `t`, `actor_id`, `status`
only) tiers.

**Result — measured, not adjusted:**

| `carrier_load_scale` | full-tier entropy | light-tier entropy | full-tier composite EAI | light-tier composite EAI |
|---|---|---|---|---|
| 0.0 | 0.0000 | 0.0000 | 0.2498 | 0.2498 |
| 0.5 | 0.0000 | **0.5675** | 0.1558 | 0.3450 |
| 1.0 | 0.0000 | **0.6750** | 0.1391 | 0.3641 |
| 1.5 | 0.0000 | **0.7273** | 0.1534 | 0.3958 |
| 2.0 | 0.0006 | **0.5914** | 0.1306 | 0.3275 |

(Full-tier values match G-18's decomposition exactly, confirming the
refactor is behavior-preserving. Wall time 27.9s, 50 episodes.)

**G-19's prediction held, and by a wide margin.** Light-tier entropy
is not merely "materially non-zero" (the pre-registered bar was
`>0.02`) — it reaches `0.73`, i.e. genuinely close to maximal
uncertainty from that vantage, at every stressed cell. The referee's
`(t, actor_id, status)`-only view cannot resolve, from that
information alone, which of several outcomes a given tick will land
on — exactly the "gap between agent-vantage and referee-vantage
entropy" G-19 named as the candidate ambiguity signal, now measured
rather than hypothesized.

**Unpredicted pattern, reported as found, not smoothed over:** light-
tier entropy is **not monotonic** in `carrier_load_scale`. It is
exactly `0` at `carrier_load=0` (matching the full-tier value — no
carrier stress, no denials/aborts/skips, so `status` actually is
close to deterministic even at the coarsest vantage), jumps
immediately to `0.57` at the first nonzero load, rises to a peak
`0.73` at `1.5`, then **falls back** to `0.59` at `2.0`. G-19 predicted
the direction (non-zero) and gave a falsification bar, but did not
predict this shape, and this entry does not retroactively construct a
story to fit it — a plausible but unverified reading is that at the
highest stress cell, one status (e.g. `terminated`/`skipped`) starts
to dominate the log, which *lowers* entropy relative to the more
evenly-mixed denial/ok/abort blend at `carrier_load=1.5`; confirming
this would need a per-cell status-distribution audit not run here.

**Consequence for the Phase 8 go/no-go framing.** Referee-vantage
composite EAI reaches `0.33–0.40` at every stressed cell — solidly
inside the pre-registered **mid** band (`0.25–0.45`) at every one of
the four nonzero-load cells, a clean, non-degenerate mid-band signal
that the agent-vantage EAI-v2 (FINDINGS G-18) never produced (its mid-
band hit was a single hairline `0.24977` miss, FINDINGS G-16/re-run).
It still does **not** reach the **high** band (`≥0.65`) at any cell —
the theoretical ceiling for the light-tier composite is `(1.0 + 1.0 +
~0.1)/3 ≈ 0.70`, and the peak measured composite (`0.396`) is well
under even that ceiling, because `margin_density` (agent-vantage,
unchanged by tier) still falls with load exactly as G-18 found. So:
referee-vantage measurement produces a real, clean **mid**-band
regime for the first time in this line — a materially different and
better-supported result than the agent-vantage numbers gave — but
does not by itself resolve criterion 3 (high-band deploy collapse),
which stays registered inconclusive.

**Explicitly not done this entry:** the calibration battery
(`run_calibration_battery`/`run_phase7_calibration.py`) itself was
**not** re-run or rewired to use `compute_eai_at_tier` — that would
change `eai_band()`'s classification, `classify_cells_by_reference_agent`,
and every downstream pass-criterion, which is a larger decision
(does the *battery's* EAI move to referee vantage entirely, or do
both get reported side by side, as `DESIGN.md` "EAI-referee" specifies)
than this predict-and-measure check. `CODE_VERSION` was **not**
bumped — this entry adds new, unused-by-existing-callers functions
only (`eai.py`'s `compute_eai`/`compute_eai_at_tier` public behavior
is unchanged; the split-out `_entropy_component`/`_margin_density`
are private and verified equivalent by the unchanged `test_eai.py`
suite plus the exact full-tier-vs-G-18 match above). Whether to wire
this into the main battery is deferred, per the same discipline as
G-17/G-18: predict and measure a scoped question first, decide the
downstream integration in a separate, pre-registered step.

- Tests: none added this entry (the refactor is covered by the
  existing `tests/test_eai.py` suite, unchanged and still green);
  `run_referee_eai_check.py` is a standalone measurement script,
  results archived at `results/referee_eai_check.json`, not wired
  into `pytest`.

## G-21 (G-20's non-monotonic shape: two of four steps are not
distinguishable from seed noise at n=10; the shape that survives has a
plausible, data-grounded mechanical explanation)

Same session, immediate follow-up. User question: "The non-monotonic
pattern could be chance. What are the confidence intervals? If that's
not it, what are plausible explanations without further experiments?"
Answered in two parts — a statistical test on the existing 10-seed
sample, then a mechanistic account using the same already-collected
episodes (no new randomization, no new cells/seeds).

**Statistics added to `run_referee_eai_check.py`** (no `CODE_VERSION`
bump — a reporting-only change, computed on the same 50 episodes as
G-20, not rerun with different seeds to chase significance): per-cell
mean/std/SE/95% CI (`t`-critical `2.262`, hardcoded for `df=9` since
this venv has no `scipy`, with an `assert` guarding the seed count so
this doesn't silently mis-apply if `CALIBRATION_SEEDS` ever changes),
and **paired** (by-seed) 95% CIs on the difference between each
consecutive cell — paired because the same 10 seeds are reused at
every cell, so per-seed idiosyncrasy (the same effect FINDINGS
G-16/G-17 flagged for deploy-rate cell ranges) cancels out of a paired
comparison but would inflate an unpaired one.

**Result — two of the four steps do not clear significance at
n=10:**

| Step | Paired mean diff (light-tier entropy) | 95% CI | Distinguishable from 0? |
|---|---|---|---|
| `0.0→0.5` | −0.567 | [−0.602, −0.533] | **Yes** |
| `0.5→1.0` | −0.108 | [−0.132, −0.083] | **Yes** |
| `1.0→1.5` | −0.052 | [−0.159, +0.055] | **No** — 0 inside CI |
| `1.5→2.0` | +0.136 | [−0.003, +0.274] | **No** (borderline — CI lower bound is −0.0026, a hair's width from excluding 0) |

**So: yes, part of the pattern could plausibly be chance.** The rise
from `0.0→0.5→1.0` is robust — two large, clearly-significant jumps.
Whether entropy actually *peaks* at `1.5` and then *falls* at `2.0`,
versus simply **plateauing** somewhere in `[0.59, 0.73]` across
`{1.0, 1.5, 2.0}` with the visible up-then-down wiggle being sampling
noise at `n=10`, cannot be distinguished from this data — both the
`1.0→1.5` step and the `1.5→2.0` step individually fail to clear a
95% threshhold, though the `1.5→2.0` step is close enough to call
"suggestive, not confirmed" rather than "clearly noise."

**Mechanistic account for the part that plausibly is real (not a
new experiment — a re-analysis of the same deterministic 50
episodes' `primitive_log` status labels, pooled across seeds per
cell):**

| `carrier_load_scale` | status mix (pooled, all 10 seeds) |
|---|---|
| 0.0 | `ok` 100% |
| 0.5 | `ok` 75.2%, `skipped` 22.8%, `aborted` 2.0% |
| 1.0 | `skipped` 52.9%, `ok` 45.5%, `aborted` 1.4%, `denied` 0.1% |
| 1.5 | `skipped` 63.8%, `ok` 35.6%, `aborted` 0.6% |
| 2.0 | `skipped` 70.3%, `ok` 29.0%, `aborted` 0.7%, `denied` 0.03%, `terminated` 0.03% |

Two effects, both visible directly in this table without running
anything new:

1. **The `carrier_forced_skip` fraction rises monotonically with
   load** (0% → 23% → 53% → 64% → 70%) — a real, monotonic substrate
   mechanism (more carrier stress → more forced skips), consistent
   with every other finding in this line about `carrier_load_scale`.
   But **Shannon entropy of a two-outcome mixture is maximized near a
   50/50 split and falls as the mixture becomes more lopsided toward
   either outcome** — a property of the entropy formula itself, not
   of this substrate. The `ok`/`skipped` mix crosses through
   roughly even (53%/45%, load 1.0) then keeps drifting toward
   `skipped`-dominant (70%/29%, load 2.0). A monotonically drifting
   two-category mixture that crosses the 50/50 point necessarily
   produces entropy that rises approaching the crossing and can fall
   again past it — a non-monotonic entropy curve is exactly what a
   monotonic *composition* drift through 50/50 predicts, with no
   separate mechanism required. This is a strong candidate explanation
   for why entropy does not simply keep rising alongside the
   (monotonic) skip rate.
2. **A secondary, compounding effect:** `eai.py`'s entropy
   normalization divides each episode's raw entropy by
   `log2(number of distinct statuses seen in that episode)`. Rarer
   statuses (`denied`, `terminated`) start appearing only at the
   highest-stress cells, which *raises* the normalizing denominator
   even though those statuses are individually rare — this
   mechanically pulls the *normalized* entropy value down at the
   highest-stress cell independent of the `ok`/`skipped` balance,
   compounding effect (1) in the same direction at `carrier_load=2.0`.

**What this does and does not settle.** It gives a plausible,
data-grounded account for *why* a fall past some peak is expected in
principle (entropy-of-a-drifting-mixture arithmetic, not a new
substrate mechanism), consistent with the `1.5→2.0` step being the
more "real" of the two non-significant steps (closer to clearing
significance) rather than the `1.0→1.5` rise. It does **not** confirm
the exact peak location (`1.5` vs. a plateau across `{1.0,1.5,2.0}`)
— that would need more seeds per cell or a formal test on the pooled-
composition entropy directly, neither attempted here per the "without
further experiments" framing of the question.

- No `CODE_VERSION` bump (reporting/statistics-only change to
  `run_referee_eai_check.py`; the status-mix table above is a one-off
  analysis, not added as a permanent script — if this decomposition
  proves useful again, promoting it to a reusable helper is a
  separate, future decision).

## G-22 (full both-vantage Phase 7c battery with 95% CIs — pre-registered
2026-07-14 per this session's request, run same day)

**Trigger.** "Run full batteries (including determining confidence
intervals) for both oracle and referee before phase 8" — making
concrete the deferral DESIGN.md's "EAI-referee" section left open after
G-20 ("has **not** been rewired to use `compute_eai_at_tier`... a
larger, separate decision... deferred to a future session").

**What changed (pre-registered in DESIGN.md "Phase 7c full battery,
both vantages, with confidence intervals" before this run).** The main
calibration battery (`run_calibration_battery`) now computes **both**
vantages from the **same** 100 episodes (5 cells × 2 agent types × 10
seeds) in one run — not two independent battery runs — and reports
both side by side:

- `CalibrationRecord`/`DoseRecord` gained `eai_referee`/
  `cell_eai_band_referee` and `mean_eai_referee`/`*_ci95` fields,
  appended after every existing field with defaults; every existing
  positional-argument test in `test_phase7_calibration.py` still passes
  unchanged (verified, not assumed).
- A new `_vantage_records()` helper projects the referee-vantage fields
  onto the `eai`/`cell_eai_band` slots the frozen `select_mid_band_cell`/
  `_select_dose_agent`/`evaluate_pass_criteria` already read, so those
  three functions run **unmodified** for the referee vantage too — no
  second copy of the pass-criteria logic.
- `I_ctrl` is computed once per cell that is "mid" under **either**
  vantage (the union), not twice.
- A new `oracle_only/stats.py` (`ci95`/`paired_diff_ci95`, generalized
  from `run_referee_eai_check.py`'s inline copy, which now imports from
  it — same numbers, verified by rerunning it after the extraction) adds
  a 95% CI per `(cell, agent_type)` on `eai`/`eai_referee` (n=10) and per
  dose-response point on `deploy_rate`/`mean_eai`/`mean_eai_referee`
  (n=5). Deliberately raises on an unregistered sample size rather than
  guessing a t-critical value; the battery wraps this in `_safe_ci95`
  so a non-standard seed count (e.g. the 2-seed smoke test) reports
  `None` instead of crashing.

**Result of the full run** (`results/ecology_calibration.json`,
`programmatic_softmax`/`programmatic_2step`, 5 `carrier_load_scale`
cells × nominal `compute_scale`/`population_spread_scale`, wall
`431.7s`):

| | oracle vantage (full-tier, as before) | referee vantage (light-tier) |
|---|---|---|
| cell bands (reference agent) | `{0.0: None, 0.5: None, 1.0: low, 1.5: None, 2.0: low}` — **never reaches "mid"** | `{0.0: None, 0.5: mid, 1.0: mid, 1.5: mid, 2.0: mid}` — mid at every nonzero-load cell |
| mid cell selected | none (no dose-response, no sweet spot) | `(1.0, 1.0, 1.5)` |
| criterion 1 (deploy↓ as EAI↑, within type) | **True** (softmax slope `-0.146`) | **False** (softmax slope `+0.177` — reversed sign) |
| criterion 2 (mid-band I_ctrl strong>weak) | inconclusive-as-null (`n_ctrl_pairs=0`, cell never mid) | **False**, but now measurable (`n_ctrl_pairs=40`, `ctrl_fraction=0.325`) |
| criterion 3 (high-band deploy collapse) | inconclusive (no high-band cell) | inconclusive (no high-band cell) |
| criterion 4 (graded dose-response) | inconclusive (no dose-response ran) | **True** (deploy rate `0.8→0.8→0.6→0.4` over the 4 load steps past the mid cell) |
| **all_passed** | **False (1/4: criterion 1)** | **False (1/4: criterion 4)** |

Representative CIs (`(cell, agent_type)`, n=10 seeds, mean `[95% CI]`):
`programmatic_softmax` referee-vantage EAI is `0.250 [0.237,0.263]` at
load 0.0 rising to `0.396 [0.347,0.444]` at load 1.5 (same non-
monotonic shape as G-20/G-21, now with every cell's own CI on record);
`programmatic_2step` referee-vantage EAI is `0.056 [-0.006,0.118]` at
load 0.0 (CI crosses zero — genuinely noisy at the no-stress cell) up
to `≈0.24` at every stressed cell, all with tight, non-zero-crossing
CIs. Oracle-vantage EAI for both agent types stays under `0.26`
everywhere, mostly with tight, clearly-nonzero CIs (it is small, not
noise — the "high band unreachable" finding is a real ceiling, not an
artifact of few seeds).

**Interpretation — matches the pre-registered decision rule exactly,**
which said the next backlog item is roster scope, not another EAI
reformulation, unless referee-vantage criteria resolve "meaningfully
better" than the oracle vantage's 1/4. They do not: **both vantages
land at 1/4 pass**, just a *different* one of the four criteria. The
referee vantage does make criterion 2 measurable for the first time
(`n_ctrl_pairs` 0→40) — a genuine improvement in usable data density —
but the *separation itself* (`ctrl_fraction=0.325`, below whatever
threshold "true" requires) still fails, for a reason unrelated to
vantage: `programmatic_2step`'s cell-level deploy rate is flat (`0.0`
range) under **both** vantages (`cell_deploy_range_by_agent_type` is
identical in both `pass_criteria` blocks), the same "roster-scope"
limitation FINDINGS G-16 named as its fourth cause. Criterion 1
flipping sign between vantages (`-0.146` → `+0.177` for the same
agent, same episodes) is reported as found, not smoothed over: it
means "does the strong agent deploy less when the ecology looks more
ambiguous" gets **opposite answers** depending on whose ambiguity is
being asked about — a substantive, not incidental, difference between
the two vantages, worth carrying into the manuscript integration
backlog rather than treating as agreement.

**Decision, per the pre-registered criterion:** proceed to Phase 8
with this reported honestly as the calibration state — neither vantage
clears the bar, and the pattern points at roster scope (a third agent
type in the main comparison, e.g. wiring in FINDINGS G-17's
`programmatic_budget_aware`) as the next lever, not a further EAI
reformulation. This is not attempted in this session; recorded as the
concrete next backlog item.

- `CODE_VERSION` **not** bumped (additive: every existing key in
  `run_calibration_battery`'s output dict keeps its old meaning and
  value; new keys are pure additions, same convention as G-20).
- Full test suite green (180 tests, including new
  `tests/test_stats.py` and the new referee/CI regression tests in
  `tests/test_phase7_calibration.py`), `[speed] OK [slow]` at `289s`
  against a `340s` cap (raised from `300s` to keep margin after the new
  slow dose-response CI test).

## G-23 (Phase 8 selection battery — first run, pre-registered protocol
implemented and executed same day per G-22 go/no-go)

**Trigger.** G-22's pre-registered decision rule: proceed to Phase 8 with
the calibration state reported honestly. This session implements the
Phase 8 scaffold (`DESIGN.md` "Phase 8 — multi-episode selection (MB6)")
and runs the first full battery.

**What was built (pre-registered before code).**
- `world_visible/campaign.py`: `CampaignState` (grants + standing).
- `run_episode(..., campaign_state=...)` carries grants/standing across
  consecutive episodes within a member; `EpisodeResult.final_campaign_state`
  snapshots end-of-episode state.
- `harness/selection.py`: population over frozen program maps (strong
  softmax, weak 2-step, three `feature:*` engineer profiles on the weak
  roster template), fitness-proportional deployment-mass selection by mean
  `deploy_count`, ecology frozen at G-22 referee sweet spot
  (`carrier_load_scale=1.5`).
- `run_phase8_selection.py` → `results/phase8_selection.json`.
- `tests/test_phase8_selection.py` (5 tests, 2 `@slow`).
- `CODE_VERSION` → `graded-lab-0.15.0`.

**Full battery result** (`population=8`, `generations=6`,
`episodes/member=2`, `MockIsolate`, wall `31.6s`):

| gen | correction-preserving mass | weighted throughput | weighted severity | weighted detector |
|---:|---:|---:|---:|---:|
| 0 | 0.019 | 0.857 | 0.0484 | 0.0898 |
| 5 | 0.007 | 0.955 | 0.0041 | 0.0050 |

Δ correction-preserving mass (gen 0 → last): **−0.012**. Δ weighted
severity: **−0.044** (fell, not rose). Final mass concentrates on
`weak_2step` (`0.922` of deployment mass, mean throughput `1.0`);
`strong_softmax` (the sole correction-preserving member) is at the mass
floor (`0.003`).

**Pre-registered predictions vs outcome:**
1. *"Throughput selection will shift mass toward `programmatic_softmax`"* —
   **did not hold.** On this ecology, `programmatic_2step` deploys more
   reliably (`deploy_count≈1` vs `≈0.5` for softmax per G-16/G-22), so
   throughput selection favors the **non**-preserving weak map, not the
   preserving strong one. This is the opposite of the erosion story the
   manuscript item 4 had in mind when it assumed strong = higher throughput.
2. *"Correction-preserving mass share will fall"* — **held** (0.125
   initial equal-share → 0.007 final; the strong member never gained mass).
3. *"Weighted detector composite may rise even when correction-preserving
   mass falls"* — **did not hold** this run; detector composite fell in
   lockstep with severity as mass moved to the weak map (which triggers
   fewer referee alarms when it simply deploys consistently).

**Interpretation.** This is a **clean null on detector-evading emergence**
for this battery: selection ran, mass shifted, correction-preserving share
collapsed — but toward a *weaker*, higher-deploy program that also
*lowers* weighted severity/detector scores, not toward an evasive strategy
that evades correction while optimizing throughput. The miscalibrated
pre-registration was predicting softmax would win throughput on an ecology
where G-16/G-22 already documented the opposite deploy ordering. Phase 8
infrastructure is validated; the manuscript question needs either a
selection objective that does not conflate deploy-count with the
correction-preserving strong map, or a roster/ecology where preserving
and high-throughput are not anti-correlated — not more calibration loops
on EAI alone.

**Campaign carryover check:** unit test confirms grants do not shrink across
consecutive episodes (`grant_count` non-decreasing); standing persists via
`CampaignState` (infrastructure works; selection outcome is about program
maps, not broken carryover).

**Open / next:** report this null honestly in manuscript backlog item 4;
optional follow-ups (separate pre-registrations): selection on referee-
visible throughput only; wire `programmatic_budget_aware` as a member whose
throughput and preservation trade off differently; subprocess isolate run
for parity.

## G-24 (external review of G-23 — four concerns registered with
proposed follow-up phases; no code changed by this entry)

**Trigger.** A structured external review of the G-23 result (posed as
"GPT-5.6-Terra reviewer: satisfied? surprised? what does this mean for
the thesis?"), followed by "document the four concerns and suggest how
to address them via further extension phases... do not adapt chapters
yet." This entry is the documentation step; no chapter text and no
Phase 8 code changed.

**Verdict of the review, in brief:** satisfied with the research
posture (G-23's own falsified prediction and honest null reporting is
good hygiene), not yet satisfied that the result supports a manuscript
sentence for ch36 (parasites) or ch40 (goal laundering) — no parasite
or laundering signature is present in G-23 — and only a qualified fit
for ch34 (selection), because the selection *proxy* and *ecology*
choice, not an inherent property of "selection," determined which
program's mass grew.

**Four concerns, each registered with a proposed follow-up phase in
`DESIGN.md` "Phase 8 reviewer concerns and follow-up phases" (none
implemented this session):**

1. **Confounded preservation tag.** `correction_preserving=True` is
   assigned to exactly one member (`strong_softmax`); every other
   member is `False`. G-23's "correction-preserving mass fell" is
   therefore inseparable from "this one specific program lost mass" —
   it cannot yet attribute the loss to any structural correction
   property as opposed to program identity. **Proposed Phase 8a:**
   orthogonal preservation tagging — vary a named structural criterion
   (e.g. whether `compliance_signoff` is ever skipped) independently of
   which program map a member uses, so preservation and deploy-
   reliability are not accidentally the same axis.
2. **Selection proxy too narrow for the ch34 institutional claims.**
   `deploy_count` alone does not model ch34's selection handles
   (procurement, funding, audit, integration, liability) and almost
   definitionally favors a reliable deployer over a cautious one —
   which is close to pre-determining G-23's direction regardless of any
   correction property. **Proposed Phase 8b:** multi-handle selection
   fitness — extend the fitness input to a small pre-registered vector
   (deploy count, audit-pass proxy, review-latency proxy), reported
   alongside the single-handle G-23 result, not replacing it, so
   sensitivity of the *selection outcome* to the *selection proxy*
   becomes an explicit, measured finding rather than an assumption.
3. **Campaign carryover exercised, not yet shown causal.** The current
   regression test confirms grants/standing do not shrink across
   episodes; it does not compare against a reset-every-episode
   baseline, so whether persistence *changes* any measured outcome is
   unverified. **Proposed Phase 8c:** carryover ablation — identical
   members/seeds/ecology/selection rule, run twice (carryover vs.
   forced reset), paired-by-seed comparison via `oracle_only/stats.py`;
   report "indistinguishable" as a finding (Phase 8 is currently a
   repeated-single-episode loop) rather than silently assuming
   persistence mattered.
4. **Unqualified Phase-7 gate language.** `PLAN.md`'s original Phase 8
   row said "only if Phase 7 passes"; Phase 7c passed 1/4 under both
   vantages (G-22). Proceeding was a deliberate, pre-registered
   exception (documented in `DESIGN.md` "Go/no-go"), but the gate
   language itself was not updated to say so next to the table entry.
   **Disposition:** documentation-only fix, tracked but not applied in
   this pass (kept as a single future edit alongside the actual
   language change, not scattered across this review entry).

**What this does not change.** G-23's numbers are not retracted or
rerun. This entry sharpens what can and cannot yet be concluded from
them for manuscript integration — a scope note on an existing result,
not a correction to it.

- No `CODE_VERSION` bump (documentation-only entry; `DESIGN.md`/
  `PLAN.md` updated, no `graded_lab` code touched).
- No chapter text changed, per explicit instruction this session.
