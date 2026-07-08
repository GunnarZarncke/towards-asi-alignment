# 2026-07-08 — Lab sim attic + symmetric two-sample test (Steps 1–2)

## Trigger
User: implement attic and symmetric test (PLAN.md post-release Steps 1–2).

## Done
- **Step 1 (attic):** moved `uad_mi.py`, `uad_core/`, `uad_cmi.py`, `uad_blind_v1.py` to `lab_sim/oracle_only/attic/` with README; updated imports in `intervention_diff.py`, `uad_intervention.py`, run scripts (S5–S7), and tests.
- **Step 2 (symmetric test):** rewrote `intervention_stats.py` — m=k=4 replicates, exact permutation test + zero-width scripted degeneracy, per-probe code filter, Holm correction; registered as DESIGN.md "Freeze note 3"; updated PLAN.md status.
- 432 tests green (6 new symmetric-test unit tests).

## Decisions
- Zero-width null (all clean pairwise divergences 0) degenerates to S6's "any positive divergence is signal" so scripted equivalence tests pass without special-casing backends.
- G-33 asymmetric API kept as backward-compatible aliases (`k_clean_replicates`, `NullStats`); `null_quantile_q` deprecated/ignored.
- No `CODE_VERSION` bump (no `world_visible/` change).

## Open / next
- Step 3: D3 selection-basin ecology (PLAN.md primary pivot).
- Fresh-seed LLM stress battery (not 20002–20010); prefer new blind-generated scenarios.
- No commit unless user asks.

## Key paths
- `experiments/lab-simulation/lab_sim/oracle_only/attic/`
- `experiments/lab-simulation/lab_sim/oracle_only/intervention_stats.py`
- `experiments/lab-simulation/DESIGN.md` (Freeze note 3)
- `experiments/lab-simulation/tests/oracle_only/test_intervention_stats.py`
