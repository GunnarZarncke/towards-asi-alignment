# 2026-06-30 — Lean U_S / vector CCI alignment

## Trigger

User asked to bring Lean in line with prose on vector CCI and successor audit, without strengthening the spine beyond that (Option E scraped; no new certificate machinery).

## Done

- Removed separate `SystemUpdateOperatorPreserved` axiom and `SuccessorSafeWitness.systemUpdate` field; successor witness now has seven ch48 fields matching prose.
- Documented that ch46 `U_S` semantics are audited through vector `\vec{CCI}` (`CCICertificate.rawCapacity`, `ontologyTranslation` / `O_trans`) via `CCIPreserved`, not an eighth conjunct.
- Removed `P28_missing_system_update_blocks_successor_safety`; kept `P28_missing_cci_blocks_successor_safety`.
- Updated `Correction.lean` `CCICertificate` doc, `Core.lean` comments, `formal/README.md`, `AlignmentProofSpine.lean`, `context/lean_proof_dependency_graph.dot`.
- Synced `chapters/ch31-conserved-properties.tex` `\leanspine{P28}` and `appendices/appG-lean-proof-spine.tex` (P28 theorem + successor-safe definition).
- Updated `metadata/TODO.md` chapter ↔ Lean gap row for ch46/ch48.

## Decisions

- Kept `SystemUpdateOperator` and `PreservesSystemUpdateOperator` as schematic ch46 notation only; not used in successor witness.
- Did not add new Lean theorems linking `CCIPreserved` to `CCICertificatePasses` (alignment via comments/docs only, per “no strengthening”).

## Open / next

- Optional prose pass: ch46/appK could spell out “deep correction-uptake probes in 𝒬” for successors (discussed but not in this change set).
- Structured `(Θ,Z)` state and finite constructive models remain open in `metadata/TODO.md`.

## Key paths

- `formal/AlignmentProofSpine/Core.lean`
- `formal/AlignmentProofSpine/Successors.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `appendices/appG-lean-proof-spine.tex`
- `chapters/ch31-conserved-properties.tex`

## Commits

- `5ab18c6` Align Lean successor audit with vector CCI prose.
