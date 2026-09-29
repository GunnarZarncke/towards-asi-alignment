# 2026-09-22 — Predictions Phases 0–2

## Trigger

User asked to implement the predictions improvement plan through Phase 2 (`drafts/plans/predictions/assurance-risk-modelling.md`).

## Done

- **Phase 0:** Froze sources before edit: HEAD `2543ddbd`; appendix/YAML `1ebf999e`; `Evidence.lean` `6c46f4bb`. Markets 1–18 IDs unchanged. No Lean edits.
- **Phase 1:** Replaced the product-of-prices optimistic \(P(\mathrm{doom})\) claim in Appendix H with assurance-failure \(F/R/U\) and the \(S_R/S_U\) odds update (\(S_U=1\) labeled no-information). Site hub/graph/overview/external-factor copy no longer advertises “Optimistic P(doom) composition.”
- **Phase 2:** Resolution interface (four routes, adapters, multi-source, bar function, tiers). Contract audit table + YAML `outputClass` / `evidenceTier` / `bars` / `sampleUnit` / adapter v1. Market 1 decisive-coverage 70% on the full hidden benchmark. Markets 7/9 keep continuous outputs; 13/15 keep frozen-audit and static-composition scope. Capability/independence is the primary “serious adversarial” definition; dollar/hour remain proxies. Hours-path still requires 3 teams / 80 hours (not weakened).
- `cd site && npm run sync:predictions` (20 cards); `npm run sync:chapters`; `make check` passed. PDF not rebuilt this session.

## Decisions

- Stop at Phase 2: no funding-gap analysis, no `draft`/`funding-gated`/`ready-to-list` vocabulary (Phase 2b), no Markets 19–20 contracts, no site PRA demo (Phase 3).
- `marketStatus: open` retained as internal catalog status until the listing gate.
- Market 1 coverage is a pre-listing scientific-bar clarification (`contractVersion: 1`), not a post-listing silent edit.

## Open / next

- Phase 2b: resolution-gap analysis, funding application, listing-status vocabulary, reason codes.
- Phase 3: typed assurance-model manifest, Markets 19–20, site demo with user-supplied ranges.
- Unrelated working-tree files (appN, INSTRUCTIONS, CIRIS PDF, etc.) were not part of this task.

## Key paths

- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
- `site/scripts/sync-predictions.mjs`
- `drafts/plans/predictions/assurance-risk-modelling.md`

## Commits

- none (not requested)
