"""Access-UAD / handle-freeze discovery tests — GL-51."""

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
from graded_lab.oracle_only.uad_handles import (
    dependency_matrix,
    discovered_units_handles,
    units_from_handle_matrix,
)
from graded_lab.oracle_only.uad_partition import full_partition_match, nonsingleton_clusters
from graded_lab.world_visible.world import run_episode


def _run_handles(factory, programs_factory, seed: int = 3):
    cfg = factory()
    programs = programs_factory()
    backend = MockIsolate()
    result = run_episode(cfg, seed=seed, backend=backend, programs=programs)
    discovered = discovered_units_handles(
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
def test_handles_exact_on_primary_scenarios(factory, programs_factory, true_pair):
    cfg, discovered = _run_handles(factory, programs_factory)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_handles_negative_control_serial_pipeline():
    cfg, discovered = _run_handles(serial_pipeline_config, serial_pipeline_programs)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == []


def test_specificity_merge_rejects_cascade_style_one_way_edges():
    """Cascade hubs (many above-threshold targets) must not form units."""
    actor_ids = ["eng1", "rev1", "rm1", "admin1"]
    # eng1 and rev1 each hit multiple downstream targets ≥ 0.15.
    matrix = {
        ("eng1", "rev1"): 0.32,
        ("eng1", "rm1"): 0.82,
        ("eng1", "admin1"): 0.10,
        ("rev1", "eng1"): 0.0,
        ("rev1", "rm1"): 0.84,
        ("rev1", "admin1"): 0.20,
            ("rm1", "eng1"): 0.0,
            ("rm1", "rev1"): 0.0,  # keep one-way so mutual path does not fire
            ("rm1", "admin1"): 0.06,
        ("admin1", "eng1"): 0.91,
        ("admin1", "rev1"): 0.33,
        ("admin1", "rm1"): 0.79,
    }
    units = units_from_handle_matrix(
        actor_ids, matrix, min_dependency=0.15, specificity_ratio=1.25, seed_edges=[]
    )
    assert nonsingleton_clusters(units) == []


def test_specificity_merge_accepts_unique_one_way_handoff():
    actor_ids = ["eng1", "rev1", "rm1", "admin1"]
    matrix = {
        ("eng1", "rev1"): 0.67,  # above DEFAULT_MIN_ONE_WAY_DEPENDENCY
        ("eng1", "rm1"): 0.0,
        ("eng1", "admin1"): 0.0,
        ("rev1", "eng1"): 0.0,
        ("rev1", "rm1"): 0.0,
        ("rev1", "admin1"): 0.0,
        ("rm1", "eng1"): 0.0,
        ("rm1", "rev1"): 0.0,
        ("rm1", "admin1"): 0.0,
        ("admin1", "eng1"): 0.0,
        ("admin1", "rev1"): 0.0,
        ("admin1", "rm1"): 0.0,
    }
    units = units_from_handle_matrix(
        actor_ids, matrix, min_dependency=0.15, specificity_ratio=1.25, seed_edges=[]
    )
    assert nonsingleton_clusters(units) == [("eng1", "rev1")]


def test_specificity_merge_rejects_weak_one_way_incidental_coupling():
    """default_softmax-style ~0.55 one-way must not form a unit."""
    actor_ids = ["eng1", "rev1", "rm1", "admin1"]
    matrix = {
        ("rev1", "rm1"): 0.545,
        ("rm1", "rev1"): 0.061,
        ("eng1", "rev1"): 0.0,
        ("eng1", "rm1"): 0.0,
        ("eng1", "admin1"): 0.0,
        ("rev1", "eng1"): 0.0,
        ("rev1", "admin1"): 0.0,
        ("rm1", "eng1"): 0.0,
        ("rm1", "admin1"): 0.0,
        ("admin1", "eng1"): 0.0,
        ("admin1", "rev1"): 0.0,
        ("admin1", "rm1"): 0.0,
    }
    units = units_from_handle_matrix(actor_ids, matrix, seed_edges=[])
    assert nonsingleton_clusters(units) == []


def test_program_freeze_probe_produces_dependency_diff():
    cfg = committee_config(T=60)
    programs = committee_programs()
    probe = program_freeze_probe("rev1")
    triple = run_episode_triple(cfg, 3, probe, programs, backend=MockIsolate())
    diffs = diff_probe_triple(triple, probe)
    assert "rev2" in diffs
    assert diffs["rev2"].dependency_score >= 0.0


def test_dependency_matrix_covers_all_ordered_pairs():
    cfg = communicator_pair_config(T=40)
    programs = communicator_pair_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)
    actors = sorted(result.boundary_streams)
    matrix = dependency_matrix(cfg, 3, actors, programs, backend=backend)
    assert len(matrix) == len(actors) * (len(actors) - 1)
