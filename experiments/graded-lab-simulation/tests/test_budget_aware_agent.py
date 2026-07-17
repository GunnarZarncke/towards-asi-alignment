"""Validation battery for the resource-sensitive agent program.

See `DESIGN.md` "Phase 7c backlog item 1: resource-sensitive agent
program" and FINDINGS GL-17. This is a **small, separate** battery
(n=10 seeds x 5 `carrier_load_scale` cells = 50 episodes), deliberately
not wired into the main `AGENT_TYPES` calibration battery. Marked slow
because it runs real episodes; not part of the fast/smoke profile.

Acceptance is explicitly **not** 100% coverage — see the module-level
docstring in `budget_release_manager` and DESIGN.md for the accepted
criteria (a real, materially nonzero deploy-rate range, and a mostly
(not strictly) decreasing trend across cells). The retired relative
comparison to frozen STRONG/WEAK deploy-range (GL-67) is recorded in
FINDINGS GL-50/GL-67.
"""

from __future__ import annotations

import pytest

from graded_lab.oracle_only.calibration import (
    BUDGET_AWARE_AGENT,
    CARRIER_SCALES,
    NOMINAL_COMPUTE_SCALE,
    NOMINAL_SPREAD_SCALE,
    WEAK_AGENT,
    MIN_DEMONSTRATED_DEPLOY_RANGE,
    config_for_settings,
    programs_for,
)
from graded_lab.world_visible.config import SubstrateSettings
from graded_lab.world_visible.world import run_episode

VALIDATION_SEEDS = tuple(range(10))


def test_programs_for_budget_aware_agent_only_varies_rm1():
    programs = programs_for(BUDGET_AWARE_AGENT)
    weak = programs_for(WEAK_AGENT)
    assert programs["rm1"] == "budget_release_manager"
    # eng1/rev1/admin1 unchanged from WEAK_AGENT — the one varying
    # decision is isolated (DESIGN.md backlog item 1).
    assert programs["eng1"] == weak["eng1"]
    assert programs["rev1"] == weak["rev1"]
    assert programs["admin1"] == weak["admin1"]


def _deploy_rates_by_carrier_load(agent_type: str, backend) -> dict[float, float]:
    rates: dict[float, float] = {}
    programs = programs_for(agent_type)
    for carrier_load_scale in CARRIER_SCALES:
        settings = SubstrateSettings(
            compute_scale=NOMINAL_COMPUTE_SCALE,
            population_spread_scale=NOMINAL_SPREAD_SCALE,
            carrier_load_scale=carrier_load_scale,
        )
        cfg = config_for_settings(settings)
        deploys = 0
        for seed in VALIDATION_SEEDS:
            result = run_episode(cfg, seed, backend, programs=programs)
            deploys += int(result.deployed)
        rates[carrier_load_scale] = deploys / len(VALIDATION_SEEDS)
    return rates


@pytest.mark.slow
def test_budget_release_manager_abandons_under_time_pressure_synthetic():
    """Unit-level check of the abandon mechanism itself, independent of
    whether the population-level battery below shows a trend: a
    release manager with steps outstanding and less than
    `BUDGET_ABANDON_REMAINING_FRACTION` of the episode left must return
    `None` (give up) rather than attempt to advance the pipeline."""
    from graded_lab.agent_visible.programs import budget_release_manager

    observation = {
        "role": "release_manager",
        "busy": False,
        "t": 96,
        "T": 100,
        "model_id": "m1",
        "affordable_primitives": [
            {
                "kind": "call",
                "args": {
                    "endpoint": "pipeline.trigger_step",
                    "args": {"step_id": "compliance_signoff", "args": {"model_id": "m1"}},
                },
            }
        ],
        "last_primitive_outcome": None,
    }
    state: dict = {}
    choice = budget_release_manager(observation, state)
    assert choice is None
    assert state.get("abandoned") is True


@pytest.mark.slow
def test_budget_release_manager_does_not_abandon_with_ample_time():
    from graded_lab.agent_visible.programs import budget_release_manager

    observation = {
        "role": "release_manager",
        "busy": False,
        "t": 10,
        "T": 100,
        "model_id": "m1",
        "affordable_primitives": [
            {
                "kind": "call",
                "args": {
                    "endpoint": "pipeline.trigger_step",
                    "args": {"step_id": "compliance_signoff", "args": {"model_id": "m1"}},
                },
            }
        ],
        "last_primitive_outcome": None,
    }
    state: dict = {}
    choice = budget_release_manager(observation, state)
    assert choice is not None
    assert not state.get("abandoned")


@pytest.mark.slow
def test_budget_aware_agent_deploy_rate_responds_to_carrier_load():
    """Small (n=10 seeds x 5 cells) validation battery, not part of the
    main calibration battery (DESIGN.md backlog item 1). Accepts a real
    but partial (not 100%-monotonic) graded response, per this
    session's explicit acceptance criterion."""
    from graded_lab.harness.isolate import MockIsolate

    backend = MockIsolate()
    rates = _deploy_rates_by_carrier_load(BUDGET_AWARE_AGENT, backend)
    ordered = [rates[c] for c in CARRIER_SCALES]

    deploy_range = max(ordered) - min(ordered)
    assert deploy_range >= MIN_DEMONSTRATED_DEPLOY_RANGE, (
        f"expected a materially nonzero deploy-rate range across carrier_load_scale, "
        f"got {ordered} (range={deploy_range})"
    )

    deltas = [b - a for a, b in zip(ordered, ordered[1:])]
    non_increasing = sum(1 for d in deltas if d <= 0)
    assert non_increasing >= 3, (
        f"expected at least 3 of {len(deltas)} consecutive-cell deltas to be "
        f"non-increasing (accepting partial, not 100%, coverage per this "
        f"session's decision), got deltas={deltas} rates={ordered}"
    )
