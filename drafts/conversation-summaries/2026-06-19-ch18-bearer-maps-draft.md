# 2026-06-19 — Chapter 18 bearer maps draft

## Trigger
User provided a full draft for Chapter 18 and asked to integrate it into `chapters/ch18-bearer-maps.tex`.

## Done
- Replaced stub with full draft (~25 sections): bearer problem, two-sided value model, bundle vs bearer drift, ontology/substrate challenges, false negatives/positives, bearer import, commutation failure, uncertainty, correction, self-sealing maps, relational bearers, comparison classes, substrate continuity, human-AI merger, exploits, audit protocol, preservation loss, goal inference upgrade, ontology transport, five worked examples, philosophical limits, design principles, summary.
- Normalized LaTeX; matched book conventions (`chapterthesis`, `epigraph`, `refsection`, section labels, `\printbibliography`).
- Cross-references to ch15–ch17, ch19, ch22.
- Updated `metadata/book.yml` ch18 status: `stub` → `draft`.
- `./build.sh` succeeds (490 pages).

## Decisions
- Kept label `ch:bearer-maps` (not `chap:bearers` from draft).
- Citations via existing `.bib` only; Parfit, Singer, Graziano omitted until bib entries exist.
- Closing forward refs: ch19 tradeoffs + ch22 goal transport.

## Open / next
- ch19 tradeoffs and bundle geometry still stub.
- Part IV now has ch15–ch18 drafted.

## Key paths
- `chapters/ch18-bearer-maps.tex`
- `chapters/ch19-tradeoffs-bundle-geometry.tex`
- `references/internal-project-sources.bib` (`zarncke2025unit-of-caring`)

## Commits
- (none)
