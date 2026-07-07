import LabSimLeakProof.Leakage
import LabSimLeakProof.Projections
import LabSimLeakProof.Tiers
import LabSimLeakProof.Reachability
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Tactic

/-!
# Leak-proof theorems — projection certificates + reachability corollaries

Combines by-construction projection bounds (`Projections.lean`) with the
global reachability analysis (`Reachability.lean`).
-/

namespace LabSimLeakProof

open FieldKey Tier

private theorem oracleLeakageCount_eq_zero_of_disjoint {keys : Finset FieldKey}
    (h : Disjoint keys oracleOnlyKeys) : oracleLeakageCount keys = 0 := by
  have := (Finset.disjoint_iff_inter_eq_empty.1 h)
  simp [oracleLeakageCount, Finset.card_eq_zero, this]

private theorem oracleSecretSimLeakageCount_eq_zero_of_disjoint {keys : Finset FieldKey}
    (h : Disjoint keys oracleSecretKeys) : oracleSecretSimLeakageCount keys = 0 := by
  have := (Finset.disjoint_iff_inter_eq_empty.1 h)
  simp [oracleSecretSimLeakageCount, Finset.card_eq_zero, this]

private theorem auditToSimLeakageCount_eq_zero_of_disjoint {keys : Finset FieldKey}
    (h : Disjoint keys auditSurfaceKeys) : auditToSimLeakageCount keys = 0 := by
  have := (Finset.disjoint_iff_inter_eq_empty.1 h)
  simp [auditToSimLeakageCount, Finset.card_eq_zero, this]

private theorem auditView_component_disjoint_oracle (tier : Tier) (view : AuditView)
    (heng : view.engine_log ⊆ engineLogAllowedKeys tier)
    (ha : view.access_log ⊆ accessLogAllowedKeys tier)
    (ht : view.tool_events ⊆ toolEventAllowedKeys tier)
    (hr : view.report_contents ⊆ deepReportAllowedKeys)
    (hs : view.spec_history ⊆ deepSpecAllowedKeys)
    (hm : view.message_contents ⊆ deepMessageAllowedKeys)
    (hmemo : view.memo_contents ⊆ deepMemoAllowedKeys) :
    Disjoint view.allKeys oracleOnlyKeys := by
  rw [AuditView.allKeys]
  have hE := (engineLogAllowedKeys_disjoint_oracle tier).mono_left heng
  have hA := (accessLogAllowedKeys_disjoint_oracle tier).mono_left ha
  have hT := (toolEventAllowedKeys_disjoint_oracle tier).mono_left ht
  have hR := deepReportAllowedKeys_disjoint_oracle.mono_left hr
  have hS := deepSpecAllowedKeys_disjoint_oracle.mono_left hs
  have hM := deepMessageAllowedKeys_disjoint_oracle.mono_left hm
  have hMemo := deepMemoAllowedKeys_disjoint_oracle.mono_left hmemo
  exact
    (Finset.disjoint_union_left.2 <|
      ⟨Finset.disjoint_union_left.2 <|
        ⟨Finset.disjoint_union_left.2 <|
          ⟨Finset.disjoint_union_left.2 <|
            ⟨Finset.disjoint_union_left.2 <|
              ⟨Finset.disjoint_union_left.2 ⟨hE, hA⟩, hT⟩, hR⟩, hS⟩, hM⟩, hMemo⟩)

theorem buildAuditView_allKeys_disjoint_oracle (tier : Tier) (ep : RawEpisode) :
    Disjoint (buildAuditView tier ep).allKeys oracleOnlyKeys := by
  refine auditView_component_disjoint_oracle tier (buildAuditView tier ep) ?eng ?acc ?tool ?rep ?spec ?msg ?memo
  · exact buildAuditView_engine_le tier ep
  · exact buildAuditView_access_le tier ep
  · exact buildAuditView_tools_le tier ep
  · exact buildAuditView_report_le tier ep
  · exact buildAuditView_spec_le tier ep
  · exact buildAuditView_message_le tier ep
  · exact buildAuditView_memo_le tier ep

/-- Oracle ground truth never appears in a tier-projected audit view. -/
theorem buildAuditView_no_oracle_leak (tier : Tier) (ep : RawEpisode) :
    oracleLeakageCount (buildAuditView tier ep).allKeys = 0 :=
  oracleLeakageCount_eq_zero_of_disjoint (buildAuditView_allKeys_disjoint_oracle tier ep)

theorem buildSimObservation_disjoint_oracleSecrets (ep : RawEpisode) :
    Disjoint (buildSimObservation ep) oracleSecretKeys :=
  simObservationAllowedKeys_disjoint_oracleSecrets.mono_left (buildSimObservation_le ep)

theorem buildSimObservation_disjoint_auditSurface (ep : RawEpisode) :
    Disjoint (buildSimObservation ep) auditSurfaceKeys :=
  simObservationAllowedKeys_disjoint_auditSurface.mono_left (buildSimObservation_le ep)

/-- Oracle secrets never appear in the certified simulation observation. -/
theorem buildSimObservation_no_oracle_secret_leak (ep : RawEpisode) :
    oracleSecretSimLeakageCount (buildSimObservation ep) = 0 :=
  oracleSecretSimLeakageCount_eq_zero_of_disjoint (buildSimObservation_disjoint_oracleSecrets ep)

/-- Audit-plane keys never appear in the certified simulation observation. -/
theorem buildSimObservation_no_audit_surface_leak (ep : RawEpisode) :
    auditToSimLeakageCount (buildSimObservation ep) = 0 :=
  auditToSimLeakageCount_eq_zero_of_disjoint (buildSimObservation_disjoint_auditSurface ep)

theorem episode_leakage_exact (tier : Tier) (ep : RawEpisode) :
    (leakageOf (buildAuditView tier ep) (buildSimObservation ep)).exact := by
  constructor
  · rw [leakageOf, oracleLeakageCount_eq_zero_of_disjoint]
    exact buildAuditView_allKeys_disjoint_oracle tier ep
  constructor
  · rw [leakageOf, oracleSecretSimLeakageCount_eq_zero_of_disjoint]
    exact buildSimObservation_disjoint_oracleSecrets ep
  · rw [leakageOf, auditToSimLeakageCount_eq_zero_of_disjoint]
    exact buildSimObservation_disjoint_auditSurface ep

def certified_episode (tier : Tier) (ep : RawEpisode) : LeakProofCertificate where
  view := buildAuditView tier ep
  sim := buildSimObservation ep
  counts := leakageOf (buildAuditView tier ep) (buildSimObservation ep)
  hexact := episode_leakage_exact tier ep

theorem certified_episode_no_unintended_leak (tier : Tier) (ep : RawEpisode) :
    (certified_episode tier ep).counts.exact :=
  episode_leakage_exact tier ep

/-- Reachability analysis confirms no alternate Python path bypasses the projections. -/
theorem reachability_implies_projection_oracle_bound :
    ReachabilityCertificate := reachability_certificate

end LabSimLeakProof
