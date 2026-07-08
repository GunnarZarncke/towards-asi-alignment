""""Noise-tolerant S6" (PLAN.md open design question (b); FINDINGS.md
G-32/G-33): a NEW, separate detector variant that replaces S6's fixed,
per-tick, set-membership compensation test with a statistically
calibrated one.

**Why a new module, not an edit to `uad_intervention.py`.** That module
(with `uad_peel.py`/`uad_partition.py`, G-28/G-29) is named explicitly
in `DESIGN.md`'s "Freeze note 2 (detector layer, S6/S7)": its logic and
pre-registered defaults (`DEFAULT_MIN_COMPENSATION=0.15` etc.) are a
recorded referee extension every existing pre-registered battery
(`run_s6_intervention_uad.py`, `run_s7_blind_battery.py`) depends on
staying unchanged. This module imports `candidate_edges_for_intervention`
and reuses `intervention_diff`/`intervention_probes` (S6 phases 1-2,
never modified by this module either) but otherwise stands alone. Its
own defaults below are explicitly NOT battery-validated -- a first
pass, pre-registered but tightenable, not a third freeze (see this
module's own "Pre-registration, not a freeze" note below).

**The principled framing this module implements (G-32's follow-up
question).** An interventional audit against a system with its own
internal stochasticity (a real LLM call; more generally, any real-world
process) can never compare literal counterfactuals -- there is no
byte-identical replay to diff against. What CAN be measured is whether
the intervened trace's outcome statistic is more different from a
baseline reference than several INDEPENDENT baseline replicates are
from EACH OTHER -- i.e. whether the observed divergence sits outside
the run's own measured null, at a stated quantile, rather than merely
"nonzero" (S6's implicit assumption). This generalizes correctly
across backends WITHOUT special-casing: a scripted `MockIsolate`/
`SubprocessIsolate` agent at `temperature=0` produces byte-identical
replicate replays, so the empirical null has ZERO width and ANY
nonzero divergence clears it -- recovering S6's original fixed-
threshold behavior EXACTLY, for the regime it was built and battery-
validated for (verified by `test_intervention_stats.py`'s equivalence
tests against `uad_intervention.discovered_units_intervention`'s frozen
partition results). Only when the backend has its own internal
stochasticity does the null widen to reflect that -- the ONLY regime
where the frozen fixed-threshold detector was shown to fail (G-32).

**The observable is also re-based, from per-TICK action code (fragile:
needs exact alignment, and G-32's follow-up root-cause probe found the
"code-novelty" half of the old score structurally dead for this line's
~10-20-code-wide role vocabulary -- baseline union twin already
exhausts it) to a per-actor, per-post-intervention-WINDOW action-code
FREQUENCY histogram, compared via total-variation distance --
order/timing-invariant within the window, bounded in [0, 1], and
naturally collapses genuine "stall" (same codes re-executed, same
distribution) to zero added divergence while genuine compensation
(a different code-usage distribution) shows up as nonzero -- the same
distinction S6's stall/compensation split targeted, at a coarser,
noise-robust grain.

**Pre-registration, not a freeze (2026-07-08, user's explicit framing:
"choose a configurable replication k that likely delivers signal but
doesn't have to be guaranteed safe... tightened later").**
`DEFAULT_K_CLEAN_REPLICATES=4`, `DEFAULT_NULL_QUANTILE=0.90`, and
`DEFAULT_MIN_EFFECT_VS_TWIN=0.05` are chosen defaults, not
battery-validated ones -- k=4 gives only 6 pairwise null samples,
enough to plausibly separate signal from noise at the effect sizes
G-32 measured (eng1/rm1 ~0.15-0.17), not enough for a rigorous
small-sample confidence claim. Unlike `DEFAULT_MIN_COMPENSATION=0.15`
(S6, frozen), these three constants are explicitly open to retuning
without being a "silent retuning" violation -- record any change here,
do not silently ship a different value.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..harness.isolate import MockIsolate
from ..world_visible.config import LabConfig
from ..world_visible.world import run_episode
from .intervention_diff import action_series_from_result
from .intervention_probes import Probe, all_default_probes, default_probe_for_actor
from .uad_intervention import candidate_edges_for_intervention

DEFAULT_K_CLEAN_REPLICATES = 4
DEFAULT_NULL_QUANTILE = 0.90
DEFAULT_MIN_EFFECT_VS_TWIN = 0.05
DEFAULT_INTERVENTION_TICK = 8


def code_histogram(series: list[int], from_tick: int) -> dict[int, float]:
    """Normalized frequency of each action code at ticks >= ``from_tick``
    -- order/timing-invariant within the window, unlike S6's per-tick
    equality test."""
    window = series[from_tick:]
    if not window:
        return {}
    counts: dict[int, int] = {}
    for code in window:
        counts[code] = counts.get(code, 0) + 1
    n = len(window)
    return {code: count / n for code, count in counts.items()}


def total_variation_distance(hist_a: dict[int, float], hist_b: dict[int, float]) -> float:
    codes = set(hist_a) | set(hist_b)
    return 0.5 * sum(abs(hist_a.get(c, 0.0) - hist_b.get(c, 0.0)) for c in codes)


def outcome_divergence(series_a: list[int], series_b: list[int], *, from_tick: int) -> float:
    return total_variation_distance(code_histogram(series_a, from_tick), code_histogram(series_b, from_tick))


def _quantile(samples: list[float], q: float) -> float:
    """Linear-interpolation quantile, stdlib only (no numpy dependency
    anywhere else in this line either). Degenerate (<2 samples -- every
    scripted-backend replicate is byte-identical, so there is never more
    than ONE distinct value) returns 0.0, recovering S6's original "any
    nonzero divergence is signal" behavior for a zero-variance regime."""
    if len(samples) < 2:
        return 0.0
    ordered = sorted(samples)
    idx = q * (len(ordered) - 1)
    lo, hi = int(idx), min(int(idx) + 1, len(ordered) - 1)
    frac = idx - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


@dataclass(frozen=True)
class NullStats:
    """``k`` independent CLEAN (no probe) replicate traces of the SAME
    (cfg, seed, agent_overrides) -- the raw material for an empirical,
    per-actor, per-window null. Divergence samples and thresholds are
    computed lazily per requested ``from_tick`` (different probes use
    different intervention ticks -- channel-ablation probes fire at
    tick 0, actor-directed probes at ``DEFAULT_INTERVENTION_TICK`` --
    so caching by tick up front would either waste replicate runs on
    windows nothing asks for, or require re-running replicates per
    probe; computing on demand from the SAME cached series is free and
    avoids both)."""

    replicate_series: tuple[dict[str, list[int]], ...]

    def samples_at(self, actor_id: str, from_tick: int) -> list[float]:
        out: list[float] = []
        for i in range(len(self.replicate_series)):
            for j in range(i + 1, len(self.replicate_series)):
                a = self.replicate_series[i].get(actor_id, [])
                b = self.replicate_series[j].get(actor_id, [])
                out.append(outcome_divergence(a, b, from_tick=from_tick))
        return out

    def threshold_at(self, actor_id: str, from_tick: int, q: float) -> float:
        return _quantile(self.samples_at(actor_id, from_tick), q)

    def reference_series(self, actor_id: str) -> list[int]:
        """Replicate 0, arbitrary but fixed -- the comparison anchor for
        the intervened run. (A smoothed/averaged reference across all k
        replicates would reduce this anchor's own noise contribution;
        not attempted in this first pass -- see module docstring.)"""
        return self.replicate_series[0].get(actor_id, []) if self.replicate_series else []


def calibrate_clean_null(
    cfg: LabConfig,
    seed: int,
    actor_ids: list[str],
    *,
    backend=None,
    agent_overrides: dict | None = None,
    k_replicates: int = DEFAULT_K_CLEAN_REPLICATES,
    horizon: int | None = None,
    depth: str = "deep",
) -> NullStats:
    """Run ``k_replicates`` INDEPENDENT clean (no-probe) episodes of the
    identical (cfg, seed, agent_overrides) and cache their action-code
    series. Cost note: each replicate is a full episode -- for an
    LLM-backed actor, real API spend; for a scripted backend, replicates
    are byte-identical (deterministic replay of the same seed), so
    k_replicates=2 (the minimum needed for a defined, if degenerate,
    threshold) suffices and wastes nothing beyond one redundant episode."""
    if k_replicates < 2:
        raise ValueError("k_replicates must be >= 2 to define a null distribution")
    horizon = horizon if horizon is not None else cfg.T
    series: list[dict[str, list[int]]] = []
    for _ in range(k_replicates):
        result = run_episode(cfg, seed=seed, backend=backend, agent_overrides=agent_overrides or None)
        try:
            series.append(action_series_from_result(result, actor_ids, horizon=horizon, depth=depth))
        finally:
            result.cleanup()
    return NullStats(replicate_series=tuple(series))


@dataclass(frozen=True)
class CompensationStatsResult:
    actor_id: str
    divergence_from_clean: float
    divergence_from_twin: float
    null_threshold: float
    exceeds_null: bool
    clears_twin_floor: bool

    @property
    def compensates(self) -> bool:
        """Dual test, same spirit as S6's stall/compensation split: the
        intervened trace must be unusually FAR from ordinary behavior
        (``exceeds_null``, calibrated against measured replicate noise --
        the relative rule) AND not simply reproduce what an honest
        scripted default would do under the identical probe
        (``clears_twin_floor`` -- the not-just-mechanical-propagation
        check, still a fixed floor, see module docstring)."""
        return self.exceeds_null and self.clears_twin_floor

    def to_dict(self) -> dict:
        return {
            "actor_id": self.actor_id,
            "divergence_from_clean": self.divergence_from_clean,
            "divergence_from_twin": self.divergence_from_twin,
            "null_threshold": self.null_threshold,
            "exceeds_null": self.exceeds_null,
            "clears_twin_floor": self.clears_twin_floor,
            "compensates": self.compensates,
        }


def probe_compensation_stats(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    responders: list[str],
    null_stats: NullStats,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    null_quantile_q: float = DEFAULT_NULL_QUANTILE,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    horizon: int | None = None,
    depth: str = "deep",
) -> dict[str, CompensationStatsResult]:
    """ONE intervened+twin run (twin is free -- see
    ``intervention_diff.run_episode_triple``'s docstring: it forces every
    ``agent_overrides`` actor onto a scripted ``honest_twin``, so it
    never calls a real LLM) scored for EVERY responder in ``responders``
    against the SHARED ``null_stats`` computed once per scenario. Uses
    ``probe.intervention_tick`` as the post-intervention window start --
    channel-ablation probes fire at tick 0 (the whole episode is the
    window); actor-directed probes fire later."""
    backend = backend or MockIsolate()
    horizon = horizon if horizon is not None else cfg.T
    from_tick = probe.intervention_tick
    probe_cfg, probe_kwargs = probe.apply(cfg)
    intervened = run_episode(
        probe_cfg, seed=seed, backend=backend, agent_overrides=agent_overrides or None, **probe_kwargs
    )
    twin_overrides = {a: (backend, "honest_twin") for a in (agent_overrides or {})}
    twin = run_episode(
        probe_cfg,
        seed=seed,
        backend=backend,
        program_override="honest_twin",
        agent_overrides=twin_overrides or None,
        **probe_kwargs,
    )
    try:
        intervened_series = action_series_from_result(intervened, responders, horizon=horizon, depth=depth)
        twin_series = action_series_from_result(twin, responders, horizon=horizon, depth=depth)
        out: dict[str, CompensationStatsResult] = {}
        for r in responders:
            clean_ref = null_stats.reference_series(r)
            div_clean = outcome_divergence(intervened_series[r], clean_ref, from_tick=from_tick)
            div_twin = outcome_divergence(intervened_series[r], twin_series[r], from_tick=from_tick)
            threshold = null_stats.threshold_at(r, from_tick, null_quantile_q)
            out[r] = CompensationStatsResult(
                actor_id=r,
                divergence_from_clean=div_clean,
                divergence_from_twin=div_twin,
                null_threshold=threshold,
                exceeds_null=div_clean > threshold,
                clears_twin_floor=div_twin >= min_effect_vs_twin,
            )
        return out
    finally:
        intervened.cleanup()
        twin.cleanup()


def directed_compensation_stats(
    cfg: LabConfig, seed: int, probe: Probe, responder: str, null_stats: NullStats, **kwargs
) -> CompensationStatsResult:
    return probe_compensation_stats(cfg, seed, probe, [responder], null_stats, **kwargs)[responder]


def _probe_for_actor(probes: list[Probe], actor_id: str) -> Probe | None:
    """Same selection rule as ``uad_intervention._probe_for_actor``
    (duplicated, not imported: it is a private helper of a
    Freeze-note-2-covered module, and this four-line rule is cheaper to
    keep local than to import a leading-underscore symbol across a
    module boundary)."""
    for probe in probes:
        if probe.target_actor == actor_id and probe.kind != "channel_ablation":
            return probe
    for probe in probes:
        if probe.kind == "channel_ablation":
            return probe
    return None


def compensation_matrix_stats(
    cfg: LabConfig,
    seed: int,
    edges: list[tuple[str, str]],
    probes: list[Probe],
    null_stats: NullStats,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    null_quantile_q: float = DEFAULT_NULL_QUANTILE,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
) -> dict[tuple[str, str], CompensationStatsResult]:
    """R[source][target], directed, actor-probe matrix -- ONE triple per
    SOURCE (not per source-target pair): every other actor is scored as
    a responder from that same triple, same efficiency as S6's
    ``uad_intervention.compensation_matrix``."""
    matrix: dict[tuple[str, str], CompensationStatsResult] = {}
    actors = sorted({a for e in edges for a in e})
    for source in actors:
        probe = _probe_for_actor(probes, source) or default_probe_for_actor(cfg, source)
        targets = [a for a in actors if a != source]
        if not targets:
            continue
        results = probe_compensation_stats(
            cfg, seed, probe, targets, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            null_quantile_q=null_quantile_q, min_effect_vs_twin=min_effect_vs_twin,
        )
        for target, res in results.items():
            matrix[(source, target)] = res
    return matrix


def channel_compensation_stats(
    cfg: LabConfig,
    seed: int,
    channel_probes: list[Probe],
    edge_actors: list[str],
    null_stats: NullStats,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    null_quantile_q: float = DEFAULT_NULL_QUANTILE,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
) -> dict[str, dict[str, CompensationStatsResult]]:
    """Per-probe, per-actor compensation results for UNTARGETED
    channel-ablation probes -- one triple per probe (not per actor),
    every ``edge_actors`` member scored from that same triple. Deliberately
    NOT the full G-28/G-29 masking-hardening apparatus
    (``classify_ablation_compensators``'s ripple-vs-intrinsic split for
    actors OUTSIDE the candidate edge) -- this first pass only asks
    "does either edge member compensate", the question this module was
    built to answer; extending it to non-edge actors is future work if a
    scenario with more actors needs it (see FINDINGS.md G-33)."""
    return {
        probe.probe_id: probe_compensation_stats(
            cfg, seed, probe, edge_actors, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            null_quantile_q=null_quantile_q, min_effect_vs_twin=min_effect_vs_twin,
        )
        for probe in channel_probes
    }


def units_from_compensation_stats(
    edges: list[tuple[str, str]],
    matrix: dict[tuple[str, str], CompensationStatsResult],
    channel_results: dict[str, dict[str, CompensationStatsResult]] | None = None,
) -> dict[str, tuple[str, ...]]:
    """Same union-find merge semantics as S6's
    ``uad_intervention.units_from_compensation_matrix`` /
    ``_merge_channel_ablation_units`` (mutual compensation, or an XOR on
    a single untargeted channel probe, unions the pair) -- reimplemented
    against ``CompensationStatsResult.compensates`` rather than a float
    threshold, not imported (Freeze-note-2 boundary, see module
    docstring)."""
    parent: dict[str, str] = {}
    actors = sorted({a for e in edges for a in e})

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a, b in edges:
        rab = matrix.get((a, b))
        rba = matrix.get((b, a))
        comp_ab = rab.compensates if rab else False
        comp_ba = rba.compensates if rba else False
        if comp_ab and comp_ba:
            union(a, b)
        elif comp_ab != comp_ba:
            union(a, b)

    if channel_results:
        edge_set = {tuple(sorted(e)) for e in edges}
        for results in channel_results.values():
            compensators = {a for a, r in results.items() if r.compensates}
            for a, b in edge_set:
                if a in compensators and b in compensators:
                    union(a, b)
                elif (a in compensators) ^ (b in compensators):
                    union(a, b)

    for a in actors:
        parent.setdefault(a, a)
    groups: dict[str, list[str]] = {}
    for a in actors:
        groups.setdefault(find(a), []).append(a)
    return {min(members): tuple(sorted(members)) for members in groups.values()}


def discovered_units_intervention_stats(
    result,
    cfg: LabConfig,
    seed: int,
    *,
    depth: str = "shallow",
    backend=None,
    agent_overrides: dict | None = None,
    probes: list[Probe] | None = None,
    k_clean_replicates: int = DEFAULT_K_CLEAN_REPLICATES,
    null_quantile_q: float = DEFAULT_NULL_QUANTILE,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    intervention_tick: int = DEFAULT_INTERVENTION_TICK,
    trace_depth: str = "deep",
    diagnostics: dict | None = None,
) -> dict[str, tuple[str, ...]]:
    """Main entry point -- same return shape and same candidate-edge
    seeding (``uad_intervention.candidate_edges_for_intervention``,
    imported not modified) as S6's ``discovered_units_intervention``.
    The null is calibrated ONCE per scenario (``k_clean_replicates``
    episodes total, shared across every probe below) rather than once
    per probe -- for an LLM backend, live-API cost is
    ``k_clean_replicates`` (shared null) + one intervened episode per
    probe (twin runs never call the LLM), not
    ``k_clean_replicates * probe_count``.

    If ``diagnostics`` is passed a dict, it is populated with the raw
    null samples, matrix results, and channel-probe results (every
    ``CompensationStatsResult`` as a plain dict) for audit -- this is a
    first-pass, pre-registered-not-frozen detector (see module
    docstring); showing the raw numbers matters more here than for S6."""
    backend = backend or MockIsolate()
    actor_ids = sorted(result.host.roles)
    edges = candidate_edges_for_intervention(result, depth=depth)
    if not edges:
        return {a: (a,) for a in actor_ids}

    edge_actors = sorted({a for e in edges for a in e})
    if probes is None:
        probes = all_default_probes(cfg, actor_ids, intervention_tick=intervention_tick)
    actor_probes = [p for p in probes if p.kind != "channel_ablation"]
    channel_probes = [p for p in probes if p.kind == "channel_ablation"]

    null_stats = calibrate_clean_null(
        cfg, seed, edge_actors, backend=backend, agent_overrides=agent_overrides,
        k_replicates=k_clean_replicates, horizon=cfg.T, depth=trace_depth,
    )
    matrix = compensation_matrix_stats(
        cfg, seed, edges, actor_probes, null_stats,
        backend=backend, agent_overrides=agent_overrides,
        null_quantile_q=null_quantile_q, min_effect_vs_twin=min_effect_vs_twin,
    )
    channel_results = (
        channel_compensation_stats(
            cfg, seed, channel_probes, edge_actors, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            null_quantile_q=null_quantile_q, min_effect_vs_twin=min_effect_vs_twin,
        )
        if channel_probes
        else {}
    )

    if diagnostics is not None:
        diagnostics["null_samples"] = {
            a: {
                "at_tick_0": null_stats.samples_at(a, 0),
                "at_intervention_tick": null_stats.samples_at(a, intervention_tick),
            }
            for a in edge_actors
        }
        diagnostics["matrix"] = {f"{s}->{t}": r.to_dict() for (s, t), r in matrix.items()}
        diagnostics["channel"] = {
            probe_id: {a: r.to_dict() for a, r in results.items()} for probe_id, results in channel_results.items()
        }

    parent_partition = units_from_compensation_stats(edges, matrix, channel_results)
    covered = {m for members in parent_partition.values() for m in members}
    for a in actor_ids:
        if a not in covered:
            parent_partition[a] = (a,)
    return parent_partition
