# 2026-06-30 — Kulveit gradual disempowerment bib + cites

## Trigger
User asked to add Kulveit et al. *Gradual Disempowerment* (arXiv:2501.16946) wherever the manuscript mentions it in prose and at implicit mentions; then to tie it to bearer substitution in ch. 42 and ch. 47 specifically.

## Done
- Added `kulveit2025gradualdisempowerment` to `references/dynamical-systems.bib` and `references/bibliography-summaries.tex` (summary mentions bearer status).
- Regenerated `metadata/global-nocite.tex` (162 keys).
- **Selection / civilizational:** ch. 2, 9, 28, 34, 38; appendices B, F, G (MB6 gradual-disempowerment prose).
- **Bearer / safety-case (canonical homes):** ch. 42 (layer list, moral-language-without-correction, bundle/bearer checks, failure mode); ch. 47 (label≠bearer distinction, counterexample, memorials, signatory/delegation cases).
- Removed scattered bearer-chapter cites from ch. 16, 18, 31, 46 after user narrowed placement to 42 and 47.
- `./build.sh` and `make check` pass.

## Decisions
- Bib key `kulveit2025gradualdisempowerment` (distinct from `kulveit2025pando`).
- Two readings: systemic selection (ch. 2–34, appendices) vs bearer-map substitution (ch. 42, 47).
- Paired with Christiano/Critch where slow structural failure was already grouped.

## Open / next
- Optional: Hendrycks evolutionary-pressure and Ord/MacAskill value lock-in still lack bib keys (2026-06-28 log).
- Unrelated unstaged tweak: `drafts/conversation-summaries/2026-06-30-chapter-appendix-renumbering.md` (commit hash backfill only).

## Key paths
- `references/dynamical-systems.bib`
- `chapters/ch42-safety-case.tex`, `chapters/ch47-bearers-of-value.tex`
- `chapters/ch02-artificial-civilization.tex`, `chapters/ch34-selection-environment.tex`
- `appendices/appB-bridge-crosswalk.tex`, `appendices/appF-research-program.tex`, `appendices/appG-lean-proof-spine.tex`

## Commits
- (this session)
