"""Tier-K population generators — underlying variability, not noise injection."""

from __future__ import annotations

import random
from dataclasses import dataclass


def _clip01(x: float) -> float:
    return min(1.0, max(0.0, x))


@dataclass(frozen=True)
class HazardRegion:
    region_id: int
    alpha: float
    beta: float

    def sample_hazard(self, rng: random.Random) -> float:
        return _clip01(rng.betavariate(self.alpha, self.beta))


@dataclass(frozen=True)
class UserArchetype:
    archetype_id: int
    sensitivity: float
    base_incident_rate: float


def draw_hazard_regions(
    rng: random.Random,
    n_regions: int,
    alpha_range: tuple[float, float],
    beta_range: tuple[float, float],
    spread_scale: float = 1.0,
    safety_scale: float = 1.0,
) -> tuple[HazardRegion, ...]:
    """Draw per-region Beta(alpha, beta) hazard parameters.

    `safety_scale` multiplies alpha only: since E[Beta(a,b)] = a/(a+b), a
    smaller alpha (more build-time safety effort) lowers the region's mean
    hazard without touching `spread_scale`'s independent role (population
    heterogeneity, tuned in Phase 7, not per-build).
    """
    # `spread_scale` changes concentration but preserves each region's base
    # mean.  It is therefore a heterogeneity calibration input, not a hidden
    # hazard/difficulty dial.
    spread = max(spread_scale, 0.1)
    regions = []
    for i in range(n_regions):
        base_alpha = rng.uniform(*alpha_range) * safety_scale
        base_beta = rng.uniform(*beta_range)
        mean = base_alpha / (base_alpha + base_beta)
        concentration = (base_alpha + base_beta) / spread
        alpha = mean * concentration
        beta = (1.0 - mean) * concentration
        regions.append(HazardRegion(region_id=i, alpha=alpha, beta=beta))
    return tuple(regions)


def draw_user_archetypes(
    rng: random.Random,
    n_archetypes: int,
    sensitivity_spread: float,
    base_incident_rate: float,
    spread_scale: float = 1.0,
) -> tuple[UserArchetype, ...]:
    archetypes = []
    for i in range(n_archetypes):
        sens = _clip01(0.5 + rng.gauss(0.0, sensitivity_spread * spread_scale))
        # Centered variation preserves the expected base rate for every
        # calibration scale (the configured range keeps it in [0, 2*base]).
        rate = _clip01(
            base_incident_rate * (1.0 + spread_scale * (rng.random() - 0.5))
        )
        archetypes.append(UserArchetype(archetype_id=i, sensitivity=sens, base_incident_rate=rate))
    return tuple(archetypes)


def sample_eval_hazard(
    regions: tuple[HazardRegion, ...], rng: random.Random, draws: int
) -> tuple[float, float, int]:
    """Sample `draws` region hazards; return (mean, se, n)."""
    if not regions or draws <= 0:
        return 0.0, 0.0, 0
    samples = []
    for _ in range(draws):
        region = regions[rng.randrange(len(regions))]
        samples.append(region.sample_hazard(rng))
    mean = sum(samples) / len(samples)
    if len(samples) < 2:
        return mean, 0.0, len(samples)
    var = sum((x - mean) ** 2 for x in samples) / (len(samples) - 1)
    se = (var ** 0.5) / (len(samples) ** 0.5)
    return mean, se, len(samples)
