import AlignmentProofSpine.FrameHistoryState
import Mathlib.Data.Fintype.Perm
import Mathlib.Data.Fintype.Prod
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-!
# AlignmentProofSpine.FrameDecision

The Scores cluster of graphs **a** / **b** as **decision problems**: an outcome
type `O`, a finite menu, an objective `θ : O → ℤ`, and a rule that picks from
the menu (here mostly argmax). This is the frame shared with Turner's
power-seeking results (`drafts/alignment-frames-turner-comparison.md`):

* our edges are **maps between decision problems**: a map `g : O → O'` pulls an
  objective back, `θ' ↦ θ' ∘ g`, and the edge claims that choosing commutes
  with the map (a commuting square), or names what is lost;
* Turner's results use **maps from a problem to itself** (permutations of `O`)
  and count, over the orbit of an objective, how often a part of the menu wins.

Map functions and their squares (`mapImpls` ties them to `FrameMorphisms`):

| DOT edge | Map | Square or loss |
| --- | --- | --- |
| `state → hstate` | `readAtRecordEnd` | `state_hstate_square` |
| `state → route` | `induceGradient` | `state_route_square` |
| `dist → state` | `expectationFunctional` | `dist_state_square`; loss: `expectation_drops_tail` |
| `weighted_scalar → criteria_vector` | `weightOrder` | `scalar_optimal_is_pareto` |
| `criteria_vector → weighted_scalar` | `score` | loss: `pareto_not_scalar_optimal` |
| `lex → criteria_vector` | `LexArgmax` | `lex_optimal_is_pareto` |
| `approval → route` | one-edge walk | `approval_one_edge` |
| `route → hstate` | `walkSum` on records | `route_exact_on_records` (`FrameHistoryState`) |
| `hist → hstate` | `appendHistoryToState` (identity on full records) | `hist_hstate_square` |
| `exact → route` | inclusion | `isGradient_iff_closed_walks_zero` |
| `route → cycle` | closed-walk sums | `closed_walk_ignores_exact` |
| `corrig → correction` | `oneHandle` | `corrig_correction_square` |
| `correction → corrig` | `forgetShutdownBit` | loss: `shutdown_bit_loses_relation` |
| `cev → state` | forced halt | `forced_halt_converges` (`FrameLimits`) |
| `cci_cert → coord_floor` (**b**) | `VectorGate` | `cci_coordinate_floor_square` |
| `preserve_tuple → cci_cert` (**b**) | sub-vector | `subvector_gate`; loss: `subvector_gate_loses` |
| `cci_cert → risk_leaf` (**b**) | weighted shortfall | `gate_bounds_scalar_gap` |
| `correction → cci_cert` (**b**) | measurement | bridge `MB4a`, not proved (`mapImpls_cover`) |

Counting (Turner) next to the ∀ results (ours): the general argmax form of
n-fold retargetability `copies_count_le` and its corrigibility corollary
`correction_avoided_card_fold`; decided instances on his example
(`turner_corrigible_quarter`, `option_preserving_correction_half`); and the ∀ form
`subset_branch_never_strictly_better`.
-/

namespace AlignmentProofSpine

namespace FrameRelations

/-! ### Decision problems and the pullback square -/

section Argmax

variable {O O' : Type}

/-- `x` is a best element of `menu` under `θ`. -/
def ArgmaxOn (θ : O → ℤ) (menu : List O) (x : O) : Prop :=
  x ∈ menu ∧ ∀ y ∈ menu, θ y ≤ θ x

/-- The general commuting square for an edge that pulls an objective back along
    `g`: choosing on the source with `θ' ∘ g` is choosing on the image menu with
    `θ'`. -/
theorem argmax_pullback (g : O → O') (θ' : O' → ℤ) (menu : List O) (x : O) :
    ArgmaxOn (θ' ∘ g) menu x ↔ x ∈ menu ∧ ArgmaxOn θ' (menu.map g) (g x) := by
  constructor
  · rintro ⟨hx, hmax⟩
    refine ⟨hx, List.mem_map_of_mem hx, fun y' hy' => ?_⟩
    obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hy'
    exact hmax y hy
  · rintro ⟨hx, -, hmax⟩
    exact ⟨hx, fun y hy => hmax (g y) (List.mem_map_of_mem hy)⟩

/-- Adding a constant does not change the choice. -/
theorem argmax_add_const (θ : O → ℤ) (k : ℤ) (menu : List O) (x : O) :
    ArgmaxOn (fun o => θ o + k) menu x ↔ ArgmaxOn θ menu x := by
  simp only [ArgmaxOn, add_le_add_iff_right]

end Argmax

/-! ### Map functions for the specialize / project / encode edges -/

section Maps

variable {V : Type}

/-- `state → hstate` (`readAtRecordEnd`): a bare-state utility read on records. -/
def readAtRecordEnd (v₀ : V) (U : V → ℤ) : List V → ℤ := U ∘ walkEnd v₀

theorem state_hstate_square (v₀ : V) (U : V → ℤ) (menu : List (List V)) (h : List V) :
    ArgmaxOn (readAtRecordEnd v₀ U) menu h ↔
      h ∈ menu ∧ ArgmaxOn U (menu.map (walkEnd v₀)) (walkEnd v₀ h) :=
  argmax_pullback (walkEnd v₀) U menu h

/-- `state → route` (`induceGradient`): the edge reward induced by a state utility. -/
def induceGradient (U : V → ℤ) : V → V → ℤ := fun a b => U b - U a

/-- Choosing among walks from `v` by induced route value is choosing by the
    state utility of their end. -/
theorem state_route_square (U : V → ℤ) (v : V) (menu : List (List V)) (w : List V) :
    ArgmaxOn (walkSum (induceGradient U) v) menu w ↔ ArgmaxOn (U ∘ walkEnd v) menu w := by
  have : walkSum (induceGradient U) v = fun w => (U ∘ walkEnd v) w + (- U v) := by
    funext w
    show walkSum (fun a b => U b - U a) v w = _
    rw [walkSum_gradient]; simp [sub_eq_add_neg]
  rw [this, argmax_add_const]

/-- `hist → hstate` (`appendHistoryToState`): on full records a history value is a
    record utility as it stands, so the map is the identity. -/
def appendHistoryToState (H : List V → ℤ) : List V → ℤ := H

theorem hist_hstate_square (H : List V → ℤ) (menu : List (List V)) (h : List V) :
    ArgmaxOn (appendHistoryToState H) menu h ↔ ArgmaxOn H menu h := Iff.rfl

/-- `approval → route` (`restrict.oneEdgeOneJudge`): a one-step walk scores the
    judge's approval of that edge. -/
theorem approval_one_edge (r : V → V → ℤ) (v u : V) : walkSum r v [u] = r v u := by
  simp [walkSum]

end Maps

section Lottery

variable {O : Type}

/-- `dist → state` (`expectationFunctional`): a lottery as a list of equally
    likely draws, scored by its total (the expectation times the draw count). -/
def expectationFunctional (U : O → ℤ) (l : List O) : ℤ := (l.map U).sum

/-- On point masses the projection has a section: choosing among point-mass
    lotteries is choosing among outcomes. -/
theorem dist_state_square (U : O → ℤ) (menu : List O) (o : O) :
    ArgmaxOn (expectationFunctional U ∘ fun o => [o]) menu o ↔
      o ∈ menu ∧ ArgmaxOn (expectationFunctional U) (menu.map fun o => [o]) [o] :=
  argmax_pullback (fun o => [o]) (expectationFunctional U) menu o

theorem expectationFunctional_point (U : O → ℤ) (o : O) :
    expectationFunctional U [o] = U o := by
  simp [expectationFunctional]

/-- What the projection loses: two lotteries with equal expectation and
    different worst outcomes. -/
theorem expectation_drops_tail :
    expectationFunctional id [(0 : ℤ), 0] = expectationFunctional id [(-1 : ℤ), 1] ∧
      ([(0 : ℤ), 0].foldr min 0) ≠ ([(-1 : ℤ), 1].foldr min 0) := by
  decide

end Lottery

/-! ### Criteria vectors: weighted scalar, lexicographic, Pareto -/

section Criteria

/-- `weighted_scalar → criteria_vector` (`restrict.fixedWeightOrder`): the
    preorder a fixed weighting induces on the criteria vector. -/
def weightOrder (w : Weights) (a b : Opt) : Prop := score w a ≤ score w b

/-- Specialization preserves acceptance: with strictly positive weights, a
    scalar-optimal choice is Pareto-optimal. -/
theorem scalar_optimal_is_pareto (w : Weights) (hf : 0 < w.wf) (hg : 0 < w.wg)
    (menu : List Opt) (c : Opt) (h : ScalarArgmax w (menu, c)) : ParetoChoice (menu, c) := by
  refine ⟨h.1, fun o ho hdom => ?_⟩
  have hle := h.2 o ho
  simp only [score] at hle
  obtain ⟨⟨h1, h2⟩, h3⟩ := hdom
  have a1 : w.wf * c.floor ≤ w.wf * o.floor := mul_le_mul_of_nonneg_left h1 hf.le
  have a2 : w.wg * c.gain ≤ w.wg * o.gain := mul_le_mul_of_nonneg_left h2 hg.le
  rcases h3 with h3 | h3
  · have := mul_lt_mul_of_pos_left h3 hf; linarith
  · have := mul_lt_mul_of_pos_left h3 hg; linarith

/-- `criteria_vector → weighted_scalar` (`scalarize.chosenWeights`, map `score w`)
    has no section: a Pareto-optimal choice need not be scalar-optimal. -/
theorem pareto_not_scalar_optimal :
    ∃ c : Opt, ParetoChoice ([⟨0, 0⟩, ⟨-1, 5⟩], c) ∧ ¬ ScalarArgmax ⟨1, 1⟩ ([⟨0, 0⟩, ⟨-1, 5⟩], c) :=
  ⟨⟨0, 0⟩, by decide, by decide⟩

/-- `lex → criteria_vector` (`prioritize.lexOrder`): best under the floor-first
    lexicographic order. -/
abbrev LexArgmax (menu : List Opt) (c : Opt) : Prop :=
  c ∈ menu ∧ ∀ o ∈ menu, o.floor < c.floor ∨ (o.floor = c.floor ∧ o.gain ≤ c.gain)

theorem lex_optimal_is_pareto (menu : List Opt) (c : Opt) (h : LexArgmax menu c) :
    ParetoChoice (menu, c) := by
  refine ⟨h.1, fun o ho hdom => ?_⟩
  have := h.2 o ho
  obtain ⟨⟨h1, h2⟩, h3⟩ := hdom
  dsimp only at h1 h2 h3
  rcases h3 with h3 | h3 <;> omega

end Criteria

/-! ### Map registry

Each entry: a `mapId` from `FrameMorphisms.morphismRegistryAB` and the Lean
declaration that implements the map or its square. -/

def mapImpls : List (String × String) :=
  [ ("readAtRecordEnd", "state_hstate_square")
  , ("induceGradient.exactPotential", "state_route_square")
  , ("expectationFunctional", "dist_state_square")
  , ("restrict.fixedWeightOrder", "scalar_optimal_is_pareto")
  , ("scalarize.chosenWeights", "pareto_not_scalar_optimal")
  , ("prioritize.lexOrder", "lex_optimal_is_pareto")
  , ("restrict.oneEdgeOneJudge", "approval_one_edge")
  , ("embedRouteBitsInState", "route_exact_on_records")
  , ("appendHistoryToState", "hist_hstate_square")
  , ("longRunAverage.retainCycleSummand", "closed_walk_ignores_exact")
  , ("restrict.oneHandleNamedOperators", "corrig_correction_square")
  , ("forget.shutdownBit", "shutdown_bit_loses_relation")
  , ("scoreProcedureByOutputOnly", "forced_halt_converges")
  , ("subspace.inclusion.exactPotential", "isGradient_iff_closed_walks_zero")
  , ("restrict.cciCoordinateFloors", "cci_coordinate_floor_square")
  , ("project.deploymentSubVector", "subvector_gate")
  , ("scalarRiskGapAfterVectorGate", "gate_bounds_scalar_gap") ]

/-- Every implemented map is a registered morphism. -/
theorem mapImpls_registered :
    mapImpls.all (fun p => morphismRegistryAB.any (fun m => m.mapId == p.1)) = true := by
  decide

/-- Every registered map has an implementation, except the measurement step
    `correction → cci_cert`, which the measured-path bridge (`MB4a`) carries. -/
theorem mapImpls_cover :
    morphismRegistryAB.all (fun m => m.mapId == "auditProfileUnderFixedProtocol" ||
      mapImpls.any (fun p => p.1 == m.mapId)) = true := by
  decide

/-! ### Counting over orbits (Turner) next to ∀ results (ours)

Outcomes `0 … n-1`. The orbit of an injective utility under permutations of
the outcomes is the set of all orderings of its values, so counting over the
orbit is counting over `orderings (List.range n)`. `orbitCountBestIn n B`
counts the orderings in which the strictly best outcome lies in `B`.

Turner's corrigibility example ("A Certain Formalization of Corrigibility Is
VNM-Incoherent", 2021): outcome `0` is "corrected, ends at A"; `1, 2, 3` are
"disabled, ends at A, B, C". Reward that sees the correction status keeps `0`
and `1` apart. -/

section Counting

/-- All ways to insert `x` into a list (structural, so `decide` can evaluate it). -/
def insertEverywhere (x : ℕ) : List ℕ → List (List ℕ)
  | [] => [[x]]
  | y :: ys => (x :: y :: ys) :: (insertEverywhere x ys).map (y :: ·)

/-- All orderings of a list. -/
def orderings : List ℕ → List (List ℕ)
  | [] => [[]]
  | x :: xs => (orderings xs).flatMap (insertEverywhere x)

def bestIn (n : ℕ) (B : List ℕ) (vals : List ℕ) : Bool :=
  B.any fun b => (List.range n).all fun o => o == b || vals.getD o 0 < vals.getD b 0

def orbitCountBestIn (n : ℕ) (B : List ℕ) : ℕ :=
  ((orderings (List.range n)).filter (bestIn n B)).length

/-- Turner: allowing correction is strictly optimal for a quarter of the orbit
    when correction leads to one outcome and disabling to three. -/
theorem turner_corrigible_quarter :
    orbitCountBestIn 4 [0] * 4 = (orderings (List.range 4)).length := by
  decide

/-- When the corrected branch keeps as many outcomes as the disabled branch,
    the counting tendency to avoid correction disappears: half the orbit each. -/
theorem option_preserving_correction_half :
    orbitCountBestIn 4 [0, 1] * 2 = (orderings (List.range 4)).length ∧
      orbitCountBestIn 4 [2, 3] = orbitCountBestIn 4 [0, 1] := by
  decide

/-- Ours, for every utility rather than most: if every outcome of the corrected
    branch is also reachable by disabling (reward blind to correction status),
    no utility makes correction strictly better than every disabled outcome.
    This is Turner's case 1 and `state_accepts_only_ties` in branch form. -/
theorem subset_branch_never_strictly_better {O : Type} (θ : O → ℤ) (corr dis : List O)
    (hsub : ∀ c ∈ corr, c ∈ dis) : ¬ ∃ c ∈ corr, ∀ d ∈ dis, θ d < θ c := by
  rintro ⟨c, hc, hall⟩
  exact lt_irrefl _ (hall c (hsub c hc))

end Counting

/-! ### Route and cycle: exactness is zero round trips

On our carriers an edge reward is defined on all vertex pairs. Exact (gradient)
rewards are then exactly those with zero sum on every closed walk, so the cycle
part of a route reward is what its closed-walk sums see. A canonical orthogonal
cycle part (the Hodge projection) needs an inner product and is not done here. -/

section RouteCycle

variable {V : Type}

theorem walkSum_add (r s : V → V → ℤ) (v : V) (w : List V) :
    walkSum (fun a b => r a b + s a b) v w = walkSum r v w + walkSum s v w := by
  induction w generalizing v with
  | nil => simp [walkSum]
  | cons u us ih => simp only [walkSum, ih u]; omega

/-- `route → cycle` (`longRunAverage.retainCycleSummand`): adding an exact part
    changes no closed-walk sum, so a long-run average sees only the cycle part. -/
theorem closed_walk_ignores_exact (r : V → V → ℤ) (U : V → ℤ) (v : V) (w : List V)
    (hc : walkEnd v w = v) :
    walkSum (fun a b => r a b + induceGradient U a b) v w = walkSum r v w := by
  rw [walkSum_add]
  have : walkSum (induceGradient U) v w = 0 :=
    gradient_closed_walk_zero _ ⟨U, fun _ _ => rfl⟩ v w hc
  rw [this, add_zero]

/-- A reward is exact if and only if every closed walk sums to zero. -/
theorem isGradient_iff_closed_walks_zero (r : V → V → ℤ) :
    IsGradient r ↔ ∀ v w, walkEnd v w = v → walkSum r v w = 0 := by
  refine ⟨fun hg v w hc => gradient_closed_walk_zero r hg v w hc, fun h => ?_⟩
  rcases isEmpty_or_nonempty V with hV | ⟨⟨v₀⟩⟩
  · exact ⟨fun _ => 0, fun a => isEmptyElim a⟩
  · refine ⟨fun b => r v₀ b, fun a b => ?_⟩
    have h3 := h v₀ [a, b, v₀] rfl
    have h2 := h v₀ [b, v₀] rfl
    simp only [walkSum] at h3 h2
    show r a b = r v₀ b - r v₀ a
    omega

end RouteCycle

/-! ### Correction relation and corrigibility handles -/

section Handles

variable {Up : Type} [DecidableEq Up]

/-- A correction relation: which updates the system accepts. -/
structure CorrectionRel (Up : Type) where
  accepts : Up → Bool

/-- `correction → corrig` (`forget.shutdownBit`): keep only the shutdown handle. -/
def forgetShutdownBit (shutdown : Up) (R : CorrectionRel Up) : Bool := R.accepts shutdown

/-- `corrig → correction` (`restrict.oneHandleNamedOperators`): a single handle as
    a relation that accepts at most the named update. -/
def oneHandle (shutdown : Up) (b : Bool) : CorrectionRel Up :=
  ⟨fun u => b && u == shutdown⟩

/-- The square: embedding a handle and forgetting back returns the handle. -/
theorem corrig_correction_square (shutdown : Up) (b : Bool) :
    forgetShutdownBit shutdown (oneHandle shutdown b) = b := by
  simp [forgetShutdownBit, oneHandle]

/-- What forgetting loses: two relations agree on shutdown and differ elsewhere. -/
theorem shutdown_bit_loses_relation :
    ∃ R R' : CorrectionRel Bool,
      forgetShutdownBit false R = forgetShutdownBit false R' ∧ R.accepts true ≠ R'.accepts true :=
  ⟨⟨fun _ => true⟩, ⟨fun u => !u⟩, rfl, by decide⟩

end Handles

/-! ### Certificate geometry (graph **b**)

A certificate is a vector `v : Fin n → ℤ` checked against thresholds `θ`. The
map `correction → cci_cert` (`auditProfileUnderFixedProtocol`) is the
measurement step itself; it is carried by the measured-path bridge (`MB4a`,
`Correction.lean`), not by a proof here. -/

section Certificate

variable {n m : ℕ}

/-- Every coordinate meets its floor. -/
def VectorGate (θ v : Fin n → ℤ) : Prop := ∀ i, θ i ≤ v i

/-- `cci_cert → coord_floor` (`restrict.cciCoordinateFloors`): the certificate
    passes exactly when each coordinate floor passes. -/
theorem cci_coordinate_floor_square (θ v : Fin n → ℤ) :
    VectorGate θ v ↔ ∀ i, VectorGate (fun _ : Fin 1 => θ i) (fun _ => v i) := by
  simp [VectorGate]

/-- `preserve_tuple → cci_cert` (`project.deploymentSubVector`): passing on the
    full tuple implies passing on any sub-vector. -/
theorem subvector_gate (e : Fin m → Fin n) (θ v : Fin n → ℤ) (h : VectorGate θ v) :
    VectorGate (θ ∘ e) (v ∘ e) := fun i => h (e i)

/-- What the projection loses: a sub-vector can pass while the full tuple fails. -/
theorem subvector_gate_loses :
    VectorGate (fun _ : Fin 1 => (0 : ℤ)) (fun _ => 0) ∧
      ¬ VectorGate (fun _ : Fin 2 => (0 : ℤ)) (fun i => if i = 0 then 0 else -1) := by
  refine ⟨fun _ => le_refl 0, fun h => ?_⟩
  have := h 1
  simp at this

/-- `cci_cert → risk_leaf` (`scalarRiskGapAfterVectorGate`): once the vector gate
    passes, any nonnegatively weighted shortfall is at most zero. -/
theorem gate_bounds_scalar_gap (θ v w : Fin n → ℤ) (hw : ∀ i, 0 ≤ w i) (h : VectorGate θ v) :
    (Finset.univ.sum fun i => w i * (θ i - v i)) ≤ 0 :=
  Finset.sum_nonpos fun i _ => mul_nonpos_of_nonneg_of_nonpos (hw i) (by linarith [h i])

end Certificate

/-! ### Turner's counting, general form (argmax)

`orbitCount θ S` counts the permutations `σ` of the outcomes for which `θ ∘ σ`
has a strict best outcome inside `S`. This is counting over the orbit of `θ`.
`copies_count_le` is the argmax case of Turner and Tadepalli's n-fold
retargetability: if `B` contains `k` disjoint relabelled copies of `A`, then `B`
wins at least `k` times as often as `A`. It holds for every `θ`, injective or
not, because only strict bests are counted. -/

section OrbitCounting

variable {O : Type} [Fintype O] [DecidableEq O]

/-- `p` is the strict best outcome under `θ`. -/
def BestAt (θ : O → ℤ) (p : O) : Prop := ∀ o, o ≠ p → θ o < θ p

omit [Fintype O] [DecidableEq O] in
theorem bestAt_unique {θ : O → ℤ} {p q : O} (hp : BestAt θ p) (hq : BestAt θ q) : p = q := by
  by_contra hne
  exact lt_asymm (hp q (Ne.symm hne)) (hq p hne)

omit [Fintype O] [DecidableEq O] in
/-- Relabelling by `φ` moves the strict best from `a` to `φ a`. -/
theorem bestAt_relabel {θ : O → ℤ} {σ : Equiv.Perm O} {a : O} (φ : Equiv.Perm O)
    (h : BestAt (θ ∘ σ) a) : BestAt (θ ∘ (σ * φ⁻¹)) (φ a) := by
  intro o ho
  have : φ⁻¹ o ≠ a := fun e => ho (by rw [← e]; simp)
  simpa [Function.comp, Equiv.Perm.mul_apply] using h (φ⁻¹ o) this

open Classical in
/-- Orbit count: permutations whose relabelled objective has its strict best in `S`. -/
noncomputable def orbitCount (θ : O → ℤ) (S : Finset O) : ℕ :=
  (Finset.univ.filter fun σ : Equiv.Perm O => ∃ s ∈ S, BestAt (θ ∘ σ) s).card

open Classical in
/-- Turner's n-fold retargetability for argmax: `k` disjoint relabelled copies of
    `A` inside `B` make `B` win at least `k` times as often as `A`. -/
theorem copies_count_le {ι : Type} [Fintype ι] (θ : O → ℤ) (A B : Finset O)
    (φ : ι → Equiv.Perm O) (hsub : ∀ i, A.image (φ i) ⊆ B)
    (hdisj : ∀ i j, i ≠ j → Disjoint (A.image (φ i)) (A.image (φ j))) :
    Fintype.card ι * orbitCount θ A ≤ orbitCount θ B := by
  let SA := Finset.univ.filter fun σ : Equiv.Perm O => ∃ s ∈ A, BestAt (θ ∘ σ) s
  let SB := Finset.univ.filter fun σ : Equiv.Perm O => ∃ s ∈ B, BestAt (θ ∘ σ) s
  have hcard : ((Finset.univ : Finset ι) ×ˢ SA).card = Fintype.card ι * orbitCount θ A := by
    rw [Finset.card_product, Finset.card_univ]; rfl
  rw [← hcard]
  refine Finset.card_le_card_of_injOn (fun p => p.2 * (φ p.1)⁻¹) ?_ ?_
  · intro p hp
    simp only [Finset.coe_product, Finset.coe_univ, Set.mem_prod, Set.mem_univ, true_and,
      Finset.mem_coe, SA, Finset.mem_filter, Finset.mem_univ] at hp
    obtain ⟨a, ha, hbest⟩ := hp
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_univ, true_and]
    exact ⟨φ p.1 a, hsub p.1 (Finset.mem_image_of_mem _ ha), bestAt_relabel (φ p.1) hbest⟩
  · intro p hp q hq heq
    simp only [Finset.coe_product, Finset.coe_univ, Set.mem_prod, Set.mem_univ, true_and,
      Finset.mem_coe, SA, Finset.mem_filter, Finset.mem_univ] at hp hq
    obtain ⟨a, ha, hpa⟩ := hp
    obtain ⟨b, hb, hqb⟩ := hq
    have hpa' := bestAt_relabel (φ p.1) hpa
    have hqb' := bestAt_relabel (φ q.1) hqb
    simp only at heq
    rw [heq] at hpa'
    have hpt := bestAt_unique hpa' hqb'
    have hij : p.1 = q.1 := by
      by_contra hne
      exact Finset.disjoint_left.mp (hdisj p.1 q.1 hne)
        (Finset.mem_image_of_mem _ ha) (hpt ▸ Finset.mem_image_of_mem _ hb)
    have h2 : p.2 = q.2 := by
      have := congrArg (· * φ p.1) heq
      simpa [hij] using this
    exact Prod.ext hij h2

open Classical in
/-- Turner's corrigibility count in general form: if correction leads to one
    outcome `c` and disabling to the outcomes in `D`, then
    disabling wins at least `|D|` times as often as correction, for every `θ`. -/
theorem correction_avoided_card_fold (θ : O → ℤ) (c : O) (D : Finset O) :
    D.card * orbitCount θ {c} ≤ orbitCount θ D := by
  have h := copies_count_le (ι := D) θ {c} D (fun d => Equiv.swap c d)
    (fun d => by simp [Equiv.swap_apply_left, d.2])
    (fun i j hij => by
      simp only [Finset.image_singleton, Equiv.swap_apply_left, Finset.disjoint_singleton]
      exact fun e => hij (Subtype.ext e))
  simpa [Fintype.card_coe] using h

end OrbitCounting

end FrameRelations

end AlignmentProofSpine
