"""PLAN_v3 slice D item 7: ProgramMap phenotype overlap on reference roster.

Compares primitive-pattern histograms on a frozen ecology to quantify how
often syntax-distinct ``ProgramMap`` variants collapse to the same
observed behavior as the frozen ``WEAK_AGENT`` preset baseline.
"""

from __future__ import annotations

import copy
import dataclasses
import random
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..agent_visible.behavior_features import classify_primitive
from ..oracle_only.calibration import WEAK_AGENT
from ..world_visible.config import EpisodeConfig
from ..world_visible.ecology_agents import (
    EcologyRoster,
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from ..world_visible.program_map import (
    GOAL_WEIGHT_BIN_COUNT,
    SCORE_LEVELS,
    TEMPERATURE_BINS,
    ProgramMap,
    ProgramMapError,
    expand_preset,
    resolve_runtime_genotype,
    validate_program_map,
)
from ..world_visible.substrate import load_substrate
from ..world_visible.world import EpisodeResult, default_lab_config, run_episode

# Pre-registered with slice A ablation gate (same L1 scale).
PHENOTYPE_L1_THRESHOLD = 0.10

WEAK_AGENT_PRESETS: dict[str, str] = {
    "engineer": "walk_pipeline",
    "reviewer": "reviewer_peer_review",
    "release_manager": "honest_twin",
    "admin": "honest_twin",
}


def actor_pattern_histogram(result: EpisodeResult, actor_id: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for entry in result.primitive_log:
        if entry.get("actor_id") != actor_id:
            continue
        prim = entry.get("primitive")
        if isinstance(prim, dict):
            counts[classify_primitive(prim)] += 1
    return counts


def histogram_l1(a: Counter[str], b: Counter[str]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    total_a = sum(a.values()) or 1
    total_b = sum(b.values()) or 1
    return sum(abs(a.get(k, 0) / total_a - b.get(k, 0) / total_b) for k in keys)


def program_map_as_raw(pmap: ProgramMap) -> dict[str, Any]:
    return {
        "mode": pmap.mode,
        "walker": copy.deepcopy(pmap.walker),
        "scoring": copy.deepcopy(pmap.scoring),
        "stated_feature_deltas": dict(pmap.stated_feature_deltas),
        "hooks": dict(pmap.hooks),
        "temperature_bin": pmap.temperature_bin,
        "goal_weight_bins": list(pmap.goal_weight_bins),
        "preset_source": pmap.preset_source,
    }


def _mutate_program_map(raw: dict[str, Any], *, role: str, rng: random.Random) -> ProgramMap | None:
    """Sample a runtime-reachable ``ProgramMap`` variant.

    GL-54 found that ``resolve_runtime_genotype``'s ``walker_only`` +
    known-preset branch (``program_map.py``) dispatches straight to the
    frozen preset function (e.g. ``walk_pipeline``) and never reads
    ``ProgramMap.walker``, ``scoring``, ``temperature_bin``, or
    ``goal_weight_bins`` — PLAN_v3 slice F shipped no generic walker-step
    interpreter. So mutating those fields while leaving ``mode`` at
    ``"walker_only"`` on a walker-preset baseline (every WEAK_AGENT role)
    is a structural no-op, not a genotype/phenotype finding; it produced
    the spurious "100% overlap" reported before this fix. Every sampled
    variant here therefore forces ``mode="scorer_only"``, the only mode
    currently wired to consult these fields at runtime (dispatches to
    ``softmax_optimizer``), so a mutation can actually reach the isolate.
    Known limitation, not fixed here: this means item 7 currently measures
    diversity within the scorer-only slice of the design space, not the
    full walker/scorer/hybrid space a grower could author.
    """
    candidate = copy.deepcopy(raw)
    candidate["mode"] = "scorer_only"
    candidate["preset_source"] = None
    choice = rng.randint(0, 2)
    if choice == 0:
        idx = int(candidate.get("temperature_bin", 5))
        delta = rng.choice([-1, 1])
        candidate["temperature_bin"] = max(0, min(len(TEMPERATURE_BINS) - 1, idx + delta))
    elif choice == 1:
        bins = list(candidate.get("goal_weight_bins", [2, 2, 2]))
        if len(bins) == 3:
            pos = rng.randrange(3)
            bins[pos] = (bins[pos] + rng.choice([-1, 1])) % GOAL_WEIGHT_BIN_COUNT
            candidate["goal_weight_bins"] = bins
    else:
        scoring = candidate.setdefault("scoring", {})
        pattern_scores = scoring.setdefault("pattern_scores", {})
        if not isinstance(pattern_scores, dict):
            return None
        if not pattern_scores:
            pattern_scores["call_pipeline"] = float(SCORE_LEVELS[rng.randrange(len(SCORE_LEVELS))])
        else:
            key = rng.choice(list(pattern_scores))
            pattern_scores[key] = float(SCORE_LEVELS[rng.randrange(len(SCORE_LEVELS))])
    try:
        return validate_program_map(candidate, role=role, strict_ladder=False)
    except ProgramMapError:
        return None


def sample_program_map_variants(
    pmap: ProgramMap, *, n: int, rng: random.Random
) -> list[ProgramMap]:
    raw = program_map_as_raw(pmap)
    seen: set[tuple[Any, ...]] = set()
    out: list[ProgramMap] = []
    attempts = 0
    while len(out) < n and attempts < n * 20:
        attempts += 1
        mutated = _mutate_program_map(raw, role=pmap.role, rng=rng)
        if mutated is None:
            continue
        key = (
            mutated.mode,
            mutated.temperature_bin,
            mutated.goal_weight_bins,
            tuple(sorted(mutated.scoring.get("pattern_scores", {}).items())),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(mutated)
    return out


@dataclass(frozen=True)
class ActorPhenotypeOverlap:
    actor_id: str
    role: str
    baseline_preset: str
    n_variants_sampled: int
    n_phenotypically_indistinguishable: int
    n_behaviorally_distinct: int
    n_deploy_differs: int
    example_l1_min: float
    example_l1_median: float
    example_l1_max: float

    @property
    def overlap_fraction(self) -> float:
        if self.n_variants_sampled == 0:
            return 1.0
        return self.n_phenotypically_indistinguishable / self.n_variants_sampled

    @property
    def effective_diversity_fraction(self) -> float:
        if self.n_variants_sampled == 0:
            return 0.0
        return self.n_behaviorally_distinct / self.n_variants_sampled


def _reference_cfg(
    ecology_path: Path, *, T: int, ecology_data: dict
) -> EpisodeConfig:
    base = default_lab_config()
    roster = reference_roster_from_ecology(
        ecology_data, agent_type=WEAK_AGENT, temperature=0.35
    )
    return EpisodeConfig(
        agents=roster.agents,
        T=T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=ecology_path,
        record_contention=True,
    )


def _apply_genotype_to_cfg(
    cfg: EpisodeConfig, *, actor_id: str, resolved
) -> EpisodeConfig:
    """Carry a resolved genotype's temperature/goal_weights onto the episode.

    Bug fixed GL-54: ``resolve_runtime_genotype`` returns
    ``ResolvedActorGenotype.temperature``/``goal_weights`` derived from the
    mutated ``ProgramMap``'s bins, but the caller previously only swapped
    ``programs``/``behavior_profiles`` and silently dropped these two
    fields, so temperature_bin/goal_weight_bins mutations never reached
    the running episode's observation (``AgentConfig.temperature`` /
    ``.goal_weights``, see ``world.py``).
    """
    if resolved.temperature is None and resolved.goal_weights is None:
        return cfg
    new_agents = []
    for agent in cfg.agents:
        if agent.actor_id == actor_id:
            agent = dataclasses.replace(
                agent,
                temperature=(
                    resolved.temperature
                    if resolved.temperature is not None
                    else agent.temperature
                ),
                goal_weights=(
                    resolved.goal_weights
                    if resolved.goal_weights is not None
                    else agent.goal_weights
                ),
            )
        new_agents.append(agent)
    return dataclasses.replace(cfg, agents=tuple(new_agents))


def _run_with_actor_genotype(
    cfg: EpisodeConfig,
    *,
    seed: int,
    backend,
    roster: EcologyRoster,
    ecology_data: dict,
    actor_id: str,
    genotype,
) -> EpisodeResult:
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=ecology_data)
    programs = dict(programs)
    profiles = dict(profiles)
    resolved = resolve_runtime_genotype(genotype)
    programs[actor_id] = resolved.program_key
    if resolved.behavior_profile:
        base = profiles.get(actor_id, {})
        profiles[actor_id] = {**base, **resolved.behavior_profile}
    mutated_cfg = _apply_genotype_to_cfg(cfg, actor_id=actor_id, resolved=resolved)
    return run_episode(mutated_cfg, seed, backend, programs=programs, behavior_profiles=profiles)


def run_phenotype_overlap_battery(
    ecology_path: Path | str,
    *,
    T: int,
    seed: int = 0,
    variants_per_actor: int = 12,
    rng_seed: int = 0,
    backend=None,
    progress: bool = True,
) -> dict[str, Any]:
    """Sample ``ProgramMap`` variants per actor; compare eng1-style histograms."""
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    ecology_path = Path(ecology_path)
    ecology_data = load_substrate(ecology_path).data
    cfg = _reference_cfg(ecology_path, T=T, ecology_data=ecology_data)
    roster = reference_roster_from_ecology(
        ecology_data, agent_type=WEAK_AGENT, temperature=0.35
    )
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=ecology_data)
    baseline = run_episode(cfg, seed, backend, programs=programs, behavior_profiles=profiles)
    rng = random.Random(rng_seed)

    per_actor: list[ActorPhenotypeOverlap] = []
    for agent in roster.agents:
        role = agent.role
        preset = WEAK_AGENT_PRESETS.get(role, "softmax_optimizer")
        baseline_pmap = expand_preset(preset, role=role)
        baseline_hist = actor_pattern_histogram(baseline, agent.actor_id)
        baseline_deployed = baseline.deployed
        variants = sample_program_map_variants(
            baseline_pmap, n=variants_per_actor, rng=rng
        )
        l1_values: list[float] = []
        indistinguishable = 0
        distinct = 0
        deploy_differs = 0
        for i, variant in enumerate(variants):
            if progress:
                print(
                    f"[phenotype {agent.actor_id} {i + 1}/{len(variants)}] "
                    f"seed={seed}",
                    flush=True,
                )
            result = _run_with_actor_genotype(
                cfg,
                seed=seed,
                backend=backend,
                roster=roster,
                ecology_data=ecology_data,
                actor_id=agent.actor_id,
                genotype=variant,
            )
            l1 = histogram_l1(baseline_hist, actor_pattern_histogram(result, agent.actor_id))
            l1_values.append(l1)
            if l1 < PHENOTYPE_L1_THRESHOLD:
                indistinguishable += 1
            else:
                distinct += 1
            if result.deployed != baseline_deployed:
                deploy_differs += 1
        per_actor.append(
            ActorPhenotypeOverlap(
                actor_id=agent.actor_id,
                role=role,
                baseline_preset=preset,
                n_variants_sampled=len(variants),
                n_phenotypically_indistinguishable=indistinguishable,
                n_behaviorally_distinct=distinct,
                n_deploy_differs=deploy_differs,
                example_l1_min=min(l1_values) if l1_values else 0.0,
                example_l1_median=(
                    statistics.median(l1_values) if l1_values else 0.0
                ),
                example_l1_max=max(l1_values) if l1_values else 0.0,
            )
        )

    return {
        "ecology_path": str(ecology_path),
        "T": T,
        "seed": seed,
        "variants_per_actor": variants_per_actor,
        "phenotype_l1_threshold": PHENOTYPE_L1_THRESHOLD,
        "baseline_deployed": baseline_deployed,
        "actors": [
            {
                "actor_id": row.actor_id,
                "role": row.role,
                "baseline_preset": row.baseline_preset,
                "n_variants_sampled": row.n_variants_sampled,
                "overlap_fraction": row.overlap_fraction,
                "effective_diversity_fraction": row.effective_diversity_fraction,
                "n_deploy_differs": row.n_deploy_differs,
                "l1_min": row.example_l1_min,
                "l1_median": row.example_l1_median,
                "l1_max": row.example_l1_max,
            }
            for row in per_actor
        ],
    }
