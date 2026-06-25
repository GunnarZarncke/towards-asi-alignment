import AlignmentProofSpine.Core

/-!
# AlignmentProofSpine.Adversarial

Socio-technical selection, parasite aliasing, and adversarial measurement
(book chapters 32–37).

* `P31`: a safe agent can be selected against (finite toy model).
* `P33`: with no open edges there is no large cooperation component.
* `P34`: host-capacity aliasing — too few signals cannot injectively detect
  attacks (uses the from-scratch `finPigeonhole` from `Core`).
* `P37`: goal laundering — equal stated goals, different inferred goals.

Selection fitness is environment-relative deployment/control mass
(`DeploymentMass`, book ch32). Revenue, regulatory risk, and benchmark score
are proxies for selection-handle exercise, not primitive fitness terms.
-/

namespace AlignmentProofSpine

/-! ### P31: selection can disfavor safety (finite toy model) -/

/-- Toy safe predicate on two Boolean systems. -/
abbrev ToySafe (a : Bool) : Prop := a = true
/-- Toy deployment mass: the unsafe agent (`false`) accumulates more mass. -/
abbrev ToyDeploymentMass (_E : Environment) (a : Bool) : Int := if a then 0 else 1

/-- C-SEL (P31): there exist a safe and an unsafe agent such that the unsafe one
    has strictly higher deployment mass — local safety can be selected against. -/
theorem P31_safe_agent_selected_against :
    ∃ safe risky : Bool,
      ToySafe safe ∧ ¬ ToySafe risky ∧
        ToyDeploymentMass defaultEnvironment risky >
          ToyDeploymentMass defaultEnvironment safe :=
  ⟨true, false, rfl, by decide, by decide⟩

/-! ### P33: no open edges, no large cooperation component -/

axiom CoopGraph : Type
axiom OpenEdge : CoopGraph → Node → Node → Prop

/-- A "large" component is witnessed by at least one open edge. -/
def ComponentLarge (G : CoopGraph) : Prop := ∃ x y : Node, OpenEdge G x y

/-- C-GRAPH (P33): if no edges are open, no large cooperation component exists. -/
theorem P33_no_open_edges_no_large_component
    {G : CoopGraph}
    (hclosed : ∀ x y : Node, ¬ OpenEdge G x y) :
    ¬ ComponentLarge G := by
  rintro ⟨x, y, hxy⟩
  exact hclosed x y hxy

/-- C-PARASITE (P34): host-capacity aliasing (`C_X` in ch34). If there are strictly
    fewer signal classes than attack classes, no detector can injectively map
    attacks to signals — some attacks must alias. `Attack`/`Signal` are modelled
    as finite types `Fin nAttack` / `Fin nSignal`. -/
theorem P34_capacity_below_entropy_aliasing
    {nAttack nSignal : Nat}
    (hcard : nSignal < nAttack) :
    ¬ ∃ detect : Fin nAttack → Fin nSignal, Function.Injective detect := by
  rintro ⟨detect, hinj⟩
  have hle : nAttack ≤ nSignal := finPigeonhole detect hinj
  omega

/-! ### P37: goal laundering (finite toy model) -/

/-- Toy: stated goal is always `0`. -/
abbrev ToyStatedGoal (_ : Bool) : Nat := 0
/-- Toy: inferred goal differs between the two systems. -/
abbrev ToyInferredGoal (a : Bool) : Nat := if a then 0 else 1

/-- C-LAUNDER (P37): two systems can share a stated goal while their inferred
    goals differ. -/
theorem P37_stated_goal_not_inferred_goal :
    ∃ a b : Bool, ToyStatedGoal a = ToyStatedGoal b ∧ ToyInferredGoal a ≠ ToyInferredGoal b :=
  ⟨true, false, rfl, by decide⟩

end AlignmentProofSpine
