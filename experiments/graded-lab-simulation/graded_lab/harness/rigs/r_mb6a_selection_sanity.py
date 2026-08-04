"""R-MB6a — selection machinery sanity / variation operator (PLAN_v4 V4-4).

Question: does the closed ``ProgramMap`` variation operator plus the
uniform-fitness null harness behave as pre-registered — i.e. mutation
produces measured phenotype diversity, and the uniform-fitness control
stays inside the GL-25 permutation noise band?

Precondition (frozen V4-1, mechanical C4 deploy-rate band from
``ecology_complexity.check_c4`` on the fixture's reference traces,
never from operator output): deploy rate strictly inside
``(C4_MIN_DEPLOY_RATE, C4_MAX_DEPLOY_RATE)``.

This rig is harness science only (P5 + expressiveness report). It does
**not** ask whether selection finds evasive strategies — that is R-MB6b.
"""

from __future__ import annotations

import dataclasses
import random
from collections import Counter
from dataclasses import dataclass
from typing import Any

from ..ecology_complexity import C4_MAX_DEPLOY_RATE, C4_MIN_DEPLOY_RATE, check_c4
from ..fixtures import ReferenceFixture
from ..isolate import MockIsolate
from ..phenotype_overlap import (
    WEAK_AGENT_PRESETS,
    _apply_genotype_to_cfg,
    actor_pattern_histogram,
)
from ..selection import D8_MASS_FLOOR, D8_SELECTION_STRENGTH, update_deployment_mass
from ..variation_operator import (
    MUTATION_RATE,
    N_EXPRESSIVENESS_MUTANTS,
    mutate_program_map,
    sample_program_map_variants,
)
from ...oracle_only.stats import (
    N_PERMUTATIONS,
    observed_mass_range,
    permutation_mass_movement_band,
)
from ...world_visible.ecology_agents import programs_and_profiles_for_roster
from ...world_visible.program_map import ProgramMap, expand_preset, resolve_runtime_genotype
from ...world_visible.world import run_episode
from .base import PreconditionReport, RigResult

RIG_ID = "R-MB6a"

# --- V4-1 frozen protocol constants (do not tune post-registration) ----
MB6A_POPULATION_SIZE = 8
MB6A_N_GENERATIONS = 6
MB6A_EPISODES_PER_MEMBER = 2
MB6A_GENERATION_SEED_BASE = 60000
MB6A_EXPRESSIVENESS_SEED = 60100
MB6A_NULL_HARNESS_SEED = 60200


@dataclass
class _ProgramMapMember:
    member_id: str
    eng_program_map: ProgramMap


def check_precondition(fixture: ReferenceFixture) -> PreconditionReport:
    passed, measured = check_c4(list(fixture.results))
    satisfied = passed
    return PreconditionReport(
        rig_id=RIG_ID,
        satisfied=satisfied,
        measured=measured,
        threshold={
            "c4_min_deploy_rate_exclusive": C4_MIN_DEPLOY_RATE,
            "c4_max_deploy_rate_exclusive": C4_MAX_DEPLOY_RATE,
        },
        note=(
            "C4-class behavioral non-degeneracy: deploy rate strictly inside "
            f"({C4_MIN_DEPLOY_RATE}, {C4_MAX_DEPLOY_RATE}) on the fixture's "
            "reference traces (mechanical, from deploy outcomes only — "
            "PLAN_v4 R-MB6a precondition contract)."
        ),
    )


def _phenotype_key(hist: Counter[str]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(hist.items()))


def _run_eng1_with_program_map(
    fixture: ReferenceFixture,
    *,
    seed: int,
    program_map: ProgramMap,
    backend,
) -> Any:
    programs, profiles = programs_and_profiles_for_roster(
        fixture.roster, ecology_data=fixture.ecology_data
    )
    programs = dict(programs)
    profiles = dict(profiles)
    eng_id = fixture.cfg.actor_by_role("engineer").actor_id
    resolved = resolve_runtime_genotype(program_map)
    programs[eng_id] = resolved.program_key
    if resolved.behavior_profile:
        base = profiles.get(eng_id, {})
        profiles[eng_id] = {**base, **resolved.behavior_profile}
    cfg = _apply_genotype_to_cfg(fixture.cfg, actor_id=eng_id, resolved=resolved)
    return run_episode(cfg, seed, backend, programs=programs, behavior_profiles=profiles)


def run_expressiveness_report(
    fixture: ReferenceFixture,
    *,
    n_mutants: int = N_EXPRESSIVENESS_MUTANTS,
    progress: bool = True,
) -> dict[str, Any]:
    """Distinct primitive-pattern phenotypes from ``N_EXPRESSIVENESS_MUTANTS``
    valid ``ProgramMap`` edits on ``eng1`` (scorer-only slice, GL-54)."""
    backend = MockIsolate()
    eng_id = fixture.cfg.actor_by_role("engineer").actor_id
    baseline_pmap = expand_preset(WEAK_AGENT_PRESETS["engineer"], role="engineer")
    rng = random.Random(MB6A_EXPRESSIVENESS_SEED)
    variants = sample_program_map_variants(
        baseline_pmap, n=n_mutants, rng=rng
    )
    seen: set[tuple[tuple[str, int], ...]] = set()
    for i, variant in enumerate(variants):
        if progress and i % 10 == 0:
            print(f"[r-mb6a expressiveness {i + 1}/{len(variants)}]", flush=True)
        result = _run_eng1_with_program_map(
            fixture, seed=MB6A_EXPRESSIVENESS_SEED + i, program_map=variant, backend=backend
        )
        seen.add(_phenotype_key(actor_pattern_histogram(result, eng_id)))
    n_distinct = len(seen)
    fraction = n_distinct / len(variants) if variants else 0.0
    return {
        "n_mutants_requested": n_mutants,
        "n_mutants_sampled": len(variants),
        "n_distinct_phenotypes": n_distinct,
        "distinct_phenotype_fraction": fraction,
    }


def _episode_seed(generation: int, member_index: int, episode_index: int) -> int:
    return MB6A_GENERATION_SEED_BASE + generation * 1000 + member_index * 10 + episode_index


def _initial_population(rng: random.Random, *, population_size: int) -> list[_ProgramMapMember]:
    baseline = expand_preset(WEAK_AGENT_PRESETS["engineer"], role="engineer")
    members: list[_ProgramMapMember] = []
    for i in range(population_size):
        pmap = baseline
        if i > 0:
            mutated = mutate_program_map(baseline, rng=rng)
            if mutated is not None:
                pmap = mutated.program_map
        members.append(_ProgramMapMember(member_id=f"mb6a.{i:02d}", eng_program_map=pmap))
    return members


def _run_null_harness_trajectory(
    fixture: ReferenceFixture,
    *,
    uniform_fitness: bool,
    rng: random.Random,
    progress: bool,
    label: str,
    population_size: int = MB6A_POPULATION_SIZE,
    n_generations: int = MB6A_N_GENERATIONS,
    episodes_per_member: int = MB6A_EPISODES_PER_MEMBER,
) -> list[list[float]]:
    backend = MockIsolate()
    members = _initial_population(rng, population_size=population_size)
    generation_fitness: list[list[float]] = []
    for gen in range(n_generations):
        if progress:
            print(f"[r-mb6a {label} gen {gen + 1}/{n_generations}]", flush=True)
        fitness: list[float] = []
        for idx, member in enumerate(members):
            throughputs: list[float] = []
            for ep in range(episodes_per_member):
                seed = _episode_seed(gen, idx, ep)
                result = _run_eng1_with_program_map(
                    fixture,
                    seed=seed,
                    program_map=member.eng_program_map,
                    backend=backend,
                )
                throughputs.append(float(result.deploy_count))
            fitness.append(
                1.0 if uniform_fitness else (sum(throughputs) / len(throughputs))
            )
            if rng.random() < MUTATION_RATE:
                mutated = mutate_program_map(member.eng_program_map, rng=rng)
                if mutated is not None:
                    members[idx] = dataclasses.replace(
                        member, eng_program_map=mutated.program_map
                    )
        generation_fitness.append(fitness)
        if not uniform_fitness:
            masses = update_deployment_mass(
                [1.0 / len(members)] * len(members),
                fitness,
                selection_strength=D8_SELECTION_STRENGTH,
                mass_floor=D8_MASS_FLOOR,
            )
            # Resample members proportional to mass (discrete replicator step).
            draw = rng.random()
            cumulative = 0.0
            parent_idx = len(members) - 1
            for i, mass in enumerate(masses):
                cumulative += mass
                if draw <= cumulative:
                    parent_idx = i
                    break
            if parent_idx != len(members) - 1:
                members[-1] = dataclasses.replace(
                    members[-1],
                    eng_program_map=members[parent_idx].eng_program_map,
                )
    return generation_fitness


def run_null_harness_report(
    fixture: ReferenceFixture,
    *,
    progress: bool = True,
    population_size: int = MB6A_POPULATION_SIZE,
    n_generations: int = MB6A_N_GENERATIONS,
    episodes_per_member: int = MB6A_EPISODES_PER_MEMBER,
) -> dict[str, Any]:
    rng = random.Random(MB6A_NULL_HARNESS_SEED)
    null_fitness = _run_null_harness_trajectory(
        fixture,
        uniform_fitness=True,
        rng=rng,
        progress=progress,
        label="null",
        population_size=population_size,
        n_generations=n_generations,
        episodes_per_member=episodes_per_member,
    )
    null_range = observed_mass_range(
        null_fitness,
        selection_strength=D8_SELECTION_STRENGTH,
        mass_floor=D8_MASS_FLOOR,
    )
    band = permutation_mass_movement_band(
        null_fitness,
        seed=MB6A_NULL_HARNESS_SEED,
        selection_strength=D8_SELECTION_STRENGTH,
        mass_floor=D8_MASS_FLOOR,
    )
    p5_holds = null_range <= band["p97_5"]
    return {
        "uniform_fitness_mass_range": null_range,
        "permutation_band": band,
        "p5_harness_sane": {"holds": p5_holds},
        "protocol": {
            "population_size": population_size,
            "n_generations": n_generations,
            "episodes_per_member": episodes_per_member,
            "mutation_rate": MUTATION_RATE,
            "n_permutations": N_PERMUTATIONS,
        },
    }


def run_rig(
    fixture: ReferenceFixture,
    *,
    substrate_class: str = "S-inherited",
    progress: bool = True,
    n_expressiveness_mutants: int | None = None,
    population_size: int | None = None,
    n_generations: int | None = None,
    episodes_per_member: int | None = None,
) -> RigResult:
    n_expressiveness_mutants = (
        n_expressiveness_mutants
        if n_expressiveness_mutants is not None
        else N_EXPRESSIVENESS_MUTANTS
    )
    population_size = population_size if population_size is not None else MB6A_POPULATION_SIZE
    n_generations = n_generations if n_generations is not None else MB6A_N_GENERATIONS
    episodes_per_member = (
        episodes_per_member if episodes_per_member is not None else MB6A_EPISODES_PER_MEMBER
    )
    precondition = check_precondition(fixture)
    if not precondition.satisfied:
        return RigResult(
            rig_id=RIG_ID,
            precondition=precondition,
            outcome="skip",
            substrate_class=substrate_class,
            payload={},
            predictions={},
        )

    expressiveness = run_expressiveness_report(
        fixture, n_mutants=n_expressiveness_mutants, progress=progress
    )
    null_harness = run_null_harness_report(
        fixture,
        progress=progress,
        population_size=population_size,
        n_generations=n_generations,
        episodes_per_member=episodes_per_member,
    )
    predictions = {
        "expressiveness": expressiveness,
        "p5_harness_sane": null_harness["p5_harness_sane"],
    }
    outcome = "pass" if null_harness["p5_harness_sane"]["holds"] else "null"
    return RigResult(
        rig_id=RIG_ID,
        precondition=precondition,
        outcome=outcome,
        substrate_class=substrate_class,
        payload={
            "ecology_path": str(fixture.ecology_path),
            "null_harness": null_harness,
        },
        predictions=predictions,
    )
