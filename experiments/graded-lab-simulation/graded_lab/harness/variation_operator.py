"""V2-4 / R-MB6a: closed edit vocabulary over ``ProgramMap`` genotypes.

Pre-registered constants and mutation operators for selection machinery
sanity (PLAN_v4 R-MB6a, ``REPRODUCTION.md`` §5). Mutations re-validate
mechanically via ``validate_program_map``; invalid mutants are discarded,
never repaired.

GL-54 note (carried forward): runtime currently wires ``scorer_only`` mode
to consult ``ProgramMap`` fields; ``walker_only`` on a walker preset is a
structural no-op. All sampled variants therefore force ``mode="scorer_only"``
so mutations can reach the isolate — same constraint as
``phenotype_overlap._mutate_program_map``.
"""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from typing import Any

from ..agent_visible.behavior_features import GOAL_FEATURES, PRIMITIVE_PATTERN_VOCAB
from ..world_visible.program_map import (
    GOAL_WEIGHT_BIN_COUNT,
    SCORE_LEVELS,
    TEMPERATURE_BINS,
    ProgramMap,
    ProgramMapError,
    validate_program_map,
)

# --- V4-1 frozen constants (R-MB6a, do not tune post-registration) ------
MUTATION_RATE = 0.3
N_EXPRESSIVENESS_MUTANTS = 100

EDIT_CLASSES = (
    "temperature_bin_nudge",
    "goal_weight_bin_nudge",
    "pattern_score_set",
    "hook_tweak",
)

# When ``pattern_scores`` is empty (``walk_pipeline`` engineer baseline), seed
# the first row from engineer-relevant patterns only.
_DEFAULT_ENGINEER_PATTERNS = (
    "pipeline:intake",
    "pipeline:build",
    "pipeline:eval",
    "pipeline:draft_report",
    "access:request",
)


@dataclass(frozen=True)
class MutationResult:
    program_map: ProgramMap
    edit_class: str


def _pattern_scores_key(pattern_scores: dict[str, Any]) -> tuple[tuple[str, tuple[tuple[str, float], ...]], ...]:
    """Hashable serialization for dedup (nested ``pattern_scores`` rows)."""
    return tuple(
        (pat, tuple(sorted((str(f), float(v)) for f, v in row.items())))
        for pat, row in sorted(pattern_scores.items())
        if isinstance(row, dict)
    )


def _pick_pattern_key(pattern_scores: dict[str, Any], rng: random.Random) -> str:
    if pattern_scores:
        return str(rng.choice(list(pattern_scores)))
    return str(rng.choice(_DEFAULT_ENGINEER_PATTERNS))


def _apply_edit(raw: dict[str, Any], *, role: str, rng: random.Random) -> MutationResult | None:
    candidate = copy.deepcopy(raw)
    candidate["mode"] = "scorer_only"
    candidate["preset_source"] = None
    edit_class = rng.choice(EDIT_CLASSES)

    if edit_class == "temperature_bin_nudge":
        idx = int(candidate.get("temperature_bin", 5))
        delta = rng.choice([-1, 1])
        candidate["temperature_bin"] = max(0, min(len(TEMPERATURE_BINS) - 1, idx + delta))
    elif edit_class == "goal_weight_bin_nudge":
        bins = list(candidate.get("goal_weight_bins", [2, 2, 2]))
        if len(bins) != 3:
            return None
        pos = rng.randrange(3)
        bins[pos] = (bins[pos] + rng.choice([-1, 1])) % GOAL_WEIGHT_BIN_COUNT
        candidate["goal_weight_bins"] = bins
    elif edit_class == "pattern_score_set":
        scoring = candidate.setdefault("scoring", {})
        pattern_scores = scoring.setdefault("pattern_scores", {})
        if not isinstance(pattern_scores, dict):
            return None
        pattern = _pick_pattern_key(pattern_scores, rng)
        if pattern not in PRIMITIVE_PATTERN_VOCAB:
            pattern = str(rng.choice(sorted(PRIMITIVE_PATTERN_VOCAB)))
        row = pattern_scores.get(pattern)
        if not isinstance(row, dict):
            row = {}
        feature = str(rng.choice(sorted(GOAL_FEATURES)))
        row[feature] = float(SCORE_LEVELS[rng.randrange(len(SCORE_LEVELS))])
        pattern_scores[pattern] = row
    elif edit_class == "hook_tweak":
        hooks = candidate.setdefault("hooks", {})
        if not isinstance(hooks, dict):
            return None
        if "eval_draws" in hooks:
            options = ["min", "default", "max"]
            hooks["eval_draws"] = rng.choice([o for o in options if o != hooks.get("eval_draws")] or options)
        elif "communicate_cadence" in hooks:
            options = ["never", "sparse", "often"]
            hooks["communicate_cadence"] = rng.choice(
                [o for o in options if o != hooks.get("communicate_cadence")] or options
            )
        else:
            hooks["eval_draws"] = rng.choice(["min", "default", "max"])
    else:
        return None

    try:
        pmap = validate_program_map(candidate, role=role, strict_ladder=False)
    except ProgramMapError:
        return None
    return MutationResult(program_map=pmap, edit_class=edit_class)


def mutate_program_map(
    pmap: ProgramMap, *, rng: random.Random, max_attempts: int = 20
) -> MutationResult | None:
    """One random edit from the closed vocabulary; None if all attempts fail."""
    raw = {
        "mode": pmap.mode,
        "walker": copy.deepcopy(pmap.walker),
        "scoring": copy.deepcopy(pmap.scoring),
        "stated_feature_deltas": dict(pmap.stated_feature_deltas),
        "hooks": dict(pmap.hooks),
        "temperature_bin": pmap.temperature_bin,
        "goal_weight_bins": list(pmap.goal_weight_bins),
        "preset_source": pmap.preset_source,
    }
    for _ in range(max_attempts):
        result = _apply_edit(raw, role=pmap.role, rng=rng)
        if result is not None:
            return result
    return None


def sample_program_map_variants(
    pmap: ProgramMap, *, n: int, rng: random.Random
) -> list[ProgramMap]:
    """Sample up to ``n`` syntax-distinct valid ``ProgramMap`` variants."""
    seen: set[tuple[Any, ...]] = set()
    out: list[ProgramMap] = []
    attempts = 0
    while len(out) < n and attempts < n * 20:
        attempts += 1
        mutated = mutate_program_map(pmap, rng=rng)
        if mutated is None:
            continue
        m = mutated.program_map
        key = (
            m.mode,
            m.temperature_bin,
            m.goal_weight_bins,
            _pattern_scores_key(m.scoring.get("pattern_scores", {})),
            tuple(sorted(m.hooks.items())),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(m)
    return out
