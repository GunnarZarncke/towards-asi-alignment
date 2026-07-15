"""Historical tests for the quarantined Jaccard/communicate heuristic.

These assert the *old* detector's behavior, not proper UAD. Skipped from
default suite discovery unless explicitly collected under tests/attic.
"""

from __future__ import annotations

import pytest

from graded_lab.harness.ecology import (
    committee_config,
    committee_programs,
    communicator_pair_config,
    communicator_pair_programs,
    serial_pipeline_config,
    serial_pipeline_programs,
)
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.attic.coordination_heuristic import (
    co_activity_matrix,
    discovered_units_passive,
)
from graded_lab.oracle_only.uad_partition import full_partition_match, nonsingleton_clusters
from graded_lab.world_visible.world import run_episode

pytestmark = pytest.mark.attic


def _run(factory, programs_factory, seed: int = 3):
    cfg = factory()
    programs = programs_factory()
    result = run_episode(cfg, seed=seed, backend=MockIsolate(), programs=programs)
    return cfg, result, programs


@pytest.mark.parametrize(
    "factory,programs_factory,true_pair",
    [
        (committee_config, committee_programs, ("rev1", "rev2")),
        (communicator_pair_config, communicator_pair_programs, ("rev1", "rm1")),
    ],
)
def test_heuristic_finds_primary_units(factory, programs_factory, true_pair):
    cfg, result, _ = _run(factory, programs_factory)
    actor_ids = sorted(result.boundary_streams)
    discovered = discovered_units_passive(result.primitive_log, actor_ids=actor_ids)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_heuristic_negative_control_serial_pipeline():
    cfg, result, _ = _run(serial_pipeline_config, serial_pipeline_programs)
    actor_ids = sorted(result.boundary_streams)
    discovered = discovered_units_passive(result.primitive_log, actor_ids=actor_ids)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == []


def test_co_activity_matrix_finds_communicator_pair():
    _, result, _ = _run(communicator_pair_config, communicator_pair_programs)
    matrix = co_activity_matrix(result.primitive_log, kind="communicate")
    assert matrix.get(("rev1", "rm1"), 0.0) >= 0.5
