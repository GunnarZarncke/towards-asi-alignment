"""Phase 7a-blind scenarios scored under proper UAD / access-UAD (GL-51).

Ground truth from a subagent that never saw oracle_only/ (see
``BLIND_GENERATION.md``). Expectations updated when the discovery
criterion changed from Jaccard+AND-merge to CMI|rest + handle specificity.
"""

from __future__ import annotations

from graded_lab.harness.ecology import (
    three_way_nod_config,
    three_way_nod_programs,
    watched_flag_config,
    watched_flag_programs,
)
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.uad_discovery import discovered_units_uad
from graded_lab.oracle_only.uad_handles import discovered_units_handles
from graded_lab.oracle_only.uad_partition import full_partition_match, nonsingleton_clusters
from graded_lab.world_visible.world import run_episode


def test_watched_flag_handle_uad_recovers():
    """One-way write-triggered behavior switch: access-UAD should recover.

    Passive may miss (no communicate sync); handle specificity allows
    directed freeze evidence — unlike mutual-AND merge.
    """
    cfg = watched_flag_config()
    programs = watched_flag_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)

    passive = discovered_units_uad(result=result, rng_seed=3)
    # Passive recovery is allowed but not required.
    _ = passive

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


def test_three_way_nod_is_registered_negative_for_pairwise_handle_uad():
    """Three-way mutual barrier remains a genuine miss (GL-12 / GL-51).

    Pairwise handle-UAD may recover a proper subset (e.g. one edge of the
    barrier) or nothing; it must not claim exact full-partition recovery
    and must not absorb admin via queue contention. Exact trio recovery
    would require multi-way blanket / handle hypotheses — future work.
    """
    cfg = three_way_nod_config()
    programs = three_way_nod_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)

    passive = discovered_units_uad(result=result, rng_seed=3)
    assert not full_partition_match(cfg.resolved_partition(), passive)

    discovered = discovered_units_handles(
        result,
        cfg,
        seed=3,
        programs=programs,
        backend=backend,
        seed_from_passive=False,
    )
    assert not full_partition_match(cfg.resolved_partition(), discovered)
    for cluster in nonsingleton_clusters(discovered):
        assert "admin1" not in cluster, (
            f"admin over-merge returned (GL-12 failure mode): {discovered!r}"
        )
