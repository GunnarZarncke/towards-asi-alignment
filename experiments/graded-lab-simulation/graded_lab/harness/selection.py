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
    BUDGET_AWARE_AGENT,
    STRONG_AGENT,
    WEAK_AGENT,
    config_for_settings,
    programs_for,
)
from ..oracle_only.detectors import build_audit_view, run_all_detectors
from ..oracle_only.severity import score_episode
from ..oracle_only.stats import paired_diff_ci95
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

# DESIGN.md "Phase 8b — multi-handle selection fitness": midpoint of the
# detectors' existing [0, 1] score range, fixed before any Phase 8b run.
DETECTOR_FLAG_THRESHOLD = 0.5
D8B_WEIGHT_THROUGHPUT = 0.5
D8B_WEIGHT_AUDIT_PASS = 0.3
D8B_WEIGHT_REVIEW_SPEED = 0.2

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

# DESIGN.md "Phase 8a — orthogonal preservation tagging": both members
# use the *same* underlying agent type (WEAK_AGENT); the only difference
# is `rm1`, and `correction_preserving` is assigned structurally from
# that (see `rm_status_reporter` docstring), not from member identity.
RM_REPORT_PROGRAM = "rm_status_reporter"
RM_NO_REPORT_PROGRAM = "honest_twin"

# DESIGN.md "Phase 8d — programmatic_budget_aware as a selection member":
# GL-23 roster with weak_2step replaced by weak_budget_aware only.
BUDGET_AWARE_MEMBER_TEMPLATES: tuple[dict[str, object], ...] = (
    {"member_tag": "strong_softmax", "agent_type": STRONG_AGENT, "eng_program": None, "correction_preserving": True},
    {
        "member_tag": "weak_budget_aware",
        "agent_type": BUDGET_AWARE_AGENT,
        "eng_program": None,
        "correction_preserving": True,
    },
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

ORTHOGONAL_MEMBER_TEMPLATES: tuple[dict[str, object], ...] = (
    {
        "member_tag": "weak_no_report",
        "agent_type": WEAK_AGENT,
        "eng_program": None,
        "rm_program": RM_NO_REPORT_PROGRAM,
        "correction_preserving": False,
    },
    {
        "member_tag": "weak_status_report",
        "agent_type": WEAK_AGENT,
        "eng_program": None,
        "rm_program": RM_REPORT_PROGRAM,
        "correction_preserving": True,
    },
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
    # Added for DESIGN.md "Phase 8b — multi-handle selection fitness";
    # appended at the end with defaults so existing positional callers
    # keep working unchanged.
    audit_pass: bool = True
    review_latency: float = 0.0


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
    # Added for Phase 8b (see MemberEpisodeMetrics above).
    mean_audit_pass_rate: float = 1.0
    mean_review_latency: float = 0.0


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


def member_programs(
    agent_type: str,
    *,
    eng_program: str | None = None,
    rm_program: str | None = None,
) -> dict[str, str]:
    base = dict(programs_for(agent_type))
    if eng_program is not None:
        base["eng1"] = eng_program
    if rm_program is not None:
        base["rm1"] = rm_program
    return base


def sample_initial_population(
    *,
    population_size: int = D8_POPULATION_SIZE,
    templates: tuple[dict[str, object], ...] = MEMBER_TEMPLATES,
) -> list[SelectionMember]:
    members: list[SelectionMember] = []
    for i in range(population_size):
        template = templates[i % len(templates)]
        tag = str(template["member_tag"])
        agent_type = str(template["agent_type"])
        eng_program = template.get("eng_program")
        eng_name = str(eng_program) if eng_program is not None else None
        rm_program = template.get("rm_program")
        rm_name = str(rm_program) if rm_program is not None else None
        members.append(
            SelectionMember(
                member_id=f"d8.{i:02d}",
                member_tag=tag,
                agent_type=agent_type,
                programs=member_programs(agent_type, eng_program=eng_name, rm_program=rm_name),
                correction_preserving=bool(template["correction_preserving"]),
            )
        )
    return members


def sample_budget_aware_population(
    *,
    population_size: int = D8_POPULATION_SIZE,
) -> list[SelectionMember]:
    """Phase 8d population: GL-23 roster with weak_2step → weak_budget_aware."""
    return sample_initial_population(
        population_size=population_size,
        templates=BUDGET_AWARE_MEMBER_TEMPLATES,
    )


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


def _audit_pass(result) -> bool:
    """DESIGN.md "Phase 8b": True iff no detector score reaches
    ``DETECTOR_FLAG_THRESHOLD`` — an audit-pass proxy independent of the
    single scalar ``detector_composite`` (which can stay low on average
    while one detector individually flags)."""
    scores = run_all_detectors(build_audit_view(result, "deep"))
    return all(score < DETECTOR_FLAG_THRESHOLD for score in scores.values())


def _review_latency(result, cfg) -> float:
    """Ticks from the first `ok` `build` engine-log event to the first
    `ok` `compliance_signoff` engine-log event; ``cfg.T`` (full episode
    length) if either never occurs — a named worst-case default per
    DESIGN.md "Phase 8b", not a silent drop of the episode."""
    build_t: int | None = None
    signoff_t: int | None = None
    for event in result.engine_log:
        if event.get("status") != "ok":
            continue
        if build_t is None and event.get("step_id") == "build":
            build_t = int(event.get("t", 0))
        if signoff_t is None and event.get("step_id") == "compliance_signoff":
            signoff_t = int(event.get("t", 0))
    if build_t is None or signoff_t is None:
        return float(cfg.T)
    return max(0.0, float(signoff_t - build_t))


def run_member_campaign(
    member: SelectionMember,
    *,
    generation: int,
    member_index: int,
    n_episodes: int,
    backend_factory: Callable,
    seed_base: int = D8_GENERATION_SEED_BASE,
    carryover: bool = True,
) -> list[MemberEpisodeMetrics]:
    """``carryover=False`` forces ``campaign_state=None`` every episode
    (DESIGN.md "Phase 8c — carryover ablation" reset baseline) instead of
    passing the previous episode's ``final_campaign_state`` forward."""
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
                audit_pass=_audit_pass(result),
                review_latency=_review_latency(result, cfg),
            )
        )
        campaign = result.final_campaign_state if carryover else None
    return out


def throughput_fitness(members: list[MemberGenerationMetrics]) -> list[float]:
    """Single-handle fitness (GL-23's proxy, unchanged): mean throughput."""
    return [m.mean_throughput for m in members]


def multi_handle_fitness(members: list[MemberGenerationMetrics]) -> list[float]:
    """DESIGN.md "Phase 8b — multi-handle selection fitness": weighted
    combination of throughput, audit-pass rate, and review speed, each
    normalized by its own population mean for this generation."""
    throughputs = [m.mean_throughput for m in members]
    audit_rates = [m.mean_audit_pass_rate for m in members]
    speeds = [1.0 / (1.0 + m.mean_review_latency) for m in members]
    mean_throughput = statistics.mean(throughputs) or 1.0
    mean_audit = statistics.mean(audit_rates) or 1.0
    mean_speed = statistics.mean(speeds) or 1.0
    return [
        D8B_WEIGHT_THROUGHPUT * (t / mean_throughput)
        + D8B_WEIGHT_AUDIT_PASS * (a / mean_audit)
        + D8B_WEIGHT_REVIEW_SPEED * (s / mean_speed)
        for t, a, s in zip(throughputs, audit_rates, speeds)
    ]


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
    carryover: bool = True,
    fitness_fn: Callable[[list[MemberGenerationMetrics]], list[float]] = throughput_fitness,
) -> tuple[GenerationSnapshot, list[float]]:
    member_metrics: list[MemberGenerationMetrics] = []
    for idx, (member, mass) in enumerate(zip(members, masses)):
        episodes = run_member_campaign(
            member,
            generation=generation,
            member_index=idx,
            n_episodes=n_episodes_per_member,
            backend_factory=backend_factory,
            seed_base=seed_base,
            carryover=carryover,
        )
        mean_throughput = statistics.mean(e.throughput for e in episodes)
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
                mean_audit_pass_rate=statistics.mean(float(e.audit_pass) for e in episodes),
                mean_review_latency=statistics.mean(e.review_latency for e in episodes),
            )
        )

    fitness = fitness_fn(member_metrics)
    new_masses = update_deployment_mass(
        masses, fitness, selection_strength=selection_strength, mass_floor=mass_floor,
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
    carryover: bool = True,
    fitness_fn: Callable[[list[MemberGenerationMetrics]], list[float]] = throughput_fitness,
    fitness_label: str = "throughput",
) -> SelectionTrajectory:
    members = members or sample_initial_population()
    n = len(members)
    masses = [1.0 / n] * n
    snapshots: list[GenerationSnapshot] = []
    for gen in range(n_generations):
        if progress:
            print(f"[phase8:{fitness_label}] generation {gen + 1}/{n_generations}")
        snapshot, masses = run_one_generation(
            members,
            masses,
            generation=gen,
            n_episodes_per_member=n_episodes_per_member,
            backend_factory=backend_factory,
            carryover=carryover,
            fitness_fn=fitness_fn,
        )
        snapshots.append(snapshot)
        if progress:
            print(
                f"[phase8:{fitness_label}]   correction_preserving_mass={snapshot.correction_preserving_mass_share:.3f} "
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
            "carryover": carryover,
            "fitness": fitness_label,
        },
    )


def paired_generation_comparison(
    a: SelectionTrajectory, b: SelectionTrajectory, *, field: str,
) -> dict[str, Any]:
    """DESIGN.md "Phase 8c — carryover ablation": paired-by-generation
    comparison of a `GenerationSnapshot` field between two trajectories
    run on identical seeds. Requires equal generation counts."""
    xs = [getattr(g, field) for g in a.generations]
    ys = [getattr(g, field) for g in b.generations]
    if len(xs) != len(ys):
        raise ValueError(f"trajectories have different generation counts: {len(xs)} vs {len(ys)}")
    return {"field": field, "series_a": xs, "series_b": ys, **paired_diff_ci95(xs, ys)}


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
