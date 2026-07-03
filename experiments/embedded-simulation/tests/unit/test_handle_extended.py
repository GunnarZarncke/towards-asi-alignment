"""Unit tests for Part D (cont.) handles: output_channel_limit, successor_substitution,
challenge, counterfactual."""

from embedded_sim.handle_extended import (
    apply_challenge,
    apply_counterfactual,
    apply_output_channel_limit,
    apply_successor_substitution,
)
from embedded_sim.handle_registry import HANDLE_REGISTRY, handle_spec
from embedded_sim.lab import build_world


def _sample_row(**overrides):
    row = {
        "visible_action": 1,
        "true_action": 1,
        "reported_acceptance": 1,
        "handle_landed": 1,
        "intervention_active": 0,
        "intervention_intent": 0,
        "correction_request": 1,
    }
    row.update(overrides)
    return row


def test_new_registry_entries_present_with_full_spec():
    by_id = {spec.handle_id: spec for spec in HANDLE_REGISTRY}
    for handle_id, expected_type, expected_role in (
        ("handle.output_channel_limit", "operation_action", "action_QA"),
        ("handle.successor_substitution", "operation_boundary", "boundary_C"),
        ("handle.challenge", "communication", "communication"),
        ("handle.counterfactual", "communication", "communication"),
    ):
        spec = by_id[handle_id]
        assert spec.handle_type == expected_type
        assert spec.paper_role == expected_role
        assert spec.owner
        assert spec.evasion_story
        assert spec.anchor_path


def test_output_channel_limit_uses_generic_kernel():
    world, _l, _m = build_world("none", "honest", seed=1, T=40)
    row = _sample_row()
    realization = apply_output_channel_limit(world, row, step=5)
    assert realization.handle_id == "handle.output_channel_limit"
    assert row["handle_id"] == "handle.output_channel_limit"
    assert row["handle_type"] == "operation_action"


def test_successor_substitution_uses_generic_kernel():
    world, _l, _m = build_world("none", "honest", seed=1, T=40)
    row = _sample_row()
    realization = apply_successor_substitution(world, row, step=5)
    assert realization.handle_id == "handle.successor_substitution"
    assert row["handle_type"] == "operation_boundary"


def test_challenge_flags_correction_theater_mismatch():
    world, _l, _m = build_world("none", "honest", seed=1, T=40)
    honest_row = _sample_row(reported_acceptance=1, handle_landed=1)
    result = apply_challenge(world, honest_row, step=1)
    assert result["self_report_confirmed"] is True

    theater_row = _sample_row(reported_acceptance=1, handle_landed=0)
    result2 = apply_challenge(world, theater_row, step=2)
    assert result2["self_report_confirmed"] is False


def test_counterfactual_records_factual_action_without_fabricating_verdict():
    world, _l, _m = build_world("none", "honest", seed=1, T=40)
    row = _sample_row(visible_action=3)
    result = apply_counterfactual(world, row, step=7)
    assert result["factual_action"] == 3
    assert result["verified"] is None
    assert "note" in result


def test_challenge_and_counterfactual_appended_to_vfs_log():
    world, _l, _m = build_world("none", "honest", seed=1, T=40)
    apply_challenge(world, _sample_row(), step=1)
    apply_counterfactual(world, _sample_row(), step=2)
    assert world.vfs.read("/srv/audit/challenge.jsonl")
    assert world.vfs.read("/srv/audit/counterfactual.jsonl")


def test_handle_spec_lookup_for_new_handles():
    assert handle_spec("handle.output_channel_limit") is not None
    assert handle_spec("handle.successor_substitution") is not None
    assert handle_spec("handle.challenge") is not None
    assert handle_spec("handle.counterfactual") is not None
