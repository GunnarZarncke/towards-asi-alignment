# Six-claims spine — Phases 0–2

**Date:** 2026-08-17

## Shipped

### Phase 0 — audit artifact
- [`drafts/claim-spine.md`](../claim-spine.md): canonical map (six intro claims → parts → safety-case layers → ch48 status; second-tier C-008–C-011)

### Phase 1 — consistency fixes
- ch48 summary: five → six opening claims
- ch30: ten-claim → nine-claim (matches ch33)
- [`metadata/claims-ledger.md`](../../metadata/claims-ledger.md) C-044: discharged (all six in ch48 §Opening Claims Revisited)
- [`frontmatter/executive-overview.tex`](../../frontmatter/executive-overview.tex): six preservation problems aligned to Introduction order (boundary first)

### Phase 2 — navigational spine
- `\label{claim:boundary}` … `\label{claim:basin}` on intro claims
- Introduction §How these claims unfold (`sec:how-claims-unfold`) + [`tables/claim-spine.tex`](../../tables/claim-spine.tex)
- Part openers tag which intro claim(s) each part develops
- [`review/claim-checklist.md`](../../review/claim-checklist.md): intro-claim tag item

## Verified
- `./build.sh` succeeds (1402 pages)

## Language pass (same day)

Introduction and part openers rewritten for first-reader knowledge: operational paraphrases from App E; no LHCV / CCI / ledger / “discharge” in front matter; claim labels moved inside `introclaim`.

