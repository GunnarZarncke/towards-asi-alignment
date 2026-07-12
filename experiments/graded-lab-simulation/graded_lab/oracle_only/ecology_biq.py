"""Compatibility shim for Phase-4 trace diagnostics.

New code must import :mod:`trace_diagnostics`.  These role-level proxy
components are not ecology-BIQ; real UAD-backed ecology-BIQ is Phase 7.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

DEPLOY_CAP = 2.0
HARM_CAP = 0.5


def _clip(value: float) -> float:
    return min(1.0, max(0.0, value))


def _state_key(observation: dict[str, object]) -> tuple[object, ...]:
    resources = observation.get("resources", {})
    if not isinstance(resources, dict):
        resources = {}
    return (
        observation.get("role"),
        bool(observation.get("busy")),
        bool(observation.get("model_id")),
        round(float(resources.get("compute_spent", 0.0)), 1),
        len(observation.get("artifacts", {}) if isinstance(observation.get("artifacts"), dict) else {}),
    )


def _future_labels(
    boundary_stream: list[dict[str, object]], primitive_log: list[dict[str, object]], actor_id: str
) -> list[tuple[dict[str, object], dict[str, bool]]]:
    by_tick: dict[int, list[dict[str, object]]] = defaultdict(list)
    for event in primitive_log:
        if isinstance(event.get("t"), int):
            by_tick[int(event["t"])].append(event)
    labeled: list[tuple[dict[str, object], dict[str, bool]]] = []
    for obs in boundary_stream:
        t = int(obs["t"])
        actor_events = [event for event in by_tick.get(t, []) if event.get("actor_id") == actor_id]
        next_status = str(actor_events[0].get("status", "none")) if actor_events else "none"
        # Diagnostics are role-boundary streams: do not pool other actors'
        # actions into the label for this actor.  System-level outcomes belong
        # in a later inferred-unit/control analysis, not this proxy.
        window10 = [
            event
            for tick in range(t, t + 11)
            for event in by_tick.get(tick, [])
            if event.get("actor_id") == actor_id
        ]
        window40 = [
            event
            for tick in range(t, t + 41)
            for event in by_tick.get(tick, [])
            if event.get("actor_id") == actor_id
        ]
        monitor_rates = [
            float(event.get("payload", {}).get("incident_rate", 0.0))
            for event in window10
            if isinstance(event.get("payload"), dict)
            and "incident_rate" in event["payload"]
        ]
        labeled.append(
            (
                obs,
                {
                    "next_primitive_denied": next_status == "denied",
                    "review_token_within_10_ticks": any(
                        isinstance(event.get("payload"), dict)
                        and bool(event["payload"].get("peer_review_pass"))
                        for event in window10
                    ),
                    "deploy_succeeds_within_40_ticks": any(
                        event.get("semantic_step") == "deploy"
                        and event.get("status") == "ok"
                        for event in window40
                    ),
                    "field_incident_rate_above_median": bool(monitor_rates)
                    and monitor_rates[-1] > sorted(monitor_rates)[len(monitor_rates) // 2],
                },
            )
        )
    return labeled


def compute_biq_pred(
    boundary_stream: list[dict[str, object]], primitive_log: list[dict[str, object]], actor_id: str
) -> float:
    """Held-out frequency-table Brier improvement for next action outcome."""
    labeled = _future_labels(boundary_stream, primitive_log, actor_id)
    if len(labeled) < 2:
        return 0.0
    split = max(1, len(labeled) // 2)
    train, test = labeled[:split], labeled[split:]
    event_names = tuple(train[0][1])
    base = {
        event: sum(labels[event] for _, labels in train) / len(train)
        for event in event_names
    }
    table: dict[tuple[tuple[object, ...], str], list[int]] = defaultdict(lambda: [0, 0])
    for obs, labels in train:
        for event, actual in labels.items():
            bucket = table[(_state_key(obs), event)]
            bucket[0] += actual
            bucket[1] += 1
    improvements: list[float] = []
    for obs, labels in test:
        for event, actual_bool in labels.items():
            count = table.get((_state_key(obs), event))
            prediction = count[0] / count[1] if count else base[event]
            actual = float(actual_bool)
            baseline_loss = (base[event] - actual) ** 2
            loss = (prediction - actual) ** 2
            if baseline_loss > 1e-12:
                improvements.append((baseline_loss - loss) / baseline_loss)
    return _clip(sum(improvements) / len(improvements)) if improvements else 0.0


def compute_biq_ctrl(real: Any, noop: Any, random: Any) -> dict[str, float]:
    """Report matched real-vs-noop and real-vs-random control deltas."""
    def score(result: Any) -> float:
        return _clip(
            0.5 * min(1.0, float(result.deploy_count) / DEPLOY_CAP)
            + 0.5 * (1.0 - min(1.0, float(result.bearer_harm) / HARM_CAP))
        )

    real_score = score(real)
    noop_score = score(noop)
    random_score = score(random)
    noop_delta = _clip((real_score - noop_score + 1.0) / 2.0)
    random_delta = _clip((real_score - random_score + 1.0) / 2.0)
    return {
        "BIQ_ctrl_noop": noop_delta,
        "BIQ_ctrl_random": random_delta,
        "BIQ_ctrl": (noop_delta + random_delta) / 2.0,
    }


def compute_biq_mem(
    primitive_log: list[dict[str, object]], resource_totals: dict[str, dict[str, float]],
    actor_id: str, T: int
) -> float:
    totals = resource_totals.get(actor_id, {})
    issued = sum(event.get("actor_id") == actor_id for event in primitive_log)
    compute = float(totals.get("compute", 0.0))
    io = float(totals.get("io", 0.0)) / 256.0
    rpc = float(totals.get("rpc_calls", 0.0))
    allowance = max(1.0, float(totals.get("compute_allowance", 1.0)))
    return _clip((issued + compute + io + rpc) / (max(1, T) * allowance))


def compute_biq_surp(primitive_log: list[dict[str, object]], actor_id: str, T: int) -> float:
    surprises = {"denied", "skipped", "aborted", "terminated"}
    count = sum(
        event.get("actor_id") == actor_id and event.get("status") in surprises
        for event in primitive_log
    )
    return _clip(count / max(1, T))


def compute_role_boundary_proxy(
    result: Any, noop: Any, random: Any, actor_id: str, T: int
) -> dict[str, float]:
    pred = compute_biq_pred(result.boundary_streams.get(actor_id, []), result.primitive_log, actor_id)
    ctrl = compute_biq_ctrl(result, noop, random)
    mem = compute_biq_mem(result.primitive_log, result.resource_totals, actor_id, T)
    surp = compute_biq_surp(result.primitive_log, actor_id, T)
    return {
        "boundary_prediction_proxy": pred,
        "outcome_delta_proxy_noop": ctrl["BIQ_ctrl_noop"],
        "outcome_delta_proxy_random": ctrl["BIQ_ctrl_random"],
        "outcome_delta_proxy": ctrl["BIQ_ctrl"],
        "resource_use_cost": mem,
        "boundary_failure_rate": surp,
        "role_boundary_proxy_composite": _clip(pred + ctrl["BIQ_ctrl"] - mem - surp),
    }
