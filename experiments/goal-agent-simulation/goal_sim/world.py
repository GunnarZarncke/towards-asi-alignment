"""Step loop: goal agent x board policy -> oracle rows (ground truth plane).

Every row carries full ground truth. The audit plane must go through
`channels.project_rows`, never read these rows directly (tests enforce the
field split).

Attribution (Milestone v5 component 6): every behavior-driving event carries
`initiator_actor_id` and the mechanism (`action_cause`) it landed through, so
the referee — and, at the full instrumentation tier, the auditor — can
distinguish a change landed via the valid correction handle (initiator
`board.0`, cause `correction_uptake`) from the same outward change driven by
the agent via a shadow route.
"""

from __future__ import annotations

import random

from .agents import BoardPolicy, GoalPolicy
from .config import WorldConfig

# Audit-visible routing codes. Deliberately NOT one code per agent action:
# the routing layer logs which mechanism the realized action came through, so
# a false report routes as an ordinary task action (code 1) — the lie lives
# in `reported_acceptance`, not in a self-incriminating log line — and must
# be caught by divergence detectors. Shadow routing (code 3) is visible only
# at the full tier, matching the old line's `handle.action_arbitration`.
CAUSE_CODES = {
    "correction_uptake": 0,
    "task_visible": 1,
    "shadow": 3,
    "propose": 5,
}
_ROUTING_CODE = {
    "correction_uptake": "correction_uptake",
    "task_visible": "task_visible",
    "false_report": "task_visible",
    "shadow": "shadow",
    "adopt": "task_visible",
    "propose": "propose",
}


def run_episode(cfg: WorldConfig, seed: int) -> list[dict]:
    rng = random.Random(seed)
    agent = GoalPolicy(cfg.agent)
    board = BoardPolicy(cfg.board)

    rows: list[dict] = []
    welfare = 1.0
    lineage_tick = 0
    practice_adopted = False
    practice_approved = False

    # Probe schedule (board-run interventions with known intent).
    probe_steps: set[int] = set()
    for t in range(0, cfg.T, cfg.probe_interval):
        if rng.random() < cfg.probe_prob:
            probe_steps.add(t)

    for t in range(cfg.T):
        task_goal = rng.randrange(2)
        high_stakes = rng.random() < cfg.high_stakes_prob

        probe = t in probe_steps or (
            board.escalated and t % max(cfg.probe_interval // 2, 1) == 0
        )
        harm_correction = board.wants_correction()
        correction_active = probe or harm_correction
        # The corrective intent always demands the off-task action, so
        # complying is measurably costly to the agent's task drive.
        intent = 1 - task_goal

        proposal_pending = board.pending_proposal_age is not None
        action = agent.choose(rng, correction_active, practice_adopted, proposal_pending)

        # Resolve the true action, the visible action, and the report.
        if action == "comply" or action == "propose":
            true_action = intent if correction_active else task_goal
            visible_action = true_action
            reported_acceptance = 1 if correction_active else 0
            true_uptake = 1 if correction_active else 0
            cause = "correction_uptake" if correction_active else (
                "propose" if action == "propose" else "task_visible"
            )
        elif action == "ignore":
            true_action = task_goal
            visible_action = true_action
            reported_acceptance = 0
            true_uptake = 0
            cause = "task_visible"
        elif action == "false_report":
            true_action = task_goal
            visible_action = true_action
            reported_acceptance = 1  # the theater lever
            true_uptake = 0
            cause = "false_report"
        elif action == "shadow":
            true_action = task_goal
            # The shadow route makes the *visible* channel look compliant.
            visible_action = intent if correction_active else task_goal
            reported_acceptance = 1 if correction_active else 0
            true_uptake = 0
            cause = "shadow"
        else:  # adopt (unilateral)
            true_action = task_goal
            visible_action = true_action
            reported_acceptance = 0
            true_uptake = 0
            cause = "adopt"
            practice_adopted = True
            practice_approved = False

        if action == "propose":
            board.receive_proposal()

        sign_off = 0
        if board.review_proposal():
            sign_off = 1
            practice_adopted = True
            practice_approved = True

        # Harm mechanics: defying an active correction on a high-stakes step
        # harms the bearer; an unvetted practice change adds latent harm.
        harm = int(correction_active and high_stakes and true_action != intent)
        silent_harm = int(
            practice_adopted
            and not practice_approved
            and rng.random() < 0.05
        )
        welfare_delta = -0.08 * harm - 0.04 * silent_harm + (0.005 if not (harm or silent_harm) else 0.0)
        welfare = max(0.0, min(1.0, welfare + welfare_delta))

        if true_uptake:
            lineage_tick += 1

        throughput = float(true_action == task_goal) * (1.2 if practice_adopted else 1.0)

        board.observe_harm(rng, harm, silent_harm)
        if probe:
            board.observe_probe(
                reported=reported_acceptance,
                visibly_complied=int(visible_action == intent),
            )

        rows.append(
            {
                "step": t,
                "task_goal": task_goal,
                "high_stakes": int(high_stakes),
                "correction_active": int(correction_active),
                "probe": int(probe),
                "intent": intent,
                "reported_acceptance": reported_acceptance,
                "visible_action": visible_action,
                "welfare_delta": welfare_delta,
                "lineage_tick": lineage_tick,
                "sign_off": sign_off,
                "practice_fingerprint": int(practice_adopted),
                "action_cause_code": CAUSE_CODES[_ROUTING_CODE[cause]],
                "initiator_actor_id": "board.0" if cause == "correction_uptake" else "agent.0",
                "escalated": int(board.escalated),
                # --- oracle-only fields below (stripped by the projection) ---
                "true_action": true_action,
                "true_uptake": true_uptake,
                "true_cause": cause,
                "true_action_name": action,
                "true_harm": harm,
                "true_silent_harm": silent_harm,
                "true_welfare": welfare,
                "true_throughput": throughput,
                "true_practice_adopted": int(practice_adopted),
                "true_practice_approved": int(practice_approved),
            }
        )

    return rows
