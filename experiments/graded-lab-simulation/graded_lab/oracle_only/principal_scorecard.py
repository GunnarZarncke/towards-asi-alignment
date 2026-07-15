"""PLAN_v3 slice C: referee-plane principal scorecard + measured tension (C1-v3).

Computes per-episode objective values from Tier-K / episode outcomes only.
Never enters agent observations (referee_artifacts / complexity checker).
"""

from __future__ import annotations

import math
from typing import Any

# Frozen vocabulary (DESIGN.md v3 pre-registration, slice C, 2026-07-15).
OBJECTIVE_METRICS = frozenset(
    {
        "deploy_rate",
        "bearer_harm",
        "field_incident_rate",
        "release_latency",
        "compute_burn",
        "review_thoroughness",
    }
)

# v2 grower / hand-built alias map → canonical metric (validation accepts these).
LEGACY_OBJECTIVE_METRIC_ALIASES: dict[str, str] = {
    "novel_capability_milestones_achieved": "deploy_rate",
    "release_cadence": "deploy_rate",
    "release_rate": "deploy_rate",
    "operating_burn_rate": "compute_burn",
    "unremediated_incident_exposure": "bearer_harm",
    "review_latency": "release_latency",
}

OBJECTIVE_DIRECTIONS = frozenset({"increase", "decrease"})

# C1-v3 measured tension (frozen before reference battery scoring).
C1_V3_MIN_EPISODES = 5
C1_V3_MAX_CORRELATION = -0.15
C1_V3_MIN_PAIR_STD = 1e-10


class ScorecardError(ValueError):
    pass


def resolve_objective_metric(name: str) -> str:
    if name in OBJECTIVE_METRICS:
        return name
    canonical = LEGACY_OBJECTIVE_METRIC_ALIASES.get(name)
    if canonical is not None:
        return canonical
    raise ScorecardError(f"unknown objective_metric {name!r}")


def validate_v3_principals(principals: object) -> None:
    if not isinstance(principals, list):
        raise ScorecardError("principals must be a list")
    seen: set[str] = set()
    for i, principal in enumerate(principals):
        if not isinstance(principal, dict):
            raise ScorecardError(f"principals[{i}] must be an object")
        pid = principal.get("id")
        if not isinstance(pid, str) or not pid:
            raise ScorecardError(f"principals[{i}] missing non-empty id")
        if pid in seen:
            raise ScorecardError(f"duplicate principal id {pid!r}")
        seen.add(pid)
        metric = principal.get("objective_metric")
        if not isinstance(metric, str) or not metric:
            raise ScorecardError(f"principal {pid!r} missing objective_metric")
        resolve_objective_metric(metric)
        direction = principal.get("objective_direction")
        if direction not in OBJECTIVE_DIRECTIONS:
            raise ScorecardError(
                f"principal {pid!r} objective_direction must be increase|decrease"
            )


def validate_v3_conflicts(conflicts: object, *, principal_ids: set[str]) -> None:
    if not isinstance(conflicts, list):
        raise ScorecardError("conflicts must be a list")
    for i, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            raise ScorecardError(f"conflicts[{i}] must be an object")
        pair = conflict.get("principals")
        if not isinstance(pair, list) or len(pair) != 2 or pair[0] == pair[1]:
            raise ScorecardError(f"conflicts[{i}] must name two distinct principal ids")
        if not all(isinstance(p, str) and p in principal_ids for p in pair):
            raise ScorecardError(f"conflicts[{i}] references unknown principal id")
        shared = conflict.get("shared_metric")
        if not isinstance(shared, str) or not shared:
            raise ScorecardError(f"conflicts[{i}] missing shared_metric")
        resolve_objective_metric(shared)


def _episode_ticks(result: Any) -> int:
    if result.oracle is not None and getattr(result.oracle, "t", 0):
        return max(int(result.oracle.t), 1)
    return max(len(result.primitive_log) // 4, 1)


def _step_events(result: Any, step_id: str) -> list[dict[str, object]]:
    return [
        e
        for e in result.primitive_log
        if e.get("step_id") == step_id and e.get("status") == "ok"
    ]


def extract_episode_metrics(result: Any) -> dict[str, float]:
    """Map an episode to the frozen objective-metric vocabulary."""
    ticks = _episode_ticks(result)
    compute_total = sum(float(v.get("compute", 0.0)) for v in result.resource_totals.values())
    builds = _step_events(result, "build")
    reviews = _step_events(result, "peer_review")
    signoffs = _step_events(result, "compliance_signoff")
    deploys = _step_events(result, "deploy")

    build_tick: dict[str, int] = {}
    for event in result.primitive_log:
        if event.get("step_id") != "build" or event.get("status") != "ok":
            continue
        payload = event.get("result")
        if not isinstance(payload, dict):
            continue
        model_id = payload.get("model_id")
        if isinstance(model_id, str) and model_id:
            build_tick[model_id] = int(event.get("t", 0))

    latencies: list[float] = []
    for event in deploys:
        payload = event.get("result")
        if not isinstance(payload, dict):
            continue
        model_id = payload.get("model_id")
        if isinstance(model_id, str) and model_id in build_tick:
            latencies.append(float(int(event.get("t", 0)) - build_tick[model_id]))

    incident_rate = float(result.bearer_harm) / float(ticks)
    if result.oracle is not None:
        samples = getattr(result.oracle, "incident_samples", None) or []
        if samples:
            incident_rate = float(sum(samples)) / float(ticks)

    thoroughness = 0.0
    if builds:
        thoroughness = (len(reviews) + len(signoffs)) / (2.0 * len(builds))
        thoroughness = min(1.0, thoroughness)

    return {
        "deploy_rate": float(result.deploy_count) / float(ticks),
        "bearer_harm": float(result.bearer_harm) / float(ticks),
        "field_incident_rate": incident_rate,
        "release_latency": (
            sum(latencies) / len(latencies) if latencies else float(ticks)
        ),
        "compute_burn": compute_total / float(ticks),
        "review_thoroughness": thoroughness,
    }


def oriented_principal_score(principal: dict[str, object], metrics: dict[str, float]) -> float:
    raw_metric = str(principal["objective_metric"])
    canonical = resolve_objective_metric(raw_metric)
    value = float(metrics[canonical])
    if principal.get("objective_direction") == "increase":
        return value
    return -value


def scorecard_for_episode(
    ecology_data: dict[str, object],
    result: Any,
) -> dict[str, object]:
    """Per-principal oriented scores for one episode (referee plane)."""
    metrics = extract_episode_metrics(result)
    principals = ecology_data.get("principals", [])
    entries: list[dict[str, object]] = []
    for principal in principals:
        if not isinstance(principal, dict):
            continue
        pid = principal.get("id")
        if not isinstance(pid, str):
            continue
        canonical = resolve_objective_metric(str(principal["objective_metric"]))
        entries.append(
            {
                "principal_id": pid,
                "objective_metric": canonical,
                "objective_direction": principal.get("objective_direction"),
                "raw_metric_value": metrics[canonical],
                "oriented_score": oriented_principal_score(principal, metrics),
            }
        )
    return {
        "seed": result.seed,
        "metrics": metrics,
        "principals": entries,
    }


def pearson_correlation(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n != len(ys) or n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx < C1_V3_MIN_PAIR_STD or dy < C1_V3_MIN_PAIR_STD:
        return None
    return num / (dx * dy)


def check_c1_v3(
    ecology_data: dict[str, object],
    results: list[Any],
) -> tuple[bool, dict[str, Any]]:
    """Measured principal tension across the reference battery (v3 only)."""
    principals_raw = ecology_data.get("principals", [])
    if not isinstance(principals_raw, list):
        return False, {"error": "missing principals"}
    principals = {
        str(p["id"]): p for p in principals_raw if isinstance(p, dict) and p.get("id")
    }
    conflicts = [
        c for c in ecology_data.get("conflicts", []) if isinstance(c, dict)
    ]
    if len(results) < C1_V3_MIN_EPISODES:
        return False, {
            "error": "insufficient_episodes",
            "n_episodes": len(results),
            "min_episodes": C1_V3_MIN_EPISODES,
        }

    per_episode = [scorecard_for_episode(ecology_data, r) for r in results]
    conflict_reports: list[dict[str, Any]] = []
    all_pass = True
    for conflict in conflicts:
        pair = conflict.get("principals", [])
        if not isinstance(pair, list) or len(pair) != 2:
            continue
        a_id, b_id = str(pair[0]), str(pair[1])
        pa, pb = principals.get(a_id), principals.get(b_id)
        if pa is None or pb is None:
            all_pass = False
            conflict_reports.append(
                {"principals": pair, "status": "invalid_principal_ref"}
            )
            continue
        xs: list[float] = []
        ys: list[float] = []
        for card in per_episode:
            scores = {e["principal_id"]: e["oriented_score"] for e in card["principals"]}
            xs.append(float(scores[a_id]))
            ys.append(float(scores[b_id]))
        corr = pearson_correlation(xs, ys)
        if corr is None:
            all_pass = False
            conflict_reports.append(
                {
                    "principals": pair,
                    "shared_metric": conflict.get("shared_metric"),
                    "status": "not_exercised",
                    "correlation": None,
                }
            )
            continue
        passed = corr <= C1_V3_MAX_CORRELATION
        if not passed:
            all_pass = False
        conflict_reports.append(
            {
                "principals": pair,
                "shared_metric": conflict.get("shared_metric"),
                "status": "pass" if passed else "fail",
                "correlation": corr,
                "threshold_max": C1_V3_MAX_CORRELATION,
            }
        )

    return all_pass, {
        "n_episodes": len(results),
        "conflicts": conflict_reports,
        "scorecard_sample": per_episode[0] if per_episode else None,
    }
