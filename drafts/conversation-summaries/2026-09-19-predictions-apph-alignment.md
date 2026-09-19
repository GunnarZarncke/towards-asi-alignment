# 2026-09-19 — Predictions App H alignment

## Trigger
User clarified Q1/Q2 and “resolve early” (calendar dates, not resolver timing); flattened `metadata/predictions.yml`; chose early resolve-by for markets 13–14; asked to fix Appendix H to match the catalog; end session and commit.

## Done
- **Q1/Q2 decided** (recorded in `drafts/plans/predictions/bridge-prediction-markets.md`): author owns design and will list on Metaculus; `marketQuestion` uses “Published method for…” (or equivalent); thresholds stay in appendix; date in `resolveBy` only.
- **`metadata/predictions.yml`** (prior commit `6f3033aa`): per-market `resolveBy`, `resolvers`, `resolverStatus`, `marketStatus`; removed top-level `resolution:` block.
- **`site/scripts/sync-predictions.mjs`** (prior commit): per-market resolve-by and resolver lines on cards.
- **`appendices/appP-bridge-predictions.tex`**: all 18 boxes — `\textbf{Resolve by.}` line; question leads match YAML (no date in question); global sections reference per-market dates; markets 13–14 → 30 June 2027.
- Sync clean: `node site/scripts/sync-predictions.mjs` (no appendix/YAML drift warnings).

## Decisions
- **Early resolve-by:** markets **13** (audit gaming) and **14** (binding deployment) → **`2027-06-30`**; rest **`2027-12-31`**.
- **“Resolve early”** meant earlier calendar close for documentary (#14) and mature audit-game (#13) rows, not judgment-stack timing.
- **`resolverStatus: confirmed`** only after written agreement from resolver; author is custodian, not adjudicator.

## Open / next
- Confirm proposed resolvers (METR/AISI, Scott Alexander, Plex, etc.) before listing.
- Surface `resolvers` / `resolverStatus` on Metaculus listing copy when live.
- Optional: empirical discharge of `Evidence.lean` eval-soundness axioms + residual criteria addenda (recertification, eval-list vs layers) — still on TODO/plans if not yet filed.
- First Metaculus listing with claim-strength header (YES = bars met; NO = lump).

## Key paths
- `metadata/predictions.yml`
- `appendices/appP-bridge-predictions.tex`
- `drafts/plans/predictions/bridge-prediction-markets.md`
- `site/scripts/sync-predictions.mjs`

## Commits
- (this session)
