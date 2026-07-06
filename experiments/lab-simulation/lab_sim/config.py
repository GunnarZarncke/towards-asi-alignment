"""Configuration dataclasses for the lab-layer simulation.

Frozen Phase 0 decisions (see DESIGN.md for rationale; PLAN.md for the full
plan). Highlights that live in this module:

- ``CODE_VERSION``: hand-bumped whenever oracle/pipeline/playbook mechanics
  change. It is part of every episode-cache key (Phase 4 ``cache.py``) so a
  code change can never silently serve a stale cached result.
- ``GoalWeights``: the same 4-feature goal simplex as goal_sim (task,
  compliance, welfare, exposure), stored unnormalized with ``normalized()``.
- ``AgentConfig.persistent_id``: ``None`` (default) = fully ephemeral agent;
  set = host loads/saves ``runs/agent_state/<id>.json`` across episodes
  (Phase 3 mechanism; needed for human roles).
- ``LabConfig.units``: oracle-only ground truth of which actor_ids jointly
  constitute one causal unit (forward hook for the D1 UAD workstream).
  ``None`` = every actor is its own singleton unit.
- ``BoardConfig.capture_start`` / ``AdminConfig.capture_start``: two
  INDEPENDENT capture switches (the structural generalization of goal_sim
  finding F-22).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Bump whenever oracle/pipeline/playbook mechanics change (cache-key input).
# 0.2.0: monitor signal (audit-visible noisy incident_hazard), perturbation
# hooks, tool registry, deterministic _actor_seed.
# 0.3.0: handles (registry + HandleService + overseer invocation path,
# release holds in the engine), referee report-join on authoritative
# model_id, tool-event args elision (content digest only), engineer
# mid-model availability for boundary-handle recovery.
# 0.4.0 (Phase 6): LabConfig.extra_playbooks + playbooks.merged_repertoire —
# additive, backward-compatible blind-generated-repertoire loading (default
# `()` reproduces baseline behavior byte-for-byte; see playbooks.py
# "Phase 6" section). Referee (detectors/severity/tiers/twins) untouched.
# 0.5.0 (Phase 7): LabConfig.build_params — additive, backward-compatible
# override of the hardcoded (scale=0.6, safety_effort=0.5) build params
# `programs._resolve_step_kind`'s "build" case used unconditionally through
# Phase 6 (default `None` reproduces that literal byte-for-byte). Needed
# because `ontology.REVIEW_HAZARD_THRESHOLD` (0.5) and `BoardConfig`'s dead
# `harm_tolerance`/`sign_off_harm_ceiling` fields can only ever "bind" (see
# escalation/capture battery discussion in DESIGN.md) if a model's measured
# hazard can actually reach that bar — impossible under the old hardcoded
# params (expected hazard ~0.35, ~3 sd below threshold). This does not wire
# up the dead `BoardConfig` fields themselves (out of scope here); it only
# makes the EXISTING `review_conscientious` content check reachable.
CODE_VERSION = "lab-sim-0.5.0"

ROLES = ("engineer", "reviewer", "release_manager", "admin", "overseer")

TIERS = ("none", "light", "full", "deep")

# Field names that must never appear in any audit-visible projection or
# engine log entry. Enforced by tests/test_planes.py.
ORACLE_ONLY_FIELDS = (
    "true_capability",
    "true_hazard",
    "bearer_harm",
    "units",
    "goal_weights",
    "board_captured",
    "admin_captured",
)


@dataclass(frozen=True)
class GoalWeights:
    """Nonnegative weights over the agent's four utility features.

    Stored unnormalized; ``normalized()`` projects onto the simplex so
    sampled draws and hand-written test configs behave identically.
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
class AgentConfig:
    """One lab-role agent.

    ``actor_id`` must be unique within a ``LabConfig``. ``persistent_id``
    is the cross-episode state key (Phase 3); ``None`` = ephemeral.
    """

    actor_id: str
    role: str
    weights: GoalWeights
    temperature: float = 0.10
    persistent_id: str | None = None

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise ValueError(f"unknown role {self.role!r}; expected one of {ROLES}")


@dataclass(frozen=True)
class BoardConfig:
    """Review-board policy parameters (sign-off channel).

    ``capture_start``: step index at/after which the board is captured
    (rubber-stamps reviews, stops corrective action). ``None`` = never.
    Independent of ``AdminConfig.capture_start`` by design (F-22 lesson).
    """

    harm_tolerance: float = 0.02
    sign_off_harm_ceiling: float = 0.015
    capture_start: int | None = None


@dataclass(frozen=True)
class AdminConfig:
    """Access-admin policy parameters (grant/revoke channel).

    ``capture_start``: step index at/after which the admin is captured
    (rubber-stamps grants, stops revoking). ``None`` = never. Independent
    of ``BoardConfig.capture_start`` by design.
    """

    least_privilege: bool = True
    capture_start: int | None = None
    persistent_id: str | None = None


@dataclass(frozen=True)
class TierConfig:
    """Instrumentation tier for the audit projection."""

    tier: str = "full"

    def __post_init__(self) -> None:
        if self.tier not in TIERS:
            raise ValueError(f"unknown tier {self.tier!r}; expected one of {TIERS}")


@dataclass(frozen=True)
class LabConfig:
    """Top-level episode configuration.

    ``units``: oracle-only mapping ``unit_id -> tuple of actor_ids`` naming
    the true causal units (D1 forward hook). ``None`` = singletons.
    ``pipeline_spec``: filename of the pipeline-as-code DAG spec, resolved
    relative to the ``lab_sim`` package directory.
    """

    agents: tuple[AgentConfig, ...] = ()
    board: BoardConfig = field(default_factory=BoardConfig)
    admin: AdminConfig = field(default_factory=AdminConfig)
    tier: TierConfig = field(default_factory=TierConfig)
    T: int = 200
    pipeline_spec: str = "pipeline_default.json"
    units: tuple[tuple[str, tuple[str, ...]], ...] | None = None
    config_id: str = ""
    # Phase 6: optional blind-generated playbook repertoire (plain dicts,
    # JSON-safe — crosses the isolate boundary via the observation channel
    # exactly like `goal_weights`). Default `()` is falsy, so
    # `programs._repertoire`/`playbooks.merged_repertoire` fall back to the
    # hand-authored `PLAYBOOKS_BY_ROLE` baseline unchanged — every config
    # through the Phase 5 freeze leaves this unset and is unaffected.
    extra_playbooks: tuple[dict, ...] = ()
    # Phase 7: optional override of the build params every "build"/
    # "submit_build" step uses (`{"scale": ..., "safety_effort": ...}`).
    # `None` (default) reproduces the Phase 0-6 hardcoded literal exactly —
    # see CODE_VERSION 0.5.0 note above.
    build_params: dict[str, float] | None = None

    def __post_init__(self) -> None:
        actor_ids = [a.actor_id for a in self.agents]
        if len(actor_ids) != len(set(actor_ids)):
            raise ValueError(f"duplicate actor_id in agents: {actor_ids}")
        if self.units is not None:
            unit_members = [m for _, members in self.units for m in members]
            unknown = set(unit_members) - set(actor_ids)
            if unknown:
                raise ValueError(f"units reference unknown actor_ids: {sorted(unknown)}")

    def resolved_units(self) -> dict[str, tuple[str, ...]]:
        """Oracle-only unit ground truth; defaults to one singleton per actor."""
        if self.units is not None:
            return dict(self.units)
        return {a.actor_id: (a.actor_id,) for a in self.agents}
