"""Phase 7a: intervention-supported unit discovery on primitive traces."""

from __future__ import annotations

from itertools import combinations

from ..world_visible.config import EpisodeConfig
from .intervention_diff import diff_probe_triple, run_episode_triple
from .intervention_probes import Probe, program_freeze_probe
from .uad_passive import discovered_units_passive

DEFAULT_MIN_COMPENSATION = 0.15


def candidate_edges_from_passive(
    result,
    *,
    tier: str = "full",
    min_jaccard: float = 0.5,
) -> list[tuple[str, str]]:
    """Pairs within passive nonsingleton clusters.

    Cheap (no extra episodes) but structurally cannot recover a unit passive
    missed entirely — see ``candidate_edges_all_pairs`` and FINDINGS G-11.
    """
    actor_ids = sorted(result.boundary_streams)
    discovered = discovered_units_passive(
        result.primitive_log, actor_ids=actor_ids, tier=tier, min_jaccard=min_jaccard
    )
    edges: list[tuple[str, str]] = []
    for members in discovered.values():
        if len(members) > 1:
            edges.extend(combinations(sorted(members), 2))
    return sorted(set(edges))


def candidate_edges_all_pairs(result) -> list[tuple[str, str]]:
    """Every actor pair — standalone mode, independent of passive output.

    Costs one probed episode-triple per actor (see ``compensation_matrix``),
    so this is O(n) extra episodes, not O(n^2); each triple yields scores
    against every other actor in one pass.
    """
    actor_ids = sorted(result.boundary_streams)
    return sorted(combinations(actor_ids, 2))


def _full_partition_from_merged(
    actor_ids: list[str], merged: dict[str, tuple[str, ...]]
) -> dict[str, tuple[str, ...]]:
    assigned: set[str] = set()
    out: dict[str, tuple[str, ...]] = {}
    unit_idx = 1
    for members in sorted(merged.values(), key=lambda m: (-len(m), m)):
        if len(members) > 1:
            out[f"unit_{unit_idx}"] = members
            assigned.update(members)
            unit_idx += 1
    for actor in sorted(actor_ids):
        if actor not in assigned:
            out[actor] = (actor,)
    return out


def discovered_units_intervention(
    result,
    cfg: EpisodeConfig,
    seed: int,
    programs: dict[str, str],
    *,
    backend=None,
    min_compensation: float = DEFAULT_MIN_COMPENSATION,
    min_jaccard: float = 0.5,
    candidate_source: str = "passive",
    score_kind: str = "compensation",
) -> dict[str, tuple[str, ...]]:
    """Intervention-supported discovery.

    ``candidate_source="passive"`` (default) only probes pairs passive
    discovery already flagged — cheap, but cannot recover a unit passive
    missed entirely. ``candidate_source="all_pairs"`` probes every actor
    pair directly and does not depend on passive at all (see FINDINGS G-11).

    ``score_kind="compensation"`` (default, matches earlier batteries) only
    rewards *novel* codes appearing under intervention and is blind to an
    actor that keeps repeating its pre-intervention behavior and simply
    never reaches a milestone. ``score_kind="dependency"`` also credits that
    missing-milestone case (``ActorDiffSummary.missing_score``).
    """
    actor_ids = sorted(result.boundary_streams)
    if candidate_source == "all_pairs":
        edges = candidate_edges_all_pairs(result)
    elif candidate_source == "passive":
        edges = candidate_edges_from_passive(result, min_jaccard=min_jaccard)
    else:
        raise ValueError(f"unknown candidate_source: {candidate_source!r}")
    if not edges:
        return {actor: (actor,) for actor in actor_ids}
    matrix = compensation_matrix(
        cfg,
        seed,
        edges,
        programs,
        backend=backend,
        min_compensation=min_compensation,
        score_kind=score_kind,
    )
    merged = units_from_compensation_matrix(edges, matrix, min_compensation=min_compensation)
    return _full_partition_from_merged(actor_ids, merged)


def compensation_matrix(
    cfg: EpisodeConfig,
    seed: int,
    edges: list[tuple[str, str]],
    programs: dict[str, str],
    *,
    backend=None,
    min_compensation: float = DEFAULT_MIN_COMPENSATION,
    score_kind: str = "compensation",
) -> dict[tuple[str, str], float]:
    if score_kind not in ("compensation", "dependency"):
        raise ValueError(f"unknown score_kind: {score_kind!r}")
    actors = sorted({actor for edge in edges for actor in edge})
    matrix: dict[tuple[str, str], float] = {}
    for source in actors:
        probe = program_freeze_probe(source)
        triple = run_episode_triple(cfg, seed, probe, programs, backend=backend)
        diffs = diff_probe_triple(triple, probe, actor_ids=actors)
        for target in actors:
            if source == target:
                continue
            summary = diffs[target]
            score = summary.dependency_score if score_kind == "dependency" else summary.compensation_score
            matrix[(source, target)] = score
    return matrix


def units_from_compensation_matrix(
    edges: list[tuple[str, str]],
    matrix: dict[tuple[str, str], float],
    *,
    min_compensation: float = DEFAULT_MIN_COMPENSATION,
) -> dict[str, tuple[str, ...]]:
    parent: dict[str, str] = {}
    actors = sorted({actor for edge in edges for actor in edge})

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a, b in edges:
        forward = matrix.get((a, b), 0.0)
        backward = matrix.get((b, a), 0.0)
        if forward >= min_compensation and backward >= min_compensation:
            union(a, b)
    groups: dict[str, list[str]] = {}
    for actor in actors:
        root = find(actor)
        groups.setdefault(root, []).append(actor)
    return {f"unit_{i}": tuple(sorted(members)) for i, members in enumerate(groups.values(), start=1)}
