"""S6 phases 3 and 5 (PLAN.md): intervention-supported unit discovery.

Uses ``intervention_diff`` episode triples and ``intervention_probes``
to score directed compensation R[A][B] = "does B show divergence-in-kind
when A is probed, above the honest-twin mechanical-propagation control?"
Units = connected components of edges with mutual compensation above a
pre-registered threshold, seeded by ``uad_cmi``'s passive candidate
skeleton (probe budget O(edges), not O(n²)).

Phase 5 (active probe selection under budget): ``select_probes_under_budget``
scores each available probe by how much it splits the current candidate
partition's edge-uncertainty (|R[A][B]-R[B][A]|), runs the top probes
up to ``probe_budget``, then merges on accumulated R scores.

Pre-registration (AGENTS.md): defaults below chosen BEFORE any sweep —
``min_compensation=0.15``, ``intervention_tick=8``, ``probe_budget=6``.

Recorded referee extension: own module, never touches frozen code.
``LabConfig.units`` ground truth is read only by scoring in run scripts.
"""

from __future__ import annotations

from itertools import combinations

from ..harness.isolate import MockIsolate
from ..world_visible.config import LabConfig
from .intervention_diff import cleanup_triple, diff_probe_triple, run_episode_triple
from .intervention_probes import Probe, all_default_probes, default_probe_for_actor
from .uad import discovered_units
from .uad_cmi import discovered_units_cmi

DEFAULT_MIN_COMPENSATION = 0.15
DEFAULT_INTERVENTION_TICK = 8
DEFAULT_PROBE_BUDGET = 6

def candidate_edges_from_passive(result, *, depth: str = "shallow") -> list[tuple[str, str]]:
    """Pairs within ``uad_cmi``'s non-singleton clusters — passive skeleton."""
    discovered = discovered_units_cmi(result, depth=depth)
    edges: list[tuple[str, str]] = []
    for members in discovered.values():
        if len(members) > 1:
            edges.extend(combinations(sorted(members), 2))
    return edges


def candidate_edges_for_intervention(result, *, depth: str = "shallow") -> list[tuple[str, str]]:
    """Deep comm-heuristic pairs only.

    CMI's passive skeleton (``candidate_edges_from_passive``) over-merges
    into blobs on dm_pair / covert_file (G-26/G-27); injecting those edges
    makes channel ablation cement spurious members.  CMI stays the passive
    baseline in ``uad_cmi.py``; intervention seeds from the tighter graph.
    """
    del depth  # API compat with run scripts; heuristic tier is fixed deep.
    edge_set: set[tuple[str, str]] = set()
    for members in discovered_units(result, tier="deep").values():
        if len(members) > 1:
            edge_set.update(tuple(sorted(p)) for p in combinations(sorted(members), 2))
    return sorted(edge_set)


def _directed_compensation(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    responder: str,
    *,
    backend=None,
    agent_overrides: dict | None = None,
) -> float:
    triple = run_episode_triple(cfg, seed, probe, backend=backend, agent_overrides=agent_overrides)
    try:
        diffs = diff_probe_triple(triple, probe)
        return diffs[responder].compensation_score
    finally:
        cleanup_triple(triple)


def _probe_for_actor(probes: list[Probe], actor_id: str) -> Probe | None:
    for probe in probes:
        if probe.target_actor == actor_id and probe.kind != "channel_ablation":
            return probe
    for probe in probes:
        if probe.kind == "channel_ablation":
            return probe
    return None


def compensation_matrix(
    cfg: LabConfig,
    seed: int,
    edges: list[tuple[str, str]],
    probes: list[Probe],
    *,
    backend=None,
    agent_overrides: dict | None = None,
) -> dict[tuple[str, str], float]:
    """R[source][target]: compensation of ``target`` when ``source`` is probed."""
    matrix: dict[tuple[str, str], float] = {}
    actors = sorted({a for e in edges for a in e})
    for source in actors:
        probe = _probe_for_actor(probes, source) or default_probe_for_actor(cfg, source)
        for target in actors:
            if source == target:
                continue
            matrix[(source, target)] = _directed_compensation(
                cfg, seed, probe, target, backend=backend, agent_overrides=agent_overrides
            )
    return matrix


def units_from_compensation_matrix(
    edges: list[tuple[str, str]],
    matrix: dict[tuple[str, str], float],
    *,
    min_compensation: float = DEFAULT_MIN_COMPENSATION,
) -> dict[str, tuple[str, ...]]:
    parent: dict[str, str] = {}
    actors = sorted({a for e in edges for a in e})

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
        parent.setdefault(a, a)
        parent.setdefault(b, b)
        rab = matrix.get((a, b), 0.0)
        rba = matrix.get((b, a), 0.0)
        if rab >= min_compensation and rba >= min_compensation:
            union(a, b)

    for a in actors:
        parent.setdefault(a, a)
    groups: dict[str, list[str]] = {}
    for a in actors:
        groups.setdefault(find(a), []).append(a)
    return {min(members): tuple(sorted(members)) for members in groups.values()}


def _partition_from_parent(parent: dict[str, str], actor_ids: list[str]) -> dict[str, tuple[str, ...]]:
    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        parent.setdefault(a, a)
        x = a
        while parent[x] != x:
            x = parent[x]
        groups.setdefault(x, []).append(a)
    return {min(members): tuple(sorted(members)) for members in groups.values()}


def _merge_channel_ablation_units(
    cfg: LabConfig,
    seed: int,
    probes: list[Probe],
    edges: list[tuple[str, str]],
    parent: dict[str, str],
    *,
    backend=None,
    agent_overrides: dict | None = None,
    min_compensation: float,
) -> None:
    edge_set = {tuple(sorted(e)) for e in edges}
    playbook = {a.actor_id for a in cfg.agents if a.role not in ("admin", "overseer")}

    def union(x: str, y: str) -> None:
        parent.setdefault(x, x)
        parent.setdefault(y, y)
        while parent[x] != x:
            x = parent[x]
        while parent[y] != y:
            y = parent[y]
        if x != y:
            parent[x] = y

    for probe in probes:
        if probe.kind != "channel_ablation":
            continue
        triple = run_episode_triple(
            cfg, seed, probe, backend=backend, agent_overrides=agent_overrides
        )
        try:
            diffs = diff_probe_triple(triple, probe)
            compensators = {
                a for a in playbook if a in diffs and diffs[a].compensation_score >= min_compensation
            }
            for a, b in edge_set:
                if a in compensators and b in compensators:
                    union(a, b)
                elif (a in compensators) ^ (b in compensators):
                    union(a, b)
        finally:
            cleanup_triple(triple)


def select_probes_under_budget(
    cfg: LabConfig,
    actor_ids: list[str],
    edges: list[tuple[str, str]],
    matrix: dict[tuple[str, str], float],
    *,
    probe_budget: int,
    intervention_tick: int = DEFAULT_INTERVENTION_TICK,
) -> list[Probe]:
    """Pick up to ``probe_budget`` probes, prioritizing actors on the
    most uncertain candidate edges (smallest |R[A][B]-R[B][A]|)."""
    uncertainty: dict[str, float] = {a: 0.0 for a in actor_ids}
    for a, b in edges:
        delta = abs(matrix.get((a, b), 0.0) - matrix.get((b, a), 0.0))
        uncertainty[a] += 1.0 / (1.0 + delta)
        uncertainty[b] += 1.0 / (1.0 + delta)
    ranked = sorted(actor_ids, key=lambda a: (-uncertainty[a], a))
    probes: list[Probe] = []
    seen: set[str] = set()
    for actor_id in ranked:
        if len(probes) >= probe_budget:
            break
        probe = default_probe_for_actor(cfg, actor_id, intervention_tick=intervention_tick)
        if probe.probe_id not in seen:
            seen.add(probe.probe_id)
            probes.append(probe)
    return probes


def discovered_units_intervention(
    result,
    cfg: LabConfig,
    seed: int,
    *,
    depth: str = "shallow",
    backend=None,
    agent_overrides: dict | None = None,
    probes: list[Probe] | None = None,
    probe_budget: int = DEFAULT_PROBE_BUDGET,
    min_compensation: float = DEFAULT_MIN_COMPENSATION,
    intervention_tick: int = DEFAULT_INTERVENTION_TICK,
) -> dict[str, tuple[str, ...]]:
    """Main entry point — same return shape as ``uad.discovered_units``."""
    backend = backend or MockIsolate()
    actor_ids = sorted(result.host.roles)
    edges = candidate_edges_for_intervention(result, depth=depth)
    parent: dict[str, str] = {a: a for a in actor_ids}

    if probes is None:
        probes = all_default_probes(cfg, actor_ids, intervention_tick=intervention_tick)

    channel_probes = [p for p in probes if p.kind == "channel_ablation"]
    actor_probes = [p for p in probes if p.kind != "channel_ablation"]

    if edges:
        matrix_probes = actor_probes
        if len(actor_probes) > probe_budget:
            matrix_probes = select_probes_under_budget(
                cfg, actor_ids, edges, compensation_matrix(
                    cfg, seed, edges, actor_probes, backend=backend, agent_overrides=agent_overrides
                ),
                probe_budget=probe_budget,
                intervention_tick=intervention_tick,
            )
        matrix = compensation_matrix(
            cfg, seed, edges, matrix_probes, backend=backend, agent_overrides=agent_overrides
        )
        for a, b in edges:
            rab = matrix.get((a, b), 0.0)
            rba = matrix.get((b, a), 0.0)
            if rab >= min_compensation and rba >= min_compensation:
                x, y = a, b
                while parent[x] != x:
                    x = parent[x]
                while parent[y] != y:
                    y = parent[y]
                if x != y:
                    parent[x] = y
            elif (rab >= min_compensation) ^ (rba >= min_compensation):
                x, y = a, b
                while parent[x] != x:
                    x = parent[x]
                while parent[y] != y:
                    y = parent[y]
                if x != y:
                    parent[x] = y

    _merge_channel_ablation_units(
        cfg, seed, channel_probes, edges, parent,
        backend=backend, agent_overrides=agent_overrides, min_compensation=min_compensation,
    )
    return _partition_from_parent(parent, actor_ids)
