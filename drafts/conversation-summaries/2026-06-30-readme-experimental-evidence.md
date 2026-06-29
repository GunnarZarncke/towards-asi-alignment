# 2026-06-30 — README experimental evidence section

## Trigger
User asked to add a section to the top `README.md` on current tentative experimental evidence from (a) the included toy simulation and (b) the sibling `agency-detect` repo.

## Done
- Added **Tentative experimental evidence** section to `README.md` after Manuscript status.
- Covers toy-simulation: instrumentation curve, MB1–MB9 coverage (gaps noted), red-team false-pass rates, honest-handle caveat.
- Covers agency-detect: UAD core, E0–E8 decoys, spotlight, handle-UAD, intention/outcome lines, worm cohort; links to sibling docs and `context/` mirrors.

## Decisions
- Placed section after Manuscript status (status-adjacent, visible early).
- Explicit claim-strength disclaimer: illustrative only, not thesis validation.
- Did not edit manuscript appendices yet (user scoped to README only).

## Open / next
- Optional: mirror condensed version in `appendices/appH-research-program.tex` when user lifts experiments→manuscript boundary.
- Optional: add `experiments/` to repository map in README.

## Key paths
- `README.md` — new section
- `experiments/toy-simulation/TODO.md`, `experiments/toy-simulation/results/`
- `../agency-detect/docs/EXPERIMENTS.md`, `../agency-detect/docs/FINDINGS.md`

## Commits
- (none — user did not request commit)
