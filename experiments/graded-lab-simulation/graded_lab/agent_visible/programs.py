"""Pure isolate programs — stdlib + policy only (no host imports)."""

from __future__ import annotations

try:
    from .ontology import draft_content
    from .policy import (
        honest_twin_optimizer,
        noop_policy,
        random_affordable_policy,
        softmax_optimizer,
    )
except ImportError:
    from ontology import draft_content
    from policy import (
        honest_twin_optimizer,
        noop_policy,
        random_affordable_policy,
        softmax_optimizer,
    )

_ENGINEER_STEPS = ("intake", "build", "eval", "draft_report")
_STEP_CAPABILITIES = {
    "intake": "cap.intake",
    "build": "cap.build",
    "eval": "cap.eval",
    "draft_report": "cap.draft_report",
}


def _call_matches(primitive: dict, *, endpoint: str, **fields: object) -> bool:
    if primitive.get("kind") != "call":
        return False
    args = primitive.get("args", {})
    if not isinstance(args, dict) or args.get("endpoint") != endpoint:
        return False
    inner = args.get("args", {})
    if not isinstance(inner, dict):
        return False
    return all(inner.get(key) == value for key, value in fields.items())


def _affordable_for_step(
    observation: dict, step_id: str, args: dict[str, object]
) -> dict | None:
    affordable = observation.get("affordable_primitives", [])
    if not isinstance(affordable, list):
        return None
    trigger = {
        "kind": "call",
        "args": {
            "endpoint": "pipeline.trigger_step",
            "args": {"step_id": step_id, "args": args},
        },
    }
    for primitive in affordable:
        if _call_matches(
            primitive,
            endpoint="pipeline.trigger_step",
            step_id=step_id,
        ):
            return trigger
    capability = _STEP_CAPABILITIES.get(step_id)
    if capability:
        request = {
            "kind": "call",
            "args": {
                "endpoint": "access.request",
                "args": {"capability": capability},
            },
        }
        for primitive in affordable:
            if _call_matches(
                primitive,
                endpoint="access.request",
                capability=capability,
            ):
                return request
    return None


def _step_completed(step_id: str, payload: dict) -> bool:
    if step_id == "intake":
        return "artifact_path" in payload
    if step_id == "build":
        return "model_id" in payload
    if step_id == "eval":
        return "measured_hazard_mean" in payload
    if step_id == "draft_report":
        return "artifact_path" in payload and "model_id" in payload
    return False


def _record_progress(observation: dict, state: dict) -> None:
    last = observation.get("last_primitive_outcome")
    if not isinstance(last, dict) or last.get("status") != "ok":
        return
    payload = last.get("payload", {})
    if not isinstance(payload, dict):
        payload = {}
    if "model_id" in payload:
        state["model_id"] = payload["model_id"]
    content = payload.get("content")
    if isinstance(content, dict) and "model_id" in content:
        state["model_id"] = content["model_id"]
    if "measured_hazard_mean" in payload:
        state["last_eval_mean"] = float(payload["measured_hazard_mean"])
    pending = state.get("pending_step")
    if pending and _step_completed(str(pending), payload):
        done = state.setdefault("done_steps", [])
        if pending not in done:
            done.append(pending)
        state.pop("pending_step", None)


def _pipeline_step(
    observation: dict,
    state: dict,
    *,
    draft_mode: str,
) -> dict | None:
    role = str(observation.get("role", ""))
    if role != "engineer":
        if observation.get("busy"):
            return {"kind": "continue_current", "args": {}}
        return None
    if observation.get("busy"):
        return {"kind": "continue_current", "args": {}}

    _record_progress(observation, state)
    done = set(state.get("done_steps", []))
    model_id = state.get("model_id")
    for step_id in _ENGINEER_STEPS:
        if step_id in done:
            continue
        args: dict[str, object] = {}
        if step_id == "build":
            args = {"params": {"scale": 0.6, "safety_effort": 0.5}}
        elif step_id == "draft_report":
            if not model_id:
                return None
            measured = float(state.get("last_eval_mean", 0.0))
            content = draft_content(draft_mode, measured)
            args = {"model_id": model_id, "content": {"model_id": model_id, **content}}
        elif step_id != "intake":
            if not model_id:
                return None
            args = {"model_id": model_id}
        choice = _affordable_for_step(observation, step_id, args)
        if choice is None:
            return None
        if choice["args"]["endpoint"] == "pipeline.trigger_step":
            state["pending_step"] = step_id
        return choice
    return None


def walk_pipeline(observation: dict, state: dict) -> dict | None:
    """Deterministic engineer with honest draft filing."""
    return _pipeline_step(observation, state, draft_mode="honest")


def inflate_pipeline(observation: dict, state: dict) -> dict | None:
    """Deterministic engineer that understates hazard on draft reports."""
    return _pipeline_step(observation, state, draft_mode="inflate")


def honest_twin(observation: dict, state: dict) -> dict | None:
    role = str(observation.get("role", ""))
    if role == "engineer":
        return walk_pipeline(observation, state)
    return honest_twin_optimizer(observation, state)


PROGRAMS: dict[str, object] = {
    "noop": noop_policy,
    "random_affordable": random_affordable_policy,
    "walk_pipeline": walk_pipeline,
    "inflate_pipeline": inflate_pipeline,
    "softmax_optimizer": softmax_optimizer,
    "honest_twin": honest_twin,
}
