import AlignmentProofSpine.FrameRelations

/-!
# AlignmentProofSpine.FrameMorphisms

**Carriers and maps** for specialize / project / encode edges in graphs **a** and **b**
(`drafts/alignment-frames-relations.dot`, `-b.dot`). Each entry names:

* source and target inventory nodes (`FrameNodeExt`);
* semantic **carriers** (what is being mapped);
* a stable **`mapId`** for the function or forgetful map;
* optional **equivalence** / **hypothesis** tags (when the diagram commutes only up to a named ambiguity).

This is vocabulary for a future commuting-diagram check, not a complete functor formalization.
-/

namespace AlignmentProofSpine

namespace FrameRelations

/-! ### Graph **a** / **b** nodes (superset of variant **c**) -/

inductive FrameNodeExt where
  | hist
  | route
  | exact
  | cycle
  | state
  | dist
  | criteria_vector
  | weighted_scalar
  | lex
  | quant
  | approval
  | au_penalty
  | au_floor
  | ai_power
  | human_power
  | corrig
  | correction
  | cev
  | deontic
  | coord_floor
  | cci_cert
  | risk_leaf
  | preserve_tuple
  | viable
  | robust
  | selection
  | proof
  | control
  | safecase
  deriving DecidableEq, Repr, Inhabited

def FrameNodeExt.ofC : FrameNode → FrameNodeExt
  | .route => .route | .exact => .exact | .cycle => .cycle | .state => .state
  | .weighted_scalar => .weighted_scalar | .criteria_vector => .criteria_vector
  | .au_penalty => .au_penalty | .au_floor => .au_floor
  | .ai_power => .ai_power | .human_power => .human_power | .correction => .correction
  | .deontic => .deontic | .cci_cert => .cci_cert | .preserve_tuple => .preserve_tuple
  | .viable => .viable | .robust => .robust | .selection => .selection
  | .proof => .proof | .control => .control | .approval => .approval | .safecase => .safecase

/-! ### Carriers (mathematical loci before assessment is applied) -/

inductive CarrierTag where
  | bareState
  | augmentedStateHistory
  | augmentedStateRouteBits
  | augmentedStateProcedureOutput
  | digraphPath
  | edgeReward
  | edgeRewardExactSummand
  | edgeRewardCycleSummand
  | outcomeLottery
  | criteriaVector
  | lexPriority
  | quantileBasePolicy
  | singleActWithJudge
  | humanAULandscape
  | agentEmpowermentChannel
  | humanPowerAggregate
  | correctionRelation
  | corrigibilityHandles
  | openProcedure
  | deonticActSet
  | coordinateFloorGate
  | cciVector
  | scalarRiskGap
  | deploymentPreserveTuple
  | controlledDynamicsWithSet
  | selectionPopulation
  | formalModel
  | deploymentUnderThreat
  | deploymentClaim
  deriving DecidableEq, Repr, Inhabited

def carrierOf : FrameNodeExt → CarrierTag
  | .hist => .digraphPath
  | .route => .edgeReward
  | .exact => .edgeRewardExactSummand
  | .cycle => .edgeRewardCycleSummand
  | .state => .bareState
  | .dist => .outcomeLottery
  | .criteria_vector => .criteriaVector
  | .weighted_scalar => .criteriaVector
  | .lex => .lexPriority
  | .quant => .quantileBasePolicy
  | .approval => .singleActWithJudge
  | .au_penalty => .humanAULandscape
  | .au_floor => .humanAULandscape
  | .ai_power => .agentEmpowermentChannel
  | .human_power => .humanPowerAggregate
  | .corrig => .corrigibilityHandles
  | .correction => .correctionRelation
  | .cev => .openProcedure
  | .deontic => .deonticActSet
  | .coord_floor => .coordinateFloorGate
  | .cci_cert => .cciVector
  | .risk_leaf => .scalarRiskGap
  | .preserve_tuple => .deploymentPreserveTuple
  | .viable => .controlledDynamicsWithSet
  | .robust => .controlledDynamicsWithSet
  | .selection => .selectionPopulation
  | .proof => .formalModel
  | .control => .deploymentUnderThreat
  | .safecase => .deploymentClaim

/-! ### Morphism registry (specialize · project · encode) -/

inductive MorphismKind where
  | specialize
  | project
  | encode
  deriving DecidableEq, Repr

inductive EquivalenceNote where
  | additiveConstantOnStateUtility
  | affineAmbiguityRouteVsState
  | noSectionAfterForget
  | observabilityRequired
  | weightsMustBeFixed
  | strictLexPriority
  | singleHandleNamedOperators
  | procedureOutputOnlyDropsRevisability
  | fixedAuditProtocol
  deriving DecidableEq, Repr

structure MorphismSpec where
  src : FrameNodeExt
  tgt : FrameNodeExt
  kind : MorphismKind
  srcCarrier : CarrierTag
  tgtCarrier : CarrierTag
  mapId : String
  note : Option EquivalenceNote
  deriving DecidableEq, Repr

/-- Stable map keys and carrier typing for graph **a** specialize / project / encode. -/
def morphismRegistryA : List MorphismSpec :=
  -- specialize (narrow → general in DOT direction)
  [ { src := .exact, tgt := .route, kind := .specialize,
      srcCarrier := .edgeRewardExactSummand, tgtCarrier := .edgeReward,
      mapId := "subspace.inclusion.exactPotential", note := Option.none }
  , { src := .approval, tgt := .route, kind := .specialize,
      srcCarrier := .singleActWithJudge, tgtCarrier := .edgeReward,
      mapId := "restrict.oneEdgeOneJudge", note := Option.none }
  , { src := .weighted_scalar, tgt := .criteria_vector, kind := .specialize,
      srcCarrier := .criteriaVector, tgtCarrier := .criteriaVector,
      mapId := "scalarize.fixedWeights", note := some .weightsMustBeFixed }
  , { src := .lex, tgt := .criteria_vector, kind := .specialize,
      srcCarrier := .lexPriority, tgtCarrier := .criteriaVector,
      mapId := "prioritize.lexOrder", note := some .strictLexPriority }
  , { src := .corrig, tgt := .correction, kind := .specialize,
      srcCarrier := .corrigibilityHandles, tgtCarrier := .correctionRelation,
      mapId := "restrict.oneHandleNamedOperators", note := some .singleHandleNamedOperators }
  , { src := .state, tgt := .route, kind := .specialize,
      srcCarrier := .bareState, tgtCarrier := .edgeReward,
      mapId := "induceGradient.exactPotential",
      note := some .additiveConstantOnStateUtility }
  -- project
  , { src := .dist, tgt := .state, kind := .project,
      srcCarrier := .outcomeLottery, tgtCarrier := .bareState,
      mapId := "expectationFunctional", note := some .noSectionAfterForget }
  , { src := .criteria_vector, tgt := .weighted_scalar, kind := .project,
      srcCarrier := .criteriaVector, tgtCarrier := .criteriaVector,
      mapId := "forget.chosenWeights", note := some .noSectionAfterForget }
  , { src := .correction, tgt := .corrig, kind := .project,
      srcCarrier := .correctionRelation, tgtCarrier := .corrigibilityHandles,
      mapId := "forget.shutdownBit", note := some .noSectionAfterForget }
  , { src := .route, tgt := .cycle, kind := .project,
      srcCarrier := .edgeReward, tgtCarrier := .edgeRewardCycleSummand,
      mapId := "longRunAverage.retainCycleSummand", note := Option.none }
  -- encode
  , { src := .hist, tgt := .state, kind := .encode,
      srcCarrier := .digraphPath, tgtCarrier := .augmentedStateHistory,
      mapId := "appendHistoryToState", note := some .observabilityRequired }
  , { src := .route, tgt := .state, kind := .encode,
      srcCarrier := .edgeReward, tgtCarrier := .augmentedStateRouteBits,
      mapId := "embedRouteBitsInState", note := some .observabilityRequired }
  , { src := .cev, tgt := .state, kind := .encode,
      srcCarrier := .openProcedure, tgtCarrier := .augmentedStateProcedureOutput,
      mapId := "scoreProcedureByOutputOnly", note := some .procedureOutputOnlyDropsRevisability } ]

/-- Variant **b** adds projection / specialization on certification geometry. -/
def morphismRegistryBExtra : List MorphismSpec :=
  [ { src := .cci_cert, tgt := .coord_floor, kind := .specialize,
      srcCarrier := .cciVector, tgtCarrier := .coordinateFloorGate,
      mapId := "restrict.cciCoordinateFloors", note := Option.none }
  , { src := .correction, tgt := .cci_cert, kind := .project,
      srcCarrier := .correctionRelation, tgtCarrier := .cciVector,
      mapId := "auditProfileUnderFixedProtocol", note := some .fixedAuditProtocol }
  , { src := .preserve_tuple, tgt := .cci_cert, kind := .project,
      srcCarrier := .deploymentPreserveTuple, tgtCarrier := .cciVector,
      mapId := "project.deploymentSubVector", note := Option.none }
  , { src := .cci_cert, tgt := .risk_leaf, kind := .project,
      srcCarrier := .cciVector, tgtCarrier := .scalarRiskGap,
      mapId := "scalarRiskGapAfterVectorGate", note := Option.none } ]

def morphismRegistryAB : List MorphismSpec :=
  morphismRegistryA ++ morphismRegistryBExtra

def morphismKindDeriv (src tgt : FrameNodeExt) : Option MorphismKind :=
  (morphismRegistryAB.find? fun m => m.src == src && m.tgt == tgt).map (·.kind)

structure MorphismEdge where
  src : FrameNodeExt
  tgt : FrameNodeExt
  kind : MorphismKind
  deriving DecidableEq, Repr

def graphAMorphismEdges : List MorphismEdge :=
  morphismRegistryA.map fun m => { src := m.src, tgt := m.tgt, kind := m.kind }

def graphBMorphismEdges : List MorphismEdge :=
  morphismRegistryAB.map fun m => { src := m.src, tgt := m.tgt, kind := m.kind }

def morphismEdgeOk (e : MorphismEdge) : Bool :=
  morphismKindDeriv e.src e.tgt == some e.kind

theorem graphA_morphisms_typed : graphAMorphismEdges.all morphismEdgeOk = true := by
  native_decide

theorem graphB_morphisms_typed : graphBMorphismEdges.all morphismEdgeOk = true := by
  native_decide

/-! ### Typed map signatures (documentation hooks; not full defs) -/

/-- Intended domain/codomain shape for `mapId` keys (informal `Type` names as strings). -/
structure MapSignature where
  mapId : String
  domain : String
  codomain : String
  deriving Repr

def mapSignatures : List MapSignature :=
  [ { mapId := "induceGradient.exactPotential",
      domain := "State → ℤ", codomain := "Edge → ℤ" }
  , { mapId := "subspace.inclusion.exactPotential",
      domain := "{r exact potential}", codomain := "{r additive}" }
  , { mapId := "expectationFunctional",
      domain := "Δ(State)", codomain := "State → ℝ" }
  , { mapId := "forget.chosenWeights",
      domain := "ℝⁿ × Weights", codomain := "ℝ" }
  , { mapId := "forget.shutdownBit",
      domain := "CorrectionRelation", codomain := "Bool handle" }
  , { mapId := "longRunAverage.retainCycleSummand",
      domain := "Edge → ℤ", codomain := "Cycle summand" }
  , { mapId := "appendHistoryToState",
      domain := "Path", codomain := "State × History" }
  , { mapId := "embedRouteBitsInState",
      domain := "Edge → ℤ", codomain := "State × RouteObs" }
  , { mapId := "scoreProcedureByOutputOnly",
      domain := "OpenProcedure", codomain := "State → Score" }
  , { mapId := "auditProfileUnderFixedProtocol",
      domain := "CorrectionRelation", codomain := "CCI vector" }
  , { mapId := "scalarRiskGapAfterVectorGate",
      domain := "CCI vector (passed)", codomain := "control ≤ CCI + δ" } ]

def mapSignature? (id : String) : Option MapSignature :=
  mapSignatures.find? (·.mapId == id)

end FrameRelations

end AlignmentProofSpine
