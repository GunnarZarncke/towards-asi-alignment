# 2026-07-18 — Graded lab PLAN_v4 V4-4: R-MB6a variation operator + null harness (GL-81)

## Trigger

User: "continue plan" — after V4-3 (GL-80), next stage per `PLAN_v4.md`
build order is V4-4 (R-MB6a selection machinery sanity).

## Done

- **V4-1 freeze** for R-MB6a in `DESIGN.md` ("PLAN_v4 pre-registration
  — R-MB6a scope") before scoring.
- **`harness/variation_operator.py`** — closed `ProgramMap` edit
  vocabulary; `phenotype_overlap.py` deduplicated to import from here.
- **`oracle_only/stats.py`** — `permutation_mass_movement_band`,
  `observed_mass_range`, `N_PERMUTATIONS=200`.
- **`harness/rigs/r_mb6a_selection_sanity.py`** — C4 precondition,
  expressiveness report (100 mutants requested), uniform-fitness null
  harness (pop 8, 6 gen, 2 ep/member).
- CLI, tests (`test_variation_operator.py`, `test_rig_r_mb6a.py`).
- **Scored (GL-81):** `results/v4_r_mb6a.json` — 710 s wall.
  Precondition pass (deploy rate 0.85). **Outcome pass** (P5 holds).
  Expressiveness: only **11/100** syntax-distinct mutants sampled on
  `walk_pipeline` baseline; all 11 distinct phenotypes.

## Decisions

- R-MB6a smoke uses **8 fixture seeds** (not 4): 4 seeds on v3_grown
  gives 100% deploy and fails C4.
- Expressiveness is **report-only** for pass/null; only P5 is blocking.
- Did not expand the baseline ProgramMap or add walker-mode interpreter
  to inflate syntax cardinality — the 11/100 saturation is recorded
  as an honest finding (GL-54 scorer-only slice + sparse baseline).

## Open / next

- V4-5: R-MB2 ∥ R-MB5 ∥ R-MB8 (medium builds) — still blocked on open
  questions for R-MB5/R-MB8 worth-it and R-MB7 budget.
- V4-7: R-MB6b — blocked on open question 1 (growth vs declared-SKIP).
- No manuscript harvest yet.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/harness/variation_operator.py`
- `experiments/graded-lab-simulation/graded_lab/harness/rigs/r_mb6a_selection_sanity.py`
- `experiments/graded-lab-simulation/results/v4_r_mb6a.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-81)

## Commits

- None yet (not asked to commit).
