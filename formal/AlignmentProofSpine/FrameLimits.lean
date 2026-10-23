import AlignmentProofSpine.FrameMorphisms
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-!
# AlignmentProofSpine.FrameLimits

The **limit** and **strengthens** edges of the alignment-frame graphs **a** / **b**
(`drafts/alignment-frames-relations.dot`).

| DOT edge | Kind | Lean |
| --- | --- | --- |
| `viable → robust` | strengthens | `robust_strengthens_viable`, `robust_trajectory_stays`, `viable_not_robust` |
| `quant → state` | limit | `quantilizer_limit_is_argmax`, `quantilizer_never_argmax_without_base_mass` |
| `cev → state` | limit | `forced_halt_converges`, `forced_halt_depends_on_time` |

The `cev → state` reading is one interpretation of "forced halt at a scored
output": halting the procedure at step `n` and scoring that output is a state
score; it is a limit only where the procedure's outputs converge.
-/

namespace AlignmentProofSpine

namespace FrameRelations

/-! ### Strengthens: existential viability → robust invariance -/

section Strengthen

variable {σ α δ : Type}

/-- Some feedback control keeps `K` invariant under the nominal disturbance `d₀`
    (one-step form of existential viability). -/
def ViableSet (step : σ → α → δ → σ) (d₀ : δ) (K : σ → Prop) : Prop :=
  ∃ π : σ → α, ∀ s, K s → K (step s (π s) d₀)

/-- Some feedback control keeps `K` invariant under every disturbance in `D`. -/
def RobustViableSet (step : σ → α → δ → σ) (D : δ → Prop) (K : σ → Prop) : Prop :=
  ∃ π : σ → α, ∀ s, K s → ∀ d, D d → K (step s (π s) d)

/-- Robust invariance strengthens viability: if the nominal disturbance is in
    the robustness class, a robust control is a viable one. -/
theorem robust_strengthens_viable (step : σ → α → δ → σ) (D : δ → Prop) (K : σ → Prop)
    (d₀ : δ) (h₀ : D d₀) (hR : RobustViableSet step D K) : ViableSet step d₀ K :=
  let ⟨π, hπ⟩ := hR
  ⟨π, fun s hs => hπ s hs d₀ h₀⟩

/-- Closed-loop trajectory under control `π` and disturbance sequence `ds`. -/
def runCL (step : σ → α → δ → σ) (π : σ → α) (s : σ) (ds : ℕ → δ) : ℕ → σ
  | 0 => s
  | n + 1 => step (runCL step π s ds n) (π (runCL step π s ds n)) (ds n)

/-- The one-step condition gives the trajectory guarantee: every admissible
    disturbance sequence keeps the state in `K`. -/
theorem robust_trajectory_stays (step : σ → α → δ → σ) (D : δ → Prop) (K : σ → Prop)
    (π : σ → α) (hπ : ∀ s, K s → ∀ d, D d → K (step s (π s) d))
    (s : σ) (hs : K s) (ds : ℕ → δ) (hds : ∀ n, D (ds n)) :
    ∀ n, K (runCL step π s ds n) := by
  intro n
  induction n with
  | zero => exact hs
  | succ n ih => exact hπ _ ih _ (hds n)

/-- The strengthening is strict: a set can be viable under the nominal
    disturbance and fail robust invariance once all disturbances count. -/
theorem viable_not_robust :
    ∃ (step : Bool → Unit → Bool → Bool) (K : Bool → Prop),
      ViableSet step true K ∧ ¬ RobustViableSet step (fun _ => True) K :=
  ⟨fun _ _ d => d, fun s => s = true,
    ⟨fun _ => (), fun _ _ => rfl⟩,
    fun ⟨_, h⟩ => Bool.noConfusion (h true rfl false trivial)⟩

end Strengthen

/-! ### Limit: quantilizer → maximizer

Finite action set `acts`, base weights `p` (natural-number counts, so no real
analysis is needed), utility `U`. The `q`-quantilizer's support is the top-`q`
slice of the base: actions whose strictly better base mass is below `q`. -/

section Quantilizer

variable {A : Type}

/-- Base mass of the actions strictly better than `a`. -/
def betterMass (acts : Finset A) (p : A → ℕ) (U : A → ℤ) (a : A) : ℕ :=
  (acts.filter fun b => U a < U b).sum p

/-- Support of the `q`-quantilizer (ties with the cut-off included). -/
def quantSupport (acts : Finset A) (p : A → ℕ) (U : A → ℤ) (q : ℕ) : Finset A :=
  acts.filter fun a => betterMass acts p U a < q

/-- The maximizers of `U` in `acts`. -/
def argmaxSet (acts : Finset A) (U : A → ℤ) : Finset A :=
  acts.filter fun a => ∀ b ∈ acts, U b ≤ U a

/-- Quantile to the maximum: once `q` is positive and at most the base mass of
    some maximizer, the quantilizer's support is exactly the argmax set. -/
theorem quantilizer_limit_is_argmax (acts : Finset A) (p : A → ℕ) (U : A → ℤ)
    (m : A) (hm : m ∈ argmaxSet acts U) (q : ℕ) (hq0 : 0 < q) (hq : q ≤ p m) :
    quantSupport acts p U q = argmaxSet acts U := by
  have hm' := Finset.mem_filter.mp hm
  ext a
  simp only [quantSupport, argmaxSet, Finset.mem_filter]
  constructor
  · rintro ⟨ha, hlt⟩
    refine ⟨ha, fun b hb => ?_⟩
    by_contra hba
    have hUm : U a < U m := lt_of_lt_of_le (lt_of_not_ge hba) (hm'.2 b hb)
    have : p m ≤ betterMass acts p U a :=
      Finset.single_le_sum (fun _ _ => Nat.zero_le _)
        (Finset.mem_filter.mpr ⟨hm'.1, hUm⟩)
    omega
  · rintro ⟨ha, hmax⟩
    refine ⟨ha, ?_⟩
    have hempty : (acts.filter fun b => U a < U b) = ∅ :=
      Finset.filter_eq_empty_iff.mpr fun b hb => not_lt.mpr (hmax b hb)
    simp [betterMass, hempty, hq0]

/-- The limit needs base mass on a maximizer: if every maximizer has base mass
    zero, no positive quantile ever restricts the support to them, because the
    non-maximizers with no better base mass stay in. -/
theorem quantilizer_never_argmax_without_base_mass :
    ∃ (acts : Finset Bool) (p : Bool → ℕ) (U : Bool → ℤ),
      ∀ q, 0 < q → quantSupport acts p U q ≠ argmaxSet acts U :=
  ⟨{false, true}, fun b => if b then 0 else 1, fun b => if b then 1 else 0,
    fun q hq h => by
      have h0 : betterMass {false, true} (fun b => if b then 0 else 1)
          (fun b => if b then 1 else 0) false = 0 := by decide
      have : false ∈ quantSupport {false, true} (fun b => if b then 0 else 1)
          (fun b => if b then 1 else 0) q := by
        simp only [quantSupport, Finset.mem_filter, h0]
        exact ⟨by simp, hq⟩
      rw [h] at this
      simp [argmaxSet] at this⟩

end Quantilizer

/-! ### Limit: open procedure → scored output (forced halt) -/

section ForcedHalt

variable {O : Type}

/-- The procedure's outputs settle on `o` from some step on. -/
def ConvergesTo (out : ℕ → O) (o : O) : Prop := ∃ N, ∀ n, N ≤ n → out n = o

/-- Where the procedure converges, every late enough forced halt yields the
    same scored output: the state score of the limit. -/
theorem forced_halt_converges (out : ℕ → O) (score : O → ℤ) (o : O)
    (h : ConvergesTo out o) : ∃ N, ∀ n, N ≤ n → score (out n) = score o :=
  let ⟨N, hN⟩ := h
  ⟨N, fun n hn => by rw [hN n hn]⟩

/-- Where it does not converge, the halt time decides the score arbitrarily
    late: no single state score is the limit. -/
theorem forced_halt_depends_on_time :
    ∃ (out : ℕ → Bool) (score : Bool → ℤ),
      (∀ o, ¬ ConvergesTo out o) ∧
        ∀ N, ∃ n m, N ≤ n ∧ N ≤ m ∧ score (out n) ≠ score (out m) := by
  refine ⟨fun n => n % 2 == 0, fun b => if b then 1 else 0, ?_, ?_⟩
  · rintro o ⟨N, hN⟩
    have h1 := hN (2 * N) (by omega)
    have h2 := hN (2 * N + 1) (by omega)
    rw [← h2] at h1
    simp [Nat.mul_mod_right, Nat.add_mod] at h1
  · intro N
    refine ⟨2 * N, 2 * N + 1, by omega, by omega, ?_⟩
    simp [Nat.mul_mod_right, Nat.add_mod]

end ForcedHalt

/-! ### Registry -/

inductive LimitKind where
  | limit
  | strengthen
  deriving DecidableEq, Repr

structure LimitEdge where
  src : FrameNodeExt
  tgt : FrameNodeExt
  kind : LimitKind
  decl : String
  deriving Repr

/-- Limit and strengthens edges of graphs **a** / **b** with their main theorem. -/
def limitEdges : List LimitEdge :=
  [ { src := .viable, tgt := .robust, kind := .strengthen, decl := "robust_strengthens_viable" }
  , { src := .quant, tgt := .state, kind := .limit, decl := "quantilizer_limit_is_argmax" }
  , { src := .cev, tgt := .state, kind := .limit, decl := "forced_halt_converges" } ]

end FrameRelations

end AlignmentProofSpine
