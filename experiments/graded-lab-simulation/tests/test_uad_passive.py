"""Proper passive UAD (CMI|rest) tests — GL-51."""

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
from graded_lab.oracle_only.uad_blanket import blanket_residual
from graded_lab.oracle_only.uad_discovery import discovered_units_uad
from graded_lab.oracle_only.uad_partition import full_partition_match, nonsingleton_clusters
from graded_lab.oracle_only.primitive_trace import action_series_from_result
from graded_lab.world_visible.world import run_episode


def _run(factory, programs_factory, seed: int = 3):
    cfg = factory()
    programs = programs_factory()
    result = run_episode(cfg, seed=seed, backend=MockIsolate(), programs=programs)
    return cfg, result, programs


@pytest.mark.parametrize(
    "factory,programs_factory,true_pair",
    [
        # Committee reviewers are below the conservative CMI floor on short
        # episodes — recovered by access-UAD (see test_uad_intervention).
        (communicator_pair_config, communicator_pair_programs, ("rev1", "rm1")),
    ],
)
def test_uad_finds_primary_units(factory, programs_factory, true_pair):
    cfg, result, _ = _run(factory, programs_factory)
    discovered = discovered_units_uad(result=result, rng_seed=3)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_committee_is_passive_miss_under_conservative_cmi_floor():
    """Documented GL-51 tradeoff: min_effect_bits=0.3 rejects serial
    false merges and also drops the committee's weak rest-conditioned CMI."""
    cfg, result, _ = _run(committee_config, committee_programs)
    discovered = discovered_units_uad(result=result, rng_seed=3)
    assert nonsingleton_clusters(discovered) == []
    assert not full_partition_match(cfg.resolved_partition(), discovered)


def test_uad_negative_control_serial_pipeline():
    cfg, result, _ = _run(serial_pipeline_config, serial_pipeline_programs)
    discovered = discovered_units_uad(result=result, rng_seed=3)
    assert full_partition_match(cfg.resolved_partition(), discovered)
    assert nonsingleton_clusters(discovered) == []


def test_blanket_residual_reports_structure_on_communicator_pair():
    _, result, _ = _run(communicator_pair_config, communicator_pair_programs)
    series = action_series_from_result(result)
    score = blanket_residual(series, ("rev1", "rm1"), all_actors=sorted(series))
    assert score.residual_bits >= 0.0
    assert score.roles.environment
