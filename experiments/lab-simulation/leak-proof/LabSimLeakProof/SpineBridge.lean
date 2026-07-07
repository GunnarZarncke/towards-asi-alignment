import LabSimLeakProof.Leakage
import LabSimLeakProof.Projections
import LabSimLeakProof.Theorems
import LabSimLeakProof.Keys

/-!
# Spine bridge — local mirror of `AlignmentProofSpine.Core.ExactBoundary`

Maps lab-simulation leakage counts to the book spine's boundary certificate
vocabulary without requiring a path dependency on `formal/`.
-/

namespace LabSimLeakProof

/-- Integer leakage proxy aligned with `AlignmentProofSpine.Core.Boundary.leakage`. -/
structure PlaneBoundary where
  oracleIntoAudit : Int
  oracleSecretIntoSim : Int
  auditIntoSim : Int
  deriving Repr

def PlaneBoundary.ofCounts (c : LeakCounts) : PlaneBoundary :=
  { oracleIntoAudit := c.oracleIntoAudit
    oracleSecretIntoSim := c.oracleSecretIntoSim
    auditIntoSim := c.auditIntoSim }

def PlaneBoundary.totalLeakage (b : PlaneBoundary) : Int :=
  b.oracleIntoAudit + b.oracleSecretIntoSim + b.auditIntoSim

/-- C-EPS-style exact plane boundary: zero unintended cross-plane keys. -/
def ExactPlaneBoundary (b : PlaneBoundary) : Prop :=
  b.oracleIntoAudit ≤ 0 ∧ b.oracleSecretIntoSim ≤ 0 ∧ b.auditIntoSim ≤ 0

theorem LeakProofCertificate.exact_plane_boundary (cert : LeakProofCertificate) :
    ExactPlaneBoundary (PlaneBoundary.ofCounts cert.counts) := by
  rcases cert.hexact with ⟨h1, h2, h3⟩
  simp [ExactPlaneBoundary, PlaneBoundary.ofCounts, h1, h2, h3, Int.ofNat_zero]

theorem certified_episode_exact_boundary (tier : Tier) (ep : RawEpisode) :
    ExactPlaneBoundary (PlaneBoundary.ofCounts (certified_episode tier ep).counts) :=
  (certified_episode tier ep).exact_plane_boundary

end LabSimLeakProof
