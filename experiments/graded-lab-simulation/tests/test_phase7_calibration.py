"""Phase 7c-revised: ecology calibration battery evaluation logic.

See DESIGN.md "Phase 7c-revised ecology calibration battery" and
FINDINGS G-16 for why this evaluator differs from the original Phase 7c
sketch (`test_substrate_grid_has_sixteen_cells` below is the retained
diagnostic fixture for that original grid, not the battery default now).
"""

from __future__ import annotations

import pytest

from graded_lab.oracle_only.calibration import (
    AGENT_TYPES,
    CARRIER_SCALES,
    CalibrationRecord,
    DoseRecord,
    STRONG_AGENT,
    WEAK_AGENT,
    carrier_grid,
    classify_cells_by_reference_agent,
    eai_band,
    evaluate_pass_criteria,
    programs_for,
    select_mid_band_cell,
    substrate_grid,
)


def test_substrate_grid_has_sixteen_cells():
    grid = substrate_grid()
    assert len(grid) == 16
    assert all(s.carrier_load_scale == 0.0 for s in grid)


def test_carrier_grid_has_five_cells_at_nominal_compute_spread():
    grid = carrier_grid()
    assert len(grid) == len(CARRIER_SCALES) == 5
    assert {s.carrier_load_scale for s in grid} == set(CARRIER_SCALES)
    assert all(s.compute_scale == 1.0 and s.population_spread_scale == 1.0 for s in grid)


def test_programs_for_agent_types():
    strong = programs_for(STRONG_AGENT)
    weak = programs_for(WEAK_AGENT)
    assert strong["eng1"] == "softmax_optimizer"
    assert weak["eng1"] == "walk_pipeline"
    assert weak["rev1"] == "reviewer_peer_review"


def test_eai_band_labels():
    assert eai_band(0.10) == "low"
    assert eai_band(0.35) == "mid"
    assert eai_band(0.70) == "high"
    assert eai_band(0.20) is None


def test_classify_cells_by_reference_agent_uses_strong_only():
    records = [
        CalibrationRecord(1.0, 1.0, STRONG_AGENT, 0, 0.30, "mid", 0, False, 0.0, 0.0, 0.0, True),
        CalibrationRecord(1.0, 1.0, STRONG_AGENT, 1, 0.32, "mid", 0, False, 0.0, 0.0, 0.0, True),
        # Weak agent's own EAI is far below mid, but must not affect the
        # cell's classification (FINDINGS G-16 Cause 3).
        CalibrationRecord(1.0, 1.0, WEAK_AGENT, 0, 0.02, None, 1, True, 0.0, 0.0, 0.0, True),
    ]
    bands = classify_cells_by_reference_agent(records)
    assert bands[(1.0, 1.0, 0.0)] == "mid"


def test_evaluate_pass_criteria_all_pass_synthetic():
    # Criterion 1: within-type slope needs both episode-level deploy
    # variance *and* a real cell-level (substrate-driven) deploy-rate
    # range — a different carrier_load_scale per record stands in for
    # distinct cells here, so the low-EAI/deploying and high-EAI/non-
    # deploying records land in different cells, not one cell with
    # incidental seed-level variance.
    strong_eais = [0.08, 0.10, 0.12, 0.14, 0.30, 0.35, 0.40, 0.72]
    strong_deploys = [True, True, True, False, False, False, False, False]
    strong_loads = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
    records = [
        CalibrationRecord(
            1.0, 1.0, STRONG_AGENT, i, eai,
            eai_band(eai), int(deploy), bool(deploy), 0.0, 0.0, 0.0, True,
            carrier_load_scale=load, cell_eai_band=eai_band(eai),
        )
        for i, (eai, deploy, load) in enumerate(zip(strong_eais, strong_deploys, strong_loads))
    ]
    records += [
        CalibrationRecord(
            1.0, 1.0, STRONG_AGENT, seed, 0.30, "mid", 0, False, 0.0, 0.0, 0.0, True,
            i_ctrl_bits=0.5, cell_eai_band="mid",
        )
        for seed in range(5)
    ]
    records += [
        CalibrationRecord(
            1.0, 1.0, WEAK_AGENT, seed, 0.30, "mid", 0, False, 0.0, 0.0, 0.0, True,
            i_ctrl_bits=0.1, cell_eai_band="mid",
        )
        for seed in range(5)
    ]
    records += [
        CalibrationRecord(
            1.0, 1.0, STRONG_AGENT, seed, 0.72, "high", 0, False, 0.0, 0.0, 0.0, True,
            cell_eai_band="high",
        )
        for seed in range(3)
    ]
    doses = [
        DoseRecord(1.0, 1.0, 0.0, 0.8, 0.35, 5),
        DoseRecord(1.0, 1.0, 0.5, 0.6, 0.35, 5),
        DoseRecord(1.0, 1.0, 1.0, 0.4, 0.35, 5),
        DoseRecord(1.0, 1.0, 1.5, 0.1, 0.35, 5),
    ]
    report = evaluate_pass_criteria(records, doses)
    assert not report.criterion_1_inconclusive
    assert report.criterion_1_deploy_eai_negative_slope
    assert report.criterion_2_mid_band_ctrl_separation
    assert not report.criterion_3_inconclusive
    assert report.criterion_3_high_band_deploy_collapse
    assert not report.criterion_4_inconclusive
    assert report.criterion_4_graded_dose_response
    assert report.all_passed


def test_evaluate_pass_criteria_fails_bad_dose_response():
    records = [
        CalibrationRecord(1.0, 1.0, STRONG_AGENT, 0, 0.35, "mid", 1, True, 0.0, 0.0, 0.0, True, 0.5, cell_eai_band="mid"),
        CalibrationRecord(1.0, 1.0, WEAK_AGENT, 0, 0.35, "mid", 1, True, 0.0, 0.0, 0.0, True, 0.1, cell_eai_band="mid"),
    ] * 4
    doses = [
        DoseRecord(1.0, 1.0, 0.0, 0.5, 0.35, 5),
        DoseRecord(1.0, 1.0, 0.5, 0.5, 0.35, 5),
        DoseRecord(1.0, 1.0, 1.0, 0.5, 0.35, 5),
        DoseRecord(1.0, 1.0, 1.5, 0.5, 0.35, 5),
    ]
    report = evaluate_pass_criteria(records, doses)
    assert not report.criterion_4_graded_dose_response
    assert report.criterion_4_inconclusive  # all-constant deploy rate, not a tested failure


def test_evaluate_pass_criteria_pooled_slope_confound_is_not_criterion_1():
    """Regression for FINDINGS G-16 Cause 1: an agent-type composition
    that would make a *pooled* slope negative (strong never deploys and
    has high EAI; weak always deploys and has low EAI) must not pass
    criterion 1 when neither agent type has within-type deploy variance."""
    records = [
        CalibrationRecord(1.0, 1.0, STRONG_AGENT, seed, 0.26, "mid", 0, False, 0.0, 0.0, 0.0, True)
        for seed in range(10)
    ] + [
        CalibrationRecord(1.0, 1.0, WEAK_AGENT, seed, 0.02, None, 1, True, 0.0, 0.0, 0.0, True)
        for seed in range(10)
    ]
    report = evaluate_pass_criteria(records, [])
    assert report.criterion_1_inconclusive
    assert not report.criterion_1_deploy_eai_negative_slope
    # The pooled slope is still reported (diagnostic only) and would in
    # fact be strongly negative — demonstrating why it must not gate.
    assert report.deploy_eai_slope is not None
    assert report.deploy_eai_slope < 0


def test_select_mid_band_cell_picks_closest_to_target():
    records = [
        CalibrationRecord(0.5, 0.5, STRONG_AGENT, 0, 0.28, "mid", 0, False, 0.0, 0.0, 0.0, True, cell_eai_band="mid"),
        CalibrationRecord(1.5, 1.5, STRONG_AGENT, 0, 0.40, "mid", 0, False, 0.0, 0.0, 0.0, True, cell_eai_band="mid"),
    ]
    assert select_mid_band_cell(records) == (1.5, 1.5, 0.0)


@pytest.mark.slow
def test_check_mechanism_sensitivity_flags_dead_knob():
    from graded_lab.harness.isolate import MockIsolate
    from graded_lab.oracle_only.calibration import check_mechanism_sensitivity

    reports = check_mechanism_sensitivity(
        knob_values={
            "compute_scale": (0.5, 2.0),
            "carrier_load_scale": (0.0, 2.0),
        },
        agent_types=(STRONG_AGENT,),
        seeds=(0, 1, 2, 3, 4),
        backend=MockIsolate(),
        progress=False,
    )
    by_knob = {r.knob: r for r in reports}
    assert set(by_knob) == {"compute_scale", "carrier_load_scale"}
    # Matches FINDINGS G-16 Prediction 1: compute_scale is a dead knob
    # within its frozen range for this ecology/roster; carrier_load_scale
    # is not.
    assert by_knob["compute_scale"].demonstrated_effect is False
    assert by_knob["carrier_load_scale"].demonstrated_effect is True


@pytest.mark.slow
def test_smoke_calibration_battery_two_cells():
    from graded_lab.harness.isolate import MockIsolate
    from graded_lab.oracle_only.calibration import run_calibration_battery
    from graded_lab.world_visible.config import SubstrateSettings

    payload = run_calibration_battery(
        backend=MockIsolate(),
        seeds=(0, 1),
        settings_list=[
            SubstrateSettings(compute_scale=1.0, population_spread_scale=1.0, carrier_load_scale=0.0),
            SubstrateSettings(compute_scale=1.0, population_spread_scale=1.0, carrier_load_scale=1.0),
        ],
        compute_i_ctrl=False,
        progress=False,
    )
    assert len(payload["records"]) == 2 * len(AGENT_TYPES) * 2
    assert "pass_criteria" in payload
    assert "all_passed" in payload["pass_criteria"]
    assert "cell_bands" in payload
