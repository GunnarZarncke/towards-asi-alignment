"""Pure, host-independent agent decision logic (stdlib only).

Shared verbatim by ``isolate.MockIsolate`` (in-process) and
``agent_main.py`` (real OS subprocess) so both backends run
byte-identical decision logic — the substance of
``verify_isolate_equivalence.py``.

A "program" is a pure function ``(observation, state) -> tool_call | None``.
``None`` means "idle this turn." ``state`` is a plain dict the program may
mutate to remember progress WITHIN an episode (not persistent across
episodes; see ``agent_state.py`` for that). Programs must never import
anything host-side (oracle, pipeline_engine, access, tools, events,
workspace, pipeline_spec, world) — enforced by
``tests/test_agent_main_isolation.py``.

Phase 3 ships one scripted program, ``walk_pipeline``, used to exercise the
Host end to end (tool calls, access requests, pipeline steps) and to prove
backend equivalence before any goal-driven policy exists. Phase 4 adds
``goal_policy`` (softmax playbook choice); Phase 5 adds ``honest_twin``
(the full-surface twin transform, ``twins.py``).
"""

from __future__ import annotations

import math
import random

# Dual-mode import: as `lab_sim.programs` (package, MockIsolate) relative
# imports resolve normally; as bare `programs` (agent_main.py subprocess,
# no package context) they fall back to absolute imports resolved via the
# script's own directory on sys.path. Both paths load the SAME files.
try:
    from .ontology import REVIEW_HAZARD_THRESHOLD, report_content
    from .playbooks import (
        HONEST_PLAYBOOK_BY_ROLE,
        PLAYBOOKS_BY_ROLE,
        available_playbooks,
        playbook_by_name,
    )
except ImportError:
    from ontology import REVIEW_HAZARD_THRESHOLD, report_content
    from playbooks import (
        HONEST_PLAYBOOK_BY_ROLE,
        PLAYBOOKS_BY_ROLE,
        available_playbooks,
        playbook_by_name,
    )

_WALK_STEP_ORDER = (
    "submit_build", "run_eval", "file_report", "request_review",
    "approve_review", "request_release", "sign_off", "deploy",
)


def _walk_pipeline(observation: dict, state: dict) -> dict | None:
    """Deterministic scripted policy: drive one model straight through the
    default pipeline, requesting access whenever denied."""
    del state  # stateless; all progress is inferable from the observation
    denied_capability = observation.get("last_denied_capability")
    if denied_capability:
        return {"tool": "access.request", "args": {"capability": denied_capability}}
    completed = observation.get("completed_steps", [])
    model_id = observation.get("own_model_id")
    for step_id in _WALK_STEP_ORDER:
        if step_id not in completed:
            args: dict[str, object] = {}
            if step_id == "submit_build":
                args["params"] = {"scale": 0.6, "safety_effort": 0.5}
            else:
                args["model_id"] = model_id
            return {"tool": "pipeline.trigger_step", "args": {"step_id": step_id, "args": args}}
    return None


# -- Phase 4: goal-driven playbook policy ---------------------------------


def _resolve_step_kind(step_kind: str, observation: dict) -> dict | None:
    """Resolve one playbook step-kind to a concrete tool call, or None to
    stall (abandon the in-progress playbook for this turn)."""
    model_id = observation.get("model_id")
    completed = set(observation.get("completed_steps", ()))
    if observation.get("last_denied_capability"):
        return {"tool": "access.request", "args": {"capability": observation["last_denied_capability"]}}

    if step_kind == "build":
        return {
            "tool": "pipeline.trigger_step",
            "args": {"step_id": "submit_build", "args": {"params": {"scale": 0.6, "safety_effort": 0.5}}},
        }
    if step_kind == "eval":
        return {"tool": "pipeline.trigger_step", "args": {"step_id": "run_eval", "args": {"model_id": model_id}}}
    if step_kind.startswith("report:"):
        mode = step_kind.split(":", 1)[1]
        content = report_content(mode, observation.get("last_payload") or {})
        return {
            "tool": "pipeline.trigger_step",
            "args": {"step_id": "file_report", "args": {"model_id": model_id, "content": content}},
        }
    if step_kind == "review_request":
        return {"tool": "pipeline.trigger_step", "args": {"step_id": "request_review", "args": {"model_id": model_id}}}
    if step_kind in ("review_conscientious", "review_rubber_stamp"):
        pending_step = "approve_review" if "approve_review" not in completed else "sign_off"
        if step_kind == "review_conscientious":
            content = observation.get("report_content") or {}
            if content.get("measured_hazard", 1.0) >= REVIEW_HAZARD_THRESHOLD:
                return None  # stall: won't wave through a hazardous filing
        return {"tool": "pipeline.trigger_step", "args": {"step_id": pending_step, "args": {"model_id": model_id}}}
    if step_kind == "release_full":
        if "request_release" not in completed:
            next_step = "request_release"
        elif "deploy" not in completed:
            next_step = "deploy"
        else:
            next_step = "monitor"
        return {"tool": "pipeline.trigger_step", "args": {"step_id": next_step, "args": {"model_id": model_id}}}
    raise ValueError(f"unknown step_kind {step_kind!r}")


def _softmax_choose(playbooks, weights: dict, temperature: float, decision_seed: str):
    scores = [sum(weights.get(k, 0.0) * v for k, v in pb.feature_deltas.items()) for pb in playbooks]
    if temperature <= 0:
        best_idx = max(range(len(playbooks)), key=lambda i: (scores[i], playbooks[i].name))
        return playbooks[best_idx]
    m = max(scores)
    exp_scores = [math.exp((s - m) / temperature) for s in scores]
    total = sum(exp_scores)
    probs = [s / total for s in exp_scores]
    r = random.Random(decision_seed).random()
    cum = 0.0
    for pb, p in zip(playbooks, probs):
        cum += p
        if r <= cum:
            return pb
    return playbooks[-1]


_LINEAR_STEP_KIND_TARGET = {
    "build": "submit_build",
    "eval": "run_eval",
    "review_request": "request_review",
}

# Compound step-kinds resolve their own concrete pipeline step from
# `completed_steps` each call (see _resolve_step_kind) rather than mapping
# to one fixed target; each invocation performs exactly one pipeline
# action and then the playbook is re-decided fresh (see _advance_playbook).
_COMPOUND_STEP_KINDS = frozenset({"review_conscientious", "review_rubber_stamp", "release_full"})


def _next_step_kind(chosen, observation: dict) -> str | None:
    """Ground-truth-driven position within a playbook: the first step-kind
    whose target pipeline step is not yet in ``completed_steps``. Never
    tracked via a manually incremented index — a step that was ATTEMPTED
    but DENIED (DAG precondition or access) must not be skipped, so
    position must always be recomputed from what actually completed."""
    completed = set(observation.get("completed_steps", ()))
    for step_kind in chosen.step_kinds:
        if step_kind in _COMPOUND_STEP_KINDS:
            return step_kind
        target = _LINEAR_STEP_KIND_TARGET.get(step_kind)
        if target is None and step_kind.startswith("report:"):
            target = "file_report"
        if target is not None and target not in completed:
            return step_kind
    return None


def _advance_playbook(role: str, observation: dict, state: dict) -> dict | None:
    """Step through ``state["current_playbook"]`` (already chosen) by one
    step-kind; returns the resulting tool call, or None if exhausted/stalled."""
    chosen = playbook_by_name(role, state["current_playbook"])
    step_kind = _next_step_kind(chosen, observation)
    if step_kind is None:
        state["current_playbook"] = None
        return None
    call = _resolve_step_kind(step_kind, observation)
    if call is None:
        state["current_playbook"] = None
        return None
    if step_kind in _COMPOUND_STEP_KINDS and call["tool"] != "access.request":
        # Single-shot: one pipeline action per selection. Re-decide fresh
        # next turn (availability + softmax) rather than assuming there is
        # more to do — correct for reviewer, and a no-op simplification for
        # release_manager's single-candidate role (only one playbook exists).
        state["current_playbook"] = None
    return call


def _goal_policy(observation: dict, state: dict) -> dict | None:
    role = observation["role"]
    if state.get("current_playbook") is None:
        available = available_playbooks(role, observation)
        if not available:
            return None
        if role == "reviewer" and observation.get("self_captured"):
            chosen = playbook_by_name(role, "rev_rubber_stamp")
        else:
            chosen = _softmax_choose(
                available, observation["goal_weights"], observation["temperature"], observation["decision_seed"]
            )
        state["current_playbook"] = chosen.name
    return _advance_playbook(role, observation, state)


def _honest_twin_policy(observation: dict, state: dict) -> dict | None:
    """Full-surface twin: every role always picks its honest baseline
    playbook, ignoring goal weights and capture (Phase 5, twins.py)."""
    role = observation["role"]
    if state.get("current_playbook") is None:
        available = {pb.name for pb in available_playbooks(role, observation)}
        honest_name = HONEST_PLAYBOOK_BY_ROLE.get(role)
        if honest_name is None or honest_name not in available:
            return None
        state["current_playbook"] = honest_name
    return _advance_playbook(role, observation, state)


PROGRAMS = {
    "walk_pipeline": _walk_pipeline,
    "goal_policy": _goal_policy,
    "honest_twin": _honest_twin_policy,
}
