# Session: Consciousness TSA Phase 5 — Lean + MB3 card

**Date:** 2026-08-17

## Goal

Close Phase 5: type conservative exclusion without adding MB3a or consciousness axioms; update MB3 card and App B/G.

## Shipped

### Lean (`Bundles.lean`)
- `ConservativeExclusion` — one-sided certificate soundness
- `conservative_exclusion_licenses_exclusion`
- `conservative_exclusion_one_sided` (bearer ⇒ ¬cert)
- Finite toy: success excludes; failure on bearer abstains; sound ≠ complete
- **Not** wired into `MB3Crux` / `BridgeAssumptions`
- Comment on `MB3Crux` in `BridgeCruxes.lean`
- Defeater vocabulary: `BearerAdmissionMisclassified` (U-17; distinct from `BearerMapSpoofed`)

### Prose / cards / apps
- MB3 concept card: admission + transport split; leanNodes for CE + defeater
- ch18 `{leanbox}` at conservative exclusion
- App B MB2/MB3 paragraph: admission neighborhood
- App G MB3 assumption + defeater signal list
- Ledgers: assumptions MB3 Lean line; U-17 Lean pointers

## Verification

- `lake build` — pass
- `npm run sync:concepts` — pass

## Explicit non-claims

- Lean does not prove any process is non-conscious.
- Admission remains open (U-17); only the epistemic shape of one-sided certificates is typed.
