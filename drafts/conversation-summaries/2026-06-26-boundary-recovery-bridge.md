# 2026-06-26 — Boundary recovery bridge

## Trigger
The user provided reviewer feedback that Chapter 7's boundary-discovery criterion looked circular and under-supported: Eq. 7.1 defined a Markov-blanket target, while Appendix I treated that definition as support for estimator soundness. The user asked for concrete edits using two angles: human intervention-based agent detection and empirical progress from the agency-detect experiments, while fixing the appearance of circular argument.

## Done
- Added Chapter 7 Section `Estimator Feasibility and Recovery`, separating the boundary target from finite-data recovery.
- Stated that naive high-dimensional conditional-MI estimation and unrestricted role search are not the claim; recovery requires structured candidate classes, coarse-graining, intervention handles, sufficient margin, and empirical recovery evidence.
- Added the human-detection bridge: humans infer agency by prodding, blocking, surprising, removing tools, varying incentives, and watching what keeps steering.
- Added an internal empirical bridge to companion agent-discovery experiments without reintroducing direct `zarncke2026access` / `zarncke2026smoothing` manuscript citations, per the earlier UAD-citation-removal decision.
- Updated Chapter 7 WWCTV and summary so feasibility failure and estimator/recovery separation are explicit.
- Calibrated Chapter 10 adversarial tests: they operationalize evidence only when the evaluator has handles the system cannot cheaply route around; otherwise they return weak evidence, not certification.
- Updated Appendix I MB1 so Eq. 7.1 is described as the boundary target, not the estimator-soundness support. MB1 now points to the Chapter 7 recovery bridge.
- Updated `metadata/claims-ledger.md`, `metadata/assumptions-ledger.md`, and `metadata/uncertainty-ledger.md` so C-003/A-004/U-05 carry the finite-data recovery condition.
- Verification: `ReadLints` reported no linter errors on edited files; `make check` passed; `./build.sh` passed.
- Follow-up refinement: added the detector-target caveat for MB1. Learned detectors can scale or amortize evaluation, but if trained to predict Eq. 7.1 they inherit the criterion's soundness gap; if trained on labeled agents they import the ontology the method was meant to discover. Chapter 7 now frames generator--detector training as evidence, not closure, and Chapter 10 names the fixed-detector Goodhart risk. Appendix I and the ledgers now carry this caveat.
- Follow-up verification: `ReadLints` clean; `make check` passed; `./build.sh` passed.
- Research-program follow-up: updated Appendix H's MB1 research-program item and Chapter 7 disconfirmation index so detector-target soundness is explicitly part of the validation/falsification program.
- Research-program verification: `ReadLints` clean for Appendix H; `make check` passed; `./build.sh` passed.

## Decisions
- Kept the fix as a feasibility bridge rather than a proof: the manuscript now concedes that boundary recovery can fail when the candidate class is too large, observation distortion collapses the margin, or adversarial presentation steers the residual.
- Did not cite the 2026 companion UAD papers directly in `.tex`; the substance is explained in book terms because the user previously asked not to cite those internal papers in manuscript prose.
- Did not commit; the user asked for implementation only, and the working tree already contains many unrelated/pre-existing changes.

## Open / next
- If desired, add a small figure or table contrasting target/estimator/recovery/evidence for Chapter 7, but the core logical repair is now in prose.
- A later pass could scan other references to "boundary estimator soundness" to make sure no other appendix or chapter treats a definition as evidence.

## Key paths
- `chapters/ch07-finding-boundary.tex`
- `chapters/ch10-strategic-opacity.tex`
- `appendices/appI-lean-proof-spine.tex`
- `metadata/claims-ledger.md`
- `metadata/assumptions-ledger.md`
- `metadata/uncertainty-ledger.md`

## Commits
- `bf237cd` Add boundary recovery bridge.
