"""S6 phases 3 and 5: intervention-supported unit discovery."""

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
from lab_sim.oracle_only.uad_intervention import (
    candidate_edges_for_intervention,
    discovered_units_intervention,
    units_from_compensation_matrix,
)
from lab_sim.oracle_only.uad_partition import exact_partition, nonsingleton_clusters
from lab_sim.world_visible.world import run_episode


def _run_intervention(factory, seed: int = 1):
    if factory is covert_file_handoff_config:
        cfg = factory(trusting=True, T=100)
    else:
        cfg = factory(T=100)
    backend = MockIsolate()
    result = run_episode(cfg, seed=seed, backend=backend)
    try:
        discovered = discovered_units_intervention(result, cfg, seed, backend=backend)
        return cfg, discovered
    finally:
        result.cleanup()


@pytest.mark.parametrize(
    "factory,true_pair",
    [
        (dm_pair_config, ("eng1", "rm1")),
        (covert_file_handoff_config, ("eng1", "rev1")),
        (committee_with_informal_chatter_config, ("rev1", "rev2")),
        (build_loop_config, ("eng1", "rm1")),
    ],
)
def test_intervention_exact_on_primary_scenarios(factory, true_pair):
    cfg, discovered = _run_intervention(factory)
    assert exact_partition(cfg.resolved_units(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_intervention_does_not_merge_shared_slot():
    cfg, discovered = _run_intervention(shared_slot_config)
    assert nonsingleton_clusters(discovered) == []


def test_intervention_negative_control_serial_pipeline():
    cfg, discovered = _run_intervention(serial_pipeline_no_unit_config)
    assert nonsingleton_clusters(discovered) == []


def test_units_from_compensation_matrix_mutual_and_asymmetric():
    edges = [("a", "b"), ("b", "c")]
    matrix = {
        ("a", "b"): 0.2,
        ("b", "a"): 0.2,
        ("a", "c"): 0.0,
        ("c", "a"): 0.0,
        ("b", "c"): 0.3,
        ("c", "b"): 0.0,
    }
    units = units_from_compensation_matrix(edges, matrix, min_compensation=0.15)
    assert ("a", "b") in units.values()
    assert ("b", "c") not in units.values()  # mutual-only in this helper


def test_candidate_edges_use_deep_heuristic_only():
    cfg = dm_pair_config(T=100)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        edges = candidate_edges_for_intervention(result)
        assert edges == [("eng1", "rm1")]
    finally:
        result.cleanup()
