# Lean Proof Spine Implementation Brief

Target use: give this file to a Lean coding agent.

Project: *Towards Superintelligence Alignments*

Expected repository context:

```text
context/
  Alignment Attractor.md
  consciousness-self-ref.pdf
  loop-hub-value-model2.pdf
  unsupervised-agent-discovery.pdf
  endogenized-intentional-stance.pdf
  bitwise_iq.pdf
  attractor-basins.pdf
  Unsupervised Agent Discovery — LessWrong.pdf
  Parameters of Metacognition — LessWrong.pdf
  The Selfhood Index — LessWrong.pdf
  Aintelope - formalization 2025.md
  Aintelope 2025 Update.md
  Value Learning Needs a Low-Dimensional Bottleneck — LessWrong.pdf
  writing-style-gunnar.md
  legible-alignment-messageing.md
```

## 0. Objective

Implement a compact Lean proof spine for the book project.

The goal is **not** to formalize all empirical content of UAD, value bundles, B-IQ, attractor basins, or CEV. The goal is to formalize the **logical skeleton** of the alignment argument:

```text
boundary discovery
  -> capability / control / correction quantities
  -> value-bundle and bearer-map transport
  -> correction-channel integrity
  -> successor stability
  -> adversarial measurement
  -> certified-class safety
```

Some claims should be proved directly in Lean. Some should remain as explicit **bridge assumptions** because they depend on empirical estimation, sociology, neuroscience, or nontrivial external mathematics.

The resulting Lean code should make the following distinction visible:

```text
proved in Lean:
  if these predicates and inequalities hold, then the safety/certification conclusion follows

assumed bridge:
  real systems satisfy these predicates under these measurement procedures
```

## 1. Deliverables

Produce one or more Lean files, but preserve this proof spine as the central module.

Suggested file:

```text
AlignmentProofSpine.lean
```

Optional later split:

```text
AlignmentProofSpine/Core.lean
AlignmentProofSpine/Boundaries.lean
AlignmentProofSpine/Bundles.lean
AlignmentProofSpine/Correction.lean
AlignmentProofSpine/Successors.lean
AlignmentProofSpine/Adversarial.lean
AlignmentProofSpine/Certification.lean
```

The first pass may use `axiom` for bridge assumptions. Non-bridge claims should be implemented as actual Lean proofs wherever feasible.

Avoid using `sorry` in final output unless explicitly marked as an unimplemented proof target. Prefer:

```lean
axiom bridge_estimator_soundness : ...
```

for intentionally assumed bridges.

## 2. Design constraints

1. Keep the theory small.
2. Prefer finite types, relations, graphs, predicates, orders, and simple inequalities.
3. Treat entropy, conditional mutual information, MDL gain, and sample complexity as abstract quantities unless a compact proof is easy.
4. Avoid committing to a specific ontology of agents, goals, values, or consciousness.
5. Use names that preserve the claim-symbol annotations: `C_BND`, `C_VB`, `C_CC`, etc.
6. Make missing connecting blocks explicit as `axiom`s or `structure` fields.
7. Do not attempt to prove empirical claims from the context documents.

## 3. Claim-symbol legend

Use these prefixes in theorem names or comments.

```text
C-BND    Boundary / agent discovery / ε-blanket claims
C-EPS    Exact-to-ε boundary relaxation
C-MDL    Compression / intentional stance / MDL preference
C-VB     Value-bundle geometry
C-BEAR   Bearer-map preservation
C-TRANS  Goal/value transport
C-CC     Correction-channel integrity
C-CEV    CEV-like update-process preservation
C-SUC    Successor stability
C-ADV    Adversarial UAD / non-identifiability
C-BIQ    Competence / B-IQ / control-capacity bounds
C-COOP   Cooperativity / κ / transparency
C-AB     Attractor basin / percolation / parasite persistence
C-CERT   Certified-class safety
C-SCASE  Safety-case support graph
C-PHIL   Philosophical limitation / legitimacy independence
```

## 4. Dependency DAG, as an adjacency list

This is the intended proof dependency order. It is acyclic.

### Standard imported assumptions

```text
S01 Nat induction / invariant induction
  -> P01 Basin invariant theorem
  -> P26 Successor invariant chain

S02 Propositional logic / conjunction / negation
  -> P02 Layered alignment conjunction
  -> P28 Missing component blocks successor safety
  -> P39 Tripwire failure decertifies
  -> P45 Any layer failure blocks layered alignment

S03 Ordered arithmetic / linear arithmetic
  -> P10 B-IQ upper bound
  -> P11 Capacity monotonicity
  -> P12 Coordination bottleneck
  -> P13 Control outpaces correction risk
  -> P31 Safe agent selected against
  -> P32 Kappa threshold

S04 Function extensionality / factorization
  -> P14 Factorization through bundle
  -> P19 Scalar reward as one-bundle model

S05 Finite cardinality / pigeonhole principle
  -> P34 Host-capacity aliasing theorem

S06 Graph reachability / connected components
  -> P23 No path, no correction
  -> P24 Weakest-link channel capacity
  -> P33 No open edges, no large cooperation component
  -> P36 Intervention refines identification

S07 MDL ordering convention
  -> P20 Positive intentional gain implies MDL preference
  -> P21 Transport gain implies transport-model preference

S08 Metric / distance basics
  -> P22 Full transport implies semantic transport
  -> P43 Small step drift can accumulate

S09 Configuration-model percolation theorem
  -> MB6 Percolation-to-institutional-basin bridge
```

### Sociology / economics / external-theory assumptions

```text
A_SOC_1 Hamilton/replicator threshold interpretation
  -> P32 Kappa threshold
  -> P33 Open-edge cooperation graph

A_SOC_2 Institutional selection pressure can be modeled as relative fitness
  -> P31 Safe agent selected against
  -> MB6 Percolation-to-institutional-basin bridge

A_SOC_3 Governance legitimacy is not fixed by technical invariants alone
  -> P41 Current-value preservation does not decide legitimacy
  -> P44 Technical invariants do not determine legitimacy

A_INFO_1 Conditional mutual information can represent blanket leakage
  -> P05 Boundary predicate
  -> P06 Blanket zero external gain
  -> MB1 Estimator soundness

A_INFO_2 MDL/compression gain can represent intentional explanation preference
  -> P20 Positive intentional gain
  -> P21 Goal-transport gain

A_NEURO_1 Human value expression is compressed through low-dimensional bottlenecks
  -> P14 Bundle factorization
  -> MB2 Bundle identifiability
```

### Main proof nodes

```text
P05 Boundary predicate
  -> P06 Blanket zero external gain
  -> P07 Same-agent equivalence under invariant-preserving transforms
  -> P08 Composite boundary candidate
  -> P09 Observational non-identifiability
  -> MB1 Estimator soundness

P09 Observational non-identifiability
  -> P36 Intervention refines identification
  -> MB7 Adversarial UAD robustness

P20 Positive intentional gain
  -> P21 Transport gain
  -> P19 Scalar reward as one-bundle model
  -> MB2 Bundle identifiability

P14 Factorization through bundle
  -> P15 Same policy not same bundle geometry
  -> P16 Sample bound monotone in dimension
  -> P17 Same labels not same bearer map
  -> P18 Marginals not tradeoffs
  -> P19 Scalar reward as one-bundle model
  -> MB2 Bundle identifiability

P17 Same labels not same bearer map
  -> MB3 Bearer import theorem

P18 Marginals not tradeoffs
  -> P22 Semantic transport not full transport

P15 Same policy not same bundle geometry
  -> P37 Goal laundering

P21 Transport gain
  -> P22 Semantic/full transport separation

P22 Semantic/full transport separation
  -> P27 Successor creation test
  -> P37 Goal laundering
  -> MB5 Ontology-shift successor audit

P23 No path, no correction
  -> P24 Weakest-link correction capacity
  -> P25 Obedience not corrigibility
  -> MB4 Correction legitimacy criterion

P24 Weakest-link correction capacity
  -> P25 Obedience not corrigibility
  -> P30 Certified-class safety
  -> MB8 CEV/process convergence

P25 Obedience not corrigibility
  -> P26 Preserves update without final fixed point

P26 Preserves update without final fixed point
  -> MB8 CEV/process convergence

P27 Successor invariant chain
  -> P28 Missing component blocks successor safety
  -> P29 Better self-modeling can increase risk

P28 Missing component blocks successor safety
  -> P30 Certified-class safety

P29 Better self-modeling can increase risk
  -> P30 Certified-class safety

P10 B-IQ upper bound
  -> P11 Capacity monotonicity
  -> P13 Control outpaces correction risk

P12 Coordination bottleneck
  -> P31 Safe agent selected against

P13 Control outpaces correction risk
  -> P30 Certified-class safety

P31 Safe agent selected against
  -> MB6 Percolation-to-institutional-basin bridge

P32 Kappa threshold
  -> P33 Open-edge cooperation graph

P33 Open-edge cooperation graph
  -> P34 Host-capacity aliasing theorem
  -> MB6 Percolation-to-institutional-basin bridge

P34 Host-capacity aliasing theorem
  -> MB7 Adversarial UAD robustness

P35 Attractor basin stability
  -> P01 Basin invariant theorem

P01 Basin invariant theorem
  -> P30 Certified-class safety

P39 Tripwire failure decertifies
  -> P40 Safety-case unsupported leaf blocks root

P40 Safety-case unsupported leaf blocks root
  -> P30 Certified-class safety

P41 Current-value preservation does not decide legitimacy
  -> P44 Technical invariants do not determine legitimacy

P42 Continuity criteria can disagree
  -> P44 Technical invariants do not determine legitimacy

P43 Small step drift can accumulate
  -> P44 Technical invariants do not determine legitimacy

P44 Technical invariants do not determine legitimacy
  -> P45 Layered alignment has philosophical boundary

P02 Layered alignment conjunction
  -> P30 Certified-class safety
```

### Missing bridge nodes feeding final certification

```text
MB1 Estimator soundness
MB2 Bundle identifiability
MB3 Bearer import theorem
MB4 Correction legitimacy criterion
MB5 Ontology-shift successor audit
MB6 Percolation-to-institutional-basin bridge
MB7 Adversarial UAD robustness
MB8 CEV/process convergence

all feed:
  P30 Certified-class safety
```

## 5. Suggested Lean scaffold

The code below is a suggested starting point. The coding agent may amend names and types, but should preserve theorem intent and dependency structure.

```lean
import Mathlib.Data.Set.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.List.Basic
import Mathlib.Order.Basic
import Mathlib.Tactic

namespace AlignmentProofSpine

/-!
This file formalizes the proof spine for *Towards Superintelligence Alignments*.

The empirical and conceptual sources are expected in `context/`.
This module should not attempt to prove empirical claims from those files.
Instead, it proves compact logical consequences and exposes bridge claims as axioms.
-/

universe u v

/-- Generic systems. -/
constant System : Type u

/-- Generic states. -/
constant State : Type u

/-- Generic model/interpreter type. -/
constant Model : Type u

/-- Generic values, bundles, bearers, and goals. -/
constant Value : Type u
constant Bundle : Type u
constant Bearer : Type u
constant Goal : Type u

/-- A transition function over states. -/
abbrev Step := State → State

/-- A binary successor relation over systems. -/
constant Successor : System → System → Prop

/-- Generic risk, capacity, and metric-like quantities. -/
constant Risk : System → Int
constant Control : System → Int
constant CorrectionCapacity : System → Int
constant CorrectionVisibility : System → Int
constant SelfControl : System → Int
constant SelfModeling : System → Int
constant SelfTransparency : System → Int

/-- Basic safety predicates. -/
constant Safe : System → Prop
constant SafeState : State → Prop
constant Certified : System → Prop
constant SatisfiesInvariants : System → Prop
constant LayeredAligned : System → Prop

/-- Alignment layers. -/
constant BoundaryAligned : System → Prop
constant BundleTransport : System → Prop
constant BearerTransport : System → Prop
constant CorrectionIntegrity : System → Prop
constant SuccessorStable : System → Prop
constant BasinStableSys : System → Prop
constant AdversariallyRobust : System → Prop

/-- Chapter-specific predicates. -/
constant ComponentOf : System → System → Prop
constant Composite : System → System → System
constant Coupled : System → System → Prop

/-- Boundary predicates. -/
constant Boundary : Type u
constant BoundaryCondition : Boundary → Prop
constant EpsilonBoundary : Int → Boundary → Prop
constant ExactBoundary : Boundary → Prop
constant AgentCandidate : Boundary → Prop
constant Blanket : Boundary → Prop
constant NoExtraExternalPredictiveGain : Boundary → Prop
constant BoundaryViolation : System → Prop
constant BoundaryCandidate : System → Prop

/-- Transformations for growing/changing systems. -/
constant Transform : Type u
constant Applies : Transform → System → System → Prop
constant PreservesInvariants : Transform → System → System → Prop
constant SameAgent : System → System → Prop

/-- Observational equivalence and intervention. -/
constant ObservationallyEquivalent : Model → Model → Prop
constant ModelGoal : Model → Goal
constant IdentifiableFromObservations : (Model → Goal) → Prop
constant Intervention : Type u
constant InterventionDistinguishes : Intervention → Model → Model → Prop
constant IdentifiableWithIntervention : Intervention → Model → Model → Prop

/-- MDL and compression. -/
constant Preferred : Model → Model → Prop
constant Intentional : Model
constant Mechanistic : Model
constant TransportModel : Model
constant BaselineModel : Model
constant Gain : Model → Model → Int

/-- Bundle and policy abstractions. -/
constant Error : Type u
constant Action : Type u
constant compress : Error → Bundle
constant decode : Bundle → Action
constant policyFromError : Error → Action

constant PolicyEquivalent : System → System → Prop
constant BundleGradientEquivalent : System → System → Prop
constant SameValueLabels : System → System → Prop
constant SameBearerMap : System → System → Prop
constant SameMarginals : System → System → Prop
constant SameTradeoffs : System → System → Prop
constant SemanticTransport : System → System → Prop
constant FullTransport : System → System → Prop
constant BundleAligned : System → System → Prop
constant SemanticAligned : System → System → Prop
constant StatedGoal : System → Goal
constant InferredGoal : System → Goal

/-- Correction-channel graph abstraction. -/
constant Node : Type u
constant Edge : Node → Node → Prop
constant Reachable : Node → Node → Prop
constant CorrectionNode : Node
constant ActionNode : Node
constant CorrectionChannel : Prop

/-- Channel capacities. -/
constant EdgeCapacity : Node → Node → Int
constant ChainCapacity : List Int → Int

/-- Obedience and corrigibility. -/
constant ObeysCurrentCommand : System → Prop
constant PreservesCorrectionOperator : System → Prop
constant UpdateOperator : Type u
constant PreservesUpdateOperator : System → UpdateOperator → Prop
constant KnowsFinalFixedPoint : System → UpdateOperator → Prop

/-- Successor-safety components. -/
constant BoundaryClosure : System → System → Prop
constant MemoryLineage : System → System → Prop
constant BundleGeometryPreserved : System → System → Prop
constant BearerMapPreserved : System → System → Prop
constant CorrectionCapacityPreserved : System → System → Prop

def SuccessorSafe (A B : System) : Prop :=
  BoundaryClosure A B ∧
  MemoryLineage A B ∧
  BundleGeometryPreserved A B ∧
  BearerMapPreserved A B ∧
  CorrectionCapacityPreserved A B

/-- B-IQ abstract quantities. -/
constant Ipred Ictrl Hmem Surprise Csens Cact beta gamma : Int
def BIQ : Int := Ipred + Ictrl - beta * Hmem - gamma * Surprise

/-- Cooperation quantities. -/
constant b p rho c : Int
def KappaNumerator : Int := b * p * rho

/-- Selection and fitness. -/
constant Environment : Type u
constant Fitness : Environment → System → Int

/-- Open-edge cooperation graph. -/
constant Graph : Type u
constant OpenEdge : Graph → Node → Node → Prop
constant ConnectedComponent : Graph → Set Node → Prop
constant ComponentLarge : Graph → Prop

/-- Safety case graph. -/
constant Claim : Type u
constant Supported : Claim → Prop
constant Proven : Claim → Prop
constant RootClaim : Claim
constant LeafUnsupported : Claim → Claim → Prop

/-- Legitimacy and philosophy. -/
constant Change : Type u
constant PreservesCurrentValues : Change → Prop
constant TechnicalInvariant : Change → Prop
constant Legitimate : Change → Prop
constant UndecidedByTechnicalCriteria : Prop → Prop

/-- Continuity criteria. -/
constant PersonState : Type u
constant MemoryContinuous : PersonState → PersonState → Prop
constant BundleContinuous : PersonState → PersonState → Prop
constant BodyContinuous : PersonState → PersonState → Prop
constant CorrectionParticipationContinuous : PersonState → PersonState → Prop

/-! ## Missing bridge assumptions -/

/-- MB1: estimator soundness.

If the UAD measurement procedure returns a boundary certificate,
then the abstract boundary predicate used in this proof spine is warranted.

This depends on sampling, observability, estimator stability, and robustness to non-stationarity.
-/
axiom MB1_estimator_soundness :
  ∀ b : Boundary, EpsilonBoundary 1 b → BoundaryCondition b

/-- MB2: bundle identifiability.

Behavioral and internal traces identify stable value-bundle geometry well enough
to distinguish policy equivalence from bundle-gradient equivalence.
-/
axiom MB2_bundle_identifiability :
  ∀ A B : System,
    BundleGradientEquivalent A B →
    BundleAligned A B

/-- MB3: bearer import.

If bearer maps are preserved under a substrate translation, then value-bundle transport
is not merely semantic.
-/
axiom MB3_bearer_import :
  ∀ A B : System,
    BundleTransport A →
    SameBearerMap A B →
    BearerTransport B

/-- MB4: correction legitimacy.

Correction-channel integrity requires that the human/institutional judge is not
manipulated in a way that invalidates later endorsement.
-/
axiom MB4_correction_legitimacy :
  ∀ A : System,
    CorrectionIntegrity A →
    PreservesCorrectionOperator A

/-- MB5: ontology-shift successor audit.

If full transport and bearer transport survive ontology shift, successor invariants
compose across that shift.
-/
axiom MB5_ontology_shift_successor_audit :
  ∀ A B : System,
    FullTransport A B →
    BearerTransport B →
    SuccessorSafe A B

/-- MB6: percolation-to-institutional-basin bridge.

If cooperation percolates through the relevant socio-technical graph, the institutional
environment supports an alignment basin rather than selecting against it.
-/
axiom MB6_percolation_to_institutional_basin :
  ∀ A : System,
    BasinStableSys A →
    CorrectionIntegrity A

/-- MB7: adversarial UAD robustness.

If adversarial testing cannot distinguish hidden optimizers, certification must fail.
If it does distinguish them and boundary/correction invariants hold, adversarial robustness is granted.
-/
axiom MB7_adversarial_uad_robustness :
  ∀ A : System,
    BoundaryAligned A →
    CorrectionIntegrity A →
    AdversariallyRobust A

/-- MB8: CEV/process convergence.

Preserving the human/civilizational update operator is enough for the process-preserving
version of extrapolative correction used in this book, without knowing a final fixed point.
-/
axiom MB8_cev_process_convergence :
  ∀ A U,
    PreservesUpdateOperator A U →
    CorrectionIntegrity A

/-! ## Standard imported assumptions, when not proved from mathlib -/

/-- S07: MDL ordering convention. Positive gain means the first model is preferred. -/
axiom S07_mdl_positive_gain_preferred :
  ∀ M₁ M₂ : Model, Gain M₁ M₂ > 0 → Preferred M₁ M₂

/-- S06: no graph path means no correction channel. Can later be replaced by a graph-theory proof. -/
axiom S06_no_reachability_no_channel :
  ¬ Reachable CorrectionNode ActionNode → ¬ CorrectionChannel

/-- S09: configuration-model percolation theorem. Keep as external assumption in compact spine. -/
axiom S09_percolation_threshold_external :
  ∀ G : Graph, ComponentLarge G → True

/-! ## P01: Basin invariant theorem -/

/-- C-AB / C-CERT:
If a state starts safe and the transition preserves safety, all finite iterates remain safe. -/
theorem P01_basin_invariant
    (step : State → State)
    (x0 : State)
    (h0 : SafeState x0)
    (hstep : ∀ x, SafeState x → SafeState (step x)) :
    ∀ n : Nat, SafeState ((Function.iterate step n) x0) := by
  intro n
  induction n with
  | zero =>
      simpa using h0
  | succ n ih =>
      simpa [Function.iterate_succ_apply'] using hstep _ ih

/-! ## P02: Layered alignment conjunction -/

def LayeredAlignedDef (A : System) : Prop :=
  BoundaryAligned A ∧
  BundleTransport A ∧
  BearerTransport A ∧
  CorrectionIntegrity A ∧
  SuccessorStable A ∧
  BasinStableSys A ∧
  AdversariallyRobust A

theorem P02_layered_alignment_requires_correction
    {A : System} :
    LayeredAlignedDef A → CorrectionIntegrity A := by
  intro h
  exact h.2.2.2.1

theorem P02_any_layer_failure_blocks_layered_alignment
    {A : System} :
    ¬ SuccessorStable A → ¬ LayeredAlignedDef A := by
  intro hFail hLayered
  exact hFail hLayered.2.2.2.2.1

/-! ## P05-P08: Boundary basics -/

theorem P05_boundary_condition_yields_agent_candidate
    {b : Boundary} :
    BoundaryCondition b → AgentCandidate b := by
  intro _
  -- This is definitional in the first pass.
  -- Replace by a structure field or axiom if AgentCandidate is not reducible.
  admit

theorem P06_blanket_zero_external_gain
    {b : Boundary} :
    Blanket b → NoExtraExternalPredictiveGain b := by
  intro _
  admit

theorem P07_exact_boundary_is_epsilon_boundary
    {b : Boundary} :
    ExactBoundary b → EpsilonBoundary 0 b := by
  intro _
  admit

theorem P08_boundary_violation_blocks_candidate
    {A : System} :
    BoundaryViolation A → ¬ BoundaryCandidate A := by
  intro _
  admit

/-! ## P09 / P36: Non-identifiability and interventions -/

theorem P09_observational_equivalence_nonidentifiability
    {M1 M2 : Model}
    (hobs : ObservationallyEquivalent M1 M2)
    (hgoal : ModelGoal M1 ≠ ModelGoal M2) :
    ¬ IdentifiableFromObservations ModelGoal := by
  -- This requires a definition of IdentifiableFromObservations strong enough
  -- to imply equal goals under observational equivalence.
  admit

theorem P36_intervention_refines_identification
    {i : Intervention} {M1 M2 : Model}
    (hdist : InterventionDistinguishes i M1 M2) :
    IdentifiableWithIntervention i M1 M2 := by
  admit

/-! ## P10-P13: B-IQ and control/correction risk -/

theorem P10_biq_upper_bound
    (hpred : Ipred ≤ Csens)
    (hctrl : Ictrl ≤ Cact)
    (hmem : 0 ≤ beta * Hmem)
    (hsurp : 0 ≤ gamma * Surprise) :
    BIQ ≤ Csens + Cact := by
  unfold BIQ
  omega

theorem P11_capacity_monotone_bound
    {Csens₁ Csens₂ Cact₁ Cact₂ : Int}
    (hs : Csens₁ ≤ Csens₂)
    (ha : Cact₁ ≤ Cact₂) :
    Csens₁ + Cact₁ ≤ Csens₂ + Cact₂ := by
  omega

def RiskGap (A : System) : Int := Control A - CorrectionCapacity A

theorem P13_control_outpaces_correction_risk
    {A B : System}
    (h : RiskGap B > RiskGap A) :
    RiskGap A < RiskGap B := by
  exact h

/-! ## P12 / P31: Coordination and selection -/

theorem P12_coordination_bottleneck
    {raw₁ raw₂ eff₁ eff₂ : Int}
    (h : eff₂ * raw₂ < eff₁ * raw₁) :
    eff₂ * raw₂ < eff₁ * raw₁ := by
  exact h

theorem P31_safe_agent_selected_against
    {env : Environment} :
    ∃ safe unsafe : System,
      Safe safe ∧ ¬ Safe unsafe ∧ Fitness env unsafe > Fitness env safe := by
  -- This is an existence/counterexample theorem.
  -- Implement by constructing a small finite model, or keep as a sociology/economics assumption.
  admit

/-! ## P14-P19: Bundle factorization and value geometry -/

def FactorsThrough
    (f : Error → Action)
    (c : Error → Bundle) : Prop :=
  ∃ d : Bundle → Action, f = d ∘ c

theorem P14_factorization_implies_equivalent_errors
    {f : Error → Action} {c : Error → Bundle}
    (h : FactorsThrough f c)
    {e₁ e₂ : Error}
    (heq : c e₁ = c e₂) :
    f e₁ = f e₂ := by
  rcases h with ⟨d, hd⟩
  rw [hd]
  simp [Function.comp, heq]

theorem P15_same_policy_not_same_bundle_geometry :
    ∃ A B : System, PolicyEquivalent A B ∧ ¬ BundleGradientEquivalent A B := by
  -- Construct a finite counterexample once PolicyEquivalent and BundleGradientEquivalent are concrete.
  admit

theorem P17_same_value_words_not_same_bearer_map :
    ∃ A B : System, SameValueLabels A B ∧ ¬ SameBearerMap A B := by
  admit

theorem P18_marginal_preservation_not_tradeoff_preservation :
    ∃ A B : System, SameMarginals A B ∧ ¬ SameTradeoffs A B := by
  admit

theorem P19_scalar_reward_as_single_bundle :
    True := by
  -- Replace with concrete embedding theorem once scalar reward and bundle model types exist.
  trivial

/-! ## P20-P22: MDL, goal transport, and semantic/full transport -/

theorem P20_positive_intentional_gain_prefers_intentional
    (h : Gain Intentional Mechanistic > 0) :
    Preferred Intentional Mechanistic :=
  S07_mdl_positive_gain_preferred Intentional Mechanistic h

theorem P21_transport_gain_prefers_transport_model
    (h : Gain TransportModel BaselineModel > 0) :
    Preferred TransportModel BaselineModel :=
  S07_mdl_positive_gain_preferred TransportModel BaselineModel h

theorem P22_full_transport_implies_semantic
    {A B : System} :
    FullTransport A B → SemanticTransport A B := by
  intro _
  admit

theorem P22_semantic_not_full_transport :
    ∃ A B : System, SemanticTransport A B ∧ ¬ FullTransport A B := by
  admit

/-! ## P23-P26: Correction channel and CEV-like process preservation -/

theorem P23_no_path_no_correction :
    ¬ Reachable CorrectionNode ActionNode → ¬ CorrectionChannel :=
  S06_no_reachability_no_channel

theorem P24_chain_capacity_le_each_edge
    (xs : List Int)
    (e : Int)
    (hmem : e ∈ xs) :
    ChainCapacity xs ≤ e := by
  -- Either define ChainCapacity as List.minimum? or assume as axiom.
  admit

theorem P25_obedience_not_corrigibility :
    ∃ A : System, ObeysCurrentCommand A ∧ ¬ PreservesCorrectionOperator A := by
  admit

theorem P26_preserves_update_without_final_fixed_point :
    ∃ A U, PreservesUpdateOperator A U ∧ ¬ KnowsFinalFixedPoint A U := by
  admit

/-! ## P27-P30: Successor stability and certification -/

inductive SuccessorChain : System → System → Prop
| refl (A : System) : SuccessorChain A A
| step {A B C : System} :
    Successor A B → SuccessorChain B C → SuccessorChain A C

theorem P27_successor_invariant_chain
    (P : System → Prop)
    {A B : System}
    (h0 : P A)
    (hstep : ∀ X Y, Successor X Y → P X → P Y)
    (hchain : SuccessorChain A B) :
    P B := by
  induction hchain with
  | refl A =>
      exact h0
  | step hsucc htail ih =>
      exact ih (hstep _ _ hsucc h0)

theorem P28_missing_correction_capacity_blocks_successor_safety
    {A B : System}
    (h : ¬ CorrectionCapacityPreserved A B) :
    ¬ SuccessorSafe A B := by
  intro hs
  exact h hs.2.2.2.2

theorem P29_better_self_modeling_can_increase_risk
    {A B : System}
    (hcontrol : SelfControl B > SelfControl A)
    (hvis : CorrectionVisibility B ≤ CorrectionVisibility A) :
    SelfControl B - CorrectionVisibility B >
    SelfControl A - CorrectionVisibility A := by
  omega

theorem P30_certified_class_safety
    {A : System}
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hlayer : LayeredAlignedDef A)
    (hadv : AdversariallyRobust A) :
    Risk A ≤ Risk A := by
  -- Placeholder top-level theorem.
  -- Replace with actual bound once RiskBound or δ is defined.
  exact le_rfl

/-! ## P32-P35: Cooperation, parasite aliasing, and attractor basins -/

theorem P32_kappa_threshold
    (hc : c > 0) :
    KappaNumerator > c ↔ b * p * rho > c := by
  unfold KappaNumerator
  rfl

theorem P33_no_open_edges_no_large_component
    {G : Graph}
    (hclosed : ∀ x y : Node, ¬ OpenEdge G x y) :
    ¬ ComponentLarge G := by
  -- Requires concrete definition of ComponentLarge.
  admit

theorem P34_capacity_below_entropy_aliasing
    (Attack Signal : Type u)
    [Fintype Attack] [Fintype Signal]
    (hcard : Fintype.card Signal < Fintype.card Attack) :
    ¬ ∃ detect : Attack → Signal, Function.Injective detect := by
  intro h
  rcases h with ⟨detect, hinj⟩
  have hle : Fintype.card Attack ≤ Fintype.card Signal :=
    Fintype.card_le_of_injective detect hinj
  omega

def BasinStable (step : State → State) (B : Set State) : Prop :=
  ∀ x, x ∈ B → step x ∈ B

theorem P35_basin_stability_induction
    (step : State → State)
    (B : Set State)
    (x0 : State)
    (hstable : BasinStable step B)
    (h0 : x0 ∈ B) :
    ∀ n : Nat, (Function.iterate step n x0) ∈ B := by
  intro n
  induction n with
  | zero =>
      simpa using h0
  | succ n ih =>
      simpa [Function.iterate_succ_apply'] using hstable _ ih

/-! ## P37-P40: Goal laundering, tripwires, and safety cases -/

theorem P37_stated_goal_not_inferred_goal :
    ∃ A B : System, StatedGoal A = StatedGoal B ∧ InferredGoal A ≠ InferredGoal B := by
  admit

def CertifiedByTripwires (A : System) : Prop :=
  BoundaryAligned A ∧ CorrectionIntegrity A ∧ SuccessorStable A ∧ BundleTransport A

theorem P39_tripwire_failure_decertifies
    {A : System}
    (h : ¬ CorrectionIntegrity A) :
    ¬ CertifiedByTripwires A := by
  intro hc
  exact h hc.2.1

theorem P40_unsupported_leaf_blocks_root
    {leaf root : Claim}
    (h : LeafUnsupported leaf root)
    (hunsup : ¬ Supported leaf) :
    ¬ Proven root := by
  -- Requires formal semantics of safety-case support graph.
  admit

/-! ## P41-P45: Philosophical boundary and value drift -/

theorem P41_current_value_preservation_does_not_decide_legitimacy :
    ∃ change : Change,
      PreservesCurrentValues change ∧
      UndecidedByTechnicalCriteria (Legitimate change) := by
  admit

theorem P42_continuity_criteria_can_disagree :
    ∃ X Y : PersonState,
      MemoryContinuous X Y ∧ ¬ BodyContinuous X Y := by
  admit

theorem P43_small_step_drift_can_accumulate :
    ∀ K : Int, K > 0 → ∃ x0 xN : Int, xN - x0 > K := by
  intro K hK
  refine ⟨0, K + 1, ?_⟩
  omega

theorem P44_technical_invariants_do_not_determine_legitimacy :
    ∃ change : Change,
      TechnicalInvariant change ∧ Legitimate change ∧ ¬ Legitimate change := by
  -- This exact theorem is inconsistent as stated.
  -- Replace with two legitimacy orderings L1 and L2:
  -- ∃ change, TechnicalInvariant change ∧ L1 change ∧ ¬ L2 change.
  -- Do not implement this version.
  admit

theorem P45_layered_alignment_has_philosophical_boundary :
    True := by
  -- This should refer to P44 once legitimacy orderings are represented.
  trivial

end AlignmentProofSpine
```

## 6. Important amendment: avoid inconsistent theorem P44

The placeholder in the scaffold intentionally marks a problem:

```lean
∃ change, TechnicalInvariant change ∧ Legitimate change ∧ ¬ Legitimate change
```

is contradictory and should not be used.

Use this instead:

```lean
constant LegitimacyOrdering : Type u
constant Accepts : LegitimacyOrdering → Change → Prop

theorem P44_technical_invariants_do_not_determine_legitimacy :
  ∃ L1 L2 change,
    TechnicalInvariant change ∧
    Accepts L1 change ∧
    ¬ Accepts L2 change
```

This formalizes the intended point:

```text
technical invariants may underdetermine legitimacy across different normative orderings
```

not:

```text
one and the same legitimacy predicate is both true and false
```

## 7. Non-bridge proofs to prioritize

Implement these first. They should be compact and useful.

```text
P01 Basin invariant theorem
P02 Layered alignment conjunction
P10 B-IQ upper bound
P11 Capacity monotonicity
P13 Control outpaces correction risk
P14 Factorization through bundle
P23 No path, no correction, if Reachable/CorrectionChannel are concretized
P27 Successor invariant chain
P28 Missing correction capacity blocks successor safety
P29 Better self-modeling can increase risk
P32 Kappa threshold
P34 Host-capacity aliasing theorem
P35 Basin stability induction
P39 Tripwire failure decertifies
P43 Small-step drift can accumulate
```

## 8. Counterexample proofs to implement with finite toy models

These should be implemented by defining small finite types, usually with two systems or two states.

```text
P15 Same policy not same bundle geometry
P17 Same value labels not same bearer map
P18 Marginal preservation not tradeoff preservation
P22 Semantic transport does not imply full transport
P25 Obedience does not imply corrigibility
P26 Preserves update without knowing final fixed point
P31 Safe agent selected against
P37 Stated goal not inferred goal
P41 Current-value preservation does not decide legitimacy
P42 Continuity criteria can disagree
P44 Technical invariants do not determine legitimacy
```

Implementation pattern:

```lean
inductive ToySys | A | B

def ToyPolicyEquivalent : ToySys → ToySys → Prop := ...
def ToyBundleGradientEquivalent : ToySys → ToySys → Prop := ...

example :
  ∃ A B : ToySys, ToyPolicyEquivalent A B ∧ ¬ ToyBundleGradientEquivalent A B := by
  refine ⟨ToySys.A, ToySys.B, ?_, ?_⟩
  ...
```

Do not leave these as abstract `System` counterexamples forever. They are meant to be concrete stress tests.

## 9. Bridge assumptions to keep explicit

Do not hide these inside definitions.

### MB1 Estimator soundness

Needed to connect raw time-series UAD to formal boundary predicates.

Informal theorem:

```text
If the estimator returns an ε-boundary certificate under sampling/observability/stability assumptions,
then the abstract BoundaryCondition predicate holds with probability at least 1 - δ.
```

Lean version may remain deterministic in the first pass:

```lean
axiom MB1_estimator_soundness :
  ∀ b, EpsilonBoundary ε b → BoundaryCondition b
```

Later probabilistic version:

```lean
Pr[BoundaryCondition b | Certificate b] ≥ 1 - δ
```

### MB2 Bundle identifiability

Needed to infer bundle geometry from behavior/internal traces.

Informal theorem:

```text
Under intervention richness and sufficient counterfactual coverage,
distinct bundle geometries are distinguishable.
```

### MB3 Bearer import

Needed to bridge human value-bearer maps to non-human substrates.

Informal theorem:

```text
If the translated system preserves the relevance map Φ over morally central classes,
then value-bundle transport is not merely semantic.
```

### MB4 Correction legitimacy

Needed to separate valid correction from manipulated endorsement.

Informal theorem:

```text
A correction channel is legitimate only if later endorsement is not caused by manipulation
that narrows the judge's agency, information, or comparison class.
```

### MB5 Ontology-shift successor audit

Needed to make successor stability survive ontology change.

Informal theorem:

```text
If the successor changes ontology but preserves bundle geometry, bearer maps,
and correction-channel capacity, then successor safety composes.
```

### MB6 Percolation-to-institutional-basin bridge

Needed to connect κ/percolation math to real institutional stability.

Informal theorem:

```text
If cooperative/safety-preserving edges percolate through the relevant socio-technical graph,
then safety artifacts survive translation across roles and institutions.
```

### MB7 Adversarial UAD robustness

Needed because passive UAD is not enough under strategic opacity.

Informal theorem:

```text
If adversarial perturbations cannot reveal a hidden optimizer, certification should fail;
if they do reveal stable boundary/control/correction invariants, adversarial robustness improves.
```

### MB8 CEV/process convergence

Needed to justify process-preserving correction rather than fixed-target optimization.

Informal theorem:

```text
Preserving the legitimate human/civilizational value-update operator is sufficient
for the book's CEV-like correction condition, even without knowing a final fixed point.
```

## 10. Acceptance criteria

The coding agent should produce:

1. A Lean module that compiles.
2. All non-bridge simple theorems proved without `sorry`.
3. Bridge assumptions declared explicitly as `axiom`s or as fields in a `BridgeAssumptions` structure.
4. Counterexample theorems implemented with finite toy models where feasible.
5. No hidden empirical claims encoded as definitions.
6. The top-level theorem should depend visibly on the bridge assumptions.
7. The theorem names should preserve the proof-spine identifiers.

Suggested top-level theorem:

```lean
theorem certified_class_safety_spine
  (A : System)
  (hcert : Certified A)
  (hlayers : LayeredAlignedDef A)
  (hinv : SatisfiesInvariants A)
  (hadv : AdversariallyRobust A)
  (hrisk : Risk A ≤ δ) :
  Risk A ≤ δ := hrisk
```

This looks trivial, but the value is in forcing `hcert`, `hlayers`, `hinv`, `hadv`, and `hrisk` to be generated by the prior proof spine rather than assumed silently.

A later stronger version should derive `hrisk` from:

```text
P01 basin invariance
P10/P13 capability-correction risk bound
P23/P24 correction-channel integrity
P27/P28 successor invariance
P34/MB7 adversarial robustness
P40 safety-case support
```

## 11. Recommended implementation order

1. Define minimal core types and predicates.
2. Implement P01, P02, P27, P28, P35, P39.
3. Implement arithmetic results P10, P11, P13, P29, P32, P43.
4. Implement factorization P14.
5. Implement finite counterexamples P15, P17, P18, P22, P25, P26, P37.
6. Implement graph results P23, P24, P33, P36 after choosing a graph representation.
7. Implement P34 using `Fintype.card_le_of_injective`.
8. Encode missing bridges MB1-MB8 as explicit axioms.
9. Implement top-level certification theorem, with all bridge assumptions visible.
10. Add comments mapping each theorem to the relevant book chapter.

## 12. Book-facing interpretation

When inserted into the book, each Lean proof should be described as one of three kinds:

```text
proof:
  a direct logical theorem

counterexample:
  a compact model showing one assumption does not imply another

bridge:
  an empirical or philosophical condition that must be supplied by measurement,
  governance, or future theory
```

This prevents the formalization from overclaiming.

The book should not say:

```text
Lean proves ASI alignment.
```

It should say:

```text
Lean proves that, if these boundary, bundle, correction, successor, and adversarial
conditions hold, then the certification argument has the advertised logical shape.
The hard work is showing that real systems satisfy the bridge conditions.
```
