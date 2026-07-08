"""S6 first step (user-directed, recorded 2026-07-07): a custom,
standalone actor-level conditional-MI unit detector implementing the
three "easy fixes" the G-26 diagnosis named — replacing all three
design decisions that made the vendored `uad_core` detector over-merge
(G-24/G-25), while staying a PASSIVE trace detector (the
intervention-supported successor is planned separately, see PLAN.md
"S6 — intervention-supported UAD").

The three fixes, mapped to G-26's three causes:

1. **Actor-level, not variable-level, clustering** (G-26 cause 1b: the
   vendored detector's globally-normalized variable distances were
   dominated by within-actor `.tool`↔`.ok` redundancy). Each actor is
   ONE unit of analysis: its per-tick symbol is the TUPLE of all its
   trace variables, so within-actor redundancy cannot generate merges
   at all — it just makes the actor's own alphabet richer.
2. **Conditional MI edge weights** (G-26 cause 2: pipeline phase is a
   common cause; plain pairwise MI cannot tell "coupled through the
   shared pipeline" from "coupled through a private channel"). The
   edge weight between actors A and B is lag-max I(A; B | rest) where
   `rest` is the joint symbol of ALL other active actors — exactly the
   statistic that separated true pairs from pipeline neighbors in the
   G-26 diagnosis (shared_slot: eng1–eng2 kept 0.26 bits conditioned
   while eng1–rm1 collapsed to 0.04).
3. **A data-driven stopping rule instead of a hard cluster count**
   (G-26 cause 1a: `n_agents` forced merges regardless of the matrix).
   An edge exists iff its observed conditional MI exceeds BOTH a
   circular-shift permutation null (the same statistic recomputed with
   B's series circularly shifted, 95th percentile over `n_shifts`
   shifts — adaptive to each pair's own baseline, including the
   everything-is-periodic-at-temperature-0 baseline) AND a small fixed
   effect floor (`min_effect_bits`, estimator-noise guard). Units are
   the connected components of significant edges. No target count
   anywhere.

Pre-registration discipline (AGENTS.md: inputs fixed first, conclusions
never baked into definitions): the defaults below (`n_shifts=40`,
`null_quantile=0.95`, `min_effect_bits=0.1`, `max_lag=3`) were chosen
BEFORE running the scenario sweep, from generic estimator-noise
reasoning, not tuned to reproduce a target verdict; the sweep script
reports whatever they yield, including failures.

Standalone by design: no import from the vendored `uad_core` package —
this module carries its own ~10-line entropy/MI helpers so the vendored
code can be deleted wholesale once the S6 line supersedes it, without
this detector breaking. It DOES reuse `uad_mi.build_lab_trace` (our own
adapter, not vendored) so both detectors read the identical trace and
stay comparable at both depths.

Same recorded-referee-extension status as `uad_mi.py`: own module, own
docstring, never touches frozen code; reads only `AuditView` structure
(full tier suffices); `LabConfig.units` ground truth is read only by
scoring in run scripts, never here.

Known approximation (recorded, not hidden): for a lagged pair
(A_t, B_{t+tau}) the conditioning symbol is `rest` at time t (the
EARLIER index). Conditioning at both endpoints would square the
conditioning alphabet against T~100 samples; the permutation null uses
the SAME alignment, so the estimator bias largely cancels in the
test even though the point estimate is approximate.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Sequence

from .uad_mi import build_lab_trace

DEFAULT_N_SHIFTS = 40
DEFAULT_NULL_QUANTILE = 0.95
DEFAULT_MIN_EFFECT_BITS = 0.1
DEFAULT_MAX_LAG = 3


def _entropy(keys: Sequence) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def conditional_mi(x: Sequence, y: Sequence, z: Sequence) -> float:
    """I(X;Y|Z) = H(X,Z) + H(Y,Z) - H(X,Y,Z) - H(Z), plug-in estimate."""
    if not (len(x) == len(y) == len(z)) or len(x) == 0:
        return 0.0
    return max(
        0.0,
        _entropy(list(zip(x, z)))
        + _entropy(list(zip(y, z)))
        - _entropy(list(zip(x, y, z)))
        - _entropy(list(z)),
    )


def lagmax_conditional_mi(x: Sequence, y: Sequence, z: Sequence, *, max_lag: int) -> float:
    """Max over lags tau in [-max_lag, max_lag] of I(x_t; y_{t+tau} | z_t).
    Same lag convention as the vendored `lagmax_mi`, with the
    conditioning symbol aligned to x's index (see module docstring)."""
    best = conditional_mi(x, y, z)
    for tau in range(1, max_lag + 1):
        if tau >= len(x):
            break
        best = max(best, conditional_mi(x[:-tau], y[tau:], z[:-tau]))
        best = max(best, conditional_mi(x[tau:], y[:-tau], z[tau:]))
    return best


def actor_symbol_series(
    trace: list[dict[str, int]], var_to_actor: dict[str, str]
) -> dict[str, list[tuple]]:
    """One composite per-tick symbol per actor: the tuple of all that
    actor's trace variables (sorted by variable name for determinism).
    This is fix 1 — within-actor variable redundancy becomes alphabet
    richness instead of a spurious merge signal."""
    by_actor: dict[str, list[str]] = {}
    for var, actor in var_to_actor.items():
        by_actor.setdefault(actor, []).append(var)
    return {
        actor: [tuple(row[v] for v in sorted(variables)) for row in trace]
        for actor, variables in by_actor.items()
    }


def _circular_shift(series: list, offset: int) -> list:
    offset %= len(series)
    return series[offset:] + series[:offset]


def discovered_units_cmi(
    result,
    actor_ids: list[str] | None = None,
    tier: str = "full",
    depth: str = "deep",
    horizon: int | None = None,
    max_lag: int = DEFAULT_MAX_LAG,
    n_shifts: int = DEFAULT_N_SHIFTS,
    null_quantile: float = DEFAULT_NULL_QUANTILE,
    min_effect_bits: float = DEFAULT_MIN_EFFECT_BITS,
    rng_seed: int = 0,
) -> dict[str, tuple[str, ...]]:
    """Same return shape as ``uad.discovered_units`` /
    ``uad_mi.discovered_units_mi`` (``{coalition_id: tuple of
    actor_ids}``), so all three detectors score through the identical
    ``uad_score`` path. Deterministic for a fixed ``rng_seed`` (the
    permutation null uses its own seeded ``random.Random``).

    Edge test, per actor pair (A, B) with `rest` = joint symbol of all
    OTHER active actors: significant iff

        observed > quantile(null, null_quantile)  AND
        observed > min_effect_bits

    where observed = lag-max I(A; B | rest) and null re-computes the
    same statistic with B's whole composite series circularly shifted
    by ``n_shifts`` random offsets drawn from [max_lag+1, T-max_lag-1]
    (outside the lag window, so a shifted copy cannot re-align).
    Inactive actors (constant series) are singletons by construction —
    a constant has zero (conditional) MI with anything."""
    from ..detectors import build_audit_view

    view = build_audit_view(result, tier)
    actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(result.host.roles)
    trace, var_to_actor = build_lab_trace(
        view.tool_events, actor_ids, access_log=view.access_log, horizon=horizon, depth=depth
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

    n_ticks = len(trace)
    if n_ticks > 2 * (max_lag + 1):
        series = actor_symbol_series(trace, var_to_actor)
        active = [a for a in actor_ids if len(set(series[a])) > 1]
        rng = random.Random(rng_seed)
        shift_lo, shift_hi = max_lag + 1, n_ticks - max_lag - 1

        for i, a in enumerate(active):
            for b in active[i + 1 :]:
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
                    union(a, b)

    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        groups.setdefault(find(a), []).append(a)
    return {min(members): tuple(sorted(members)) for members in groups.values()}
