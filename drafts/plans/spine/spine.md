# Spine — Lean dependency spine follow-through

Status: **Spine lane** (2026-08-22). Krym revision **closed** 2026-08-17. Module map + build: [`formal/README.md`](../../../formal/README.md). Per-chapter `% TODO[formalize]:` stay local.

**Boundaries:** reader copy + WWCTV refs → [`voice-plan.md`](../../attic/voice-plan.md) (closed); **bridge first-use / home `\leanspine`** → [`bridge-first-use.md`](bridge-first-use.md); external fixtures → [`backtest.md`](../backtest/backtest.md); field homographs → [`../field/field.md`](../field/field.md); construction / constructibility → [`../construct/construct.md`](../construct/construct.md) (not a spine `MB*` column); context-relative 2.0 reading → [`../construct/embedded-v2.md`](../construct/embedded-v2.md) (no covering `AlignmentContext` tuple); grain map → [`reference/embedded-v2-grain-map.md`](../../../reference/embedded-v2-grain-map.md).

## Goal

Align **drafted chapter formalism** with the **Lean dependency spine**: finite models, typed interfaces, bridge vocabulary, `\leanspine{}` / `{leanbox}` where chapters cite the spine. Done = checked Lean module, explicit **refuse** in prose, or deferral named to another lane.

**Non-goals:** discharge bridges on real systems; prove `Safe`; Backtest measurand protocols; field synonym renames.

---

## Checklist

- [ ] **P1 MB10** — non-enumerability prose (ch08/ch30/ch31/ch48); prove or type `ConservedPropertySignatureVerifiable_of_chokepoint`; optional audit-forgeability toy beyond `forgeability_gap`
- [ ] **P1 Chokepoint** — optional rename gravestone identifiers; optional empirical note on `SharedInstrumentHypothesis` (Backtest may supply data)
- [ ] **P2** — `Field/Finite/PredictorLoop.lean` (ch10 genesis path)
- [x] **P2** — **MB6 signed gradient.** Live objects: `CorrectionSelectionGradient`, `CorrectionSupportingBasin` / `CorrectionSupportingBasinSys`, `MB6a_gradient_estimator_soundness`, `MB6b_correction_supporting_basin`. Unsigned `BasinShockRobust` (`abbrev BasinStableSys`) is not the MB6 consequent. Frozen `ε` is independent of the measured gradient. `LockedInBadBasin` kept as the negative. No covering tuple. Detail: [`../predictions/bridge-prediction-markets.md`](../predictions/bridge-prediction-markets.md) § MB6. Shipped 2026-09-18.
- [x] **P2** — **Certificate / evidence layer** (`Evidence.lean`). Typed per-system certificates + soundness adapters onto **existing unary** predicates; `CoherentCertificateBundle` (same `A`); derive `Certified` as bundle inhabitance; derive `SatisfiesInvariants` as `LayeredAlignedDef`. `HiddenRouteBound` beside Boolean `HiddenBIQBoundedSys`. `SafeIn` stub (does **not** retarget `MB11`). Fold `PositiveMeasuredPath → CorrectionIntegrity` as eval-soundness adapter, not reverse of `MB4a`. No `AlignmentContext`. No market YES constructors. No 80/90/15% in `RiskGap`. Detail: [`../predictions/prediction-interface.md`](../predictions/prediction-interface.md). Shipped 2026-09-19.
- [ ] **P2** — Defeaters finite toys: MB2, MB3, MB5, MB6a, MB7a, MB9
- [x] **P2** — `PositiveMeasuredPath → CorrectionIntegrity` — **subsumed** by `Evidence.positive_measured_path_eval_soundness`
- [ ] **P3** — Trace ↔ Shannon MI on pinned fixture; `WorkedInstance` vs rich `cci_audit` scoping
- [ ] **P3** — `{leanbox}` on remaining high-value chapters (~26 without)
- [x] **P3** — Bridge first-use: Ch. 10 genus + home-chapter `\leanspine{bridge}` only ([`bridge-first-use.md`](bridge-first-use.md)); freeze Lean/`MB*` before Ch. 10 (2026-09-01)
- [ ] **P3** — Chapter ↔ Lean gaps opportunistically: `Bundles.lean`, ch13 `P12`, ch07 boundaries, ch48 basins, ch42 `P40` (do not scatter extra `{bridge}` tags; see first-use plan)
- [ ] **P3** — App G translation spine opener (**author**); wire `BundleEvidenceAdequate` to experiments
- [ ] **P4** — App B secondary sync (overlaps Field); regret leaf; field-agenda build-time codegen; axiom budget in `make check`; Debate site prose grep
- [ ] **2.0 (not v1):** if authorized, MB6 then MB11 context-relative (`Environment` / `SafeIn`); comments on unary MB1/2/9. No `AlignmentContext` n-tuple; no new axiom to `Safe`. `BridgeCut` stays a review method until a rewrite needs it. **Certificate adapters are v1**, not this bullet ([`../predictions/prediction-interface.md`](../predictions/prediction-interface.md)).

**Voice coordinates (not duplicated here):** WWCTV → chokepoint forward refs; U-ledger U-03/U-05/U-14/U-16. Source: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.

---

## Verification

`lake build` · `python3 formal/scripts/check_axiom_budget.py` · `./build.sh` after App G / `\leanspine` edits. Claim strength: proof / counterexample / bridge only.

## Related

[`appendices/appG-lean-proof-spine.tex`](../../../appendices/appG-lean-proof-spine.tex) · [`appendices/appB-bridge-crosswalk.tex`](../../../appendices/appB-bridge-crosswalk.tex) · [`metadata/assumptions-ledger.md`](../../../metadata/assumptions-ledger.md) · [`metadata/uncertainty-ledger.md`](../../../metadata/uncertainty-ledger.md) (U-04 forgeability) · [`../construct/embedded-v2.md`](../construct/embedded-v2.md) · [`../predictions/prediction-interface.md`](../predictions/prediction-interface.md) · [`drafts/attic/krym-architecture-revision-plan.md`](../../attic/krym-architecture-revision-plan.md)
