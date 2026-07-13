"""Phase 7a intervention-supported UAD tests."""

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
from graded_lab.oracle_only.intervention_diff import diff_probe_triple, run_episode_triple
from graded_lab.oracle_only.intervention_probes import program_freeze_probe
from graded_lab.oracle_only.uad_intervention import (
    candidate_edges_from_passive,
    discovered_units_intervention,
    units_from_compensation_matrix,
)
from graded_lab.oracle_only.uad_partition import full_partition_match, nonsingleton_clusters
from graded_lab.world_visible.world import run_episode


def _run_intervention(factory, programs_factory, seed: int = 3):
    cfg = factory()
    programs = programs_factory()
    backend = MockIsolate()
    result = run_episode(cfg, seed=seed, backend=backend, programs=programs)
    discovered = discovered_units_intervention(
        result, cfg, seed, programs, backend=backend
    )
    return cfg, discovered


@pytest.mark.parametrize(
    "factory,programs_factory,true_pair",
    [
        (committee_config, committee_programs, ("rev1", "rev2")),
        (communicator_pair_config, communicator_pair_programs, ("rev1", "rm1")),
    ],
)
def test_intervention_exact_on_primary_scenarios(factory, programs_factory, true_pair):
    cfg, discovered = _run_intervention(factory, programs_factory)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_intervention_negative_control_serial_pipeline():
    cfg, discovered = _run_intervention(serial_pipeline_config, serial_pipeline_programs)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == []


def test_units_from_compensation_matrix_mutual_only():
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
    assert ("b", "c") not in units.values()


def test_candidate_edges_from_committee_passive_skeleton():
    cfg = committee_config()
    programs = committee_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    edges = candidate_edges_from_passive(result)
    assert ("rev1", "rev2") in edges


def test_program_freeze_probe_produces_compensation_diff():
    cfg = committee_config(T=60)
    programs = committee_programs()
    probe = program_freeze_probe("rev1")
    triple = run_episode_triple(cfg, 3, probe, programs, backend=MockIsolate())
    diffs = diff_probe_triple(triple, probe)
    assert "rev2" in diffs
