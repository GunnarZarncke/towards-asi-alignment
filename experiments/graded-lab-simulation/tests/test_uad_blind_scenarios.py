"""Phase 7a-blind: frozen UAD scored against blindly-designed scenarios.

Ground truth and scenario descriptions come from a subagent that never saw
`oracle_only/`, `DESIGN.md`, `FINDINGS.md`, or the golden ecologies (see
`BLIND_GENERATION.md` Phase 7a-blind and
`graded_lab/harness/blind_scenarios_v1.md`). Results here are reported
honestly, including misses predicted in the registered predictions.

Of the 4 designer scenarios, 2 (`quiet-handoff`, `mailbox-tempo`) are not
implementable in this substrate without adding new host mechanics (see
FINDINGS GL-12) and are not run; this file covers the 2 that were.
"""

from __future__ import annotations

from graded_lab.harness.ecology import (
    three_way_nod_config,
    three_way_nod_programs,
    watched_flag_config,
    watched_flag_programs,
)
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.uad_intervention import discovered_units_intervention
from graded_lab.oracle_only.uad_partition import full_partition_match
from graded_lab.oracle_only.uad_passive import discovered_units_passive
from graded_lab.world_visible.world import run_episode


def test_watched_flag_passive_misses_and_intervention_recovers():
    """Matches registered prediction 2: a non-communicate coordination
    channel is a passive blind spot; standalone dependency-scored
    intervention recovers it."""
    cfg = watched_flag_config()
    programs = watched_flag_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)
    actor_ids = sorted(result.boundary_streams)

    passive = discovered_units_passive(result.primitive_log, actor_ids=actor_ids)
    assert not full_partition_match(cfg.resolved_partition(), passive)

    discovered = discovered_units_intervention(
        result, cfg, seed=3, programs=programs, backend=backend,
        candidate_source="all_pairs", score_kind="dependency",
    )
    assert full_partition_match(cfg.resolved_partition(), discovered), (
        f"expected {cfg.resolved_partition()!r}, got {discovered!r}"
    )


def test_three_way_nod_is_a_genuine_miss_for_both_methods():
    """Registered prediction 4 explicitly did not promise 100% recovery.
    Passive misses the mutual three-way barrier entirely (no pairwise
    signal it tracks fires across all three). Standalone dependency-scored
    intervention also fails here, but for a different and instructive
    reason: it *does* detect the trio's mutual dependency, but also
    absorbs the admin actor, which is causally coupled through ordinary
    capability-queue contention, not through the joint-approval mechanism.
    Recorded as a negative result (FINDINGS GL-12), not patched by
    excluding admin post hoc."""
    cfg = three_way_nod_config()
    programs = three_way_nod_programs()
    backend = MockIsolate()
    result = run_episode(cfg, seed=3, backend=backend, programs=programs)
    actor_ids = sorted(result.boundary_streams)

    passive = discovered_units_passive(result.primitive_log, actor_ids=actor_ids)
    assert not full_partition_match(cfg.resolved_partition(), passive)

    discovered = discovered_units_intervention(
        result, cfg, seed=3, programs=programs, backend=backend,
        candidate_source="all_pairs", score_kind="dependency",
    )
    assert not full_partition_match(cfg.resolved_partition(), discovered)
    clusters = {frozenset(members) for members in discovered.values()}
    trio = frozenset({"eng_marlowe", "rev_saito", "rm_okafor"})
    over_merged = frozenset({"eng_marlowe", "rev_saito", "rm_okafor", "admin1"})
    assert trio in clusters or over_merged in clusters, (
        f"expected the trio to at least be merged (possibly with admin1 "
        f"over-merged in), got {discovered!r}"
    )
