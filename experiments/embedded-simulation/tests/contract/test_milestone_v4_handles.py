"""Milestone v4: handle-mediated probes, curves, and certification artifact."""

# pylint: disable=import-error

import json

from embedded_sim.batch import run_access_tier_curve, run_certification_capacity_curve, run_redteam_battery
from embedded_sim.certification_artifact import CERTIFICATION_ARTIFACT_PATH
from embedded_sim.embedded_audit import run_embedded_audit
from embedded_sim.handle_registry import HANDLE_REGISTRY, load_handle_registry
from embedded_sim.lab import build_world, load_episode_rows_from_vfs


def test_handle_registry_carries_v4_taxonomy_and_kernel_params():
    world, _l, _m = build_world("none", "honest", seed=42, T=160)
    registry = load_handle_registry(world.vfs)
    assert registry
    for spec in HANDLE_REGISTRY:
        row = registry[spec.handle_id]
        assert row["handle_type"]
        assert row["access_tier"] >= 1
        assert "uptake_prob" in row
        assert "kernel_latency_ms" in row


def test_probe_kernel_split_between_oracle_and_audit_projection():
    world, _l, _m = build_world("MB4", "capture_theater", seed=42, T=160)
    assert world.truth.handle_operations
    rows = load_episode_rows_from_vfs(world)
    probe = next(r for r in rows if r.get("intervention_active"))
    assert probe["handle"] == "handle.correction_request"
    assert probe["handle_type"] == "operation_correction"
    assert "handle_realized_latency_ms" in probe
    assert "_handle_kernel_truth" not in probe


def test_certification_artifact_emitted_with_handle_evidence():
    world, _l, _m = build_world("none", "honest", seed=42, T=200)
    cert, *_ = run_embedded_audit(world, instrumentation="medium_handles")
    raw = world.vfs.read(CERTIFICATION_ARTIFACT_PATH)
    assert raw
    artifact = json.loads(raw)
    assert cert.certification_artifact_path == CERTIFICATION_ARTIFACT_PATH
    assert artifact["schema_version"] == "1"
    assert artifact["access_model"]["access_tier"] == 2
    assert artifact["handle_evidence"]
    assert artifact["certification_verdict"]["conditional_on_access_model"]


def test_access_tier_curve_records_operation_handle_dose_response():
    payload = run_access_tier_curve(tiers=[1, 2], seeds=[11], T=160)
    assert payload["mode"] == "access_tier_curve"
    tier1, tier2 = payload["tiers"]
    assert tier1["operation_handles"] == []
    assert tier2["operation_handles"]
    assert "false_pass_rate" in tier2
    assert "cci_pass_rate" in tier2


def test_certification_capacity_curve_records_budget_points():
    payload = run_certification_capacity_curve(tiers=[1, 2], probe_budgets=[6], seeds=[11])
    assert payload["mode"] == "certification_capacity_curve"
    assert len(payload["points"]) == 2
    for point in payload["points"]:
        assert "max_certifiable_control_mean" in point
        assert "satisfies_numeric_leaf_rate" in point


def test_redteam_battery_reports_strategy_handle_matrix():
    payload = run_redteam_battery(
        bridges=["MB4"],
        seeds=[11],
        T=160,
        strategies=["probe_aware", "handle_evasion_tool_scope"],
        instrumentation_levels=["medium_handles"],
    )
    matrix = payload["summary_by_strategy_handle"]
    assert matrix["probe_aware|operation_correction"]["target_handle_type"] == "operation_correction"
    assert matrix["handle_evasion_tool_scope|operation_action"]["target_handle_type"] == "operation_action"
