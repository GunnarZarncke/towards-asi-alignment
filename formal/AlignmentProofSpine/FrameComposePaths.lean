import AlignmentProofSpine.FrameRelations

/-!
# AlignmentProofSpine.FrameComposePaths

**Compose paths** for the correction-centered reading: slots group into parallel
tracks that meet at hub nodes (`correction`, `cci_cert`, `viable`, `safecase`).
-/

namespace AlignmentProofSpine

namespace FrameRelations

namespace CorrectionCentered

inductive ComposePathId where
  | landscapeHumanTarget
  | admissibleRegion
  | routeResidueInRegion
  | certificateOnRelation
  | certificateEvidence
  | guaranteeSuppliedSet
  | selectionEcology
  | warrantBundle
  deriving DecidableEq, Repr, Inhabited

def composeSlotPathId (s : ComposeSlot) : ComposePathId :=
  match s with
  | .landscapeSoftToFloor | .floorToHumanPower | .humanPowerToCorrection =>
      .landscapeHumanTarget
  | .deonticToCorrection => .admissibleRegion
  | .cycleResidueToCorrection => .routeResidueInRegion
  | .deonticToCert | .correctionToCert | .correctionToViability | .certToViability =>
      .certificateOnRelation
  | .proofToCert | .controlToCert | .approvalToCert => .certificateEvidence
  | .preserveToViability => .guaranteeSuppliedSet
  | .preserveToSelection | .viabilityToSelection => .selectionEcology
  | .proofToSafecase | .controlToSafecase | .certToSafecase | .correctionToSafecase =>
      .warrantBundle

def ComposePathId.label : ComposePathId → String
  | .landscapeHumanTarget => "Human AU landscape → power → correction"
  | .admissibleRegion => "Non-compensatory admissible region → correction"
  | .routeResidueInRegion => "Cycle / route residue inside region → correction"
  | .certificateOnRelation => "Coordinate floors, relation scored, viability of K"
  | .certificateEvidence => "Protocol leaves → CCI coordinates"
  | .guaranteeSuppliedSet => "Deployment tuple → supplied set K"
  | .selectionEcology => "Viability / deployment → selection stability"
  | .warrantBundle => "Safety case conjuncts and leaves"

def pathAllowedEdges (p : ComposePathId) : List (FrameNode × FrameNode) :=
  match p with
  | .landscapeHumanTarget =>
      [(.au_penalty, .au_floor), (.au_floor, .human_power), (.human_power, .correction)]
  | .admissibleRegion => [( .deontic, .correction)]
  | .routeResidueInRegion => [( .cycle, .correction)]
  | .certificateOnRelation =>
      [(.deontic, .cci_cert), (.correction, .cci_cert), (.correction, .viable), (.cci_cert, .viable)]
  | .certificateEvidence =>
      [(.proof, .cci_cert), (.control, .cci_cert), (.approval, .cci_cert)]
  | .guaranteeSuppliedSet => [( .preserve_tuple, .viable)]
  | .selectionEcology =>
      [(.preserve_tuple, .selection), (.viable, .selection)]
  | .warrantBundle =>
      [(.proof, .safecase), (.control, .safecase), (.cci_cert, .safecase), (.correction, .safecase)]

def pathSlots (p : ComposePathId) : List ComposeSlot :=
  allComposeSlots.filter fun s => composeSlotPathId s == p

def allPaths : List ComposePathId :=
  [ .landscapeHumanTarget, .admissibleRegion, .routeResidueInRegion,
    .certificateOnRelation, .certificateEvidence, .guaranteeSuppliedSet,
    .selectionEcology, .warrantBundle ]

def composeHubs : List FrameNode :=
  [.correction, .cci_cert, .viable, .safecase]

def slotOnPath (s : ComposeSlot) : Bool :=
  let p := composeSlotPathId s
  (s.src, s.tgt) ∈ pathAllowedEdges p

theorem slot_on_path (s : ComposeSlot) : slotOnPath s = true := by
  cases s <;> native_decide

theorem all_slots_on_paths : allComposeSlots.all slotOnPath = true := by
  native_decide

theorem paths_partition_slots :
    (allPaths.flatMap pathSlots).length = allComposeSlots.length := by
  native_decide

theorem slots_have_unique_path :
    allComposeSlots.all fun s =>
      (allPaths.filter fun p => composeSlotPathId s == p).length == 1 = true := by
  native_decide

end CorrectionCentered

end FrameRelations

end AlignmentProofSpine
