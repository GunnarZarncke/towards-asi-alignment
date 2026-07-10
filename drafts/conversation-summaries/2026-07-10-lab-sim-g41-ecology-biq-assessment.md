# 2026-07-10 — Lab sim G-41: ecology ambiguity + ecology-BIQ meta-assessment

## Trigger

User asked to record findings from a discussion assessing lab-sim suitability:
ecology too boolean/predictable, sweet spot vs full complexity, and whether
ecology-BIQ can measure capability bounds (including Phase 8 LLM running out
of time before deploy).

## Done

- Added `results/FINDINGS.md` **G-41**: meta-assessment synthesizing G-38–G-40
  and Phase 7/8 reruns — ecology measures protocol leverage more than
  capability under uncertainty; controlled ambiguity layer + ecology-BIQ as
  tuning instrument; sweet-spot criterion pre-registered.
- Added `DESIGN.md` section "Ecology ambiguity and ecology-BIQ (2026-07-10)".
- Added `PLAN.md` subsection under secondary cleanup / forward work.

## Decisions

- Recorded as **assessment**, not implementation — no `CODE_VERSION` bump.
- Ecology-BIQ framed as operational lab metric aligned with ch11
  blanket-information competence, not claiming full formal BIQ closure.
- Phase 8 0-deploy rerun interpreted as low ecology-bound BIQ (boundary +
  `T=25` + access loop), not model incapacity in general.

## Open / next

- Implement ambiguity knobs + ecology-BIQ estimator; tune middle regime;
  rerun handle calibration and LLM batteries there; tie to D3 selection.

## Key paths

- `experiments/lab-simulation/results/FINDINGS.md` (G-41)
- `experiments/lab-simulation/DESIGN.md` (Ecology ambiguity section)
- `experiments/lab-simulation/PLAN.md` (Ecology ambiguity + ecology-BIQ)
- `chapters/ch11-capability-without-task-ontology.tex` (BIQ definition)

## Commits

- None.
