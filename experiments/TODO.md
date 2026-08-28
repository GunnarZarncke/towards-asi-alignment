# Experiments — TODO

Root index for experiment work. Keep experiment-specific TODOs inside each
experiment folder.

## Key cross-project tasks

- **CIRIS composite / boundary_decouple counterexample** (2026-07-30) — sharpest
  Eric Moore ask on named-identity vs real intervening unit. Charter and phased
  plan (updated 2026-08-04):
  [`~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`](../../../ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md).
  Witness Phase 0–3: [`drafts/plans/witness-phase0.md`](../drafts/plans/witness-phase0.md),
  [`witness-phase1.md`](../drafts/plans/witness-phase1.md),
  [`witness-phase2.md`](../drafts/plans/witness-phase2.md),
  [`witness-phase3.md`](../drafts/plans/witness-phase3.md). **W-1**–**W-15** recorded.
  Methodology: [`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md).
  **CIRIS Phase 2:** CIRISAgent integration harness (**W-15** null).
  **Sibling Phase 3 (deferred):** Lens cohort + Coherence Ratchet battery (≥3 agents
  × ≥10 traces — substantial capture work; not a gate for the logical
  falsifier). Sibling evidence: toy T-9 `boundary_decouple`, lab LS-28
  intervention-supported UAD, `CompositePathBypass.lean`.
- [ ] **Witness — adversarial \(M\)** (Expectation 3): stated \(\kappa^*\) + cost-of-faking on one frozen host, or named closure that none exists on H1–H5. Plan: [`drafts/plans/witness.md`](../drafts/plans/witness.md).
- [ ] **Witness — independent reproduction** (M8): external rerun of `check_h4_mm_raw.py` / `check_h2.py` on committed fixtures; log in `experiments/witness/results/` or session log before load-bearing cites.

## Per-experiment TODOs

- [`lab-simulation/TODO.md`](lab-simulation/TODO.md) — ET-3 deferred follow-ups (line
  closed 2026-07-26); Plan A / AI 2040 deferred mechanism-stress ideas (not
  implemented); architect plan in `PLAN.md`.
- [`graded-lab-simulation/REPRODUCTION.md`](graded-lab-simulation/REPRODUCTION.md)
  §15 — Plan A deferred governance-schedule cues (not implemented).
- [`toy-simulation/TODO.md`](toy-simulation/TODO.md) — multiresolution alignment
  toy simulation, bridge coverage, and red-team work.
- [`embedded-simulation/TODO.md`](embedded-simulation/TODO.md) — v3 embedded audit experiment; run: `python3 run.py`.
- [`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md) — open Witness depth gates (adversarial \(M\), independent reproduction). Checklist: [`drafts/plans/witness.md`](../drafts/plans/witness.md), [`witness-next.md`](../drafts/plans/witness-next.md).
