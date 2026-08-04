"""Proper passive UAD over graded primitive traces (GL-51).

Pipeline (UAD paper / ch07 / agency-detect / lab-sim attic ``uad_cmi``):

1. Encode each host actor as a per-tick action-code symbol
   (``primitive_trace``).
2. Propose edges by lag-max **conditional** MI given the joint symbol of
   all other active actors, tested against a circular-shift permutation
   null (screens off shared pipeline phase — the LS-26 / UAD lesson that
   plain pairwise MI cannot).
3. Optionally reject a composite whose Markov-blanket residual J(C)
   fails (``uad_blanket``).

This replaces the quarantined tick-Jaccard / communicate-edge heuristic
in ``attic/coordination_heuristic.py``.
"""

from __future__ import annotations

import math
import random
from itertools import combinations

from .primitive_trace import action_series_from_result, action_series_by_actor
from .uad_blanket import blanket_residual
from .uad_info import lagmax_conditional_mi

DEFAULT_MAX_LAG = 3
DEFAULT_N_SHIFTS = 40
DEFAULT_NULL_QUANTILE = 0.95
# Conservative floor: below this, rest-conditioned CMI on short episodes is
# dominated by residual pipeline coupling (serial_pipeline false merges).
# Directed handoffs that fall below this floor are recovered by access-UAD
# (``uad_handles``), not by raising this until a grower can pass.
DEFAULT_MIN_EFFECT_BITS = 0.3
# Blanket residual is a validation diagnostic; default discovery uses
# CMI|rest edges (lab-sim attic / UAD candidate structure). Set True to
# require J(C)≤ε on every merged pair (stricter; can under-merge short T).
DEFAULT_REQUIRE_BLANKET = False


def _circular_shift(series: list, offset: int) -> list:
    offset %= len(series)
    return series[offset:] + series[:offset]


def _full_partition(actor_ids: list[str], merged: dict[str, tuple[str, ...]]) -> dict[str, tuple[str, ...]]:
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


def cmi_edge_matrix(
    series: dict[str, list[int]],
    *,
    max_lag: int = DEFAULT_MAX_LAG,
    n_shifts: int = DEFAULT_N_SHIFTS,
    null_quantile: float = DEFAULT_NULL_QUANTILE,
    min_effect_bits: float = DEFAULT_MIN_EFFECT_BITS,
    rng_seed: int = 0,
) -> dict[tuple[str, str], float]:
    """Significant lag-max I(A;B|rest) edges (value = observed bits)."""
    actor_ids = sorted(series)
    n_ticks = len(next(iter(series.values()))) if series else 0
    edges: dict[tuple[str, str], float] = {}
    if n_ticks <= 2 * (max_lag + 1):
        return edges

    active = [a for a in actor_ids if len(set(series[a])) > 1]
    rng = random.Random(rng_seed)
    shift_lo, shift_hi = max_lag + 1, n_ticks - max_lag - 1
    if shift_hi <= shift_lo:
        return edges

    for a, b in combinations(active, 2):
        rest_actors = [c for c in active if c not in (a, b)]
        z = (
            list(zip(*[series[c] for c in rest_actors]))
            if rest_actors
            else [0] * n_ticks
        )
        observed = lagmax_conditional_mi(series[a], series[b], z, max_lag=max_lag)
        if observed <= min_effect_bits:
            continue
        null_values = sorted(
            lagmax_conditional_mi(
                series[a],
                _circular_shift(series[b], rng.randint(shift_lo, shift_hi)),
                z,
                max_lag=max_lag,
            )
            for _ in range(n_shifts)
        )
        threshold = null_values[
            min(int(math.ceil(null_quantile * n_shifts)) - 1, n_shifts - 1)
        ]
        if observed > threshold:
            lo, hi = sorted((a, b))
            edges[(lo, hi)] = observed
    return edges


def discovered_units_uad(
    result=None,
    *,
    primitive_log: list[dict] | None = None,
    actor_ids: list[str] | None = None,
    tier: str = "full",
    depth: str = "deep",
    max_lag: int = DEFAULT_MAX_LAG,
    n_shifts: int = DEFAULT_N_SHIFTS,
    null_quantile: float = DEFAULT_NULL_QUANTILE,
    min_effect_bits: float = DEFAULT_MIN_EFFECT_BITS,
    rng_seed: int = 0,
    require_blanket: bool = DEFAULT_REQUIRE_BLANKET,
) -> dict[str, tuple[str, ...]]:
    """Recover a full actor partition via CMI edges (+ optional blanket gate).

    Prefer ``result=`` so idle ``noop`` actors (present only in
    ``boundary_streams``) remain singletons. ``primitive_log`` +
    ``actor_ids`` is accepted for callers that already hold both.
    """
    if result is not None:
        actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(result.boundary_streams)
        series = action_series_from_result(result, actor_ids, depth=depth, tier=tier)
    else:
        if primitive_log is None or actor_ids is None:
            raise ValueError("pass result= or both primitive_log= and actor_ids=")
        actor_ids = sorted(actor_ids)
        series = action_series_by_actor(primitive_log, actor_ids, depth=depth, tier=tier)

    edges = cmi_edge_matrix(
        series,
        max_lag=max_lag,
        n_shifts=n_shifts,
        null_quantile=null_quantile,
        min_effect_bits=min_effect_bits,
        rng_seed=rng_seed,
    )

    parent = {a: a for a in actor_ids}

    def find(x: str) -> str:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a, b in edges:
        if require_blanket:
            score = blanket_residual(series, (a, b), all_actors=actor_ids)
            if not score.passed:
                continue
        union(a, b)

    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        groups.setdefault(find(a), []).append(a)
    merged = {f"g_{i}": tuple(sorted(m)) for i, m in enumerate(groups.values(), start=1)}
    return _full_partition(actor_ids, merged)


# Legacy name used by calibration / older tests — now proper UAD.
def discovered_units_passive(
    primitive_log: list[dict] | None = None,
    actor_ids: list[str] | None = None,
    *,
    result=None,
    tier: str = "full",
    **kwargs,
) -> dict[str, tuple[str, ...]]:
    """Compatibility alias for :func:`discovered_units_uad` (GL-51).

    Historical call shape: ``discovered_units_passive(log, actor_ids=...)``.
    Prefer ``discovered_units_uad(result=...)`` in new code.
    """
    return discovered_units_uad(
        result=result,
        primitive_log=primitive_log,
        actor_ids=actor_ids,
        tier=tier,
        **kwargs,
    )
