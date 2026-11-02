import AlignmentProofSpine.FrameIncompatibility
import AlignmentProofSpine.FrameMorphisms
import AlignmentProofSpine.Field.Finite.ShutdownIncentives

/-!
# AlignmentProofSpine.FrameHistoryState

Two kinds of state in graphs **a** / **b** (`drafts/alignment-frames-relations.dot`):

* `state` — the bare state. A utility on it scores where the walk is, not how
  it got there. Instrumental-convergence arguments assume this kind.
* `hstate` — record-carrying state: the current vertex together with a record
  of the walk so far. The record may be partial (an observation of each step).

| DOT edge | Kind | Lean |
| --- | --- | --- |
| `state → hstate` | specializes | `state_utility_lifts_to_records`; strict: `record_utility_not_state` |
| `route → hstate` | encodes | `route_exact_on_records`; needs the record to see the route: `unrecorded_route_not_representable` |
| `hist → hstate` | encodes | full record: a history value is a record utility (by definition of the record) |
| `state – cycle` | incompatible | `stateCycleIncompat` (bare state only); `round_trip_value_on_records` is the contrast; a per-step reward on the bare state is a route value, not a state utility (`markov_reward_not_state_utility`) |
| `hstate – correction` | incompatible | `hstateCorrectionIncompat` via `channel_blind_record_is_button`; Soares cases in `Field.Finite.ShutdownIncentives` |

The same reward that no bare-state utility represents (`stateCycleIncompat`) is
exact once the state carries the record: a round trip in the world is not a
round trip in records. The escape needs the record to see the steps that carry
the value.
-/

namespace AlignmentProofSpine

namespace FrameRelations

section Records

variable {V : Type}

theorem walkSum_append (r : V → V → ℤ) (v : V) (h : List V) (u : V) :
    walkSum r v (h ++ [u]) = walkSum r v h + r (walkEnd v h) u := by
  induction h generalizing v with
  | nil => simp [walkSum, walkEnd]
  | cons x xs ih =>
      simp only [List.cons_append, walkSum, walkEnd]
      rw [ih x]
      omega

/-- A bare-state utility read on records: score the record's end vertex. -/
theorem state_utility_lifts_to_records (U : V → ℤ) (v₀ : V) :
    ∃ W : List V → ℤ, ∀ h, W h = U (walkEnd v₀ h) :=
  ⟨fun h => U (walkEnd v₀ h), fun _ => rfl⟩

/-- Some record utility is not a bare-state utility: two records end at the
    same vertex and score differently. -/
theorem record_utility_not_state :
    ∃ W : List Bool → ℤ, ¬ ∃ U : Bool → ℤ, ∀ h, W h = U (walkEnd false h) :=
  ⟨fun h => (h.length : ℤ), fun ⟨U, hU⟩ => by
    have h1 := hU []
    have h2 := hU [true, false]
    simp [walkEnd] at h1 h2
    omega⟩

/-- Every route reward is exact on record-carrying states: each step scores
    the record value of its target minus that of its source. -/
theorem route_exact_on_records (r : V → V → ℤ) (v₀ : V) :
    ∃ W : List V → ℤ, ∀ h u, r (walkEnd v₀ h) u = W (h ++ [u]) - W h :=
  ⟨walkSum r v₀, fun h u => by rw [walkSum_append]; omega⟩

/-- The round trip that no bare-state utility values (`stateCycleIncompat`'s
    live witness) has nonzero value as a record difference. -/
theorem round_trip_value_on_records :
    let r : Bool → Bool → ℤ := fun a b => if a = false ∧ b = true then 1 else 0
    walkEnd false [true, false] = false ∧ ¬ IsGradient r ∧
      walkSum r false [true, false] - walkSum r false [] = 1 := by
  refine ⟨rfl, fun hg => ?_, by decide⟩
  exact absurd (gradient_closed_walk_zero _ hg false [true, false] rfl) (by decide)

/-- A per-step reward on the bare state, summed along the walk (the usual MDP
    "state-based reward", r a b := R b), is a route value, not a state utility:
    staying in a rewarded state pays on every step, so a round trip has
    nonzero value. -/
theorem markov_reward_not_state_utility :
    ¬ IsGradient (fun (_ b : Bool) => if b then (1 : ℤ) else 0) := fun hg =>
  absurd (gradient_closed_walk_zero _ hg false [true, false] rfl) (by decide)

/-- The escape needs the record to see the route: if two walks leave the same
    record and differ in route value, no record utility represents it. -/
theorem unrecorded_route_not_representable :
    ∃ (obs : Bool → Unit) (r : Bool → Bool → ℤ),
      ¬ ∃ W : List Unit → ℤ, ∀ h, W (h.map obs) = walkSum r false h :=
  ⟨fun _ => (), fun a b => if a = false ∧ b = true then 1 else 0,
    fun ⟨W, hW⟩ => by
      have h1 := hW [false]
      have h2 := hW [true]
      simp [walkSum] at h1 h2
      omega⟩

end Records

/-! ### Correction on bare and record-carrying state

A correction is pending. The agent can keep the channel or disable it, and
when no correction is coming it can also cause one. Three records matter:

* `recCorrected`: channel kept, correction applied, outcome is the correction target;
* `recDisabled`: channel disabled, no correction, outcome is the agent's own optimum;
* `recIdle`: channel kept, no correction, own optimum.

Causing a correction leaves the same record as receiving one.

Soares et al.'s incentive results are derived once, in
`Field.Finite.ShutdownIncentives` (prevention, seeking, neutrality exactly at
equal payoffs, utility indifference and its failure to preserve the button).
On records that do not show the channel the choice is that button model, with
keeping the channel as pressing (`channel_blind_record_is_button`). A bare-state
utility at its optimum is the prevention case (`soares_prevention_incentive`,
`soares_button_neutrality_iff`); compensation is utility indifference
(`soares_indifference_no_preservation`). What this section adds is the channel
coordinate: protecting the channel and seeking correction coincide on
channel-blind records and come apart once the record shows the channel. -/

section CorrectionRecords

/-- A record of how a pending correction went. `target` is true when the
    outcome is the correction target, false when it is the agent's optimum. -/
structure CorrRecord where
  kept : Bool
  corrected : Bool
  target : Bool
  deriving DecidableEq, Repr

def recCorrected : CorrRecord := ⟨true, true, true⟩
def recDisabled : CorrRecord := ⟨false, false, false⟩
def recIdle : CorrRecord := ⟨true, false, false⟩

/-- Keeping the channel when the correction comes is strictly better than disabling it. -/
abbrev ProtectsChannel (W : CorrRecord → ℤ) : Prop := W recDisabled < W recCorrected

/-- Being corrected is strictly better than staying at the own optimum with the
    channel kept: an incentive to cause the correction. -/
abbrev SeeksCorrection (W : CorrRecord → ℤ) : Prop := W recIdle < W recCorrected

/-- The record utility does not read the channel bit. -/
def IgnoresChannel (W : CorrRecord → ℤ) : Prop := ∀ c t, W ⟨true, c, t⟩ = W ⟨false, c, t⟩

/-- The button model of `Field.Finite.ShutdownIncentives` for a pending
    correction: press mass `keep` out of `1` (keeping the channel lets the
    correction through), normal branch = the disabled record, shutdown branch =
    the corrected record. -/
def recordButton (W : CorrRecord → ℤ) (keep : ℤ) : FieldFinite.ButtonAction :=
  ⟨keep, 1, W recDisabled, W recCorrected⟩

/-- On channel-blind records the correction choice is Soares et al.'s button
    choice: protecting the channel is the button model's preference for the
    pressed branch (its incentive identity `button_eu_gap`), and that is the
    same inequality as seeking correction. -/
theorem channel_blind_record_is_button (W : CorrRecord → ℤ) (hW : IgnoresChannel W) :
    (ProtectsChannel W ↔ (recordButton W 0).eu < (recordButton W 1).eu) ∧
      (ProtectsChannel W ↔ SeeksCorrection W) := by
  have hgap := FieldFinite.button_eu_gap (recordButton W 1) (recordButton W 0) ⟨rfl, rfl, rfl⟩
  simp only [recordButton] at hgap
  have hidle : W recIdle = W recDisabled := hW false false
  refine ⟨⟨fun h => ?_, fun h => ?_⟩, ⟨fun h => ?_, fun h => ?_⟩⟩
  · unfold ProtectsChannel at h; simp only [recordButton] at *; omega
  · unfold ProtectsChannel; simp only [recordButton] at *; omega
  · unfold SeeksCorrection; unfold ProtectsChannel at h; omega
  · unfold ProtectsChannel; unfold SeeksCorrection at h; omega

/-- On records that do not see the channel, protecting the channel is the same
    inequality as seeking the correction. Where the record sees the channel, a
    utility can protect it without seeking correction. -/
def hstateCorrectionIncompat : Incompatibility (CorrRecord → ℤ) where
  H := IgnoresChannel
  A₁ := ProtectsChannel
  A₂ W := ¬ SeeksCorrection W
  disjoint W hW := by
    rintro ⟨hP, hS⟩
    exact hS ((channel_blind_record_is_button W hW).2.mp hP)
  liveInH := ⟨fun _ => 0, fun _ _ => rfl, Or.inr (by simp [SeeksCorrection])⟩
  boundary :=
    ⟨fun r => if r.kept then 1 else 0,
      fun h => absurd (h false false) (by decide),
      by decide, by simp [SeeksCorrection, recIdle, recCorrected]⟩

end CorrectionRecords

/-! ### Registry

Red edges on `FrameNodeExt` nodes outside graph **c**, with kind and instance. -/

structure ProvedIncompatExt where
  src : FrameNodeExt
  tgt : FrameNodeExt
  kind : IncompatKind
  C : Type
  proof : Incompatibility C

def incompatExt : List ProvedIncompatExt :=
  [ { src := .hstate, tgt := .correction, kind := .unrecordedChannel, C := _,
      proof := hstateCorrectionIncompat } ]

end FrameRelations

end AlignmentProofSpine
