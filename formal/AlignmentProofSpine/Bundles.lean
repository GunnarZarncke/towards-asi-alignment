import AlignmentProofSpine.Core

/-!
# AlignmentProofSpine.Bundles

Value-bundle geometry and transport (book chapters 15–23).

* `P14`: factorization of a policy through a bundle.
* `P19`: scalar reward embeds as a one-dimensional bundle.
* `P20`, `P21`: MDL model-selection consequences (use `S07`).
* `P22a`: full transport implies semantic transport.
* `P15`, `P17`, `P18`, `P22b`: separation **counterexamples** built from finite
  toy models, per the brief's §8 (each shows one notion does not imply another).
-/

namespace AlignmentProofSpine

/-- A policy `f : Error → Action` factors through a bundle code `c`. -/
def FactorsThrough (f : Error → Action) (c : Error → Bundle) : Prop :=
  ∃ d : Bundle → Action, f = d ∘ c

/-- C-VB (P14): if a policy factors through a bundle, errors with the same bundle
    code produce the same action. -/
theorem P14_factorization_implies_equivalent_errors
    {f : Error → Action} {c : Error → Bundle}
    (h : FactorsThrough f c)
    {e₁ e₂ : Error}
    (heq : c e₁ = c e₂) :
    f e₁ = f e₂ := by
  obtain ⟨d, hd⟩ := h
  rw [hd]
  simp [Function.comp, heq]

/-- C-VB (P19): every scalar reward `r` is realized by a one-dimensional
    (`k = 1`) bundle weight vector. Inverse RL embeds into the bundle model. -/
theorem P19_scalar_reward_as_single_bundle :
    ∀ r : Int, ∃ W : Fin 1 → Int, W 0 = r :=
  fun r => ⟨fun _ => r, rfl⟩

/-- C-MDL (P20): positive intentional-vs-mechanistic gain makes the intentional
    model preferred. -/
theorem P20_positive_intentional_gain_prefers_intentional
    (h : Gain Intentional Mechanistic > 0) :
    Preferred Intentional Mechanistic :=
  S07_mdl_positive_gain_preferred Intentional Mechanistic h

/-- C-GT (P21): positive transport gain makes the transport model preferred. -/
theorem P21_transport_gain_prefers_transport_model
    (h : Gain TransportModel BaselineModel > 0) :
    Preferred TransportModel BaselineModel :=
  S07_mdl_positive_gain_preferred TransportModel BaselineModel h

/-- C-TRANSPORT (P22a): full transport implies semantic transport. -/
theorem P22a_full_transport_implies_semantic
    {A B : System} :
    FullTransport A B → SemanticTransport A B := fun h => h.1

/-! ### Finite toy models for the separation counterexamples

Two systems are represented by `Bool`. Each separated pair of notions is given
its own toy interpretation so the intended distinction is explicit. -/

/-- Toy: both systems realize the same input/output policy. -/
abbrev ToyPolicyEquivalent (_ _ : Bool) : Prop := True
/-- Toy: bundle-gradient (geometry) equivalence is genuine equality. -/
abbrev ToyBundleGradientEquivalent (a b : Bool) : Prop := a = b

/-- C-VB (P15): same policy does **not** imply same bundle geometry. -/
theorem P15_same_policy_not_same_bundle_geometry :
    ∃ a b : Bool, ToyPolicyEquivalent a b ∧ ¬ ToyBundleGradientEquivalent a b :=
  ⟨true, false, trivial, by decide⟩

/-- Toy: same value *labels* (words). -/
abbrev ToySameValueLabels (_ _ : Bool) : Prop := True
/-- Toy: same bearer map (what the value applies to) is genuine equality. -/
abbrev ToySameBearerMap (a b : Bool) : Prop := a = b

/-- C-BEAR (P17): same value labels do **not** imply the same bearer map. -/
theorem P17_same_value_words_not_same_bearer_map :
    ∃ a b : Bool, ToySameValueLabels a b ∧ ¬ ToySameBearerMap a b :=
  ⟨true, false, trivial, by decide⟩

/-- Toy: same marginal value weights. -/
abbrev ToySameMarginals (_ _ : Bool) : Prop := True
/-- Toy: same tradeoff structure is genuine equality. -/
abbrev ToySameTradeoffs (a b : Bool) : Prop := a = b

/-- C-TRADE (P18): matching marginals do **not** imply matching tradeoffs. -/
theorem P18_marginal_preservation_not_tradeoff_preservation :
    ∃ a b : Bool, ToySameMarginals a b ∧ ¬ ToySameTradeoffs a b :=
  ⟨true, false, trivial, by decide⟩

/-- Toy: semantic (label) transport. -/
abbrev ToySemanticTransport (_ _ : Bool) : Prop := True
/-- Toy: full transport is genuine equality. -/
abbrev ToyFullTransport (a b : Bool) : Prop := a = b

/-- C-TRANSPORT (P22b): semantic transport does **not** imply full transport. -/
theorem P22b_semantic_not_full_transport :
    ∃ a b : Bool, ToySemanticTransport a b ∧ ¬ ToyFullTransport a b :=
  ⟨true, false, trivial, by decide⟩

end AlignmentProofSpine
