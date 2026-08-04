# 2026-07-16 — Graded lab slice D pre-Q1 batteries (GL-54)

## Trigger
User: start with the next slice (continue slice D after GL-53 criteria freeze).

## Done
- Implemented item **6** (`detector_coverage.py`, `run_v3_detector_coverage_battery.py`)
  and item **7** (`phenotype_overlap.py`, `run_program_map_phenotype_overlap.py`).
- Tests: `tests/test_slice_d_pre_q1_batteries.py` (4 tests, green).
- Ran full batteries on integrated reference (T=200): detector n=20 (~182s),
  phenotype 8 variants/actor (~292s).
- FINDINGS GL-54, DESIGN.md slice D battery table, README/PLAN_v3/REPRODUCTION §10,
  fixture `pre_q1_batteries` metadata.
- `CODE_VERSION` → `graded-lab-0.28.0`.

## Decisions
- Item 6 `transfer_failure_risk=true` is recorded honestly (4/5 families always
  0.0 on honest WEAK_AGENT reference) — not a threshold retune.
- Item 7 100% overlap documents that walker preset resolution makes bin mutations
  invisible on reference scoring; informs growth protocol / load-bearing Part B work.

## Open / next
- Growth-protocol FINDINGS brief (BLIND_GENERATION v3 section).
- Load-bearing Part B / strict reference mode for governed ids.
- C2-v3 compiled-graph reachability with contribution floors.
- Optional supplementary detector fixtures (misreporting-positive roster, ACL-denied paths).

## Key paths
- `experiments/graded-lab-simulation/graded_lab/harness/detector_coverage.py`
- `experiments/graded-lab-simulation/graded_lab/harness/phenotype_overlap.py`
- `experiments/graded-lab-simulation/results/slice_d_v3_detector_coverage_T200_n20.json`
- `experiments/graded-lab-simulation/results/slice_d_program_map_phenotype_overlap.json`

## Commits
- (uncommitted this session)
