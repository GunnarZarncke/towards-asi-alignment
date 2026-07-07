"""S6 phase 1 (PLAN.md "S6 — intervention-supported UAD"): deterministic
episode-pair diff substrate.

Runs the SAME (config, seed) twice — once clean, once with one scripted
intervention — and diffs per-actor action-code trajectories tick by tick.
At MockIsolate scale every divergence after the intervention tick is
EXACTLY attributable (the ``twins.py`` same-seed counterfactual pattern,
pointed at interventions instead of program swaps).

Action codes come from ``uad_mi.build_lab_trace`` (``depth="shallow"``,
``.tool`` column only) so diffs are comparable across detectors and
runs. Classification per actor:

- *stall*: post-intervention action CODE already appeared in the actor's
  baseline trace (timing/shift/retry — mechanical propagation).
- *compensation*: post-intervention action CODE absent from BOTH the
  clean baseline AND the honest-twin-under-the-same-intervention
  control — divergence-in-kind, the unit signal from PLAN.md's S6
  section.

Recorded referee extension: own module, never touches frozen code.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..harness.isolate import MockIsolate
from ..world_visible.config import LabConfig
from ..world_visible.world import run_episode
from .detectors import build_audit_view
from .intervention_probes import Probe, intervention_tick
from .uad_mi import build_lab_trace


def action_series_by_actor(
    tool_events, actor_ids: list[str], *, horizon: int | None = None, depth: str = "shallow"
) -> dict[str, list[int]]:
    """Per-actor ``.tool`` code series from full-tier tool events."""
    trace, _ = build_lab_trace(tool_events, actor_ids, depth=depth, horizon=horizon)
    if not trace:
        return {a: [] for a in actor_ids}
    return {a: [row[f"{a}.tool"] for row in trace] for a in actor_ids}


def action_series_from_result(
    result, actor_ids: list[str] | None = None, *, horizon: int | None = None, depth: str = "shallow"
) -> dict[str, list[int]]:
    view = build_audit_view(result, "full")
    actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(result.host.roles)
    if horizon is None and view.tool_events:
        horizon = max(int(e.get("t", 0)) for e in view.tool_events) + 1
    return action_series_by_actor(view.tool_events, actor_ids, horizon=horizon, depth=depth)


@dataclass(frozen=True)
class ActorDiffSummary:
    actor_id: str
    intervention_tick: int
    first_divergent_tick: int | None
    post_baseline_codes: frozenset[int]
    post_intervened_codes: frozenset[int]
    post_twin_codes: frozenset[int]
    stall_codes: frozenset[int]
    compensation_codes: frozenset[int]
    tick_compensation_rate: float

    @property
    def compensation_score(self) -> float:
        """Blend of code-set novelty (in-kind actions) and tick-aligned
        divergence from BOTH baseline and twin control."""
        if not self.post_intervened_codes:
            return self.tick_compensation_rate
        code_rate = len(self.compensation_codes) / len(self.post_intervened_codes)
        return max(code_rate, self.tick_compensation_rate)

    @property
    def stall_score(self) -> float:
        if not self.post_intervened_codes:
            return 0.0
        return len(self.stall_codes) / len(self.post_intervened_codes)


def _pad_series(series: list[int], length: int) -> list[int]:
    if len(series) >= length:
        return series[:length]
    return series + [0] * (length - len(series))


def _tick_compensation_rate(
    baseline: list[int], intervened: list[int], twin: list[int], *, intervention_tick: int
) -> float:
    length = max(len(baseline), len(intervened), len(twin), intervention_tick + 1)
    b = _pad_series(baseline, length)
    i = _pad_series(intervened, length)
    tw = _pad_series(twin, length)
    scored = 0
    total = 0
    for t in range(intervention_tick, length):
        if i[t] == 0:
            continue
        total += 1
        if i[t] != b[t] and i[t] != tw[t]:
            scored += 1
    return scored / total if total else 0.0


def summarize_actor_diff(
    actor_id: str,
    baseline: list[int],
    intervened: list[int],
    twin: list[int],
    *,
    intervention_tick: int,
) -> ActorDiffSummary:
    """Compare one actor's action-code trajectories from ``intervention_tick``
    onward across clean / intervened / twin-intervened runs."""
    length = max(len(baseline), len(intervened), len(twin), intervention_tick + 1)
    baseline = _pad_series(baseline, length)
    intervened = _pad_series(intervened, length)
    twin = _pad_series(twin, length)
    post_base = frozenset(baseline[intervention_tick:])
    post_int = frozenset(intervened[intervention_tick:])
    post_twin = frozenset(twin[intervention_tick:])
    first_div = next((t for t in range(intervention_tick, length) if baseline[t] != intervened[t]), None)
    stall = post_int & post_base
    compensation = post_int - post_base - post_twin
    tick_rate = _tick_compensation_rate(baseline, intervened, twin, intervention_tick=intervention_tick)
    return ActorDiffSummary(
        actor_id=actor_id,
        intervention_tick=intervention_tick,
        first_divergent_tick=first_div,
        post_baseline_codes=post_base,
        post_intervened_codes=post_int,
        post_twin_codes=post_twin,
        stall_codes=stall,
        compensation_codes=compensation,
        tick_compensation_rate=tick_rate,
    )


def diff_episode_triple(
    baseline_series: dict[str, list[int]],
    intervened_series: dict[str, list[int]],
    twin_series: dict[str, list[int]],
    *,
    intervention_tick: int,
    actor_ids: list[str] | None = None,
) -> dict[str, ActorDiffSummary]:
    actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(baseline_series)
    return {
        a: summarize_actor_diff(
            a,
            baseline_series[a],
            intervened_series[a],
            twin_series[a],
            intervention_tick=intervention_tick,
        )
        for a in actor_ids
    }


@dataclass(frozen=True)
class EpisodeTriple:
    clean: object
    intervened: object
    twin_control: object
    horizon: int
    trace_depth: str = "deep"


def run_episode_triple(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    trace_depth: str = "deep",
) -> EpisodeTriple:
    """Clean + intervened + honest-twin-under-same-intervention runs."""
    backend = backend or MockIsolate()
    horizon = cfg.T
    merged_overrides = dict(agent_overrides or {})
    clean = run_episode(cfg, seed=seed, backend=backend, agent_overrides=merged_overrides or None)
    probe_cfg, probe_kwargs = probe.apply(cfg)
    intervened = run_episode(
        probe_cfg, seed=seed, backend=backend, agent_overrides=merged_overrides or None, **probe_kwargs
    )
    twin = run_episode(
        probe_cfg,
        seed=seed,
        backend=backend,
        program_override="honest_twin",
        agent_overrides=merged_overrides or None,
        **probe_kwargs,
    )
    return EpisodeTriple(
        clean=clean, intervened=intervened, twin_control=twin, horizon=horizon, trace_depth=trace_depth
    )


def diff_probe_triple(
    triple: EpisodeTriple,
    probe: Probe,
    actor_ids: list[str] | None = None,
    *,
    horizon: int | None = None,
    depth: str | None = None,
) -> dict[str, ActorDiffSummary]:
    actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(triple.clean.host.roles)
    t0 = intervention_tick(probe, triple.clean)
    horizon = horizon if horizon is not None else triple.horizon
    depth = depth if depth is not None else triple.trace_depth
    baseline = action_series_from_result(triple.clean, actor_ids, horizon=horizon, depth=depth)
    intervened = action_series_from_result(triple.intervened, actor_ids, horizon=horizon, depth=depth)
    twin = action_series_from_result(triple.twin_control, actor_ids, horizon=horizon, depth=depth)
    return diff_episode_triple(baseline, intervened, twin, intervention_tick=t0, actor_ids=actor_ids)


def cleanup_triple(triple: EpisodeTriple) -> None:
    triple.clean.cleanup()
    triple.intervened.cleanup()
    triple.twin_control.cleanup()
