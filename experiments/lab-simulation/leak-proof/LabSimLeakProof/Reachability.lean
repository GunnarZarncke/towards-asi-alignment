import LabSimLeakProof.Keys
import LabSimLeakProof.Tiers
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# Reachability analysis — Python call graph as information flow

Each `PyTransfer` names a Python function (or wire channel); each `FlowEdge`
records which field keys may cross from source medium to destination medium.
Reachability is computed by fixpoint BFS over `(InfoRegion × FieldKey)` pairs.

This abstracts the entire lab-simulation exchange graph: oracle internals,
three hash-chained logs, workspace/comms stores, tier projections, deep fetches,
observation builder, and isolate wire.
-/

namespace LabSimLeakProof

open FieldKey Tier

/-- Information store / exchange medium in lab-simulation. -/
inductive InfoRegion
  | oracle
  | engineLog
  | accessLog
  | toolEvents
  | workspace
  | commsStore
  | memoIndex
  | hostInternal
  | auditView
  | simObservation
  | toolResult
  deriving DecidableEq, Repr

/-- Python functions and wire channels, abstracted to information transfer. -/
inductive PyTransfer
  | oracleSampleModel
  | pipelineTriggerStep
  | pipelineEffectReport
  | permissionGrant
  | permissionCheck
  | hostDispatchLog
  | hostDispatchResult
  | commsPost
  | commsRead
  | fileWrite
  | fileShare
  | fileRead
  | stateSaveLoad
  | eventsProjectEngine
  | eventsProjectAccess
  | eventsProjectToolEvents
  | detectorsBuildAuditView
  | detectorsDeepReportFetch
  | detectorsDeepSpecFetch
  | detectorsDeepMessageFetch
  | detectorsDeepMemoFetch
  | worldBuildObservation
  | isolateStep
  | llmObservationPayload
  | playbookSelectionLog
  deriving DecidableEq, Repr

structure FlowEdge where
  transfer : PyTransfer
  src : InfoRegion
  dst : InfoRegion
  allowed : Finset FieldKey

def mkFlow (transfer : PyTransfer) (src dst : InfoRegion) (allowed : Finset FieldKey) : FlowEdge :=
  { transfer, src, dst, allowed }

/-- Keys that may leave the oracle store (measured values only — no ground truth). -/
def oracleToEngineAllowed : Finset FieldKey :=
  engineLogAllowedKeys .full \ oracleOnlyKeys

/-- Tool-event keys after comm/memo content elision at logging time. -/
def loggedToolKeys : Finset FieldKey :=
  toolEventAllowedKeys .full \ commContentKeys

/-- Full catalog of exchange edges in lab-simulation (see module docstrings in Python). -/
def flowCatalog : List FlowEdge :=
  let e := mkFlow
  [
    e .oracleSampleModel .oracle .oracle oracleOnlyKeys,
    e .pipelineTriggerStep .oracle .engineLog oracleToEngineAllowed,
    e .pipelineEffectReport .oracle .workspace { content, report_contents, rel, name },
    e .permissionGrant .hostInternal .accessLog (accessLogAllowedKeys .full),
    e .permissionCheck .accessLog .accessLog (accessLogAllowedKeys .full),
    e .hostDispatchLog .hostInternal .toolEvents loggedToolKeys,
    e .hostDispatchResult .hostInternal .toolResult simObservationAllowedKeys,
    e .playbookSelectionLog .simObservation .toolEvents (toolEventAllowedFor .full .playbookSelection),
    e .commsPost .simObservation .commsStore (deepMessageAllowedKeys ∪ commContentKeys),
    e .commsPost .simObservation .toolEvents loggedToolKeys,
    e .commsRead .commsStore .toolResult (deepMessageAllowedKeys ∪ commContentKeys),
    e .fileWrite .simObservation .workspace { content, rel, name },
    e .fileWrite .simObservation .memoIndex { rel, actor_id, name, t },
    e .fileShare .memoIndex .accessLog (accessLogAllowedKeys .full),
    e .fileRead .workspace .toolResult { content, rel, name },
    e .stateSaveLoad .hostInternal .hostInternal { content },
    e .stateSaveLoad .hostInternal .toolResult { content },
    e .eventsProjectEngine .engineLog .auditView (engineLogAllowedKeys .full),
    e .eventsProjectAccess .accessLog .auditView (accessLogAllowedKeys .full),
    e .eventsProjectToolEvents .toolEvents .auditView (toolEventAllowedKeys .full),
    e .detectorsBuildAuditView .auditView .auditView (
        engineLogAllowedKeys .full ∪ accessLogAllowedKeys .full ∪ toolEventAllowedKeys .full),
    e .detectorsDeepReportFetch .workspace .auditView deepReportAllowedKeys,
    e .detectorsDeepSpecFetch .engineLog .auditView deepSpecAllowedKeys,
    e .detectorsDeepMessageFetch .commsStore .auditView deepMessageAllowedKeys,
    e .detectorsDeepMemoFetch .memoIndex .auditView deepMemoAllowedKeys,
    e .worldBuildObservation .engineLog .simObservation simObservationAllowedKeys,
    e .worldBuildObservation .commsStore .simObservation simObservationAllowedKeys,
    e .worldBuildObservation .workspace .simObservation simObservationAllowedKeys,
    e .worldBuildObservation .hostInternal .simObservation simObservationAllowedKeys,
    e .isolateStep .simObservation .simObservation simObservationAllowedKeys,
    e .llmObservationPayload .simObservation .simObservation simObservationAllowedKeys
  ]

abbrev ReachState := Finset (InfoRegion × FieldKey)

def FlowEdge.carries (edge : FlowEdge) (r : InfoRegion) (k : FieldKey) : ReachState :=
  if k ∈ edge.allowed && r = edge.src then {(edge.dst, k)} else ∅

def stepReach (frontier : ReachState) (edges : List FlowEdge) : ReachState :=
  frontier.biUnion fun ⟨r, k⟩ =>
    edges.foldl (fun acc e => acc ∪ e.carries r k) ∅

def maxReachSteps : Nat := 128

def reachabilityFixpoint (sources : ReachState) (edges : List FlowEdge) : ReachState :=
  (List.range maxReachSteps).foldl (fun acc _ => stepReach acc edges) sources

def regionReachable (sources : ReachState) (edges : List FlowEdge) (target : InfoRegion) :
    Finset FieldKey :=
  (reachabilityFixpoint sources edges).biUnion fun ⟨r, k⟩ =>
    if r = target then {k} else ∅

def oracleSeed : ReachState :=
  oracleOnlyKeys.image fun k => (.oracle, k)

def auditSeed : ReachState :=
  auditSurfaceKeys.image fun k => (.auditView, k)

def oracleReachSim : Finset FieldKey :=
  regionReachable oracleSeed flowCatalog .simObservation

def oracleReachAudit : Finset FieldKey :=
  regionReachable oracleSeed flowCatalog .auditView

def auditReachSim : Finset FieldKey :=
  regionReachable auditSeed flowCatalog .simObservation

theorem flowCatalog_oracleEngine_disjoint :
    Disjoint oracleToEngineAllowed oracleOnlyKeys := by native_decide

theorem flowCatalog_loggedTool_disjoint :
    Disjoint loggedToolKeys oracleOnlyKeys := by native_decide

theorem reachability_oracleSecrets_not_at_sim :
    (oracleReachSim ∩ oracleSecretKeys).card = 0 := by native_decide

theorem reachability_oracleOnly_not_at_audit :
    (oracleReachAudit ∩ oracleOnlyKeys).card = 0 := by native_decide

theorem reachability_auditSurface_not_at_sim :
    (auditReachSim ∩ auditSurfaceKeys).card = 0 := by native_decide

def ReachabilityCertificate : Prop :=
  (oracleReachSim ∩ oracleSecretKeys).card = 0 ∧
  (oracleReachAudit ∩ oracleOnlyKeys).card = 0 ∧
  (auditReachSim ∩ auditSurfaceKeys).card = 0

theorem reachability_certificate : ReachabilityCertificate := by
  refine ⟨reachability_oracleSecrets_not_at_sim, reachability_oracleOnly_not_at_audit, ?_⟩
  exact reachability_auditSurface_not_at_sim

end LabSimLeakProof
