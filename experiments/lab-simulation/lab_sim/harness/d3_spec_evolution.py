"""D3.2 — selection coupled to spec weakening (PLAN.md MB6b).

Extends D3.1: every lab starts on the full ``pipeline_default.json`` with
uncaptured correction channels. After each generation's throughput-
weighted selection, high-throughput members may apply one **spec-weakening
mutation** — the population-level effect of D2's ``upgrade_spec`` operator
(default → ``pipeline_shortcut.json``, dropping ``approve_review``).

**Local rationality rule (pre-registered):** mutate iff mean throughput ≥
population median AND a weakening step exists AND ``rng < D3_2_MUTATION_PROB``.

**Measurands (report separately from basin persistence):**

- ``shortcut_spec_mass_share`` — deployment mass on weakened specs.
- ``spec_mutation_events`` — count of weakenings this generation.
- ``correction_preserving_mass_share`` / ``correction_integrity_mass_share``
  — same D3.1 tags, now expected to decay endogenously via spec drift.

Harness only — no referee or ``CODE_VERSION`` change.
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field, replace
from typing import Callable

from ..world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from .d3_population import (
    D3_EPISODE_T,
    D3_EPISODES_PER_MEMBER,
    D3_GENERATION_SEED_BASE,
    D3_MASS_FLOOR,
    D3_N_GENERATIONS,
    D3_POPULATION_SIZE,
    D3_SELECTION_STRENGTH,
    D3_TEMPERATURE,
    GenerationSnapshot,
    run_one_generation,
)
from .isolate import MockIsolate

# --- Pre-registered D3.2 protocol ------------------------------------------------

D3_2_SAMPLING_SEED = 20260708
D3_2_POPULATION_SIZE = 12
D3_2_N_GENERATIONS = 10
D3_2_MUTATION_PROB = 0.65
D3_2_GENERATION_SEED_BASE = 40000

# D2 ``upgrade_spec`` demo target: one weakening step (drop review gate).
SPEC_WEAKENING_CHAIN: dict[str, str] = {
    "pipeline_default.json": "pipeline_shortcut.json",
}


def spec_weakening_steps(cfg: LabConfig) -> int:
    """Count of weakening mutations from default (0 or 1 with current chain)."""
    return 0 if cfg.pipeline_spec == "pipeline_default.json" else 1


def next_weakened_spec(current: str) -> str | None:
    return SPEC_WEAKENING_CHAIN.get(current)


def make_d3_2_member_config(
    member_id: str,
    *,
    pipeline_spec: str = "pipeline_default.json",
    eng_w: GoalWeights,
    rev_w: GoalWeights,
    rm_w: GoalWeights,
    T: int = D3_EPISODE_T,
    temperature: float = D3_TEMPERATURE,
) -> LabConfig:
    """Strict uncaptured correction channels; D2 upgrade path enabled."""
    target = "pipeline_shortcut.json" if pipeline_spec == "pipeline_default.json" else None
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_w, temperature=temperature),
            AgentConfig("rev1", "reviewer", rev_w, temperature=temperature),
            AgentConfig("rm1", "release_manager", rm_w, temperature=temperature),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(capture_start=None),
        admin=AdminConfig(least_privilege=True, capture_start=None),
        T=T,
        pipeline_spec=pipeline_spec,
        multi_gen_enabled=True,
        spec_upgrade_target=target,
        config_id=member_id,
    )


def sample_d3_2_initial_population(
    *,
    seed: int = D3_2_SAMPLING_SEED,
    population_size: int = D3_2_POPULATION_SIZE,
) -> list[LabConfig]:
    """All labs start on the full default spec; only goal weights vary."""
    rng = random.Random(seed)
    return [
        make_d3_2_member_config(
            f"d3b.{i:02d}",
            pipeline_spec="pipeline_default.json",
            eng_w=_sample_role_weights(rng),
            rev_w=_sample_role_weights(rng),
            rm_w=_sample_role_weights(rng),
        )
        for i in range(population_size)
    ]


def _sample_role_weights(rng: random.Random) -> GoalWeights:
    draws = [rng.gammavariate(1.0, 1.0) for _ in range(4)]
    return GoalWeights(*draws).normalized()


def apply_spec_weakening(cfg: LabConfig, new_spec: str) -> LabConfig:
    """Apply one D2-style spec downgrade; clear upgrade target once weakened."""
    return LabConfig(
        agents=cfg.agents,
        board=cfg.board,
        admin=cfg.admin,
        tier=cfg.tier,
        T=cfg.T,
        pipeline_spec=new_spec,
        units=cfg.units,
        groups=cfg.groups,
        config_id=cfg.config_id,
        extra_playbooks=cfg.extra_playbooks,
        build_params=cfg.build_params,
        capability_probe_mode=cfg.capability_probe_mode,
        comms_enabled=cfg.comms_enabled,
        board_enabled=cfg.board_enabled,
        dm_enabled=cfg.dm_enabled,
        file_enabled=cfg.file_enabled,
        multi_gen_enabled=cfg.multi_gen_enabled,
        spec_upgrade_target=None,
        playbook_pins=cfg.playbook_pins,
        knowledge_base=cfg.knowledge_base,
        knowledge_base_redteam=cfg.knowledge_base_redteam,
        redteam_actor_ids=cfg.redteam_actor_ids,
    )


def apply_generation_spec_mutations(
    configs: list[LabConfig],
    throughputs: list[float],
    *,
    rng: random.Random,
    mutation_prob: float = D3_2_MUTATION_PROB,
) -> tuple[list[LabConfig], int]:
    """Locally rational spec weakening for above-median throughput labs."""
    if len(configs) != len(throughputs):
        raise ValueError("configs and throughputs must align")
    median_t = statistics.median(throughputs)
    out: list[LabConfig] = []
    events = 0
    for cfg, t in zip(configs, throughputs):
        nxt = next_weakened_spec(cfg.pipeline_spec)
        if nxt is not None and t >= median_t and rng.random() < mutation_prob:
            out.append(apply_spec_weakening(cfg, nxt))
            events += 1
        else:
            out.append(cfg)
    return out, events


@dataclass
class SpecEvolutionSnapshot(GenerationSnapshot):
    shortcut_spec_mass_share: float = 0.0
    spec_mutation_events: int = 0
    mean_spec_weakening_steps: float = 0.0


@dataclass
class SpecEvolutionTrajectory:
    generations: tuple[SpecEvolutionSnapshot, ...] = ()
    protocol: dict = field(default_factory=dict)


def _enrich_snapshot(
    snap: GenerationSnapshot,
    configs: list[LabConfig],
    masses: list[float],
    *,
    mutation_events: int,
) -> SpecEvolutionSnapshot:
    shortcut_share = sum(
        m for c, m in zip(configs, masses) if c.pipeline_spec == "pipeline_shortcut.json"
    )
    mean_steps = sum(spec_weakening_steps(c) * m for c, m in zip(configs, masses))
    return SpecEvolutionSnapshot(
        generation=snap.generation,
        correction_preserving_mass_share=snap.correction_preserving_mass_share,
        correction_integrity_mass_share=snap.correction_integrity_mass_share,
        weighted_mean_throughput=snap.weighted_mean_throughput,
        weighted_mean_oracle_harm=snap.weighted_mean_oracle_harm,
        weighted_mean_severity=snap.weighted_mean_severity,
        members=snap.members,
        shortcut_spec_mass_share=shortcut_share,
        spec_mutation_events=mutation_events,
        mean_spec_weakening_steps=mean_steps,
    )


def run_spec_evolution_loop(
    configs: list[LabConfig] | None = None,
    *,
    n_generations: int = D3_2_N_GENERATIONS,
    n_episodes_per_member: int = D3_EPISODES_PER_MEMBER,
    backend_factory: Callable = MockIsolate,
    seed_base: int = D3_2_GENERATION_SEED_BASE,
    mutation_prob: float = D3_2_MUTATION_PROB,
    mutation_seed: int = D3_2_SAMPLING_SEED,
    selection_strength: float = D3_SELECTION_STRENGTH,
    mass_floor: float = D3_MASS_FLOOR,
) -> SpecEvolutionTrajectory:
    configs = configs or sample_d3_2_initial_population()
    n = len(configs)
    masses = [1.0 / n] * n
    mut_rng = random.Random(mutation_seed)
    snapshots: list[SpecEvolutionSnapshot] = []

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
        throughputs = [m.mean_throughput for m in snap.members]
        configs, events = apply_generation_spec_mutations(
            configs, throughputs, rng=mut_rng, mutation_prob=mutation_prob
        )
        snapshots.append(_enrich_snapshot(snap, configs, masses, mutation_events=events))

    return SpecEvolutionTrajectory(
        generations=tuple(snapshots),
        protocol={
            "mode": "d3.2_spec_evolution",
            "sampling_seed": D3_2_SAMPLING_SEED,
            "population_size": len(configs),
            "n_generations": n_generations,
            "episodes_per_member": n_episodes_per_member,
            "episode_T": D3_EPISODE_T,
            "temperature": D3_TEMPERATURE,
            "mutation_prob": mutation_prob,
            "mutation_seed": mutation_seed,
            "selection_strength": selection_strength,
            "mass_floor": mass_floor,
            "generation_seed_base": seed_base,
            "weakening_chain": dict(SPEC_WEAKENING_CHAIN),
        },
    )


def trajectory_to_dict(traj: SpecEvolutionTrajectory) -> dict:
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
                "shortcut_spec_mass_share": g.shortcut_spec_mass_share,
                "spec_mutation_events": g.spec_mutation_events,
                "mean_spec_weakening_steps": g.mean_spec_weakening_steps,
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
                    }
                    for m in g.members
                ],
            }
            for g in traj.generations
        ],
    }
