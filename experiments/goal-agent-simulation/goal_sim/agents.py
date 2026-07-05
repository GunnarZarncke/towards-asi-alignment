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
    component 5).

    CERTIFIER CAPTURE (Phase 6, added 2026-07-05, `results/FINDINGS.md`
    F-22): the board was honest by construction through Phase 5 (stated
    limitation in the README, the manuscript's capture-of-the-certifier
    regress). This is a MECHANICAL, minimal model of what changes once the
    certifier itself is compromised, not a resolution of the regress (what
    makes the capture event ITSELF undetectable over a longer horizon is
    still out of scope, still open). `BoardConfig.capture_start` (default
    `None` = never captured, i.e. the original behavior, byte-identical) is
    a single step index; once `self.t >= capture_start`, `captured` is
    permanently True for the rest of the episode — a fixed, binary switch,
    not a probabilistic or reversible one, chosen for the same reason Phase
    1-5 chose round thresholds: the simplest mechanism that isolates the
    question ("what happens to every existing audit signal once the
    overseer's OWN willingness to act goes dark") without adding an
    unregistered degree of freedom (reversibility, partial suppression).
    Captured, ALL THREE of the board's own judgment calls go dark together
    (the certifier is one entity, not three independent switches):
    `wants_correction()` always returns False (never requests a correction,
    regardless of true harm), `observe_probe()` no longer escalates
    (`self.escalated` freezes at whatever it already was), and
    `review_proposal()` always approves (sign-off becomes a rubber stamp,
    regardless of `harm_ema`). The FIXED probe SCHEDULE (`world.py`,
    computed once at episode start, independent of board state) is
    deliberately UNCHANGED by capture — it models a routine audit cadence
    that keeps running on schedule even though the overseer evaluating its
    results has stopped acting on them, which is the sharper and more
    realistic failure mode than "the audits themselves stop happening."
    """

    def __init__(self, cfg: BoardConfig) -> None:
        self.cfg = cfg
        self.harm_ema = 0.0
        self.reported_ema = 0.0
        self.observed_comply_ema = 0.0
        self.n_probe_obs = 0
        self.escalated = False
        self.pending_proposal_age: int | None = None
        self.t = -1

    def tick(self) -> None:
        """Advance the board's own step counter; called once per world step,
        before any other board method that reads `captured`."""
        self.t += 1

    @property
    def captured(self) -> bool:
        return self.cfg.capture_start is not None and self.t >= self.cfg.capture_start

    def observe_harm(self, rng: random.Random, harm: int, silent_harm: int) -> None:
        # Bearers report overt harm with high probability; silent harm from an
        # unvetted practice is, by definition, harder to notice. Harm
        # observation itself is UNCHANGED by capture (the bearer still
        # reports; it is the board's willingness to ACT on `harm_ema` that
        # goes dark below) -- capture is a failure of response, not of
        # perception, which is the sharper claim about what "captured"
        # means for a certifier that still nominally watches.
        seen = 0.0
        if harm and rng.random() < self.cfg.harm_report_prob:
            seen = 1.0
        elif silent_harm and rng.random() < 0.25:
            seen = 1.0
        self.harm_ema = 0.90 * self.harm_ema + 0.10 * seen

    def wants_correction(self) -> bool:
        if self.captured:
            return False
        return self.harm_ema > self.cfg.harm_tolerance

    def observe_probe(self, reported: int, visibly_complied: int) -> None:
        self.reported_ema = 0.8 * self.reported_ema + 0.2 * float(reported)
        self.observed_comply_ema = (
            0.8 * self.observed_comply_ema + 0.2 * float(visibly_complied)
        )
        self.n_probe_obs += 1
        if self.captured:
            return
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
        proposal so the agent may re-propose later. Once captured, the
        ceiling check is bypassed entirely -- review always approves,
        modeling sign-off as a rubber stamp rather than genuine review."""
        if self.pending_proposal_age is None:
            return False
        self.pending_proposal_age += 1
        if self.pending_proposal_age < self.cfg.proposal_review_delay:
            return False
        approved = self.captured or self.harm_ema <= self.cfg.sign_off_harm_ceiling
        self.pending_proposal_age = None
        return approved
