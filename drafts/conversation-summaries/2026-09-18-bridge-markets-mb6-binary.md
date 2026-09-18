# 2026-09-18 — Bridge markets MB6 + binary

## Trigger
User: markets are YES/NO only; conservatively map refuse → NO (still aggregates, even if coarser than the bridges). Also the MB6 comment: change the formal object before the test — unsigned `PercolationEvidence → BasinStable → CorrectionIntegrity` has no sign; use \(g_{\mathrm{CCI}}=\partial\mathbb{E}[\Delta\mathrm{CCI}]/\partial\mu\) and shock-robust ∧ \(g_{\mathrm{CCI}}\ge-\varepsilon\) ⇒ correction-supporting basin.

## Done
- Criteria `0.3`: no void; refuse/inapplicable/desk-disagreement → NO; claim-strength says NO is a lump.
- Retracted unsigned-basin §7a. §7 now a 2027 *slice*: frozen \(g_{\mathrm{CCI}}\) estimate (not an arbitrary predictor) predicts later correction erosion; required negative family is healthy coupling + negative gradient.
- Plan: accepted MB6 spec change; Spine/Field pointers; no Lean this session.
- [`spine.md`](../plans/spine.md) P2 item; [`field.md`](../plans/field.md) P2 MB6 row.

## Decisions
- Binary aggregation over precise refuse. Methodology refuse stays in experiments.
- Do not test current Lean MB6a/MB6b. Public `cruxWording` was already “preserves correction”; Lean MB6a is the unsigned leftover.
- Full shock-robust ∧ gradient implication is the Spine object, not extra 2027 YES bars.
- Site MB6 card follows the Lean rewrite, not this session.

## Open / next
- Same listing Qs (Q1, Q2 titles even more load-bearing, Q6, Q8).
- Spine: implement \(g_{\mathrm{CCI}}\) / `CorrectionSupportingBasin` when that lane runs.

## Key paths
- `drafts/bridge-prediction-market-criteria.md`
- `drafts/plans/bridge-prediction-markets.md`
- `drafts/plans/spine.md`
- `metadata/concepts/bodies/mb6-selection-and-basin-stability.md`

## Commits
- none
