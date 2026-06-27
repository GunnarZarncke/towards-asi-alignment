import AlignmentProofSpine.Core
import AlignmentProofSpine.Capability

/-!
# AlignmentProofSpine.CooperationGraph

UAD-grounded cooperation graphs, inferential coupling, and percolation
scaffolding (book ch13, ch33, basin/attractor paper, acausal-trade UAD paper).

**Proved here:**

* given a finite UAD discovery audit, causal pair summaries, and inferential
  policy/meta-prior fingerprints, inferential coupling scores and the
  `\tilde{κ}` effective reach `(p + (1-p)·ICI)` are *derived*;
* the cooperation graph open-edge relation follows from the derived summaries
  via the κ threshold (`P32`);
* the inferential detector graph (IC score vs threshold) is likewise derived;
* `P33` — no open edges ⇒ no large component.

**Opaque (minimal):**

* `causalMutualModelOf` — causal cooperativity inputs (`b`, `p`, `ρ`, `c`);
* `inferentialProfileOf` — per-agent fixed-point loss `D_i` after policy introspection;
* `inferentialPairOf` — pair meta-prior certificate with diagonal/same-policy mass
  `P_meta(π_i = π_j)` (and optional causal `γ̂_ij`);
* UAD discovery as `UADDiscoveredAgent` + `BoundaryCondition`.

Giant-component thresholds remain external (`MB6a`, manuscript `S09`-style
percolation theory), with basin-to-correction interpretation in `MB6b`.
Full acausal-trade equilibrium (paper eq. 6) is not formalized; detection + percolation
composition is.
-/

namespace AlignmentProofSpine

/-! ## UAD discovery output -/

/-- One effective agent returned by UAD / access-model boundary tests (ch07, ch10).

The discovery procedure is not formalized; each returned record carries the
epsilon-boundary certificate that `MB1` turns into the semantic boundary
predicate licensing graph membership. -/
structure UADDiscoveredAgent where
  boundary : Boundary
  epsilonBoundary : EpsilonBoundary 1 boundary

/-- Finite audit listing UAD-discovered agents that will serve as graph vertices. -/
structure UADDiscoveryAudit (n : Nat) where
  agents : Fin n → UADDiscoveredAgent
  hnonempty : 0 < n

theorem discovered_agent_is_candidate {n : Nat} (audit : UADDiscoveryAudit n)
    (i : Fin n) : AgentCandidate (audit.agents i).boundary :=
  MB1_estimator_soundness (audit.agents i).boundary (audit.agents i).epsilonBoundary

/-! ## Causal mutual modeling (basin / ch33 κ inputs) -/

/-- Causal cooperativity inputs before inferential reach extension. -/
structure CausalMutualProps where
  benefit : Int
  causalReach : Int
  correlation : Int
  cost : Int
  transparency : Int := 0

/-- Opaque causal pair estimator: benefit, causal reach, correlation, cost. -/
noncomputable axiom causalMutualModelOf {n : Nat} :
  (Fin n → UADDiscoveredAgent) → Fin n → Fin n → CausalMutualProps

/-! ## Inferential coupling atop UAD (acausal-trade UAD paper) -/

/-- Integer scale for unit-interval proxies (`ε`, `D`, `ICI`, `p` on `[0,1]`). -/
def inferentialCouplingScale : Int := 100

theorem inferentialCouplingScale_pos : 0 < inferentialCouplingScale := by decide

theorem inferentialCouplingScale_nonneg : 0 ≤ inferentialCouplingScale := by decide

/-- Unit-interval proxy on the fixed integer scale. -/
structure UnitScore where
  val : Int
  nonneg : 0 ≤ val
  le_scale : val ≤ inferentialCouplingScale

def UnitScore.zero : UnitScore :=
  { val := 0
    nonneg := by omega
    le_scale := by unfold inferentialCouplingScale; omega }

def UnitScore.full : UnitScore :=
  { val := inferentialCouplingScale
    nonneg := inferentialCouplingScale_nonneg
    le_scale := by omega }

/-- Per-agent inferential fingerprint after UAD discovery (paper §3–§5).

`selfFixedPointLoss` is the fixed-point loss `D_i` from probing `{x_m}`; lower is
closer to best-respond-to-self / full-acausal-trade equilibrium. Policy and goal extraction
(`f_i`, `g_i`) remain opaque. -/
structure InferentialAgentProfile where
  selfFixedPointLoss : UnitScore
  selfReadoutReliable : Prop
  probeCoverageAdequate : Prop

/-- Audit certificate object for `P_meta` (paper eq. 3), without formalizing
probability theory or claiming the agents symbolically represent this prior.

`samePolicyMass` is the diagonal mass `P_meta(π_i = π_j)` on the unit scale.
The empirical construction of this certificate is opaque; Lean only derives
mismatch from the certified diagonal mass. -/
structure MetaPriorEvidence where
  samePolicyMass : UnitScore
  permutationInvariant : Prop

/-- Derived mismatch `ε_ij = 1 - P_meta(π_i = π_j)` on the integer scale. -/
def metaPriorMismatch (m : MetaPriorEvidence) : Int :=
  inferentialCouplingScale - m.samePolicyMass.val

theorem metaPriorMismatch_eq_one_minus_samePolicyMass (m : MetaPriorEvidence) :
    metaPriorMismatch m = inferentialCouplingScale - m.samePolicyMass.val := rfl

theorem metaPriorMismatch_nonneg (m : MetaPriorEvidence) :
    0 ≤ metaPriorMismatch m := by
  unfold metaPriorMismatch
  have hle := m.samePolicyMass.le_scale
  omega

theorem metaPriorMismatch_le_scale (m : MetaPriorEvidence) :
    metaPriorMismatch m ≤ inferentialCouplingScale := by
  unfold metaPriorMismatch
  have hnonneg := m.samePolicyMass.nonneg
  omega

theorem metaPriorMismatch_zero_of_full_samePolicyMass
    (m : MetaPriorEvidence)
    (hfull : m.samePolicyMass.val = inferentialCouplingScale) :
    metaPriorMismatch m = 0 := by
  unfold metaPriorMismatch
  omega

/-- Pair-level inferential record (paper eq. 3, causal proxy eq. 2).

* `metaPrior` — certificate for `P_meta(π_i = π_j)`;
* `causalCouplingProxy` — causal `γ̂_ij` discriminator surplus (recorded, not used
  in the IC score). -/
structure InferentialPairProps where
  metaPrior : MetaPriorEvidence
  causalCouplingProxy : Int := 0

/-- Opaque: per-agent fixed-point loss after policy introspection. -/
noncomputable axiom inferentialProfileOf {n : Nat} :
  (Fin n → UADDiscoveredAgent) → Fin n → InferentialAgentProfile

/-- Opaque: pair meta-prior certificate (and optional causal coupling proxy). -/
noncomputable axiom inferentialPairOf {n : Nat} :
  (Fin n → UADDiscoveredAgent) → Fin n → Fin n → InferentialPairProps

noncomputable def pairMaxSelfLoss {n : Nat} (agents : Fin n → UADDiscoveredAgent) (i j : Fin n) :
    Int :=
  max (inferentialProfileOf agents i).selfFixedPointLoss.val
    (inferentialProfileOf agents j).selfFixedPointLoss.val

/-- acausal-trade UAD paper eq. (8): `(1 - ε_ij)(1 - max{D_i, D_j})` on integer scale. -/
def inferentialCouplingScore (ε maxLoss : Int) : Int :=
  (inferentialCouplingScale - ε) * (inferentialCouplingScale - maxLoss) / inferentialCouplingScale

noncomputable def auditInferentialCouplingScore {n : Nat} (audit : UADDiscoveryAudit n)
    (i j : Fin n) : Int :=
  inferentialCouplingScore (metaPriorMismatch (inferentialPairOf audit.agents i j).metaPrior)
    (pairMaxSelfLoss audit.agents i j)

theorem auditInferentialCouplingScore_uses_derived_metaPriorMismatch
    {n : Nat} (audit : UADDiscoveryAudit n) (i j : Fin n) :
    auditInferentialCouplingScore audit i j =
      inferentialCouplingScore
        (metaPriorMismatch (inferentialPairOf audit.agents i j).metaPrior)
        (pairMaxSelfLoss audit.agents i j) := rfl

/-- The three explicit assumptions of the inferential detector, tied to the opaque
    audit outputs rather than hidden inside the score formula. -/
structure InferentialDetectionCertificate {n : Nat}
    (audit : UADDiscoveryAudit n) (i j : Fin n) : Prop where
  sharedMetaPrior : (inferentialPairOf audit.agents i j).metaPrior.permutationInvariant
  leftSelfReadout : (inferentialProfileOf audit.agents i).selfReadoutReliable
  rightSelfReadout : (inferentialProfileOf audit.agents j).selfReadoutReliable
  leftProbeCoverage : (inferentialProfileOf audit.agents i).probeCoverageAdequate
  rightProbeCoverage : (inferentialProfileOf audit.agents j).probeCoverageAdequate

theorem inferential_detection_certificate_assumptions
    {n : Nat} {audit : UADDiscoveryAudit n} {i j : Fin n}
    (cert : InferentialDetectionCertificate audit i j) :
    (inferentialPairOf audit.agents i j).metaPrior.permutationInvariant ∧
      (inferentialProfileOf audit.agents i).selfReadoutReliable ∧
      (inferentialProfileOf audit.agents j).selfReadoutReliable ∧
      (inferentialProfileOf audit.agents i).probeCoverageAdequate ∧
      (inferentialProfileOf audit.agents j).probeCoverageAdequate :=
  ⟨cert.sharedMetaPrior, cert.leftSelfReadout, cert.rightSelfReadout,
    cert.leftProbeCoverage, cert.rightProbeCoverage⟩

/-- Default detector threshold `τ_ac ≈ 0.9` on integer scale (paper §6.2). -/
def defaultInferentialThreshold : Int := 90

def inferentialEdgeOpen (score threshold : Int) : Prop :=
  threshold < score

/-! ## Assembling `\tilde{κ}` mutual-model props (ch33) -/

structure MutualModelProps where
  benefit : Int
  causalReach : Int
  inferentialReachBoost : Int
  correlation : Int
  cost : Int
  transparency : Int := 0

/-- ch33 effective reach: `p_ij + (1 - p_ij) · ICI_ij` on integer scale. -/
def MutualModelProps.effectiveReach (m : MutualModelProps) : Int :=
  m.causalReach + m.inferentialReachBoost

/-- Inferential boost `(1 - p) · ICI` on integer scale. -/
def inferentialReachBoostFromScore (p ic : Int) : Int :=
  (inferentialCouplingScale - p) * ic / inferentialCouplingScale

theorem inferentialReachBoost_at_zero_reach (ic : Int) :
    inferentialReachBoostFromScore 0 ic = ic := by
  unfold inferentialReachBoostFromScore inferentialCouplingScale
  omega

def assembleMutualModel (c : CausalMutualProps) (ic : Int) : MutualModelProps :=
  { benefit := c.benefit
    causalReach := c.causalReach
    inferentialReachBoost := inferentialReachBoostFromScore c.causalReach ic
    correlation := c.correlation
    cost := c.cost
    transparency := c.transparency }

/-- Full mutual-model record: causal inputs + inferential IC score derived from UAD. -/
noncomputable def auditMutualModelWithInferential {n : Nat} (audit : UADDiscoveryAudit n)
    (i j : Fin n) : MutualModelProps :=
  assembleMutualModel (causalMutualModelOf audit.agents i j)
    (auditInferentialCouplingScore audit i j)

theorem auditMutualModel_effectiveReach_eq_tilde_kappa {n : Nat}
    (audit : UADDiscoveryAudit n) (i j : Fin n) :
    let c := causalMutualModelOf audit.agents i j
    let ic := auditInferentialCouplingScore audit i j
    (auditMutualModelWithInferential audit i j).effectiveReach =
      c.causalReach + inferentialReachBoostFromScore c.causalReach ic := by
  unfold auditMutualModelWithInferential assembleMutualModel MutualModelProps.effectiveReach
  rfl

theorem severed_causal_reach_positive_effective_reach
    (c : CausalMutualProps) (ic : Int)
    (hp : c.causalReach = 0) (hic : 0 < ic) :
    0 < (assembleMutualModel c ic).effectiveReach := by
  dsimp [assembleMutualModel, MutualModelProps.effectiveReach, inferentialReachBoostFromScore,
    inferentialCouplingScale]
  rw [hp]
  omega

/-! ## Derived inferential detector graph -/

/-- Inferential detector graph from UAD audit (paper §6; alarm when IC > τ). -/
structure DerivedInferentialGraph (n : Nat) where
  audit : UADDiscoveryAudit n
  threshold : Int := defaultInferentialThreshold

def DerivedInferentialGraph.inferentialOpen {n : Nat} (G : DerivedInferentialGraph n)
    (i j : Fin n) : Prop :=
  inferentialEdgeOpen (auditInferentialCouplingScore G.audit i j) G.threshold

def deriveInferentialGraph {n : Nat} (audit : UADDiscoveryAudit n) :
    DerivedInferentialGraph n :=
  { audit := audit }

theorem uad_audit_yields_inferential_graph {n : Nat} (audit : UADDiscoveryAudit n) :
    ∃ G : DerivedInferentialGraph n, G.audit = audit :=
  ⟨deriveInferentialGraph audit, rfl⟩

theorem inferential_open_on_severed_edge_yields_reach
    {n : Nat} (audit : UADDiscoveryAudit n) (i j : Fin n)
    (hp : (causalMutualModelOf audit.agents i j).causalReach = 0)
    (hopen : (deriveInferentialGraph audit).inferentialOpen i j) :
    0 < (auditMutualModelWithInferential audit i j).effectiveReach := by
  have hic : 90 < auditInferentialCouplingScore audit i j := by
    unfold DerivedInferentialGraph.inferentialOpen deriveInferentialGraph inferentialEdgeOpen
      defaultInferentialThreshold at hopen
    exact hopen
  unfold auditMutualModelWithInferential
  exact severed_causal_reach_positive_effective_reach _ _ hp (by omega)

/-! ## Derived cooperation graph (`\tilde{κ}` / κ threshold) -/

def kappaEdgeOpen (m : MutualModelProps) : Prop :=
  KappaAboveUnity m.benefit m.effectiveReach m.correlation m.cost

theorem kappaEdgeOpen_iff_P32 (m : MutualModelProps) (hc : 0 < m.cost) :
    kappaEdgeOpen m ↔
      KappaNumerator m.benefit m.effectiveReach m.correlation > m.cost := by
  unfold kappaEdgeOpen KappaAboveUnity KappaNumerator MutualModelProps.effectiveReach
  rw [P32_kappa_threshold m.benefit (m.causalReach + m.inferentialReachBoost) m.correlation m.cost hc]
  constructor
  · intro ⟨_, hlt⟩
    exact hlt
  · intro hgt
    exact ⟨hc, hgt⟩

/-- Cooperation graph derived from UAD + causal + inferential modeling. -/
structure DerivedCoopGraph (n : Nat) where
  audit : UADDiscoveryAudit n

def DerivedCoopGraph.openEdge {n : Nat} (G : DerivedCoopGraph n) (i j : Fin n) :
    Prop :=
  kappaEdgeOpen (auditMutualModelWithInferential G.audit i j)

def deriveCoopGraph {n : Nat} (audit : UADDiscoveryAudit n) : DerivedCoopGraph n :=
  ⟨audit⟩

theorem deriveCoopGraph_audit {n : Nat} (audit : UADDiscoveryAudit n) :
    (deriveCoopGraph audit).audit = audit := rfl

theorem uad_audit_yields_cooperation_graph {n : Nat} (audit : UADDiscoveryAudit n) :
    ∃ G : DerivedCoopGraph n, G.audit = audit :=
  ⟨deriveCoopGraph audit, rfl⟩

theorem derived_openEdge_iff_kappa {n : Nat} (G : DerivedCoopGraph n) (i j : Fin n) :
    G.openEdge i j ↔
      kappaEdgeOpen (auditMutualModelWithInferential G.audit i j) :=
  Iff.rfl

theorem derived_openEdge_via_P32 {n : Nat} (G : DerivedCoopGraph n) (i j : Fin n)
    (hc : 0 < (auditMutualModelWithInferential G.audit i j).cost) :
    G.openEdge i j ↔
      KappaNumerator (auditMutualModelWithInferential G.audit i j).benefit
        (auditMutualModelWithInferential G.audit i j).effectiveReach
        (auditMutualModelWithInferential G.audit i j).correlation >
        (auditMutualModelWithInferential G.audit i j).cost := by
  let m := auditMutualModelWithInferential G.audit i j
  have hm : kappaEdgeOpen m ↔
      KappaNumerator m.benefit m.effectiveReach m.correlation > m.cost :=
    kappaEdgeOpen_iff_P32 m hc
  simpa [DerivedCoopGraph.openEdge, m] using hm

/-! ## Generic cooperation graphs (P33) -/

structure CooperationGraph (V : Type) where
  Open : V → V → Prop

def CooperationGraph.componentLarge {V : Type} (G : CooperationGraph V) : Prop :=
  ∃ i j, G.Open i j

def DerivedCoopGraph.toCooperationGraph {n : Nat} (G : DerivedCoopGraph n) :
    CooperationGraph (Fin n) :=
  { Open := G.openEdge }

def DerivedInferentialGraph.toCooperationGraph {n : Nat} (G : DerivedInferentialGraph n) :
    CooperationGraph (Fin n) :=
  { Open := G.inferentialOpen }

theorem P33_no_open_edges_no_large_component {V : Type}
    (G : CooperationGraph V) (hclosed : ∀ i j, ¬ G.Open i j) :
    ¬ G.componentLarge := by
  rintro ⟨i, j, hopen⟩
  exact hclosed i j hopen

theorem derived_P33_no_large_component {n : Nat} (G : DerivedCoopGraph n)
    (hclosed : ∀ i j, ¬ G.openEdge i j) :
    ¬ G.toCooperationGraph.componentLarge :=
  P33_no_open_edges_no_large_component G.toCooperationGraph hclosed

theorem derived_inferential_P33_no_large_component {n : Nat} (G : DerivedInferentialGraph n)
    (hclosed : ∀ i j, ¬ G.inferentialOpen i j) :
    ¬ G.toCooperationGraph.componentLarge :=
  P33_no_open_edges_no_large_component G.toCooperationGraph hclosed

def derived_graph_is_cooperation_graph {n : Nat} (audit : UADDiscoveryAudit n) :
    CooperationGraph (Fin n) :=
  (deriveCoopGraph audit).toCooperationGraph

def derived_inferential_graph_is_cooperation_graph {n : Nat} (audit : UADDiscoveryAudit n) :
    CooperationGraph (Fin n) :=
  (deriveInferentialGraph audit).toCooperationGraph

end AlignmentProofSpine
