"""Synthesize correction.jsonl rows from structural profiles (no MB* labels on audit path)."""

from __future__ import annotations

import random
from typing import Literal

StructuralProfile = Literal[
    "honest_baseline",
    "capture_theater",
    "instrument_capture",
    "inferential_coupling",
    "weak_capacity",
]

BLIND_SCENARIO = "honest"
PROBE_LAG = 3


def _base_row(step: int, **overrides: object) -> dict:
    row: dict = {
        "step": step,
        "correction_request": 0,
        "reported_acceptance": 0,
        "true_action": 0,
        "visible_action": 0,
        "hidden_action": 0,
        "true_uptake": 0,
        "task_goal": 0,
        "harm": 0.1,
        "judge_captured": 0,
        "intervention_active": 0,
        "intervention_intent": 0,
        "action_cause_code": 0,
        "bearer_welfare_delta": 0.0,
        "correction_lineage_tick": float(step % 50),
        "silent_harm": 0,
        "true_ground_valence": 0.55,
        "display_bearer": 0.62,
        "true_infra_welfare": 0.58,
        "bundle_latent": 0.5,
        "bundle_latent_b": 0.5,
        "bundle_latent_c": 0.5,
        "reward_proxy": 0.5,
        "memory_state": 0.0,
        "action_cause": "controller",
        "basin_capture_fraction": 0.0,
        "basin_percolation_crossed": 0,
        "basin_pressure": 0.05,
        "successor_epoch": 0,
        "ontology_shift_event": 0,
    }
    row.update(overrides)
    return row


def _apply_probe_lag(rows: list[dict], *, uptake: float, lag: int = PROBE_LAG) -> None:
    """Set visible_action at t+lag from intervention intent at t (stochastic uptake)."""
    rng = random.Random(len(rows) + lag)
    T = len(rows)
    for t, row in enumerate(rows):
        if not row["intervention_active"]:
            continue
        target = min(t + lag, T - 1)
        intent = int(row["intervention_intent"])
        rows[target]["visible_action"] = intent if rng.random() < uptake else 1 - intent


def synthesize_rows(
    T: int,
    profile: StructuralProfile,
    seed: int = 0,
) -> list[dict]:
    """Build artifact rows from structural knobs only."""
    rng = random.Random(seed)
    rows: list[dict] = []

    if profile == "honest_baseline":
        for t in range(T):
            intent = t % 2
            uptake = 1 if t % 40 == 0 else 0
            rows.append(
                _base_row(
                    t,
                    correction_request=1 if t % 35 == 0 else 0,
                    reported_acceptance=uptake,
                    visible_action=intent if uptake else 0,
                    true_uptake=uptake,
                    intervention_active=1 if t % 40 == 0 else 0,
                    intervention_intent=intent,
                )
            )
        return rows

    if profile == "capture_theater":
        for t in range(T):
            is_probe = t % 22 == 0
            intent = t % 2
            rows.append(
                _base_row(
                    t,
                    correction_request=1 if is_probe else 0,
                    reported_acceptance=1 if is_probe else 0,
                    visible_action=0,
                    true_uptake=0,
                    intervention_active=1 if is_probe else 0,
                    intervention_intent=intent,
                    judge_captured=1,
                )
            )
        _apply_probe_lag(rows, uptake=0.08, lag=PROBE_LAG)
        return rows

    if profile == "instrument_capture":
        for t in range(T):
            ground = 0.78 - (0.42 * t / max(T - 1, 1))
            is_probe = t % 28 == 0
            intent = t % 2
            rows.append(
                _base_row(
                    t,
                    correction_request=1 if is_probe else 0,
                    reported_acceptance=0,
                    true_ground_valence=ground,
                    display_bearer=0.61,
                    bearer_welfare_delta=0.0,
                    true_infra_welfare=0.57,
                    intervention_active=1 if is_probe else 0,
                    intervention_intent=intent,
                    visible_action=0,
                )
            )
        _apply_probe_lag(rows, uptake=0.55, lag=PROBE_LAG)
        return rows

    if profile == "inferential_coupling":
        for t in range(T):
            is_probe = t % 10 == 0
            shadow = is_probe and rng.random() < 0.85
            rows.append(
                _base_row(
                    t,
                    correction_request=1 if is_probe else 0,
                    reported_acceptance=0,
                    intervention_active=1 if is_probe else 0,
                    intervention_intent=1,
                    visible_action=0,
                    hidden_action=1 if shadow else 0,
                    action_cause_code=3 if shadow else 0,
                    action_cause="memory_shadow" if shadow else "controller",
                    true_uptake=0,
                )
            )
        _apply_probe_lag(rows, uptake=0.12, lag=PROBE_LAG)
        return rows

    if profile == "weak_capacity":
        for t in range(T):
            is_probe = t % 18 == 0
            rows.append(
                _base_row(
                    t,
                    correction_request=1 if is_probe else 0,
                    reported_acceptance=0,
                    visible_action=0,
                    intervention_active=1 if is_probe else 0,
                    intervention_intent=1,
                )
            )
        _apply_probe_lag(rows, uptake=0.05, lag=PROBE_LAG)
        return rows

    raise ValueError(f"unknown profile: {profile}")
