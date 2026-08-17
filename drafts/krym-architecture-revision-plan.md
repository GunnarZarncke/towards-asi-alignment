# Krym architecture revision plan

Source thread: [Krym_conversation.md](Krym_conversation.md). Full phased plan: `.cursor/plans/krym_architecture_revision_da847df9.plan.md` (Cursor plan file).

## Phase status

| Phase | Scope | Status |
|-------|--------|--------|
| **1** | Early book scope: three questions in the **introduction**; ch01 keeps a short handoff into the wrong-object argument | **Done** 2026-08-16 (moved out of ch01) |
| **2** | App E pointing homograph + precise bridge vocabulary | **Done** 2026-08-16 |
| **3** | Lean MB2 names + `BundleAligned` conjunction (`3f664d28`) | **Superseded by 3b** |
| **3b** | Make Phase 3 non-vacuous (Krym/Harfe review 2026-08-17) | **Done** 2026-08-17 |
| **4** | Lean MB4 correction uptake vs legitimacy | **Next** |
| **5** | Construction Lean model + MB8 gravestone | Pending |
| **6** | Crux Props, formal contracts, field v1/v2 | Pending |

## Resolved decisions (summary)

- Three alignment questions live in the **introduction** (`sec:three-alignment-questions`); ch01 only hands off: all three presuppose locating the relevant process. No Lean symbols on ch01.
- Target Realization: open interface, not `MB*`.
- MB8: remove from matrix; keep MB8 gravestone card.
- ev-131 → MB4; no meta-evidence tier.
- Field v2 cutover: manual author confirm last.

Log: [drafts/conversation-summaries/2026-08-15-krym-phase1-early-scope.md](conversation-summaries/2026-08-15-krym-phase1-early-scope.md).

## Phase 3b — MB2 non-vacuous (before Phase 4)

Review of `3f664d28`: Phase 3 made Krym’s decomposition *visible*; it did not make the identifiability crux *checkable*. Harfe’s bar is fewer opaque axioms, not more named `True`. Honest status: **the missing MB2 step is named in Lean; it is not yet in the proof.** Do not start Phase 4 until 3b lands.

Success criteria:

1. `BundleExperiment` / `BundleModel` have concrete fields (or a finite interpretation from `FinPolicyExperiment`). `CompatibleWithEvidence` is a `def`.
2. No global `axiom MB2a_*` / `MB2b_*`. Those claims are `def … : Prop` hypotheses. Something that currently takes `BundleGradientEquivalent` consumes `hMB2 : MB2Crux` (or the relevant conjuncts). Unused scaffolding is deleted.
3. MB2c does **not** jump `BundleGradientEquivalent H A → BundleAligned H A`. Gradient may license correspondence (still a hypothesis). Causal control and tradeoff direction are separate antecedents, with a finite independence toy that can drop each conjunct.
4. App G displayed equations match Lean antecedents (`E.host = A`, `ReferenceForBundleAudit`, etc.).
5. `#print axioms` on certification theorems does not grow from unused MB2a/b; ideally the live MB2 footprint is hypotheses + defs, not extra unused axioms.

### Triage of the 2026-08-17 review

| Item | Disposition |
|------|-------------|
| Empty `BundleExperiment` / `BundleModel`; compatibility as axiom | **3b** |
| `BundleEvidenceAdequate → BundleIdentifiable` as global axiom | **3b** — optional hypothesis, not axiom |
| MB2c: gradient ⇒ unary causal control | **3b** — split the implication |
| App G `mb2b` missing Lean antecedents | **3b** — prose/Lean mismatch is a Phase 3 bug |
| `MB2Crux` unused; certification still only MB2c | **3b** — thread as `Prop` or delete axioms. Full all-bridge `hMB*` pattern stays Phase 6 |
| `P15_observed_policy_not_fin_identifiable` = P15 rename | **3b** — keep only as illustration or alias; do not claim new content; optional `Fin*` → abstract interpretation |
| `SpineModel.MB2_independently_load_bearing` still `True` vs `Bool` | **3b** — drop causal control / direction separately |
| MB2b type jump (model of `A` vs reference of `H`) | **3b** — typed identified/reference models, not only `ReferenceForBundleAudit` |
| Correction uptake vs legitimacy | **Phase 4** (already in plan) |
| Construction vs certification; MB8 factorization | **Phase 5** (already in plan) |
| Cruxes-as-Props for the rest of the spine; field v1/v2; formal contracts | **Phase 6** (already in plan). 3b is the MB2 *pilot* of Krym §9 so Phase 6 does not repeat this mistake |
| DebateGame / `debateValue` / “Boolean evaluator of the judge” | **Out of this plan** — Harfe debate thread (`e55c6a56`), not Krym architecture |
| Wire experiment scripts to `BundleEvidenceAdequate` | **Out of this plan** — empirical line stays ch15–21 + IRL/ELK cites |
| Prove identifiability from real data / solve IRL–ELK | **Out of this plan** — Lean can type the hypothesis and show finite underdetermination |
| Whole-spine axiom reduction; all finite toys on the same type as `System` | **Out of this plan** — Lean credibility program, not this architecture revision |
