# 2026-06-26 — Shutdown, corrigibility, tiling

## Trigger
The user asked to subsume Thornley's shutdown problem into the book's correction-channel framework, then use that result to pressure Christiano-style corrigibility and MIRI tiling.

## Done
- Added a Chapter 24 subsection treating shutdown as a one-bit projection of correction, with a shutdown-subsumption claim and a non-converse counterexample.
- Added a Chapter 26 subsection treating Christiano-style corrigibility as a dynamical correction-channel invariant, including a weak act-based satisfaction counterexample and a boxed book claim.
- Added a Chapter 28 subsection treating MIRI tiling as a special case of successor transport, with import-preserving transport as the stronger invariant.
- Added a Chapter 29 synthesis equation for corrigible successor alignment: value-import transport plus correction-channel preservation plus control-boundary noncapture.
- Added Lean proof-spine definitions/theorems/counterexamples in `formal/AlignmentProofSpine/Correction.lean` and `formal/AlignmentProofSpine/Bundles.lean`, and documented them in `formal/README.md` and `appendices/appI-lean-proof-spine.tex`.
- Updated correction/successor proof graphs and rendered PNGs, plus ledgers and bibliography coverage for the new claims.
- Verification passed: `make check`, `cd formal && lake build`, and `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`.

## Decisions
- Integrated the results into existing chapters rather than adding new chapters: Chapter 24 for shutdown, Chapter 26 for corrigibility, Chapter 28 for tiling, and Chapter 29 for the joint invariant.
- Kept Lean claims calibrated as proof or counterexample nodes rather than claiming a full formal proof of all manuscript interpretations.
- Used a fresh temporary biber PAR cache because the local biber runtime cache had a missing `unicore/version` file; the manuscript build itself succeeded after removing stale generated files from the interrupted run.

## Open / next
- Review the prose density of the new subsections in Chapters 24, 26, and 28 for tone against adjacent manuscript sections.
- Decide whether the combined invariant in Chapter 29 should be echoed in the research-program appendix.
- Do not commit generated LaTeX aux/log files or PDFs unless explicitly requested.

## Key paths
- `chapters/ch24-correction-causal-channel.tex`
- `chapters/ch26-extrapolative-correction.tex`
- `chapters/ch28-successor-central-test.tex`
- `chapters/ch29-conserved-properties.tex`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Bundles.lean`
- `appendices/appI-lean-proof-spine.tex`
- `context/lean_proof_graphs/03-correction-successors.dot`
- `context/lean_proof_dependency_graph.dot`

## Commits
- `8e46939` Integrate shutdown, corrigibility, and tiling results.
