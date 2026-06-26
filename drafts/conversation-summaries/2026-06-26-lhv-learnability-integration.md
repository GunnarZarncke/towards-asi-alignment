# 2026-06-26 — LHV learnability integration

## Trigger
The user asked to integrate a stronger value-learning argument: attack the strong claim that values are arbitrary/high-dimensional, keep the defensible underidentification claim, connect the result to the Loop--Hub--Value model, update Lean/appendices/diagrams, and add small experiments under `src/demos/`.

## Done
- Follow-up: added a dedicated explanatory bridge in Chapter 15, Section `sec:lhcv-model-ch15`, for the Loop--Hub--Control--Value model from the brain-to-values sibling project.
- The new Chapter 15 material explains \(L\to H\to C\leadsto V\): free-energy / prediction-error loops, hub bottlenecks, control-relevance proxies, and mediated value readouts. It includes compact equations for loop-to-hub compression, hub-to-control policy modulation, and control-to-value readout.
- Included the LHV illustration in Chapter 15 as `figures/lhv/hub-centric-brain-value-map.png`, rendered directly from sibling source `../brain-to-values/viz/brain_values/output/brain_values.svg` with `rsvg-convert`.
- Strengthened frontmatter claims in `frontmatter/executive-overview.tex` and `frontmatter/introduction.tex`: the book now more confidently rejects the strong claim that values are arbitrary/unlearnable, while preserving the weaker claim that full values are not identifiable from sparse behavior under ontology shift.
- Calibrated the neuroscience claim with examples (PAG/protection, VTA/learning, LC/vigilance, hypothalamic/care, insula/ACC/fairness/justice, septal/loyalty) as hypothesis generators, not one-to-one value dictionaries.
- Updated Chapter 17 and Chapter 20 to cross-reference the Chapter 15 LHCV section; Chapter 20 now distinguishes hub signals/control proxies from value-bundle readouts and fixes the LHV error-bound noise term.
- Added the strong-vs-defensible value-learning split to Chapter 17, including the Fano-style lower bound \(I(Y;E(X)) \geq H(Y)-h_2(p_e)\), empirical plausibility hooks, and a minimal synthetic-results paragraph.
- Added an LHV-constrained sample-complexity refinement to Chapter 20: arbitrary flat rewards remain hard in ambient dimension \(D\), while bundle-response geometry can be tractable in \(K\ll n\ll D\).
- Added Lean proof-spine node `P16_lhv_sample_window_separates_flat_reward_learning` in `formal/AlignmentProofSpine/Bundles.lean`, plus README and Appendix I documentation.
- Updated Appendix H research-program hooks for response-matrix rank, effective dimension, parallel analysis, embedding recoverability, and ontology/bearer-shift failure modes.
- Updated proof graph DOT sources and regenerated `context/lean_proof_dependency_graph.png` and `figures/lean_proof/02-value-transport.png`.
- Added `src/demos/ch17-lhv-learnability/`, a deterministic synthetic demo with PCA/parallel analysis, raw-vs-LHV-vs-oracle probes, tests, built JS, and README; wired it into `src/index.html` and `src/README.md`.
- Added bibliography entries for Moral Foundations, Schwartz values, ETHICS, and Moral Machine; regenerated `metadata/global-nocite.tex`.

## Decisions
- Use `LHCV` when the control-proxy layer matters and allow `LHV` only as a shortened form when the control layer is implicit.
- Keep the strongest claim architectural: hubs shape control relevance; cultures and persons read some of that relevance as values. Do not say a hub directly stores a moral label.
- Prefer the sibling SVG source for the LHV illustration; ImageMagick rendered the source SVG poorly, while `rsvg-convert` preserved the layout.
- Frontmatter confidence is now stronger only for fixed-ontology structured learnability and the non-arbitrariness of value judgments; bearer import, correction preservation, ontology shift, and successor transport remain open load-bearing problems.
- Kept the claim calibrated: above-chance prediction refutes "values are unlearnably arbitrary" on a tested distribution, but does not prove full alignment, bearer import, or safe ontology-shift identification.
- Treated Lean `P16` as a small arithmetic proof-spine node for the sample-window shape, not as a theorem about human data.
- Kept the synthetic result in the manuscript as a minimal toy result with no reference to implementation code.
- Removed generated `src/package-lock.json` and `.biber-par-cache/`; `node_modules/` remains ignored.

## Open / next
- Consider whether the response-matrix experiment should become a real analysis script later, using ETHICS, Moral Machine, MFQ/MFQ-2, Schwartz PVQ, or ESS values data.
- If the book later gains a demo index in the PDF, decide whether to reference `src/demos/ch17-lhv-learnability/`; current `src/README.md` says demos are not wired into the PDF.
- Review prose density in Chapter 17 after adjacent low-dimensionality edits settle.

## Key paths
- `chapters/ch15-values-compressed-control.tex`
- `figures/lhv/hub-centric-brain-value-map.png`
- `frontmatter/executive-overview.tex`
- `frontmatter/introduction.tex`
- `chapters/ch17-low-dimensional-value-learning.tex`
- `chapters/ch20-reward-to-bundle-inference.tex`
- `formal/AlignmentProofSpine/Bundles.lean`
- `appendices/appH-research-program.tex`
- `appendices/appI-lean-proof-spine.tex`
- `context/lean_proof_graphs/02-value-transport.dot`
- `context/lean_proof_dependency_graph.dot`
- `src/demos/ch17-lhv-learnability/`

## Verification
- Follow-up verification after LHCV explanation: `make check`, full PDF build with `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`, ReadLints on `ch15`/`ch17`/`ch20`.
- Figure verification: source SVG rendered with `rsvg-convert`; full PDF build succeeded after including `figures/lhv/hub-centric-brain-value-map.png`.
- Frontmatter verification: `make check`, ReadLints on frontmatter files, full PDF build with `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`.
- `cd formal && lake build`
- `cd src && npm install && npm run build && npm test`
- `./scripts/render_lean_graphs.sh`
- `make check`
- `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh` after `./clean.sh` and cache recreation
- ReadLints on edited chapter/demo/Lean files: no linter errors

## Commits
- None.
