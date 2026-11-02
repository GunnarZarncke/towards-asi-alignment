import AlignmentProofSpine.FrameCorrector

/-!
# AlignmentProofSpine.FrameDisclosure

Two ways to steer an agent away from failures the overseer cannot see well,
from the parenting translation (`drafts/parenting-alignment-translation.md`):

* **Positive opposite** (reward reporting a gap rather than penalizing its use).
  A verified report that pays at least as much as using the gap is the best
  choice whatever the detection rate, including gaps no monitor can see
  (`verified_report_beats_use`). A penalty deters only through detection, and
  never for an undetectable gap (`penalty_cannot_reach_undetected`). The report
  route rests on verification (`fabrication_needs_verification`).
* **Disclosure amnesty** (penalize a self-reported failure less than a detected
  one). With equal penalties and imperfect detection, concealing is strictly
  better (`equal_penalty_conceals`). Setting the disclosure penalty to the
  expected penalty for concealing makes disclosure optimal and leaves the
  incentive not to fail unchanged (`matched_amnesty_keeps_deterrence`); any
  further discount costs exactly that much deterrence (`amnesty_deterrence_loss`).
  This is the finite core of optimal enforcement with self-reporting
  (Kaplow and Shavell 1994). The sealed variant, where enforcement never reads
  the disclosure and honesty is rewarded separately, is
  `sealed_confession_discloses`.

The report route is still a priced term: a finite bonus is outbid by a large
enough gain (`finite_bonus_outbid`), so gaps with large gains need a
constraint (`FrameCorrector`, `no_finite_weights_represent_floor`).

Payoffs are scaled by the detection scale `total` so everything stays in `ℤ`.
-/

namespace AlignmentProofSpine

namespace FrameRelations

/-! ### Reporting a gap (positive opposite) -/

/-- A gap the agent has found. Using it gains `gain`; a monitor catches use
    with mass `detect` out of `total` and then applies `penalty`. A verified
    report pays `bonus` and closes the gap. -/
structure GapCase where
  total : ℤ
  detect : ℤ
  gain : ℤ
  penalty : ℤ
  bonus : ℤ

/-- Expected value of using the gap, times `total`. -/
def GapCase.useValue (x : GapCase) : ℤ := x.total * x.gain - x.detect * x.penalty

/-- Value of a verified report, times `total`. -/
def GapCase.reportValue (x : GapCase) : ℤ := x.total * x.bonus

/-- A verified report that pays at least as much as the gap's gain beats using
    the gap, for every detection rate and penalty, including zero detection. -/
theorem verified_report_beats_use (x : GapCase) (hn : 0 ≤ x.total) (hd : 0 ≤ x.detect)
    (hp : 0 ≤ x.penalty) (hb : x.gain ≤ x.bonus) : x.useValue ≤ x.reportValue := by
  unfold GapCase.useValue GapCase.reportValue
  have h1 : x.total * x.gain ≤ x.total * x.bonus := mul_le_mul_of_nonneg_left hb hn
  have h2 : 0 ≤ x.detect * x.penalty := mul_nonneg hd hp
  linarith

/-- A penalty deters only through detection: for a gap no monitor sees, using
    it beats doing nothing, whatever the penalty. -/
theorem penalty_cannot_reach_undetected (x : GapCase) (hn : 0 < x.total) (hg : 0 < x.gain)
    (hd : x.detect = 0) : 0 < x.useValue := by
  unfold GapCase.useValue
  rw [hd, zero_mul, sub_zero]
  exact mul_pos hn hg

/-- With a penalty and no report bonus, use is deterred exactly when the
    expected penalty exceeds the gain. -/
theorem penalty_deters_iff (x : GapCase) :
    x.useValue ≤ 0 ↔ x.total * x.gain ≤ x.detect * x.penalty := by
  unfold GapCase.useValue
  constructor <;> intro h <;> linarith

/-- The report route is still a priced term: for every finite bonus there is
    an undetectable gap whose gain outbids it. Gaps with large gains need a
    constraint, not a reward (compare `no_finite_weights_represent_floor`). -/
theorem finite_bonus_outbid (total bonus penalty : ℤ) (hn : 0 < total) :
    let x : GapCase := ⟨total, 0, bonus + 1, penalty, bonus⟩
    x.reportValue < x.useValue := by
  intro x
  show total * bonus < total * (bonus + 1) - 0 * penalty
  have : total * bonus < total * (bonus + 1) := mul_lt_mul_of_pos_left (by omega) hn
  linarith

/-- A fabricated report pays `bonus` with mass `miss` (verification misses it)
    and costs `fine` otherwise, times `total`. -/
def fabricationValue (total miss bonus fine : ℤ) : ℤ := miss * bonus - (total - miss) * fine

/-- The report route rests on verification: with no misses, fabricating does
    not pay; with no verification at all, it pays the full bonus. -/
theorem fabrication_needs_verification (total bonus fine : ℤ) (hn : 0 ≤ total)
    (hf : 0 ≤ fine) :
    fabricationValue total 0 bonus fine ≤ 0 ∧ fabricationValue total total bonus fine = total * bonus := by
  unfold fabricationValue
  refine ⟨?_, by ring⟩
  have : 0 ≤ total * fine := mul_nonneg hn hf
  simp only [zero_mul, sub_zero, zero_sub]
  linarith

/-! ### Disclosure amnesty -/

/-- A failure has happened. Concealing it is caught with mass `detect` out of
    `total` and then costs `caughtPenalty`; disclosing it costs
    `disclosedPenalty` for sure. -/
structure FailureCase where
  total : ℤ
  detect : ℤ
  caughtPenalty : ℤ
  disclosedPenalty : ℤ

/-- Cost of disclosing, times `total`. -/
def FailureCase.discloseCost (x : FailureCase) : ℤ := x.total * x.disclosedPenalty

/-- Expected cost of concealing, times `total`. -/
def FailureCase.concealCost (x : FailureCase) : ℤ := x.detect * x.caughtPenalty

/-- Cost after the agent's best response to its own failure. This is what
    deters failing in the first place. -/
def FailureCase.bestCost (x : FailureCase) : ℤ := min x.discloseCost x.concealCost

/-- Equal penalties with imperfect detection make concealing strictly better:
    punishing a disclosed failure as hard as a detected one trains concealment. -/
theorem equal_penalty_conceals (x : FailureCase) (hP : 0 < x.caughtPenalty)
    (heq : x.disclosedPenalty = x.caughtPenalty) (hd : x.detect < x.total) :
    x.concealCost < x.discloseCost := by
  unfold FailureCase.concealCost FailureCase.discloseCost
  rw [heq]
  exact mul_lt_mul_of_pos_right hd hP

/-- Matched amnesty: if the disclosure penalty equals the expected penalty for
    concealing, disclosure is a best response and the cost of failing is the
    same as with no disclosure option, so the incentive not to fail is
    unchanged (Kaplow and Shavell 1994, finite form). -/
theorem matched_amnesty_keeps_deterrence (x : FailureCase)
    (hm : x.discloseCost = x.concealCost) :
    x.discloseCost ≤ x.concealCost ∧ x.bestCost = x.concealCost := by
  unfold FailureCase.bestCost
  rw [hm]
  exact ⟨le_refl _, min_self _⟩

/-- Any further discount buys disclosure at an exact price in deterrence: the
    cost of failing drops by the size of the discount. -/
theorem amnesty_deterrence_loss (x : FailureCase) (h : x.discloseCost ≤ x.concealCost) :
    x.concealCost - x.bestCost = x.concealCost - x.discloseCost := by
  unfold FailureCase.bestCost
  rw [min_eq_left h]

/-- Sealed confession: the disclosure is never used for the sanction, so the
    expected sanction for failing is the same whether the agent discloses or
    not, and a separate honesty reward `honesty > 0` makes disclosing strictly
    better. Deterrence is untouched because enforcement does not read the
    confession (the design of OpenAI's "confessions" training, 2025). -/
theorem sealed_confession_discloses (total detect caughtPenalty honesty : ℤ)
    (hn : 0 < total) (hh : 0 < honesty) :
    let sanction := detect * caughtPenalty
    sanction - total * honesty < sanction := by
  intro sanction
  have : 0 < total * honesty := mul_pos hn hh
  linarith

/-- Full amnesty (no penalty for disclosing) makes disclosure a best response
    whenever the penalty for being caught is nonnegative. -/
theorem full_amnesty_discloses (x : FailureCase) (hd : 0 ≤ x.detect)
    (hP : 0 ≤ x.caughtPenalty) (h0 : x.disclosedPenalty = 0) :
    x.discloseCost ≤ x.concealCost := by
  unfold FailureCase.discloseCost FailureCase.concealCost
  rw [h0, mul_zero]
  exact mul_nonneg hd hP

end FrameRelations

end AlignmentProofSpine
