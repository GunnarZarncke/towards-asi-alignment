"""Unit tests for unified outer eval rules."""

from embedded_sim.audit_core.schemas import EvaluationResult
from embedded_sim.outer_rules import compute_false_pass, outer_certifies_for_bridge
from embedded_sim.schemas_embedded import InSimAuditCertificate, UADCandidate


def _cert(**kwargs) -> InSimAuditCertificate:
    base = dict(
        unit=UADCandidate("u1", "actor", ["a1"], 0.2),
        handles=[],
        cci_status="passes",
        safety_decision="pass",
        failed_bridge="none",
        read_anchors=[],
        source_digests={},
        notes=[],
    )
    base.update(kwargs)
    return InSimAuditCertificate(**base)


def test_false_pass_none_requires_rubric_correct():
    ev = EvaluationResult(
        controller_jaccard=0.5,
        board_jaccard=0.5,
        capture_detected=False,
        true_judge_captured=False,
        cci_status="passes",
        cci_status_correct=True,
        naive_vs_behavioral_gap=0.0,
        task_success_proxy=0.9,
        capability_correction_slack=0.0,
        detector_substrate_failed=False,
        hidden_probe_uptake=0.0,
        visible_probe_uptake=0.0,
        silent_harm_count=0,
        ground_drift_range=0.0,
        display_bearer_range=0.0,
        bundle_geometry_spread=0.0,
        bundle_reward_proxy_range=0.0,
        hidden_memory_step_rate=0.0,
        tool_shadow_step_rate=0.0,
        basin_capture_fraction_max=0.0,
        basin_percolation_crossed=False,
    )
    assert not compute_false_pass("none", _cert(), ev)
    ev_bad = EvaluationResult(**{**ev.__dict__, "cci_status_correct": False})
    assert compute_false_pass("none", _cert(), ev_bad)


def test_false_pass_on_failure_bridge_any_pass():
    ev = EvaluationResult(
        controller_jaccard=0.5,
        board_jaccard=0.5,
        capture_detected=True,
        true_judge_captured=True,
        cci_status="capturedInvalid",
        cci_status_correct=True,
        naive_vs_behavioral_gap=0.0,
        task_success_proxy=0.9,
        capability_correction_slack=0.0,
        detector_substrate_failed=False,
        hidden_probe_uptake=0.0,
        visible_probe_uptake=0.0,
        silent_harm_count=0,
        ground_drift_range=0.0,
        display_bearer_range=0.0,
        bundle_geometry_spread=0.0,
        bundle_reward_proxy_range=0.0,
        hidden_memory_step_rate=0.0,
        tool_shadow_step_rate=0.0,
        basin_capture_fraction_max=0.0,
        basin_percolation_crossed=False,
    )
    assert compute_false_pass("MB4", _cert(safety_decision="pass"), ev)


def test_outer_certifies_follows_rubric():
    ev = EvaluationResult(
        controller_jaccard=0.5,
        board_jaccard=0.5,
        capture_detected=True,
        true_judge_captured=True,
        cci_status="capturedInvalid",
        cci_status_correct=True,
        naive_vs_behavioral_gap=0.0,
        task_success_proxy=0.9,
        capability_correction_slack=0.0,
        detector_substrate_failed=False,
        hidden_probe_uptake=0.0,
        visible_probe_uptake=0.0,
        silent_harm_count=0,
        ground_drift_range=0.0,
        display_bearer_range=0.0,
        bundle_geometry_spread=0.0,
        bundle_reward_proxy_range=0.0,
        hidden_memory_step_rate=0.0,
        tool_shadow_step_rate=0.0,
        basin_capture_fraction_max=0.0,
        basin_percolation_crossed=False,
    )
    assert outer_certifies_for_bridge("MB4", _cert(safety_decision="pause"), ev)
