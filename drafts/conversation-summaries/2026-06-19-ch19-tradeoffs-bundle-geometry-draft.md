# 2026-06-19 — Chapter 19 tradeoffs bundle geometry draft

## Trigger
User provided a full LaTeX draft for Chapter 19 and asked to integrate it into `chapters/ch19-tradeoffs-bundle-geometry.tex`.

## Done
- Replaced stub with full draft (~25 sections): scalar-value critique, bundle triples, tradeoff geometry ($J$, $H$), response geometry $G_B$, bundle interaction examples, Pareto/feasible sets, lexical regions, bundle metrics, contextual weight failure modes, uncertainty/reversibility, ontology shift, substrate transfer, cross-agent invariants, measurement protocols, Goodhart on geometry, toy model, social choice, moral learning as geometry revision, summary.
- Preserved prior stub's paternalism failure pattern in autonomy/non-suffering subsection.
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, section labels, `\printbibliography` with `\autocite`.
- Cross-references to ch16, ch18, ch20.
- Updated `metadata/book.yml` ch19 status: `stub` → `draft`.
- `./build.sh` succeeds (515 pages).

## Decisions
- Draft was already well-formed LaTeX; minimal normalization needed.
- Arrow, Harsanyi, Nussbaum, Sen 1999 omitted (no `.bib` entries); Sen 2009 justice, Rawls, Goodhart/Manheim cited.
- Removed `\addcontentsline` from draft references block; used standard chapter bibliography pattern.

## Open / next
- ch20 reward-to-bundle inference still stub.
- Part IV ch15–ch19 now drafted.

## Key paths
- `chapters/ch19-tradeoffs-bundle-geometry.tex`
- `chapters/ch20-reward-to-bundle-inference.tex`

## Commits
- (none)
