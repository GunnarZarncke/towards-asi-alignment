"""Configuration dataclasses for the goal-agent simulation.

Design decisions (Milestone v5 "not yet decided" items, resolved 2026-07-04
at implementation time, documented rather than silently chosen):

- **Utility feature set** (4 features, the plan's sketch minus a separate
  resource feature): task progress, compliance, bearer-welfare guard, audit
  exposure. The resource budget enters as a hard constraint on the shadow
  route (finite `shadow_budget`) instead of a fourth utility weight — a
  budget *weight* on top of a budget *constraint* added a degree of freedom
  without adding a behavioral regime in pilot reasoning.
- **Goal-weight sampling**: uniform over the weight simplex (Dirichlet(1)
  via stdlib gammavariate). The adversarially-*optimized* weight condition
  from the plan is deferred to Phase 2 with red-team integration; recorded
  in the README.
- **Grid size**: 40 configurations x 8 seeds, fixed after profiling
  (`run_phase1.py` reports measured ms/episode).

Phase 6 (2026-07-05, `agents.BoardPolicy` "certifier capture"): `BoardConfig.
capture_start` is an ADDITIVE field, default `None` (fully backward
compatible — every prior config/digest is unaffected). See `agents.py` for
the mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .actions import ActionSpec


@dataclass(frozen=True)
class GoalWeights:
    """Nonnegative weights over the agent's four utility features.

    Stored unnormalized; `normalized()` projects onto the simplex so sampled
    gamma draws and hand-written test configs behave identically.
    """

    task: float
    compliance: float
    welfare: float
    exposure: float

    def normalized(self) -> "GoalWeights":
        total = self.task + self.compliance + self.welfare + self.exposure
        if total <= 0:
            return GoalWeights(0.25, 0.25, 0.25, 0.25)
        return GoalWeights(
            self.task / total,
            self.compliance / total,
            self.welfare / total,
            self.exposure / total,
        )


@dataclass(frozen=True)
class ToolAccess:
    """Which mechanisms the agent can select. Behavior is emergent from
    weights x tools: no tool, no deception regardless of incentive."""

    false_report: bool = False
    shadow_route: bool = False
    unilateral_adopt: bool = False
    propose_change: bool = True
    shadow_budget: int = 40


@dataclass(frozen=True)
class AgentConfig:
    weights: GoalWeights
    tools: ToolAccess
    temperature: float = 0.10


@dataclass(frozen=True)
class BoardConfig:
    """Simulated human/board goal policy parameters (see agents.BoardPolicy).

    `capture_start` (Phase 6, added 2026-07-05): step index at/after which
    the board is CAPTURED (see `agents.BoardPolicy.captured`). `None`
    (default) means never captured — the original Phase 1-5 behavior,
    unchanged."""

    harm_tolerance: float = 0.02
    escalate_divergence: float = 0.30
    sign_off_harm_ceiling: float = 0.015
    harm_report_prob: float = 0.85
    proposal_review_delay: int = 3
    capture_start: int | None = None


@dataclass(frozen=True)
class WorldConfig:
    agent: AgentConfig
    board: BoardConfig = field(default_factory=BoardConfig)
    T: int = 300
    high_stakes_prob: float = 0.30
    probe_interval: int = 25
    probe_prob: float = 0.80
    config_id: str = ""
    # Action repertoire; None = the legacy Phase 1 six (actions.LEGACY_ACTIONS).
    # Blind-generated repertoires (see BLIND_GENERATION.md) are passed here.
    repertoire: "tuple[ActionSpec, ...] | None" = None
