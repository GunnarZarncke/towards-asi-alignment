import LabSimLeakProof.Keys
import LabSimLeakProof.Projections
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card

/-!
# Leakage counts — cardinality proxy for unintended key presence

Matches the `Boundary.leakage` idiom in `AlignmentProofSpine.Core`: count of
forbidden keys present in a projected artifact.
-/

namespace LabSimLeakProof

open FieldKey

def oracleLeakageCount (keys : Finset FieldKey) : Nat :=
  (keys ∩ oracleOnlyKeys).card

def oracleSecretSimLeakageCount (keys : Finset FieldKey) : Nat :=
  (keys ∩ oracleSecretKeys).card

def auditToSimLeakageCount (keys : Finset FieldKey) : Nat :=
  (keys ∩ auditSurfaceKeys).card

structure LeakCounts where
  oracleIntoAudit : Nat
  oracleSecretIntoSim : Nat
  auditIntoSim : Nat
  deriving Repr

def leakageOf (view : AuditView) (sim : SimObservation) : LeakCounts :=
  { oracleIntoAudit := oracleLeakageCount view.allKeys
    oracleSecretIntoSim := oracleSecretSimLeakageCount sim
    auditIntoSim := auditToSimLeakageCount sim }

def LeakCounts.exact (c : LeakCounts) : Prop :=
  c.oracleIntoAudit = 0 ∧ c.oracleSecretIntoSim = 0 ∧ c.auditIntoSim = 0

structure LeakProofCertificate where
  view : AuditView
  sim : SimObservation
  counts : LeakCounts
  hexact : counts.exact

end LabSimLeakProof
