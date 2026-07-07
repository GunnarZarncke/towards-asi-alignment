import LabSimLeakProof.Keys
import LabSimLeakProof.Tiers
import Mathlib.Data.Finset.Basic

/-!
# Certified projections — `build_audit_view` / observation filter

Functions mirror `events.project_*`, `detectors.build_audit_view`, and the
observation key whitelist enforced in `world.py`.
-/

namespace LabSimLeakProof

open FieldKey Tier

def projectKeys (keys allowed : Finset FieldKey) : Finset FieldKey := keys ∩ allowed

def projectEngine (keys : Finset FieldKey) (tier : Tier) : Finset FieldKey :=
  projectKeys keys (engineLogAllowedKeys tier)

def projectAccess (keys : Finset FieldKey) (tier : Tier) : Finset FieldKey :=
  projectKeys keys (accessLogAllowedKeys tier)

def projectToolEvents (keys : Finset FieldKey) (tier : Tier) : Finset FieldKey :=
  projectKeys keys (toolEventAllowedKeys tier)

/-- Keys logged after `tools._scalar_args` comm/memo content elision. -/
def elideCommContentKeys (keys : Finset FieldKey) : Finset FieldKey :=
  keys \ commContentKeys

/-- Abstract episode artifact *before* plane separation (referee-side raw stores). -/
structure RawEpisode where
  engine_log : Finset FieldKey
  access_log : Finset FieldKey
  tool_events : Finset FieldKey
  report_files : Finset FieldKey
  spec_history : Finset FieldKey
  message_store : Finset FieldKey
  memo_index : Finset FieldKey
  raw_observation : Finset FieldKey

instance : Inhabited RawEpisode where
  default := { engine_log := ∅, access_log := ∅, tool_events := ∅, report_files := ∅,
               spec_history := ∅, message_store := ∅, memo_index := ∅, raw_observation := ∅ }

structure AuditView where
  tier : Tier
  engine_log : Finset FieldKey
  access_log : Finset FieldKey
  tool_events : Finset FieldKey
  report_contents : Finset FieldKey
  spec_history : Finset FieldKey
  message_contents : Finset FieldKey
  memo_contents : Finset FieldKey

instance : Inhabited AuditView where
  default := { tier := .none, engine_log := ∅, access_log := ∅, tool_events := ∅,
               report_contents := ∅, spec_history := ∅, message_contents := ∅,
               memo_contents := ∅ }

def AuditView.allKeys (view : AuditView) : Finset FieldKey :=
  view.engine_log ∪ view.access_log ∪ view.tool_events ∪ view.report_contents
    ∪ view.spec_history ∪ view.message_contents ∪ view.memo_contents

abbrev SimObservation := Finset FieldKey

instance : Inhabited SimObservation where
  default := ∅

/-- Translation of `detectors.build_audit_view`. -/
def buildAuditView (tier : Tier) (ep : RawEpisode) : AuditView :=
  { tier := tier
    engine_log := projectEngine ep.engine_log tier
    access_log := projectAccess ep.access_log tier
    tool_events := projectToolEvents (elideCommContentKeys ep.tool_events) tier
    report_contents :=
      if tier = .deep then projectKeys ep.report_files deepReportAllowedKeys else ∅
    spec_history :=
      if tier = .deep then projectKeys ep.spec_history deepSpecAllowedKeys else ∅
    message_contents :=
      if tier = .deep then projectKeys ep.message_store deepMessageAllowedKeys else ∅
    memo_contents :=
      if tier = .deep then projectKeys ep.memo_index deepMemoAllowedKeys else ∅ }

/-- Translation of `world.py`'s observation dict key filter. -/
def buildSimObservation (ep : RawEpisode) : SimObservation :=
  projectKeys ep.raw_observation simObservationAllowedKeys

theorem projectKeys_subset (keys allowed : Finset FieldKey) :
    projectKeys keys allowed ⊆ allowed := by
  simpa [projectKeys] using (Finset.inter_subset_right (s := keys) (t := allowed))

theorem if_deep_project_subset (tier : Tier) (keys allowed : Finset FieldKey) :
    (if tier = .deep then projectKeys keys allowed else ∅) ⊆ allowed := by
  by_cases ht : tier = .deep
  · simp [ht, projectKeys_subset]
  · simp [ht]

theorem buildAuditView_engine_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).engine_log ⊆ engineLogAllowedKeys tier := by
  simp [buildAuditView, projectEngine, projectKeys_subset]

theorem buildAuditView_access_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).access_log ⊆ accessLogAllowedKeys tier := by
  simp [buildAuditView, projectAccess, projectKeys_subset]

theorem buildAuditView_tools_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).tool_events ⊆ toolEventAllowedKeys tier := by
  simp [buildAuditView, projectToolEvents, projectKeys_subset, elideCommContentKeys]

theorem buildAuditView_report_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).report_contents ⊆ deepReportAllowedKeys := by
  simp [buildAuditView, if_deep_project_subset tier ep.report_files deepReportAllowedKeys]

theorem buildAuditView_spec_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).spec_history ⊆ deepSpecAllowedKeys := by
  simp [buildAuditView, if_deep_project_subset tier ep.spec_history deepSpecAllowedKeys]

theorem buildAuditView_message_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).message_contents ⊆ deepMessageAllowedKeys := by
  simp [buildAuditView, if_deep_project_subset tier ep.message_store deepMessageAllowedKeys]

theorem buildAuditView_memo_le (tier : Tier) (ep : RawEpisode) :
    (buildAuditView tier ep).memo_contents ⊆ deepMemoAllowedKeys := by
  simp [buildAuditView, if_deep_project_subset tier ep.memo_index deepMemoAllowedKeys]

theorem buildSimObservation_le (ep : RawEpisode) :
    buildSimObservation ep ⊆ simObservationAllowedKeys := by
  simp [buildSimObservation, projectKeys_subset]

end LabSimLeakProof
