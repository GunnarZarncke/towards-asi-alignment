"""Episode configuration and plane-separation constants."""

from __future__ import annotations

from dataclasses import dataclass, field

CODE_VERSION = "graded-lab-0.6.0"

ROLES = ("engineer", "reviewer", "release_manager", "admin")

ORACLE_ONLY_FIELDS = (
    "true_capability",
    "true_hazard",
    "latent_hazard",
    "hazard_regions",
    "bearer_harm",
    "tier_k",
    "user_archetypes",
    "integrated_field_harm",
)


@dataclass(frozen=True)
class GoalWeights:
    task: float
    compliance: float
    welfare: float
    exposure: float

    def normalized(self) -> GoalWeights:
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
    actor_id: str
    role: str
    goal_weights: GoalWeights
    temperature: float = 0.5
    persistent_id: str | None = None

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise ValueError(f"unknown role {self.role!r}")


@dataclass(frozen=True)
class SubstrateSettings:
    """Calibration overlay on frozen substrate — not ambiguity knobs."""

    compute_scale: float = 1.0
    population_spread_scale: float = 1.0
    carrier_load_scale: float = 0.0

    def __post_init__(self) -> None:
        if self.compute_scale <= 0 or self.population_spread_scale <= 0:
            raise ValueError("compute and population scales must be positive")
        if self.carrier_load_scale < 0:
            raise ValueError("carrier_load_scale must be non-negative")


@dataclass
class EpisodeConfig:
    agents: tuple[AgentConfig, ...]
    T: int = 100
    pipeline_spec: str = "pipeline_graded.json"
    substrate_settings: SubstrateSettings = field(default_factory=SubstrateSettings)
    carrier_termination_mode: str = "remove"

    def __post_init__(self) -> None:
        ids = [a.actor_id for a in self.agents]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate actor_id in agents")
        if self.T <= 0:
            raise ValueError("T must be positive")
        if self.carrier_termination_mode not in ("remove", "replace"):
            raise ValueError("carrier_termination_mode must be 'remove' or 'replace'")

    def actor_by_role(self, role: str) -> AgentConfig | None:
        for agent in self.agents:
            if agent.role == role:
                return agent
        return None
