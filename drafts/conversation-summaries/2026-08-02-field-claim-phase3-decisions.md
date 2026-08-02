# Field-claim Phase 3 bridge decisions

**Date:** 2026-08-02  
**Scope:** Record user decisions on the five Phase 3 open points from `drafts/field-claim-formalization-and-bridge-review-plan.md`. No new Lean theorems; documentation + TODO anchors only. Book/App B/matrix still deferred.

## Context

After Phase 1–2 Lean (finite models, `FieldInterfaces`, MB10 chokepoint reading), options were presented in canvas `phase3-bridge-options.canvas.tsx`. User confirmed dispositions for all five rows.

## Decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Misspec / nonrealizability | **A — ambient MB1/MB9** + defeaters + `EpistemicCoverageEvidence`; document in prose; **no MB12** |
| 2 | Regret ⇒ Safe | **Side channel** — keep `SystemRegretSafetyEvidence` non-consumer; numeric harm leaf later |
| 3 | Logical uncertainty / reflection | **Keep split** — `LobTiling` for reflection; LI exclude-by-reference |
| 4 | Positive path → integrity | **Keep structure** — `PositiveMeasuredPathCertificate`; TODO for CIRIS; try derive before MB4b |
| 5 | MB10 chokepoint interface | **Keep** `ConservedPropertySignatureVerifiable_of_chokepoint`; TODO prove or better type |

## Changes made

- `drafts/field-claim-formalization-and-bridge-review-plan.md` — Phase 3 section → decided table; status updated
- `reference/field-agendas/field-agenda-index.md` — missing-bridge table + Phase 3 prose dispositions
- `metadata/TODO.md` — misspec marked decided; three deferred follow-up items added
- `formal/AlignmentProofSpine/FieldInterfaces.lean` — TODO comments (regret harm leaf, positive path CIRIS)
- `formal/AlignmentProofSpine/Forgeability.lean` — TODO on chokepoint interface axiom
- `drafts/conversation-summaries/HANDOFF.md` — open work updated

## Open / next

- App B / matrix sync when separately authorized
- CIRIS composite counterexample → positive-path derivation or MB4b
- Optional numeric harm leaf if book adopts expected-harm language
- Prove or type `ConservedPropertySignatureVerifiable_of_chokepoint`
- Optional App B/G prose split of MB9 antecedent (editorial)

## Verification

- `lake build` in `formal/` — pass (comment-only `.lean` edits)
- Commit: `4bf8d630`
