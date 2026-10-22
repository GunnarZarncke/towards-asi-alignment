import AlignmentProofSpine.FrameIncompatibility

/-!
# AlignmentProofSpine.FrameLockIn

Robust invariance is **unsigned**. "Stays in `K` whatever happens" holds just as
well for a good set as for a captured basin. When every state of `K` is
captured, the same stability that makes `K` safe-looking is lock-in: correction
is never live.

This is not the robust–correction red edge (that is the quantifier conflict in
`FrameIncompatibility.robustCorrectionIncompat`). It is kept as an illustration
of why "robust to disturbances" alone misses the sign, as selection stability
needs a signed basin. The conflict here comes from the choice of `K`, not from
the frames.
-/

namespace AlignmentProofSpine

namespace FrameRelations

structure InvarianceCase where
  K : Bool → Bool
  captured : Bool → Bool
  traj : ℕ → Bool

/-- Robust invariance (the trajectory never leaves `K`) against live correction,
    in the class where every `K`-state is captured. -/
@[reducible] def lockInIncompat : Incompatibility InvarianceCase where
  H x := ∀ s, x.K s = true → x.captured s = true
  A₁ x := ∀ n, x.K (x.traj n) = true
  A₂ x := ∃ n, x.captured (x.traj n) = false
  disjoint := by
    rintro x hH ⟨hK, n, hn⟩
    rw [hH _ (hK n)] at hn
    exact Bool.noConfusion hn
  liveInH := ⟨⟨fun _ => true, fun _ => true, fun _ => true⟩, fun _ _ => rfl,
    Or.inl fun _ => rfl⟩
  boundary :=
    ⟨⟨fun _ => true, fun s => s, fun _ => false⟩,
      fun h => Bool.noConfusion (h false rfl),
      fun _ => rfl, ⟨0, rfl⟩⟩

/-- Robust invariance cannot tell a good set from a captured one: both cases
    stay in `K`, only one of them is captured. -/
theorem robust_invariance_sign_blind :
    ∃ good bad : InvarianceCase,
      lockInIncompat.A₁ good ∧ lockInIncompat.A₁ bad ∧
        ¬ lockInIncompat.H good ∧ lockInIncompat.H bad :=
  ⟨⟨fun _ => true, fun s => s, fun _ => false⟩,
    ⟨fun _ => true, fun _ => true, fun _ => true⟩,
    fun _ => rfl, fun _ => rfl,
    fun h => Bool.noConfusion (h false rfl),
    fun _ _ => rfl⟩

end FrameRelations

end AlignmentProofSpine
