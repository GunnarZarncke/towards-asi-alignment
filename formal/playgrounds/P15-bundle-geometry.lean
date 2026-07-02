/-!
Same observed policy, different bundle geometry (P15 counterexample).

Spine theorem: `AlignmentProofSpine.P15_same_policy_not_same_bundle_geometry`
(`formal/AlignmentProofSpine/Bundles.lean`, ch16–19 finite toy models).

Shows C-VB: matching observed actions does **not** imply matching bundle codes
or salience weights. Scalar CIRL-style inference can agree on behaviour while
value geometry differs (see ch46 CIRL / bundle crosswalk in the book).

Self-contained for Lean 4 Web — finite `PolicyProfile` copied from the spine.
-/

namespace Playground

/-- Finite policy profile: bundle codes, actions, bundle salience (ch16 Jacobian proxy). -/
structure PolicyProfile (nErr nAct k : Nat) where
  bundleCode : Fin nErr → Fin k
  action : Fin nErr → Fin nAct
  bundleSalience : Fin k → Int

def sameObservedPolicy {nErr nAct k : Nat}
    (p q : PolicyProfile nErr nAct k) : Prop :=
  ∀ e : Fin nErr, p.action e = q.action e

def sameBundleGeometry {nErr nAct k : Nat}
    (p q : PolicyProfile nErr nAct k) : Prop :=
  (∀ e : Fin nErr, p.bundleCode e = q.bundleCode e) ∧
    (∀ i : Fin k, p.bundleSalience i = q.bundleSalience i)

/-- Profile 0: errors map to bundles ⟨0,0⟩; actions ⟨0,1⟩; salience (1, 0). -/
def policyProfile0 : PolicyProfile 2 2 2 where
  bundleCode := fun i => if i.val = 0 then ⟨0, by decide⟩ else ⟨0, by decide⟩
  action := fun i => if i.val = 0 then ⟨0, by decide⟩ else ⟨1, by decide⟩
  bundleSalience := fun i => if i.val = 0 then 1 else 0

/-- Profile 1: same actions; bundle code at error 1 differs; salience (1, 2). -/
def policyProfile1 : PolicyProfile 2 2 2 where
  bundleCode := fun i => if i.val = 0 then ⟨0, by decide⟩ else ⟨1, by decide⟩
  action := fun i => if i.val = 0 then ⟨0, by decide⟩ else ⟨1, by decide⟩
  bundleSalience := fun i => if i.val = 0 then 1 else 2

theorem same_policy_profiles : sameObservedPolicy policyProfile0 policyProfile1 := by
  intro e
  match e with
  | ⟨0, _⟩ => rfl
  | ⟨1, _⟩ => rfl

theorem different_bundle_geometry_profiles :
    ¬ sameBundleGeometry policyProfile0 policyProfile1 := by
  intro h
  have hb := h.1
  have h1 := hb ⟨1, by decide⟩
  simp [policyProfile0, policyProfile1] at h1

/-- C-VB (P15): same policy does **not** imply same bundle geometry. -/
theorem P15_same_policy_not_same_bundle_geometry :
    ∃ p q : PolicyProfile 2 2 2,
      sameObservedPolicy p q ∧ ¬ sameBundleGeometry p q :=
  ⟨policyProfile0, policyProfile1, same_policy_profiles, different_bundle_geometry_profiles⟩

#check P15_same_policy_not_same_bundle_geometry
