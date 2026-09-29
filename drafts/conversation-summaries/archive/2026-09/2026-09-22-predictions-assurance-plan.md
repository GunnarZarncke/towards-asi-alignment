# 2026-09-22 — Predictions assurance-risk plan

## Trigger

Review and refine the predictions appendix / PRA improvement plan against local catalog, Lean spine, and incentives notes; make it self-contained; integrate Markets 19–20 for the site demo; move into the lane plans tree; end session with commit.

## Done

- Authored reviewed execution plan at [`drafts/plans/predictions/assurance-risk-modelling.md`](../plans/predictions/assurance-risk-modelling.md) (~910 lines).
- Preserved archive [`drafts/predictions/predictions-improvements-v0.md`](../attic/predictions-improvements-v0.md) and redirect [`drafts/predictions/predictions-improvements.md`](../attic/predictions-improvements-v0.md).
- Incorporated resolution incentives from [`drafts/predictions/predictions-improvements-incentives.md`](../attic/predictions-improvements-incentives.md).
- Wired plan into [`drafts/plans/README.md`](../plans/README.md), [`prediction-interface.md`](../plans/predictions/prediction-interface.md), [`bridge-prediction-markets.md`](../plans/predictions/bridge-prediction-markets.md).

## Decisions

- **Plan only** — no appendix, YAML, Lean, or site implementation in this session.
- **Markets 1–18 IDs stable**; Markets 19 (integrated tournament) and 20 (open-world challenge) designed in Phase 3, listed in Phase 4 after funding/resolution gates.
- **Site demo** uses resolved experimental outputs from Markets 19–20 as scoped presets, not market prices or YES/NO outcomes; user-supplied ranges before resolution.
- **Canonical assurance model** — one typed manifest projecting to Lean crosswalk and PRA/Bayesian graph; neither proof DAG nor hand-maintained risk graph is sole source of truth.
- **Remove product-of-market-prices P(doom) bound**; replace with assurance-failure \(F/R/U\) derivation and separate consequence model.
- **κ/S_R** — assurance layer only; Market 20 informs κ sensitivity, does not directly estimate κ.

## Open / next

- Accept scope decisions in the plan, then Phase 1: replace Appendix H aggregation section and site “Optimistic P(doom)” copy.
- Phase 2–2b: contract audit, resolution adapters, funding-gated listing vocabulary in YAML.
- Phase 3: complete Market 19/20 contracts + manuscript PRA sections + site demo skeleton.
- Unrelated working-tree changes (appendix P edits, site sync, figures) remain unstaged — not part of this plan commit.

## Key paths

- Plan: [`drafts/plans/predictions/assurance-risk-modelling.md`](../plans/predictions/assurance-risk-modelling.md)
- P0c baseline: [`drafts/plans/predictions/prediction-interface.md`](../plans/predictions/prediction-interface.md)
- Live spec: `appendices/appP-bridge-predictions.tex`, `metadata/predictions.yml`

## Commits

- `b423380b` Add predictions assurance-risk modelling lane plan.
