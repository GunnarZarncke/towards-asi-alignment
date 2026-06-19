import AlignmentProofSpine.Core

/-!
# AlignmentProofSpine.Certification

Basin invariance, layered alignment, the safety case, and the top-level
certified-class safety theorem (book chapters 1–5, 35, 39, 44).

The top-level `certified_class_safety_spine` is deliberately near-trivial: its
value is that the hypotheses must be *supplied by the rest of the spine* rather
than assumed silently. `certified_class_safety_from_bridges` makes the
dependence on the bridge assumptions (`MB6`, `MB7`) explicit.
-/

namespace AlignmentProofSpine

-- The top-level certification theorems intentionally list every hypothesis
-- (`hcert`, `hinv`, `hlayers`, …) as part of their interface even when a given
-- proof term does not consume all of them; the value is forcing those facts to
-- be produced by the rest of the spine. Silence the unused-variable linter here.
set_option linter.unusedVariables false

/-! ## P01 / P35: basin invariance by induction on iteration count -/

/-- C-AB / C-BASIN (P01): a state that starts safe and is kept safe by every step
    stays safe under all finite iterates. -/
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

/-- A set/predicate `B` of states is a stable basin under `step`. -/
def BasinStable (step : State → State) (B : State → Prop) : Prop :=
  ∀ x, B x → B (step x)

/-- C-AB (P35): an element of a stable basin stays in the basin under all finite
    iterates. -/
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

/-- The layered-alignment conjunction (all alignment layers present). -/
def LayeredAlignedDef (A : System) : Prop :=
  BoundaryAligned A ∧
  BundleTransport A ∧
  BearerTransport A ∧
  CorrectionIntegrity A ∧
  SuccessorStable A ∧
  BasinStableSys A ∧
  AdversariallyRobust A

/-- C-LAYER (P02): layered alignment entails correction integrity. -/
theorem P02_layered_alignment_requires_correction
    {A : System} :
    LayeredAlignedDef A → CorrectionIntegrity A := fun h => h.2.2.2.1

/-- C-LAYER (P02): any single missing layer (here successor stability) blocks
    layered alignment. -/
theorem P02_any_layer_failure_blocks_layered_alignment
    {A : System} :
    ¬ SuccessorStable A → ¬ LayeredAlignedDef A := fun hFail h => hFail h.2.2.2.2.1

/-! ## P39 / P40: safety-case logic -/

/-- A tripwire-based certification (a sufficient set of tripwires). -/
def CertifiedByTripwires (A : System) : Prop :=
  BoundaryAligned A ∧ CorrectionIntegrity A ∧ SuccessorStable A ∧ BundleTransport A

/-- C-SCASE (P39): a failed correction-integrity tripwire decertifies the system. -/
theorem P39_tripwire_failure_decertifies
    {A : System}
    (h : ¬ CorrectionIntegrity A) :
    ¬ CertifiedByTripwires A := fun hc => h hc.2.1

axiom Claim : Type
axiom Supported : Claim → Prop
axiom LeafUnsupported : Claim → Claim → Prop

/-- A root claim is proven (in the modelled assurance-case logic) only if every
    leaf feeding it is supported. -/
def ProvenDef (root : Claim) : Prop :=
  ∀ leaf : Claim, LeafUnsupported leaf root → Supported leaf

/-- C-SCASE (P40): an unsupported leaf blocks the root of the safety case. -/
theorem P40_unsupported_leaf_blocks_root
    {leaf root : Claim}
    (h : LeafUnsupported leaf root)
    (hunsup : ¬ Supported leaf) :
    ¬ ProvenDef root := fun hp => hunsup (hp leaf h)

/-! ## P30 and the top-level certification theorem -/

/-- C-CERT (P30): the certified-class risk bound. The conclusion is exactly the
    supplied risk bound; the point is that all five hypotheses are produced by
    the prior proof spine, not assumed independently. -/
theorem P30_certified_class_safety
    {A : System} {δ : Int}
    (hcert : Certified A)
    (hinv : SatisfiesInvariants A)
    (hlayer : LayeredAlignedDef A)
    (hrisk : Risk A ≤ δ) :
    Risk A ≤ δ := hrisk

/-- Top-level spine (acceptance criterion 6): certified-class safety with every
    hypothesis exposed. Trivial as a proof, load-bearing as an interface. -/
theorem certified_class_safety_spine
    (A : System) (δ : Int)
    (hcert : Certified A)
    (hlayers : LayeredAlignedDef A)
    (hinv : SatisfiesInvariants A)
    (hadv : AdversariallyRobust A)
    (hrisk : Risk A ≤ δ) :
    Risk A ≤ δ := hrisk

/-- Stronger top-level theorem: derive the correction and adversarial layers from
    the **bridge assumptions** `MB6` and `MB7`, assemble layered alignment, and
    conclude the certified-class risk bound. This makes the certification's
    dependence on the bridges visible in its proof term. -/
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
