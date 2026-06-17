# 2026-06-18 — Chapter 10 strategic opacity draft

## Trigger
User provided a full draft for Chapter 10 (Agency Under Strategic Opacity) and asked to integrate it into `ch10-strategic-opacity.tex`.

## Done
- Replaced stub chapter with integrated draft: epigraph, chapter thesis, 18 sections (including subsections), adversarial tests, examples, decision triggers, summary.
- Converted draft notation to LaTeX: `I(` → `\MI`, fixed align block, markdown subscript artifacts, quote typos.
- Wrapped chapter in `\begin{refsection}` / `\printbibliography`; replaced `\citep` with `\autocite`.
- Kept label `ch:strategic-opacity` (draft had `chap:agency-under-strategic-opacity`).
- Added BibTeX entries: `demski2019embedded`, `goodfellow2015explaining`, `park2024deception`; mapped other refs to existing keys (`critch2020ai`, `ng2000irl`, etc.).
- `./build.sh` succeeds (303 pages).

## Decisions
- Kept the draft's section structure rather than the scaffold template.
- Equation labels use `-ch10` suffix where draft had `-ch9`.

## Open / next
- Part II (Ch. 6–10) now drafted; Ch. 5 remains stub in Part I.
- Later polish: cross-link to `ch37-goal-laundering.tex` when that chapter is drafted.

## Key paths
- `chapters/ch10-strategic-opacity.tex`
- `references/external-alignment.bib`

## Commits
- (none)
