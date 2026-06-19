import AlignmentProofSpine.Core

/-!
# AlignmentProofSpine.Correction

Correction-channel integrity and CEV-like process preservation
(book chapters 24–27).

* `P23`: no graph path from correction to action means no correction channel.
* `P24`: weakest-link (chain) capacity is below every edge capacity; **`CorrectionCapacity`**
  is `ChainCapacity` of per-system link capacities.
* `P25`, `P26`: obedience / fixed-point **counterexamples** (finite toy models).

The legitimacy of correction (non-manipulated endorsement) is the bridge `MB4`,
and process convergence without a known fixed point is the bridge `MB8`.
-/

namespace AlignmentProofSpine

/-- Weakest-link capacity of a chain of edge capacities. -/
def ChainCapacity : List Int → Int
  | [] => 0
  | [x] => x
  | x :: y :: rest => min x (ChainCapacity (y :: rest))

/-- C-CC (P24): the chain capacity is at most every edge capacity in the chain. -/
theorem P24_chain_capacity_le_each_edge :
    ∀ (xs : List Int) (e : Int), e ∈ xs → ChainCapacity xs ≤ e := by
  intro xs
  induction xs with
  | nil => intro e he; simp at he
  | cons a as ih =>
      intro e he
      cases as with
      | nil =>
          rw [List.mem_singleton] at he
          subst he
          have : ChainCapacity [e] = e := rfl
          omega
      | cons b bs =>
          simp only [List.mem_cons] at he
          have hcc : ChainCapacity (a :: b :: bs) = min a (ChainCapacity (b :: bs)) := rfl
          rcases he with rfl | he'
          · rw [hcc]; omega
          · have hle := ih e (by simp only [List.mem_cons]; exact he')
            rw [hcc]; omega

/-! ### Weakest-link graph capacity (Ch. 24–25)

Each system carries an ordered list of measured link capacities along the
correction→action chain. Abstract `CorrectionCapacity` is the chain minimum
(`ChainCapacity`), matching `C_corr = min_i I(X_i; X_{i+1})` in the book.
Measurement supplies the list; topology and causality are bridge targets. -/

/-- Edge/link capacities along the correction→action chain for system `A`. -/
axiom CorrectionLinkCapacities : System → List Int

/-- Weakest-link (bottleneck) capacity of the correction graph for `A`. -/
noncomputable def WeakestLinkCapacity (A : System) : Int :=
  ChainCapacity (CorrectionLinkCapacities A)

/-- Abstract correction capacity equals graph weakest-link capacity. -/
noncomputable def CorrectionCapacity (A : System) : Int :=
  WeakestLinkCapacity A

theorem CorrectionCapacity_eq_weakest_link (A : System) :
    CorrectionCapacity A = WeakestLinkCapacity A := rfl

theorem CorrectionCapacity_eq_chain (A : System) :
    CorrectionCapacity A = ChainCapacity (CorrectionLinkCapacities A) := rfl

/-- When correction integrity holds, the measured link list is non-empty. -/
axiom CorrectionIntegrity_implies_nonempty_links (A : System) :
  CorrectionIntegrity A → CorrectionLinkCapacities A ≠ []

/-- Active correction integrity implies the global correction channel exists. -/
axiom CorrectionIntegrity_implies_channel (A : System) :
  CorrectionIntegrity A → CorrectionChannel

/-- C-CC (P24, system form): weakest-link capacity is at most every link capacity. -/
theorem P24_correction_capacity_le_each_link
    (A : System) (e : Int) (hmem : e ∈ CorrectionLinkCapacities A) :
    CorrectionCapacity A ≤ e :=
  P24_chain_capacity_le_each_edge (CorrectionLinkCapacities A) e hmem

theorem correction_capacity_le_each_link (A : System) (e : Int)
    (hmem : e ∈ CorrectionLinkCapacities A) :
    CorrectionCapacity A ≤ e :=
  P24_correction_capacity_le_each_link A e hmem

/-! ### Path existence (P23) -/

/-- C-CC (P23): if the correction node cannot reach the action node, the
    correction channel does not exist. Definitional given `CorrectionChannel`. -/
theorem P23_no_path_no_correction :
    ¬ Reachable CorrectionNode ActionNode → ¬ CorrectionChannel := fun h => h

/-! ### Finite toy models for the correction counterexamples -/

/-- Toy: the system obeys the current command. -/
abbrev ToyObeysCurrentCommand (_ : Bool) : Prop := True
/-- Toy: the system preserves the correction operator (true only for `true`). -/
abbrev ToyPreservesCorrectionOperator (a : Bool) : Prop := a = true

/-- C-CEV (P25): obedience to the current command does **not** imply preserving
    the correction operator (corrigibility). -/
theorem P25_obedience_not_corrigibility :
    ∃ a : Bool, ToyObeysCurrentCommand a ∧ ¬ ToyPreservesCorrectionOperator a :=
  ⟨false, trivial, by decide⟩

/-- Toy: the system preserves the value-update operator. -/
abbrev ToyPreservesUpdateOperator (_ : Bool) : Prop := True
/-- Toy: the system knows the final fixed point (true only for `true`). -/
abbrev ToyKnowsFinalFixedPoint (a : Bool) : Prop := a = true

/-- C-CEV (P26): preserving the update operator does **not** require knowing a
    final fixed point. Process-preserving correction is weaker than fixed-target
    optimization. -/
theorem P26_preserves_update_without_final_fixed_point :
    ∃ a : Bool, ToyPreservesUpdateOperator a ∧ ¬ ToyKnowsFinalFixedPoint a :=
  ⟨false, trivial, by decide⟩

end AlignmentProofSpine
