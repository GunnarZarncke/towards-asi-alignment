# Spine — Lean dependency spine follow-through

Status: **Spine lane** (2026-08-22). Krym revision **closed** 2026-08-17. Module map + build: [`formal/README.md`](../../formal/README.md). Per-chapter `% TODO[formalize]:` stay local.

**Boundaries:** reader copy + WWCTV refs → [`voice.md`](voice.md); external fixtures → [`witness.md`](witness.md); field homographs → [`field.md`](field.md).

## Goal

Align **drafted chapter formalism** with the **Lean dependency spine**: finite models, typed interfaces, bridge vocabulary, `\leanspine{}` / `{leanbox}` where chapters cite the spine. Done = checked Lean module, explicit **refuse** in prose, or deferral named to another lane.

**Non-goals:** discharge bridges on real systems; prove `Safe`; Witness measurand protocols; field synonym renames.

---

## Checklist

- [ ] **P1 MB10** — non-enumerability prose (ch08/ch30/ch31/ch48); prove or type `ConservedPropertySignatureVerifiable_of_chokepoint`; optional audit-forgeability toy beyond `forgeability_gap`
- [ ] **P1 Chokepoint** — optional rename gravestone identifiers; optional empirical note on `SharedInstrumentHypothesis` (Witness may supply data)
- [ ] **P2** — `Field/Finite/PredictorLoop.lean` (ch10 genesis path)
- [ ] **P2** — Defeaters finite toys: MB2, MB3, MB5, MB6a, MB7a, MB9
- [ ] **P2** — `PositiveMeasuredPath → CorrectionIntegrity` after Witness H1 (`CompositePathBypass.lean`; sibling CIRIS charter)
- [ ] **P3** — Trace ↔ Shannon MI on pinned fixture; `WorkedInstance` vs rich `cci_audit` scoping
- [ ] **P3** — `{leanbox}` on remaining high-value chapters (~26 without)
- [ ] **P3** — Chapter ↔ Lean gaps opportunistically: `Bundles.lean`, ch13 `P12`, ch07 boundaries, ch48 basins, ch42 `P40`, more `\leanspine{}`
- [ ] **P3** — App G translation spine opener (**author**); wire `BundleEvidenceAdequate` to experiments
- [ ] **P4** — App B secondary sync (overlaps Field); regret leaf; field-agenda build-time codegen; axiom budget in `make check`; Debate site prose grep

**Voice coordinates (not duplicated here):** WWCTV → chokepoint forward refs; U-ledger U-03/U-05/U-14/U-16. Source: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.

---

## Verification

`lake build` · `python3 formal/scripts/check_axiom_budget.py` · `./build.sh` after App G / `\leanspine` edits. Claim strength: proof / counterexample / bridge only.

## Related

[`appendices/appG-lean-proof-spine.tex`](../../appendices/appG-lean-proof-spine.tex) · [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex) · [`metadata/assumptions-ledger.md`](../../metadata/assumptions-ledger.md) · [`metadata/uncertainty-ledger.md`](../../metadata/uncertainty-ledger.md) (U-04 forgeability) · [`drafts/attic/krym-architecture-revision-plan.md`](../attic/krym-architecture-revision-plan.md)
