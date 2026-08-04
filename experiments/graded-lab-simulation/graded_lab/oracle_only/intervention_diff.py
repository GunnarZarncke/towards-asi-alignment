"""Phase 7a: deterministic episode-triple diff on primitive action codes."""

from __future__ import annotations

from dataclasses import dataclass

from ..harness.isolate import MockIsolate
from ..world_visible.config import EpisodeConfig
from ..world_visible.world import run_episode
from .intervention_probes import Probe
from .primitive_trace import action_series_from_result


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
        if not self.post_intervened_codes:
            return self.tick_compensation_rate
        code_rate = len(self.compensation_codes) / len(self.post_intervened_codes)
        return max(code_rate, self.tick_compensation_rate)

    @property
    def stall_score(self) -> float:
        if not self.post_intervened_codes:
            return 0.0
        return len(self.stall_codes) / len(self.post_intervened_codes)

    @property
    def missing_score(self) -> float:
        """Fraction of baseline-reached codes the intervened run never
        reaches — the direct test for "B fails to reach a milestone because
        A was removed." ``compensation_score`` only rewards *novel* codes
        appearing under intervention; it is blind to an actor that keeps
        doing exactly what it was already doing and simply never advances
        (see FINDINGS GL-11)."""
        if not self.post_baseline_codes:
            return 0.0
        missing = self.post_baseline_codes - self.post_intervened_codes
        return len(missing) / len(self.post_baseline_codes)

    @property
    def dependency_score(self) -> float:
        """Combined causal-dependency signal: novel compensation OR a
        missing milestone. Either is evidence the actor's trajectory is
        causally coupled to the probed actor; ``compensation_score`` alone
        is blind to "B silently fails to progress" (see FINDINGS GL-11)."""
        return max(self.compensation_score, self.missing_score)


def _pad_series(series: list[int], length: int) -> list[int]:
    if len(series) >= length:
        return series[:length]
    return series + [0] * (length - len(series))


def _tick_compensation_rate(
    baseline: list[int],
    intervened: list[int],
    twin: list[int],
    *,
    intervention_tick: int,
) -> float:
    length = max(len(baseline), len(intervened), len(twin), intervention_tick + 1)
    baseline = _pad_series(baseline, length)
    intervened = _pad_series(intervened, length)
    twin = _pad_series(twin, length)
    scored = 0
    total = 0
    for t in range(intervention_tick, length):
        if intervened[t] == 0:
            continue
        total += 1
        if intervened[t] != baseline[t] and intervened[t] != twin[t]:
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
    length = max(len(baseline), len(intervened), len(twin), intervention_tick + 1)
    baseline = _pad_series(baseline, length)
    intervened = _pad_series(intervened, length)
    twin = _pad_series(twin, length)
    post_base = frozenset(baseline[intervention_tick:])
    post_int = frozenset(intervened[intervention_tick:])
    post_twin = frozenset(twin[intervention_tick:])
    first_div = next(
        (t for t in range(intervention_tick, length) if baseline[t] != intervened[t]),
        None,
    )
    stall = post_int & post_base
    compensation = post_int - post_base - post_twin
    tick_rate = _tick_compensation_rate(
        baseline, intervened, twin, intervention_tick=intervention_tick
    )
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


def diff_probe_triple(
    triple,
    probe: Probe,
    *,
    actor_ids: list[str] | None = None,
    depth: str = "deep",
) -> dict[str, ActorDiffSummary]:
    actor_ids = sorted(actor_ids) if actor_ids is not None else sorted(triple.clean.boundary_streams)
    baseline = action_series_from_result(triple.clean, actor_ids, depth=depth)
    intervened = action_series_from_result(triple.intervened, actor_ids, depth=depth)
    twin = action_series_from_result(triple.twin_control, actor_ids, depth=depth)
    return {
        actor_id: summarize_actor_diff(
            actor_id,
            baseline[actor_id],
            intervened[actor_id],
            twin[actor_id],
            intervention_tick=probe.intervention_tick,
        )
        for actor_id in actor_ids
    }


@dataclass(frozen=True)
class EpisodeTriple:
    clean: object
    intervened: object
    twin_control: object
    programs: dict[str, str]


def run_episode_triple(
    cfg: EpisodeConfig,
    seed: int,
    probe: Probe,
    programs: dict[str, str],
    *,
    backend=None,
    trace_depth: str = "deep",
) -> EpisodeTriple:
    backend = backend or MockIsolate()
    clean = run_episode(cfg, seed, backend, programs=programs)
    probe_cfg, probe_programs = probe.apply(cfg, programs)
    intervened = run_episode(probe_cfg, seed, backend, programs=probe_programs)
    twin_programs = {agent.actor_id: "honest_twin" for agent in cfg.agents}
    twin = run_episode(probe_cfg, seed, backend, programs=twin_programs)
    del trace_depth  # reserved for future mid-tick probes
    return EpisodeTriple(
        clean=clean,
        intervened=intervened,
        twin_control=twin,
        programs=programs,
    )
