"""Markov-blanket residual scoring for candidate actor clusters (GL-51).

Proper UAD accepts a candidate C when the boundary residual
J(C) = I(I_{t+1}; E_{t+1} | S_t, A_t) is small (ch07 / UAD paper /
``agency_detect.markov_blanket``).

In graded-lab the observables are per-actor action-code series. Within a
candidate cluster we classify members into soft S/A/I roles by env-MI and
future-MI heuristics (same spirit as ``agency_detect``), then estimate
J(C). A composite that fails the residual check is not reported as a
unit even if pairwise coupling heuristics fire.
"""

from __future__ import annotations

from dataclasses import dataclass

from .uad_info import conditional_mi, mutual_info

# Pre-registered (GL-51): finite-sample CMI on short episodes is noisy;
# tolerance is intentionally loose relative to agency-detect's discrete
# ε=1.0 nats — we work in bits and short T. Chosen before fixture sweeps
# as an estimator-noise floor, not tuned to pass a target partition.
DEFAULT_BLANKET_TOLERANCE_BITS = 0.35
MIN_INTERNAL_FOR_COMPOSITE = 1


@dataclass(frozen=True)
class RolePartition:
    sensors: tuple[str, ...]
    actions: tuple[str, ...]
    internals: tuple[str, ...]
    environment: tuple[str, ...]


@dataclass(frozen=True)
class BlanketScore:
    residual_bits: float
    roles: RolePartition
    passed: bool
    detail: str


def classify_roles(
    series: dict[str, list[int]],
    cluster: tuple[str, ...],
    *,
    all_actors: list[str] | None = None,
) -> RolePartition:
    """Heuristic S/A/I assignment inside ``cluster`` (agency_detect-style)."""
    members = list(cluster)
    env = [a for a in (all_actors or sorted(series)) if a not in members]
    if len(members) == 1:
        return RolePartition(sensors=(), actions=(), internals=(members[0],), environment=tuple(env))

    n = len(next(iter(series.values())))
    if n < 3:
        return RolePartition(sensors=(), actions=tuple(members), internals=(), environment=tuple(env))

    env_mi: dict[str, float] = {}
    future_mi: dict[str, float] = {}
    for a in members:
        env_mi[a] = 0.0
        for e in env:
            env_mi[a] += mutual_info(series[a], series[e])
        future_mi[a] = 0.0
        for b in members:
            if a == b:
                continue
            future_mi[a] += mutual_info(series[a][:-1], series[b][1:])

    env_vals = sorted(env_mi.values())
    fut_vals = sorted(future_mi.values())
    env_thr = env_vals[max(0, len(env_vals) - 2)] if env_vals else 0.0
    fut_thr = fut_vals[max(0, len(fut_vals) - 2)] if fut_vals else 0.0

    sensors: list[str] = []
    actions: list[str] = []
    for a in members:
        if env and env_mi[a] >= env_thr and env_mi[a] > 0:
            sensors.append(a)
        elif future_mi[a] >= fut_thr and future_mi[a] > 0:
            actions.append(a)
    internals = [a for a in members if a not in sensors and a not in actions]
    # Composites need at least one internal for a meaningful residual; if the
    # heuristic emptied I, demote the lowest-env member into I.
    if not internals and members:
        pick = min(members, key=lambda a: env_mi.get(a, 0.0))
        if pick in sensors:
            sensors.remove(pick)
        if pick in actions:
            actions.remove(pick)
        internals = [pick]
    return RolePartition(
        sensors=tuple(sorted(sensors)),
        actions=tuple(sorted(actions)),
        internals=tuple(sorted(internals)),
        environment=tuple(sorted(env)),
    )


def _joint_series(series: dict[str, list[int]], actors: tuple[str, ...]) -> list:
    if not actors:
        return [0] * len(next(iter(series.values())))
    if len(actors) == 1:
        return list(series[actors[0]])
    return list(zip(*(series[a] for a in actors)))


def blanket_residual(
    series: dict[str, list[int]],
    cluster: tuple[str, ...],
    *,
    all_actors: list[str] | None = None,
    tolerance_bits: float = DEFAULT_BLANKET_TOLERANCE_BITS,
) -> BlanketScore:
    """Estimate J(C) for an actor cluster and pass/fail against tolerance."""
    roles = classify_roles(series, cluster, all_actors=all_actors)
    if not roles.internals:
        return BlanketScore(
            residual_bits=1.0,
            roles=roles,
            passed=False,
            detail="no internal variables after role classification",
        )
    if not roles.environment:
        return BlanketScore(
            residual_bits=1.0,
            roles=roles,
            passed=False,
            detail="no environment variables outside cluster",
        )
    n = len(next(iter(series.values())))
    if n < 4:
        return BlanketScore(
            residual_bits=1.0,
            roles=roles,
            passed=False,
            detail="insufficient timesteps",
        )

    i_t1 = _joint_series(series, roles.internals)[1:]
    e_t1 = _joint_series(series, roles.environment)[1:]
    s_t = _joint_series(series, roles.sensors)[:-1]
    a_t = _joint_series(series, roles.actions)[:-1]
    if roles.sensors and roles.actions:
        cond = list(zip(s_t, a_t))
    elif roles.sensors:
        cond = s_t
    elif roles.actions:
        cond = a_t
    else:
        cond = [0] * (n - 1)

    residual = conditional_mi(i_t1, e_t1, cond)
    # Composites must keep a non-empty internal set for the residual to mean
    # "screened autonomy" rather than "all interface, no inside."
    structure_ok = len(roles.internals) >= MIN_INTERNAL_FOR_COMPOSITE
    passed = structure_ok and residual <= tolerance_bits
    detail = (
        f"J={residual:.4f} bits (tol={tolerance_bits}), "
        f"S={roles.sensors}, A={roles.actions}, I={roles.internals}, E={len(roles.environment)}"
    )
    return BlanketScore(residual_bits=residual, roles=roles, passed=passed, detail=detail)
