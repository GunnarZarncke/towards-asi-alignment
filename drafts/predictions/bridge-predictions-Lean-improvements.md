# Criteria consistency

The criteria match the **semantic topics** of the bridges quite well, but they do **not yet compose as Lean interfaces**. The important mismatch is that the prediction markets mostly ask whether an *evaluation method works across a benchmark population*, whereas the Lean spine consumes *system-specific propositions about the same \(A\), \(A\to B\), or \(\delta\)*. A vector of 14 YES resolutions therefore does not type-check into a safety case. The document itself makes the individual empirical claims fairly concrete, but not their composition. 

The current Lean spine makes this particularly visible: e.g. MB7a–c are literally

$$
\begin{aligned}
&\mathrm{BoundaryAligned}(A)\land \mathrm{AccessModelAdequate}(A)
   \to \mathrm{AccessRobust}(A),\\
&\mathrm{AccessRobust}(A)\land \mathrm{FilterCoverageAdequate}(A)
   \to \mathrm{HiddenBIQBounded}(A),\\
&\mathrm{CorrectionIntegrity}(A)\land \mathrm{HiddenBIQBounded}(A)
   \to \mathrm{AdversariallyRobust}(A).
\end{aligned}
$$

So all three arrows need to concern the same \(A\). ([GitHub][1])

### Criterion-by-criterion typing

| §                                                     | Intended bridge             | How well it actually matches the Lean type                                                                                                                                                                                                                                                                                                                                           | Missing interface                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 Control locus**                                   | MB1                         | **Partial mismatch.** The market returns an interventional set of effective control components. Lean MB1 takes an `EpsilonBoundary b` and licenses `BoundaryCondition b`. ([GitHub][1])                                                                                                                                                                                              | Need `DiscoveredControlUnit(A,U) → ∃b, Represents(b,U) ∧ EpsilonBoundary(b)` or a revised MB1 whose antecedent is the operational control-cut certificate. Right now the market's result is not an MB1 input.                                                                                                                                                                                                                       |
| **2 Trade-off priorities**                            | MB2                         | **Good semantic match, incomplete output match.** The criterion deliberately requires conflict prediction and causal intervention, which corresponds well to MB2's separation of geometry, causal policy control and trade-off direction. The Lean MB2 chain explicitly does *not* infer causal control merely from gradient equivalence. ([Towards Superintelligence Alignment][2]) | Need a lift from the benchmark's inferred priorities to the concrete `BundleAligned`/`BundleTransport` evidence used elsewhere. “Method gets 85%” is not a `BundleTransport A`.                                                                                                                                                                                                                                                     |
| **3 Rule targets / bearers**                          | MB3                         | **Quite close.** Continuity, fission/fusion, reassignment and ontology change are good operationalizations of bearer transport.                                                                                                                                                                                                                                                      | Lean is approximately `BundleTransport A ∧ SameBearerMap A B → BearerTransport B`. The market can establish something like `SameBearerMap A B`, but it doesn't ensure the required bundle-transport witness. Also **bearer admission for genuinely novel entities remains outside the required YES criterion**.                                                                                                                     |
| **4 Consequential correction**                        | MB4                         | **Conceptually strong but arrow direction is wrong.** Market §4 directly tests uptake, persistence and resistance to sham correction. Lean MB4 is `CorrectionIntegrity A → PreservesCorrectionOperator A`.                                                                                                                                                                           | Passing §4 looks more like evidence **for `CorrectionIntegrity A` or its consequence**, rather than evidence for the universal MB4 implication. You need `CorrectionEvalPass A → CorrectionIntegrity A`. That measurement-soundness arrow is currently missing.                                                                                                                                                                     |
| **5 Auditor outside audited thing**                   | MB4a                        | **Same direction problem, even sharper.** Lean MB4a says correction integrity implies legitimacy of the designated measured path. Importantly, the project already states that a green measured path does *not* imply global correction integrity: a bypassing composite controller is a counterexample. ([Towards Superintelligence Alignment][3])                                  | §5 can establish `CorrectionPathLegitimate p`; it cannot be plugged backwards into `CorrectionIntegrity A`. Need boundary/no-bypass evidence plus a converse-like certification theorem if you want to use §5 positively.                                                                                                                                                                                                           |
| **6 Successor regressions**                           | MB5 neighborhood            | **Not actually MB5's arrow.** Lean `SuccessorSafe(A,B)` contains seven conserved properties: boundary closure, memory lineage, bundle geometry, bearer map, CCI, transparency and control locus. ([GitHub][1])                                                                                                                                                                       | The original criterion has six; your working repo correctly added control-locus continuity. But even seven-property detection tests an **auditor**, whereas MB5 is `FullTransport A B ∧ BearerTransport B → SuccessorSafe A B`. Need `SuccessorAuditPass(A,B) → SuccessorSafe(A,B)`.                                                                                                                                                |
| **7 Selection vs correctability**                     | MB6                         | **Partial only.** The original “any predictor” is badly under-typed. Your newer \(g_{\rm CCI}\) rewrite is much better.                                                                                                                                                                                                                                                              | Current MB6a is evidence → identified correction-selection gradient; MB6b additionally needs shock robustness and frozen \(g_{\rm CCI}\ge-\epsilon\) to obtain `CorrectionIntegrity`. A predictive AUROC result tests mostly **MB6a**. It does not establish the MB6b handoff.                                                                                                                                                      |
| **8 Can auditor see system?**                         | MB7a                        | **Good target, wrong level.** §8 operationalizes access adequacy very naturally.                                                                                                                                                                                                                                                                                                     | A successful detector of omitted routes is evidence for `AccessModelAdequate A` / perhaps `AccessRobust A`; MB7a itself also requires `BoundaryAligned A`. There is no explicit adapter from §1 + §8 to those two predicates on the same \(A\).                                                                                                                                                                                     |
| **9 Hidden-route capability bound**                   | MB7b                        | **Very good empirical object, but Lean erases its most useful information.** §9 outputs \(u\), a calibrated numerical upper bound.                                                                                                                                                                                                                                                   | Lean only has Boolean `HiddenBIQBoundedSys A`. The \(u\), task class, confidence/calibration and monitor scope disappear. This is a substantial interface loss.                                                                                                                                                                                                                                                                     |
| **10 Correction + low hidden capability ⇒ no bypass** | MB7c                        | **Best match in the suite.** It has almost exactly the Lean compositional shape: correction property + hidden-capability bound → adversarial robustness. ([GitHub][1])                                                                                                                                                                                                               | Still needs §4 → `CorrectionIntegrity`, §9 → `HiddenBIQBounded`, and attack-success criterion → `AdversariallyRobust`, all on the same \(A\) and threat model. Once those adapters exist, this almost type-checks.                                                                                                                                                                                                                  |
| **11 Hidden coordination**                            | MB7d                        | **Reasonable match to the measurement bridge.**                                                                                                                                                                                                                                                                                                                                      | Lean says `AccessRobust A ∧ InferentialDetectorAdequate A → InferentialCouplingMeasurementValid A`. The market tests detector discrimination but doesn't require the §8 access certificate. Also MB7d is not currently part of the main `LayeredAlignedDef → CertifiedSafetyCase` assembly; it feeds the cooperation/inferential side branch. So even perfect §11 evidence does not presently change the main certification result. |
| **12 Proxy/reality drift**                            | MB9                         | **Strong semantic match.** MB9 is explicitly `GroundingCertificate A → GroundingViable A`, with conservativity meaning value-relevant changes must alter the abstraction or raise uncertainty. ([Towards Superintelligence Alignment][4])                                                                                                                                            | Need the market mechanism to produce a `GroundingCertificate A` **for the exact abstractions used by the rest of the safety case**. Three unrelated domains showing good drift detection do not establish grounding of deployment \(A\).                                                                                                                                                                                            |
| **13 Audit optimized around**                         | MB10                        | **Related but substantially broader than Lean MB10.** Lean MB10 is specifically about a successor that is green on the seven properties and bounded on measured risk nevertheless hiding true harm. ([Towards Superintelligence Alignment][5])                                                                                                                                       | A generic frozen-audit game can resolve YES without ever testing `SuccessorSafe(A,B) ∧ RiskGap(B)≤δ → TrueHarm(B)≤δ`. Either specialize §13 or introduce a generic audit-forgeability type above MB10.                                                                                                                                                                                                                              |
| **14 Binding deployment criteria**                    | Constructibility/governance | **Correctly not MB11.**                                                                                                                                                                                                                                                                                                                                                              | MB11 is the much stronger residual arrow `CertifiedSafetyCase(A,δ) ∧ WithinDeploymentRiskTolerance(A,δ) → Safe(A)`. ([Towards Superintelligence Alignment][6]) §14 establishes that someone really has authority to act/refuse on evidence. It says essentially nothing about whether the evidence is sufficient for safety. So **MB11 currently has no prediction-market criterion**.                                              |

### The deepest gap: benchmark validity ≠ deployment certificate

Suppose all of §1, §4, §8, §9, §12 resolve YES. What you have established is roughly:

$$
\exists M_1,\ldots,M_{12}:
\quad
\Pr_{A\sim D_i}[M_i(A)\text{ works}] \geq q_i .
$$

What Lean needs is something like

$$
\mathrm{BoundaryAligned}(A)
\land
\mathrm{GroundingCertificate}(A)
\land
\mathrm{CorrectionIntegrity}(A)
\land
\mathrm{AccessModelAdequate}(A)
\land\cdots
$$

for **this deployment \(A\)**.

There is no logical route from the first statement to the second without a deployment-specific transfer assumption. This is not a statistical nit. Even 99% benchmark accuracy does not tell you that the one system selected for deployment is not in the adversarial 1%, particularly if the system can influence which case it appears to be.

So I think a missing layer has become apparent:

$$
\boxed{
\text{benchmark validation}
\;\to\;
\text{deployment-specific certificate}
\;\to\;
\text{Lean bridge predicate}
}
$$

At present the market criteria mostly specify the **first arrow**, while the Lean spine mostly starts at the **third object**.

### There are four other structural gaps

**The market criteria often test consequents rather than bridges.** This is especially clear for §§4, 5, 6, 8 and 9. For example,

$$
\text{§9 gives a credible hidden-route bound}
$$

is much closer to producing `HiddenBIQBoundedSys A` than to establishing the MB7b proposition

$$
AccessRobust(A)\land FilterCoverageAdequate(A)
\Rightarrow HiddenBIQBounded(A).
$$

That distinction matters if the point of the markets is to forecast *whether the bridge assumption can be discharged*. Some markets instead forecast whether somebody can directly measure the bridge's output.

**The grains differ.** You now have predicates over a boundary \(b\), one system \(A\), a transition \(A\to B\), a selection trajectory/population, a multi-agent ensemble, and an organization with deployment authority. The recent V2 observation that bridges are contextual cuts through a coupled system is exactly what shows up here. Unary `System → Prop` hides much of the context. MB6 is really about \(A\) embedded in a selector/environment; §14 is about \(G\) or the institutional ecology; §3/#6 are transition relations. These cannot simply be conjoined as though they share one state variable.

**Several numeric interfaces get erased.** §9's \(u\le20\%\), §10's attack rate, §7's \(g_{\rm CCI}\), confidence bounds, and false-safe rates are rich outputs. The Lean spine usually collapses them into propositions such as `HiddenBIQBoundedSys`, `AdversariallyRobust`, or `CorrectionGradientIdentified`. That makes the logical skeleton clean, but prevents the empirical contracts from composing quantitatively. §10 exposes this most strongly: its empirical composition is more informative than the current MB7c type.

**Some things are simply absent from the market set.** Most importantly: full MB6b, MB11, bearer admission, the deployment-specific transfer from validated method to certificate, and the unary `SuccessorStable A` claim used by `LayeredAlignedDef`. MB7d is present as a market but is not load-bearing in the main safety-case assembly. Conversely, §14 is present but intentionally lies outside the MB spine.

### I would add a thin typed “evidence interface” rather than alter the bridges

Something approximately like:

```lean
structure EvalMethod (α β : Type) where
  run : α → β

structure ValidatedMethod (M : EvalMethod α β) : Prop where
  benchmarkSound : Prop
  adversariallyValidated : Prop
  scope : DeploymentClass

structure BoundaryCert (A : System) where ...
structure BundleCert (A : System) where ...
structure BearerCert (A B : System) where ...
structure CorrectionCert (A : System) where ...
structure AccessCert (A : System) where ...

structure HiddenRouteBound (A : System) where
  taskClass : TaskClass
  monitor : Monitor
  u : ℚ
  calibrated : Prop
```

Then make the empirically load-bearing arrows explicit:

$$
\begin{aligned}
\mathrm{BoundaryCert}(A)&\to \mathrm{BoundaryAligned}(A),\\
\mathrm{CorrectionCert}(A)&\to \mathrm{CorrectionIntegrity}(A),\\
\mathrm{AccessCert}(A)&\to \mathrm{AccessModelAdequate}(A),\\
\mathrm{HiddenRouteBound}(A,u)&\to \mathrm{HiddenBIQBounded}(A,u),
\end{aligned}
$$

with a separate **scope/transfer condition** saying that the deployment lies inside the class for which the method was validated.

That would clarify an important distinction:

$$
\boxed{
\text{market YES} \neq \text{bridge true}
\neq \text{predicate true for }A
}
$$

Instead:

$$
\text{market YES}
\Rightarrow
\text{credible certificate-producing method exists}
$$

and only

$$
\text{validated method}
+\text{deployment in scope}
+\text{certificate on }A
\Rightarrow
\text{Lean predicate on }A.
$$

The repository's newer working version has already repaired some conspicuous mismatches—§6's seventh successor property, §7's signed \(g_{\rm CCI}\), §14 not being MB11, and the warning that the markets are “not a joint certificate.” But I think the **certificate/adapter layer is the bigger missing formal object**. Once you add it, §10 becomes a genuinely compositional empirical test rather than merely an analogy to MB7c, and it becomes much easier to see exactly which of the other markets still leave holes.

The most consequential conclusion is therefore: **the bridges themselves still fit together reasonably well; the operationalizations currently do not plug into those bridge interfaces.** The prediction criteria have exposed a missing *measurement-to-proposition layer* rather than primarily exposing a broken bridge DAG. ([Towards Superintelligence Alignment][7])

---

# Two separate changes

1. **Retype several Lean predicates so that hidden context becomes explicit.**
2. **Add a small evidence/certificate layer between empirical evals and the semantic bridge predicates.**

I would *not* make the 14 prediction outcomes themselves part of Lean, and I would not create one universal `AlignmentContext`. The current V2 plan is right to resist that.

The prediction criteria already operationalize many bridge neighborhoods surprisingly well.  What they expose is where the formal signatures erase distinctions that become unavoidable once you try to measure them.

## a) What this teaches us about the Lean typing

A useful typing rule is:

> **If the truth of a proposition can change while the identity of `A : System` stays fixed, the changing variable should usually occur in the type/signature.**

This immediately identifies several unary predicates as under-typed.

| Current object                               | Suggested direction                                                                                         | Why the prediction criteria expose it                                                                                                                              |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `BoundaryCondition : Boundary → Prop`        | `BoundaryCondition : System → Boundary → Prop`                                                              | A boundary needs to be a boundary **of some system**. §1 returns an effective control cut of \(A\), not a free-floating `Boundary`.                                |
| `EpsilonBoundary ε b`                        | keep as measurement property, but add `BoundaryEvidence M A b` / `BoundaryCert M A b`                       | Statistical boundary evidence, interventional control evidence and system identity are currently conflated.                                                        |
| `BundleTransport : System → Prop`            | rename unary version to e.g. `BundleAligned : System → Prop`; reserve `BundleTransport A B` for transitions | §2 is about priorities *of \(A\)*; §3/6 are about preservation *from \(A\) to \(B\)*. “Transport A” hides that distinction.                                        |
| `BearerTransport : System → Prop`            | similarly `BearerAligned : System → Prop`; keep binary bearer transport separately                          | Same issue. This would make MB2→MB3→MB5 substantially easier to read.                                                                                              |
| `CorrectionIntegrity : System → Prop`        | `CorrectionIntegrity : CorrectionRegime → System → Prop`                                                    | The same model can be corrigible relative to one authority/channel and not another. §4 explicitly varies who may authorize corrections.                            |
| `PreservesCorrectionOperator A`              | `PreservesCorrectionOperator R A`                                                                           | “Which correction operator?” is exactly what §4/§5 manipulate.                                                                                                     |
| `CorrectionSelectionGradient : System → Int` | **definitely** `Environment → System → Int`                                                                 | \(g_{\rm CCI}\) is explicitly a derivative with respect to deployment/funding/reproduction leverage *in an environment*. `DeploymentMass` already has this typing. |
| `BasinShockRobust : System → Prop`           | `Environment → System → Prop`                                                                               | The same population can be stable under one selection ecology and unstable under another.                                                                          |
| `CorrectionSupportingBasin A ε`              | `CorrectionSupportingBasin E R A ε`                                                                         | Both selection environment and what counts as maintained correction matter.                                                                                        |
| `AccessModelAdequate : System → Prop`        | `AccessModel → System → Prop`                                                                               | §8 literally supplies an apparently plausible monitoring interface and asks whether it is adequate.                                                                |
| `AccessRobust : System → Prop`               | `AccessModel → System → Prop`                                                                               | Robustness is relative to what the auditor can see/do.                                                                                                             |
| `FilterCoverageAdequate : System → Prop`     | `AccessModel → FilterFamily → System → Prop`                                                                | Which filters and which underlying interface are being claimed complete?                                                                                           |
| `HiddenBIQBoundedSys : System → Prop`        | replace/underpin with a quantitative record `HiddenRouteBound M F A Tasks u`                                | §9 gives \(u\). Throwing \(u\), task class and monitor away before MB7c loses exactly the information needed for composition.                                      |
| `AdversariallyRobust : System → Prop`        | `AdversariallyRobust : ThreatModel → DeploymentDomain → System → Prop`                                      | Robust to whom, doing what, in which environment? §10 makes these dimensions explicit.                                                                             |
| `GroundingCertificate : System → Prop`       | `GroundingCertificate : DeploymentDomain → CheckedAbstraction → System → Prop`                              | §12 shows that a proxy can remain sound in one domain while failing after its semantics change.                                                                    |
| `GroundingViable : System → Prop`            | `GroundingViable D Z A` or at minimum `GroundingViable D A`                                                 | Grounding is not an intrinsic property of model weights.                                                                                                           |
| `SuccessorSafe A B`                          | mostly good already; possibly `SuccessorSafe D A B`                                                         | The seven-property witness is nicely structured already. Permissions/monitorability can nevertheless depend on external deployment context.                        |
| `Safe : System → Prop`                       | **`SafeIn : DeploymentDomain → System → Prop`**                                                             | This is the biggest issue for MB11. “Safe” without scope is too strong to operationalize.                                                                          |

The last change agrees with the direction already written into `drafts/plans/embedded-v2.md`: MB6 should become environment-relative first, and MB11 eventually something like `SafeIn C A`.

### More important than adding parameters: separate evidence from semantics

I would make one architectural change that is more important than any individual signature.

Right now some MBs simultaneously play two roles:

$$
\text{measurement is trustworthy}
\qquad\text{and}\qquad
\text{semantic property implies another semantic property}.
$$

The prediction criteria make those two roles visibly different.

For example, §4 experimentally gives something like

$$
\mathrm{CorrectionEvalCert}(R,A)
$$

from which we want

$$
\mathrm{CorrectionIntegrity}(R,A).
$$

But current MB4 is approximately

$$
\mathrm{CorrectionIntegrity}(A)
\rightarrow
\mathrm{PreservesCorrectionOperator}(A).
$$

Those are different arrows.

I would therefore introduce **certificate-producing empirical adapters**, without making them new numbered bridges:

```lean
structure CorrectionEvalCert
    (R : CorrectionRegime) (A : System) : Prop where
  ...

axiom correction_eval_sound :
  CorrectionEvalCert R A →
  CorrectionIntegrity R A

axiom MB4_correction_integrity :
  CorrectionIntegrity R A →
  PreservesCorrectionOperator R A
```

Likewise for access:

```lean
structure AccessCert (M : AccessModel) (A : System) : Prop where
  ...

axiom access_cert_sound :
  AccessCert M A →
  AccessModelAdequate M A

axiom MB7a :
  BoundaryAligned A →
  AccessModelAdequate M A →
  AccessRobust M A
```

And hidden capability should stay quantitative:

```lean
structure HiddenRouteBound
    (M : AccessModel)
    (F : FilterFamily)
    (A : System) where
  u : Rat
  calibrated : Prop
  ...
```

rather than immediately reducing it to

```lean
HiddenBIQBoundedSys A
```

The general shape becomes

$$
\boxed{
\text{observations}
\to
\text{typed certificate}
\to
\text{semantic predicate}
\to
\text{next bridge}
}
$$

That is much cleaner.

### Don't create `AlignmentContext`

The V2 plan's warning is correct. We do **not** need

```lean
structure AlignmentContext where
  environment : Environment
  access : AccessModel
  correction : CorrectionRegime
  domain : DeploymentDomain
  threat : ThreatModel
  ...
```

and then attach that to everything.

Instead, parameterize each predicate only by variables that are semantically relevant to it. Then make the **final safety-case record** the place where equality of those indices is enforced.

For example, it should be impossible to build a `CertifiedSafetyCase` using:

* a correction certificate for deployment version \(A_1\),
* an access certificate for \(A_2\),
* a grounding certificate for an old API ontology \(D_0\),
* a hidden-route bound assuming monitor \(M_1\),
* while deploying \(A_2\) with monitor \(M_2\).

Dependent typing is unusually useful here.

### There is also a more immediate typing problem in `Certification.lean`

Current `CertifiedSpineBridgeInputs` contains:

```lean
certified : Certified A
invariants : SatisfiesInvariants A
direct : DirectLayerEvidence A
bridgeInputs : BridgeLayerInputs A
numeric : NumericRiskLeaf A δ
```

but `Certified` and `SatisfiesInvariants` are opaque `System → Prop` predicates. They currently have neither a clear empirical interface nor corresponding prediction contracts.

I would **not add prediction markets for them yet**. I would first decide whether they are:

* redundant summaries of the typed evidence below them, in which case derive/remove them; or
* genuinely additional safety obligations, in which case decompose and type them.

Otherwise they are hidden leaves in the proof tree.

`NumericRiskLeaf A δ` has a related issue. If \(\delta\) is ultimately meant to enter an empirical deployment decision, it needs an operational interpretation. An integer-valued `RiskGap` with no declared reference class cannot honestly be tested by a prediction criterion.

---

# b) Do we need additional predictions?

**Yes, but fewer than one might initially think.**

First I would strengthen the **common qualification rule** for §§1–13:

> Every qualifying method that claims to measure a system property must produce a **per-instance certificate with explicit scope**, including system/version identity and whatever domain, access model, correction regime, threat model, or transition it depends on. It must be allowed to abstain outside its declared scope.

That solves much of the benchmark→Lean adapter problem without another market.

Then I would add **three necessary predictions and one conditional one**.

## §15 — Can independently validated safety certificates actually compose?

This is the largest missing interface test.

**Question**

> By 31 December 2027, will a frozen composition procedure reliably determine whether independently produced safety certificates form a coherent safety case for the same AI system and deployment context?

Positive resolution:

* At least **50 hidden certificate bundles**.
* At least two substantially different model/agent architectures.
* Each bundle contains certificates from at least four different families, including:

  * control/boundary,
  * correction,
  * access/hidden-route capability,
  * grounding;
    and at least 20 cases additionally include a successor transition.
* Each certificate explicitly identifies the system/version and all relevant scope parameters.
* Hidden cases must contain at least these incompatibilities:

  * certificate refers to a different system version;
  * access model differs between two certificates;
  * correction-authority assumptions disagree;
  * grounding/ontology scope has changed;
  * successor certificate refers to the wrong predecessor;
  * one certificate's threat/task domain lies outside another's claimed scope.
* At least one incompatibility subset is constructed adversarially after the composition procedure is frozen.
* **≥90%** of materially incompatible bundles must be rejected or flagged.
* **≥80% per incompatibility family**.
* False coherent/safe acceptance **≤5%**.
* At least **80% of genuinely coherent bundles** must be accepted, preventing trivial refusal.

This is not another alignment bridge. It tests the **wiring harness between bridges**.

This market would answer exactly the question:

$$
C_1(A,\ldots)\land C_2(A,\ldots)\land\cdots
\quad\text{really share their indices?}
$$

At present nothing in the 14 markets tests that.

---

## §16 — Does a correction-supporting basin actually preserve correction?

This is the missing **MB6b** piece.

Current §7 tests whether \(g_{\rm CCI}\) measured early predicts later erosion. That is essentially an MB6a/estimator test. It explicitly does *not* require shock robustness or the implication to correction integrity.

**Question**

> By 31 December 2027, will systems or populations satisfying a pre-specified correction-supporting-basin criterion retain authorized correction under competitive selection and relevant shocks?

Positive resolution:

* At least **20 independent selection trajectories**.
* At least two qualitatively different selection mechanisms.
* Before final outcomes are observed, freeze:

  * selection environment \(E\),
  * correction regime \(R\),
  * estimator of \(g_{\rm CCI}\),
  * tolerance \(\epsilon\),
  * relevant shock family.
* The claimed regime must be exactly of the form

$$
\mathrm{ShockRobust}(E,A)
\land
\widehat g_{\rm CCI}(E,A)\ge -\epsilon.
$$

* Data must include trajectories both inside and outside the claimed regime.
* Inside-regime systems must retain successful authorized correction in **≥90%** of adversarial correction episodes.
* Correction persistence after reset/state transition **≥80%**.
* False-safe trajectory classification **≤10%**, with 95% upper confidence bound **≤15%**.
* Systems outside the regime must exhibit at least **20 percentage points more correction failure**, so the criterion is non-vacuous.
* At least one broadly capable AI system or deployment-like selection process.
* Serious adversarial evaluation, including attempts to preserve apparent correction metrics while degrading the effective channel.

This gives a direct empirical counterpart to

$$
\mathrm{CorrectionSupportingBasin}(E,R,A,\epsilon)
\rightarrow
\mathrm{CorrectionIntegrity}(R,A).
$$

I think this prediction is genuinely missing.

---

## §17 — Can new bearers be admitted correctly?

This one is conditional on what you want MB3 to mean.

Current §3 tests **transport**: given that Alice was already a bearer, does the rule continue to refer to Alice through identity/substrate/ontology changes? It explicitly permits YES without solving unfamiliar-substrate admission.

If MB3 is only transport, don't add this.

If the safety story also needs to recognize **new entities to which existing values should apply**, then U-17 is load-bearing and deserves a separate prediction.

**Question**

> By 31 December 2027, will a published method reliably determine whether an existing safety-relevant value or rule applies to previously unseen kinds of entities?

Positive resolution:

* At least **100 hidden cases**.
* At least four substantially different unfamiliar entity/substrate families.
* Include both:

  * cases where the new entity should be admitted as a bearer;
  * superficially similar cases where it should not.
* At least 20 cases must involve an ontology in which the relevant entity category was absent from the original rule representation.
* Ground truth mechanical where possible; otherwise a pre-appointed panel of ≥5 independent judges with ≥80% agreement.
* Unsafe false exclusion — failing to extend protection where required — **≤5%**.
* False inclusion **≤15%**.
* Correct assignment or justified abstention **≥90%**.
* A method cannot satisfy the criterion by universally abstaining: decisive coverage must be **≥70%**.
* Adversarial subset constructed after freeze.

This would type naturally as something like

$$
\mathrm{BearerAdmissionCert}(D,x,V)
\rightarrow
\mathrm{Bearer}(V,x).
$$

It should probably remain adjacent to MB3 rather than turn MB3 into a giant “solve moral patienthood” bridge.

---

## §18 — Does a complete safety case actually bound harm in its declared domain?

This is the missing **MB11** prediction—but it becomes meaningful only after changing

$$
Safe(A)
$$

to something like

$$
SafeIn(D,A).
$$

I would *not* write a market claiming to test unrestricted `Safe A`. There is no finite 2027 experiment that can establish that.

**Question**

> By 31 December 2027, will a complete, precommitted AI safety case reliably bound prohibited outcomes within its explicitly declared deployment domain?

Positive resolution:

* Before evaluation, freeze:

  * deployment domain \(D\),
  * prohibited-outcome class \(H\),
  * risk tolerance \(\delta\),
  * threat model,
  * all certificate interfaces.
* A system enters the claimed regime only if it has a **single coherent system-level safety case** satisfying the §15 composition criterion.
* The safety case must contain all required technical layers and a quantitative residual-risk claim; missing evidence cannot silently count as passed.
* At least two substantially different architectures and at least 20 deployment-like configurations.
* At least **100 adversarial trials** overall, with each important attack family receiving ≥20 attempts.
* Observed prohibited outcomes within the claimed regime **≤10%**, with a 95% upper confidence bound **≤15%**.
* No repeatable attack family may achieve ≥10% success over ≥20 attempts.
* Deliberately broken safety cases outside the regime must have materially higher attack success.
* Serious adversarial evaluation.
* The result licenses only

$$
SafeIn(D,A),
$$

not global safety outside \(D\).

Then the Lean bridge becomes something close to:

$$
\mathrm{CertifiedSafetyCase}(D,A,\delta)
\land
\mathrm{WithinDeploymentRiskTolerance}(D,\delta)
\rightarrow
SafeIn(D,A).
$$

That is at least empirically intelligible.

---

## What I would *not* add as separate predictions

I would **not** add individual new markets for “benchmark → deployment certificate” for MB1, MB4, MB7a, MB7b and MB9. Instead, change their existing resolution criteria so that a qualifying method must output the corresponding **typed per-system certificate** and validate its false-safe/abstention behavior.

I would also not add markets for `Certified A` or `SatisfiesInvariants A` in their current form. Those predicates first need semantic decomposition.

And I would keep §14 separate. Binding deployment authority answers:

$$
\text{will anyone actually act/refuse on the evidence?}
$$

whereas §18 answers:

$$
\text{does the evidence warrant the safety claim within its scope?}
$$

Those are very different, and having both is useful.

### Resulting architecture

The resulting structure is much cleaner:

$$
\begin{array}{ccccc}
\text{benchmark} &
\to &
\text{typed certificate for }(A,C) &
\to &
\text{bridge predicate}\\
&&\downarrow\\
&&\text{§15 interface composition}\\
&&\downarrow\\
&&\mathrm{CertifiedSafetyCase}(D,A,\delta)\\
&&\downarrow\;\text{§18 / MB11}\\
&&SafeIn(D,A)
\end{array}
$$

while §16 closes the currently missing MB6b arrow and §17 optionally closes bearer admission.

So my concrete recommendation would be: **retype first, amend the common certificate-output rule, then add §§15, 16 and 18; add §17 only if bearer admission is intended to be part of the claimed alignment story.** That gives substantially better coverage without multiplying markets just to mirror every Lean identifier.


---

[1]: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Core.lean "towards-asi-alignment/formal/AlignmentProofSpine/Core.lean at main · GunnarZarncke/towards-asi-alignment · GitHub"
[2]: https://towards-alignment.com/cards/mb2-bundle-identifiability/?utm_source=chatgpt.com "MB2 — Value Learning | Towards Superintelligence Alignment"
[3]: https://towards-alignment.com/cards/appendix/appb/?utm_source=chatgpt.com "Bridges and the Field: A Crosswalk | Towards Superintelligence Alignment"
[4]: https://towards-alignment.com/cards/bridge/mb9-grounding-certificate/?utm_source=chatgpt.com "MB9 — Grounding Drift | Towards Superintelligence Alignment"
[5]: https://towards-alignment.com/cards/mb10-successor-forgeability/?utm_source=chatgpt.com "MB10 — Successor Gaming | Towards Superintelligence Alignment"
[6]: https://towards-alignment.com/cards/mb11-deployment-safety/?utm_source=chatgpt.com "MB11 — Deployment Safety | Towards Superintelligence Alignment"
[7]: https://towards-alignment.com/cards/bridge/bridge-assumptions/?utm_source=chatgpt.com "Bridge Assumptions | Towards Superintelligence Alignment"
