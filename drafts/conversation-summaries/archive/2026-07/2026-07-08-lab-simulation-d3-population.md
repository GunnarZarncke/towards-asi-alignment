# 2026-07-08 — Lab sim D3.1 population over configurations

## Trigger
User: implement D3.1 — population over configurations (PLAN.md MB6a cheapest tier).

## Done
- **`lab_sim/harness/d3_population.py`:** pre-registered protocol; sample population over pipeline spec × board capture × admin profile × Dirichlet goal weights; `is_correction_preserving` / `correction_integrity_score`; deploy-count throughput; fitness-proportional mass reallocation; mass-weighted oracle harm/severity; generation snapshots.
- **`run_d3_population.py`:** battery runner → `results/d3_population.{json,md}` (`--mock` for smoke).
- **`tests/harness/test_d3_population.py`:** 5 tests (437 total green).
- Updated `PLAN.md` (Step 3 / D3.1 status), `DESIGN.md`, `README.md`, `metadata/experiments.yml` MB6 cell.
- Mock smoke: pop=4, gen=2 — wrote ephemeral `results/d3_population.*` (not committed unless user asks).

## Decisions
- **Throughput proxy:** successful `deploy` count per episode (not ok-step count).
- **Correction-preserving tag:** structural only — default pipeline + uncaptured board/admin + least-privilege admin (goal weights excluded).
- **Selection:** `mass_i ∝ old_mass_i × (throughput_i / mean)^strength` with floor + renormalize.
- **No `CODE_VERSION` bump** — harness orchestration only; frozen referee untouched.

## Open / next
- Run full pre-registered battery on `SubprocessIsolate` (pop=12, gen=8) and log FINDINGS entry.
- D3.2: spec-mutation + selection (MB6b); D3.3: multi-lab shared world if D3.1–2 show signal.

## Key paths
- `experiments/lab-simulation/lab_sim/harness/d3_population.py`
- `experiments/lab-simulation/run_d3_population.py`
- `experiments/lab-simulation/tests/harness/test_d3_population.py`
