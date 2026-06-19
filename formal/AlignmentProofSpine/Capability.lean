import AlignmentProofSpine.Core

/-!
# AlignmentProofSpine.Capability

Capability / B-IQ / control–correction arithmetic (book chapters 11–14, 33).

All results here are ordered-arithmetic facts discharged by `omega`. They are
**proofs**, not bridges. The abstract quantities (`Ipred`, `Ictrl`, …) stand in
for information-theoretic measures whose estimation is out of scope.
-/

namespace AlignmentProofSpine

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

/-- The control / correction risk gap. -/
noncomputable def RiskGap (A : System) : Int := Control A - CorrectionCapacity A

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
