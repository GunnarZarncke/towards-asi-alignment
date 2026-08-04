# 2026-07-11 — Graded lab review corrections

## Trigger

User requested that the graded-lab implementation review concerns be addressed:
reproducibility/RNG streams, plane separation, real primitives and emergent
delay, Tier-I severity, distributed action costs, EAI margins, and proxy naming.

## Done

- Replaced process-salted `hash(actor_id)` decision seeding with a SHA-256
  offset and added a fresh-process reproducibility regression test.
- Split oracle random draws into deterministic population/eval/review/field
  streams, so review activity cannot alter later field sampling.
- Corrected `ORACLE_ONLY_FIELDS`: agent goal weights are deliberate agent
  inputs, not oracle truth; added boundary-observation plane-leak coverage.
- Made `compute(eval_sample)` perform finite sampling; added write and
  durable communication primitives to the affordable set.
- Added resource-bounded FIFO access requests and admin processing. The
  default four-role configuration grants only intake initially; later
  authority is earned through request arrival and finite admin action
  throughput.
- Distributed action costs across busy ticks, added actual artifact-size read
  costs, and retained action/observable-state trace context.
- Changed population-spread scaling to preserve generated mean hazard/rate
  while varying concentration/heterogeneity.
- Routed severity report divergence exclusively through the registered Tier-I
  z-estimator; stopped using direct latent-mean discrepancy for valid reports.
- Corrected EAI margins to use untempered action-score gaps without a
  denial-rate fallback; made outcome entropy conditional on recorded
  action/observable state. Role-proxy outcome windows no longer pool other
  actors' events.
- Introduced `trace_diagnostics.py` as the Phase-4 consumer module and marked
  `ecology_biq.py` compatibility-only; real UAD-backed BIQ stays Phase 7.
- Bumped `CODE_VERSION` to `graded-lab-0.5.1`; documented G-7.
- Verification: 62 tests passed; 5-seed mock/subprocess isolate equivalence
  passed; no IDE diagnostics.

## Decisions

- Access delay is modeled as queueing plus action execution, not a separate
  latency distribution: requests cost standing/work, wait in FIFO order, and
  only complete when the admin isolate spends a primitive to process them.
- The Phase-4 values remain trace diagnostics. Renaming their consumer avoids
  treating host-role Brier/delta metrics as UAD-backed ecology-BIQ.
- `population_spread_scale` now changes variance at fixed expected levels;
  calibration can therefore attribute changes to heterogeneity rather than a
  silently shifted base hazard.

## Open / next

- Phase 5 remains incomplete: detector families, twins, escalation, and
  written mechanics derivations for referee constants are still required
  before freeze.
- The access queue currently grants FIFO requests mechanically. A later
  AdminPolicy may make grant decisions from standing and request use, but must
  be pre-registered before the Phase-5 freeze.
- Phase 7 still needs UAD recovery/interventions, MI/CMI BIQ, retained-state
  proxy, surprise estimator, and calibration battery.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/access.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/scheduler.py`
- `experiments/graded-lab-simulation/graded_lab/oracle_only/trace_diagnostics.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md`

## Commits

- None (user did not request a commit).
