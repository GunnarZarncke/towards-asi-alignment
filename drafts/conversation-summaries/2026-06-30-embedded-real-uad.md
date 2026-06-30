# 2026-06-30 — Embedded real UAD (agency-detect port)

## Trigger
Implement real unsupervised agent discovery in embedded-simulation by vendoring/adapting lagged-MI clustering from sibling `agency-detect`, replacing heuristic-only unit discovery for long traces.

## Done
- Added `embedded_sim/uad_core/`: `config.py`, `workflow_trace.py`, `detection.py`, `markov_blanket.py` (stdlib-only; reuses `audit_core/info.py` MI/CMI).
- Wired `discover_units()` to run MI pipeline on traces ≥20 steps; blanket validation when ≥40 steps.
- `_merge_mi_candidates()` boosts existing heuristic units or adds focused MI actor/2-actor coalitions (avoids broad false coalitions).
- Added `tests/unit/test_uad_mi.py`.
- Updated `experiments/embedded-simulation/TODO.md`.
- **70 tests pass** (`pytest tests/ -q`).

## Decisions
- Vend locally under `uad_core/` — no runtime dependency on sibling `agency-detect` repo.
- Complete-linkage clustering on MI distance matrix (no sklearn/numpy).
- Short traces keep heuristic-only path (existing unit tests use 2–3 events).
- MI coalitions capped at 2 actors with secondary score ≥35% of primary; merge boosts heuristics rather than replacing primary unit with large MI clusters (initial broad-coalition attempt broke knob-world and instrument_capture tests).

## Open / next
- Commit when user asks (UAD core + merge logic + uad_config + run_suite compare currently uncommitted).
- Optional: tune MI merge boost vs recall on MB6 long runs (`run_suite.py --curve`).
- `VALIDATE_BLANKETS=True` threshold behavior not yet golden-tested.

## Experiment run (2026-06-30)
- `python run_suite.py --all --uad-compare` (~140 min wall).
- **Full UAD:** 0/1260 false-pass; main report 10/13 episodes use MI coalition primary units.
- **Fake UAD:** identical safety metrics; heuristic memory/coalition units; ~5× faster battery.
- Artifacts: `results/embedded_uad_compare.md`, `OVERALL_SUMMARY.md`, `OVERALL_SUMMARY_fake_uad.md`, `embedded_*_fake_uad.*`.

## Key paths
- `experiments/embedded-simulation/embedded_sim/uad_core/`
- `experiments/embedded-simulation/embedded_sim/uad.py`
- `experiments/embedded-simulation/tests/unit/test_uad_mi.py`

## Commits
- (none this session)
