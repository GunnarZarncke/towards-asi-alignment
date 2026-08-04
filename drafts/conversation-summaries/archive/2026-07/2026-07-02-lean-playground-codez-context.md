# 2026-07-02 — Lean playground codez context and size limits

## Trigger
User asked that “Try out” Lean proof links include all needed context and respect `codez` URL size limitations.

## Done
- Extended `site/scripts/lib/lean4web-url.mjs`: `buildLean4WebUrl` with round-trip check, conservative (1800) and max (8000) limits, `#url=` GitHub raw fallback when `codez` exceeds max.
- Updated `site/scripts/sync-lean-spine.mjs`: validates playgrounds at sync time; stores `liveEncoding`, `codeLength`, `liveUrlLength`; warns/fails on limit breaches.
- Enriched `formal/playgrounds/P01-basin-invariant.lean`: spine mapping, `BasinStable`, axiom footprint notes.
- Aligned `formal/playgrounds/P15-bundle-geometry.lean` with spine `Bundles.lean` (full `sameBundleGeometry`, `Int` salience, spine counterexample profiles).
- Updated `formal/playgrounds/README.md` and `LeanTryIt.astro` copy.
- Re-ran `npm run sync:lean-spine` — P01 codez 1438 chars, P15 codez 1942 chars (conservative warning only).

## Decisions
- Prefer inline `#codez=` whenever it fits under 8000 chars (works pre-push); use `#url=` only when `codez` exceeds max.
- Conservative 1800-char warning matches practical share-link limits; does not block sync.

## Open / next
- Add playgrounds for more high-traffic spine nodes if desired.
- Spot-check generated URLs in Lean 4 Web browser (P15 at 1942 chars).

## Key paths
- `site/scripts/lib/lean4web-url.mjs`
- `site/scripts/sync-lean-spine.mjs`
- `formal/playgrounds/*.lean`

## Commits
- (none — user did not request commit)
