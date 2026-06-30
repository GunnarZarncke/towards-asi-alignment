# 2026-06-27 — Grounding viability integration

## Trigger

The user approved the grounding/capture integration plan and asked to execute it. The goal was to make grounding viability a sixth Introduction claim, canonicalize the concept in Chapter 3, propagate it through value-bundle/correction/safety-case chapters, and add metadata plus Lean support.

## Done

- Updated frontmatter: `frontmatter/introduction.tex` now states six claims and adds the grounding claim; `frontmatter/executive-overview.tex` and `frontmatter/preface.tex` now mention grounded correction / six claims.
- Made `chapters/ch03-dynamical-guarantee.tex` the canonical home for grounding viability, conservative abstraction, abstraction-gap exploitation, and the alignment-specific symbol-grounding formulation.
- Added targeted propagation in `chapters/ch16-value-bundle-model.tex`, `chapters/ch21-reward-to-bundle-inference.tex`, `chapters/ch26-correction-channel-integrity.tex`, `chapters/ch42-safety-case.tex`, `chapters/ch43-verifiability-and-ontology-adequacy.tex`, and `chapters/ch48-towards-alignment.tex`.
- Made grounding viability the eighth safety-case layer in ch46 and added a TODO to review whether the layer list has a completeness argument.
- Updated ledgers and metadata: `metadata/terminology.md`, `metadata/notation.md`, `metadata/claims-ledger.md` (`C-004a`), `metadata/assumptions-ledger.md` (`A-014`, `MB9`), `metadata/uncertainty-ledger.md` (`U-16`), `metadata/open-problems.md`, `metadata/TODO.md`, generated `metadata/notation-index.tex`, `metadata/assumptions-index.tex`, and `metadata/global-nocite.tex`.
- Added symbol-grounding references to `references/philosophy.bib`: Harnad, Searle, Taddeo/Floridi, Barsalou, Cangelosi/Harnad, and Steels.
- Updated Lean: `formal/AlignmentProofSpine/Core.lean` now defines `GroundingViable`, `GroundingCertificate`, `ConservativeAbstraction`, `SilentAbstractionGap`, proves `conservative_abstraction_no_silent_gap`, and adds `MB9`; `formal/AlignmentProofSpine/Certification.lean` adds grounding to `LayeredAlignedDef` and bridge-composed certification; `formal/README.md` documents the new bridge/layer.
- Updated public summary surfaces: `README.md` and `tables/assumptions-table.tex`.
- Verification: `lake -d formal build` passed; `make check` passed; full `./build.sh` passed after `./clean.sh` and explicit biber cache setup.
- Follow-up ch46 refinement: split grounding validity from residual ontology translation loss, renamed the residual coordinate to \(O_{\mathrm{trans}}\), made vector/status CCI primary, made \(CCI_\lambda\) the scalar projection, and changed \(C_{\mathrm{raw}}\) from a fixed six-link minimum to a bottleneck-over-certified-traces expression.

## Decisions

- Used `C-004a` for the new grounding claim rather than renumbering later claim IDs.
- Kept grounding preconditions technical: independent evidence, monitor integrity, dissent, exit, and uncertainty escalation are certificate-validity conditions, not a moral catalogue.
- In Lean, real-world grounding validity remains the bridge (`MB9`); the proved contribution is the structural theorem that conservative abstraction rules out silent abstraction gaps.
- In ch46, grounding failure is now an invalidation of `ValidRef`, not a large ontology-mismatch penalty. Ontology/representation mismatch remains only as residual translation loss after grounded correction has reached the system.

## Open / next

- The full PDF build still reports one pre-existing undefined reference: `ch:boundary-expansion` in `chapters/ch44-lethality-stress-test-open-issues.tex`.
- Review ch46's eight-layer safety-case list for completeness. If no completeness argument is available, frame it explicitly as a provisional checklist.
- Future pass: connect grounding certificates to concrete bundle/bearer/CCI measurands rather than only the abstract Lean predicates.
- Future pass: revisit MB taxonomy after broader manuscript integration, as planned.

## Key paths

- `chapters/ch03-dynamical-guarantee.tex`
- `chapters/ch42-safety-case.tex`
- `formal/AlignmentProofSpine/Core.lean`
- `formal/AlignmentProofSpine/Certification.lean`
- `metadata/claims-ledger.md`
- `metadata/assumptions-ledger.md`
- `metadata/uncertainty-ledger.md`
- `review/grounding-correction-viability-integration-plan-2026-06-27.md`

## Commits

- None.
