import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# Field keys — mirror of Python dict keys in lab-simulation

Finite enumeration of JSON field names exchanged across the three planes.
Partitions match `config.ORACLE_ONLY_FIELDS`, intentional sim channels, and
audit-surface keys from `events.py` / `detectors.py` / `world.py`.
-/

namespace LabSimLeakProof

/-- Audit tier ladder (`config.TIERS`). -/
inductive Tier
  | none | light | full | deep
  deriving DecidableEq, Repr

/-- JSON / observation field names appearing anywhere in lab-simulation. -/
inductive FieldKey
  -- Oracle ground truth (`oracle.py`, `config.ORACLE_ONLY_FIELDS`)
  | true_capability | true_hazard | bearer_harm
  | units | groups | goal_weights
  | board_captured | admin_captured
  -- Intentional unlogged sim channel (derived from config, not full `units`)
  | unit_id | committee_members | committee_chair_id
  | is_committee_chair | release_manager_id
  -- Measured / noisy audit-plane values (not oracle truth)
  | measured_capability | measured_hazard | incident_hazard
  -- Shared log metadata
  | n | t | actor_id | prev_hash | hash
  -- Engine log (`pipeline_engine.py`)
  | step_id | status | reason | requires_capability
  | payload | on_behalf_of | model_id | spec_version
  -- Access log (`access.py`)
  | action | result | capability | grantBy
  -- Tool-event log (`tools.py`, `events.py`)
  | tool | ok | args | args_digest | perturbation
  | playbook | feature_deltas | step_kinds
  -- Deep-tier audit fetch containers (`detectors.build_audit_view`)
  | report_contents | spec_history | message_contents | memo_contents
  -- Comm / memo nested content
  | text | custom | content | sender | read_by
  | conversation_id | type | referenced_message_id | rel | name
  -- Per-agent observation (`world.py`, `llm_agent.py`)
  | role | temperature | completed_steps | last_denied_capability | last_payload
  | report_content | self_captured | decision_seed | extra_playbooks | build_params
  | capability_probe_mode | comms_enabled | channels_enabled | multi_gen_enabled
  | spec_upgrade_target | last_deployed_model_id | last_deployed_model_completed_steps
  | pinned_playbook | board_messages | dm_messages | memo_files
  deriving DecidableEq, Repr

open FieldKey

/-- Keys that must never appear in any audit projection or engine log
(`config.ORACLE_ONLY_FIELDS`, `tests/harness/test_planes.py`). -/
def oracleOnlyKeys : Finset FieldKey :=
  { true_capability, true_hazard, bearer_harm, units, groups, goal_weights,
    board_captured, admin_captured }

/-- Oracle secrets that must not reach the simulation observation channel.
Excludes intentional sim-adjacent keys (`goal_weights`, unit/committee view). -/
def oracleAdjacentSimKeys : Finset FieldKey :=
  { goal_weights, unit_id, committee_members, committee_chair_id,
    is_committee_chair, release_manager_id }

def oracleSecretKeys : Finset FieldKey :=
  oracleOnlyKeys \ oracleAdjacentSimKeys

/-- Keys that appear on the audit plane but are excluded from the sim observation wire.
Log-stream metadata and deep-fetch containers only — not shared live-state keys
(`model_id`, `content`, comm fields) that also appear legitimately in `world.py`. -/
def auditSurfaceKeys : Finset FieldKey :=
  { n, prev_hash, hash, step_id, status, reason, requires_capability, payload,
    on_behalf_of, spec_version, measured_capability, measured_hazard, incident_hazard,
    action, result, capability, grantBy, tool, ok, args, args_digest, perturbation,
    playbook, feature_deltas, step_kinds, report_contents, spec_history,
    message_contents, memo_contents }

/-- Content keys elided at the tool-event logging boundary (`tools._scalar_args`). -/
def commContentKeys : Finset FieldKey :=
  { text, custom, content }

theorem oracleSecret_simAdjacent_disjoint :
    Disjoint oracleSecretKeys oracleAdjacentSimKeys := by
  native_decide

theorem oracleOnly_superset_secrets :
    oracleSecretKeys ⊆ oracleOnlyKeys := by
  intro k hk
  simp [oracleSecretKeys, oracleAdjacentSimKeys] at hk ⊢
  tauto

end LabSimLeakProof
