import AlignmentProofSpine.Core
import AlignmentProofSpine.Capability

/-!
# AlignmentProofSpine.Successors

Successor stability and self-model risk (book chapters 28–31).

* `P27`: invariant induction along a successor chain.
* `P28`: a missing conserved property blocks successor safety.
* `P29`: a widening self-control / correction-visibility gap raises risk.
* Successor-safe chains propagate risk-gap bounds when control does not grow and
  correction capacity does not shrink (operational reading of `SuccessorSafe`).
-/

namespace AlignmentProofSpine

/-- A finite chain of successor steps. -/
inductive SuccessorChain : System → System → Prop
  | refl (A : System) : SuccessorChain A A
  | step {A B C : System} : Successor A B → SuccessorChain B C → SuccessorChain A C

/-- A successor chain where every step is successor-safe. -/
inductive SuccessorSafeChain : System → System → Prop
  | refl (A : System) : SuccessorSafeChain A A
  | step {A B C : System} :
      Successor A B → SuccessorSafe A B → SuccessorSafeChain B C → SuccessorSafeChain A C

/-- Along a successor-safe step, control must not increase and correction capacity
    must not decrease for a risk bound to propagate. This is the operational
    reading of `CorrectionCapacityPreserved` plus bounded control growth; target:
    derive from `MB5` once successor audit is concrete. -/
axiom SuccessorSafe_risk_monotone :
  ∀ {A B : System}, SuccessorSafe A B →
    Control B ≤ Control A ∧ CorrectionCapacity A ≤ CorrectionCapacity B

/-- C-SUC (P27): an invariant that holds initially and is preserved by each
    successor step holds at the end of any successor chain. -/
theorem P27_successor_invariant_chain
    (P : System → Prop)
    {A B : System}
    (h0 : P A)
    (hstep : ∀ X Y, Successor X Y → P X → P Y)
    (hchain : SuccessorChain A B) :
    P B := by
  induction hchain with
  | refl A => exact h0
  | step hsucc _ ih => exact ih (hstep _ _ hsucc h0)

/-- C-SUC: a risk-gap bound propagates across one successor-safe step when control
    is non-increasing and correction capacity is non-decreasing. -/
theorem risk_gap_bound_successor_safe_step
    {A B : System} {δ : Int}
    (hctrl : Control B ≤ Control A)
    (hcorr : CorrectionCapacity A ≤ CorrectionCapacity B)
    (h0 : RiskGap A ≤ δ) :
    RiskGap B ≤ δ := by
  unfold RiskGap at h0 ⊢
  omega

theorem risk_bound_successor_safe_step
    {A B : System} {δ : Int}
    (hctrl : Control B ≤ Control A)
    (hcorr : CorrectionCapacity A ≤ CorrectionCapacity B)
    (h0 : Risk A ≤ δ) :
    Risk B ≤ δ := by
  have hgap : RiskGap A ≤ δ := by rw [← Risk_eq_RiskGap]; exact h0
  rw [Risk_eq_RiskGap]
  exact risk_gap_bound_successor_safe_step hctrl hcorr hgap

/-- C-SUC + P27-style: propagate a risk-gap bound along a successor-safe chain.
    The preservation side-conditions may be supplied explicitly (`hpres`) or
    obtained from `SuccessorSafe_risk_monotone`. -/
theorem risk_gap_bound_along_successor_safe_chain
    {A B : System} {δ : Int}
    (h0 : RiskGap A ≤ δ)
    (hpres :
      ∀ X Y, SuccessorSafe X Y →
        Control Y ≤ Control X ∧ CorrectionCapacity X ≤ CorrectionCapacity Y)
    (hchain : SuccessorSafeChain A B) :
    RiskGap B ≤ δ := by
  let rec go (X Y : System) (hchain : SuccessorSafeChain X Y) (hX : RiskGap X ≤ δ) :
      RiskGap Y ≤ δ :=
    match hchain with
    | .refl _ => hX
    | .step _ hsafe tail =>
        let hmid :=
          risk_gap_bound_successor_safe_step (hpres _ _ hsafe).1 (hpres _ _ hsafe).2 hX
        go _ _ tail hmid
  exact go A B hchain h0

theorem risk_gap_bound_along_successor_safe_chain_from_safe
    {A B : System} {δ : Int}
    (h0 : RiskGap A ≤ δ)
    (hchain : SuccessorSafeChain A B) :
    RiskGap B ≤ δ :=
  risk_gap_bound_along_successor_safe_chain h0
    (fun _ _ h => SuccessorSafe_risk_monotone h) hchain

theorem risk_bound_along_successor_safe_chain
    {A B : System} {δ : Int}
    (h0 : Risk A ≤ δ)
    (hchain : SuccessorSafeChain A B) :
    Risk B ≤ δ := by
  have hgap : RiskGap A ≤ δ := by rw [← Risk_eq_RiskGap]; exact h0
  rw [Risk_eq_RiskGap]
  exact risk_gap_bound_along_successor_safe_chain_from_safe hgap hchain

/-- Capacity slack (`Control ≤ CorrectionCapacity + δ`) propagates along the
    same successor-safe chain for the same monotonicity reasons. -/
theorem capacity_slack_along_successor_safe_chain
    {A B : System} {δ : Int}
    (h0 : Control A ≤ CorrectionCapacity A + δ)
    (hchain : SuccessorSafeChain A B) :
    Control B ≤ CorrectionCapacity B + δ := by
  have hrisk : RiskGap B ≤ δ :=
    risk_gap_bound_along_successor_safe_chain_from_safe
      (by unfold RiskGap; omega) hchain
  unfold RiskGap at hrisk
  omega

/-- C-SUC (P28): if correction capacity is not preserved, the successor is not
    safe (one missing conjunct breaks the whole conjunction). -/
theorem P28_missing_correction_capacity_blocks_successor_safety
    {A B : System}
    (h : ¬ CorrectionCapacityPreserved A B) :
    ¬ SuccessorSafe A B := fun hs => h hs.2.2.2.2

/-- C-SELF (P29): if a successor gains self-control but loses (or does not gain)
    correction visibility, its self-control-minus-visibility gap strictly grows. -/
theorem P29_better_self_modeling_can_increase_risk
    {A B : System}
    (hcontrol : SelfControl A < SelfControl B)
    (hvis : CorrectionVisibility B ≤ CorrectionVisibility A) :
    SelfControl A - CorrectionVisibility A < SelfControl B - CorrectionVisibility B := by
  omega

end AlignmentProofSpine
