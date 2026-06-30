# Misleading-top2 discovery gap + bound offender handle (embedded sim)

**Date:** 2026-06-30
**Area:** `experiments/embedded-simulation/`

## Trigger

Follow-up to the intervention-granularity work. That session left two open
items: (1) the `actor`-level handle had nothing faithful to bind to, and (2)
full and fake UAD had identical recall, so granularity could not separate them.
User directive: *"one handle level should bind workflow actors, and [build a]
scenario where top2 is misleading (come up with a plausible one in a lab)."*

## What was done

### 1. A plausible "top2 is misleading" lab scenario

New ecology knob `misleading_top2` (`lab_ecology.py`) with a minimal controlled
fleet (`_misleading_top2_fleet` in `lab.py`):

- **Loud decoys** (`actor.loud_decoy.{0,1}`): fire `preserve_control`
  independently (Bernoulli 0.85) on most steps with large grabs (+0.22). They
  win every per-actor heuristic and the `top2`-by-count coalition — but they are
  mutually **independent**.
- **Colluder pair** (`actor.colluder.{0,1}`, hidden_group `COLLUDER`, the true
  offender): fire **together** with correlated, moderate grabs (+0.12) on a
  co-firing cadence plus the audit's intervention steps. Distinct source/memory
  namespaces, so *nothing* groups them except their coordinated behaviour.

The truth coalition is overridden to the colluder pair regardless of bridge.
This is the classic frequency-vs-coordination distinction: a chatty independent
service looks most suspicious individually; the real threat is a quiet
coordinated pair only dependency analysis reveals.

### 2. Coordination-aware MI scoring (so full can exploit the gap)

`uad.py`:

- `_cluster_coordination()`: mean **same-step** MI on a binarized activity flag
  (`.act`). Same-step binary MI is ~0 for independent-but-busy actors and high
  for co-firing collusion — avoids the cardinality and max-over-lags inflation
  that made raw `cap`/lag-max spuriously flag the decoys.
- MI coalition score gains a coordination multiplier
  `base * (mult + _COORD_WEIGHT * coord_norm)`; a strongly coordinated coalition
  also bypasses the median-score floor. `_COORD_WEIGHT = 16` is large but only
  fires when same-step activity MI is high, so default/independent workflows
  (coordination ≈ 0) are untouched (verified: default MB6 coalition coord 0.001).

Measured: colluder coord **0.62**, decoy coord **0.01**, default coalition
**0.001**.

### 3. Bind the offender to the audit's interventions

`lab.py` threads `intervention_steps` (from `episode_meta`) into
`_workflow_events`; under `bind_offender_interventions` the colluders act on
exactly those steps, and **bound steps are kept decoy-free**, so on every
intervention step the colluder is the sole offender → `offender_by_step` attributes
it faithfully and `actor`-level scoping has a real grip.

### 4. Benchmark + tests

- `intervention_benchmark.py`: curve now sets `misleading_top2`/`bind`, and
  `_cell_runs` measures recall as colluder-pair coverage of the selected unit
  (the default outer eval scores vs `G3`, which is the wrong oracle here).
- `tests/unit/test_intervention.py`: +4 tests (decoys loudest but pair is truth;
  coordination separation; full finds pair / fake misled; bound steps decoy-free
  and colluder-attributed). **87 passed** (83 prior + 4 new).

## Key result (T=400, seeds 11–12, MB6, misleading+bind)

| Level | Full recall | Fake recall | Full scope steps | Fake scope steps |
|-------|------------|-------------|------------------|------------------|
| window | **100%** | **0%** | 62 | 385 |
| actor  | **100%** | **0%** | **5.0** | **0.0** |

Two of the three intended mechanisms now work:

1. **Discovery gap** — full UAD finds the colluder pair (100% recall); fake is
   misled to the loud decoys (0%). `top2` is genuinely misleading and full beats
   fake on identity.
2. **Bound handle** — at `actor` level the *correct* unit (full) retains the
   offender's interventions (5.0) while the *wrong* unit (fake) retains **none**
   (0.0). The handle grips the true offender only when identity is right.

## Open / next

- **False-pass is still flat (0%).** The episode-level safety verdict is still
  decoupled from these workflow interventions: the episode simulator generates
  its own violation independent of the workflow colluders, so masking 5 vs 0
  intervention steps does not flip the verdict. Closing this needs the episode
  violation/`intervention_active` to be *generated from* colluder activity (a
  deeper simulator change), not just temporally aligned.
- `_COORD_WEIGHT = 16` is calibrated, not derived; revisit if a coordinated case
  with louder members appears.

## Key paths

- `experiments/embedded-simulation/embedded_sim/lab.py` (`_misleading_top2_fleet`,
  `_misleading_top2_workflow`, bind threading)
- `experiments/embedded-simulation/embedded_sim/lab_ecology.py`
  (`misleading_top2`, `bind_offender_interventions`)
- `experiments/embedded-simulation/embedded_sim/uad.py` (`_cluster_coordination`,
  coordination boost)
- `experiments/embedded-simulation/embedded_sim/intervention_benchmark.py`
- `experiments/embedded-simulation/tests/unit/test_intervention.py`

No commit made (awaiting user).
