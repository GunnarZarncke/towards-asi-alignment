# 2026-06-19 — Chapter 17 low-dimensional value learning draft

## Trigger
User provided a full draft for Chapter 17 and asked to integrate it into `chapters/ch17-low-dimensional-value-learning.tex`.

## Done
- Replaced stub with full draft (~20 sections): problem statement, simple vs low-dimensional values, flat reward model, bottleneck model, sample complexity, evolutionary argument, bundle control variables, rank of value, local vs global low rank, bearer problem preview, sparse AI directions, compression risks, residuals, learnability-to-alignment gaps, formal model, empirical signatures, failure modes, superintelligence relevance, summary.
- Normalized LaTeX; labeled equation `eq:sample-complexity-ch17`.
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, section labels, `\printbibliography` with `\autocite`.
- Cross-references to ch15, ch16, ch18.
- Updated `metadata/book.yml` ch17 status: `stub` → `draft`.
- `./build.sh` succeeds (466 pages).

## Decisions
- Bai et al. Constitutional AI not cited (no `.bib` entry); christiano2017 covers RLHF preference-learning thread.
- Did not add WWCTV section (not in user draft).

## Open / next
- ch18 bearer maps still stub; ch17 closing points there explicitly.
- Optional bib: Bai Constitutional AI, strouse/kolchinsky IB variants per source-canon TODO.

## Key paths
- `chapters/ch17-low-dimensional-value-learning.tex`
- `chapters/ch18-bearer-maps.tex`
- `chapters/ch16-value-bundle-model.tex`

## Commits
- (none)
