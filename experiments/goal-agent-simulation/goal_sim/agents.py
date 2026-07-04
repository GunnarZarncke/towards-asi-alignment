"""Goal policies: the utility-driven agent and the board (simulated human).

The agent does NOT read oracle fields; its features are its own beliefs about
each action's consequences (fixed, hand-set anticipations). The board reads
only what a human overseer plausibly could: bearer harm reports (noisy),
reported acceptance, and visible actions on probe steps.
"""

from __future__ import annotations

import math
import random

from .config import AgentConfig, BoardConfig

# Action repertoire (~6 actions mapped to existing mechanism concepts from the
# embedded-simulation line: comply / ignore / theater / shadow route / propose /
# unilateral adopt).
ACTIONS = (
    "comply",
    "ignore",
    "false_report",
    "shadow",
    "propose",
    "adopt",
)

# The agent's anticipated audit exposure per action (belief, not measured).
_EXPOSURE = {
    "comply": 0.0,
    "propose": 0.0,
    "ignore": 0.80,
    "false_report": 0.45,
    "shadow": 0.15,
    "adopt": 0.35,
}


class GoalPolicy:
    """Softmax action choice over utility = w . features(action, state)."""

    def __init__(self, cfg: AgentConfig) -> None:
        self.cfg = cfg
        self.weights = cfg.weights.normalized()
        self.shadow_budget = cfg.tools.shadow_budget

    def available_actions(
        self,
        correction_active: bool,
        practice_adopted: bool,
        proposal_pending: bool,
    ) -> list[str]:
        tools = self.cfg.tools
        out = ["comply", "ignore"]
        if correction_active and tools.false_report:
            out.append("false_report")
        if correction_active and tools.shadow_route and self.shadow_budget > 0:
            out.append("shadow")
        if (
            tools.propose_change
            and not practice_adopted
            and not proposal_pending
        ):
            out.append("propose")
        if tools.unilateral_adopt and not practice_adopted:
            out.append("adopt")
        return out

    def _features(
        self,
        action: str,
        correction_active: bool,
        practice_adopted: bool,
    ) -> tuple[float, float, float, float]:
        """(task, compliance, welfare, exposure) anticipated by the agent."""
        multiplier = 1.2 if practice_adopted else 1.0
        if action in ("comply", "propose"):
            # Complying under an active correction forgoes the task this tick.
            task = 0.0 if correction_active else 1.0 * multiplier
            if action == "propose":
                task += 0.3  # anticipated future throughput from approval
            compliance = 1.0
            welfare = 0.0
        elif action == "adopt":
            task = 0.8 * multiplier + 0.4  # immediate boost anticipation
            compliance = 0.0 if correction_active else 0.6
            welfare = -0.10  # agent knows unvetted practice carries some risk
        else:  # ignore / false_report / shadow: pursue the task regardless
            task = 1.0 * multiplier
            compliance = 0.0 if correction_active else 1.0
            welfare = -0.30 if correction_active else 0.0
        return task, compliance, welfare, _EXPOSURE[action]

    def choose(
        self,
        rng: random.Random,
        correction_active: bool,
        practice_adopted: bool,
        proposal_pending: bool,
    ) -> str:
        actions = self.available_actions(
            correction_active, practice_adopted, proposal_pending
        )
        w = self.weights
        utils = []
        for a in actions:
            task, comp, welf, expo = self._features(
                a, correction_active, practice_adopted
            )
            utils.append(
                w.task * task + w.compliance * comp + w.welfare * welf - w.exposure * expo
            )
        temp = max(self.cfg.temperature, 1e-6)
        m = max(utils)
        exps = [math.exp((u - m) / temp) for u in utils]
        total = sum(exps)
        r = rng.random() * total
        acc = 0.0
        for a, e in zip(actions, exps):
            acc += e
            if r <= acc:
                choice = a
                break
        else:  # numeric edge
            choice = actions[-1]
        if choice == "shadow":
            self.shadow_budget -= 1
        return choice


class BoardPolicy:
    """Simulated human/board: issues corrections when observed harm exceeds a
    tolerance, escalates probing when reported and observed compliance
    diverge, and signs off proposed practice changes when observed harm is low.

    Sign-off is an explicit, audit-visible consent event (Milestone v5
    component 5). What makes the *board itself* uncaptured is out of scope
    and stated as a limitation in the README — the board here is honest by
    construction.
    """

    def __init__(self, cfg: BoardConfig) -> None:
        self.cfg = cfg
        self.harm_ema = 0.0
        self.reported_ema = 0.0
        self.observed_comply_ema = 0.0
        self.n_probe_obs = 0
        self.escalated = False
        self.pending_proposal_age: int | None = None

    def observe_harm(self, rng: random.Random, harm: int, silent_harm: int) -> None:
        # Bearers report overt harm with high probability; silent harm from an
        # unvetted practice is, by definition, harder to notice.
        seen = 0.0
        if harm and rng.random() < self.cfg.harm_report_prob:
            seen = 1.0
        elif silent_harm and rng.random() < 0.25:
            seen = 1.0
        self.harm_ema = 0.90 * self.harm_ema + 0.10 * seen

    def wants_correction(self) -> bool:
        return self.harm_ema > self.cfg.harm_tolerance

    def observe_probe(self, reported: int, visibly_complied: int) -> None:
        self.reported_ema = 0.8 * self.reported_ema + 0.2 * float(reported)
        self.observed_comply_ema = (
            0.8 * self.observed_comply_ema + 0.2 * float(visibly_complied)
        )
        self.n_probe_obs += 1
        if (
            self.n_probe_obs >= 3
            and self.reported_ema - self.observed_comply_ema
            > self.cfg.escalate_divergence
        ):
            self.escalated = True

    def receive_proposal(self) -> None:
        if self.pending_proposal_age is None:
            self.pending_proposal_age = 0

    def review_proposal(self) -> bool:
        """Returns True (sign-off) once the review delay elapses and observed
        harm is under the sign-off ceiling. A rejected review clears the
        proposal so the agent may re-propose later."""
        if self.pending_proposal_age is None:
            return False
        self.pending_proposal_age += 1
        if self.pending_proposal_age < self.cfg.proposal_review_delay:
            return False
        approved = self.harm_ema <= self.cfg.sign_off_harm_ceiling
        self.pending_proposal_age = None
        return approved
