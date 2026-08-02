# Field-claim formalization and Lean-bridge review plan

Status: Phase 1–3 decided (2026-08-02). Lean Phases 1–2 implemented; Phase 3 bridge dispositions recorded (no new `MB*`). Book/App B/matrix sync still deferred.

## Scope and assumptions

- **Audience:** book/formal-spine maintainers and alignment researchers, not general readers.
- **Scope:** the six field claims reviewed in the 2026-08-02 pass (originally listed under a since-dissolved “Missing-bridge candidates” table in `reference/field-agendas/field-agenda-index.md`; dispositions now live under **Coverage vs book treatment**).
- **Claim strength:** these are candidate type signatures and architecture decisions. They are not proofs that a field agenda works or that a real deployment satisfies a bridge.
- **Operational paraphrase:** for each field claim, identify (1) the object being certified, (2) the evidence supplied, (3) the conclusion sought, and (4) the counterexample that shows why the conclusion is not automatic.
- **Success criterion for a future Lean pass:** every adopted claim has a field-local model, a non-converse or defeater where appropriate, an explicit interface to the book’s predicates, and a checked axiom footprint. No field claim should reach `Safe` by bypassing `CertifiedSafetyCase` and `MB11`.

## Main conclusion

The table contains three different categories and should not be treated as six candidate peer bridges:

1. **Already explicit book bridges:** safety-case adequacy (`MB11`), measured-path anti-capture (`MB4a`), and the legacy CEV/process route (`MB8`).
2. **Field theories that need their own formal objects before any bridge decision:** model-class misspecification and regret.
3. **A conflated foundations neighborhood:** logical uncertainty and reflection are distinct. The spine already models a narrow reflection/tiling obstruction, but not logical induction.

The recommended first move is therefore **field-local modeling plus interface counterexamples, not adding `MB12`**. A new numbered bridge should be considered only after a theorem statement shows exactly which existing book predicate the field certificate is meant to warrant.

## Claim-by-claim formal sketches

### 1. Model-class misspecification / nonrealizability / grain of truth

#### Objects

- Environment/world model type `Env`
- Hypothesis/model type `Hyp`
- Policy type `Policy`
- observation histories and a likelihood or compatibility relation
- a represented model class `H : Set Hyp`
- true environment `μ : Env`
- an evidence-relative ambiguity set `Plausible : Evidence → Set Env`
- a safety-relevant property `Q : Env → Policy → Prop`

#### Predicates

- `Realizable μ H := ∃ h ∈ H, observationallyEquivalent h μ`
- `Nonrealizable μ H := ¬ Realizable μ H`
- `GrainOfTruth H opponents` for the stronger multi-agent closure condition; do not identify this with ordinary realizability
- `CoverageCertificate ev := μ ∈ Plausible ev` is not directly checkable for the unknown `μ`; the deployable form must instead be a conservative-coverage condition such as “every evidence-compatible environment is retained or uncertainty escalates”
- `RobustUnderAmbiguity π ev Q := ∀ μ ∈ Plausible ev, Q μ π`
- `MisspecificationDetected` or `UncertaintyEscalates` when observations leave the certified domain

#### Theorem and counterexample shapes

- Pure theorem: robust satisfaction over an ambiguity set transfers to the true environment **if** the true environment is in that set.
- Counterexample: a policy is optimal/safe in every model in `H`, the true environment is outside `H`, and the policy is unsafe in the true environment.
- Defeater: observations remain compatible with the represented class while a safety-relevant off-class environment differs only off-distribution.

#### Relation to the existing spine

- `MB1` is too narrow: it maps one measured boundary certificate to `BoundaryCondition`; it does not quantify over a hypothesis class or a true environment.
- `MB9` is the closer interface because `ConservativeAbstraction` already requires value-relevant change either to move the checked abstraction or raise uncertainty, and `MB9` maps a `GroundingCertificate` to `GroundingViable`.
- However, current `GroundingCertificate : System → Prop` is opaque. Saying misspecification is “covered by MB9” records the location of the wall, not a formal model of it.

#### Recommendation

Build a field-local finite model first, tentatively `Field/Finite/Nonrealizability.lean`, with the off-class counterexample and an ambiguity-set robustness theorem. Then define an explicit interface record from that model to a deployment-specific `GroundingCertificate`. Keep the real-system validity step under `MB9`.

Do **not** add a new bridge merely for “nonrealizability.” Add one only if the book adopts a distinct conclusion not already represented by grounding viability—for example, a misspecification-robust decision certificate that directly supplies a named safety-case layer.

### 2. Regret bounds imply deployment safety

The implication is false without additional assumptions. Low regret is relative to a loss, comparator class, horizon, and observation protocol; none of those ensures that catastrophic harm is represented.

#### Objects

- finite or measurable action, observation, and environment types
- policy `π`
- loss `ℓ : Env → Action → Cost`
- comparator class `Π`
- cumulative regret `Regret T π μ Π ℓ`
- deployment harm predicate or cost `Harm : Trace → Prop` / `TrueHarm : Trace → Cost`
- optional tail-risk or invariant certificate, since average regret can hide rare catastrophe

#### Predicates

- `RegretBounded π r := ∀ T, Regret T ... ≤ r T`
- `LossRepresentsHarm ℓ Harm`: safety-relevant harm is upper-bounded or otherwise detected by the learning loss
- `ComparatorContainsSafePolicy Π`
- `ExplorationSafe` or an invariant over all prefixes, not just asymptotic average performance
- `DistributionCovered` / ambiguity-set robustness
- `RegretSafetyCertificate`: packages the regret theorem and all transfer premises, but does not itself assert `Safe`

#### Theorem and counterexample shapes

- Counterexample A: zero regret under a constant loss while every action is catastrophic under `Harm`.
- Counterexample B: sublinear regret with one irreversible catastrophe, showing asymptotic average performance does not imply prefix safety.
- Conditional theorem: regret bound + loss-to-harm domination + safe comparator + safe exploration/tail condition + environment coverage yields a bounded deployment-specific harm leaf.

#### Relation to the existing spine

- `MB11` is only the final `CertifiedSafetyCase + WithinDeploymentRiskTolerance → Safe` gate. It should not absorb the whole learning-theoretic transfer.
- A regret result should enter upstream as evidence for a particular layer or numeric leaf. The exact target must be chosen before a bridge can be named.
- `RiskGap` is an influence/correction-capacity quantity, explicitly not expected loss or failure probability. A regret theorem must not be coerced into `NumericRiskLeaf` unless a separate theorem relates its loss to `Control − CCI`.

#### Recommendation

Add a field-local `RegretSafety.lean` only after fixing a small finite online-learning model. Prove the two counterexamples first. Then choose one honest interface:

1. regret certificate → a new harm-bound leaf carried alongside `NumericRiskLeaf`, or
2. regret certificate → evidence for one existing layer, leaving the safety case to combine it.

This may require a larger `CertifiedSafetyCase` extension if quantified harm becomes a real book commitment. It should not be hidden as a strengthening of `MB11`.

### 3. Logical uncertainty / reflection

This row currently joins two different claims:

- **logical uncertainty:** calibrated reasoning about unresolved mathematical statements under bounded computation;
- **reflection/tiling:** trusting or constructing successors that reason about the current system or proof process.

They should be modeled and decided separately.

#### Logical-uncertainty objects and predicates

- sentence type, deductive process over time, and market/probability sequence
- coherence/calibration/no-exploitation properties
- bounded reasoner and a decision rule consuming logical probabilities
- a task-specific predicate connecting calibrated beliefs to an audit or decision

Possible results are finite fragments of coherence or no-trader-exploitation. They do not by themselves imply `InferentialCouplingMeasurementValid`, `SuccessorSafe`, or `Safe`.

#### Reflection objects and predicates

The existing `Field/Finite/LobTiling.lean` already supplies:

- `HBLConditions`
- `LobFixedPoint`
- `ProvableSuccessorSafe`
- `self_certifying_tiling_obstruction`
- an explicit contrast with externally audited successor risk transport

This is an adequate narrow formal model of the stated Löbian obstruction, with correctly explicit proof-theoretic hypotheses.

#### Relation to the existing spine

- `MB5` is an ontology-shift successor-audit bridge; it is not a logical-uncertainty bridge.
- `MB7d` is inferential-UAD detector soundness; logical induction could potentially support a detector or forecast, but only through an additional task-specific interface.
- Reflection already has a field-local obstruction and a contrast to `SuccessorAuditLinks`; no new core bridge follows from it.

#### Recommendation

Split the index row conceptually. Keep reflection mapped to `LobTiling` / successor auditing. If logical induction is worth formal coverage despite “exclude by reference,” add a field-local module with no core bridge and one explicit non-implication to deployment safety. Promote it to a bridge only if a manuscript claim actually consumes logical-induction evidence.

### 4. Safety case implies `Safe`

#### Existing model

- `CertifiedSafetyCase A δ` packages certification, invariants, all eight alignment layers, and `RiskGap A ≤ δ`.
- `WithinDeploymentRiskTolerance A δ` supplies the governance acceptance judgment.
- `MB11_safety_case_adequacy` yields `Safe A`.
- `P30_safe_of_case` and `safe_from_spine_inputs` expose the dependency.
- `SpineModel.MB11_independently_load_bearing` shows that case and tolerance do not imply safety by logic alone.

#### Assessment

The existing bridge is sufficient for exactly the book’s deliberately abstract claim. No new bridge is needed.

Possible decomposition is editorial rather than required: distinguish case scope/completeness, tolerance legitimacy, and case-to-safety adequacy if reviewers need separate falsifiers. Do not split `MB11` until concrete independent evidence producers exist for those parts; otherwise decomposition only multiplies opaque axioms.

### 5. Anti-capture / measured-path legitimacy

#### Existing model

- `CorrectionPath A` contains the designated corrector, handles, and measured capacities.
- `CorrectionPathLegitimate` contains correct-agent, human-coincidence, control, reach, persistence, and no-capture conditions.
- `MB4a_measured_path_legitimacy` states `CorrectionIntegrity A → CorrectionPathLegitimate (SystemCorrectionPath A)`.
- Capture of one designated handle refutes legitimacy and, by contraposition through `MB4a`, refutes `CorrectionIntegrity`.

#### Important directional distinction

`MB4a` models a **necessary condition and falsifier**:

> genuine correction integrity implies that the measured path is legitimate.

It does not model the stronger positive inference:

> a green measured path implies genuine correction integrity.

That stronger claim is exactly where named-identity/composite-boundary mistakes can occur. A signed or apparently uncaptured named component may not be the real intervening composite.

#### Recommended model extension before any bridge change

- target system/composite boundary `A`
- named audited component `N`
- measured path `p`
- `PathCoversEffectiveController p A`
- `NoBypass p A`
- `CorrectionPathLegitimate p`
- counterexample with `CorrectionPathLegitimate p` for `N` but a bypassing composite controller, so `¬ CorrectionIntegrity A`

#### Assessment

`MB4a` is sufficient for the anti-capture necessity claim. It is insufficient for positive certification from a green path. Do not reverse it. If the book later needs the positive route, introduce a separate certificate requiring boundary coverage and no-bypass evidence—likely depending on `MB1`/`MB7a` as well as path legitimacy—rather than broadening `MB4a`.

### 6. CEV-process / extrapolated-volition route

#### Existing model

- `PreservesValueUpdateOperator A U`
- `MB8_cev_process_convergence : PreservesValueUpdateOperator A U → CorrectionIntegrity A`
- the operational alternative `ValueUpdateEnvelope`, which decomposes preservation into existing grounding, bundle, bearer, correction, successor, and adversarial layers
- a `LegitimacyTheater` defeater and finite counterexample

#### Assessment

`MB8` is sufficient as a clearly labeled **legacy opaque route**. It is not a substantive formalization of CEV, convergence, or extrapolated volition. Its current theorem name says “convergence,” while its antecedent states process preservation; this semantic mismatch should be reviewed before any code change.

If promoted beyond a comparison route, decompose it into:

- identity/legitimacy of the human update process,
- preservation/transport across ontology change,
- continued correction capacity and non-capture,
- a convergence or non-convergence property only if the field claim actually requires one,
- relation to `ValueUpdateEnvelope`.

Until then, leave `MB8` outside the live certification path and avoid multiplying axioms.

## Proof-spine architecture assessment

### What is already adequate

- The proof/counterexample/bridge distinction is explicit.
- `MB11`, `MB4a`, and `MB10` are threaded at the module level where their types become available.
- `Defeaters.lean`, `Chokepoint.lean`, and `SpineModel.lean` provide the right review pattern: name the failure signal, build a finite counterexample, and mechanically check independent load-bearingness.
- `Field/Finite/LobTiling.lean` demonstrates the right treatment for an external foundations result: formalize the local theorem without pretending it is a book bridge.

### Structural pressure points

1. **The bridge list mixes roles.** Some bridges turn measured evidence into semantic predicates (`MB1`, `MB9`), some transport properties (`MB3`, `MB5`), some assert normative legitimacy (`MB4`, `MB8`), and `MB11` converts a whole case into `Safe`. A field claim should be classified by role before receiving an `MB` number.
2. **Antecedent direction matters.** `MB4a` is a semantic-property-to-required-measurement implication used contrapositively, unlike most evidence-to-conclusion bridges. Documentation should keep this visible.
3. **`BridgeAssumptions` is early and monolithic.** Later typed bridges already live outside it. New field-local claims should not be forced into `Core.lean` merely for numbering symmetry.
4. **Unary versus transition evidence is not a fundamental blocker.** `MeasurementChannel` is generic in its carrier; a transition target can be represented by a dedicated structure or pair. This can unify the `MB10` verifiability story with `Chokepoint` without redesigning the whole spine.
5. **The safety case has one numeric leaf with a narrow meaning.** Regret, probability of catastrophe, expected value loss, and true harm are different quantities. Adding any of them is a safety-case architecture decision, not a bridge-labeling edit.
6. **The defeater ledger lags the bridge inventory.** `Defeaters.lean` systematically covers `MB1`–`MB9`, while `MB4a`, `MB10`, and `MB11` have independence witnesses or counterexamples elsewhere but no rows in that ledger.
7. **One defeater-table name is not implemented.** The `MB1` row names `EstimatorNonstationary`, but the module only implements the finite toy’s `distributionShifted` field. A future Lean pass should either add the named signal or change the table to the object that exists.
8. **Reader-facing inventories are stale by design but need reconciliation.** App B still omits `MB11` and does not present `MB4a` as a full row; some field-module comments still refer to `MB1`–`MB9`. These are documentation follow-ups, not evidence for a new bridge.

## Proposed implementation sequence

### Phase 0 — claim normalization, no Lean edits

1. Split “logical uncertainty / reflection” into two claims.
2. Clarify whether the anti-capture row means a necessary falsifier or positive certification.
3. Rename the conceptual MB8 claim as “process preservation → correction integrity” unless convergence becomes an explicit antecedent.
4. Record that “regret ⇒ safety” is rejected as stated; retain only a conditional transfer question.
5. Inventory reader-facing bridge ranges and queue App B rows for `MB4a` and `MB11`, while preserving the prior decision that App B edits require a separate authorized pass.
6. Record the `EstimatorNonstationary` table/implementation mismatch and the missing `MB4a`/`MB10`/`MB11` defeater-ledger rows as formal hygiene tasks.

**Gate:** each row has one unambiguous antecedent and consequent in ordinary language.

### Phase 1 — field-local finite models

**Done 2026-08-02** (Lean only; no book/matrix edits; no new `MB*`):

1. Defeater vocabulary repaired in `Defeaters.lean`:
   - named `EstimatorNonstationary` (+ toy signal theorem);
   - `ModelClassMisspecified` / `GrainOfTruthViolated`;
   - typed signals + toys for `MB4a` (`MeasuredPathCaptured`), `MB10` (`SignatureForgeableAtCapability`), `MB11` (`SafetyCaseScopeExceeded`).
2. `Field/Finite/Nonrealizability.lean` — off-class counterexample, ambiguity-set transfer, class-certificate ⇏ deployment safety.
3. `Field/Finite/RegretSafety.lean` — zero-regret/wrong-loss, prefix-catastrophe, conditional transfer / `RegretSafetyCertificate`.
4. Optional `Field/Finite/LogicalUncertainty.lean` — still deferred (exclude-by-reference; `LobTiling` covers reflection).
5. `Field/Finite/CompositePathBypass.lean` — green named path + bypass ⇏ integrity; positive certificate needs no-bypass.

**Gate:** `lake build`, `check_spine_model.py`, and `check_axiom_budget.py` passed with no new bridge axioms.

### Phase 2 — explicit interfaces to book predicates

**Done 2026-08-02** in `formal/AlignmentProofSpine/FieldInterfaces.lean` + `Forgeability.lean` / `Chokepoint.lean` (still no new `MB*`, no book/matrix edits):

1. **Epistemic coverage → grounding** — `EpistemicCoveragePackage` / `EpistemicCoverageEvidence`: definitional packaging of `ConservativeAbstraction` with opaque `GroundingCertificate`; consumer `EpistemicCoverageEvidence.grounding_viable` via existing `MB9`. Finite shape: `epistemic_coverage_finite_shape_not_deployment_safety`.
2. **Regret certificate** — finite `RegretSafetyCertificate` kept; System-level `SystemRegretSafetyEvidence` / `DeploymentHarmBounded` **not** mapped to `RiskGap`.
3. **Regret consumer decision** — optional side channel only; `regret_evidence_not_deployment_safe` and `regret_evidence_not_risk_gap_leaf` record non-consumption by `Safe` / capacity leaf.
4. **Positive measured path** — `PositiveMeasuredPathCertificate` = legitimacy + `PathCoversEffectiveController` + `NoBypassOfMeasuredPath`; `MB4a` unchanged; no positive→integrity axiom yet (Phase 3).
5. **Transition channel / MB10** — `SystemTransition` in `Chokepoint`; `conservedPropertyAuditChannel` + `ConservedPropertySignatureVerifiable_of_chokepoint` + `true_harm_bound_of_successor_safe_step_via_chokepoint`.

**Gate:** each interface has a concrete consumer or named non-consumer theorem; `lake build` + spine/axiom checks pass.

### Phase 3 — bridge decision

**Decided 2026-08-02** (user confirmation). Interactive options summary: canvas `phase3-bridge-options.canvas.tsx`.

| Interface | Decision | New `MB*`? | Follow-up |
|---|---|---|---|
| **Misspec / nonrealizability** | **A — ambient `MB1`/`MB9` + defeaters + `EpistemicCoverageEvidence`; document in prose** (field index + plan; optional App B/G split of `MB9` antecedent later) | No | Prose in `reference/field-agendas/field-agenda-index.md`; no `MB12` |
| **Regret ⇒ Safe** | **Keep `SystemRegretSafetyEvidence` as non-consumer side channel**; do not fold into `MB11` or `RiskGap` | No | TODO: optional numeric harm leaf (`DeploymentHarmBounded` consumer) if book adopts expected-harm architecture |
| **Logical uncertainty / reflection** | **Keep split** — reflection via `LobTiling`; logical induction exclude-by-reference / matrix neighborhood of `MB5`/`MB7d` only | No | No LI finite module unless catalog demand rises |
| **Positive path → integrity** | **Keep `PositiveMeasuredPathCertificate` structure**; no positive→integrity axiom yet; `MB4a` stays one-way | No (maybe **MB4b** later) | TODO: CIRIS composite consumer; try derive from `MB1`/`MB7a` before threading a bridge |
| **MB10 chokepoint reading** | **Keep `ConservedPropertySignatureVerifiable_of_chokepoint`** as unnumbered interface axiom | No (already `MB10`) | TODO: try to prove or better type the interface axiom; optional axiom-budget headline |

**Package:** no new bridge numbers in this pass. App B/matrix sync remains a separate authorized pass.

If a future pass accepts a new bridge (e.g. **MB4b** for positive path), add its defeater, independence witness, axiom-ledger entry, README/App G/App B documentation, and graph node in the same change.

### Phase 4 — verification for any later Lean implementation

1. `lake -d formal build`
2. inspect `#print axioms` for every new headline theorem
3. `python3 formal/scripts/check_axiom_budget.py`
4. `python3 formal/scripts/check_spine_model.py`
5. add finite counterexample theorem names to the reader-facing proof/counterexample/bridge ledger
6. update `formal/README.md`, Appendix G, App B, assumptions/uncertainty ledgers, and `metadata/TODO.md`
7. run `make check`; build the PDF only if manuscript/appendix text changes

## Recorded decisions (Phase 3, 2026-08-02)

- **No new bridge numbers** in this pass (`MB12` rejected).
- **Misspec:** ambient `MB1`/`MB9` + defeater vocabulary + `EpistemicCoverageEvidence`; finite counterexamples in `Nonrealizability.lean`; prose documented in field index.
- **Regret:** side channel only; reject unconditional regret→`Safe`; numeric harm leaf deferred.
- **Logical uncertainty / reflection:** keep split; no LI bridge.
- **Positive path:** structure retained; `MB4a` unchanged; CIRIS-driven derivation or **MB4b** deferred.
- **MB10 chokepoint:** interface axiom retained; prove-or-type improvement deferred.
- **Unchanged bridge labels:** `MB11`, `MB4a`, `MB8` with existing directional/opacity caveats.
- **Next authorized surfaces:** App B/G prose sync; optional **MB4b** if CIRIS consumer needs positive export in Lean.
