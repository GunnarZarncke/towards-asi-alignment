# 2026-09-19 — Predictions positive titles and aggregation

## Trigger
User renamed prediction market titles in `metadata/predictions.yml`, asked to promote renames, rewrite negative titles as positive predictions, add aggregation (spine + pause), external Metaculus factor with embed, and clarify optimistic P(doom) bound. Later: add and use `marketQuestion` tier (label vs dated lead vs scope/YES bars).

## Done
- **Appendix H (`appP-bridge-predictions.tex`):** Positive catalog/subsection/box titles; positive question leads and authbar prose; new §aggregation (spine dependencies, q_pause, optimistic bound sketch, frontier gap); intro reframed as optimistic upper bound on P(doom).
- **`metadata/predictions.yml`:** All 18 markets — positive titles; `marketQuestion` per market; `externalFactors` (Metaculus Q44423 pause/governance).
- **Site:** `sync-predictions.mjs` — `marketQuestion` + Scope split from appendix; external factor card; aggregation metadata in `predictions.json` (gitignored, build-time); `MetaculusEmbed.astro`; `/predictions/` hub (aggregation blurb, external factors section); prediction card external badge + embed; `content.config.ts` schema fields.
- **`site/README.md`:** Document shortQuestion vs marketQuestion sync.

## Decisions
- **Three text tiers:** `shortQuestion` = catalog/aggregation label; `marketQuestion` = dated listing lead (yaml canon for site); scope + YES bars stay in appendix (sync extracts Scope for cards).
- **External pause factor:** Metaculus Q44423 (AI safety legislation 2027–2028), not an 18th bridge market; pairs with Market 14 in aggregation sketch.
- **P(doom) composition:** Schematic bound only — optimistic because YES = tool exists, not frontier bridge discharge; correlated markets 1/4/8/12/13 noted.

## Open / next
- List eighteen markets on Metaculus/Manifold when ready (plan Q1/Q2 still open).
- Optional: split `\textbf{Scope.}` in appendix TeX (currently sync splits lead vs rest of Question block).
- Draft `marketQuestion` drift check: run `sync-predictions` after TeX lead edits.

## Verification
- `cd site && node scripts/sync-predictions.mjs`
- `cd site && npm run build` (passed this session)
