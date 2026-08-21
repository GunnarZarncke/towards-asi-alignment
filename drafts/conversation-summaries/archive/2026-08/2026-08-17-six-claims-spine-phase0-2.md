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

### Phase 3 — safety-case dedup
- [`tables/claim-layer-map.tex`](../../tables/claim-layer-map.tex): ch03 preview / ch33 nine-claim / ch42 eight-layer ↔ intro claims
- ch03 §Shape of a Safety Case: grounding kept; Claims 1–6 → table + cross-ref
- ch33, ch42: pointer to `tab:claim-layer-map`

### Phase 4 — chapter claim tags
- First chapter per part: one-line intro-claim tag in `epistemicstatus` (ch01, ch06, ch11, ch15, ch21, ch25, ch30, ch34, ch39, ch45)

### Phase 5 — ch48 discharge
- [`tables/claim-status-ch48.tex`](../../tables/claim-status-ch48.tex)
- `sec:spine-beyond-intro-ch48` (C-008–C-011)

## Commits
- `e76251c9` Phases 0–2 + language pass
- `16d78603` Phases 3–5
- `c9113a8e` Phase 6 companion site + check script

### Phase 6 — companion site + tooling
- [`metadata/concepts/bodies/six-thesis-claims.md`](../metadata/concepts/bodies/six-thesis-claims.md) + roster entry; synced card at `/cards/six-thesis-claims/`
- Homepage callout; all four reading paths; FAQ + `llms.txt`; cross-link from standalone-claims
- [`scripts/check_claim_spine.py`](../../scripts/check_claim_spine.py) wired into `make check`
- Plan: [`drafts/six-claims-spine-plan.md`](../six-claims-spine-plan.md)
- Minor part opener fixes (part01 `sec:how-claims-unfold`; part03 explicit Claim refs)

## Next
- None required from six-claims spine plan scope.
