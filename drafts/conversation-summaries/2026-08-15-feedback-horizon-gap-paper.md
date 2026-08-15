# 2026-08-15 — Feedback horizon gap paper structure

## Trigger
Convert standalone `papers/feedback_horizon_gap.tex` into the standard spin-out paper layout used by `papers/et4-secret-loyalties/` (dedicated folder, build script, external bibliography).

## Done
- Moved paper to `papers/feedback-horizon-gap/` with `feedback-horizon-gap.tex`, `feedback-horizon-gap.bib` (20 entries), and `build.sh` (pdflatex → biber → pdflatex ×2).
- Replaced inline `\begin{thebibliography}` with biblatex authoryear; citations use `\parencite`.
- Built frozen PDF `papers/feedback-horizon-gap/feedback-horizon-gap.pdf` (11 pages).
- Updated `papers/README.md` index row.
- Deleted root-level `papers/feedback_horizon_gap.tex`.

## Decisions
- Used biblatex + external `.bib` (et4 neighbor uses inline bib; this paper's citation count justified external bib).
- Authoryear citation style (not numeric) to match manuscript repo convention.

## Open / next
- Optional: switch to `style=numeric` if author prefers bracket citations.
- Table 1 still triggers float-too-large warning (~128pt over); layout pass if publishing.

## Key paths
- `papers/feedback-horizon-gap/feedback-horizon-gap.tex`
- `papers/feedback-horizon-gap/feedback-horizon-gap.bib`
- `papers/feedback-horizon-gap/build.sh`

## Commits
- (this session)
