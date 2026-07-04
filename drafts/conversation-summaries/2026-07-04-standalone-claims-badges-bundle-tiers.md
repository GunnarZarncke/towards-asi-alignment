# Session: standalone claims, badge index, bundle catalogue

**Date:** 2026-07-04  
**Trigger:** User follow-up after manuscript hygiene pass — bundle Learning/Loyalty handling; fix stale appendix letters; extract publishable notes; authorship hygiene; clickable badge pages.

## Done

1. **Bundle catalogue:** Nine bundles canonical; **Truth** and **Legacy** are coordinate names in \(B_t\). **Learning** and **loyalty** are footnoted alternative labels (ch15/ch16), not separate axes or promotion tiers. ch03/ch31 aligned. User rejected the interim two-tier promotion-criteria model as cumbersome.

2. **Stale appendix letters:** Fixed `metadata/TODO.md` appendices follow-through (A–G built; H–K stubs; appL unwired). Fixed BIG REVIEW and logical-induction pointers (`appH` → **appF** for research program).

3. **Standalone claims (4 cards):** `anti-capture-correction-validity`, `bearer-map-commutation-failure`, `goodhart-as-selector`, `certification-under-manipulation`. Featured on homepage and README.

4. **Authorship / framing:** README authorship + what-this-is/isn't; site About (user-edited AI-generated site text note).

5. **Badge index pages:** `/badges/`, `/badges/type/{value}/`, `/badges/status/{value}/`; linked badges on card pages; nav **Badges**.

6. **Prior session log hash backfill:** commit refs added to 2026-07-04 hygiene and Phase 0.5 battery logs.

## Verification

- `npm run build` in `site/` — success.

## Open

- LaTeX `./build.sh` not re-run (prose-only bundle edits; no new cites).
- Strategic advice still open: Lean headline audit, tiling/mesa, falsification ledgers, adversarial review.

## Key paths

- Manuscript: `chapters/ch15-values-compressed-control.tex`, `ch16-value-bundle-model.tex`, `ch03-dynamical-guarantee.tex`, `ch31-conserved-properties.tex`
- Site: `site/src/pages/badges/`, `site/src/content/cards/*.md`, `site/src/pages/index.astro`
- Tracking: `metadata/TODO.md`, `README.md`

## Commits

- (this session)
