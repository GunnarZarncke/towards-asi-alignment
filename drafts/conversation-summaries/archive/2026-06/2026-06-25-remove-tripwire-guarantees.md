# 2026-06-25 — Remove Tripwire Guarantees

## Trigger
User asked to remove Tripwire Guarantees as ad-hoc, easily attacked, and lacking explanatory power.

## Done
- Removed ch48 § Tripwire Guarantees (`sec:tripwire-guarantees-ch48`), `\leanspine{proof}{P39}`, safety-case tripwire claim, start-criteria `T_{\text{detect}}` term, and key-definition entry.
- Trimmed tripwire mentions in ch46 and ch48.
- Removed `CertifiedByTripwires` and `P39_tripwire_failure_decertifies` from `Certification.lean`; updated module map in `AlignmentProofSpine.lean` and `formal/README.md`.
- Removed tripwire certification block and P39 lemma from `appendices/appG-lean-proof-spine.tex`.
- Updated `metadata/TODO.md`.
- `lake build` succeeds.

## Decisions
- Deferred draft chapter `drafts/chapter-notes/ch46-tripwires-stop-conditions-deferred.tex` left untouched (already off-spine).
- Did not edit `LeanProofSpineImplementationBrief.md` (stale brief reference to P39 tripwire remains).

## Open / next
- Optional: sync `LeanProofSpineImplementationBrief.md` to drop P39 tripwire node.

## Key paths
- `chapters/ch33-certification-without-construction.tex`
- `formal/AlignmentProofSpine/Certification.lean`
- `appendices/appG-lean-proof-spine.tex`

## Commits
- `c4725b6` Refine fitness and proof-spine diagrams for the book appendix.
