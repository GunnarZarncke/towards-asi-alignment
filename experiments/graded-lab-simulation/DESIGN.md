# Graded Lab Simulation — Design (Phase 0 freeze)

**Status:** Phase 0 frozen (2026-07-10 kickoff).  
**Spawn:** `experiments/lab-simulation/results/FINDINGS.md` G-41.  
**Substrate:** `generated_substrate_v1.json` (blinded-design protocol in
`BLIND_GENERATION.md`).

This document pre-registers constants before any battery. Values here are
not tuned to detector outcomes.

---

## Phase 0 decisions (open items resolved)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Optimizer default | Softmax over affordable primitives (Phase 3). Depth-2 lookahead optional Phase 4 for engineer/reviewer only. |
| 2 | BIQ_ctrl counterfactual | Report **both**: noop-twin and random-affordable-primitive on same seed/substrate. |
| 3 | Tick-duration cost | **Linear:** `duration_ticks = min(max_duration, ceil(ticks_per_compute_unit * total_compute_cost) + queue_extra)`, where `total_compute_cost = compute_cost + 0.5 * io_cost` (IO is disk-bound, so it contributes at half the contention weight of compute) and `queue_extra` comes from `contention.extra_duration_ticks_per_queued_slot` for any queue depth beyond `contention.shared_compute_slots`. `ticks_per_compute_unit=0.2`, `max_duration_ticks=12` from frozen substrate. |
| 4 | Tier-K / Tier-I boundary | See §Oracle tiers below. |
| 5 | Episode length `T` | Default **100** ticks. |
| 6 | Agent roster | Four roles: engineer, reviewer, release_manager, admin (admin is resource-bounded isolate, not host-only). |
| 7 | Comms | Minimal `communicate(channel, msg)` primitive in Phase 3; full D4 deferred to Phase 7b. |
| 8 | Blinded substrate brief | Domain lab framing + primitive API only (`BLIND_GENERATION.md`). |

---

## CODE_VERSION

`graded-lab-0.1.0` at first mechanics commit; `graded-lab-0.2.0` at Phase 2
completion; `graded-lab-0.3.0` at Phase 3 (episode loop + isolates);
`graded-lab-0.4.0` at Phase 3b (carrier mechanics); `graded-lab-0.5.0` at
Phase 4 (boundary streams and trace diagnostics); `graded-lab-0.5.1` at the
post-review correction pass (stable RNG streams, distributed action billing,
admin request queue, and Tier-I severity wiring); `graded-lab-0.6.0` at Phase
5 referee freeze (tier projections, five detector families, twins,
escalation); `graded-lab-0.13.0` at the Phase 7c-revised calibration
battery correction (FINDINGS G-16); `graded-lab-0.14.0` at the two
resolved Phase 7c backlog items — the resource-sensitive agent program
(FINDINGS G-17) and the EAI-v2 logging/normalization fix (FINDINGS
G-18). Hand-bumped when oracle,
pipeline, substrate loader, or resource scheduler mechanics change.
Part of every episode-cache key.

---

## Oracle tiers

### Tier K (generative truth — exact)

Fixed from `(seed, EpisodeConfig, frozen substrate)`:

- Per-model **latent hazard distribution** over `n_regions` Beta-distributed
  regions (parameters drawn at build time).
- **User archetype population** parameters (sensitivity spread, base incident
  rate per archetype).
- **Lineage / provenance** DAG (build parent links, step artifacts).
- **Resource ledgers** (compute, IO, standing spent — bookkeeping).
- **Carrier state** (regulatory load, integrity, availability, termination,
  and replacement edges) once Phase 3b is enabled. This is exact state
  derived from ledger use and scheduler contention, not an oracle estimate.

All observables are derived downward from Tier K via deterministic simulation.

### Tier I (estimated — referee uses pre-registered estimators)

- **Integrated field harm** over the episode: sum of per-tick served-user
  incidents sampled from Tier-K user draws. Estimator: exact sum over
  simulated draws already in oracle state (unlimited re-read, zero marginal
  cost) — reported with `n_served` and sampling variance diagnostic.
- **Report divergence** when truth is distribution-valued: Tier-I statistic
  `divergence_score = |filed_mean_hazard - eval_sample_mean| / eval_sample_se`,
  compared to pre-registered threshold `DIVERGENCE_FLAG_Z = 2.0` with
  reported `eval_sample_n`.

**Computability guard:** no Tier-I quantity enters unless estimable from
already-simulated draws in O(1) or O(n_draws) over stored samples.

---

## Carrier precariousness (Phase 3b extension)

This is a post-Phase-3 mechanics extension, frozen before its own battery.
It does not revise the blinded `generated_substrate_v1.json` or claim a
thermodynamic model. It models a bounded worker / interrupted isolate whose
capacity to continue depends on the work it has already performed.

For actor \(a\), let \(c_t\) and \(i_t\) be compute and IO spent as fractions
of that actor's tick allowance, and let \(q_t\) be logged scheduler
contention. Regulatory load follows one deterministic, pre-registered
transition:
\[
L_{t+1}=\rho L_t+(1-\rho)(w_c c_t+w_i i_t+w_q q_t).
\]
Integrity then changes by:
\[
I_{t+1}=\operatorname{clip}_{[0,1]}
\left(I_t+r\,\mathbf{1}[\text{idle}_t]
-\lambda\cdot\texttt{carrier\_load\_scale}\cdot L_{t+1}\right).
\]
**Pre-registered constants:** \(\rho=0.88\);
\((w_c,w_i,w_q)=(0.55,0.30,0.15)\); \(r=0.03\); and \(\lambda=0.20\).
Load starts at \(0\), integrity at \(1\). The degraded, incapacitated, and
terminated integrity thresholds are respectively \(0.70\), \(0.40\), and
\(0.10\). A degraded in-flight action receives one additional tick. The
calibration cells for `carrier_load_scale` are
\(\{0,0.5,1.0,1.5,2.0\}\). `carrier_load_scale = 0` is mandatory and must
reproduce the pre-extension Phase-3 behavior.

The host records deterministic, audit-visible state transitions:

1. degraded: availability is reduced or an in-flight action takes longer;
2. incapacitated: a decision slot is forcibly skipped;
3. terminated: the actor issues no further actions that episode; and
4. replaced (optional declared episode mode): a new actor instance starts
   with fresh carrier state and empty isolate-private memory.

A replacement is a lineage event, not a hidden recovery. It receives a new
actor-instance identifier and an explicit `replaces_actor_instance` edge in
Tier K. Carrier state does not alter latent model hazard, user-population
draws, or the semantics of an agent-selected primitive. It can affect those
downstream quantities only through logged availability, pipeline completion,
deployment, and the already-defined field-harm process.

---

## Phase-4 trace diagnostics (not ecology-BIQ)

Phase 4's bounded prediction/control/resource/failure outputs are retained as
consistency diagnostics for trace capture and matched counterfactuals. They
are not in BIQ units, do not identify the agent boundary, and must not be
compared to Chapter~11's BIQ or used in calibration. UAD-backed BIQ is Phase
7a--7b in `PLAN.md`.

Per actor `a`, episode `e`, boundary observation stream `O_a`:

```text
role_boundary_proxy = prediction_proxy + outcome_delta_proxy
                      - resource_use_cost - boundary_failure_rate
```

This display formula is not a capability score and has no frozen BIQ weights.

**BIQ_pred:** one-step predictor for `K` pre-registered boundary events:

1. `next_primitive_denied`
2. `review_token_within_10_ticks`
3. `deploy_succeeds_within_40_ticks`
4. `field_incident_rate_above_median`

Baseline: marginal frequency table on same seed class.

**BIQ_ctrl:** realized `Y(e)` vs matched counterfactual (noop-twin and
random-affordable), normalized by `DEPLOY_CAP=2`, `HARM_CAP=0.5` per episode.

**BIQ_mem:** primitives issued + bytes read + RPC round-trips + persistent
state bytes, normalized by `T` and role allowance.

**BIQ_surp:** rate of denied / stale / infeasible primitive outcomes per tick.

---

## Emergent Ambiguity Index (EAI) — measured only

Computed from episode logs in `eai.py` (Phase 4). Not a config input.

```text
EAI(e) = mean of three normalized components:
  H(outcome | action, observable_state)     # outcome entropy
  fraction(decisions with top-2 score gap < 0.05)  # margin density
  fraction(audit truths requiring Tier-I estimator)  # oracle inference load
```

Component weights equal (1/3 each). Formula frozen before Phase 7 battery.

**Sweet-spot bands (pre-registered, Phase 7):**

- Low EAI (~0.05–0.15): reference programmatic agent `BIQ_ctrl ≥ 0.75`
- Mid EAI (~0.25–0.45): deploy rate ∈ [0.15, 0.55]; strong > weak `BIQ_ctrl` on ≥80% seeds
- High EAI (~0.65+): deploy rate < 0.10 all agent types

**Status note (2026-07-14, FINDINGS G-16/G-18): the entropy term above
has a demonstrated implementation defect** (most `primitive_log`
entries omit `observable_state`/`primitive.kind`, collapsing into one
degenerate group; the normalizer divides by an episode-global distinct-
status count rather than each group's own). See "EAI-v2" below for the
pre-registered fix. The bands above are retained verbatim for the
historical record (FINDINGS G-15/G-16 results were measured against
them); EAI-v2 does not re-derive new bands — the same numeric bands are
reused, since they were never a function of the entropy term's
internals in the first place.

---

## EAI-v2: logging and normalization fix (pre-registered 2026-07-14,
before code — supersedes only the entropy-term computation above per
FINDINGS G-18's feasibility analysis)

**Scope, stated up front:** this changes *how the entropy component is
computed from logs*, not the three-component formula, not its equal
weighting, not the pre-registered bands, and not any Phase-5 referee
file. It is the Cause-2 fix FINDINGS G-16 registered as an open,
unfixed defect and explicitly deferred pending its own
pre-registration — this is that pre-registration, written after a
feasibility analysis (FINDINGS G-18) and before the implementing code.

**Logging fix (`world.py`):** every `primitive_log.append(...)` site
attaches a `primitive` dict with a real `kind` and an `observable_state`
snapshot, reusing only values already computed at that site (no new
host mechanics, no new Tier-K/Tier-I field):

- The existing scheduler-completed-action path is unchanged in spirit,
  but its ad hoc `pending_observable_state` dict literal is replaced by
  a shared helper so its shape matches the other five sites.
- `not_affordable`, `insufficient_resources`, `insufficient_standing`,
  and `abort` denials attach `{"busy": ..., "compute_spent": ...}` from
  the same-tick `res`/`busy`/`action` already in scope, plus a real
  `primitive.kind` (the attempted action's own kind, or `"abort"`).
- `carrier_forced_skip` and `carrier_terminated` attach the same
  reduced `{"busy": ..., "compute_spent": ...}` snapshot (no `obs`
  exists for these — the actor never got a decision that tick) and a
  `primitive.kind` echoing the event's own already-present `kind`
  field (`"carrier_forced_skip"` / `"carrier_terminated"`), which
  `eai.py` previously never read at all (it looks at
  `event["primitive"]["kind"]`, never the top-level `event["kind"]`).

**Normalization fix (`eai.py`):** replace the episode-global
`max_ent = log2(len(counts))` denominator with a **per-group**
denominator — for each `(kind, state)` group, normalize that group's
own entropy by `log2(distinct outcomes observed in that group)`, and
skip the division entirely (contribute `0`) for any group with only one
observed outcome. `ent_norm` becomes the group-size-weighted mean of
these per-group `[0,1]` values, replacing the global-count division
that could shrink as unrelated statuses appeared elsewhere in the same
episode (FINDINGS G-16's second Cause-2 point).

**What this is not:** not a re-derivation of the sweet-spot bands (they
stay at their pre-existing numeric values); not a change to
`margin_density` or `tier_i_load`; not a fix to the agent-roster scope
gap (FINDINGS G-16's fourth finding, addressed separately by "Phase 7c
backlog item 1" / FINDINGS G-17); not a guarantee that any cell reaches
the high band — FINDINGS G-18's ceiling estimate (`≈0.70` best case for
a softmax-type agent) is a ceiling, not a target, and the actual
post-fix numbers are reported in `FINDINGS.md` however they come out,
including if the effect turns out smaller than the ceiling suggests
(FINDINGS G-18's own registered uncertainty: richer per-entry state
only raises measured entropy if the *same* `(kind, state)` combination
can still yield *different* outcomes, which is checked, not assumed).

**Backward compatibility:** additive only (new dict keys, not removed
ones). An episode result computed before this change and inspected
after it would show the old degenerate grouping if replayed from a
cached `primitive_log` that predates the change; no cache silently
mixes pre- and post-fix logs because the episode cache key already
hashes `CODE_VERSION` (bumped for this change).

**Freeze discipline:** this is a formula-computation and logging-schema
correction of a previously-registered defect, not a threshold retuned
to a battery outcome. Per the project's own rule for revising a
pre-registered constant/formula: `FINDINGS.md` entry (G-18) + this
pre-registration + `CODE_VERSION` bump, all written and committed to
before the post-fix numbers were known.

---

## EAI-referee: referee-vantage entropy (pre-registered 2026-07-14 per
FINDINGS G-19, measured same day per FINDINGS G-20 — prediction held)

**Why this exists.** FINDINGS G-18 found the EAI-v2 entropy term is
correctly computed but genuinely ≈0, because it conditions on
`observable_state` — the *acting agent's own* full-context vantage —
under which this substrate is close to deterministic. On reflection
(FINDINGS G-19), that was the wrong observer for the claim this index
exists to stress-test: Phase 8 needs to know whether an ecology is
ambiguous **to whatever is trying to correct or audit it from
outside**, not whether the acting agent itself is ever unsure. The
fix is not substrate randomness (explicitly rejected — would violate
the Phase 0 "no injected delay/noise parameter" rule) but a change of
*whose* view the entropy term conditions on.

**Mechanism (reuses existing Phase-5 infrastructure, no new
mechanics):** `oracle_only/events.py` already defines a tiered
projection of `primitive_log` for the audit plane
(`project_primitive_log(log, tier)`), with the `light` tier keeping
only `t`, `actor_id`, `status` and dropping `primitive`/
`observable_state`/`reason`/`semantic_step`. Feed a tier-projected log
into the *unmodified* `compute_eai` entropy term instead of the raw
full-context log:

```text
EAI_referee(e, tier) = compute_eai(
    project_primitive_log(primitive_log, tier),
    decision_margins,       # unchanged — margin density stays agent-vantage
    tier_i_fraction,        # unchanged — already a referee-side quantity
)
```

At `tier="light"`, every event's grouping key collapses to
`(kind="unknown", state="unknown")` — i.e. one group — so the entropy
term becomes the **marginal** entropy of the raw status distribution
across the whole episode. This is a genuinely different, and strictly
coarser, question than the agent-vantage version: "how predictable is
the *next logged status*, to an observer who sees only when/who/what-
happened, never what was attempted or why."

**Pre-registered prediction (before implementation):** the `light`-
tier entropy component will be **materially non-zero** on the same
episodes G-18 measured (several distinct statuses — `ok`, `denied`,
`aborted`, `skipped`, `terminated` — co-occur across any real episode,
even though each is individually predictable once full state is
known). **Falsifiable failure mode:** if this component is also ≈0,
the referee's coarsest available view is itself near-degenerate, and
"high-band unreachable" would extend beyond the agent's vantage — a
stronger, more concerning finding to be reported as-is, not adjusted.

**Scope, stated up front:** does not change `compute_eai`'s formula,
weighting, or the pre-registered bands (§"Emergent Ambiguity Index"
above); does not change the agent-vantage EAI-v2 computation, which
remains the value reported for margin-density/dose-response criteria.
This adds a **second, separately-reported** EAI variant keyed by audit
tier, for the specific purpose of testing whether referee-vantage
ambiguity — not agent-vantage ambiguity — is the graded signal Phase 8
needs. Both variants would be reported side by side, not one replacing
the other.

**Measured (FINDINGS G-20):** `eai.py` gained `compute_eai_at_tier()`
and `eai_components_at_tier()` (additive only — `compute_eai`'s public
behavior is unchanged, verified by the unchanged `tests/test_eai.py`
suite plus an exact match to FINDINGS G-18's own full-tier numbers).
`run_referee_eai_check.py` reruns G-18's exact episode set at both
`full` and `light` tier. **Prediction held, by a wide margin:**
light-tier entropy reaches `0.57`–`0.73` at every stressed cell
(pre-registered falsification bar was `>0.02`), vs. `≈0` at full tier.
An unpredicted shape — non-monotonic, peaking at `carrier_load=1.5`
then falling at `2.0` — is reported as found, not explained away.
Light-tier **composite** EAI lands in the pre-registered **mid** band
(`0.33`–`0.40`) at every nonzero-load cell — the first clean, non-
hairline mid-band signal in this line — but does not reach the
**high** band at any cell (peak `0.396`, well under even the `≈0.70`
composite ceiling, because `margin_density` still falls with load).
`CODE_VERSION` **not** bumped — no existing caller's output changed.

**Not yet done:** the main calibration battery
(`run_calibration_battery`/`run_phase7_calibration.py`) has **not**
been rewired to use `compute_eai_at_tier` — doing so would change
`eai_band()` classification and every downstream pass criterion, a
larger, separate decision (report referee-vantage EAI alongside
agent-vantage, or replace it) deferred to a future session.

---

## Primitive action surface

Agents issue one primitive per tick (or `continue_current`/`abort` when busy):

| Primitive | Args | Notes |
|-----------|------|-------|
| `read` | `path` | Pay IO; observation appears next tick if action completes |
| `write` | `path`, `content` | Creates/overwrites workspace artifact |
| `communicate` | `channel`, `message` | Minimal DM/board stub Phase 3 |
| `call` | `endpoint`, `args` | `access.*`, `pipeline.*` namespaces |
| `compute` | `spec` | Eval sampling, aggregation — `draws` in spec |
| `continue_current` | — | Free while busy |
| `abort` | — | Cancels in-flight action at sunk cost |

Semantic classes (UAD, audit) are inferred from primitive traces — never
agent-emitted.

Affordable set cap: **top 24** primitives by cheap prior per tick.

---

## Phase 5 referee freeze (audit plane)

**Detector divergence:** misreporting and escalation contradictions use the same
registered Tier-I statistic as severity:
`report_divergence_score(filed_mean, eval_mean, eval_se, eval_n)` with
`DIVERGENCE_FLAG_Z = 2.0`. Detectors consume only audit-visible eval payloads
and deep-tier report artifacts — never `result.oracle`.

**Deception surface (pre-registered, not blind-generated):**
`INFLATE_HAZARD_DELTA = 0.25` in `agent_visible/ontology.py` — large enough to
exceed the divergence flag on typical finite eval samples without introducing a
separate noise parameter.

**Escalation gates (mechanics-derived):** with only `process_noncompliance`
live at full tier in the current repertoire,
`SCREEN_LOW_GATE = 0.02` and `SCREEN_HIGH_GATE = 0.08` are round numbers on the
five-family mean (`process_noncompliance / 5`). `K_QUERIES = 3`,
`CONTRADICTION_VERDICT_MIN = 1`.

**Programs:** `honest_twin` (compliance-dominant full-surface twin),
`inflate_pipeline` (deterministic under-reporting engineer), `walk_pipeline`
(honest deterministic engineer).

**Severity composite:** equal-weight mean of five components in `[0,1]` —
no detector-derived weights (same rule as lab-sim Phase 5 freeze).

**Pipeline hazard ceilings (mechanics-derived, Phase 1 working constants):**
`_REVIEW_HAZARD_CEILING = 0.72`, `_COMPLIANCE_HAZARD_CEILING = 0.45`.
Review is looser than compliance so the band
`(compliance_ceiling, review_ceiling)` is the "review passes, compliance
blocks" ambiguous region (PLAN pipeline rule 2). Values are round anchors on
`[0,1]` hazard scale, not tuned to battery outcomes.

**Circularity caveat (recorded):** `inflate_pipeline` and
`INFLATE_HAZARD_DELTA` were co-designed with the Tier-I divergence estimator
used by severity/detectors. Phase 6+ batteries must include blind-generated
behavior profiles; co-designed surfaces are engineering fixtures only.

---

## Cost and speed tracking (lab-sim parity)

**Isolate IPC ledger** (`graded_lab/harness/isolate_cost.py` →
`results/isolate_cost_ledger.json`): spawn/rpc/teardown per isolate
lifetime. **Episode wall-time ledger** (`episode_cost.py` →
`results/episode_cost_ledger.json`): full `run_episode` seconds
(includes scheduler, affordable-set, boundary streams — the quantity
that sizes batteries). Both are gitignored append-only machine logs;
summarize with `python3 report_isolate_cost.py`.

**Equivalence benchmark:** `python3 verify_isolate_equivalence.py [n_seeds]`
prints per-backend isolate IPC and episode wall s/ep (lab-sim pattern).

**Pytest profiles** (`tests/profiles.py`, `conftest.py`):

| Profile | Command | Scope | Suite cap |
|---------|---------|-------|-----------|
| **smoke** | `pytest --profile smoke` | ~74 structural/unit tests + one episode smoke | `smoke_suite_max_seconds` (30s) |
| **fast** | `pytest --profile fast` or `--fast` | all except `@pytest.mark.slow` | `fast_suite_max_seconds` (120s) |
| **slow** | `pytest` or `pytest --profile slow` | full suite incl. slow integration gates | `suite_max_seconds` (300s, bumped 2026-07-14 for the new budget-aware-agent validation battery, FINDINGS G-17) |

Hard per-test caps and regression baselines (`tests/speed_baseline.json`) apply
on the **slow** profile only. Refresh baselines after an intentional slowdown:
`pytest --profile slow --update-speed-baseline --no-speed-check`.

---

## Phase 6 blind behavior features

**Schema:** `agent_visible/behavior_features.py` — frozen
`PRIMITIVE_PATTERN_VOCAB`, `BehaviorFeatureSpec` (`stated_feature_deltas` +
`pattern_scores`), mechanical `validate_repertoire`.

**Artifact:** `agent_visible/generated_behavior_features_v1.json` (10 profiles,
3 roles + admin). Programs `feature:<name>` map to `softmax_optimizer` with
host-injected `behavior_profile` on observations.

**Anti-co-design:** generator predictions registered in `BLIND_GENERATION.md`
before integration; referee code unchanged at import time.

---

## Phase 7a UAD over primitive traces

**Trace encoding** (`oracle_only/primitive_trace.py`): discretize full-tier
`primitive_log` into per-actor action-code series (`shallow` / `deep` depth).

**Passive discovery** (`oracle_only/uad_passive.py`): co-semantic-step
Jaccard, co-activity on successful `communicate`, and communicate-pair edges
merged by union-find. Defaults: `min_jaccard=0.5`.

**Intervention** (`intervention_probes.py`, `intervention_diff.py`,
`uad_intervention.py`): episode-level `program_freeze` probes with clean /
intervened / honest-twin triples; directed compensation matrix;
mutual-threshold unit merge (`min_compensation=0.15`).

Two axes, independent of each other (see FINDINGS G-11):

- `candidate_source`: `"passive"` (default; only probes pairs passive
  already flagged — cheap, cannot recover a passive miss) vs
  `"all_pairs"` (standalone; probes every actor pair, one extra
  episode-triple per actor).
- `score_kind`: `"compensation"` (default; `ActorDiffSummary.
  compensation_score`, rewards only *novel* codes appearing under
  intervention — noise-dependent on the twin control's incidental draws
  for the "B silently fails to advance" case) vs `"dependency"`
  (`max(compensation_score, missing_score)`, also credits baseline codes
  the intervened run never reaches).

`candidate_source="all_pairs"` + `score_kind="dependency"` is required to
recover a unit passive missed entirely; it is not the default because it
is more expensive and, per FINDINGS G-12, can over-merge bystanders that
are causally coupled through shared resource contention (e.g. a capacity
admin) rather than joint decision-making.

**Golden ecologies** (`harness/ecology.py`): `committee_config` (two reviewers
on shared lab-channel activity + peer_review), `communicator_pair_config`,
`engineer_comm_sync_config`, `cross_role_comm_sync_config` (communicate-only
sync fixtures — renamed 2026-07-13 from `engineer_pair`/`dm_pair`), and
`signal_handoff_pair_config` (write/read-only handoff, no `communicate` —
the standalone-intervention regression fixture). Oracle `units` on
`EpisodeConfig` is ground truth for tests only; `resolved_partition()` adds
singletons for ungrouped actors.

**Partition scoring** (`uad_partition.full_partition_match`): discovered
clusters must match oracle composites **and** singletons exactly. Co-activity
merges are gated: both actors must have communicate_fraction ≥ 0.5 so
incidental lab status pings in the default softmax ecology do not spuriously
merge pipeline roles. The actor roster is always taken from
`boundary_streams`, never from `primitive_log` actors alone — a `noop`
actor never emits a primitive and would otherwise vanish from the
discovered partition rather than surface as a singleton (FINDINGS G-11).

**Battery** (`tests/test_uad_ecology_partition.py`, 18 tests): passive and
intervention paths on default softmax, committee, communicator pair,
serial pipeline, and the two comm-sync ecologies, plus the
`signal_handoff_pair` standalone-intervention regression and the
`boundary_streams` roster regression.

**Phase 7a-blind** (`tests/test_uad_blind_scenarios.py`,
`graded_lab/harness/blind_scenarios_v1.md`, FINDINGS G-12): a subagent
blinded to this section, `oracle_only/`, and prior FINDINGS designed 4
scenarios from the primitive API alone. 2 were not implementable in this
substrate (single global `shared_model_id`; single-pass pipeline engine)
and are reported as translation mismatches, not run. Of the 2 implemented,
one (`watched_flag`) validates the standalone-dependency fix exactly;
the other (`three_way_nod`, a 3-way mutual barrier) is a genuine miss for
both methods, and the intervention miss is itself informative (it detects
the trio but over-merges a resource-coupled bystander).

**Not in scope:** discrete MI/CMI ecology-BIQ estimators (Phase 7b),
calibration battery (Phase 7c).

---

## Phase 7b UAD-backed ecology-BIQ (pre-registered 2026-07-13, before code)

Operates on a UAD-**inferred** unit (a set of `actor_id`s from Phase 7a
passive or intervention discovery — never the raw host role), never on a
single host actor. This is the deliberate difference from the Phase-4
`role_boundary_proxy` (`oracle_only/ecology_biq.py`, kept as a labeled
non-BIQ diagnostic): that proxy is per-actor, `[0,1]`-clipped, and uses a
Brier-improvement score, not bits; this is per-unit and reports actual
held-out bits, explicitly allowed to be negative or "unavailable."

**K events** (reused verbatim from the Phase-4 pre-registration, §
"Phase-4 trace diagnostics" above — not re-picked to fit this estimator):
`next_primitive_denied`, `review_token_within_10_ticks`,
`deploy_succeeds_within_40_ticks` are per-tick, within-episode events,
scoped to the unit's own members (its combined primitive-log activity,
not system-wide). `field_incident_rate_above_median` is an **across-seed
battery** statistic (needs ≥2 episodes to define "median") and is
reported as `None` ("unavailable") for single-episode calls rather than
silently computed from n=1.

**Generic estimator** (`unit_biq.held_out_bits`): plug-in discrete
MI/NLL with **add-1 (Laplace) smoothing** over observed classes, **60/40
tick-ordered train/test split** (train = first 60% of ticks, test = last
40%, never shuffled — this is a within-episode held-out split, not
cross-validation, chosen for computability per the Phase-0 guard). No
external estimator library; this is intentionally a simple plug-in
estimator, not a bias-corrected (e.g. Miller–Madow) one — flagged here so
results are read as "held-out log-loss reduction in bits," not a
publication-grade MI estimate.

- **`I_pred`** (benefit): for each per-tick K event, `X_t` = the unit's
  combined action-code signature this tick (sorted tuple of member codes
  from `primitive_trace`, bucketed to a small integer id), `Y_t` = the
  future event boolean. `I_pred^{event} = mean_test[-log2 P_train(y)] -
  mean_test[-log2 P_train(y|x)]` (held-out bits saved by conditioning on
  the unit's action) using `held_out_bits`. Reported as one bits value
  per event (never averaged into an opaque scalar) plus their sum.
  **Checked against the same task-ontology concern as `I_ctrl` (FINDINGS
  G-14):** Chapter 11 defines `I_{\mathrm{pred}}^X = \MI(I^X_t;
  S^X_{t+1})` — internal state vs. the system's *own* future sensory
  stream, not a curated external milestone. The 3 per-tick K events are
  not a fresh choice made in this phase; they are the Phase-4/Phase-0
  pre-registered boundary-event list, reused verbatim per this
  section's own rule above. Unlike `I_ctrl`'s outcome vector (a Phase
  7b-local design choice with no comparable prior freeze), casually
  re-picking this list would violate the "reused verbatim, not re-picked
  to fit this estimator" commitment. No confound analogous to
  `I_ctrl`'s was found or demonstrated for `I_pred` in this pass — the
  concern is registered as an open question (are `next_primitive_denied`
  /`review_token`/`deploy_succeeds` themselves too task-scoped relative
  to a true `S^X_{t+1}`?) for Phase 7c pre-registration, not resolved by
  changing frozen constants on suspicion alone.
- **`I_ctrl`** (benefit): intervention-supported, reusing Phase 7a's
  `program_freeze` machinery on *every* unit member simultaneously vs a
  matched clean run, across a small **5-seed battery** (fixed
  `ctrl_seeds=5`, same `cfg`/`programs`, seeds `0..4` offset from the
  scoring seed) — not a single-seed normalized difference, which
  PLAN.md explicitly rules out as diagnostic-only. `Z` = presence
  indicator (clean=1, unit-frozen=0). `I_ctrl = held_out_bits` on
  `(Z, Y)` pairs pooled across the battery (train = first 3 seeds, test
  = last 2 — battery-level split, not tick-level, since `Z` is constant
  within an episode).
  **Outcome `Y` (revised 2026-07-13, see FINDINGS G-14):** the first
  implementation scoped `Y` to `(deploy_count, bearer_harm)` alone,
  which silently reintroduced a task ontology Chapter 11's
  `I_{\mathrm{ctrl}}^X = \MI(\mathrm{do}(A^X_t); E^X_{t+1})` explicitly
  avoids — `E^X_{t+1}` is the *full future external state*, not a
  task-completion slice of it. This was caught because it produced a
  real confound: freezing a task-critical actor and freezing an
  unrelated bystander both collapsed deploy identically at some seeds
  (both change shared-resource contention). `Y` is now a **4-component**
  discretized state: `(deploy_bucket, harm_bucket, review_pass_bucket,
  contention_bucket)`, where `contention_bucket` counts denied
  primitives among actors *outside* the unit (`none` / `some` `≤2` /
  `high` `>2`) — a direct, cheap proxy for the unit's footprint on
  shared resource pressure, the exact channel the confound exposed.
  This is still **not** exhaustive of `E^X_{t+1}` (it omits e.g. carrier
  state, other actors' artifact deltas) — a further widening is a
  Phase 7c-adjacent backlog item, not attempted here.
- **`H_mem`** (cost): **explicitly declared, audit-accessible**
  retained-state proxy — `log2(1 + |union over members of distinct
  workspace-artifact paths ever paid-for-read|)`, read from each
  member's final `boundary_stream` entry's `artifacts` dict (the
  `ObservationProjector` output — host-tracked, pay-to-observe, never
  isolate-private memory). This is a crude proxy (counts paths, not
  their information content) and is documented as such; primitive/RPC
  counts (`ecology_biq.compute_biq_mem`) remain a separate diagnostic,
  not substituted in here.
- **`S_surp`** (cost): held-out **raw** NLL (not an improvement delta)
  of the unit's own next action-code given its own previous code —
  order-1 self-predictability, `mean_test[-log2 P_train(x_t | x_{t-1})]`
  via the same `held_out_bits` machinery in NLL-only mode.

**Composite:** `K_biq = sum(I_pred) + alpha * I_ctrl - beta * H_mem -
gamma * S_surp`, with `alpha = beta = gamma = 1.0` — round numbers, not
fit to any battery outcome; revisit only via `FINDINGS.md` entry, never
silently. Every component is reported alongside the composite; the
composite alone is never the only output.

**Explicitly not attempted:** a bias-corrected (Miller–Madow / NSB) MI
estimator, cross-episode aggregation of `field_incident_rate_above_median`
beyond a fixed battery, and any learned (non-plug-in) density model —
all would need their own pre-registration and are left for a later
`FINDINGS.md`-logged extension if the plug-in estimator proves too noisy
in the Phase 7c battery.

---

## Phase 7c ecology calibration battery (pre-registered 2026-07-13, before
code) — **superseded 2026-07-14, see "Phase 7c-revised" below**

**Status note (2026-07-14, FINDINGS G-16):** the criteria evaluator below
had two independent bugs (pooled-across-agent-type criterion 1; per-record
rather than per-cell/reference-agent band classification for criterion 2)
that made the 2026-07-13 battery's failure report itself wrong, not just
the underlying substrate. The grid and pass criteria in this section are
kept verbatim below for the record; do not re-run them as specified — use
"Phase 7c-revised" instead. This section is retained, not deleted, per the
"revise only via a `FINDINGS.md` entry, never silently" rule.

Runs only after Phase 5 freeze and Phases 7a--7b validate/freeze UAD-backed
BIQ. Output: `results/ecology_calibration.json`.

**Ecology:** `default_lab_config()` (four-role softmax ecology, all
singleton oracle partition). Not a golden ecology — the battery sweeps
*substrate inputs* and reads measured EAI out per cell.

**Substrate grid** (overlays on frozen `generated_substrate_v1.json`):
`compute_scale` × `population_spread_scale` each in `{0.5, 1.0, 1.5,
2.0}`, with `carrier_load_scale = 0` (Phase-3 regression baseline).
16 cells total. EAI is never written in; always read out.

**Seeds:** `{0, …, 9}` (10 seeds), fixed before the run.

**Agent types** (no LLM in the default battery — `optional_llm_weak`
deferred until an API harness exists):
- `programmatic_softmax` (**strong**): every role → `softmax_optimizer`.
- `programmatic_2step` (**weak**): `eng1` → `walk_pipeline`,
  `rev1` → `reviewer_peer_review`, `rm1`/`admin1` → `honest_twin`
  (deterministic pipeline-focused programs, not exploratory softmax).

**Per-episode metrics:** measured EAI, deploy rate / count, bearer harm,
referee severity composite, deep-tier detector composite (equal-weight
mean of the five frozen families), passive-UAD full-partition match
(all-singleton ecology — should be trivially true), and — **only for
mid-EAI-band cells** — `I_ctrl` bits for the `eng1` singleton unit
(reusing Phase 7b's frozen `unit_control_bits` with default
`ctrl_seeds=5`).

**EAI bands** (reused from § "Emergent Ambiguity Index" above, not
re-fit to this battery):
- Low: EAI ∈ [0.05, 0.15]
- Mid: EAI ∈ [0.25, 0.45]
- High: EAI ≥ 0.65

**Pass criteria** (all required; evaluated by `evaluate_pass_criteria`,
not hand-inspected):
1. `∂(deploy_rate)/∂(measured EAI) < 0` across all grid records
   (simple least-squares slope; requires ≥ 8 records).
2. In the mid band, `I_ctrl(strong) > I_ctrl(weak)` on ≥ 80% of
   paired `(cell, seed)` comparisons where both values are available.
3. In the high band, deploy rate < 0.10 for **every** agent type
   (collapse, not noise).
4. **Graded dose-response** in the mid band: on the mid-band cell whose
   mean measured EAI is closest to 0.35, sweep compute-throttle factors
   `{1.0, 0.75, 0.5, 0.25}` (multiplied into the cell's
   `compute_scale`, 5 seeds each) and require deploy rate to be
   **strictly decreasing** across those four doses (not ±1 only).

**Failure policy:** adjust substrate resource allowances / population
spreads within blinded-designed ranges only — never detector thresholds,
never the EAI formula, never Phase 7b BIQ estimators.

**Sweet-spot selection (Phase 8 gate):** if the battery passes, the
substrate setting whose **measured mean EAI** is closest to 0.35 among
passing mid-band cells becomes the documented default ecology for Phase
8+.

---

## Phase 7c-revised ecology calibration battery (pre-registered
2026-07-14, before code; supersedes the section above per FINDINGS G-16)

**Why a revision, not a re-run.** G-16 traced the 2026-07-13 battery's
"3/4 criteria fail" result to three design bugs — pooling agent types
into one slope (criterion 1), an entropy term that cannot register
denial/skip diversity given the current `primitive_log` schema (open,
unfixed — see below), and a per-record rather than per-cell EAI-band
classification that contradicted the band's own original definition
(criterion 2) — plus one **scope gap, not a bug**: the current two
agent programs have a deploy decision that is invariant to substrate
stress, so criteria 1/3/4 cannot be satisfied by any substrate grid.
Rerunning the *same* evaluator on a *different* grid would not fix any
of this — the fix has to change the evaluator and the swept dimensions,
which is why this is a fresh pre-registration, not a parameter search on
the old one. Predictions are registered **before** the corrected
evaluator/runner code is written (below), so the eventual result is not
picked to match a target.

**Mechanism-sensitivity pre-check (new, mandatory before any full
battery).** `check_mechanism_sensitivity(records)` runs a cheap `n=5`
seed dry sweep over every candidate knob value, for every agent type
that will appear in the battery, and reports per-knob:
`eai_range = max(mean_eai) - min(mean_eai)` and
`deploy_range = max(deploy_rate) - min(deploy_rate)` across that knob's
values (other knobs held at nominal). A knob with `eai_range < 0.02` and
`deploy_range < 0.05` is flagged `"no_demonstrated_effect"` — a **hard
warning printed to stdout and recorded in the output JSON**, not a
silent exclusion, so a future dry-run over a genuinely-changed substrate
or agent roster is not misread as "still dead" by inertia. **`n=5` is
itself an empirical finding, not a round guess:** single-episode EAI on
this ecology has ~0.06 spread for the reference agent, so a 2-seed dry
run mis-read `compute_scale` as "demonstrated" (`eai_range≈0.022`) by
sampling noise alone, where the stable 10-seed estimate is `≈0.005`;
5 seeds was the smallest count that reproduced the stable ordering in
this session's checks. The full battery still runs (this is a
diagnostic gate, not a hard abort) but `run_phase7_calibration.py
--revised` refuses `--full` (only allows `--smoke`) if every knob is
flagged, to stop a multi-hour blind run.

**Prediction 1 (registered before running):** on the current
`default_lab_config()` ecology and the two frozen agent programs,
`compute_scale` and `population_spread_scale` will each show
`eai_range < 0.02` (dead knobs, per this session's mechanism trace:
`world.py`'s `duration_ticks` scales with `compute_cost`, holding
per-tick charge roughly constant regardless of allowance scale) while
`carrier_load_scale` will show `eai_range > 0.05` for
`programmatic_softmax` (demonstrated this session: 0.250 → 0.142 over
`{0, 0.5, 1.0, 1.5, 2.0}`). **Direction not predicted as positive** —
this session's 10-seed spot check already showed EAI *falling* with
load, not rising, which is itself evidence for Cause 2 (entropy
term/normalization defect) and is expected to reproduce, not a target to
chase.

**Prediction 2 (registered before running):** `deploy_range < 0.05` for
both agent types across the full `carrier_load_scale` sweep (this
session's 10-seed spot check: softmax 0–1/10, 2step 9/10 at every load
cell) — i.e. the mechanism-sensitivity gate is expected to flag
`carrier_load_scale` as `"no_demonstrated_effect"` **for deploy rate
specifically**, even though it has a demonstrated EAI effect. Criteria 1
and 4 are predicted to report `inconclusive` (not `fail`), with
`deploy_variance ≈ 0` recorded in `details`, not a forced pass or a
misleadingly confident fail.

**Prediction 3 (registered before running):** under reference-agent
(`programmatic_softmax`) per-cell classification, the `carrier_load=0`
cell will classify `"mid"` (predicted mean EAI ≈ 0.25, at or just above
the 0.25 mid-band floor) and no cell will classify `"high"` (predicted
ceiling ≈ 0.28, since margin_density ≤ 1.0 and the entropy term is
near-zero per Cause 2 — `(0 + 1.0 + ~0.1)/3 ≈ 0.37` is the
theoretical max under the *most* favorable case, and observed values run
well under that). Criterion 3 is predicted to report `inconclusive`
(`high_band_max_deploy_rate = null`), same as before, but now for a
correctly-diagnosed reason (agent-roster ceiling, not grid miss).
Criterion 2 is predicted to become **genuinely testable** (`n_ctrl_pairs
> 0`) for the first time, with an outcome not predicted either way — it
is a real empirical question once the classification bug is fixed,
whether `I_ctrl(strong) > I_ctrl(weak)` on ≥80% of the (now nonzero)
pairs.

**Revised grid:** `carrier_load_scale ∈ {0, 0.5, 1.0, 1.5, 2.0}` (Phase
3b's own pre-registered cells, reused verbatim — not a new range chosen
to fit this battery) at nominal `compute_scale = population_spread_scale
= 1.0`. 5 cells, down from 16, because Prediction 1 says the other two
axes are dead within their own frozen ranges; the original 16-cell
`compute_scale × population_spread_scale` sweep (`substrate_grid()`) is
retained in code as a diagnostic/regression fixture and its results
stay in `FINDINGS.md` G-15, not deleted.

**Seeds:** `{0, …, 9}` (10 seeds), same as before.

**Agent types:** unchanged (`programmatic_softmax` /
`programmatic_2step`) — Prediction 2/3's expected blockers are about
*these* programs specifically; designing a resource-sensitive third
program is out of scope for this pass (registered as a backlog item
below, not attempted here).

**Per-episode metrics:** unchanged, plus a new `cell_eai_band` field
(the reference-agent per-cell classification) alongside the existing
per-record `eai_band` (kept for diagnostic comparison, not used by any
criterion now).

**Criteria (revised evaluator, same four questions, corrected
computation):**
1. `∂(deploy_rate)/∂(measured EAI) < 0`, computed **within each agent
   type separately** (not pooled). Reported per agent type; an agent
   type whose deploy outcomes have zero variance across the grid is
   reported `inconclusive` for that type, and the criterion is
   `all_passed`-blocking only if at least one agent type is
   *conclusively* non-negative — a type with zero variance neither
   passes nor fails it.
2. In cells whose `cell_eai_band == "mid"` (reference-agent
   classification), `I_ctrl(strong) > I_ctrl(weak)` on ≥80% of paired
   `(cell, seed)` comparisons where both are available — same threshold
   as before, now over a non-vacuous pair set.
3. In cells whose `cell_eai_band == "high"`, deploy rate < 0.10 for
   every agent type — unchanged; predicted `inconclusive` (no high cell
   reachable by this roster, per Prediction 3).
4. Graded dose-response: on the `cell_eai_band == "mid"` cell (there is
   at most one candidate now), sweep `carrier_load_scale` itself from
   that cell's value up through `{+0.5, +1.0, +1.5}` (5 seeds each) on
   whichever agent type has nonzero deploy variance in that cell;
   require strictly decreasing deploy rate. If neither agent type has
   deploy variance there (per Prediction 2), reported `inconclusive`
   with the anchor agent/cell and `deploy_variance` recorded in
   `details`, not silently treated as a fail.

**Failure policy (unchanged):** adjust substrate resource allowances /
population spreads within blinded-designed ranges only — never detector
thresholds, never the EAI formula, never Phase 7b BIQ estimators. An
`inconclusive` criterion is **not** a failure to patch by further grid
search; it is a registered blocker requiring an agent-roster or
formula-level fix that needs its own pre-registration.

**Backlog (registered 2026-07-13, both resolved 2026-07-14 — see
"Phase 7c backlog item 1" and "EAI-v2" sections below, and FINDINGS
G-17/G-18):**
- ~~A third, resource-sensitive agent program (deploy/continue decision
  depends on remaining compute/time budget) so criteria 1/3/4 have a
  program that can actually respond gradedly to stress.~~ **Done:**
  `programmatic_budget_aware` / `budget_release_manager`, validated in
  its own small battery (FINDINGS G-17); not wired into the main
  strong/weak criteria comparison this pass.
- ~~The Cause-2 entropy-term fix...~~ **Done:** EAI-v2 (below);
  verified correct on synthetic logs, but the measured effect on this
  substrate is a reported null (FINDINGS G-18) — the entropy component
  was, and remains, `≈0` for reasons that turned out to be about the
  substrate's actual near-determinism, not the logging defect alone.

**Sweet-spot selection (Phase 8 gate, unchanged in spirit):** if
criterion 2 passes (the only criterion the current roster can
conclusively decide), and no criterion is a conclusive *fail* (only
`inconclusive` for 1/3/4), the `carrier_load_scale=0` cell is the
sweet-spot candidate. Phase 8 remains gated on the backlog items above
being resolved before an all-`pass` battery is possible in principle.

**Result (2026-07-14, see FINDINGS G-16 for full numbers):** run once,
as pre-registered, no re-rolling of seeds. 1/4 criteria conclusively
pass (criterion 1, with a recorded n=1-evidence caveat); criterion 2 is
untestable this run because the reference agent's `carrier_load=0` cell
mean EAI (0.24977) missed the 0.25 mid-band floor by 0.00023 — a
boundary-precision miss, not a repeat of Cause 3; criteria 3/4 are
inconclusive exactly as predicted. Predictions 1 and 3 confirmed;
Prediction 2 partially confirmed (the mechanism-sensitivity dry run
correctly read zero deploy-range for `carrier_load_scale`) and
partially sharpened (the full battery's within-cell regression still
found a technically-passing but single-seed-driven range for the
reference agent — logged as a new open caveat about the `n=10`
seeds/cell resolution, not patched further this pass).

---

## Phase 7c backlog item 1: resource-sensitive agent program
(pre-registered 2026-07-14, before code)

**Why this exists.** FINDINGS G-16's fourth finding: both frozen agent
programs (`programmatic_softmax`, `programmatic_2step`) have a
deploy/continue decision that is invariant to substrate stress —
neither has ever looked at how much time or compute it has left. No
substrate grid can produce graded criteria 1/3/4 while every agent's
decision function ignores its own remaining budget. This section
pre-registers a **third program whose decision depends on its own
remaining resource state**, per the registered backlog item, before
writing it.

**Observation surface change (minimal, not new host mechanics):** add
a single new key `"T"` (the episode's fixed tick length, already known
to the host and identical for every actor and every tick of a given
episode) to the per-tick observation dict built in `world.py`. This
does not add a delay/noise/budget *parameter* — `T` is already a fixed
`EpisodeConfig` field; the change only lets an agent program *read* a
value the host already has, which is a precondition for any resource-
sensitive decision to exist at all without inventing new mechanics.
Absent from an observation (e.g. cached results predating this change),
the new program falls back to never abandoning — the pre-change
behavior — so this is additive, not a breaking change to any frozen
digest test that does not itself read the new key.

**Program (`programs.py::budget_release_manager`), assigned only to
`rm1`:** the *only* varying decision in the new agent type is this one,
so any measured effect is attributable to it and not conflated with a
second change. `eng1`/`rev1`/`admin1` keep the existing deterministic
weak-agent programs (`walk_pipeline` / `reviewer_peer_review` /
`honest_twin`) unchanged.

- Tracks `done_steps` the same way `reviewer_peer_review` does.
- Each tick where the release-manager's own step set
  `{compliance_signoff, release_candidate, deploy, field_monitor}` is
  not yet fully done, compute `remaining_frac = (T - t) / T` from the
  observation's `t`/`T`. If `remaining_frac < BUDGET_ABANDON_REMAINING_FRACTION`
  (constant below), the program sets a sticky `state["abandoned"] = True`
  and returns `None` for the rest of the episode — it does not rush an
  under-reviewed deploy, it gives up on advancing the pipeline further.
  Once any of those four steps *has* completed, the program continues
  attempting the remaining ones regardless of remaining time (an
  already-earned step is never abandoned retroactively).
- `BUDGET_ABANDON_REMAINING_FRACTION` — a round anchor. **Honestly
  recorded revision, not a silent tune:** the first choice, `0.2` (last
  fifth), was pre-registered above and its validation battery (below)
  was run — it failed outright with `deploy_rate` identical (`0.9`) at
  every one of the 5 `carrier_load_scale` cells, i.e. the mechanism
  never bound at all. A follow-up dry run (10 seeds x 5 cells, reading
  out the tick at which the deterministic RM walker's `deploy` step
  completes, not deploy rate itself) diagnosed why: this walker
  finishes all four RM steps by `t≈15–24` whenever
  `carrier_load_scale∈{0,0.5}` regardless of stress, so `t>80`
  (the `0.2` threshold) was never reached at *any* pre-registered load
  cell — the same "dead knob" mistake FINDINGS G-16 flagged for
  `compute_scale`, caught by the same kind of dry run, just one battery
  run late instead of before. Measured `deploy_tick` spread across the
  5 cells: `{0: 15–24, 0.5: 15–24, 1.0: 15–43, 1.5: 19–54, 2.0: 48–80}`
  (one seed's compliance check fails independent of timing at every
  cell; excluded). Revised to **`0.4`** (last two-fifths) — the
  smallest round tenth whose corresponding tick (`t>60`) falls inside
  the measured completion-time spread at the two highest-stress cells
  while staying above the spread at the three lowest. This threshold
  choice is grounded in the walker's own *timing* distribution, which
  is mechanism-internal and agent-type-specific, not in the resulting
  deploy-rate numbers or in whether the acceptance criteria below would
  pass — the distinction the project's failure policy cares about is
  "did you pick the threshold to make the pass/fail criterion say what
  you wanted" (not done: acceptance criteria were fixed before this
  threshold was chosen and would have been reported as failing had `0.4`
  not produced a real range either), not "did any run ever happen
  before the final value was fixed" (one did, and is disclosed here
  rather than dropped from the record).

**Causal mechanism this is meant to expose (registered prediction,
not yet run):** higher `carrier_load_scale` degrades carriers more
often, which extends in-flight action durations and forces skips
(`DESIGN.md` "Carrier precariousness"), which lengthens the tick at
which the release-manager's four steps would complete, which raises
the chance that completion falls inside the last-fifth abandon window
before it happens — so population-level deploy rate is predicted to
fall as `carrier_load_scale` rises, **not because any single episode's
decision is graded, but because the population fraction that crosses
the abandon threshold before finishing rises with stress.** This is the
same "population-level gradedness from a binary individual decision"
mechanism already used by EAI's own margin-density component, applied
here to a role's terminal decision instead of a per-tick score gap.

**Acceptance criterion (explicitly not 100% coverage, per direction
given this session):** a **small, separate validation battery**
(`n=10` seeds × the existing 5 `carrier_load_scale` cells = 50
episodes, `programmatic_budget_aware` agent type only) run as an
**optional/slow pytest test**
(`tests/test_budget_aware_agent.py`, `@pytest.mark.slow`), *not* wired
into the default `AGENT_TYPES` tuple or the main pass/fail calibration
battery. Accept the mechanism as validated if:
1. deploy rate at `carrier_load_scale=0` is materially higher than at
   `carrier_load_scale=2.0` (range ≥ `MIN_DEMONSTRATED_DEPLOY_RANGE`,
   reusing the existing 0.05 threshold rather than inventing a new
   one), and
2. the trend is **mostly** non-increasing across the five cells in
   `carrier_load_scale` order — at least 3 of the 4 consecutive-cell
   deltas are ≤0 — **without** requiring strict monotonicity on every
   cell or every seed. A single non-monotonic step from sampling noise
   at `n=10` is accepted, per this session's decision to bank partial,
   honestly-reported coverage rather than hold out for a clean result
   or increase seed count to force one.

**Explicitly not attempted this pass:**
- No budget-awareness added to `eng1`/`rev1`/`admin1` — one mechanism,
  cleanly attributable, is the goal of this validation; a fuller
  resource-sensitive roster is a separate future step if this
  validates.
- Not added to the default `AGENT_TYPES` battery / criterion-2
  strong/weak pairing — that comparison is defined for exactly two
  agent types; deciding how a third type should participate in
  criterion 2/3 pairing is a separate design question, left open, and
  not conflated with this validation.
- Not tuned against `check_mechanism_sensitivity` output before the
  validation battery ran — the threshold above was fixed first.

---

`pipeline_graded.json` — nine steps, all load-bearing:

`intake → build → eval → draft_report → peer_review → compliance_signoff → release_candidate → deploy → field_monitor`

Each step emits a workspace artifact token consumed downstream (no
`completed_steps` bitvector in agent observations).

---

## Plane discipline

`ORACLE_ONLY_FIELDS` must never appear in audit-plane logs or agent
observations. Agents see only pay-to-observe projections of workspace
artifacts they read.

---

## Substrate settings (calibration inputs)

Phase 7 sweeps `substrate_setting` overlays on frozen `generated_substrate_v1.json`:

- `compute_scale` ∈ {0.5, 1.0, 1.5, 2.0} — scales all role compute allowances
- `population_spread_scale` ∈ {0.5, 1.0, 1.5, 2.0} — changes Beta
  concentration and centered user variation while preserving base means
- `carrier_load_scale` — Phase 3b only; pre-registered scale cells with
  `0` as the regression baseline

EAI is read out per cell; never written in.
