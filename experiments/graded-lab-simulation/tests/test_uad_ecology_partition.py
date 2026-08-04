"""Full-partition proper UAD recovery on every ecology (GL-51)."""

from __future__ import annotations

import pytest

from graded_lab.harness.ecology import (
    committee_config,
    committee_programs,
    communicator_pair_config,
    communicator_pair_programs,
    cross_role_comm_sync_config,
    cross_role_comm_sync_programs,
    engineer_comm_sync_config,
    engineer_comm_sync_programs,
    serial_pipeline_config,
    serial_pipeline_programs,
    signal_handoff_pair_config,
    signal_handoff_pair_programs,
)
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.uad_discovery import discovered_units_uad
from graded_lab.oracle_only.uad_handles import discovered_units_handles
from graded_lab.oracle_only.uad_partition import full_partition_match
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.world import default_lab_config, run_episode


def _default_programs(cfg: EpisodeConfig) -> dict[str, str]:
    return {agent.actor_id: "softmax_optimizer" for agent in cfg.agents}


# Passive CMI|rest (conservative floor) recovers sync / communicator / serial
# negatives; committee needs access-UAD (weak rest-conditioned CMI).
PASSIVE_ECOLOGY_CASES = [
    pytest.param("default_softmax", default_lab_config, _default_programs, id="default_softmax"),
    pytest.param(
        "communicator_pair", communicator_pair_config, communicator_pair_programs, id="communicator_pair"
    ),
    pytest.param("serial_pipeline", serial_pipeline_config, serial_pipeline_programs, id="serial_pipeline"),
    pytest.param(
        "engineer_comm_sync", engineer_comm_sync_config, engineer_comm_sync_programs, id="engineer_comm_sync"
    ),
    pytest.param(
        "cross_role_comm_sync",
        cross_role_comm_sync_config,
        cross_role_comm_sync_programs,
        id="cross_role_comm_sync",
    ),
]

HANDLE_ECOLOGY_CASES = PASSIVE_ECOLOGY_CASES + [
    pytest.param("committee", committee_config, committee_programs, id="committee"),
]


@pytest.mark.parametrize("name,factory,programs_factory", PASSIVE_ECOLOGY_CASES)
def test_passive_uad_full_partition_on_ecology(name, factory, programs_factory):
    cfg = factory()
    programs = programs_factory(cfg) if name == "default_softmax" else programs_factory()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    discovered = discovered_units_uad(result=result, rng_seed=3)
    assert full_partition_match(cfg.resolved_partition(), discovered), (
        f"{name}: expected {cfg.resolved_partition()!r}, got {discovered!r}"
    )


@pytest.mark.parametrize("name,factory,programs_factory", HANDLE_ECOLOGY_CASES)
def test_handle_uad_full_partition_on_ecology(name, factory, programs_factory):
    cfg = factory()
    programs = programs_factory(cfg) if name == "default_softmax" else programs_factory()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)
    discovered = discovered_units_handles(
        result, cfg, seed=3, programs=programs, backend=backend
    )
    assert full_partition_match(cfg.resolved_partition(), discovered), (
        f"{name}: expected {cfg.resolved_partition()!r}, got {discovered!r}"
    )


@pytest.mark.parametrize("seed", [3, 7, 11])
def test_default_softmax_all_singletons_across_seeds(seed: int):
    cfg = default_lab_config()
    programs = _default_programs(cfg)
    result = run_episode(cfg, seed=seed, backend=MockIsolate(), programs=programs)
    expected = cfg.resolved_partition()
    assert full_partition_match(expected, discovered_units_uad(result=result, rng_seed=seed))
    assert all(len(members) == 1 for members in expected.values())


def test_boundary_streams_is_required_for_full_actor_roster():
    """Idle noop actors appear only in boundary_streams — roster must use them."""
    cfg = communicator_pair_config()
    programs = communicator_pair_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    primitive_log_actors = {e.get("actor_id") for e in result.primitive_log}
    boundary_stream_actors = set(result.boundary_streams)
    idle_actors = boundary_stream_actors - primitive_log_actors
    assert idle_actors, "expected at least one fully-idle (noop) actor in this fixture"
    assert idle_actors <= {"eng1", "admin1"}
    discovered = discovered_units_uad(result=result, rng_seed=3)
    discovered_actors = {actor for members in discovered.values() for actor in members}
    assert idle_actors <= discovered_actors


def test_signal_handoff_may_be_passive_blind_spot():
    """Write/read handoff can lack rest-conditioned CMI on short episodes.

    Proper UAD does not *require* a miss here (lagged CMI may recover it);
    this test only documents whether passive recovered the unit, and
    asserts singletons when it does not.
    """
    cfg = signal_handoff_pair_config()
    programs = signal_handoff_pair_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    discovered = discovered_units_uad(result=result, rng_seed=3)
    if full_partition_match(cfg.resolved_partition(), discovered):
        return  # lagged CMI recovered it — allowed under proper UAD
    clusters = {frozenset(members) for members in discovered.values()}
    assert frozenset({"eng1"}) in clusters
    assert frozenset({"rev1"}) in clusters


def test_signal_handoff_recovered_by_handle_specificity():
    """Access-UAD: one-way freeze + specificity recovers write/read handoff.

    Replaces the pre-GL-51 claim that mutual-AND + dependency_score was
    required (that path rejected genuine one-way units).
    """
    cfg = signal_handoff_pair_config()
    programs = signal_handoff_pair_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)
    discovered = discovered_units_handles(
        result,
        cfg,
        seed=3,
        programs=programs,
        backend=backend,
        seed_from_passive=False,
    )
    assert full_partition_match(cfg.resolved_partition(), discovered), (
        f"expected {cfg.resolved_partition()!r}, got {discovered!r}"
    )
