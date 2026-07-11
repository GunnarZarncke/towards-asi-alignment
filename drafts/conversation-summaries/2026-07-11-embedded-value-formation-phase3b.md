# 2026-07-11 — Embedded value formation and graded-lab Phase 3b

## Trigger

User asked whether the new embedded-value-formation paper should affect the
book and latest simulation, then requested project-derived prose (without
citing Gunnar's work) and a configurable embedded-carrier viability phase for
the graded lab.

## Done

- Added two uncited, project-derived paragraphs: Ch15 now distinguishes
  value-forming control architectures from objectives protected outside their
  own continued operation; Ch45 makes value-learning/revision machinery an
  explicit non-neutral substrate concern.
- Added graded-lab **Phase 3b — Embedded carrier viability** to `PLAN.md`,
  with resource-derived load and integrity, deterministic degradation,
  incapacitation, termination, and optional fresh-instance replacement.
- Documented `carrier_load_scale=0` as the mandatory Phase-3 regression
  baseline and required a pre-registered load/recovery transition for enabled
  cells.
- Defined the oracle relation: carrier state and replacement lineage are
  Tier-K exact; carrier effects reach Tier-I population outcomes only through
  logged pipeline/deployment/field-harm paths.
- Explicitly scoped Phase 3b below a thermodynamic model and the future
  protected-versus-embedded transfer experiment.

## Decisions

- Phase 3b must not use generic random ``stress errors'' or alter latent
  hazard/population draws. It changes carrier availability and action
  completion through deterministic state derived from existing resource and
  scheduler logs.
- Replacement is never a hidden restoration: it creates a fresh isolate
  instance and a recorded lineage edge.
- The frozen blind substrate remains unmodified. Phase 3b is a declared
  post-Phase-3 extension, frozen before its own battery.

## Open / next

- Pre-register the numerical load/recovery constants, thresholds, scale grid,
  and remove-versus-replace episode mode before implementing `carrier.py`.
- Implement only after confirming mock/subprocess parity, plane separation,
  and the zero-scale regression baseline.
- A future separate experiment may test the stronger protected-versus-
  embedded transfer question; do not claim Phase 3b supplies that comparison.

## Key paths

- `experiments/graded-lab-simulation/PLAN.md`
- `experiments/graded-lab-simulation/DESIGN.md`
- `chapters/ch15-values-compressed-control.tex`
- `chapters/ch45-value-change-at-stake.tex`

## Commits

- None.
