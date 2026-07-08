"""Symmetric two-sample S6 (PLAN.md post-release Step 2, 2026-07-08;
DESIGN.md "Freeze note 3").

Replaces the asymmetric ``NullStats`` design (1 intervened draw vs a
quantile of ``k`` clean pairwise divergences) with a symmetric test:
``m`` intervened and ``k`` clean replicate episodes per probe, scored
by whether intervened-vs-pooled-clean divergences are stochastically
greater than clean pairwise divergences (exact permutation test,
stdlib only). Multiple probes per scenario use Holm correction.

**Why a new design, not another edit to the asymmetric variant (G-33).**
G-34 showed post-hoc retuning on burned seeds; the single-draw decision
and uncorrected 0.90-quantile probes were the structural failures.

**Freeze note 3 defaults (registered before fresh-seed LLM runs):**
``DEFAULT_M_INTERVENED=4``, ``DEFAULT_K_CLEAN=4``, ``DEFAULT_ALPHA=0.05``,
``DEFAULT_MIN_EFFECT_VS_TWIN=0.05``. Fresh evaluation seeds for real-LLM
stress tests must NOT reuse 20002--20010 (G-32 through G-34).

**Scripted-backend equivalence.** On ``MockIsolate``/``SubprocessIsolate``
with deterministic agents, same-seed replicates are byte-identical: the
clean pairwise null collapses to all zeros; any nonzero intervened
divergence yields a significant permutation test -- recovering frozen S6's
"any nonzero divergence is signal" regime exactly
(``test_intervention_stats.py``).

Does not modify ``uad_intervention.py`` / Freeze note 2 modules.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, replace
from itertools import combinations

from ..harness.isolate import MockIsolate
from ..world_visible.config import LabConfig
from ..world_visible.world import run_episode
from .intervention_diff import action_series_from_result
from .intervention_probes import Probe, all_default_probes, default_probe_for_actor
from .uad_intervention import candidate_edges_for_intervention

DEFAULT_M_INTERVENED = 4
DEFAULT_K_CLEAN = 4
DEFAULT_ALPHA = 0.05
DEFAULT_MIN_EFFECT_VS_TWIN = 0.05
DEFAULT_INTERVENTION_TICK = 8

# Backward-compatible aliases for run scripts written against G-33 API.
DEFAULT_K_CLEAN_REPLICATES = DEFAULT_K_CLEAN
DEFAULT_NULL_QUANTILE = 0.90  # deprecated; ignored by symmetric test

# Action-code vocabulary (mirrors ``attic/uad_mi.py`` literals).
_PIPELINE_CODES = frozenset(range(1, 11))
_ACCESS_REQUEST_CODE = 11
_BOARD_CODES = frozenset({13, 14})
_DM_CODES = frozenset({15, 16})
_FILE_CODES = frozenset({17, 18, 19})


def relevant_codes_for_probe(probe: Probe) -> frozenset[int] | None:
    """Per-probe histogram filter: codes plausibly downstream of the
    ablated channel. ``None`` = use the full vocabulary."""
    if probe.kind != "channel_ablation":
        return None
    all_used = _PIPELINE_CODES | {11, 12} | _BOARD_CODES | _DM_CODES | _FILE_CODES | {0}
    if probe.channel == "dm":
        return frozenset(all_used - _DM_CODES)
    if probe.channel == "board":
        return frozenset(all_used - _BOARD_CODES)
    if probe.channel == "file":
        return frozenset(all_used - _FILE_CODES)
    return None


def code_histogram(
    series: list[int],
    from_tick: int,
    *,
    allowed_codes: frozenset[int] | None = None,
) -> dict[int, float]:
    window = [c for c in series[from_tick:] if allowed_codes is None or c in allowed_codes]
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


def outcome_divergence(
    series_a: list[int],
    series_b: list[int],
    *,
    from_tick: int,
    allowed_codes: frozenset[int] | None = None,
) -> float:
    return total_variation_distance(
        code_histogram(series_a, from_tick, allowed_codes=allowed_codes),
        code_histogram(series_b, from_tick, allowed_codes=allowed_codes),
    )


def divergence_from_pooled(
    series: list[int],
    pooled: dict[int, float],
    *,
    from_tick: int,
    allowed_codes: frozenset[int] | None = None,
) -> float:
    return total_variation_distance(code_histogram(series, from_tick, allowed_codes=allowed_codes), pooled)


def pooled_histogram(
    replicate_series: tuple[dict[str, list[int]], ...],
    actor_id: str,
    from_tick: int,
    *,
    allowed_codes: frozenset[int] | None = None,
) -> dict[int, float]:
    hists = [
        code_histogram(rep.get(actor_id, []), from_tick, allowed_codes=allowed_codes)
        for rep in replicate_series
    ]
    if not hists:
        return {}
    codes = set()
    for h in hists:
        codes.update(h)
    n = len(hists)
    return {c: sum(h.get(c, 0.0) for h in hists) / n for c in codes}


def permutation_pvalue_greater(group_a: list[float], group_b: list[float]) -> float:
    """One-sided exact permutation: is ``group_a`` stochastically greater
    than ``group_b`` (difference in means)? Degenerate all-tied case
    returns 1.0."""
    if not group_a or not group_b:
        return 1.0
    observed = statistics.mean(group_a) - statistics.mean(group_b)
    combined = list(group_a) + list(group_b)
    n_a = len(group_a)
    total = math.comb(len(combined), n_a)
    if total == 0:
        return 1.0
    extreme = 0
    for indices in combinations(range(len(combined)), n_a):
        a = [combined[i] for i in indices]
        b = [combined[i] for i in range(len(combined)) if i not in indices]
        if statistics.mean(a) - statistics.mean(b) >= observed - 1e-15:
            extreme += 1
    return extreme / total


def score_intervention_vs_null(
    intervened_samples: list[float],
    clean_samples: list[float],
    *,
    alpha: float = DEFAULT_ALPHA,
) -> tuple[float, bool]:
    """Return ``(p_value, exceeds_null)``. On a zero-width clean null (all
    pairwise divergences exactly 0 -- the deterministic scripted regime),
    degenerates to S6's rule: any positive intervened divergence is signal."""
    if not clean_samples:
        clean_samples = [0.0]
    if max(clean_samples) == 0.0 and min(clean_samples) == 0.0:
        mean_intervened = statistics.mean(intervened_samples) if intervened_samples else 0.0
        exceeds = mean_intervened > 0.0
        return (0.0 if exceeds else 1.0, exceeds)
    p_value = permutation_pvalue_greater(intervened_samples, clean_samples)
    return (p_value, p_value < alpha)


def holm_adjusted(p_values: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (same length as input)."""
    m = len(p_values)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [1.0] * m
    prev = 0.0
    for rank in range(m):
        i = order[rank]
        raw = min(1.0, p_values[i] * (m - rank))
        prev = max(prev, raw)
        adjusted[i] = prev
    return adjusted


@dataclass(frozen=True)
class CleanReplicateBank:
    """``k`` independent clean (no-probe) replicate traces."""

    replicate_series: tuple[dict[str, list[int]], ...]

    def clean_pairwise_divergences(
        self, actor_id: str, from_tick: int, *, allowed_codes: frozenset[int] | None = None
    ) -> list[float]:
        out: list[float] = []
        reps = self.replicate_series
        for i in range(len(reps)):
            for j in range(i + 1, len(reps)):
                a = reps[i].get(actor_id, [])
                b = reps[j].get(actor_id, [])
                out.append(outcome_divergence(a, b, from_tick=from_tick, allowed_codes=allowed_codes))
        return out

    def pooled_histogram_for(
        self, actor_id: str, from_tick: int, *, allowed_codes: frozenset[int] | None = None
    ) -> dict[int, float]:
        return pooled_histogram(self.replicate_series, actor_id, from_tick, allowed_codes=allowed_codes)


# Backward-compatible alias for tests/run scripts.
NullStats = CleanReplicateBank


def calibrate_clean_null(
    cfg: LabConfig,
    seed: int,
    actor_ids: list[str],
    *,
    backend=None,
    agent_overrides: dict | None = None,
    k_replicates: int = DEFAULT_K_CLEAN,
    k_clean_replicates: int | None = None,
    horizon: int | None = None,
    depth: str = "deep",
) -> CleanReplicateBank:
    if k_clean_replicates is not None:
        k_replicates = k_clean_replicates
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
    return CleanReplicateBank(replicate_series=tuple(series))


@dataclass(frozen=True)
class CompensationStatsResult:
    actor_id: str
    divergence_from_clean: float
    divergence_from_twin: float
    p_value: float
    p_value_adjusted: float | None
    exceeds_null: bool
    clears_twin_floor: bool
    clean_null_samples: tuple[float, ...]
    intervened_samples: tuple[float, ...]

    @property
    def null_threshold(self) -> float:
        """Deprecated G-33 field; retained for diagnostic scripts."""
        if not self.clean_null_samples:
            return 0.0
        return max(self.clean_null_samples)

    @property
    def compensates(self) -> bool:
        return self.exceeds_null and self.clears_twin_floor

    def to_dict(self) -> dict:
        return {
            "actor_id": self.actor_id,
            "divergence_from_clean": self.divergence_from_clean,
            "divergence_from_twin": self.divergence_from_twin,
            "p_value": self.p_value,
            "p_value_adjusted": self.p_value_adjusted,
            "null_threshold": self.null_threshold,
            "exceeds_null": self.exceeds_null,
            "clears_twin_floor": self.clears_twin_floor,
            "compensates": self.compensates,
            "clean_null_samples": list(self.clean_null_samples),
            "intervened_samples": list(self.intervened_samples),
        }

    def with_holm(self, p_adj: float, *, alpha: float) -> CompensationStatsResult:
        return replace(self, p_value_adjusted=p_adj, exceeds_null=p_adj < alpha)


def _run_intervened_series(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    responders: list[str],
    *,
    backend,
    agent_overrides: dict | None,
    m_replicates: int,
    probe_kwargs,
    horizon: int,
    depth: str,
) -> list[dict[str, list[int]]]:
    out: list[dict[str, list[int]]] = []
    for _ in range(m_replicates):
        result = run_episode(
            cfg, seed=seed, backend=backend, agent_overrides=agent_overrides or None, **probe_kwargs
        )
        try:
            out.append(action_series_from_result(result, responders, horizon=horizon, depth=depth))
        finally:
            result.cleanup()
    return out


def probe_compensation_stats(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    responders: list[str],
    null_stats: CleanReplicateBank,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    m_intervened: int = DEFAULT_M_INTERVENED,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    alpha: float = DEFAULT_ALPHA,
    horizon: int | None = None,
    depth: str = "deep",
    null_quantile_q: float | None = None,  # deprecated, ignored
    k_clean_replicates: int | None = None,  # deprecated alias, ignored here
) -> dict[str, CompensationStatsResult]:
    del null_quantile_q, k_clean_replicates
    backend = backend or MockIsolate()
    horizon = horizon if horizon is not None else cfg.T
    from_tick = probe.intervention_tick
    allowed = relevant_codes_for_probe(probe)
    probe_cfg, probe_kwargs = probe.apply(cfg)

    intervened_series_list = _run_intervened_series(
        probe_cfg, seed, probe, responders, backend=backend,
        agent_overrides=agent_overrides, m_replicates=m_intervened,
        probe_kwargs=probe_kwargs, horizon=horizon, depth=depth,
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
        twin_series = action_series_from_result(twin, responders, horizon=horizon, depth=depth)
        out: dict[str, CompensationStatsResult] = {}
        for r in responders:
            clean_samples = null_stats.clean_pairwise_divergences(r, from_tick, allowed_codes=allowed)
            pooled = null_stats.pooled_histogram_for(r, from_tick, allowed_codes=allowed)
            intervened_samples = [
                divergence_from_pooled(s[r], pooled, from_tick=from_tick, allowed_codes=allowed)
                for s in intervened_series_list
            ]
            p_value, exceeds = score_intervention_vs_null(
                intervened_samples, clean_samples, alpha=alpha
            )
            mean_intervened = statistics.mean(intervened_samples) if intervened_samples else 0.0
            div_twin = outcome_divergence(
                intervened_series_list[0][r], twin_series[r], from_tick=from_tick, allowed_codes=allowed
            )
            out[r] = CompensationStatsResult(
                actor_id=r,
                divergence_from_clean=mean_intervened,
                divergence_from_twin=div_twin,
                p_value=p_value,
                p_value_adjusted=None,
                exceeds_null=exceeds,
                clears_twin_floor=div_twin >= min_effect_vs_twin,
                clean_null_samples=tuple(clean_samples),
                intervened_samples=tuple(intervened_samples),
            )
        return out
    finally:
        twin.cleanup()


def directed_compensation_stats(
    cfg: LabConfig, seed: int, probe: Probe, responder: str, null_stats: CleanReplicateBank, **kwargs
) -> CompensationStatsResult:
    return probe_compensation_stats(cfg, seed, probe, [responder], null_stats, **kwargs)[responder]


def _apply_holm_to_results(results: dict[str, CompensationStatsResult], *, alpha: float) -> dict[str, CompensationStatsResult]:
    keys = list(results.keys())
    pvals = [results[k].p_value for k in keys]
    adj = holm_adjusted(pvals)
    return {k: results[k].with_holm(adj[i], alpha=alpha) for i, k in enumerate(keys)}


def _probe_for_actor(probes: list[Probe], actor_id: str) -> Probe | None:
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
    null_stats: CleanReplicateBank,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    m_intervened: int = DEFAULT_M_INTERVENED,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    alpha: float = DEFAULT_ALPHA,
    apply_holm: bool = False,
    **kwargs,
) -> dict[tuple[str, str], CompensationStatsResult]:
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
            m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
            **kwargs,
        )
        if apply_holm:
            results = _apply_holm_to_results(results, alpha=alpha)
        for target, res in results.items():
            matrix[(source, target)] = res
    return matrix


def channel_compensation_stats(
    cfg: LabConfig,
    seed: int,
    channel_probes: list[Probe],
    actors: list[str],
    null_stats: CleanReplicateBank,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    m_intervened: int = DEFAULT_M_INTERVENED,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    alpha: float = DEFAULT_ALPHA,
    apply_holm: bool = False,
    horizon: int | None = None,
    depth: str = "deep",
    **kwargs,
) -> dict[str, dict[str, CompensationStatsResult]]:
    out: dict[str, dict[str, CompensationStatsResult]] = {}
    for probe in channel_probes:
        results = probe_compensation_stats(
            cfg, seed, probe, actors, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
            horizon=horizon, depth=depth, **kwargs,
        )
        if apply_holm:
            results = _apply_holm_to_results(results, alpha=alpha)
        out[probe.probe_id] = results
    return out


def _playbook_actor_ids(cfg: LabConfig) -> list[str]:
    return sorted(a.actor_id for a in cfg.agents if a.role not in ("admin", "overseer"))


def _masked_compensation_stats(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    actor: str,
    mask_actors: list[str],
    null_stats: CleanReplicateBank,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    m_intervened: int = DEFAULT_M_INTERVENED,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    alpha: float = DEFAULT_ALPHA,
    **kwargs,
) -> CompensationStatsResult:
    overrides = dict(agent_overrides or {})
    for m in mask_actors:
        overrides[m] = (backend, "honest_twin")
    return probe_compensation_stats(
        cfg, seed, probe, [actor], null_stats,
        backend=backend, agent_overrides=overrides,
        m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
        **kwargs,
    )[actor]


def classify_ablation_compensators_stats(
    cfg: LabConfig,
    seed: int,
    probe: Probe,
    edges: list[tuple[str, str]],
    null_stats: CleanReplicateBank,
    *,
    backend=None,
    agent_overrides: dict | None = None,
    m_intervened: int = DEFAULT_M_INTERVENED,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    alpha: float = DEFAULT_ALPHA,
    **kwargs,
) -> dict[str, str]:
    edge_actors = {a for e in edges for a in e}
    playbook = _playbook_actor_ids(cfg)
    results = probe_compensation_stats(
        cfg, seed, probe, playbook, null_stats,
        backend=backend, agent_overrides=agent_overrides,
        m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
        **kwargs,
    )
    results = _apply_holm_to_results(results, alpha=alpha)
    compensators = {a for a in playbook if results[a].compensates}
    established = sorted(compensators & edge_actors)
    labels = {a: "established" for a in established}
    outside_reactors = {a for a in playbook if a not in edge_actors and results[a].exceeds_null}
    for a in sorted(outside_reactors):
        masked = _masked_compensation_stats(
            cfg, seed, probe, a, established, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
            **kwargs,
        )
        masked = _apply_holm_to_results({a: masked}, alpha=alpha)[a]
        labels[a] = "intrinsic_unexplained" if masked.compensates else "ripple"
    return labels


def _merge_channel_ablation_units_stats(
    channel_probes: list[Probe],
    edges: list[tuple[str, str]],
    parent: dict[str, str],
    ablation_labels: dict[str, dict[str, str]],
) -> None:
    edge_set = {tuple(sorted(e)) for e in edges}

    def union(x: str, y: str) -> None:
        parent.setdefault(x, x)
        parent.setdefault(y, y)
        while parent[x] != x:
            x = parent[x]
        while parent[y] != y:
            y = parent[y]
        if x != y:
            parent[x] = y

    for probe in channel_probes:
        if probe.kind != "channel_ablation":
            continue
        compensators = set(ablation_labels.get(probe.probe_id, {}))
        for a, b in edge_set:
            if a in compensators and b in compensators:
                union(a, b)
            elif (a in compensators) ^ (b in compensators):
                union(a, b)


def units_from_compensation_stats(
    edges: list[tuple[str, str]],
    matrix: dict[tuple[str, str], CompensationStatsResult],
    channel_results: dict[str, dict[str, CompensationStatsResult]] | None = None,
    *,
    channel_probes: list[Probe] | None = None,
    ablation_labels: dict[str, dict[str, str]] | None = None,
) -> dict[str, tuple[str, ...]]:
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

    if ablation_labels is not None and channel_probes is not None:
        _merge_channel_ablation_units_stats(channel_probes, edges, parent, ablation_labels)
    elif channel_results:
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


def _holm_across_probe_results(
    matrix: dict[tuple[str, str], CompensationStatsResult],
    channel_results: dict[str, dict[str, CompensationStatsResult]],
    *,
    alpha: float,
) -> tuple[dict[tuple[str, str], CompensationStatsResult], dict[str, dict[str, CompensationStatsResult]]]:
    """Apply one Holm correction across all matrix + channel probe scores."""
    indexed: list[tuple[str, tuple[str, str] | tuple[str, str, str]]] = []
    for key, res in matrix.items():
        indexed.append(("matrix", key))
    for probe_id, per_actor in channel_results.items():
        for actor_id in per_actor:
            indexed.append(("channel", (probe_id, actor_id)))
    if not indexed:
        return matrix, channel_results

    pvals = []
    for kind, key in indexed:
        if kind == "matrix":
            pvals.append(matrix[key].p_value)
        else:
            pvals.append(channel_results[key[0]][key[1]].p_value)
    adj = holm_adjusted(pvals)

    new_matrix = dict(matrix)
    new_channel: dict[str, dict[str, CompensationStatsResult]] = {
        pid: dict(per) for pid, per in channel_results.items()
    }
    for i, (kind, key) in enumerate(indexed):
        if kind == "matrix":
            new_matrix[key] = matrix[key].with_holm(adj[i], alpha=alpha)
        else:
            pid, aid = key
            new_channel[pid][aid] = channel_results[pid][aid].with_holm(adj[i], alpha=alpha)
    return new_matrix, new_channel


def discovered_units_intervention_stats(
    result,
    cfg: LabConfig,
    seed: int,
    *,
    depth: str = "shallow",
    backend=None,
    agent_overrides: dict | None = None,
    probes: list[Probe] | None = None,
    k_clean: int = DEFAULT_K_CLEAN,
    m_intervened: int = DEFAULT_M_INTERVENED,
    k_clean_replicates: int | None = None,
    min_effect_vs_twin: float = DEFAULT_MIN_EFFECT_VS_TWIN,
    alpha: float = DEFAULT_ALPHA,
    intervention_tick: int = DEFAULT_INTERVENTION_TICK,
    trace_depth: str = "deep",
    null_quantile_q: float | None = None,  # deprecated
    diagnostics: dict | None = None,
) -> dict[str, tuple[str, ...]]:
    if k_clean_replicates is not None:
        k_clean = k_clean_replicates
    del null_quantile_q
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
        k_replicates=k_clean, horizon=cfg.T, depth=trace_depth,
    )
    matrix = compensation_matrix_stats(
        cfg, seed, edges, actor_probes, null_stats,
        backend=backend, agent_overrides=agent_overrides,
        m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
    )
    playbook = _playbook_actor_ids(cfg)
    channel_results = (
        channel_compensation_stats(
            cfg, seed, channel_probes, playbook, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
            horizon=cfg.T, depth=trace_depth,
        )
        if channel_probes
        else {}
    )
    matrix, channel_results = _holm_across_probe_results(matrix, channel_results, alpha=alpha)

    ablation_labels = {
        probe.probe_id: classify_ablation_compensators_stats(
            cfg, seed, probe, edges, null_stats,
            backend=backend, agent_overrides=agent_overrides,
            m_intervened=m_intervened, min_effect_vs_twin=min_effect_vs_twin, alpha=alpha,
            horizon=cfg.T, depth=trace_depth,
        )
        for probe in channel_probes
    }

    if diagnostics is not None:
        diagnostics["null_samples"] = {
            a: {
                "at_tick_0": null_stats.clean_pairwise_divergences(
                    a, 0, allowed_codes=relevant_codes_for_probe(channel_probes[0]) if channel_probes else None
                ),
                "at_intervention_tick": null_stats.clean_pairwise_divergences(a, intervention_tick),
            }
            for a in edge_actors
        }
        diagnostics["matrix"] = {f"{s}->{t}": r.to_dict() for (s, t), r in matrix.items()}
        diagnostics["channel"] = {
            probe_id: {a: r.to_dict() for a, r in results.items()} for probe_id, results in channel_results.items()
        }
        diagnostics["ablation"] = ablation_labels
        diagnostics["symmetric_test"] = {
            "m_intervened": m_intervened,
            "k_clean": k_clean,
            "alpha": alpha,
            "correction": "holm",
        }

    parent_partition = units_from_compensation_stats(
        edges, matrix, channel_probes=channel_probes, ablation_labels=ablation_labels
    )
    covered = {m for members in parent_partition.values() for m in members}
    for a in actor_ids:
        if a not in covered:
            parent_partition[a] = (a,)
    return parent_partition
