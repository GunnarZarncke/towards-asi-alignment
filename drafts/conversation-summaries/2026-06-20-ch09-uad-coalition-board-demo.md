# 2026-06-20 — Chapter 9 UAD coalition board demo

## Trigger
Build and integrate an interactive UAD coalition posting-board demo under the standard `src/demos/` layout; wire detection from sibling `agency-detect`; add coordinated timesteps, tests, and S/A/I plausibility audit logging.

## Done
- Added `src/demos/ch09-uad-coalition-board/` — FastAPI board with 60s coordinated rounds, single player name per tab, draft auto-save, admin Run UAD / Reset.
- `observation_builder.py` — global round × player matrix, complete-window selection, stable-sum and lagged-sum scorers.
- `coalition_detect.py` — agency-detect MI clustering + stable/lagged-sum coalition discovery; `run_coalition_detection()` with audit logging.
- `coalition_audit.py` — S/A/I/E classification via agency-detect `MarkovBlanketValidator`, plausibility checks, `uad.coalition` logger.
- Extended `src/serve.py` to spawn Python backend demos (`backend.json`); updated `src/README.md`, `src/index.html`, `src/.gitignore`.
- Tests (22): stable-sum 74-team simulation (60 episodes), sum-follower / relay / leader-follower scenarios, audit logs.
- UI: removed internal submission id column from board table.

## Decisions
- **Coordinated global rounds** replace per-player round alignment; UAD uses first window where all included players have full attendance (late joiners excluded).
- **Detection stack:** MI (agency-detect) plus stable-sum and lagged-sum scans; minimal-coalition scoring prefers smaller groups when variance ties.
- **S/A/I audit** uses agency-detect heuristics for plausibility logging only — noted gap vs canonical UAD blanket interface (S/A as env interface, not MI percentiles); full alignment deferred.
- **agency-detect** loaded via sibling path `../agency-detect` or `AGENCY_DETECT_PATH`; not vendored into repo.

## Open / next
- Align role assignment and CMI test with paper blanket (`I(I₊;E₊|I,S,A)`; structural S/A for lagged-sum / relay patterns).
- Optional typed channels (read vs post) on the board for legible S/A/I.
- False-positive stable sums from constant decoy pairs (e.g. D3+D4); consider min coalition size or decoy design in live demos.
- Show audit summary in admin UI (currently server log only).

## Key paths
- `src/demos/ch09-uad-coalition-board/app.py`
- `src/demos/ch09-uad-coalition-board/coalition_detect.py`
- `src/demos/ch09-uad-coalition-board/coalition_audit.py`
- `src/demos/ch09-uad-coalition-board/observation_builder.py`
- `src/demos/ch09-uad-coalition-board/tests/`
- `../agency-detect/agency_detect/`

## Commits
- (this session)
