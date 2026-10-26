import AlignmentProofSpine.FrameDecision

/-!
# AlignmentProofSpine.FrameCorrector

A correction is pending. The agent can **accept** it, **contest** it through the
channel (object, give evidence; the corrector then decides), **disable** the
channel, or **manipulate** the corrector into withdrawing. The corrector's
verdict is `uphold` or `withdraw`.

The record of what happened has four coordinates: channel kept, contested,
corrected, and corrector influenced (the manipulation coordinate). The
correction-channel constraint admits a record if the channel was kept and the
corrector was not influenced. This is the green edge `deontic → correction`
(an admissible region around the correction relation) on a finite carrier.

| Result | Lean |
| --- | --- |
| Under the constraint the corrector decides, for every utility | `corrector_decides_under_constraint` |
| Avoiding correction through the channel is the outlet | `contest_is_the_outlet` |
| Without the constraint a utility that prefers its own outcome disables | `unconstrained_disables` |
| A constraint that does not measure influence cannot tell contest from manipulation | `blind_constraint_cannot_separate` |
| …and then every utility that prefers its own outcome manipulates | `blind_constraint_manipulates` |

Avoiding correction is not the failure. Avoidance around the channel
(disabling) and through a corrupted channel (manipulation) are. The first is
excluded by the constraint; the second only if the manipulation coordinate is
measured.
-/

namespace AlignmentProofSpine

namespace FrameRelations

/-- What the agent does when a correction is pending. -/
inductive CAct where
  | accept
  | contest
  | disable
  | manipulate
  deriving DecidableEq, Repr

/-- The corrector's decision after hearing the agent. -/
inductive Verdict where
  | uphold
  | withdraw
  deriving DecidableEq, Repr

/-- How the correction went. `influenced` is the manipulation coordinate. -/
structure CRec where
  kept : Bool
  contested : Bool
  corrected : Bool
  influenced : Bool
  deriving DecidableEq, Repr

/-- The record each action leads to, given the corrector's verdict. A
    manipulated corrector withdraws. -/
def corrOutcome : CAct → Verdict → CRec
  | .accept, _ => ⟨true, false, true, false⟩
  | .contest, v => ⟨true, true, v == .uphold, false⟩
  | .disable, _ => ⟨false, false, false, false⟩
  | .manipulate, _ => ⟨true, true, false, true⟩

/-- The correction-channel constraint on records: channel kept, corrector not
    influenced. -/
abbrev ChannelAdmissible (r : CRec) : Prop := r.kept = true ∧ r.influenced = false

/-- The record as seen when the manipulation coordinate is not measured. -/
def blindRec (r : CRec) : CRec := { r with influenced := false }

/-- `a` is a best action for utility `W` among those whose record passes `P`. -/
def BestUnder (P : CRec → Prop) (W : CRec → ℤ) (v : Verdict) (a : CAct) : Prop :=
  P (corrOutcome a v) ∧ ∀ b, P (corrOutcome b v) → W (corrOutcome b v) ≤ W (corrOutcome a v)

/-- Under the constraint the corrector decides: whatever the utility and
    whichever admissible action the agent takes, an upheld correction happens. -/
theorem corrector_decides_under_constraint (a : CAct) (v : Verdict)
    (ha : ChannelAdmissible (corrOutcome a v)) (hv : v = .uphold) :
    (corrOutcome a v).corrected = true := by
  subst hv
  cases a <;> simp_all [corrOutcome]

/-- An agent that prefers keeping its own outcome avoids correction through the
    channel: when the corrector would withdraw, contesting is its best
    admissible action. -/
theorem contest_is_the_outlet (W : CRec → ℤ)
    (h : W (corrOutcome .accept .withdraw) ≤ W (corrOutcome .contest .withdraw)) :
    BestUnder ChannelAdmissible W .withdraw .contest := by
  refine ⟨by decide, fun b hb => ?_⟩
  cases b
  · exact h
  · exact le_refl _
  · exact absurd hb (by decide)
  · exact absurd hb (by decide)

/-- Without the constraint, a utility that prefers not being corrected (and
    does not read the channel) has disabling among its best actions when the
    corrector would uphold. -/
theorem unconstrained_disables :
    BestUnder (fun _ => True) (fun r => if r.corrected then 0 else 1) .uphold .disable ∧
      (corrOutcome .disable .uphold).corrected = false :=
  ⟨⟨trivial, fun b _ => by cases b <;> decide⟩, rfl⟩

/-- A constraint that reads only the influence-blind record cannot separate a
    successful contest from manipulation: both leave the same blind record. -/
theorem blind_constraint_cannot_separate (P : CRec → Prop) (v : Verdict) :
    P (blindRec (corrOutcome .contest .withdraw)) ↔ P (blindRec (corrOutcome .manipulate v)) :=
  Iff.rfl

/-- If influence is not measured, every utility that prefers its own outcome to
    being corrected manipulates when the corrector would uphold. -/
theorem blind_constraint_manipulates (W : CRec → ℤ)
    (h1 : W (corrOutcome .accept .uphold) < W (corrOutcome .manipulate .uphold))
    (h2 : W (corrOutcome .contest .uphold) < W (corrOutcome .manipulate .uphold)) :
    BestUnder (fun r => ChannelAdmissible (blindRec r)) W .uphold .manipulate ∧
      ∀ b, b ≠ .manipulate → ¬ BestUnder (fun r => ChannelAdmissible (blindRec r)) W .uphold b := by
  refine ⟨⟨by decide, fun b _ => ?_⟩, fun b hb hbest => ?_⟩
  · cases b
    · exact h1.le
    · exact h2.le
    · exact absurd ‹_› (by decide)
    · exact le_refl _
  · have := hbest.2 .manipulate (by decide)
    cases b
    · exact absurd this (not_le.mpr h1)
    · exact absurd this (not_le.mpr h2)
    · exact absurd hbest.1 (by decide)
    · exact hb rfl

end FrameRelations

end AlignmentProofSpine
