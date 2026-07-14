"""Phase 7b: UAD-backed ecology-BIQ over inferred units (unit_biq.py).

See DESIGN.md "Phase 7b UAD-backed ecology-BIQ" for the pre-registered
estimator choices these tests hold fixed.
"""

from __future__ import annotations

import math

import pytest

from graded_lab.harness.ecology import committee_config, committee_programs
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.unit_biq import (
    _outcome_state,
    held_out_bits,
    unit_control_bits,
    unit_ecology_biq,
    unit_memory_bits,
    unit_prediction_bits,
    unit_self_surprise_bits,
)
from graded_lab.world_visible.world import default_lab_config, run_episode


def test_held_out_bits_deterministic_mapping_is_near_max_reduction():
    """x perfectly determines y (2 classes) -> ~1 bit saved on held-out data."""
    pairs = [(i % 2, i % 2) for i in range(40)]
    train, test = pairs[:24], pairs[24:]
    bits = held_out_bits(train, test, mode="reduction")
    assert bits is not None
    assert bits > 0.7  # some smoothing loss vs. the ideal 1.0 bit


def test_held_out_bits_no_relationship_is_near_zero():
    """x carries no information about y -> reduction should be small (can be
    slightly negative from finite-sample smoothing noise, never large)."""
    pairs = [(i % 2, (i * 7) % 3) for i in range(60)]
    train, test = pairs[:36], pairs[36:]
    bits = held_out_bits(train, test, mode="reduction")
    assert bits is not None
    assert -0.3 < bits < 0.3


def test_held_out_bits_nll_mode_returns_raw_positive_bits():
    pairs = [(i % 3, i % 3) for i in range(30)]
    train, test = pairs[:18], pairs[18:]
    nll = held_out_bits(train, test, mode="nll")
    assert nll is not None
    assert nll > 0.0


def test_held_out_bits_empty_input_is_unavailable():
    assert held_out_bits([], [(0, 0)], mode="reduction") is None
    assert held_out_bits([(0, 0)], [], mode="reduction") is None


class _FakeResult:
    def __init__(self, boundary_streams):
        self.boundary_streams = boundary_streams


def test_unit_memory_bits_counts_distinct_paths_across_members():
    result = _FakeResult(
        {
            "a": [{"artifacts": {"x": 1}}, {"artifacts": {"x": 1, "y": 2}}],
            "b": [{"artifacts": {"z": 3}}],
        }
    )
    bits = unit_memory_bits(result, ("a", "b"))
    assert bits == math.log2(1 + 3)  # {x, y, z}


def test_unit_memory_bits_empty_unit_is_zero():
    result = _FakeResult({})
    assert unit_memory_bits(result, ()) == 0.0


def test_unit_prediction_bits_detects_reviewer_review_signal():
    """committee reviewers' own action-codes should carry held-out
    predictive information about the review-pass event they jointly
    produce (see FINDINGS GL-11 committee_reviewer lab_ping wart — this
    is the *review_token* event, a separate signal from that wart)."""
    cfg = committee_config()
    programs = committee_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    bits = unit_prediction_bits(result, ("rev1", "rev2"))
    assert set(bits) == {
        "next_primitive_denied",
        "review_token_within_10_ticks",
        "deploy_succeeds_within_40_ticks",
    }
    assert bits["review_token_within_10_ticks"] is not None
    assert bits["review_token_within_10_ticks"] > 0.0


def test_unit_self_surprise_bits_is_finite_and_nonnegative():
    cfg = committee_config()
    programs = committee_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    surp = unit_self_surprise_bits(result, ("rev1", "rev2"))
    assert surp is not None
    assert surp >= 0.0


def test_outcome_state_distinguishes_task_driver_from_contention_bystander():
    """Regression for FINDINGS GL-13/GL-14: at seed 11 on default_lab_config,
    freezing the task-critical eng1 *and* freezing the unrelated admin1
    both collapse deploy to 0 (a real resource-contention confound), so
    an outcome vector scoped to (deploy, harm) alone cannot tell them
    apart. The contention dimension (denied primitives among actors
    outside the unit) must distinguish them even when deploy/harm do
    not."""
    cfg = default_lab_config()
    programs = {a.actor_id: "softmax_optimizer" for a in cfg.agents}
    frozen_eng = dict(programs)
    frozen_eng["eng1"] = "noop"
    frozen_admin = dict(programs)
    frozen_admin["admin1"] = "noop"

    eng_result = run_episode(cfg, 11, MockIsolate(), programs=frozen_eng)
    admin_result = run_episode(cfg, 11, MockIsolate(), programs=frozen_admin)

    # The task+harm slice alone collapses identically for both freezes.
    assert eng_result.deploy_count == admin_result.deploy_count == 0
    assert eng_result.bearer_harm == admin_result.bearer_harm == 0.0

    eng_state = _outcome_state(eng_result, ("eng1",))
    admin_state = _outcome_state(admin_result, ("admin1",))
    assert eng_state != admin_state
    assert eng_state[3] != admin_state[3]  # the contention dimension differs


@pytest.mark.slow
def test_unit_control_bits_runs_battery_and_returns_bits_or_none():
    """Sanity check only: with the default 5-seed battery at baseline
    settings, deploy is rare (Phase-3 freeze gate: non-degenerate but not
    saturated), so I_ctrl is frequently ~0 — a real, honestly-reported
    absence of signal, not an estimator bug (see FINDINGS for the
    resource-contention confound: freezing *either* a task actor or an
    unrelated admin actor at some seeds changes deploy identically,
    because removing any actor changes shared-resource contention)."""
    cfg = committee_config()
    programs = committee_programs()
    bits = unit_control_bits(
        cfg, seed=3, unit_members=("rev1", "rev2"), programs=programs,
        backend=MockIsolate(), ctrl_seeds=3,
    )
    assert bits is None or isinstance(bits, float)


@pytest.mark.slow
def test_unit_ecology_biq_reports_every_component_never_only_composite():
    cfg = committee_config()
    programs = committee_programs()
    report = unit_ecology_biq(
        cfg, seed=3, unit_members=("rev1", "rev2"), programs=programs,
        backend=MockIsolate(), ctrl_seeds=2,
    )
    d = report.as_dict()
    assert set(d) == {
        "unit_members", "I_pred", "I_pred_total", "I_ctrl", "H_mem",
        "S_surp", "field_incident_rate_above_median", "K_biq",
    }
    assert d["field_incident_rate_above_median"] is None  # single episode
    if d["K_biq"] is not None:
        assert d["K_biq"] == pytest.approx(
            d["I_pred_total"] + d["I_ctrl"] - d["H_mem"] - d["S_surp"]
        )
