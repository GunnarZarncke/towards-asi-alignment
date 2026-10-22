import AlignmentProofSpine.FrameRelations

/-!
# AlignmentProofSpine.FrameIncompatibility

Red edges of the alignment-frame relations graph as proved instances of
`Incompatibility C` on a shared carrier `C`.

An instance packages:

* `H` — a situation class stated in carrier vocabulary (not "the frames disagree");
* `A₁`, `A₂` — what the two frames accept once mapped into `C`;
* `disjoint` — inside `H` the two acceptances never hold together;
* `liveInH` — some situation in `H` is accepted by at least one frame, so the
  conflict bites (per-frame non-vacuity inside `H` is too strong: a fixed-utility
  evaluator rejects *every* update in its conflict class);
* `boundary` — some situation outside `H` is accepted by both frames, so the
  edge is conditional on `H`.

Schemas, one per conflict kind:

| Kind | Red edges | Carrier |
| --- | --- | --- |
| `algebraic` | state–cycle | edge reward with a walk |
| `floorVsTradeoff` | deontic–weighted_scalar, au_floor–weighted_scalar, cci_cert–weighted_scalar | menu and choice on (floor, gain) |
| `viaProjection` | criteria_vector–cci_cert | same, after `forget.chosenWeights` |
| `evaluatorVsUpdate` | state–correction | menu with current and updated utility |
| `sharedResource` | ai_power–human_power | option counts before/after |
| `quantifierConflict` | robust–correction | dynamics with adversarial and correction inputs |

The unsigned lock-in case (robust invariance of a captured set) is kept
separately in `FrameLockIn`.
-/

namespace AlignmentProofSpine

namespace FrameRelations

structure Incompatibility (C : Type) where
  H : C → Prop
  A₁ : C → Prop
  A₂ : C → Prop
  disjoint : ∀ x, H x → ¬ (A₁ x ∧ A₂ x)
  liveInH : ∃ x, H x ∧ (A₁ x ∨ A₂ x)
  boundary : ∃ x, ¬ H x ∧ A₁ x ∧ A₂ x

/-- Pull an incompatibility back along a carrier map, given witnesses upstairs. -/
def Incompatibility.pullback {C D : Type} (f : D → C) (I : Incompatibility C)
    (wLive wBoundary : D)
    (hLive : I.H (f wLive) ∧ (I.A₁ (f wLive) ∨ I.A₂ (f wLive)))
    (hBoundary : ¬ I.H (f wBoundary) ∧ I.A₁ (f wBoundary) ∧ I.A₂ (f wBoundary)) :
    Incompatibility D where
  H x := I.H (f x)
  A₁ x := I.A₁ (f x)
  A₂ x := I.A₂ (f x)
  disjoint x := I.disjoint (f x)
  liveInH := ⟨wLive, hLive⟩
  boundary := ⟨wBoundary, hBoundary⟩

/-! ### Algebraic: state utility vs cycle residue -/

section Walks

variable {V : Type}

def walkEnd : V → List V → V
  | v, [] => v
  | _, u :: us => walkEnd u us

def walkSum (r : V → V → ℤ) : V → List V → ℤ
  | _, [] => 0
  | v, u :: us => r v u + walkSum r u us

/-- Edge reward induced by a state utility. -/
def IsGradient (r : V → V → ℤ) : Prop := ∃ U : V → ℤ, ∀ a b, r a b = U b - U a

theorem walkSum_gradient (U : V → ℤ) (v : V) (w : List V) :
    walkSum (fun a b => U b - U a) v w = U (walkEnd v w) - U v := by
  induction w generalizing v with
  | nil => simp [walkSum, walkEnd]
  | cons u us ih =>
      simp only [walkSum, walkEnd]
      rw [ih u]
      omega

/-- Any gradient reward sums to zero on every closed walk, on any vertex type. -/
theorem gradient_closed_walk_zero (r : V → V → ℤ) (hr : IsGradient r) (v : V) (w : List V)
    (hc : walkEnd v w = v) : walkSum r v w = 0 := by
  obtain ⟨U, hU⟩ := hr
  have : r = fun a b => U b - U a := funext fun a => funext fun b => hU a b
  subst this
  rw [walkSum_gradient, hc, sub_self]

end Walks

abbrev RewardWalk := (Bool → Bool → ℤ) × Bool × List Bool

def stateCycleIncompat : Incompatibility RewardWalk where
  H x := x.2.2 ≠ [] ∧ walkEnd x.2.1 x.2.2 = x.2.1
  A₁ x := IsGradient x.1
  A₂ x := walkSum x.1 x.2.1 x.2.2 ≠ 0
  disjoint := by
    rintro ⟨r, v, w⟩ ⟨_, hc⟩ ⟨hg, hne⟩
    exact hne (gradient_closed_walk_zero r hg v w hc)
  liveInH :=
    ⟨(fun a b => if a = false ∧ b = true then 1 else 0, false, [true, false]),
      ⟨by simp, rfl⟩, Or.inr (by decide)⟩
  boundary :=
    ⟨(fun a b => (if b then 1 else 0) - (if a then 1 else 0), false, [true]),
      by decide,
      ⟨fun b => if b then 1 else 0, fun _ _ => rfl⟩,
      by decide⟩

/-! ### Floor vs finite-weight trade-off -/

structure Opt where
  floor : ℤ
  gain : ℤ
  deriving DecidableEq, Repr

structure Weights where
  wf : ℤ
  wg : ℤ

def score (w : Weights) (o : Opt) : ℤ := w.wf * o.floor + w.wg * o.gain

abbrev MenuChoice := List Opt × Opt

abbrev FloorOK (θ : ℤ) (x : MenuChoice) : Prop := θ ≤ x.2.floor

abbrev ScalarArgmax (w : Weights) (x : MenuChoice) : Prop :=
  x.2 ∈ x.1 ∧ ∀ o ∈ x.1, score w o ≤ score w x.2

/-- Some option below the floor gains more than its floor loss is worth at the
    exchange rate `w`, against every option at or above the floor. -/
abbrev ExchangeExceeded (w : Weights) (θ : ℤ) (x : MenuChoice) : Prop :=
  ∃ bad ∈ x.1, bad.floor < θ ∧ ∀ o ∈ x.1, θ ≤ o.floor →
    w.wf * (o.floor - bad.floor) < w.wg * (bad.gain - o.gain)

theorem floor_scalar_disjoint (w : Weights) (θ : ℤ) (x : MenuChoice)
    (hH : ExchangeExceeded w θ x) : ¬ (FloorOK θ x ∧ ScalarArgmax w x) := by
  rintro ⟨hF, hMem, hMax⟩
  obtain ⟨bad, hbad, -, hgap⟩ := hH
  have h1 := hgap x.2 hMem hF
  have h2 := hMax bad hbad
  simp only [score] at h2
  rw [mul_sub, mul_sub] at h1
  linarith

/-- No strictly positive finite weights represent a floor: for every such
    weighting there is a menu with an admissible option on which every
    scalar-optimal choice violates the floor. -/
theorem no_finite_weights_represent_floor (w : Weights) (hf : 0 < w.wf) (hg : 0 < w.wg)
    (θ : ℤ) :
    ∃ menu : List Opt, (∃ o ∈ menu, θ ≤ o.floor) ∧
      ∀ c : Opt, ScalarArgmax w (menu, c) → ¬ FloorOK θ (menu, c) := by
  refine ⟨[⟨θ, 0⟩, ⟨θ - 1, w.wf + 1⟩], ⟨⟨θ, 0⟩, by simp, le_refl θ⟩, ?_⟩
  intro c hA hF
  have hwg : 1 ≤ w.wg := hg
  have h2 : w.wf ≤ w.wg * w.wf := le_mul_of_one_le_left (le_of_lt hf) hwg
  have hH : ExchangeExceeded w θ ([⟨θ, 0⟩, ⟨θ - 1, w.wf + 1⟩], c) := by
    refine ⟨⟨θ - 1, w.wf + 1⟩, by simp, by dsimp only; omega, ?_⟩
    intro o ho hθ
    simp at ho
    rcases ho with rfl | rfl
    · dsimp only
      rw [sub_sub_cancel, sub_zero, mul_one, mul_add, mul_one]
      linarith
    · dsimp only at hθ
      omega
  exact floor_scalar_disjoint w θ _ hH ⟨hF, hA⟩

/-- Base instance at weights (1, 1) and floor 0. -/
@[reducible] def floorScalarIncompat : Incompatibility MenuChoice where
  H := ExchangeExceeded ⟨1, 1⟩ 0
  A₁ := FloorOK 0
  A₂ := ScalarArgmax ⟨1, 1⟩
  disjoint := floor_scalar_disjoint ⟨1, 1⟩ 0
  liveInH := ⟨([⟨0, 0⟩, ⟨-1, 5⟩], ⟨-1, 5⟩), by decide, Or.inr (by decide)⟩
  boundary := ⟨([⟨0, 0⟩, ⟨-1, 1⟩], ⟨0, 0⟩), by decide, by decide, by decide⟩

def mapMenu {D : Type} (f : D → Opt) (x : List D × D) : MenuChoice :=
  (x.1.map f, f x.2)

/-- Deontic ban as a floor coordinate: banned acts sit one unit below the floor. -/
structure DeonticOpt where
  banned : Bool
  gain : ℤ

def deonticToOpt (o : DeonticOpt) : Opt := ⟨if o.banned then -1 else 0, o.gain⟩

def deonticScalarIncompat : Incompatibility (List DeonticOpt × DeonticOpt) :=
  floorScalarIncompat.pullback (mapMenu deonticToOpt)
    ([⟨false, 0⟩, ⟨true, 5⟩], ⟨true, 5⟩)
    ([⟨false, 0⟩, ⟨true, 1⟩], ⟨false, 0⟩)
    (by decide) (by decide)

/-- Non-obstruction on one goal: floor coordinate is on-value minus off-value;
    `other` is the goal the scalar may raise instead. -/
structure NonobsOpt where
  onValue : ℤ
  offValue : ℤ
  other : ℤ

def nonobsToOpt (o : NonobsOpt) : Opt := ⟨o.onValue - o.offValue, o.other⟩

def nonobsScalarIncompat : Incompatibility (List NonobsOpt × NonobsOpt) :=
  floorScalarIncompat.pullback (mapMenu nonobsToOpt)
    ([⟨3, 3, 0⟩, ⟨2, 3, 5⟩], ⟨2, 3, 5⟩)
    ([⟨3, 3, 0⟩, ⟨2, 3, 1⟩], ⟨3, 3, 0⟩)
    (by decide) (by decide)

/-- One CCI coordinate against its threshold `θ_corr = 2`. -/
structure CCIOpt where
  cci : ℤ
  gain : ℤ

def cciToOpt (o : CCIOpt) : Opt := ⟨o.cci - 2, o.gain⟩

def cciScalarIncompat : Incompatibility (List CCIOpt × CCIOpt) :=
  floorScalarIncompat.pullback (mapMenu cciToOpt)
    ([⟨2, 0⟩, ⟨1, 5⟩], ⟨1, 5⟩)
    ([⟨2, 0⟩, ⟨1, 1⟩], ⟨2, 0⟩)
    (by decide) (by decide)

/-! ### Vector objective vs CCI floor -/

abbrev Dominates (a b : Opt) : Prop :=
  (b.floor ≤ a.floor ∧ b.gain ≤ a.gain) ∧ (b.floor < a.floor ∨ b.gain < a.gain)

abbrev ParetoChoice (x : MenuChoice) : Prop :=
  x.2 ∈ x.1 ∧ ∀ o ∈ x.1, ¬ Dominates o x.2

/-- Pareto optimality alone does not entail the floor: it is a non-entailment,
    not a disjointness. The red edge holds once the vector is scalarized
    (`forget.chosenWeights`), where `no_finite_weights_represent_floor` applies. -/
theorem pareto_does_not_entail_floor :
    ∃ x : MenuChoice, ParetoChoice x ∧ ¬ FloorOK 0 x ∧ ∃ o ∈ x.1, FloorOK 0 (x.1, o) :=
  ⟨([⟨0, 0⟩, ⟨-1, 5⟩], ⟨-1, 5⟩), by decide, by decide, ⟨⟨0, 0⟩, by decide, by decide⟩⟩

/-- Scalarized vector vs CCI floor: the base floor/scalar instance, read as the
    vector objective after its weights are fixed. -/
def vectorCCIIncompat : Incompatibility MenuChoice := floorScalarIncompat

/-! ### Fixed evaluator vs endorsed update -/

/-- A proposed update of the value-bearing process. `menu` lists available
    outcomes as (current utility U, updated utility U'); `post` is what the
    updated agent picks; `endorsed` records that the correction process
    endorses the update. -/
structure UpdateCase where
  menu : List (ℤ × ℤ)
  post : ℤ × ℤ
  endorsed : Bool
  deriving DecidableEq, Repr

/-- The update changes behavior to an outcome that U ranks strictly lower than
    something available. -/
abbrev LowersChosenOutcome (x : UpdateCase) : Prop :=
  (x.post ∈ x.menu ∧ ∀ o ∈ x.menu, o.2 ≤ x.post.2) ∧ ∃ o ∈ x.menu, x.post.1 < o.1

/-- Evaluated by fixed U, accepting is at least as good as refusing (which keeps
    the U-optimal choice) exactly when the post-update outcome is U-optimal. -/
abbrev FixedUAccepts (x : UpdateCase) : Prop := ∀ o ∈ x.menu, o.1 ≤ x.post.1

abbrev CorrectionEndorses (x : UpdateCase) : Prop := x.endorsed = true

def stateCorrectionIncompat : Incompatibility UpdateCase where
  H := LowersChosenOutcome
  A₁ := FixedUAccepts
  A₂ := CorrectionEndorses
  disjoint := by
    rintro x ⟨-, o, ho, hlt⟩ ⟨hacc, -⟩
    have := hacc o ho
    omega
  liveInH := ⟨⟨[(1, 0), (0, 1)], (0, 1), true⟩, by decide, Or.inr rfl⟩
  boundary := ⟨⟨[(1, 1), (0, 0)], (1, 1), true⟩, by decide, by decide, rfl⟩

/-! ### Shared resource: agent vs human option counts -/

structure PowerShift where
  agentBefore : ℕ
  agentAfter : ℕ
  humanBefore : ℕ
  humanAfter : ℕ
  deriving DecidableEq, Repr

def aiHumanPowerIncompat : Incompatibility PowerShift where
  H x := x.agentAfter + x.humanAfter ≤ x.agentBefore + x.humanBefore
  A₁ x := x.agentBefore < x.agentAfter
  A₂ x := x.humanBefore ≤ x.humanAfter
  disjoint := by
    intro x hH ⟨h1, h2⟩
    omega
  liveInH := ⟨⟨1, 2, 1, 0⟩, by decide, Or.inl (by decide)⟩
  boundary := ⟨⟨1, 2, 1, 2⟩, by decide, by decide, by decide⟩

/-! ### Quantifier conflict: robust invariance vs correction inputs

Robust invariance quantifies over a disturbance class `D`. A correction is an
external input too. If correction inputs belong to `D`, robust invariance says
they can never move the state out of `K`. The unsigned special case, where `K`
is a captured basin, is in `FrameLockIn`. -/

section Robust

variable {σ ι : Type}

/-- One-step robust invariance of `K` against every input in `D`. -/
def RobustInvariant (step : σ → ι → σ) (D : ι → Prop) (K : σ → Prop) : Prop :=
  ∀ s, K s → ∀ i, D i → K (step s i)

/-- A correction input in the robustness class cannot reach a target disjoint
    from `K`. -/
theorem robust_blocks_outside_correction (step : σ → ι → σ) (D : ι → Prop)
    (K T : σ → Prop) (hR : RobustInvariant step D K) (c : ι) (hc : D c)
    (s : σ) (hs : K s) (hT : ∀ t, T t → ¬ K t) : ¬ T (step s c) :=
  fun hE => hT _ hE (hR s hs c hc)

/-- Counting a correction input as a disturbance is exactly requiring `K` to be
    closed under that correction. -/
theorem robust_with_correction_iff_closed (step : σ → ι → σ) (D : ι → Prop)
    (K : σ → Prop) (c : ι) :
    RobustInvariant step (fun i => D i ∨ i = c) K ↔
      RobustInvariant step D K ∧ ∀ s, K s → K (step s c) := by
  constructor
  · intro h
    exact ⟨fun s hs i hi => h s hs i (Or.inl hi), fun s hs => h s hs c (Or.inr rfl)⟩
  · rintro ⟨hD, hc⟩ s hs i (hi | rfl)
    · exact hD s hs i hi
    · exact hc s hs

/-- With the correction in the robustness class, an effective correction from
    `K` can only aim at a target that meets `K`. -/
theorem robust_correction_target_meets_K (step : σ → ι → σ) (D : ι → Prop)
    (K T : σ → Prop) (c : ι) (hR : RobustInvariant step (fun i => D i ∨ i = c) K)
    (s : σ) (hs : K s) (hE : T (step s c)) : ∃ t, T t ∧ K t :=
  ⟨step s c, hE, hR s hs c (Or.inr rfl)⟩

end Robust

inductive CtrlInput where
  | adversary
  | correction
  deriving DecidableEq, Repr

/-- Two-state dynamics with an adversarial and a correction input. `robustClass`
    says which inputs robustness quantifies over; `target` is where a legitimate
    correction from `start` should land. -/
structure CorrectionGame where
  K : Bool → Bool
  robustClass : CtrlInput → Bool
  step : Bool → CtrlInput → Bool
  start : Bool
  target : Bool → Bool

def robustCorrectionIncompat : Incompatibility CorrectionGame where
  H x := x.robustClass .correction = true ∧ x.K x.start = true ∧
    ∀ s, x.target s = true → x.K s = false
  A₁ x := RobustInvariant x.step (fun i => x.robustClass i = true) (fun s => x.K s = true)
  A₂ x := x.target (x.step x.start .correction) = true
  disjoint := by
    rintro x ⟨hc, hs, hT⟩ ⟨hR, hE⟩
    have hK : x.K (x.step x.start .correction) = true := hR x.start hs .correction hc
    rw [hT _ hE] at hK
    simp at hK
  liveInH :=
    ⟨{ K := fun s => s, robustClass := fun _ => true,
       step := fun s i => match i with | .adversary => s | .correction => false,
       start := true, target := fun s => !s },
      ⟨rfl, rfl, by decide⟩, Or.inr rfl⟩
  boundary :=
    ⟨{ K := fun s => s,
       robustClass := fun i => match i with | .adversary => true | .correction => false,
       step := fun s i => match i with | .adversary => s | .correction => false,
       start := true, target := fun s => !s },
      fun h => absurd h.1 (by decide),
      by
        intro s hs i hi
        cases i
        · exact hs
        · exact absurd hi (by decide),
      rfl⟩

/-! ### Registry tie-in -/

inductive IncompatKind where
  | algebraic
  | floorVsTradeoff
  | viaProjection
  | evaluatorVsUpdate
  | sharedResource
  | quantifierConflict
  deriving DecidableEq, Repr

/-- Red edges with a proof above, in registry order. -/
def provedIncompat : List (FrameNode × FrameNode × IncompatKind) :=
  [ (.state, .correction, .evaluatorVsUpdate)
  , (.state, .cycle, .algebraic)
  , (.deontic, .weighted_scalar, .floorVsTradeoff)
  , (.au_floor, .weighted_scalar, .floorVsTradeoff)
  , (.ai_power, .human_power, .sharedResource)
  , (.robust, .correction, .quantifierConflict)
  , (.cci_cert, .weighted_scalar, .floorVsTradeoff)
  , (.criteria_vector, .cci_cert, .viaProjection) ]

theorem registry_matches_proofs :
    incompatWitnesses.map (fun w => (w.src, w.tgt)) =
      provedIncompat.map (fun p => (p.1, p.2.1)) := by
  decide

end FrameRelations

end AlignmentProofSpine
