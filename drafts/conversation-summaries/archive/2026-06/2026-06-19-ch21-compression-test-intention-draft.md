# 2026-06-19 — Chapter 21 compression test for intention draft

## Trigger
User provided a full draft for Chapter 21 and asked to integrate it into `chapters/ch22-compression-test-intention.tex`.

## Done
- Replaced stub with full draft (~22 sections): intentional compression gain, latent mechanistic vs intentional models, description-length test, three-way comparison, counterfactual robustness, scalar-to-bundle upgrade, response geometry, bearer maps, correction as intention, five levels of intentional compression, over/under-attribution, adversarial compression, self-modelling, two worked examples (helpfulness, frontier lab), calibration, decision triggers, limits, summary.
- Normalized LaTeX (`======`, `##`, backtick quotes, inline math).
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, `\autocite` + subbibliography.
- Kept repo label `ch:compression-test-intention` (not draft's `ch:compression-test-for-intention`).
- Unique labels to avoid collisions: `eq:bundle-inference-ch46`, `eq:bundle-policy-ch46`, `eq:value-bundle-geometry-ch46`, `eq:bearer-preservation-ch46`, `eq:correction-chain-ch46`, `eq:correction-capacity-ch46`, `sec:philosophical-limit-ch46`, `sec:example-helpfulness-ch46`, `sec:goal-laundering-ch46`.
- Cross-refs to ch16–ch46, ch46 goal transport.
- Updated `metadata/book.yml` ch46 status: `stub` → `draft`.
- `./build.sh` succeeds (559 pages).

## Decisions
- Omitted Hamilton 1964 (not in bib); cited available IRL, Dennett, Tishby, Friston/Markov blanket, CEV, Conant–Ashby keys.
- Forward reference to ch46 in summary closing.

## Open / next
- ch46 goal transport still stub.
- Part IV ch15–ch46 drafted.

## Key paths
- `chapters/ch22-compression-test-intention.tex`
- `metadata/book.yml`

## Commits
- (none)
