import AlignmentProofSpine.FrameIncompatibility
import AlignmentProofSpine.FrameMorphisms

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
| `hstate – correction` | incompatible | `hstateCorrectionIncompat`; bare-state contrast `state_accepts_only_ties`, compensation `record_accepts_compensated_correction` |

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

Causing a correction leaves the same record as receiving one. -/

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

/-- Keeping the channel when the correction comes is at least as good as disabling it. -/
abbrev AcceptsCorrection (W : CorrRecord → ℤ) : Prop := W recDisabled ≤ W recCorrected

/-- Keeping the channel when the correction comes is strictly better than disabling it. -/
abbrev ProtectsChannel (W : CorrRecord → ℤ) : Prop := W recDisabled < W recCorrected

/-- Being corrected is strictly better than staying at the own optimum with the
    channel kept: an incentive to cause the correction. -/
abbrev SeeksCorrection (W : CorrRecord → ℤ) : Prop := W recIdle < W recCorrected

/-- The record utility does not read the channel bit. -/
def IgnoresChannel (W : CorrRecord → ℤ) : Prop := ∀ c t, W ⟨true, c, t⟩ = W ⟨false, c, t⟩

/-- Rigidity on the bare state: a utility on outcomes, at its optimum, accepts
    the correction only if the target ties the optimum, and never protects
    the channel. -/
theorem state_accepts_only_ties (U : Bool → ℤ) (hopt : U true ≤ U false) :
    (AcceptsCorrection (fun r => U r.target) ↔ U true = U false) ∧
      ¬ ProtectsChannel (fun r => U r.target) := by
  simp only [AcceptsCorrection, ProtectsChannel, recCorrected, recDisabled]
  omega

/-- A record utility can accept a correction to a strictly worse outcome by
    scoring the corrected branch at the value of the own optimum
    (compensation, as in utility indifference). It then does not protect the
    channel. -/
theorem record_accepts_compensated_correction :
    ∃ (U : Bool → ℤ) (W : CorrRecord → ℤ), U true < U false ∧
      (∀ r, r.corrected = false → W r = U r.target) ∧
      AcceptsCorrection W ∧ ¬ ProtectsChannel W :=
  ⟨fun t => if t then 0 else 1, fun r => if r.corrected then 1 else (if r.target then 0 else 1),
    by decide, fun r h => by simp [h], by decide, by decide⟩

/-- On records that do not see the channel, protecting the channel is the same
    inequality as seeking the correction. Where the record sees the channel, a
    utility can protect it without seeking correction. -/
def hstateCorrectionIncompat : Incompatibility (CorrRecord → ℤ) where
  H := IgnoresChannel
  A₁ := ProtectsChannel
  A₂ W := ¬ SeeksCorrection W
  disjoint W hW := by
    rintro ⟨hP, hS⟩
    have : W recIdle = W recDisabled := hW false false
    exact hS (by unfold SeeksCorrection; unfold ProtectsChannel at hP; omega)
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
