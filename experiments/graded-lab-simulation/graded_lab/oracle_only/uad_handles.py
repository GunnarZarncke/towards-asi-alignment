"""Access-model / handle-UAD over graded primitive episodes (GL-51).

Follows ``access-uad`` / ``uad_handles``: interventions are operations on
handles (here: ``program_freeze`` of a host actor's program), not ideal
``do(X=x)``. Discovery scores **agent-loop hypotheses** (which actors
belong in one measurement unit), not mutual freeze-AND of actor pairs.

Merge rule (pre-registered GL-51, before fixture sweeps):

1. Build a directed dependency matrix via freeze probes
   (``dependency_score`` = max(compensation, missing milestone)).
2. An unordered pair {A,B} is a unit edge under the mutual-or-unique
   rule in ``_pair_is_specific_unit`` (mutual distinctive dependence, or
   a unique one-way handoff from a non-cascade hub). Absolute OR-merge
   and mutual-AND-only merge are both rejected — see that helper.
3. Optional: also accept a pair that passive CMI already flagged
   (``seed_from_passive``), so handle tests refine rather than ignore
   observational structure.

Quarantined mutual-AND merge lives in ``attic/freeze_and_merge.py``.
"""

from __future__ import annotations

from itertools import combinations

from ..world_visible.config import EpisodeConfig
from .intervention_diff import diff_probe_triple, run_episode_triple
from .intervention_probes import program_freeze_probe
from .uad_discovery import discovered_units_uad

DEFAULT_MIN_DEPENDENCY = 0.15
# One-way handoffs need a higher floor than mutual pairs: incidental
# softmax coupling on default_lab_config produces ~0.5 one-way scores
# (rev1→rm1) that are not units. Genuine write/read handoffs measure ~0.67+.
DEFAULT_MIN_ONE_WAY_DEPENDENCY = 0.60
DEFAULT_SPECIFICITY_RATIO = 1.25


def _targets_above(
    source: str,
    matrix: dict[tuple[str, str], float],
    actor_ids: list[str],
    *,
    min_dependency: float,
) -> list[str]:
    return [
        x
        for x in actor_ids
        if x != source and matrix.get((source, x), 0.0) >= min_dependency
    ]


def dependency_matrix(
    cfg: EpisodeConfig,
    seed: int,
    actor_ids: list[str],
    programs: dict[str, str],
    *,
    backend=None,
) -> dict[tuple[str, str], float]:
    """Directed freeze→target ``dependency_score`` for every ordered pair."""
    matrix: dict[tuple[str, str], float] = {}
    for source in actor_ids:
        probe = program_freeze_probe(source)
        triple = run_episode_triple(cfg, seed, probe, programs, backend=backend)
        diffs = diff_probe_triple(triple, probe, actor_ids=actor_ids)
        for target in actor_ids:
            if source == target:
                continue
            matrix[(source, target)] = diffs[target].dependency_score
    return matrix


def _pair_is_specific_unit(
    a: str,
    b: str,
    matrix: dict[tuple[str, str], float],
    actor_ids: list[str],
    *,
    min_dependency: float,
    specificity_ratio: float,
    min_one_way_dependency: float = DEFAULT_MIN_ONE_WAY_DEPENDENCY,
) -> bool:
    """Access-UAD pair test (GL-51).

    - **Mutual** freeze dependence (≥ ``min_dependency`` both ways): accept
      when each directed score also clears specificity against other targets
      (committee / sync pairs).
    - **One-way** handoff: accept only when the directed score clears the
      higher ``min_one_way_dependency`` floor, the source has a *unique*
      above-threshold target (not a cascade hub), and specificity holds.

    Absolute-threshold OR-merge is rejected because serial pipelines produce
    many strong one-way scores; mutual-AND is rejected because genuine
    producer→consumer units are directed.
    """
    ab = matrix.get((a, b), 0.0)
    ba = matrix.get((b, a), 0.0)
    if ab < min_dependency and ba < min_dependency:
        return False

    if ab >= min_dependency and ba >= min_dependency:
        # Mutual: each must be a distinctive partner for the other.
        a_others = [matrix.get((a, x), 0.0) for x in actor_ids if x not in (a, b)]
        b_others = [matrix.get((b, x), 0.0) for x in actor_ids if x not in (a, b)]
        a_ok = not a_others or ab >= specificity_ratio * max(a_others)
        b_ok = not b_others or ba >= specificity_ratio * max(b_others)
        return a_ok and b_ok

    # One-way only.
    if ab >= ba:
        source, target, score = a, b, ab
    else:
        source, target, score = b, a, ba
    if score < min_one_way_dependency:
        return False
    hubs = _targets_above(source, matrix, actor_ids, min_dependency=min_dependency)
    if len(hubs) != 1 or hubs[0] != target:
        return False  # cascade hub or wrong unique target
    others = [matrix.get((source, x), 0.0) for x in actor_ids if x not in (source, target)]
    if not others:
        return True
    return score >= specificity_ratio * max(others)


def units_from_handle_matrix(
    actor_ids: list[str],
    matrix: dict[tuple[str, str], float],
    *,
    min_dependency: float = DEFAULT_MIN_DEPENDENCY,
    specificity_ratio: float = DEFAULT_SPECIFICITY_RATIO,
    min_one_way_dependency: float = DEFAULT_MIN_ONE_WAY_DEPENDENCY,
    seed_edges: list[tuple[str, str]] | None = None,
) -> dict[str, tuple[str, ...]]:
    parent = {a: a for a in actor_ids}

    def find(x: str) -> str:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    seed = {tuple(sorted(e)) for e in (seed_edges or [])}
    for a, b in combinations(sorted(actor_ids), 2):
        if (a, b) in seed:
            # Passive CMI|rest already screened shared pipeline phase.
            union(a, b)
            continue
        if _pair_is_specific_unit(
            a,
            b,
            matrix,
            actor_ids,
            min_dependency=min_dependency,
            specificity_ratio=specificity_ratio,
            min_one_way_dependency=min_one_way_dependency,
        ):
            union(a, b)

    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        groups.setdefault(find(a), []).append(a)

    out: dict[str, tuple[str, ...]] = {}
    unit_idx = 1
    assigned: set[str] = set()
    for members in sorted(groups.values(), key=lambda m: (-len(m), m)):
        tup = tuple(sorted(members))
        if len(tup) > 1:
            out[f"unit_{unit_idx}"] = tup
            assigned.update(tup)
            unit_idx += 1
    for a in sorted(actor_ids):
        if a not in assigned:
            out[a] = (a,)
    return out


def discovered_units_handles(
    result,
    cfg: EpisodeConfig,
    seed: int,
    programs: dict[str, str],
    *,
    backend=None,
    min_dependency: float = DEFAULT_MIN_DEPENDENCY,
    specificity_ratio: float = DEFAULT_SPECIFICITY_RATIO,
    seed_from_passive: bool = True,
) -> dict[str, tuple[str, ...]]:
    """Handle-UAD partition: freeze probes + specificity merge (+ optional CMI seed)."""
    actor_ids = sorted(result.boundary_streams)
    seed_edges: list[tuple[str, str]] = []
    if seed_from_passive:
        passive = discovered_units_uad(result=result, rng_seed=seed)
        for members in passive.values():
            if len(members) > 1:
                seed_edges.extend(combinations(sorted(members), 2))
    matrix = dependency_matrix(cfg, seed, actor_ids, programs, backend=backend)
    return units_from_handle_matrix(
        actor_ids,
        matrix,
        min_dependency=min_dependency,
        specificity_ratio=specificity_ratio,
        seed_edges=seed_edges,
    )


# Compatibility name used by older tests / DESIGN text.
def discovered_units_intervention(
    result,
    cfg: EpisodeConfig,
    seed: int,
    programs: dict[str, str],
    *,
    backend=None,
    min_compensation: float = DEFAULT_MIN_DEPENDENCY,
    min_jaccard: float = 0.5,
    candidate_source: str = "passive",
    score_kind: str = "dependency",
    specificity_ratio: float = DEFAULT_SPECIFICITY_RATIO,
) -> dict[str, tuple[str, ...]]:
    """Compatibility wrapper → :func:`discovered_units_handles`.

    ``candidate_source`` / ``score_kind`` / ``min_jaccard`` are accepted for
    call-site compatibility but no longer select the quarantined AND-merge
    path. ``all_pairs`` disables passive CMI seeding; ``passive`` seeds from
    proper UAD. Scoring is always ``dependency_score``.
    """
    del min_jaccard, score_kind  # legacy kwargs
    seed_from_passive = candidate_source != "all_pairs"
    return discovered_units_handles(
        result,
        cfg,
        seed,
        programs,
        backend=backend,
        min_dependency=min_compensation,
        specificity_ratio=specificity_ratio,
        seed_from_passive=seed_from_passive,
    )
