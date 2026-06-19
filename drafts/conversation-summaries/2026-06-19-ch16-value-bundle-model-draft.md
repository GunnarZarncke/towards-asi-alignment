# 2026-06-19 — Chapter 16 value-bundle model draft

## Trigger
User provided a full draft for Chapter 16 and asked to integrate it into `chapters/ch16-value-bundle-model.tex`, following the ch15 integration pattern.

## Done
- Replaced stub with full draft (~30 sections): why a value model is needed, basic claim, distinctions (needs/preferences/goals/norms/values), four-part bundle definition, candidate bundle examples, policy geometry, flat-reward failure, sample efficiency, inconsistency, bundle inference, counterfactual tests, cultures, institutions, drift, preservation, failure modes, moral philosophy relation, audit protocol, two worked examples, open questions, summary.
- Normalized LaTeX; used `equation` env for labeled equations (`eq:bundle-compression`, `eq:q-bundle-expansion`, `eq:sample-complexity`, `eq:bundle-inference`).
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, section labels, `\printbibliography` with `\autocite`.
- Cross-reference to Chapter~\ref{ch:values-compressed-control}.
- Renamed duplicate label `sec:value-bundle-preservation` → `sec:bundle-preservation-geometry` (conflicted with ch14).
- Updated `metadata/book.yml` ch16 status: `stub` → `draft`.
- `./build.sh` succeeds (449 pages).

## Decisions
- Folded opening `\section*{Chapter summary}` into `chapterthesis`; kept closing Summary section.
- Did not use draft's manual `thebibliography`; wired existing `.bib` keys only.
- Did not add WWCTV section (not in user draft).

## Open / next
- ch17 low-dimensional value learning still stub.
- Optional bib imports: Haidt, Kahneman, Damasio, Churchland, Sutton & Barto, Menon, Sen 1985.

## Key paths
- `chapters/ch16-value-bundle-model.tex`
- `chapters/ch15-values-compressed-control.tex`
- `chapters/ch17-low-dimensional-value-learning.tex`

## Commits
- (none)
