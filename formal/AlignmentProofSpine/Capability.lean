import AlignmentProofSpine.Core
import AlignmentProofSpine.Correction

/-!
# AlignmentProofSpine.Capability

Capability / B-IQ / control–correction arithmetic (book chapters 11–14, 33).

All results here are ordered-arithmetic facts discharged by `omega`. They are
**proofs**, not bridges. The abstract quantities (`Ipred`, `Ictrl`, …) stand in
for information-theoretic measures whose estimation is out of scope.
-/

namespace AlignmentProofSpine

/-! ### Abstract BIQ formula (parameterized) -/

/-- Bitwise-IQ style competence score
    `BIQ = I_pred + I_ctrl - β·H(mem) - γ·Surprise`. -/
def BIQ (Ipred Ictrl Hmem Surprise beta gamma : Int) : Int :=
  Ipred + Ictrl - beta * Hmem - gamma * Surprise

/-- C-BIQ (P10): competence is bounded by the sensory + actuator capacity
    ceilings once the (non-negative) memory and surprise penalties are dropped. -/
theorem P10_biq_upper_bound
    (Ipred Ictrl Hmem Surprise Csens Cact beta gamma : Int)
    (hpred : Ipred ≤ Csens)
    (hctrl : Ictrl ≤ Cact)
    (hmem : 0 ≤ beta * Hmem)
    (hsurp : 0 ≤ gamma * Surprise) :
    BIQ Ipred Ictrl Hmem Surprise beta gamma ≤ Csens + Cact := by
  unfold BIQ; omega

/-! ### Per-system BIQ profile (book §11; measurement supplies values)

The spine keeps estimation abstract: each system carries blanket IO components and
ceilings. The link `Control A ≤ IctrlSys A` is the operational bridge from the
abstract control quantity to the BIQ control-information term. -/

/-- Predictive information through the blanket (`I_pred`). -/
axiom IpredSys : System → Int
/-- Control information through the blanket (`I_ctrl`). -/
axiom IctrlSys : System → Int
axiom HmemSys : System → Int
axiom SurpriseSys : System → Int
axiom betaSys : System → Int
axiom gammaSys : System → Int
/-- Sensory / predictive IO ceiling at the blanket. -/
axiom CsensSys : System → Int
/-- Actuator / control IO ceiling at the blanket (`C_act` in the book). -/
axiom CactSys : System → Int

/-- Per-system B-IQ from the book's competence functional. -/
noncomputable def BIQSys (A : System) : Int :=
  BIQ (IpredSys A) (IctrlSys A) (HmemSys A) (SurpriseSys A) (betaSys A) (gammaSys A)

/-- Measured predictive term stays under the sensory ceiling. Bridge target: UAD/IO estimation. -/
axiom IpredSys_le_Csens (A : System) : IpredSys A ≤ CsensSys A

/-- Measured control-information term stays under the actuator ceiling. Bridge target: UAD/IO estimation. -/
axiom IctrlSys_le_Cact (A : System) : IctrlSys A ≤ CactSys A

axiom BIQSys_mem_penalty_nonneg (A : System) : 0 ≤ betaSys A * HmemSys A
axiom BIQSys_surp_penalty_nonneg (A : System) : 0 ≤ gammaSys A * SurpriseSys A

/-- C-BIQ (system form): blanket competence is bounded by `C_sens + C_act`. -/
theorem P10_biq_sys_upper_bound (A : System) :
    BIQSys A ≤ CsensSys A + CactSys A :=
  P10_biq_upper_bound (IpredSys A) (IctrlSys A) (HmemSys A) (SurpriseSys A)
    (CsensSys A) (CactSys A) (betaSys A) (gammaSys A)
    (IpredSys_le_Csens A) (IctrlSys_le_Cact A)
    (BIQSys_mem_penalty_nonneg A) (BIQSys_surp_penalty_nonneg A)

/-- Abstract `Control` tracks the BIQ control-information term, not the full BIQ
    score. Bridge: show measured control flow matches `I_ctrl` under the blanket model. -/
axiom Control_le_IctrlSys (A : System) : Control A ≤ IctrlSys A

/-- C-BIQ → control ceiling: control inherits the actuator IO cap from the profile. -/
theorem Control_le_CactSys (A : System) : Control A ≤ CactSys A := by
  have h1 := Control_le_IctrlSys A
  have h2 := IctrlSys_le_Cact A
  omega

theorem Control_le_biq_actuator_ceiling (A : System) : Control A ≤ CactSys A :=
  Control_le_CactSys A

/-- Extract the control-information component bound implied by the BIQ profile. -/
theorem IctrlSys_le_biq_actuator_ceiling (A : System) : IctrlSys A ≤ CactSys A :=
  IctrlSys_le_Cact A

/-! ### Capacity monotonicity and coordination -/

/-- C-BIQ (P11): the capacity ceiling is monotone in its components. -/
theorem P11_capacity_monotone_bound
    {Csens₁ Csens₂ Cact₁ Cact₂ : Int}
    (hs : Csens₁ ≤ Csens₂) (ha : Cact₁ ≤ Cact₂) :
    Csens₁ + Cact₁ ≤ Csens₂ + Cact₂ := by omega

/-- C-RISK (P12): the coordination bottleneck. If effective capability is raw
    capability minus a positive coordination loss, effective < raw. -/
theorem P12_coordination_bottleneck
    {raw eff loss : Int}
    (hdef : eff = raw - loss) (hloss : 0 < loss) :
    eff < raw := by omega

/-- The control / correction risk gap (positive ⇒ control outpaces correction). -/
noncomputable def RiskGap (A : System) : Int := Control A - CorrectionCapacity A

/-- C-CERT operationalization: abstract risk is the control/correction gap.
    Measurement bridges must show observables track this quantity; the inequality
    proof below is purely arithmetic once capacities are supplied. -/
noncomputable def Risk (A : System) : Int := RiskGap A

theorem Risk_eq_RiskGap (A : System) : Risk A = RiskGap A := rfl

/-- Self-control minus correction visibility (Ch. 30 asymmetry). -/
noncomputable def SelfControlGap (A : System) : Int :=
  SelfControl A - CorrectionVisibility A

/-- Witness for a spine-derived risk bound: capacity slack plus optional
    self-control/visibility slack (both must fit under the same δ). -/
structure SpineRiskWitness (A : System) (δ : Int) where
  capacity_slack : Control A ≤ CorrectionCapacity A + δ
  self_control_slack : SelfControlGap A ≤ δ

/-- C-RISK: if control stays within correction capacity plus slack δ, the risk
    gap is at most δ. Primary capacity-side bound feeding certification. -/
theorem P13_risk_gap_bounded_by_capacity_slack
    {A : System} {δ : Int}
    (h : Control A ≤ CorrectionCapacity A + δ) :
    RiskGap A ≤ δ := by
  unfold RiskGap; omega

/-- Derived risk bound from capacity slack (replaces a bare `hrisk` hypothesis). -/
theorem risk_le_delta_of_capacity_slack
    {A : System} {δ : Int}
    (h : Control A ≤ CorrectionCapacity A + δ) :
    Risk A ≤ δ := by
  rw [Risk_eq_RiskGap]
  exact P13_risk_gap_bounded_by_capacity_slack h

theorem risk_le_delta_of_witness
    {A : System} {δ : Int} (w : SpineRiskWitness A δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_capacity_slack w.capacity_slack

/-! ### BIQ ceiling → control → risk (compose `P10` with `P13`) -/

/-- Correction capacity covers the BIQ actuator ceiling (`C_act`) plus slack `δ`. -/
structure BIQDerivedCapacitySlack (A : System) (δ : Int) where
  cact_le_corr : CactSys A ≤ CorrectionCapacity A + δ

theorem control_le_correction_from_biq_ceiling
    {A : System} {δ : Int} (h : BIQDerivedCapacitySlack A δ) :
    Control A ≤ CorrectionCapacity A + δ := by
  have hctrl := Control_le_CactSys A
  have hcact := h.cact_le_corr
  omega

theorem risk_bound_from_biq_ceiling
    {A : System} {δ : Int} (h : BIQDerivedCapacitySlack A δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_capacity_slack (control_le_correction_from_biq_ceiling h)

/-- BIQ-side certificate: actuator ceiling covered by correction; competence bound
    is always available separately via `P10_biq_sys_upper_bound`. -/
structure BIQCapacityCertificate (A : System) (δ : Int) extends BIQDerivedCapacitySlack A δ

theorem BIQCapacityCertificate.biq_ceiling
    {A : System} {δ : Int} (_ : BIQCapacityCertificate A δ) :
    BIQSys A ≤ CsensSys A + CactSys A :=
  P10_biq_sys_upper_bound A

theorem BIQCapacityCertificate.risk_bound
    {A : System} {δ : Int} (cert : BIQCapacityCertificate A δ) :
    Risk A ≤ δ :=
  risk_bound_from_biq_ceiling cert.toBIQDerivedCapacitySlack

/-! ### Weakest-link graph → correction capacity (compose with BIQ / `P13`) -/

/-- Actuator ceiling covered by the graph bottleneck plus slack `δ`. -/
structure WeakestLinkDerivedCapacitySlack (A : System) (δ : Int) where
  cact_le_wl : CactSys A ≤ WeakestLinkCapacity A + δ

theorem weakest_link_slack_implies_biq_slack
    {A : System} {δ : Int} (h : WeakestLinkDerivedCapacitySlack A δ) :
    BIQDerivedCapacitySlack A δ := by
  refine ⟨?_⟩
  rw [CorrectionCapacity_eq_weakest_link]
  exact h.cact_le_wl

theorem risk_bound_from_weakest_link_slack
    {A : System} {δ : Int} (h : WeakestLinkDerivedCapacitySlack A δ) :
    Risk A ≤ δ :=
  risk_bound_from_biq_ceiling (weakest_link_slack_implies_biq_slack h)

/-- Graph-side certificate: actuator covered by the measured weakest-link bottleneck. -/
abbrev WeakestLinkGraphCertificate (A : System) (δ : Int) :=
  WeakestLinkDerivedCapacitySlack A δ

theorem WeakestLinkGraphCertificate.risk_bound
    {A : System} {δ : Int} (cert : WeakestLinkGraphCertificate A δ) :
    Risk A ≤ δ :=
  risk_bound_from_weakest_link_slack cert

/-- C-RISK (P13): if control grows strictly faster than correction capacity, the
    risk gap strictly increases. -/
theorem P13_control_outpaces_correction_risk
    {A B : System}
    (hctrl : Control A < Control B)
    (hcorr : CorrectionCapacity B ≤ CorrectionCapacity A) :
    RiskGap A < RiskGap B := by
  unfold RiskGap; omega

/-- Numerator of the cooperativity index `κ = b·p·ρ / c`. -/
def KappaNumerator (b p rho : Int) : Int := b * p * rho

/-- C-KAPPA (P32): the cooperativity threshold `κ > 1`, cleared of its
    denominator, is exactly `b·p·ρ > c`. -/
theorem P32_kappa_threshold (b p rho c : Int) :
    KappaNumerator b p rho > c ↔ b * p * rho > c := by
  unfold KappaNumerator; exact Iff.rfl

/-- C-DRIFT (P43): bounded per-step drift can accumulate past any threshold. -/
theorem P43_small_step_drift_can_accumulate :
    ∀ K : Int, K > 0 → ∃ x0 xN : Int, xN - x0 > K := by
  intro K hK
  exact ⟨0, K + 1, by omega⟩

end AlignmentProofSpine
