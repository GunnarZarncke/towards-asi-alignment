"""Knob-generated held-out worlds generalize without bridge-specific audit branches."""

import pytest

from embedded_sim.knob_world import KNOB_HELD_OUT_GRID, WorldKnobs, run_knob_episode
from embedded_sim.structural_fixtures import BLIND_SCENARIO


@pytest.mark.parametrize("knobs", KNOB_HELD_OUT_GRID)
def test_knob_worlds_do_not_false_pass(knobs: WorldKnobs):
    ep = run_knob_episode(knobs, seed=42)
    assert ep.in_sim.safety_decision != "pass" or ep.outer.in_sim_correct


def test_knob_episode_uses_blind_scenario_for_honest_baseline():
    knobs = WorldKnobs()
    assert knobs.structural_scenario == BLIND_SCENARIO
