# 2026-06-27 — Grounding viability plan

## Trigger

The user asked for a reviewable plan to integrate a missing foundation layer into the book: the viability of the value-correction grounding relation under optimization pressure.

## Done

- Read the current book structure, instructions, metadata, recent handoff log, formal spine map, and affected chapter/appendix/metadata homes.
- Mapped the existing machinery: boundary discovery, value-bundle modeling, correction-channel integrity, successor transport, attractor basins, safety cases, adversarial verifiability, and Lean bridge assumptions.
- Added `review/grounding-correction-viability-integration-plan-2026-06-27.md`.
- The plan proposes grounding viability as a foundation beneath existing layers, not a new value model.
- Updated the plan after author clarification: grounding viability is now specified as a sixth named Introduction claim, an eighth Chapter 39 safety-case layer, a new assumptions-ledger row, and a new Lean bridge.
- Added a rough manuscript size estimate and symbol-grounding reference targets to the plan.
- No manuscript chapters, formal Lean files, ledgers, or appendices were changed.

## Decisions

- Canonical conceptual home remains Chapter 3 (`ch03-dynamical-guarantee.tex`), with operational homes in Chapter 25, Chapter 39, Chapter 39b, Appendix D, and Appendix G.
- Author decision: grounding viability should become a sixth named Introduction claim.
- Author decision: grounding viability should be an eighth safety-case layer in Chapter 39, with an explicit TODO to review whether the layer list has a completeness argument or is only a pragmatic checklist.
- Recommended using `\mathsf{Unc}_{\alpha}` rather than `U_\alpha` to avoid conflict with `U_H` and `U_S`.
- Author decision: add a new assumptions-ledger row and a new Lean bridge for grounding viability; revisit the `MB*` taxonomy after the larger manuscript integration.
- Author decision: use "grounding viability" after first definition, "grounded correction" where useful in plain language, and frame "capture of grounding" as the master adversarial failure mode.
- Author decision: avoid giving grounding preconditions special moral status; keep them technical validity/capture conditions.
- Symbol-grounding framing to use: "A symbol is grounded when changes in the value-relevant world reliably change the model state, correction signal, or uncertainty state in the right way."

## Open / next

- After approval, execute the integration in phases: frontmatter/ch03/metadata first, value and correction homes second, successor/safety/adversarial chapters third, appendices/formal spine last.
- During implementation, add symbol-grounding references (Harnad 1990; Searle 1980; Taddeo and Floridi 2005; Barsalou 1999; Cangelosi and Harnad 2001; Steels 2008 as appropriate).
- Update claims/assumptions/uncertainty ledgers and regenerate generated appendices during the implementation pass.

## Key paths

- `review/grounding-correction-viability-integration-plan-2026-06-27.md`
- `frontmatter/introduction.tex`
- `frontmatter/executive-overview.tex`
- `chapters/ch03-dynamical-guarantee.tex`
- `chapters/ch26-correction-channel-integrity.tex`
- `chapters/ch42-safety-case.tex`
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`
- `metadata/notation.md`
- `metadata/terminology.md`
- `metadata/claims-ledger.md`
- `metadata/assumptions-ledger.md`
- `metadata/uncertainty-ledger.md`
- `formal/AlignmentProofSpine/Certification.lean`

## Commits

- None.
