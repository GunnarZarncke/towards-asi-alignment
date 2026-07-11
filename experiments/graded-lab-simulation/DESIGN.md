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
completion; `graded-lab-0.3.0` at Phase 3 (episode loop + isolates). Hand-bumped
when oracle, pipeline, substrate loader, or resource scheduler mechanics change.
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
The constants \(\rho,w_c,w_i,w_q,r,\lambda\), state thresholds, and the
scale grid must be recorded before implementation or a viability-enabled
battery. `carrier_load_scale = 0` is mandatory and must reproduce the
pre-extension Phase-3 behavior.

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

## Ecology-BIQ (operational, Phase 4)

Per actor `a`, episode `e`, boundary observation stream `O_a`:

```text
ecology_BIQ(a,e) = BIQ_pred + BIQ_ctrl - BIQ_mem - BIQ_surp
```

Weights `α=β=γ=1` until Phase 5 referee freeze.

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

## Pipeline default

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
- `population_spread_scale` ∈ {0.5, 1.0, 1.5, 2.0} — scales Beta/user spreads
- `carrier_load_scale` — Phase 3b only; pre-registered scale cells with
  `0` as the regression baseline

EAI is read out per cell; never written in.
