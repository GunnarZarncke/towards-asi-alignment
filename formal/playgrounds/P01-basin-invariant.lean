/-!
Basin invariance (P01) — playground for `AlignmentProofSpine.P01_basin_invariant`.

Spine location: `formal/AlignmentProofSpine/Certification.lean`
Axiom footprint: `State`, `SafeState` (see `formal/axiom-ledger.json`).

Claim: if a safety predicate holds at the initial state and every transition
preserves it, it holds after any finite number of steps.

This file is self-contained for Lean 4 Web:
- `Safe` stands in for spine `SafeState`
- `iterateN` matches `AlignmentProofSpine.Core.iterateN`
- No Mathlib or spine imports
-/

namespace Playground

/-- Finite iteration of a step function (spine: `AlignmentProofSpine.iterateN`). -/
def iterateN {α : Type} (f : α → α) : Nat → α → α
  | 0, x => x
  | n + 1, x => iterateN f n (f x)

/-- Basin invariance: initial safety + step preservation ⇒ safety after n steps. -/
theorem basin_invariant {α : Type} (step : α → α) (Safe : α → Prop)
    (x0 : α) (h0 : Safe x0) (hstep : ∀ x, Safe x → Safe (step x)) :
    ∀ n, Safe (iterateN step n x0) := by
  have aux : ∀ n x, Safe x → Safe (iterateN step n x) := by
    intro n
    induction n with
    | zero => intro x hx; exact hx
    | succ k ih => intro x hx; exact ih (step x) (hstep x hx)
  intro n
  exact aux n x0 h0

/-- Spine names this `BasinStable`; same one-step preservation hypothesis. -/
def BasinStable {α : Type} (step : α → α) (B : α → Prop) : Prop :=
  ∀ x, B x → B (step x)

example : BasinStable id (fun (_ : Nat) => True) := by
  intro _ _
  trivial

example : ∀ n, (2 * n) % 2 = 0 := by
  intro n
  induction n with
  | zero => rfl
  | succ k ih => simp [Nat.mul_succ, ih]

#check basin_invariant
#check BasinStable
