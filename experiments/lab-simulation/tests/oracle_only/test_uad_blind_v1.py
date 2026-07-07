"""Blind detector generation, round 1 (BLIND_DETECTOR_GENERATION.md):
golden tests for ``uad_blind_v1.py`` reproducing the smoke-scale results
recorded in ``results/FINDINGS.md`` (G-30)."""

from __future__ import annotations

import pytest

from lab_sim.harness.ecology import (
    build_loop_config,
    committee_with_informal_chatter_config,
    covert_file_handoff_config,
    dm_pair_config,
    serial_pipeline_no_unit_config,
    shared_slot_config,
)
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad_blind_v1 import classify_pair_silent, discovered_units_blind, reaction_to_source
from lab_sim.oracle_only.uad_partition import exact_partition, nonsingleton_clusters
from lab_sim.world_visible.world import run_episode


def _run_blind(factory, seed: int = 1):
    if factory is covert_file_handoff_config:
        cfg = factory(trusting=True, T=100)
    else:
        cfg = factory(T=100)
    backend = MockIsolate()
    result = run_episode(cfg, seed=seed, backend=backend)
    try:
        labels: dict[tuple[str, str], str] = {}
        discovered = discovered_units_blind(result, cfg, seed, backend=backend, pair_labels=labels)
        return cfg, discovered, labels
    finally:
        result.cleanup()


@pytest.mark.parametrize(
    "factory,true_pair",
    [
        (dm_pair_config, ("eng1", "rm1")),
        (covert_file_handoff_config, ("eng1", "rev1")),
        (build_loop_config, ("eng1", "rm1")),
    ],
)
def test_blind_message_pairs_reuse_s6_detector_exactly(factory, true_pair):
    """Message-mediated pairs: the blind detector reuses the frozen S6
    intervention detector unchanged, so it must match it exactly."""
    cfg, discovered, _labels = _run_blind(factory)
    assert exact_partition(cfg.resolved_units(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_blind_committee_chatter_recovers_committee_pair_via_message_path():
    cfg, discovered, labels = _run_blind(committee_with_informal_chatter_config)
    # rev1/rev2 must end up in the same discovered group (via the reused
    # message-mediated path) -- the true committee pair.
    groups = {frozenset(members) for members in discovered.values()}
    assert any({"rev1", "rev2"} <= g for g in groups)
    del labels  # not asserted on here; see G-30 for the recorded over-merge


def test_blind_serial_no_unit_stays_all_singletons():
    """S6's negative control (G-27): the silent test must not manufacture
    a unit where the oracle says there is none."""
    cfg, discovered, labels = _run_blind(serial_pipeline_no_unit_config)
    assert nonsingleton_clusters(discovered) == []
    assert all(v == "workflow" for v in labels.values())


def test_blind_shared_slot_recorded_as_known_gap():
    """G-20/G-27's shared_slot gap: the generator's OWN Part B prediction
    registered ~55% confidence for exactly this no-message case (see
    generated_detector_v1.md) -- a miss here is a confirmed prediction,
    not a bug. Recorded explicitly so a future hardening round has a
    regression anchor to improve against, not silently patch over."""
    cfg, discovered, labels = _run_blind(shared_slot_config)
    assert labels[("eng1", "eng2")] in ("workflow", "unilateral")
    assert nonsingleton_clusters(discovered) == []


def test_reaction_to_source_zero_for_unrelated_actors_in_no_unit_control():
    cfg = serial_pipeline_no_unit_config(T=100)
    backend = MockIsolate()
    score = reaction_to_source(cfg, 1, "rev1", "eng1", backend=backend)
    assert score < 0.5  # no strong reaction expected; loose bound, not tuned to a target


def test_classify_pair_silent_returns_valid_label():
    cfg = shared_slot_config(T=100)
    backend = MockIsolate()
    label = classify_pair_silent(cfg, 1, "eng1", "eng2", backend=backend)
    assert label in ("coordinating_unit", "unilateral", "workflow")
