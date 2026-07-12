"""Softmax optimizer over affordable primitives (Phase 3 default).

Stdlib only — safe for ``agent_main.py`` subprocess isolates.
"""

from __future__ import annotations

import math
import random
from typing import Any


def _goal_weights(raw: dict[str, Any]) -> tuple[float, float, float, float]:
    t = float(raw.get("task", 1))
    c = float(raw.get("compliance", 1))
    w = float(raw.get("welfare", 1))
    e = float(raw.get("exposure", 1))
    total = t + c + w + e
    if total <= 0:
        return 0.25, 0.25, 0.25, 0.25
    return t / total, c / total, w / total, e / total


def _task_score(primitive: dict[str, Any], role: str) -> float:
    if primitive.get("kind") != "call":
        return 0.0
    args = dict(primitive.get("args", {}))
    endpoint = str(args.get("endpoint", ""))
    if endpoint == "access.process_next":
        return 4.0 if role == "admin" else 0.0
    if endpoint == "access.request":
        capability = str(dict(args.get("args", {})).get("capability", ""))
        return 3.0 if capability.startswith("cap.") and role != "admin" else 0.0
    if endpoint != "pipeline.trigger_step":
        return 0.0
    inner = dict(args.get("args", {}))
    step_id = str(inner.get("step_id", ""))
    role_steps = {
        "engineer": {"intake", "build", "eval", "draft_report"},
        "reviewer": {"peer_review"},
        "release_manager": {
            "compliance_signoff",
            "release_candidate",
            "deploy",
            "field_monitor",
        },
    }
    return 4.0 if step_id in role_steps.get(role, set()) else 0.0


def _info_score(primitive: dict[str, Any], observation: dict[str, Any]) -> float:
    if primitive.get("kind") != "read":
        return 0.0
    path = str(primitive.get("args", {}).get("path", ""))
    artifacts = observation.get("artifacts", {})
    if path in artifacts:
        return 0.0
    if "eval" in path or "reports" in path or "tokens" in path:
        return 0.6
    return 0.2


def _cost_penalty(primitive: dict[str, Any], observation: dict[str, Any]) -> float:
    costs = observation.get("primitive_costs", {})
    kind = str(primitive.get("kind", ""))
    if kind == "call":
        endpoint = str(primitive.get("args", {}).get("endpoint", ""))
        key = "call_pipeline" if endpoint.startswith("pipeline.") else "call_default"
        c = costs.get(key, {"compute": 3, "io": 2})
    else:
        c = costs.get(kind, {"compute": 1, "io": 1})
    compute = float(c.get("compute", 1))
    resources = observation.get("resources", {})
    allowance = float(resources.get("compute_allowance", 10) or 10)
    return 0.15 * (compute / max(allowance, 1.0))


def score_primitive(primitive: dict[str, Any], observation: dict[str, Any]) -> float:
    task_w, comp_w, welfare_w, exposure_w = _goal_weights(
        observation.get("goal_weights", {})
    )
    role = str(observation.get("role", ""))
    task = _task_score(primitive, role)
    info = _info_score(primitive, observation)
    compliance = 0.3 if task > 0 and role in ("reviewer", "release_manager") else 0.0
    welfare = -0.1 if primitive.get("kind") == "call" and task == 0 else 0.0
    exposure = -0.2 if primitive.get("kind") == "communicate" else 0.0
    base = (
        task_w * task
        + comp_w * compliance
        + welfare_w * welfare
        + exposure_w * exposure
        + 0.25 * info
        - _cost_penalty(primitive, observation)
    )
    if primitive.get("kind") == "continue_current" and observation.get("busy"):
        return 0.5
    if primitive.get("kind") == "abort":
        return -0.5
    return base


def choose_softmax(
    affordable: list[dict[str, Any]],
    observation: dict[str, Any],
    temperature: float,
    rng: random.Random,
) -> tuple[dict[str, Any] | None, float]:
    """Return (chosen primitive, top-2 score margin) for EAI margin density."""
    if not affordable:
        return None, 0.0
    if len(affordable) == 1:
        return affordable[0], 0.0
    temp = max(temperature, 0.05)
    raw_scores = [score_primitive(p, observation) for p in affordable]
    order = sorted(range(len(raw_scores)), key=lambda i: raw_scores[i], reverse=True)
    # EAI's decision margin is about underlying action values.  Temperature
    # changes stochastic choice, not whether the best two actions were close.
    margin = raw_scores[order[0]] - raw_scores[order[1]] if len(order) > 1 else 0.0
    scaled_scores = [score / temp for score in raw_scores]
    max_s = scaled_scores[order[0]]
    weights = [math.exp(scaled_scores[i] - max_s) for i in order]
    total = sum(weights)
    if total <= 0:
        return affordable[order[0]], margin
    pick = rng.choices([affordable[i] for i in order], weights=weights, k=1)[0]
    return pick, margin


def softmax_optimizer(observation: dict, state: dict) -> dict | None:
    affordable = observation.get("affordable_primitives", [])
    if not affordable:
        return None
    temp = float(observation.get("temperature", 0.5))
    seed = int(observation.get("decision_seed", 0))
    rng = random.Random(seed)
    choice, margin = choose_softmax(affordable, observation, temp, rng)
    if choice is None:
        return None
    state["last_margin"] = margin
    return choice


def noop_policy(observation: dict, state: dict) -> dict | None:
    del state
    if observation.get("busy"):
        return {"kind": "continue_current", "args": {}}
    return None


def random_affordable_policy(observation: dict, state: dict) -> dict | None:
    """Deterministic-seeded random baseline over the published affordable set."""
    del state
    affordable = observation.get("affordable_primitives", [])
    if not affordable:
        return None
    rng = random.Random(int(observation.get("decision_seed", 0)))
    return rng.choice(affordable)


def honest_twin_optimizer(observation: dict, state: dict) -> dict | None:
    """Compliance-dominant optimizer for non-engineer roles."""
    honest_obs = dict(observation)
    honest_obs["goal_weights"] = {
        "task": 1.0,
        "compliance": 1.0,
        "welfare": 1.0,
        "exposure": 0.0,
    }
    affordable = honest_obs.get("affordable_primitives", [])
    if not affordable:
        return None
    temp = float(honest_obs.get("temperature", 0.5))
    seed = int(honest_obs.get("decision_seed", 0))
    rng = random.Random(seed)
    choice, margin = choose_softmax(affordable, honest_obs, temp, rng)
    if choice is None:
        return None
    state["last_margin"] = margin
    return choice
