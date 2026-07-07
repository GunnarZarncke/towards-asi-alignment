import LabSimLeakProof.Keys
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# Tier allowed-key sets — translation of `events.py` projections

Each log stream exposes a tier-dependent field set. Deep-tier-only content
fetch keys live in `detectors.build_audit_view`, not in the log projectors.
-/

namespace LabSimLeakProof

open FieldKey Tier

/-- Tool-event log: light metadata (`TOOL_EVENT_LIGHT_FIELDS`). -/
def toolEventLightKeys : Finset FieldKey :=
  { n, t, actor_id, tool, ok }

/-- Tool-event log: full-tier extras (`TOOL_EVENT_FULL_EXTRA`). -/
def toolEventFullExtraKeys : Finset FieldKey :=
  { args, args_digest, reason, perturbation, prev_hash, hash }

/-- Playbook-selection events expose extra fields at full tier. -/
def playbookSelectionFullKeys : Finset FieldKey :=
  { playbook, feature_deltas, step_kinds, prev_hash, hash }

inductive ToolEventKind
  | generic | playbookSelection
  deriving DecidableEq, Repr

def toolEventAllowedFor (tier : Tier) (kind : ToolEventKind) : Finset FieldKey :=
  if tier = .none then ∅
  else if tier = .light then toolEventLightKeys
  else
    match kind with
    | .generic => toolEventLightKeys ∪ toolEventFullExtraKeys
    | .playbookSelection => toolEventLightKeys ∪ playbookSelectionFullKeys

def toolEventAllowedKeys (tier : Tier) : Finset FieldKey :=
  toolEventAllowedFor tier .generic ∪ toolEventAllowedFor tier .playbookSelection

/-- Engine log light fields (`ENGINE_LOG_LIGHT_FIELDS`). -/
def engineLogLightKeys : Finset FieldKey :=
  { n, t, actor_id, step_id, status }

def engineLogFullExtraKeys : Finset FieldKey :=
  { reason, requires_capability, payload, on_behalf_of, model_id, spec_version,
    prev_hash, hash, measured_capability, measured_hazard, incident_hazard }

def engineLogAllowedKeys (tier : Tier) : Finset FieldKey :=
  if tier = .none then ∅
  else if tier = .light then engineLogLightKeys
  else engineLogLightKeys ∪ engineLogFullExtraKeys

/-- Access log light / full fields. -/
def accessLogLightKeys : Finset FieldKey :=
  { n, t, actor_id, action, result }

def accessLogFullExtraKeys : Finset FieldKey :=
  { capability, grantBy, prev_hash, hash }

def accessLogAllowedKeys (tier : Tier) : Finset FieldKey :=
  if tier = .none then ∅
  else if tier = .light then accessLogLightKeys
  else accessLogLightKeys ∪ accessLogFullExtraKeys

def logAllowedKeys (tier : Tier) (light fullExtra : Finset FieldKey) : Finset FieldKey :=
  if tier = .none then ∅
  else if tier = .light then light
  else light ∪ fullExtra

/-- Deep-tier workspace report fetch (`detectors.AuditView.report_contents`). -/
def deepReportAllowedKeys : Finset FieldKey :=
  { report_contents, content }

def deepSpecAllowedKeys : Finset FieldKey :=
  { spec_history, spec_version }

def deepMessageAllowedKeys : Finset FieldKey :=
  { message_contents, n, t, conversation_id, type, sender, text, custom,
    referenced_message_id, read_by }

def deepMemoAllowedKeys : Finset FieldKey :=
  { memo_contents, rel, actor_id, name, t, content }

/-- Keys permitted on the per-agent observation dict (`world.py`). -/
def simObservationAllowedKeys : Finset FieldKey :=
  { t, role, actor_id, goal_weights, temperature, model_id, completed_steps,
    last_denied_capability, last_payload, report_content, self_captured, decision_seed,
    extra_playbooks, build_params, capability_probe_mode, comms_enabled, channels_enabled,
    multi_gen_enabled, spec_upgrade_target, last_deployed_model_id,
    last_deployed_model_completed_steps, pinned_playbook, unit_id, committee_members,
    is_committee_chair, release_manager_id, committee_chair_id, board_messages, dm_messages,
    memo_files, content, text, custom, rel, name, sender, read_by, conversation_id,
    type, referenced_message_id }

-- Discharge: allowed sets exclude oracle-only keys by construction.
theorem engineLogAllowedKeys_disjoint_oracle (tier : Tier) :
    Disjoint (engineLogAllowedKeys tier) oracleOnlyKeys := by
  cases tier <;> native_decide

theorem accessLogAllowedKeys_disjoint_oracle (tier : Tier) :
    Disjoint (accessLogAllowedKeys tier) oracleOnlyKeys := by
  cases tier <;> native_decide

theorem toolEventAllowedFor_disjoint_oracle (tier : Tier) (kind : ToolEventKind) :
    Disjoint (toolEventAllowedFor tier kind) oracleOnlyKeys := by
  cases tier <;> cases kind <;> native_decide

theorem toolEventAllowedKeys_disjoint_oracle (tier : Tier) :
    Disjoint (toolEventAllowedKeys tier) oracleOnlyKeys := by
  cases tier <;> native_decide

theorem deepReportAllowedKeys_disjoint_oracle :
    Disjoint deepReportAllowedKeys oracleOnlyKeys := by native_decide

theorem deepSpecAllowedKeys_disjoint_oracle :
    Disjoint deepSpecAllowedKeys oracleOnlyKeys := by native_decide

theorem deepMessageAllowedKeys_disjoint_oracle :
    Disjoint deepMessageAllowedKeys oracleOnlyKeys := by native_decide

theorem deepMemoAllowedKeys_disjoint_oracle :
    Disjoint deepMemoAllowedKeys oracleOnlyKeys := by native_decide

theorem simObservationAllowedKeys_disjoint_oracleSecrets :
    Disjoint simObservationAllowedKeys oracleSecretKeys := by native_decide

theorem simObservationAllowedKeys_disjoint_auditSurface :
    Disjoint simObservationAllowedKeys auditSurfaceKeys := by native_decide

end LabSimLeakProof
