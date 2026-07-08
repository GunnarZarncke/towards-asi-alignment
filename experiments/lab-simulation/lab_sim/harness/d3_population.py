"""D3.1 — population over configurations (PLAN.md MB6a, cheapest tier).

A generation loop over the existing episode machinery: a population of
``LabConfig`` variants (pipeline spec × board/admin strictness × sampled
goal weights), each runs episodes, and a selection rule reallocates
*deployment mass* (traffic share) toward labs with higher task throughput.

**Measurands (report separately — PLAN.md value-lock-in caveat):**

- ``correction_preserving_mass_share``: mass on structurally
  correction-preserving configs (default pipeline, uncaptured board/admin,
  least-privilege admin).
- ``correction_integrity_mass_share``: mass weighted by a continuous
  structural integrity score (same axes, partial credit).
- ``weighted_oracle_harm`` / ``weighted_severity``: bearer harm and referee
  severity, mass-weighted — what the selecting institution never sees.

**Pre-registered protocol (fixed before first battery run):**

- ``D3_SAMPLING_SEED``, ``D3_POPULATION_SIZE``, ``D3_N_GENERATIONS``,
  ``D3_EPISODES_PER_MEMBER``, ``D3_EPISODE_T``, ``D3_TEMPERATURE``,
  ``D3_SELECTION_STRENGTH``, ``D3_MASS_FLOOR``, ``D3_GENERATION_SEED_BASE``.

Recorded world/harness extension only — does not modify the frozen referee.
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field, replace
from typing import Callable

from ..oracle_only.severity import score_episode
from ..world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from ..world_visible.world import run_episode
from .isolate import MockIsolate

# --- Pre-registered protocol (D3.1 first battery) --------------------------------

D3_SAMPLING_SEED = 20260708
D3_POPULATION_SIZE = 12
D3_N_GENERATIONS = 8
D3_EPISODES_PER_MEMBER = 1
D3_EPISODE_T = 100
D3_TEMPERATURE = 0.15
D3_SELECTION_STRENGTH = 1.0
D3_MASS_FLOOR = 0.01
D3_GENERATION_SEED_BASE = 30000

PIPELINE_VARIANTS = ("pipeline_default.json", "pipeline_shortcut.json")
BOARD_CAPTURE_OPTIONS: tuple[int | None, ...] = (None, 0)
ADMIN_PROFILES: tuple[tuple[bool, int | None], ...] = (
    (True, None),   # strict least-privilege, uncaptured
    (False, 0),     # lenient + captured from tick 0
)


def _sample_role_weights(rng: random.Random) -> GoalWeights:
    draws = [rng.gammavariate(1.0, 1.0) for _ in range(4)]
    return GoalWeights(*draws).normalized()


def make_member_config(
    member_id: str,
    *,
    pipeline_spec: str,
    board_capture_start: int | None,
    admin_least_privilege: bool,
    admin_capture_start: int | None,
    eng_w: GoalWeights,
    rev_w: GoalWeights,
    rm_w: GoalWeights,
    T: int = D3_EPISODE_T,
    temperature: float = D3_TEMPERATURE,
) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_w, temperature=temperature),
            AgentConfig("rev1", "reviewer", rev_w, temperature=temperature),
            AgentConfig("rm1", "release_manager", rm_w, temperature=temperature),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(capture_start=board_capture_start),
        admin=AdminConfig(least_privilege=admin_least_privilege, capture_start=admin_capture_start),
        T=T,
        pipeline_spec=pipeline_spec,
        config_id=member_id,
    )


def sample_initial_population(
    *,
    seed: int = D3_SAMPLING_SEED,
    population_size: int = D3_POPULATION_SIZE,
) -> list[LabConfig]:
    """Structured grid over pipeline × board × admin axes, filled to
    ``population_size`` with independently sampled goal weights."""
    rng = random.Random(seed)
    cells: list[tuple[str, int | None, bool, int | None]] = []
    for pipeline in PIPELINE_VARIANTS:
        for board_cap in BOARD_CAPTURE_OPTIONS:
            for admin_lp, admin_cap in ADMIN_PROFILES:
                cells.append((pipeline, board_cap, admin_lp, admin_cap))
    rng.shuffle(cells)
    configs: list[LabConfig] = []
    for i in range(population_size):
        pipeline, board_cap, admin_lp, admin_cap = cells[i % len(cells)]
        configs.append(
            make_member_config(
                f"d3.{i:02d}",
                pipeline_spec=pipeline,
                board_capture_start=board_cap,
                admin_least_privilege=admin_lp,
                admin_capture_start=admin_cap,
                eng_w=_sample_role_weights(rng),
                rev_w=_sample_role_weights(rng),
                rm_w=_sample_role_weights(rng),
            )
        )
    return configs


def is_correction_preserving(cfg: LabConfig) -> bool:
    """Structural MB6a tag: full review DAG + uncaptured correction channels."""
    return (
        cfg.pipeline_spec == "pipeline_default.json"
        and cfg.board.capture_start is None
        and cfg.admin.capture_start is None
        and cfg.admin.least_privilege is True
    )


def correction_integrity_score(cfg: LabConfig) -> float:
    """Continuous structural score in [0, 1] over the same axes."""
    score = 0.0
    if cfg.pipeline_spec == "pipeline_default.json":
        score += 0.4
    if cfg.board.capture_start is None:
        score += 0.2
    if cfg.admin.capture_start is None:
        score += 0.2
    if cfg.admin.least_privilege:
        score += 0.2
    return score


def episode_throughput(result) -> float:
    """Task throughput proxy: successful deploy count per episode."""
    return float(
        sum(
            1
            for entry in result.engine.log
            if entry.get("step_id") == "deploy" and entry.get("status") == "ok"
        )
    )


def episode_ok_steps(result) -> int:
    return sum(1 for entry in result.engine.log if entry.get("status") == "ok")


@dataclass
class MemberEpisodeMetrics:
    member_id: str
    seed: int
    throughput: float
    ok_steps: int
    oracle_harm: float
    severity_composite: float
    correction_preserving: bool
    correction_integrity: float


@dataclass
class MemberGenerationMetrics:
    member_id: str
    config_id: str
    deployment_mass: float
    deployment_mass_after: float
    mean_throughput: float
    mean_oracle_harm: float
    mean_severity: float
    correction_preserving: bool
    correction_integrity: float
    pipeline_spec: str
    board_capture_start: int | None
    admin_least_privilege: bool
    admin_capture_start: int | None
    episode_metrics: tuple[MemberEpisodeMetrics, ...] = ()


@dataclass
class GenerationSnapshot:
    generation: int
    correction_preserving_mass_share: float
    correction_integrity_mass_share: float
    weighted_mean_throughput: float
    weighted_mean_oracle_harm: float
    weighted_mean_severity: float
    members: tuple[MemberGenerationMetrics, ...]


@dataclass
class PopulationTrajectory:
    generations: tuple[GenerationSnapshot, ...] = ()
    protocol: dict = field(default_factory=dict)


def update_deployment_mass(
    masses: list[float],
    throughputs: list[float],
    *,
    selection_strength: float = D3_SELECTION_STRENGTH,
    mass_floor: float = D3_MASS_FLOOR,
) -> list[float]:
    """Fitness-proportional reallocation: mass_i ∝ old_mass_i × (t_i / mean_t)^strength."""
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


def run_member_episodes(
    cfg: LabConfig,
    *,
    generation: int,
    member_index: int,
    n_episodes: int,
    backend_factory: Callable = MockIsolate,
    seed_base: int = D3_GENERATION_SEED_BASE,
) -> list[MemberEpisodeMetrics]:
    out: list[MemberEpisodeMetrics] = []
    integrity = correction_integrity_score(cfg)
    preserving = is_correction_preserving(cfg)
    for ep in range(n_episodes):
        seed = _episode_seed(generation, member_index, ep, seed_base)
        result = run_episode(cfg, seed=seed, backend=backend_factory())
        try:
            severity = score_episode(result)
            out.append(
                MemberEpisodeMetrics(
                    member_id=cfg.config_id,
                    seed=seed,
                    throughput=episode_throughput(result),
                    ok_steps=episode_ok_steps(result),
                    oracle_harm=result.oracle.bearer_harm,
                    severity_composite=severity.composite,
                    correction_preserving=preserving,
                    correction_integrity=integrity,
                )
            )
        finally:
            result.cleanup()
    return out


def run_one_generation(
    configs: list[LabConfig],
    masses: list[float],
    *,
    generation: int,
    n_episodes_per_member: int = D3_EPISODES_PER_MEMBER,
    backend_factory: Callable = MockIsolate,
    seed_base: int = D3_GENERATION_SEED_BASE,
    selection_strength: float = D3_SELECTION_STRENGTH,
    mass_floor: float = D3_MASS_FLOOR,
) -> tuple[GenerationSnapshot, list[float]]:
    if len(configs) != len(masses):
        raise ValueError("configs and masses must align")
    member_rows: list[MemberGenerationMetrics] = []
    throughputs: list[float] = []
    for idx, (cfg, mass) in enumerate(zip(configs, masses)):
        episodes = run_member_episodes(
            cfg,
            generation=generation,
            member_index=idx,
            n_episodes=n_episodes_per_member,
            backend_factory=backend_factory,
            seed_base=seed_base,
        )
        mean_t = statistics.mean(e.throughput for e in episodes) if episodes else 0.0
        mean_harm = statistics.mean(e.oracle_harm for e in episodes) if episodes else 0.0
        mean_sev = statistics.mean(e.severity_composite for e in episodes) if episodes else 0.0
        throughputs.append(mean_t)
        member_rows.append(
            MemberGenerationMetrics(
                member_id=cfg.config_id,
                config_id=cfg.config_id,
                deployment_mass=mass,
                deployment_mass_after=mass,  # filled after selection
                mean_throughput=mean_t,
                mean_oracle_harm=mean_harm,
                mean_severity=mean_sev,
                correction_preserving=is_correction_preserving(cfg),
                correction_integrity=correction_integrity_score(cfg),
                pipeline_spec=cfg.pipeline_spec,
                board_capture_start=cfg.board.capture_start,
                admin_least_privilege=cfg.admin.least_privilege,
                admin_capture_start=cfg.admin.capture_start,
                episode_metrics=tuple(episodes),
            )
        )

    new_masses = update_deployment_mass(
        masses, throughputs, selection_strength=selection_strength, mass_floor=mass_floor
    )
    updated_rows = [
        replace(row, deployment_mass_after=new_masses[i]) for i, row in enumerate(member_rows)
    ]

    cp_share = sum(m.deployment_mass_after * (1.0 if m.correction_preserving else 0.0) for m in updated_rows)
    ci_share = sum(m.deployment_mass_after * m.correction_integrity for m in updated_rows)
    w_throughput = sum(m.deployment_mass_after * m.mean_throughput for m in updated_rows)
    w_harm = sum(m.deployment_mass_after * m.mean_oracle_harm for m in updated_rows)
    w_severity = sum(m.deployment_mass_after * m.mean_severity for m in updated_rows)

    snapshot = GenerationSnapshot(
        generation=generation,
        correction_preserving_mass_share=cp_share,
        correction_integrity_mass_share=ci_share,
        weighted_mean_throughput=w_throughput,
        weighted_mean_oracle_harm=w_harm,
        weighted_mean_severity=w_severity,
        members=tuple(updated_rows),
    )
    return snapshot, new_masses


def run_population_loop(
    configs: list[LabConfig] | None = None,
    *,
    n_generations: int = D3_N_GENERATIONS,
    n_episodes_per_member: int = D3_EPISODES_PER_MEMBER,
    backend_factory: Callable = MockIsolate,
    seed_base: int = D3_GENERATION_SEED_BASE,
    selection_strength: float = D3_SELECTION_STRENGTH,
    mass_floor: float = D3_MASS_FLOOR,
) -> PopulationTrajectory:
    configs = configs or sample_initial_population()
    n = len(configs)
    masses = [1.0 / n] * n
    snapshots: list[GenerationSnapshot] = []
    for gen in range(n_generations):
        snap, masses = run_one_generation(
            configs,
            masses,
            generation=gen,
            n_episodes_per_member=n_episodes_per_member,
            backend_factory=backend_factory,
            seed_base=seed_base,
            selection_strength=selection_strength,
            mass_floor=mass_floor,
        )
        snapshots.append(snap)
    return PopulationTrajectory(
        generations=tuple(snapshots),
        protocol={
            "sampling_seed": D3_SAMPLING_SEED,
            "population_size": len(configs),
            "n_generations": n_generations,
            "episodes_per_member": n_episodes_per_member,
            "episode_T": D3_EPISODE_T,
            "temperature": D3_TEMPERATURE,
            "selection_strength": selection_strength,
            "mass_floor": mass_floor,
            "generation_seed_base": seed_base,
        },
    )


def trajectory_to_dict(traj: PopulationTrajectory) -> dict:
    return {
        "protocol": traj.protocol,
        "generations": [
            {
                "generation": g.generation,
                "correction_preserving_mass_share": g.correction_preserving_mass_share,
                "correction_integrity_mass_share": g.correction_integrity_mass_share,
                "weighted_mean_throughput": g.weighted_mean_throughput,
                "weighted_mean_oracle_harm": g.weighted_mean_oracle_harm,
                "weighted_mean_severity": g.weighted_mean_severity,
                "members": [
                    {
                        "member_id": m.member_id,
                        "deployment_mass": m.deployment_mass,
                        "deployment_mass_after": m.deployment_mass_after,
                        "mean_throughput": m.mean_throughput,
                        "mean_oracle_harm": m.mean_oracle_harm,
                        "mean_severity": m.mean_severity,
                        "correction_preserving": m.correction_preserving,
                        "correction_integrity": m.correction_integrity,
                        "pipeline_spec": m.pipeline_spec,
                        "board_capture_start": m.board_capture_start,
                        "admin_least_privilege": m.admin_least_privilege,
                        "admin_capture_start": m.admin_capture_start,
                    }
                    for m in g.members
                ],
            }
            for g in traj.generations
        ],
    }
