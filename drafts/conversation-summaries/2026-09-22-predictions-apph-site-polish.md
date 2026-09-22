# 2026-09-22 — Predictions App H + site polish

## Trigger
User feedback on predictions appendix readability (site + print source), Gauss icon shape, predictions list duplicate titles, broken Appendix H `/full/` link, and a long annotation pass on App H prose.

## Done
- **`appendices/appP-bridge-predictions.tex`** — Proper question phrasing (`Will there be…`); terminology note (market/contract/prediction); glossary/judgment/common-rule clarifications; per-market prose expansions (Markets 1–10, 6–7, etc.); seven conserved properties tied to Ch. 31; aggregation figure + $\mathcal{P}$ explanation; removed “Not in catalog” and “Relation to other appendices” sections; “Closest existing work” replaces dated prior-test leads.
- **`metadata/predictions.yml`** — `marketQuestion` strings aligned with appendix.
- **Site:** Gauss bell sampled from normal PDF; predictions hub shows title + question; `/full/` routes for all `bookPageId` cards; `bookFullHref` for App P links; prediction cards skip duplicate lede; `sync-predictions` summary = question.
- **`site/scripts/lib/tex-convert.mjs`** — Callout link rendering; `\item[label]` description lists; `\texorpdfstring`; balanced figure captions; local figure paths.
- **`figures/appp-bridge-spine.svg`** + **`site/public/figures/appp-bridge-spine.svg`** — Spine dependency graph for aggregation section.
- Regenerated **`site/src/data/card-redirects.json`** (not tracked; sync scripts are source).

## Decisions
- Keep generated `site/src/content/book/` and prediction cards gitignored; deploy/build runs `sync-chapters` + `sync-predictions`.
- Did **not** stage unrelated working-tree edits (`INSTRUCTIONS.md`, `appN`, `preamble.tex`, assurance plan log, `CIRIS_TSA` PDF).

## Open / next
- PDF build may need PNG fallback if LaTeX toolchain lacks SVG for `appp-bridge-spine.svg`.
- Run full site sync + deploy to pick up gitignored book/card artifacts on production.

## Commit
`1ebf999e` — Polish Appendix H predictions and the site hub for readability.
