import AlignmentProofSpine.Core
import AlignmentProofSpine.Capability
import AlignmentProofSpine.Successors

/-!
# AlignmentProofSpine.Certification

Basin invariance, layered alignment, the safety case, and the top-level
certified-class safety theorem (book chapters 1–5, 35, 39, 44).

**Risk bound (critical point #1).** The primary certification theorems derive
`Risk A ≤ δ` from a *capacity certificate*
`Control A ≤ CorrectionCapacity A + δ` via `P13_risk_gap_bounded_by_capacity_slack`,
not from a bare `hrisk` hypothesis. Legacy theorems that still take `hrisk` are
kept for backward compatibility.

Toy status: counterexamples and several predicates are still finite `Bool`
separations; see `metadata/TODO.md` and `formal/README.md`.
-/

namespace AlignmentProofSpine

set_option linter.unusedVariables false

/-! ## P01 / P35: basin invariance by induction on iteration count -/

theorem P01_basin_invariant
    (step : State → State)
    (x0 : State)
    (h0 : SafeState x0)
    (hstep : ∀ x, SafeState x → SafeState (step x)) :
    ∀ n : Nat, SafeState (iterateN step n x0) := by
  have aux : ∀ n x, SafeState x → SafeState (iterateN step n x) := by
    intro n
    induction n with
    | zero => intro x hx; exact hx
    | succ k ih => intro x hx; exact ih (step x) (hstep x hx)
  intro n; exact aux n x0 h0

def BasinStable (step : State → State) (B : State → Prop) : Prop :=
  ∀ x, B x → B (step x)

theorem P35_basin_stability_induction
    (step : State → State)
    (B : State → Prop)
    (x0 : State)
    (hstable : BasinStable step B)
    (h0 : B x0) :
    ∀ n : Nat, B (iterateN step n x0) := by
  have aux : ∀ n x, B x → B (iterateN step n x) := by
    intro n
    induction n with
    | zero => intro x hx; exact hx
    | succ k ih => intro x hx; exact ih (step x) (hstable x hx)
  intro n; exact aux n x0 h0

/-! ## P02: layered alignment conjunction -/

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
    LayeredAlignedDef A → CorrectionIntegrity A := fun h => h.2.2.2.1

theorem P02_any_layer_failure_blocks_layered_alignment
    {A : System} :
    ¬ SuccessorStable A → ¬ LayeredAlignedDef A := fun hFail h => hFail h.2.2.2.2.1

/-! ## P39 / P40: safety-case logic -/

def CertifiedByTripwires (A : System) : Prop :=
  BoundaryAligned A ∧ CorrectionIntegrity A ∧ SuccessorStable A ∧ BundleTransport A

theorem P39_tripwire_failure_decertifies
    {A : System}
    (h : ¬ CorrectionIntegrity A) :
    ¬ CertifiedByTripwires A := fun hc => h hc.2.1

axiom Claim : Type
axiom Supported : Claim → Prop
axiom LeafUnsupported : Claim → Claim → Prop

def ProvenDef (root : Claim) : Prop :=
  ∀ leaf : Claim, LeafUnsupported leaf root → Supported leaf

theorem P40_unsupported_leaf_blocks_root
    {leaf root : Claim}
    (h : LeafUnsupported leaf root)
    (hunsup : ¬ Supported leaf) :
    ¬ ProvenDef root := fun hp => hunsup (hp leaf h)

/-! ## Risk bound derived from the spine (critical point #1) -/

/-- Inputs the spine can supply instead of a bare risk bound. The capacity slack
    is the load-bearing field; layered alignment and certification are the
    assurance-case context. -/
structure CertifiedSpineInputs (A : System) (δ : Int) where
  certified : Certified A
  invariants : SatisfiesInvariants A
  layered : LayeredAlignedDef A
  capacity_slack : Control A ≤ CorrectionCapacity A + δ

/-- C-CERT (P30, strengthened): derive the risk bound from capacity slack. -/
theorem P30_certified_class_safety_derived
    {A : System} {δ : Int}
    (h : CertifiedSpineInputs A δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_capacity_slack h.capacity_slack

/-- Top-level spine: layered alignment + capacity certificate ⇒ risk bound.
    The conclusion is proved via `P13`, not assumed. -/
theorem certified_class_safety_spine_derived
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hlayers : LayeredAlignedDef A)
    (hinv : SatisfiesInvariants A)
    (_hadv : AdversariallyRobust A)
    (hcap : Control A ≤ CorrectionCapacity A + δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_capacity_slack hcap

/-- Bridges assemble layered alignment; capacity certificate derives the risk bound. -/
theorem certified_class_safety_from_spine_and_bridges
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hbound : BoundaryAligned A)
    (hbundle : BundleTransport A)
    (hbearer : BearerTransport A)
    (hsucc : SuccessorStable A)
    (hbasin : BasinStableSys A)
    (hcap : Control A ≤ CorrectionCapacity A + δ) :
    LayeredAlignedDef A ∧ Risk A ≤ δ := by
  have hcorr : CorrectionIntegrity A :=
    MB6_percolation_to_institutional_basin A hbasin
  have hadv : AdversariallyRobust A :=
    MB7_adversarial_uad_robustness A hbound hcorr
  exact ⟨⟨hbound, hbundle, hbearer, hcorr, hsucc, hbasin, hadv⟩,
    risk_le_delta_of_capacity_slack hcap⟩

/-- C-SUC + C-CERT: if the root system is certified with capacity slack, every
    system reachable by a successor-safe chain inherits the same risk bound. -/
theorem certified_class_safety_along_successor_safe_chain
    {A B : System} {δ : Int}
    (hcap : Control A ≤ CorrectionCapacity A + δ)
    (hchain : SuccessorSafeChain A B) :
    Risk B ≤ δ :=
  risk_bound_along_successor_safe_chain (risk_le_delta_of_capacity_slack hcap) hchain

/-- Full spine at the successor: bridges + capacity at root + safe chain ⇒ bound. -/
theorem certified_class_safety_from_spine_bridges_and_successor_chain
    {A B : System} {δ : Int}
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hbound : BoundaryAligned A)
    (hbundle : BundleTransport A)
    (hbearer : BearerTransport A)
    (hsucc : SuccessorStable A)
    (hbasin : BasinStableSys A)
    (hcap : Control A ≤ CorrectionCapacity A + δ)
    (hchain : SuccessorSafeChain A B) :
    LayeredAlignedDef A ∧ Risk B ≤ δ := by
  have hroot := certified_class_safety_from_spine_and_bridges A δ hcert hinv
    hbound hbundle hbearer hsucc hbasin hcap
  exact ⟨hroot.1, risk_bound_along_successor_safe_chain hroot.2 hchain⟩

/-! ## BIQ ceiling → control → risk (compose `P10` with `P13`) -/

/-- C-CERT from BIQ actuator ceiling: if correction covers `C_act + δ`, risk is bounded. -/
theorem certified_class_safety_from_biq_ceiling
    {A : System} {δ : Int}
    (cert : BIQCapacityCertificate A δ) :
    Risk A ≤ δ :=
  BIQCapacityCertificate.risk_bound cert

/-- Bridges + BIQ-derived capacity slack (no direct `Control ≤ CorrectionCapacity + δ`). -/
theorem certified_class_safety_from_spine_bridges_and_biq
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hbound : BoundaryAligned A)
    (hbundle : BundleTransport A)
    (hbearer : BearerTransport A)
    (hsucc : SuccessorStable A)
    (hbasin : BasinStableSys A)
    (hbiq : BIQDerivedCapacitySlack A δ) :
    LayeredAlignedDef A ∧ Risk A ≤ δ :=
  certified_class_safety_from_spine_and_bridges A δ hcert hinv
    hbound hbundle hbearer hsucc hbasin (control_le_correction_from_biq_ceiling hbiq)

/-- BIQ certificate at root + successor-safe chain ⇒ bound at successor. -/
theorem certified_class_safety_from_biq_along_successor_chain
    {A B : System} {δ : Int}
    (hbiq : BIQDerivedCapacitySlack A δ)
    (hchain : SuccessorSafeChain A B) :
    Risk B ≤ δ :=
  certified_class_safety_along_successor_safe_chain
    (control_le_correction_from_biq_ceiling hbiq) hchain

/-! ## Weakest-link graph → correction capacity (compose with BIQ / `P13`) -/

theorem certified_class_safety_from_weakest_link_slack
    {A : System} {δ : Int}
    (h : WeakestLinkDerivedCapacitySlack A δ) :
    Risk A ≤ δ :=
  risk_bound_from_weakest_link_slack h

theorem certified_class_safety_from_spine_bridges_and_weakest_link
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hbound : BoundaryAligned A)
    (hbundle : BundleTransport A)
    (hbearer : BearerTransport A)
    (hsucc : SuccessorStable A)
    (hbasin : BasinStableSys A)
    (hwl : WeakestLinkDerivedCapacitySlack A δ) :
    LayeredAlignedDef A ∧ Risk A ≤ δ :=
  certified_class_safety_from_spine_bridges_and_biq A δ hcert hinv
    hbound hbundle hbearer hsucc hbasin (weakest_link_slack_implies_biq_slack hwl)

theorem certified_class_safety_from_weakest_link_along_successor_chain
    {A B : System} {δ : Int}
    (hwl : WeakestLinkDerivedCapacitySlack A δ)
    (hchain : SuccessorSafeChain A B) :
    Risk B ≤ δ :=
  certified_class_safety_along_successor_safe_chain
    (control_le_correction_from_biq_ceiling (weakest_link_slack_implies_biq_slack hwl)) hchain

/-! ## Legacy interface (risk bound supplied explicitly) -/

theorem P30_certified_class_safety
    {A : System} {δ : Int}
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hlayer : LayeredAlignedDef A)
    (hrisk : Risk A ≤ δ) :
    Risk A ≤ δ := hrisk

theorem certified_class_safety_spine
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hlayers : LayeredAlignedDef A)
    (hinv : SatisfiesInvariants A)
    (hadv : AdversariallyRobust A)
    (hrisk : Risk A ≤ δ) :
    Risk A ≤ δ := hrisk

theorem certified_class_safety_from_bridges
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hbound : BoundaryAligned A)
    (hbundle : BundleTransport A)
    (hbearer : BearerTransport A)
    (hsucc : SuccessorStable A)
    (hbasin : BasinStableSys A)
    (hrisk : Risk A ≤ δ) :
    LayeredAlignedDef A ∧ Risk A ≤ δ := by
  have hcorr : CorrectionIntegrity A :=
    MB6_percolation_to_institutional_basin A hbasin
  have hadv : AdversariallyRobust A :=
    MB7_adversarial_uad_robustness A hbound hcorr
  exact ⟨⟨hbound, hbundle, hbearer, hcorr, hsucc, hbasin, hadv⟩, hrisk⟩

end AlignmentProofSpine
