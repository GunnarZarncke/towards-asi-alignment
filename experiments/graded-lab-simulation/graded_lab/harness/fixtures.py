"""Shared fixture layer for v4 per-bridge rigs (PLAN_v4 V4-0).

``ReferenceFixture`` bundles one (ecology, roster, seed-set) tuple's
already-run reference episodes. Rigs consume a fixture's traces; they do
not re-simulate (PLAN_v4 architecture item 2). This module also promotes
the GL-75c ``ProcessPoolExecutor`` pattern out of
``machinery_transfer.py`` so every rig can build its fixture in parallel
the same way, instead of each rig re-implementing pool bookkeeping.

This is deliberately a thin wrapper around pieces that already existed
(``reference_bundle`` in ``machinery_transfer.py``, ``run_episode``):
V4-0's gate is that GL-76 reproduces bit-for-bit through this plumbing,
so nothing about episode construction changes here, only how the traces
are assembled and shared.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import WEAK_AGENT
from ..world_visible.config import EpisodeConfig
from ..world_visible.ecology_agents import (
    EcologyRoster,
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from ..world_visible.substrate import load_substrate
from ..world_visible.world import run_episode
from .ecology_complexity import _reference_episode_config


@dataclass(frozen=True)
class ReferenceFixture:
    """One (ecology_path, roster, seed-set) tuple's reference traces.

    ``results_by_seed`` holds already-executed ``EpisodeResult`` objects;
    rigs read from it (or from ``results``) rather than calling
    ``run_episode`` again.
    """

    ecology_path: Path
    ecology_data: dict
    roster: EcologyRoster
    cfg: EpisodeConfig
    programs: dict[str, str]
    profiles: dict
    seeds: tuple[int, ...]
    results_by_seed: dict[int, Any] = field(repr=False)
    agent_type: str = WEAK_AGENT

    @property
    def results(self) -> list[Any]:
        return [self.results_by_seed[s] for s in self.seeds]


_FIXTURE_CTX: dict[str, Any] | None = None


def _init_fixture_worker(ctx: dict[str, Any]) -> None:
    global _FIXTURE_CTX
    _FIXTURE_CTX = ctx


def _work_fixture_seed(seed: int) -> tuple[int, Any]:
    from .isolate import MockIsolate

    assert _FIXTURE_CTX is not None
    result = run_episode(
        _FIXTURE_CTX["cfg"],
        seed,
        MockIsolate(),
        programs=_FIXTURE_CTX["programs"],
        behavior_profiles=_FIXTURE_CTX["profiles"],
    )
    return seed, result


def _run_episodes_parallel(
    cfg: EpisodeConfig,
    seeds: tuple[int, ...],
    programs: dict[str, str],
    profiles: dict,
    *,
    workers: int,
    progress: bool,
    label: str,
) -> dict[int, Any]:
    ctx = {"cfg": cfg, "programs": programs, "profiles": profiles}
    results_by_seed: dict[int, Any] = {}
    with ProcessPoolExecutor(
        max_workers=workers, initializer=_init_fixture_worker, initargs=(ctx,)
    ) as pool:
        futures = {pool.submit(_work_fixture_seed, seed): seed for seed in seeds}
        done = 0
        for fut in as_completed(futures):
            done += 1
            seed, result = fut.result()
            results_by_seed[seed] = result
            if progress:
                print(f"[{label} parallel {done}/{len(seeds)}] seed={seed} done", flush=True)
    return results_by_seed


def build_reference_fixture(
    ecology_path: Path | str,
    *,
    seeds: tuple[int, ...],
    agent_type: str = WEAK_AGENT,
    backend=None,
    workers: int = 1,
    progress: bool = True,
    label: str = "fixture",
) -> ReferenceFixture:
    """Build one ``ReferenceFixture`` (substrate + roster + episode traces).

    Rigs that need only these reference episodes should call this once and
    reuse the returned fixture for every precondition check and battery;
    they must not call ``run_episode`` again for the same
    (ecology_path, seeds, agent_type) tuple.
    """
    from .isolate import MockIsolate

    ecology_path = Path(ecology_path)
    ecology_data = load_substrate(ecology_path).data
    roster = reference_roster_from_ecology(
        ecology_data, agent_type=agent_type, temperature=0.35
    )
    cfg = _reference_episode_config(ecology_data, ecology_path=ecology_path)
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=ecology_data)

    if workers > 1:
        results_by_seed = _run_episodes_parallel(
            cfg, seeds, programs, profiles, workers=workers, progress=progress, label=label
        )
    else:
        backend = backend or MockIsolate()
        results_by_seed = {}
        for i, seed in enumerate(seeds):
            if progress:
                print(
                    f"[{label} {i + 1}/{len(seeds)}] seed={seed} ecology={ecology_path.name}",
                    flush=True,
                )
            results_by_seed[seed] = run_episode(
                cfg, seed, backend, programs=programs, behavior_profiles=profiles
            )

    return ReferenceFixture(
        ecology_path=ecology_path,
        ecology_data=ecology_data,
        roster=roster,
        cfg=cfg,
        programs=programs,
        profiles=profiles,
        seeds=tuple(seeds),
        results_by_seed=results_by_seed,
        agent_type=agent_type,
    )
