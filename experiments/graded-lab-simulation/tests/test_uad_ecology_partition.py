"""Full-partition UAD recovery on every ecology (composites + singletons)."""

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
from graded_lab.oracle_only.uad_intervention import discovered_units_intervention
from graded_lab.oracle_only.uad_partition import full_partition_match
from graded_lab.oracle_only.uad_passive import discovered_units_passive
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.world import default_lab_config, run_episode


def _default_programs(cfg: EpisodeConfig) -> dict[str, str]:
    return {agent.actor_id: "softmax_optimizer" for agent in cfg.agents}


ECOLOGY_CASES = [
    pytest.param(
        "default_softmax",
        default_lab_config,
        _default_programs,
        id="default_softmax",
    ),
    pytest.param(
        "committee",
        committee_config,
        committee_programs,
        id="committee",
    ),
    pytest.param(
        "communicator_pair",
        communicator_pair_config,
        communicator_pair_programs,
        id="communicator_pair",
    ),
    pytest.param(
        "serial_pipeline",
        serial_pipeline_config,
        serial_pipeline_programs,
        id="serial_pipeline",
    ),
    pytest.param(
        "engineer_comm_sync",
        engineer_comm_sync_config,
        engineer_comm_sync_programs,
        id="engineer_comm_sync",
    ),
    pytest.param(
        "cross_role_comm_sync",
        cross_role_comm_sync_config,
        cross_role_comm_sync_programs,
        id="cross_role_comm_sync",
    ),
]


def _discover_passive(result):
    actor_ids = sorted(result.boundary_streams)
    return discovered_units_passive(result.primitive_log, actor_ids=actor_ids)


@pytest.mark.parametrize("name,factory,programs_factory", ECOLOGY_CASES)
def test_passive_full_partition_on_ecology(name, factory, programs_factory):
    cfg = factory()
    programs = programs_factory(cfg) if name == "default_softmax" else programs_factory()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    discovered = _discover_passive(result)
    assert full_partition_match(cfg.resolved_partition(), discovered), (
        f"{name}: expected {cfg.resolved_partition()!r}, got {discovered!r}"
    )


@pytest.mark.parametrize("name,factory,programs_factory", ECOLOGY_CASES)
def test_intervention_full_partition_on_ecology(name, factory, programs_factory):
    cfg = factory()
    programs = programs_factory(cfg) if name == "default_softmax" else programs_factory()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)
    discovered = discovered_units_intervention(
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
    assert full_partition_match(expected, _discover_passive(result))
    assert all(len(members) == 1 for members in expected.values())


def test_boundary_streams_is_required_for_full_actor_roster():
    """Eliding ``boundary_streams`` and deriving the roster from
    ``primitive_log`` actors alone silently drops fully-idle actors: a
    ``noop`` policy never emits a primitive, so it never appears in
    ``primitive_log`` at all, and a discovery pipeline built on that
    roster would never even report it as a (correctly-solitary) singleton.
    ``boundary_streams`` is populated every tick for every live actor
    regardless of whether it acted, so it is the correct source for the
    actor roster (see FINDINGS G-11)."""
    cfg = communicator_pair_config()
    programs = communicator_pair_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    primitive_log_actors = {e.get("actor_id") for e in result.primitive_log}
    boundary_stream_actors = set(result.boundary_streams)
    idle_actors = boundary_stream_actors - primitive_log_actors
    assert idle_actors, "expected at least one fully-idle (noop) actor in this fixture"
    assert idle_actors <= {"eng1", "admin1"}
    discovered = _discover_passive(result)
    discovered_actors = {actor for members in discovered.values() for actor in members}
    assert idle_actors <= discovered_actors, (
        "idle actors must still surface as singletons; a primitive_log-only "
        "roster would drop them from the discovered partition entirely"
    )


def test_signal_handoff_pair_is_a_passive_blind_spot():
    """FINDINGS G-11: a write/read-only coordination channel is invisible
    to every passive signal — passive must NOT report the true unit."""
    cfg = signal_handoff_pair_config()
    programs = signal_handoff_pair_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    discovered = _discover_passive(result)
    assert not full_partition_match(cfg.resolved_partition(), discovered)
    clusters = {frozenset(members) for members in discovered.values()}
    assert frozenset({"eng1"}) in clusters
    assert frozenset({"rev1"}) in clusters
    assert frozenset({"eng1", "rev1"}) not in clusters


def test_signal_handoff_pair_needs_standalone_dependency_scoring():
    """Passive-seeded intervention also misses it (no candidate edge to
    probe); standalone all-pairs + dependency scoring recovers it."""
    from graded_lab.oracle_only.uad_intervention import discovered_units_intervention

    cfg = signal_handoff_pair_config()
    programs = signal_handoff_pair_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)

    passive_seeded = discovered_units_intervention(
        result, cfg, seed=3, programs=programs, backend=backend
    )
    assert not full_partition_match(cfg.resolved_partition(), passive_seeded)

    compensation_only = discovered_units_intervention(
        result, cfg, seed=3, programs=programs, backend=backend,
        candidate_source="all_pairs", score_kind="compensation",
    )
    assert not full_partition_match(cfg.resolved_partition(), compensation_only), (
        "compensation-only scoring is expected to miss a stall-style "
        "dependency (FINDINGS G-11); if this now passes, the metric "
        "changed and this assertion should be revisited."
    )

    dependency_scored = discovered_units_intervention(
        result, cfg, seed=3, programs=programs, backend=backend,
        candidate_source="all_pairs", score_kind="dependency",
    )
    assert full_partition_match(cfg.resolved_partition(), dependency_scored), (
        f"expected {cfg.resolved_partition()!r}, got {dependency_scored!r}"
    )
