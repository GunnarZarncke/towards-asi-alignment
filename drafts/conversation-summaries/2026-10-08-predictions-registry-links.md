# 2026-10-08 — Predictions registry links

kind: new-work
uptake: status

## Trigger
End-of-session commit: wire manuscript and site to versioned claims-registry pages via a single `registrySite` base URL; fix prediction-card LaTeX link rendering; restore full appendix boxes for Markets 19–21; improve Market 14 card readability and remove redundant audit/notes when YES requires is present.

## Done
- content: **`metadata/predictions.yml`** — `registrySite` / `registryRepo`; Market 14 `notes` rewritten for card legibility.
- content: **`scripts/generate_claims_base_tex.py`** (new) + **`scripts/generate_manuscript_tex.sh`** + **`metadata/preamble.tex`** + **`.gitignore`** — gitignored `metadata/claims-base.tex` defines `\claimsbase` and `\claimspage{market-NN}{K}`.
- content: **`appendices/appP-bridge-predictions.tex`** — catalog 1–13 & 15–18 use `\claimspage`; Market 14 full box; Markets 19–21 restored to full boxes (not registry stubs until Phase 4).
- content: **`site/scripts/sync-predictions.mjs`**, **`site/scripts/lib/tex-convert.mjs`** — Property/Closest-work use full LaTeX converter; `registryContractUrl` → versioned site page; `expandClaimspage`; skip audit/notes on cards with YES requires (M14 only keeps full box on card); Market 14 readable evidence line.
- content: **`site/src/pages/predictions/index.astro`**, **`PredictionMarketPanel.astro`** — resolution-criteria external link + registry footer on hub panels.
- content: **`drafts/plans/predictions/eval-registry-split.md`**, **`INSTRUCTIONS.md`** — 19–21 stay full-box until Phase 4; appendix scope notes registry pointers.
- content: **`metadata/TODO.md`** — closest-evidence → registry sketches lane.
- bookkeeping: **`npm run sync:predictions`** and **`npm run sync:chapters`** — OK; no `#1/v#2` macro leak in synced `appP.md`.
- bookkeeping: Sibling repos committed earlier in session (`ai-safety-claims` `0874cae`, `ai-safety-claims-workbench` `7fb366b`).

## Decisions
- Registry URL shape: `{registrySite}/markets/market-NN/vK/` (change base once for domain migration).
- Cards for registry markets: property + closest work + resolution link; numeric bars live on registry version page only.
- Market 14: appendix and card keep YES requires; no registry link; custom evidence-class text on card.

## Open / next
- Independent host + `snapshot-0`; Metaculus listing; Phase 4 for Markets 19–21.
- Closest-evidence audit per catalog market → registry sketches (TODO lane).
- Optional: `make check` / PDF build with `.venv/bin/python scripts/generate_claims_base_tex.py`.

## Key paths
- `metadata/predictions.yml`, `appendices/appP-bridge-predictions.tex`
- `scripts/generate_claims_base_tex.py`, `site/scripts/sync-predictions.mjs`
- `drafts/plans/predictions/eval-registry-split.md`

## Commits
- (this session)
