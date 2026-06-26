# 2026-06-26 — Alignment work subsumption pass

## Trigger
The user asked to add "subsumption + break" comparisons against more existing alignment work: Orseau--Armstrong safe interruptibility, AUP / relative reachability, CIRL, CIDs, debate, iterated amplification / recursive reward modeling, ELK, and quantilizers; also to update Lean proofs, Appendix I, Appendix H, and the proof diagrams.

## Done
- Added compact manuscript integrations:
  - Chapter 24: safe interruptibility as a one-bit correction projection weaker than broad correction-channel preservation.
  - Chapter 25: AUP / relative reachability / low impact and quantilization as separable from CCI / trajectory correction preservation.
  - Chapter 4 and Chapter 20: CIRL / cooperative reward inference as weaker than value-bundle and update-process preservation.
  - Chapter 7: Causal influence diagram incentives as variable-ontology / abstraction-boundary relative.
  - Chapter 27: debate as vulnerable to judge-state / correction-channel capture.
  - Chapter 38: amplification and recursive reward modeling as requiring correction-channel contraction across decomposition levels.
  - Chapter 39b: ELK as latent readout, not correction uptake or successor preservation.
- Added Lean finite separation nodes in:
  - `formal/AlignmentProofSpine/Correction.lean`
  - `formal/AlignmentProofSpine/Bundles.lean`
  - `formal/AlignmentProofSpine/Boundaries.lean`
- Updated `formal/README.md`, Appendix I theorem inventory / captions, Appendix H research-program hooks, and the Lean proof graph DOT sources plus rendered PNGs.
- Added NEW / SUBSUMED status markers to the Lean proof diagrams and Appendix I legend: NEW marks the recent literature-separation nodes; SUBSUMED marks existing nodes that embed or project external proposals into stronger book invariants.
- Added citation entries for the nine external works in `references/manuscript-citations.bib`; verified they remained present after the parallel bibliography update.
- Fixed `book.tex` load order so `metadata/preamble.tex` is loaded after `biblatex`, allowing the bibliography formatting macros in the preamble to be defined.
- Verification passed: `lake -d formal build`, `make check`, `./scripts/render_lean_graphs.sh`, `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`, and lints on edited files.

## Decisions
- Kept each comparison short and placed it in the chapter where the book already has the relevant invariant: CCI for impact/quantilization, value bundles for CIRL, boundary discovery for CIDs, manipulation for debate, multiscale decomposition for amplification, and verifiability for ELK.
- Lean additions are calibrated as finite toy counterexamples / separations, not empirical proofs that deployed systems satisfy the relevant conditions.
- Did not revert or stage parallel bibliography-summary changes (`AGENTS.md`, `metadata/preamble.tex`, `references/bibliography-summaries.tex`, and the bibliography summary log).

## Open / next
- Review prose density of the new subsections for tone against surrounding chapters.
- Decide later whether any of these separations deserve claim-ledger entries; this pass kept ledgers unchanged because the claims are localized extensions of existing invariants.

## Key paths
- `chapters/ch24-correction-causal-channel.tex`
- `chapters/ch25-correction-channel-integrity.tex`
- `chapters/ch20-reward-to-bundle-inference.tex`
- `chapters/ch07-finding-boundary.tex`
- `chapters/ch27-manipulation-false-consent.tex`
- `chapters/ch38-multiscale-decomposition.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Bundles.lean`
- `formal/AlignmentProofSpine/Boundaries.lean`
- `appendices/appI-lean-proof-spine.tex`
- `appendices/appH-research-program.tex`
- `context/lean_proof_dependency_graph.dot`
- `context/lean_proof_graphs/01-boundary-measurement.dot`
- `context/lean_proof_graphs/02-value-transport.dot`
- `context/lean_proof_graphs/03-correction-successors.dot`

## Commits
- None.
