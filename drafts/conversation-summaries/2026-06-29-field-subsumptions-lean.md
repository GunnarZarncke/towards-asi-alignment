# 2026-06-29 — Field subsumptions in Lean

> **Superseded by** [2026-06-29-lean-field-subsumptions-checkpoint.md](2026-06-29-lean-field-subsumptions-checkpoint.md) (intermediate checkpoint; session ongoing).

## Trigger
User feedback asked whether the book's field-agenda subsumption claims (CIRL, shutdown, corrigibility, ELK, debate, low impact/quantilization) can be implemented in Lean beyond prose re-description.

## Done
- Added `formal/AlignmentProofSpine/FieldSubsumptions.lean`:
  - `FieldProjection`, `SubsumedForward`, `SeparatedFrom` vocabulary
  - Finite-profile subsumption + separation for all eight crosswalk agendas
  - Pure proof: `cirl_subsumption_forward` (full transport → semantic/CIRL layer)
  - Pure separations on structured profiles (ELK, debate, impact, shutdown, interrupt)
  - System-level re-exports: shutdown subsumption, Christiano via `MB4`
  - Legacy links to existing `Toy*` counterexample theorems in `Correction.lean` / `Bundles.lean`
- Imported module in `AlignmentProofSpine.lean`; updated `formal/README.md`
- Verified `lake build`; `#print axioms` shows finite subsumptions are axiom-free

## Decisions
- Subsumption = proved forward implication + proved non-converse separation, not a formal reduction of external programs into book axioms.
- Finite profiles use explicit witness structures (`ELKProfile`, `DebateProfile`, etc.) instead of `abbrev ... := True` toy predicates.
- System-level subsumptions (`CorrectionIntegrity → ...`) remain bridge-assisted where they must; finite-layer proofs are the honest "earned" part.

## Open / next
- Wire `FieldSubsumptions` into Appendix I and lean proof graphs (optional).
- Strengthen finite models toward manuscript semantics (e.g. policy profiles for CIRL, handle lists for shutdown).
- Manuscript prose could cite `#print axioms` distinction: what's pure vs bridge-dependent.

## Key paths
- `formal/AlignmentProofSpine/FieldSubsumptions.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Bundles.lean`
- `appendices/appBridge-crosswalk.tex`

## Commits
- None.
