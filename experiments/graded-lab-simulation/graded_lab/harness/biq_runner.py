"""Same-seed ecology-BIQ episodes and counterfactual baselines."""

from __future__ import annotations

from typing import Any

from ..oracle_only.trace_diagnostics import compute_role_boundary_proxy
from ..world_visible.config import EpisodeConfig
from ..world_visible.world import EpisodeResult, run_episode


def run_with_baselines(
    cfg: EpisodeConfig, seed: int, backend_factory: Any, *, programs: dict[str, str] | None = None
) -> tuple[EpisodeResult, EpisodeResult, EpisodeResult, dict[str, dict[str, float]]]:
    """Run real, noop, and random-affordable episodes on identical seed/config."""
    real = run_episode(cfg, seed, backend_factory(), programs=programs)
    noop_programs = {agent.actor_id: "noop" for agent in cfg.agents}
    random_programs = {agent.actor_id: "random_affordable" for agent in cfg.agents}
    noop = run_episode(cfg, seed, backend_factory(), programs=noop_programs)
    random = run_episode(cfg, seed, backend_factory(), programs=random_programs)
    reports = {
        agent.actor_id: compute_role_boundary_proxy(
            real, noop, random, agent.actor_id, cfg.T
        )
        for agent in cfg.agents
    }
    return real, noop, random, reports
