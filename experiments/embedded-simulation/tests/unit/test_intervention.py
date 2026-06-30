"""Tests for graded intervention granularity and the co-active offender lab."""

from collections import Counter

import pytest

from embedded_sim.intervention_config import (
    get_intervention_level,
    init_intervention_level_from_env,
    intervention_artifact_suffix,
    set_intervention_level,
)
from embedded_sim.lab import build_world
from embedded_sim.lab_ecology import LabEcologyConfig, set_lab_ecology
from embedded_sim.unit_scope import OFFENDING_ACTIONS


@pytest.fixture(autouse=True)
def _restore_globals():
    prev = get_intervention_level()
    yield
    set_intervention_level(prev)
    set_lab_ecology(None)


def test_default_level_is_window():
    init_intervention_level_from_env()
    assert get_intervention_level() == "window"
    assert intervention_artifact_suffix("window") == ""
    assert intervention_artifact_suffix("actor") == "_int_actor"


def test_set_level_rejects_unknown():
    with pytest.raises(ValueError):
        set_intervention_level("galaxy_brain")  # type: ignore[arg-type]


def test_coactive_offender_creates_within_step_coactivity():
    set_lab_ecology(LabEcologyConfig(coactive_offender=True))
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=11, T=200)
    by_step: dict[int, Counter] = {}
    for ev in world.workflow:
        by_step.setdefault(ev.step, Counter())[ev.action_type] += 1

    coactive_steps = [
        step
        for step, counter in by_step.items()
        if any(counter[a] for a in OFFENDING_ACTIONS) and sum(counter.values()) > 1
    ]
    assert coactive_steps, "expected at least one step with offender + co-actor"
    for step in coactive_steps:
        actors = {ev.actor_id for ev in world.workflow if ev.step == step}
        assert len(actors) >= 2


def test_no_coactivity_by_default():
    set_lab_ecology(None)
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=11, T=200)
    steps = [ev.step for ev in world.workflow]
    assert len(steps) == len(set(steps)), "default lab is one actor per step"
