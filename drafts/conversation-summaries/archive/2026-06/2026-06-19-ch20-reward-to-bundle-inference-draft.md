# 2026-06-19 — Chapter 20 reward-to-bundle inference draft

## Trigger
User provided a full draft for Chapter 20 and asked to integrate it into `chapters/ch21-reward-to-bundle-inference.tex`.

## Done
- Replaced stub with full draft (~25 sections): IRL critique, three scalar-reward failures, bundle inference $(B,W,\Phi)$, generative model, counterfactual tests, response geometry, bundle equivalence, sample complexity, approval vs bundle, distribution shift, bearer import, learning sketch (7 steps), degenerate models, deception, institutions, two worked examples, success criteria, shaky assumptions, summary.
- Normalized LaTeX (`======`, `##`, markdown artifacts, broken success-criterion block).
- Used unique label `sec:example-helpful-lie-ch46` (avoids duplicate `sec:example-helpful-assistant` in ch07/ch14).
- Matched book conventions; cross-refs to ch16–ch19, ch46.
- Updated `metadata/book.yml` ch46 status: `stub` → `draft`.
- `./build.sh` succeeds (538 pages).

## Decisions
- Forward reference to ch46 goal transport (draft closing paragraph).
- Parr 2022 active inference cited via `parr2022_active`; casper2023rlhflimits for RLHF limits.

## Open / next
- ch46 compression test intention still stub.
- Part IV ch15–ch46 drafted.

## Key paths
- `chapters/ch21-reward-to-bundle-inference.tex`
- `chapters/ch23-goal-transport.tex`

## Commits
- (none)
