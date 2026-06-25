import AlignmentProofSpine.Core
import AlignmentProofSpine.Correction

/-!
# AlignmentProofSpine.Capability

Capability / B-IQ / control–correction arithmetic (book chapters 11–14, 33).

* Capability at the blanket: `K` (`KSys`; not value-bundle `B`).
* Effective control `Control` from ch11 control information (integer proxy).
* Collective competence and coordination loss (ch13).
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

/-! ### Effective control (ch11 §physical envelopes)

Book: \(0 \leq \mathrm{Control}(A) \leq I_{\mathrm{ctrl}}(A) \leq C_{\mathrm{act}}(A)\).
The integer spine identifies effective control with measured control information. -/

/-- Effective actuator control capacity (ch11). -/
noncomputable def Control (A : System) : Int := IctrlSys A

theorem Control_eq_IctrlSys (A : System) : Control A = IctrlSys A := rfl

theorem Control_le_IctrlSys (A : System) : Control A ≤ IctrlSys A := by
  rw [Control_eq_IctrlSys]
  exact Int.le_refl _

theorem Control_le_CactSys (A : System) : Control A ≤ CactSys A := by
  rw [Control_eq_IctrlSys]
  exact IctrlSys_le_Cact A

theorem Control_le_biq_actuator_ceiling (A : System) : Control A ≤ CactSys A :=
  Control_le_CactSys A

theorem IctrlSys_le_biq_actuator_ceiling (A : System) : IctrlSys A ≤ CactSys A :=
  IctrlSys_le_Cact A

theorem P10_biq_sys_upper_bound (A : System) :
    BIQSys A ≤ CsensSys A + CactSys A :=
  P10_biq_upper_bound (IpredSys A) (IctrlSys A) (HmemSys A) (SurpriseSys A)
    (CsensSys A) (CactSys A) (betaSys A) (gammaSys A)
    (IpredSys_le_Csens A) (IctrlSys_le_Cact A)
    (BIQSys_mem_penalty_nonneg A) (BIQSys_surp_penalty_nonneg A)

theorem P11_capacity_monotone_bound
    {Csens₁ Csens₂ Cact₁ Cact₂ : Int}
    (hs : Csens₁ ≤ Csens₂) (ha : Cact₁ ≤ Cact₂) :
    Csens₁ + Cact₁ ≤ Csens₂ + Cact₂ := by omega

/-! ### Collective competence and coordination bottleneck (ch13) -/

/-- ch13 Eq. collective competence: weighted local sum plus gain minus loss. -/
def CollectiveCompetence (localSum gain loss : Int) : Int :=
  localSum + gain - loss

/-- The seven coordination-loss terms (ch13 §seven-losses). -/
structure CoordinationLoss where
  latency : Int
  bandwidth : Int
  translation : Int
  authority : Int
  incentive : Int
  trust : Int
  irreversibility : Int

def totalCoordinationLoss (l : CoordinationLoss) : Int :=
  l.latency + l.bandwidth + l.translation + l.authority +
  l.incentive + l.trust + l.irreversibility

theorem collective_competence_with_loss
    (localSum gain : Int) (l : CoordinationLoss) :
    CollectiveCompetence localSum gain (totalCoordinationLoss l) =
      localSum + gain - totalCoordinationLoss l := rfl

theorem P12_coordination_bottleneck
    {raw eff loss : Int}
    (hdef : eff = raw - loss) (hloss : 0 < loss) :
    eff < raw := by omega

theorem coordination_bottleneck_when_loss_positive
    (localSum gain loss : Int)
    (hloss : 0 < loss) :
    CollectiveCompetence localSum gain loss < localSum + gain := by
  unfold CollectiveCompetence; omega

/-- ch13: coordination loss can consume a local competence increment entirely. -/
theorem loss_can_wipe_local_competence_gain
    (localSum delta loss : Int)
    (_hdelta : 0 < delta)
    (hloss : delta ≤ loss) :
    CollectiveCompetence (localSum + delta) 0 loss ≤ CollectiveCompetence localSum 0 0 := by
  unfold CollectiveCompetence; omega

theorem collective_competence_drop_when_loss_exceeds_gain
    (localSum gain loss : Int)
    (h : gain < loss) :
    CollectiveCompetence localSum gain loss < localSum := by
  unfold CollectiveCompetence; omega

/-! ### Cooperativity threshold κ (ch13) -/

def KappaNumerator (b p rho : Int) : Int := b * p * rho

/-- Coordination efficiency exceeds threshold 1 iff `b * p * ρ > c` when `c > 0` (ch13). -/
theorem P32_kappa_threshold
    (b p rho c : Int)
    (_hc : 0 < c) :
    c < b * p * rho ↔ KappaNumerator b p rho > c := by
  unfold KappaNumerator; omega

def KappaAboveUnity (b p rho c : Int) : Prop :=
  0 < c ∧ c < KappaNumerator b p rho

theorem kappa_above_unity_iff (b p rho c : Int) (hc : 0 < c) :
    KappaAboveUnity b p rho c ↔ KappaNumerator b p rho > c := by
  unfold KappaAboveUnity KappaNumerator; omega

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
