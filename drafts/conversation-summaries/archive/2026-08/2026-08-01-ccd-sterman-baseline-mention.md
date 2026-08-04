# 2026-08-01 — CCD and Sterman baseline mentions

## Trigger
User asked to consider cyclic causal discovery (CCD; Zanga et al. survey arXiv:2305.10032) as a plausible passive baseline for agent discovery, and Sterman (*Business Dynamics*) for systems-dynamics / causal-loop vocabulary.

## Done
- Assessed fit: CCD appropriate only as passive cyclic-coupling baseline among fixed observables, not full UAD.
- Added bib entries `richardson1996ccd`, `zanga2025causaldiscoverysurvey`, `sterman2000businessdynamics` + `\bibsummary` lines.
- **Ch. 2:** Sterman cite when introducing civilizational control loops (CLDs / stock-flow as human-built maps).
- **Ch. 7:** Paragraph contrasting Sterman CLDs vs CCD; scope limits vs intervention-based discovery; updated Chapter References.
- **Ch. 34:** Short cross-ref at selection turn (institutional feedback loops).
- `python3 scripts/check_bibliography_summaries.py` passes (437/437).

## Decisions
- No CCD experiment implementation this pass (risk of straw-man without trace→variable pipeline).
- Sterman in three chapters with distinct roles (Ch. 2 canonical, Ch. 7 contrast, Ch. 34 short ref); skip Ch. 37/41.

## Open / next
- Optional: run full `./build.sh` if PDF cite resolution needs visual check.
- Pre-existing `make check` failure: missing `kwon2026` in `papers/et4-secret-loyalties/` (unrelated).

## Key paths
- `chapters/ch07-finding-boundary.tex` (~583–592, §estimator-feasibility)
- `chapters/ch02-artificial-civilization.tex` (~38)
- `chapters/ch34-selection-environment.tex` (~40)
- `references/dynamical-systems.bib`

## Commits
- `ff380cfe` Cite CCD and Sterman as calibrated passive baselines for feedback structure.
