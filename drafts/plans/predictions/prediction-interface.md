# Prediction interface (P0c)

Status: **plans locked** (2026-09-19). Source review: [`../../attic/bridge-predictions-Lean-improvements.md`](../../attic/bridge-predictions-Lean-improvements.md). Prior-test snapshot: [`../../predictions/bridge-predictions-prior-tests.md`](../../predictions/bridge-predictions-prior-tests.md). Working criteria: [`../../predictions/bridge-prediction-market-criteria.md`](../../predictions/bridge-prediction-market-criteria.md) (`0.4-working`). Instrument plan: [`bridge-prediction-markets.md`](bridge-prediction-markets.md).

This file is the **integration checklist** across Predictions, Spine, Construct/v2, manuscript appendix, and site. It does not replace the instrument plan’s Q1/Q2/Q6 listing questions.

## Decisions (do not re-litigate)

- Bridges still compose; the missing object is **benchmark → per-system scoped certificate → semantic predicate**, not a broken `MB*` DAG.
- Certificates carry extra indices now; unary Lean predicates stay until Lean 2.0. No `AlignmentContext`.
- **§17** (bearer admission / U-17) is a separate 2027 market. §3 stays transport-only.
- **§15** composition, **§16** MB6b, **§18** scoped safety-in-a-declared-setting (`SafeIn`, not unrestricted `Safe`) are in the 2027 catalog (criteria draft). Listing still Q1/Q6.
- **§14** stays constructibility / binding authority. Not MB11. Do not widen to cycle-preserve / \(D_{\mathrm{joint}}\).
- Derive `Certified` / `SatisfiesInvariants` in Lean (`Evidence.lean` / `Certification.lean`). Residuals: recertification (§6/§15 addendum), eval-list vs layers (§13). No markets for those names. No market for acceptable-risk (values vote).
- Three δ objects: measured slack (`NumericRiskLeaf`); observed harm in a declared domain (§18); accepted tolerance (`WithinDeploymentRiskTolerance`, vote).
- v2-later (not 2027 boxes): named restorer; path-legal successors; cycle-preserve / structural stop authority; grain-mixing; construction-vs-constructibility. Do not move §§1–15 or §17 into a waiting room. Do not widen §1/§6/§14 YES bars.
- **Appendix** print H, after research program, before Lean. Source `appendices/appP-bridge-predictions.tex`. Two registers: boxed spec = Metaculus/Manifold English; surrounding = glossary / research-program language. Almost no formulas (risk bound only).
- **Site:** `/predictions/` hub, nav item, Gauss-curve symbol, coming-soon offsite graph placeholder, `prediction` cards (overview + §1–§18).
- Q8 = appendix (+ optional App B pointer). No sixth intro claim. No green cells from prices.

## Phases

| Phase | Work | Status |
|-------|------|--------|
| **P0c plans** | This file; criteria 0.4; instrument-plan P0c; spine P2 certificate layer; embedded-v2 note | **done** 2026-09-19 |
| **Appendix** | `appP-bridge-predictions.tex`; `predictionbox`; print-letter plumbing; prior-test snapshot in sections | **done** 2026-09-19 |
| **Site** | card type, hub, nav, Gauss SVG, coming-soon embed | **done** 2026-09-19 |
| **Lean (v1 adapters)** | `Evidence.lean`: certs, adapters onto unary preds, `CoherentCertificateBundle`, derive `Certified`/`SatisfiesInvariants`, `HiddenRouteBound`, `SafeIn` stub | **done** 2026-09-19 |
| **Lean 2.0** | MB6 `Environment` then MB11 `SafeIn`; no covering tuple | later; author |

## Lean now (not v2)

Reuse `FieldInterfaces.lean` (`PositiveMeasuredPathCertificate`, `EpistemicCoverageEvidence`). New adapters are **not** numbered bridges. Do not reverse `MB4`/`MB4a`. Do not put market YES into Lean. Do not import 80/90/15% into `RiskGap`.

Detail: spine checklist in [`spine.md`](../spine/spine.md); implementation in `formal/AlignmentProofSpine/Evidence.lean`.

## Language

Public spec (criteria YES text, appendix boxes, site card bodies): ordinary AI-safety English for a Metaculus/Manifold audience. No Lean ids, no `MB*` keys, no gradient notation in that register.

Spine map (this file, instrument-plan table, `Evidence.lean`): where types must match.

## Next phase

PRA/Bayesian assurance layer: Phases 0–2 shipped; Phase 2b gap analysis shipped ([`../../predictions/resolution-gap-analysis.md`](../../predictions/resolution-gap-analysis.md), CIRIS context). Remaining: funding application + site listing-status cards; Phase 3 Markets 19–20 + site demo. [`assurance-risk-modelling.md`](assurance-risk-modelling.md).

## Related

[`bridge-prediction-markets.md`](bridge-prediction-markets.md) · [`assurance-risk-modelling.md`](assurance-risk-modelling.md) · [`../spine/spine.md`](../spine/spine.md) · [`../construct/embedded-v2.md`](../construct/embedded-v2.md) · session `2026-09-19-prediction-interface-p0c.md`
