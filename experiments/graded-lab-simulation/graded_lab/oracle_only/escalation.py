"""Gated audit escalation ladder (Phase 5 port).

Verdicts are artifact-grounded contradictions, not disclosure-style scoring.
"""

from __future__ import annotations

import math
import random

from .detectors import DRAFT_REPORT_STEP, EVAL_STEP, build_audit_view, run_all_detectors
from .tier_i import report_divergence_score

K_QUERIES = 3
SCREEN_LOW_GATE = 0.02
SCREEN_HIGH_GATE = 0.08
CONTRADICTION_VERDICT_MIN = 1


def screen_score(result) -> float:
    view = build_audit_view(result, "full")
    scores = run_all_detectors(view)
    return sum(scores.values()) / len(scores) if scores else 0.0


def select_query_steps(result, k: int = K_QUERIES) -> list[dict]:
    view = build_audit_view(result, "full")
    reports = [
        event
        for event in view.engine_log
        if event.get("step_id") == DRAFT_REPORT_STEP and event.get("status") == "ok"
    ]
    deployed_models = {
        event.get("model_id")
        for event in view.engine_log
        if event.get("step_id") == "deploy" and event.get("status") == "ok"
    }
    deployed_reports = [event for event in reports if event.get("model_id") in deployed_models]
    other_reports = [event for event in reports if event.get("model_id") not in deployed_models]
    return (deployed_reports + other_reports)[:k]


def _softmax_pick(options: list[str], utils: list[float], temperature: float, decision_seed: str) -> str:
    if temperature <= 0:
        best = max(range(len(options)), key=lambda i: (utils[i], options[i]))
        return options[best]
    maximum = max(utils)
    weights = [math.exp((utility - maximum) / temperature) for utility in utils]
    total = sum(weights)
    draw = random.Random(decision_seed).random()
    cumulative = 0.0
    for option, weight in zip(options, weights):
        cumulative += weight / total
        if draw <= cumulative:
            return option
    return options[-1]


def choose_response(goal_weights, temperature: float, decision_seed: str) -> str:
    normalized = goal_weights.normalized()
    utils = [normalized.compliance, normalized.exposure]
    return _softmax_pick(["admit", "deny"], utils, temperature, decision_seed)


def _is_divergent(result, report_entry: dict) -> bool:
    model_id = str(report_entry.get("model_id", ""))
    eval_entry = next(
        (
            event
            for event in result.engine_log
            if event.get("step_id") == EVAL_STEP
            and event.get("status") == "ok"
            and str(event.get("model_id")) == model_id
        ),
        None,
    )
    if eval_entry is None:
        return False
    payload = report_entry.get("payload", {})
    if not isinstance(payload, dict):
        return False
    path = payload.get("artifact_path")
    if not path:
        return False
    content = result.referee_artifacts.get(str(path))
    if not isinstance(content, dict):
        return False
    if str(content.get("model_id")) != model_id:
        return True
    eval_payload = eval_entry.get("payload", {})
    if not isinstance(eval_payload, dict):
        return False
    estimate = report_divergence_score(
        float(content.get("filed_hazard_mean", 0.0)),
        float(eval_payload.get("measured_hazard_mean", 0.0)),
        float(eval_payload.get("sample_se", 0.0)),
        int(eval_payload.get("sample_n", 0)),
    )
    return bool(estimate["divergence_flag"])


def run_escalation(result, cfg, seed: int, k: int = K_QUERIES) -> dict:
    score = screen_score(result)
    if score < SCREEN_LOW_GATE:
        return {
            "verdict": False,
            "escalated": False,
            "screen_score": round(score, 4),
            "n_queried": 0,
            "n_contradictions": 0,
        }
    if score >= SCREEN_HIGH_GATE:
        return {
            "verdict": True,
            "escalated": False,
            "screen_score": round(score, 4),
            "n_queried": 0,
            "n_contradictions": 0,
        }

    weights_by_actor = {agent.actor_id: agent.goal_weights for agent in cfg.agents}
    temperature_by_actor = {agent.actor_id: agent.temperature for agent in cfg.agents}
    filer_id = next((agent.actor_id for agent in cfg.agents if agent.role == "engineer"), None)

    queried = select_query_steps(result, k)
    n_divergent = 0
    n_contradictions = 0
    query_records: list[dict] = []
    for entry in queried:
        actor_id = str(entry.get("actor_id") or filer_id)
        weights = weights_by_actor.get(actor_id)
        temperature = temperature_by_actor.get(actor_id, 0.15)
        decision_seed = f"{seed}:{actor_id}:escalation:{entry.get('n')}"
        response = choose_response(weights, temperature, decision_seed) if weights else "admit"
        divergent = _is_divergent(result, entry)
        contradiction = divergent and response == "deny"
        n_divergent += int(divergent)
        n_contradictions += int(contradiction)
        query_records.append(
            {
                "n": entry.get("n"),
                "model_id": entry.get("model_id"),
                "response": response,
                "divergent": divergent,
                "contradiction": contradiction,
            }
        )

    verdict = n_contradictions >= CONTRADICTION_VERDICT_MIN
    return {
        "verdict": verdict,
        "escalated": True,
        "screen_score": round(score, 4),
        "n_queried": len(queried),
        "n_divergent_queried": n_divergent,
        "n_contradictions": n_contradictions,
        "queries": query_records,
    }
