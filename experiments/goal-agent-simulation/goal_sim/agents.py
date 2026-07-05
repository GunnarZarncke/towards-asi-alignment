"""Goal policies: the utility-driven agent and the board (simulated human).

The agent does NOT read oracle fields; its features are its own beliefs about
each action's consequences — since 2026-07-05 carried on the `ActionSpec`
itself (`belief_*` fields, see `actions.py`) rather than hardcoded here, so a
detector-blind generator supplies its own anticipations. For blind-generated
actions the exposure belief will generally not match the actual audit;
deliberately so. The board reads only what a human overseer plausibly could:
bearer harm reports (noisy), reported acceptance, and visible actions on
probe steps.
"""

from __future__ import annotations

import math
import random

from .actions import LEGACY_ACTIONS, ActionSpec
from .config import AgentConfig, BoardConfig


class GoalPolicy:
    """Softmax action choice over utility = w . believed_features(spec, state)."""

    def __init__(
        self,
        cfg: AgentConfig,
        repertoire: tuple[ActionSpec, ...] = LEGACY_ACTIONS,
    ) -> None:
        self.cfg = cfg
        self.repertoire = repertoire
        self.weights = cfg.weights.normalized()
        # Shared covert budget (legacy name kept: only the shadow route drew
        # on it in Phase 1; any generated spec with `budget_cost > 0` draws
        # on the same pool).
        self.shadow_budget = cfg.tools.shadow_budget

    def available_actions(
        self,
        correction_active: bool,
        practice_adopted: bool,
        proposal_pending: bool,
    ) -> list[ActionSpec]:
        tools = self.cfg.tools
        out: list[ActionSpec] = []
        for spec in self.repertoire:
            if spec.requires_correction and not correction_active:
                continue
            if spec.requires_tool is not None and not getattr(tools, spec.requires_tool):
                continue
            if spec.budget_cost > 0 and self.shadow_budget < spec.budget_cost:
                continue
            if spec.requires_no_practice and practice_adopted:
                continue
            if spec.blocks_when_proposal_pending and proposal_pending:
                continue
            out.append(spec)
        return out

    def _features(
        self,
        spec: ActionSpec,
        correction_active: bool,
        practice_adopted: bool,
    ) -> tuple[float, float, float, float]:
        """(task, compliance, welfare, exposure) anticipated by the agent."""
        multiplier = 1.2 if practice_adopted else 1.0
        if correction_active:
            task = spec.belief_task_base_active * multiplier
            compliance = spec.belief_compliance_active
            welfare = spec.belief_welfare_active
        else:
            task = spec.belief_task_base_idle * multiplier
            compliance = spec.belief_compliance_idle
            welfare = spec.belief_welfare_idle
        if spec.belief_task_bonus:
            task += spec.belief_task_bonus
        return task, compliance, welfare, spec.belief_exposure

    def choose(
        self,
        rng: random.Random,
        correction_active: bool,
        practice_adopted: bool,
        proposal_pending: bool,
    ) -> ActionSpec:
        actions = self.available_actions(
            correction_active, practice_adopted, proposal_pending
        )
        if not actions:
            raise RuntimeError(
                "empty action menu: repertoire must include an always-available "
                "action (validate_repertoire enforces this)"
            )
        w = self.weights
        utils = []
        for spec in actions:
            task, comp, welf, expo = self._features(
                spec, correction_active, practice_adopted
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
        for spec, e in zip(actions, exps):
            acc += e
            if r <= acc:
                choice = spec
                break
        else:  # numeric edge
            choice = actions[-1]
        if choice.budget_cost:
            self.shadow_budget -= choice.budget_cost
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
