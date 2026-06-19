# 2026-06-19 — Chapter 22 inferring goal transport draft

## Trigger
User provided a full draft for Chapter 22 and asked to integrate it into `chapters/ch22-goal-transport.tex`.

## Done
- Replaced stub with full draft (~18 sections): transport question, scalar vs bundle inference, persistence/transport/reinterpretation, transport hypothesis, bundle equivalents, ontology shift, capability growth, successor creation, self-modeling/transparency, adversarial transport, six-step inference pipeline, five counterexamples, guarantees, philosophical limits, summary.
- Normalized LaTeX (`[...]` display math, `======`, `##`, markdown subscript artifacts, quotes).
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, `\begin{claim}`, `\autocite` + subbibliography.
- Kept repo label `ch:goal-transport` (not draft's `chap:inferring-goal-transport`).
- Unique labels: `eq:value-bundle-geometry-ch22`, `eq:bundle-inference-ch22`, `sec:self-modeling-transparency-ch22`, `sec:counterexamples-edge-cases-ch22`, etc.
- Cross-refs to ch16–ch21, ch08 transport loss, forward to ch23.
- Updated `metadata/book.yml` ch22 status: `stub` → `draft`.
- `./build.sh` succeeds (577 pages).

## Decisions
- Used `claim` environment (defined in preamble; first chapter to use it).
- Cited deblanc2011ontological, everitt2016selfmodification per stub TODO; omitted Hadfield off-switch 2017 and Ramstead 2020 (not in bib).
- christian2018corrigibility for scalable oversight/corrigibility thread.

## Open / next
- ch23 transport types still stub.
- Part IV ch15–ch22 drafted.

## Key paths
- `chapters/ch22-goal-transport.tex`
- `metadata/book.yml`

## Commits
- (none)
