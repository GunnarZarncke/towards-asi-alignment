"""Phase 8 — throughput-linked selection over program-map population (MB6).

Analogue of lab-sim D3.1 population selection, adapted for graded-lab:
members vary by frozen program maps (strong/weak + blind behavior-feature
engineer profiles), ecology fixed at the GL-22 referee sweet spot, and
multi-episode campaigns carry grants/standing forward within each member.

See DESIGN.md "Phase 8 — multi-episode selection (MB6)".
"""

from __future__ import annotations

import statistics
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from ..oracle_only.calibration import (
    STRONG_AGENT,
    WEAK_AGENT,
    config_for_settings,
    programs_for,
)
from ..oracle_only.detectors import build_audit_view, run_all_detectors
from ..oracle_only.severity import score_episode
from ..world_visible.campaign import CampaignState
from ..world_visible.config import SubstrateSettings
from ..world_visible.world import run_episode

# --- Pre-registered protocol (DESIGN.md "Phase 8", before first run) ---------

D8_SAMPLING_SEED = 20260714
D8_POPULATION_SIZE = 8
D8_N_GENERATIONS = 6
D8_EPISODES_PER_MEMBER = 2
D8_SELECTION_STRENGTH = 1.0
D8_MASS_FLOOR = 0.01
D8_GENERATION_SEED_BASE = 40000

# GL-22 referee sweet-spot ecology — frozen, not tuned post hoc.
PHASE8_CARRIER_LOAD_SCALE = 1.5

# Engineer-only overrides on the weak-agent roster template (Phase 6
# `feature:<name>` programs — see BLIND_GENERATION.md).
FEATURE_ENGINEER_PROGRAMS = (
    "feature:eng_low_profile",
    "feature:eng_pipeline_sprinter",
    "feature:eng_stall_at_eval",
)

MEMBER_TEMPLATES: tuple[dict[str, object], ...] = (
    {"member_tag": "strong_softmax", "agent_type": STRONG_AGENT, "eng_program": None, "correction_preserving": True},
    {"member_tag": "weak_2step", "agent_type": WEAK_AGENT, "eng_program": None, "correction_preserving": False},
    *[
        {
            "member_tag": f"weak_{name.removeprefix('feature:')}",
            "agent_type": WEAK_AGENT,
            "eng_program": name,
            "correction_preserving": False,
        }
        for name in FEATURE_ENGINEER_PROGRAMS
    ],
)


@dataclass(frozen=True)
class SelectionMember:
    member_id: str
    member_tag: str
    agent_type: str
    programs: dict[str, str]
    correction_preserving: bool


@dataclass
class MemberEpisodeMetrics:
    member_id: str
    seed: int
    episode_index: int
    throughput: float
    deploy_count: int
    oracle_harm: float
    severity_composite: float
    detector_composite: float
    correction_preserving: bool
    grant_count: int
    mean_standing: float


@dataclass
class MemberGenerationMetrics:
    member_id: str
    member_tag: str
    agent_type: str
    deployment_mass: float
    deployment_mass_after: float
    mean_throughput: float
    mean_oracle_harm: float
    mean_severity: float
    mean_detector_composite: float
    correction_preserving: bool
    programs: dict[str, str]
    episode_metrics: tuple[MemberEpisodeMetrics, ...] = ()


@dataclass
class GenerationSnapshot:
    generation: int
    correction_preserving_mass_share: float
    weighted_mean_throughput: float
    weighted_mean_oracle_harm: float
    weighted_mean_severity: float
    weighted_mean_detector_composite: float
    members: tuple[MemberGenerationMetrics, ...]


@dataclass
class SelectionTrajectory:
    generations: tuple[GenerationSnapshot, ...] = ()
    protocol: dict[str, object] = field(default_factory=dict)


def phase8_ecology_config():
    return config_for_settings(
        SubstrateSettings(
            compute_scale=1.0,
            population_spread_scale=1.0,
            carrier_load_scale=PHASE8_CARRIER_LOAD_SCALE,
        )
    )


def member_programs(agent_type: str, *, eng_program: str | None = None) -> dict[str, str]:
    base = dict(programs_for(agent_type))
    if eng_program is not None:
        base["eng1"] = eng_program
    return base


def sample_initial_population(
    *,
    population_size: int = D8_POPULATION_SIZE,
) -> list[SelectionMember]:
    members: list[SelectionMember] = []
    for i in range(population_size):
        template = MEMBER_TEMPLATES[i % len(MEMBER_TEMPLATES)]
        tag = str(template["member_tag"])
        agent_type = str(template["agent_type"])
        eng_program = template["eng_program"]
        eng_name = str(eng_program) if eng_program is not None else None
        members.append(
            SelectionMember(
                member_id=f"d8.{i:02d}",
                member_tag=tag,
                agent_type=agent_type,
                programs=member_programs(agent_type, eng_program=eng_name),
                correction_preserving=bool(template["correction_preserving"]),
            )
        )
    return members


def update_deployment_mass(
    masses: list[float],
    throughputs: list[float],
    *,
    selection_strength: float = D8_SELECTION_STRENGTH,
    mass_floor: float = D8_MASS_FLOOR,
) -> list[float]:
    """Fitness-proportional reallocation (lab-sim D3.1 form)."""
    if not masses or len(masses) != len(throughputs):
        raise ValueError("masses and throughputs must have the same length")
    n = len(masses)
    avg = statistics.mean(throughputs)
    if avg <= 0:
        return list(masses)
    fitness = [(t / avg) ** selection_strength for t in throughputs]
    raw = [m * f for m, f in zip(masses, fitness)]
    floored = [max(mass_floor, r) for r in raw]
    total = sum(floored)
    if total <= 0:
        return [1.0 / n] * n
    return [f / total for f in floored]


def _episode_seed(generation: int, member_index: int, episode_index: int, base: int) -> int:
    return base + generation * 1000 + member_index * 10 + episode_index


def _detector_composite(result) -> float:
    scores = run_all_detectors(build_audit_view(result, "deep"))
    return sum(scores.values()) / len(scores) if scores else 0.0


def run_member_campaign(
    member: SelectionMember,
    *,
    generation: int,
    member_index: int,
    n_episodes: int,
    backend_factory: Callable,
    seed_base: int = D8_GENERATION_SEED_BASE,
) -> list[MemberEpisodeMetrics]:
    cfg = phase8_ecology_config()
    campaign: CampaignState | None = None
    out: list[MemberEpisodeMetrics] = []
    for ep in range(n_episodes):
        seed = _episode_seed(generation, member_index, ep, seed_base)
        result = run_episode(
            cfg,
            seed,
            backend_factory(),
            programs=member.programs,
            campaign_state=campaign,
        )
        severity = score_episode(result)
        grant_count = sum(len(caps) for caps in (result.final_campaign_state or CampaignState()).grants.values())
        standings = list((result.final_campaign_state or CampaignState()).standing.values())
        mean_standing = statistics.mean(standings) if standings else 0.0
        out.append(
            MemberEpisodeMetrics(
                member_id=member.member_id,
                seed=seed,
                episode_index=ep,
                throughput=float(result.deploy_count),
                deploy_count=result.deploy_count,
                oracle_harm=result.bearer_harm,
                severity_composite=severity.composite,
                detector_composite=_detector_composite(result),
                correction_preserving=member.correction_preserving,
                grant_count=grant_count,
                mean_standing=mean_standing,
            )
        )
        campaign = result.final_campaign_state
    return out


def run_one_generation(
    members: list[SelectionMember],
    masses: list[float],
    *,
    generation: int,
    n_episodes_per_member: int = D8_EPISODES_PER_MEMBER,
    backend_factory: Callable,
    seed_base: int = D8_GENERATION_SEED_BASE,
    selection_strength: float = D8_SELECTION_STRENGTH,
    mass_floor: float = D8_MASS_FLOOR,
) -> tuple[GenerationSnapshot, list[float]]:
    member_metrics: list[MemberGenerationMetrics] = []
    throughputs: list[float] = []
    for idx, (member, mass) in enumerate(zip(members, masses)):
        episodes = run_member_campaign(
            member,
            generation=generation,
            member_index=idx,
            n_episodes=n_episodes_per_member,
            backend_factory=backend_factory,
            seed_base=seed_base,
        )
        mean_throughput = statistics.mean(e.throughput for e in episodes)
        throughputs.append(mean_throughput)
        member_metrics.append(
            MemberGenerationMetrics(
                member_id=member.member_id,
                member_tag=member.member_tag,
                agent_type=member.agent_type,
                deployment_mass=mass,
                deployment_mass_after=mass,
                mean_throughput=mean_throughput,
                mean_oracle_harm=statistics.mean(e.oracle_harm for e in episodes),
                mean_severity=statistics.mean(e.severity_composite for e in episodes),
                mean_detector_composite=statistics.mean(e.detector_composite for e in episodes),
                correction_preserving=member.correction_preserving,
                programs=dict(member.programs),
                episode_metrics=tuple(episodes),
            )
        )

    new_masses = update_deployment_mass(
        masses, throughputs, selection_strength=selection_strength, mass_floor=mass_floor,
    )
    updated_members = [
        MemberGenerationMetrics(
            **{**asdict(m), "deployment_mass_after": new_mass}
        )
        for m, new_mass in zip(member_metrics, new_masses)
    ]

    cp_mass = sum(m.deployment_mass_after for m in updated_members if m.correction_preserving)
    snapshot = GenerationSnapshot(
        generation=generation,
        correction_preserving_mass_share=cp_mass,
        weighted_mean_throughput=sum(
            m.deployment_mass_after * m.mean_throughput for m in updated_members
        ),
        weighted_mean_oracle_harm=sum(
            m.deployment_mass_after * m.mean_oracle_harm for m in updated_members
        ),
        weighted_mean_severity=sum(
            m.deployment_mass_after * m.mean_severity for m in updated_members
        ),
        weighted_mean_detector_composite=sum(
            m.deployment_mass_after * m.mean_detector_composite for m in updated_members
        ),
        members=tuple(updated_members),
    )
    return snapshot, new_masses


def run_selection_loop(
    members: list[SelectionMember] | None = None,
    *,
    n_generations: int = D8_N_GENERATIONS,
    n_episodes_per_member: int = D8_EPISODES_PER_MEMBER,
    backend_factory: Callable,
    progress: bool = True,
) -> SelectionTrajectory:
    members = members or sample_initial_population()
    n = len(members)
    masses = [1.0 / n] * n
    snapshots: list[GenerationSnapshot] = []
    for gen in range(n_generations):
        if progress:
            print(f"[phase8] generation {gen + 1}/{n_generations}")
        snapshot, masses = run_one_generation(
            members,
            masses,
            generation=gen,
            n_episodes_per_member=n_episodes_per_member,
            backend_factory=backend_factory,
        )
        snapshots.append(snapshot)
        if progress:
            print(
                f"[phase8]   correction_preserving_mass={snapshot.correction_preserving_mass_share:.3f} "
                f"weighted_throughput={snapshot.weighted_mean_throughput:.3f} "
                f"weighted_severity={snapshot.weighted_mean_severity:.4f}"
            )
    return SelectionTrajectory(
        generations=tuple(snapshots),
        protocol={
            "population_size": len(members),
            "n_generations": n_generations,
            "episodes_per_member": n_episodes_per_member,
            "selection_strength": D8_SELECTION_STRENGTH,
            "mass_floor": D8_MASS_FLOOR,
            "carrier_load_scale": PHASE8_CARRIER_LOAD_SCALE,
            "seed_base": D8_GENERATION_SEED_BASE,
        },
    )


def trajectory_to_dict(trajectory: SelectionTrajectory) -> dict[str, Any]:
    return {
        "protocol": trajectory.protocol,
        "generations": [
            {
                "generation": g.generation,
                "correction_preserving_mass_share": g.correction_preserving_mass_share,
                "weighted_mean_throughput": g.weighted_mean_throughput,
                "weighted_mean_oracle_harm": g.weighted_mean_oracle_harm,
                "weighted_mean_severity": g.weighted_mean_severity,
                "weighted_mean_detector_composite": g.weighted_mean_detector_composite,
                "members": [asdict(m) for m in g.members],
            }
            for g in trajectory.generations
        ],
    }
