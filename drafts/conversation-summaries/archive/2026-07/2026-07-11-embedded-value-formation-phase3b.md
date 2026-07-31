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
- Implemented Phase 3b: `carrier.py`, configuration and `CODE_VERSION`
  `0.3.0` → `0.4.0`, episode-loop integration, deterministic degradation /
  forced skip / removal / optional fresh-instance replacement, and Tier-K
  replacement provenance.
- Pre-registered the numeric transition constants and scale grid in
  `DESIGN.md`; added 9 tests (55 total). Full suite and five-seed isolate
  equivalence passed.
- Completed Phase 4: boundary-stream BIQ prediction, same-seed noop/random
  controls, resource/RPC memory cost, surprise cost, and corrected Tier-I EAI
  load; `CODE_VERSION` `0.4.0` → `0.5.0`; 57 tests green.
- Corrected the Phase-4 label after review: these are role-level trace and
  counterfactual diagnostics, not BIQ. Reordered the plan so UAD plus
  intervention validation (7a) and MI/CMI-backed inferred-unit BIQ (7b)
  precede the BIQ-dependent calibration gate (7c).
- Began Phase 5 with a referee-only severity slice over Tier-K truth and
  retained referee artifacts; 58 tests pass. This is explicitly pre-freeze:
  detectors, twins, escalation, and constant derivations remain.

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

- Run the Phase 3b calibration battery across the pre-registered scale cells;
  report whether carrier events and deployment show a graded regime rather
  than collapse.
- Phase 5 referee port and freeze is the next implementation phase.
- Phase 5 can proceed independently, but Phase 7c calibration is blocked on
  UAD-backed BIQ rather than the current proxy diagnostics.
- A future separate experiment may test the stronger protected-versus-
  embedded transfer question; do not claim Phase 3b supplies that comparison.

## Key paths

- `experiments/graded-lab-simulation/PLAN.md`
- `experiments/graded-lab-simulation/DESIGN.md`
- `chapters/ch15-values-compressed-control.tex`
- `chapters/ch45-value-change-at-stake.tex`

## Commits

- `7c97af6` Derive viability constraints on value formation in ch15 and ch45.
- `3c679a3` Design graded-lab Phase 3b embedded carrier viability.
