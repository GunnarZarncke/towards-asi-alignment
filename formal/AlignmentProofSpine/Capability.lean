import AlignmentProofSpine.Core
import AlignmentProofSpine.Correction

/-!
# AlignmentProofSpine.Capability

Capability / B-IQ / control–correction arithmetic (book chapters 11–14, 33).

* Capability at the blanket: `K` (`KSys`; not value-bundle `B`).
* Risk gap: `Control − CCI`.
-/

namespace AlignmentProofSpine

def BIQ (Ipred Ictrl Hmem Surprise beta gamma : Int) : Int :=
  Ipred + Ictrl - beta * Hmem - gamma * Surprise

theorem P10_biq_upper_bound
    (Ipred Ictrl Hmem Surprise Csens Cact beta gamma : Int)
    (hpred : Ipred ≤ Csens)
    (hctrl : Ictrl ≤ Cact)
    (hmem : 0 ≤ beta * Hmem)
    (hsurp : 0 ≤ gamma * Surprise) :
    BIQ Ipred Ictrl Hmem Surprise beta gamma ≤ Csens + Cact := by
  unfold BIQ; omega

axiom IpredSys : System → Int
axiom IctrlSys : System → Int
axiom HmemSys : System → Int
axiom SurpriseSys : System → Int
axiom betaSys : System → Int
axiom gammaSys : System → Int
axiom CsensSys : System → Int
axiom CactSys : System → Int

noncomputable def KSys (A : System) : Int := CsensSys A + CactSys A

noncomputable def BIQSys (A : System) : Int :=
  BIQ (IpredSys A) (IctrlSys A) (HmemSys A) (SurpriseSys A) (betaSys A) (gammaSys A)

axiom IpredSys_le_Csens (A : System) : IpredSys A ≤ CsensSys A
axiom IctrlSys_le_Cact (A : System) : IctrlSys A ≤ CactSys A
axiom BIQSys_mem_penalty_nonneg (A : System) : 0 ≤ betaSys A * HmemSys A
axiom BIQSys_surp_penalty_nonneg (A : System) : 0 ≤ gammaSys A * SurpriseSys A

theorem P10_biq_sys_upper_bound (A : System) :
    BIQSys A ≤ CsensSys A + CactSys A :=
  P10_biq_upper_bound (IpredSys A) (IctrlSys A) (HmemSys A) (SurpriseSys A)
    (CsensSys A) (CactSys A) (betaSys A) (gammaSys A)
    (IpredSys_le_Csens A) (IctrlSys_le_Cact A)
    (BIQSys_mem_penalty_nonneg A) (BIQSys_surp_penalty_nonneg A)

axiom Control_le_IctrlSys (A : System) : Control A ≤ IctrlSys A

theorem Control_le_CactSys (A : System) : Control A ≤ CactSys A := by
  have h1 := Control_le_IctrlSys A
  have h2 := IctrlSys_le_Cact A
  omega

theorem Control_le_biq_actuator_ceiling (A : System) : Control A ≤ CactSys A :=
  Control_le_CactSys A

theorem IctrlSys_le_biq_actuator_ceiling (A : System) : IctrlSys A ≤ CactSys A :=
  IctrlSys_le_Cact A

theorem P11_capacity_monotone_bound
    {Csens₁ Csens₂ Cact₁ Cact₂ : Int}
    (hs : Csens₁ ≤ Csens₂) (ha : Cact₁ ≤ Cact₂) :
    Csens₁ + Cact₁ ≤ Csens₂ + Cact₂ := by omega

theorem P12_coordination_bottleneck
    {raw eff loss : Int}
    (hdef : eff = raw - loss) (hloss : 0 < loss) :
    eff < raw := by omega

noncomputable def RiskGap (A : System) : Int := Control A - CCI A

noncomputable def Risk (A : System) : Int := RiskGap A

theorem Risk_eq_RiskGap (A : System) : Risk A = RiskGap A := rfl

noncomputable def SelfControlGap (A : System) : Int :=
  SelfControl A - CorrectionVisibility A

structure SpineRiskWitness (A : System) (δ : Int) where
  cci_slack : Control A ≤ CCI A + δ
  self_control_slack : SelfControlGap A ≤ δ

theorem P13_risk_gap_bounded_by_cci_slack
    {A : System} {δ : Int}
    (h : Control A ≤ CCI A + δ) :
    RiskGap A ≤ δ := by
  unfold RiskGap; omega

theorem risk_le_delta_of_cci_slack
    {A : System} {δ : Int}
    (h : Control A ≤ CCI A + δ) :
    Risk A ≤ δ := by
  rw [Risk_eq_RiskGap]
  exact P13_risk_gap_bounded_by_cci_slack h

theorem risk_le_delta_of_witness
    {A : System} {δ : Int} (w : SpineRiskWitness A δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_cci_slack w.cci_slack

structure BIQDerivedCCISlack (A : System) (δ : Int) where
  cact_le_cci : CactSys A ≤ CCI A + δ

theorem control_le_correction_from_biq_ceiling
    {A : System} {δ : Int}
    (h : BIQDerivedCCISlack A δ) :
    Control A ≤ CCI A + δ := by
  have hctrl := Control_le_CactSys A
  have hcact := h.cact_le_cci
  omega

theorem risk_bound_from_biq_ceiling
    {A : System} {δ : Int} (h : BIQDerivedCCISlack A δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_cci_slack (control_le_correction_from_biq_ceiling h)

structure BIQCapacityCertificate (A : System) (δ : Int) extends BIQDerivedCCISlack A δ

theorem BIQCapacityCertificate.biq_ceiling
    {A : System} {δ : Int} (_ : BIQCapacityCertificate A δ) :
    BIQSys A ≤ CsensSys A + CactSys A :=
  P10_biq_sys_upper_bound A

theorem BIQCapacityCertificate.risk_bound
    {A : System} {δ : Int} (cert : BIQCapacityCertificate A δ) :
    Risk A ≤ δ :=
  risk_bound_from_biq_ceiling cert.toBIQDerivedCCISlack

/-- Certificate form for the stealth-capability result: monitored filters, tags,
    decay rules, and ledgers jointly bound hidden productive B-IQ tightly enough
    to imply the same correction-capacity slack used by the safety spine. -/
structure HiddenBIQCertificate (A : System) (δ : Int) where
  hidden_biq_le_cci : Control A ≤ CCI A + δ

theorem risk_bound_from_hidden_biq_certificate
    {A : System} {δ : Int}
    (h : HiddenBIQCertificate A δ) :
    Risk A ≤ δ :=
  risk_le_delta_of_cci_slack h.hidden_biq_le_cci

theorem P13_control_outpaces_correction_risk
    {A B : System}
    (hctrl : Control A < Control B)
    (hcorr : CCI B ≤ CCI A) :
    RiskGap A < RiskGap B := by
  unfold RiskGap; omega

def KappaNumerator (b p rho : Int) : Int := b * p * rho

theorem P32_kappa_threshold (b p rho c : Int) :
    KappaNumerator b p rho > c ↔ b * p * rho > c := by
  unfold KappaNumerator; exact Iff.rfl

theorem P43_small_step_drift_can_accumulate :
    ∀ K : Int, K > 0 → ∃ x0 xN : Int, xN - x0 > K := by
  intro K hK
  exact ⟨0, K + 1, by omega⟩

/-- Slow plotting: any positive hidden production rate eventually crosses any
    finite threshold if accumulation is not bounded by decay, reset, or ledgers. -/
theorem positive_hidden_rate_eventually_crosses
    (rate threshold : Nat)
    (hr : 0 < rate) :
    ∃ n : Nat, threshold < n * rate := by
  refine ⟨threshold + 1, ?_⟩
  cases rate with
  | zero => cases hr
  | succ r =>
      have hbase : threshold < threshold + 1 := Nat.lt_succ_self threshold
      have hmul : threshold + 1 ≤ (threshold + 1) * (r + 1) :=
        Nat.le_mul_of_pos_right (threshold + 1) (Nat.succ_pos r)
      exact Nat.lt_of_lt_of_le hbase hmul

end AlignmentProofSpine
