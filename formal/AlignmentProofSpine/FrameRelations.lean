import AlignmentProofSpine.Mathlib

/-!
# AlignmentProofSpine.FrameRelations

Typed **alignment-frame interfaces** and **derivation rules** for the relations
graph (draft `alignment-frames-relations*.dot`). Goal: edges in variant **c**
should be *obligations* of a small formal signature, not ad hoc DOT annotations.

## What is derivable from structure

| Edge kind in variant **c** | Derivation source |
| --- | --- |
| **Summand** (`route` ↔ `exact` / `cycle`) | `summandPair` on nodes (registry). One direction is proved: `FrameIncompatibility.gradient_closed_walk_zero` (an exact part sums to zero on every closed walk). No general direct-sum decomposition yet. |
| **Incompatible** | `incompatWitnesses` registry; each entry carries an `Incompatibility` instance in `FrameIncompatibility.provedIncompat` (`registry_matches_proofs`). |
| **Compose** | Lookup table `CorrectionCentered.compose` (`ComposeSlot`). Roles in `interfaceOf` label nodes; they do not constrain compose. |

`variantC_all_derived` checks that the three tables do not shadow each other
under the classifier's priority (summand, then incompatible, then compose). It
does not derive edges from interface types. Agreement with
`drafts/alignment-frames-relations-c.dot` is checked outside Lean by
`scripts/check_frame_graph.py`.

Variant **c** is **not** the full compose-closure of interface types. See
`drafts/alignment-frames-relations.md` (*Formal layer (Lean)*).
-/

namespace AlignmentProofSpine

namespace FrameRelations

/-! ### Compact interface (inventory hook) -/

inductive Role where
  | target
  | constraint
  | guarantee
  | protocol
  deriving DecidableEq, Repr, Inhabited

inductive ObjectKind where
  | route
  | routeExact
  | routeCycle
  | state
  | criteriaVector
  | humanAULandscape
  | humanPowerChannel
  | agentPowerChannel
  | correctionRelation
  | deonticAdmissibility
  | correctionCertificate
  | deploymentVector
  | dynamicsSet
  | selectionPopulation
  | formalModelSpec
  | deploymentUnderThreat
  | deploymentClaim
  | singleAct
  deriving DecidableEq, Repr, Inhabited

inductive AssessmentKind where
  | additivePathScore
  | exactPotential
  | cycleResidue
  | scalarOrder
  | fixedWeightScalarMax
  | multiObjectiveOrder
  | optionPenalty
  | onOffFloor
  | aggregateCapacityOrder
  | empowermentFunctional
  | relationAndChannelProfile
  | forbidCompensatoryTrade
  | vectorCCIThreshold
  | tuplePreservation
  | existsControlInSet
  | forallDisturbanceInSet
  | invasionResistance
  | proofRelativeToModel
  | monitorProtocol
  | localApproval
  | safetyArgument
  deriving DecidableEq, Repr, Inhabited

structure Interface where
  role : Role
  object : ObjectKind
  assessment : AssessmentKind
  deriving DecidableEq, Repr

/-! ### Variant **c** nodes (DOT ids) -/

inductive FrameNode where
  | route
  | exact
  | cycle
  | state
  | weighted_scalar
  | criteria_vector
  | au_penalty
  | au_floor
  | ai_power
  | human_power
  | correction
  | deontic
  | cci_cert
  | preserve_tuple
  | viable
  | robust
  | selection
  | proof
  | control
  | approval
  | safecase
  deriving DecidableEq, Repr, Inhabited

def interfaceOf : FrameNode → Interface
  | .route => { role := .target, object := .route, assessment := .additivePathScore }
  | .exact => { role := .target, object := .routeExact, assessment := .exactPotential }
  | .cycle => { role := .target, object := .routeCycle, assessment := .cycleResidue }
  | .state => { role := .target, object := .state, assessment := .scalarOrder }
  | .weighted_scalar => { role := .target, object := .criteriaVector, assessment := .fixedWeightScalarMax }
  | .criteria_vector => { role := .target, object := .criteriaVector, assessment := .multiObjectiveOrder }
  | .au_penalty => { role := .constraint, object := .humanAULandscape, assessment := .optionPenalty }
  | .au_floor => { role := .constraint, object := .humanAULandscape, assessment := .onOffFloor }
  | .ai_power => { role := .target, object := .agentPowerChannel, assessment := .empowermentFunctional }
  | .human_power => { role := .target, object := .humanPowerChannel, assessment := .aggregateCapacityOrder }
  | .correction => { role := .target, object := .correctionRelation, assessment := .relationAndChannelProfile }
  | .deontic => { role := .constraint, object := .deonticAdmissibility, assessment := .forbidCompensatoryTrade }
  | .cci_cert => { role := .constraint, object := .correctionCertificate, assessment := .vectorCCIThreshold }
  | .preserve_tuple => { role := .constraint, object := .deploymentVector, assessment := .tuplePreservation }
  | .viable => { role := .guarantee, object := .dynamicsSet, assessment := .existsControlInSet }
  | .robust => { role := .guarantee, object := .dynamicsSet, assessment := .forallDisturbanceInSet }
  | .selection => { role := .guarantee, object := .selectionPopulation, assessment := .invasionResistance }
  | .proof => { role := .protocol, object := .formalModelSpec, assessment := .proofRelativeToModel }
  | .control => { role := .protocol, object := .deploymentUnderThreat, assessment := .monitorProtocol }
  | .approval => { role := .protocol, object := .singleAct, assessment := .localApproval }
  | .safecase => { role := .protocol, object := .deploymentClaim, assessment := .safetyArgument }

inductive EdgeKind where
  | summand
  | compose
  | incompatible
  deriving DecidableEq, Repr

structure FrameEdge where
  src : FrameNode
  tgt : FrameNode
  kind : EdgeKind
  deriving DecidableEq, Repr

/-! ### Summands (inventory nodes ↔ graph decomposition) -/

def summandPair (a b : FrameNode) : Bool :=
  (a == .exact && b == .route) || (a == .route && b == .exact) ||
  (a == .cycle && b == .route) || (a == .route && b == .cycle)

/-! ### Incompatibility registry -/

/-- Red-edge registry. `FrameIncompatibility.provedIncompat` pairs each entry
    with its `Incompatibility` instance; `registry_matches_proofs` checks the
    pairs line up. The shared carrier lives there, not here. -/
structure IncompatWitness where
  src : FrameNode
  tgt : FrameNode
  reason : String
  deriving Repr

def incompatWitnesses : List IncompatWitness :=
  [ { src := .state, tgt := .correction,
      reason := "fixed U rejects an endorsed update that lowers its chosen outcome" }
  , { src := .state, tgt := .cycle,
      reason := "gradient rewards sum to zero on every closed walk" }
  , { src := .deontic, tgt := .weighted_scalar,
      reason := "ban as floor coordinate vs finite-weight scalar" }
  , { src := .au_floor, tgt := .weighted_scalar,
      reason := "on-off floor on one goal vs finite-weight scalar" }
  , { src := .ai_power, tgt := .human_power,
      reason := "closed option pool: agent gain forces human loss" }
  , { src := .robust, tgt := .correction,
      reason := "corrections counted as disturbances cannot leave the invariant set" }
  , { src := .cci_cert, tgt := .weighted_scalar,
      reason := "CCI threshold as floor coordinate vs finite-weight scalar" }
  , { src := .criteria_vector, tgt := .cci_cert,
      reason := "scalarized vector vs CCI floor; Pareto alone does not entail the floor" } ]

def incompatibleDeriv (a b : FrameNode) : Bool :=
  incompatWitnesses.any fun w =>
    (w.src == a && w.tgt == b) || (w.src == b && w.tgt == a)

/-! ### Compose: correction-centered reading (variant **c** greens) -/

inductive ComposeSlot where
  | landscapeSoftToFloor
  | floorToHumanPower
  | humanPowerToCorrection
  | deonticToCorrection
  | deonticToCert
  | cycleResidueToCorrection
  | correctionToCert
  | correctionToViability
  | certToViability
  | preserveToViability
  | preserveToSelection
  | viabilityToSelection
  | proofToCert
  | controlToCert
  | approvalToCert
  | proofToSafecase
  | controlToSafecase
  | certToSafecase
  | correctionToSafecase
  deriving DecidableEq, Repr, Inhabited

def ComposeSlot.src : ComposeSlot → FrameNode
  | .landscapeSoftToFloor => .au_penalty
  | .floorToHumanPower => .au_floor
  | .humanPowerToCorrection => .human_power
  | .deonticToCorrection => .deontic
  | .deonticToCert => .deontic
  | .cycleResidueToCorrection => .cycle
  | .correctionToCert => .correction
  | .correctionToViability => .correction
  | .certToViability => .cci_cert
  | .preserveToViability => .preserve_tuple
  | .preserveToSelection => .preserve_tuple
  | .viabilityToSelection => .viable
  | .proofToCert => .proof
  | .controlToCert => .control
  | .approvalToCert => .approval
  | .proofToSafecase => .proof
  | .controlToSafecase => .control
  | .certToSafecase => .cci_cert
  | .correctionToSafecase => .correction

def ComposeSlot.tgt : ComposeSlot → FrameNode
  | .landscapeSoftToFloor => .au_floor
  | .floorToHumanPower => .human_power
  | .humanPowerToCorrection => .correction
  | .deonticToCorrection => .correction
  | .deonticToCert => .cci_cert
  | .cycleResidueToCorrection => .correction
  | .correctionToCert => .cci_cert
  | .correctionToViability => .viable
  | .certToViability => .viable
  | .preserveToViability => .viable
  | .preserveToSelection => .selection
  | .viabilityToSelection => .selection
  | .proofToCert => .cci_cert
  | .controlToCert => .cci_cert
  | .approvalToCert => .cci_cert
  | .proofToSafecase => .safecase
  | .controlToSafecase => .safecase
  | .certToSafecase => .safecase
  | .correctionToSafecase => .safecase

namespace CorrectionCentered

def allComposeSlots : List ComposeSlot :=
  [ .landscapeSoftToFloor, .floorToHumanPower, .humanPowerToCorrection,
    .deonticToCorrection, .deonticToCert, .cycleResidueToCorrection,
    .correctionToCert, .correctionToViability, .certToViability,
    .preserveToViability, .preserveToSelection, .viabilityToSelection,
    .proofToCert, .controlToCert, .approvalToCert, .proofToSafecase,
    .controlToSafecase, .certToSafecase, .correctionToSafecase ]

def compose (a b : FrameNode) : Bool :=
  allComposeSlots.any fun s => s.src == a && s.tgt == b

def composeProp (a b : FrameNode) : Prop := compose a b = true

def composeEdge (s : ComposeSlot) : FrameEdge :=
  { src := s.src, tgt := s.tgt, kind := .compose }

def allComposeEdges : List FrameEdge := allComposeSlots.map composeEdge

theorem compose_from_slot (s : ComposeSlot) : compose s.src s.tgt = true := by
  cases s <;> decide

end CorrectionCentered

/-! ### Derived edge classifier (variant **c**) -/

def derivedEdgeKind (a b : FrameNode) : Option EdgeKind :=
  if summandPair a b then some .summand
  else if incompatibleDeriv a b then some .incompatible
  else if CorrectionCentered.compose a b then some .compose
  else none

def variantCEdges : List FrameEdge :=
  let summands : List FrameEdge := [
    { src := .route, tgt := .exact, kind := .summand },
    { src := .exact, tgt := .route, kind := .summand },
    { src := .route, tgt := .cycle, kind := .summand },
    { src := .cycle, tgt := .route, kind := .summand } ]
  let composes := CorrectionCentered.allComposeEdges
  let conflicts : List FrameEdge := incompatWitnesses.flatMap fun w =>
    [ { src := w.src, tgt := w.tgt, kind := .incompatible },
      { src := w.tgt, tgt := w.src, kind := .incompatible } ]
  summands ++ composes ++ conflicts

def derivedEdgeKind? (e : FrameEdge) : Bool :=
  derivedEdgeKind e.src e.tgt == some e.kind

/-- The summand, incompatibility, and compose tables do not shadow one another
    under `derivedEdgeKind`'s priority order. -/
theorem variantC_all_derived : variantCEdges.all derivedEdgeKind? = true := by
  decide

end FrameRelations

end AlignmentProofSpine
