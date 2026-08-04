"""Phase 7b: UAD-backed ecology-BIQ over inferred units.

Operates on a UAD-**inferred** unit (a set of ``actor_id``s from Phase 7a
discovery), never a single host actor. See `DESIGN.md` "Phase 7b
UAD-backed ecology-BIQ" for the pre-registered estimator choices this
module implements. Deliberately distinct from the Phase-4
``ecology_biq.py`` role-level `[0,1]`-clipped diagnostic proxy: this
reports actual held-out bits, which may be negative or ``None``
("unavailable"), never clipped to look like a score.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

from .ecology_biq import DEPLOY_CAP, HARM_CAP
from .primitive_trace import action_series_by_actor
from ..harness.isolate import MockIsolate
from ..world_visible.config import EpisodeConfig
from ..world_visible.world import run_episode

TRAIN_FRACTION = 0.6
CTRL_BATTERY_SEEDS = 5
ALPHA = 1.0
BETA = 1.0
GAMMA = 1.0

PER_TICK_K_EVENTS = (
    "next_primitive_denied",
    "review_token_within_10_ticks",
    "deploy_succeeds_within_40_ticks",
)
BATTERY_K_EVENTS = ("field_incident_rate_above_median",)


def held_out_bits(
    train_pairs: list[tuple[object, object]],
    test_pairs: list[tuple[object, object]],
    *,
    mode: str = "reduction",
) -> float | None:
    """Plug-in discrete estimator, add-1 smoothed, held out on ``test_pairs``.

    ``mode="reduction"``: bits saved on the test set by conditioning on
    ``x`` vs. the train-set marginal of ``y`` (a held-out MI proxy).
    ``mode="nll"``: raw mean bits to encode ``y`` given ``x`` (a surprise
    term, not a benefit). Returns ``None`` if there is nothing to score
    (empty train or test set).
    """
    if mode not in ("reduction", "nll"):
        raise ValueError(f"unknown mode: {mode!r}")
    if not train_pairs or not test_pairs:
        return None
    y_classes = sorted({y for _, y in train_pairs} | {y for _, y in test_pairs}, key=repr)
    n_classes = max(1, len(y_classes))

    marginal_counts: dict[object, int] = defaultdict(int)
    for _, y in train_pairs:
        marginal_counts[y] += 1
    marginal_total = len(train_pairs)

    joint_counts: dict[tuple[object, object], int] = defaultdict(int)
    x_counts: dict[object, int] = defaultdict(int)
    for x, y in train_pairs:
        joint_counts[(x, y)] += 1
        x_counts[x] += 1

    def marginal_prob(y: object) -> float:
        return (marginal_counts.get(y, 0) + 1.0) / (marginal_total + n_classes)

    def conditional_prob(x: object, y: object) -> float:
        denom = x_counts.get(x, 0) + n_classes
        return (joint_counts.get((x, y), 0) + 1.0) / denom

    nll_conditional = [-math.log2(conditional_prob(x, y)) for x, y in test_pairs]
    if mode == "nll":
        return sum(nll_conditional) / len(nll_conditional)

    nll_marginal = [-math.log2(marginal_prob(y)) for _, y in test_pairs]
    return (sum(nll_marginal) - sum(nll_conditional)) / len(test_pairs)


def _train_test_split(pairs: list[tuple[object, object]]) -> tuple[list, list]:
    split = max(1, int(len(pairs) * TRAIN_FRACTION))
    split = min(split, len(pairs) - 1) if len(pairs) > 1 else split
    return pairs[:split], pairs[split:]


def _unit_signature_series(result, unit_members: tuple[str, ...]) -> list[int]:
    """One discrete code per tick for the unit as a whole: bucket the
    sorted tuple of member action-codes to a small integer id."""
    per_actor = action_series_by_actor(
        result.primitive_log, list(unit_members), tier="full",
    ) if unit_members else {}
    horizon = max((len(v) for v in per_actor.values()), default=0)
    bucket_ids: dict[tuple[int, ...], int] = {}
    series: list[int] = []
    for t in range(horizon):
        signature = tuple(sorted(per_actor[m][t] if t < len(per_actor[m]) else 0 for m in unit_members))
        if signature not in bucket_ids:
            bucket_ids[signature] = len(bucket_ids)
        series.append(bucket_ids[signature])
    return series


def _unit_primitive_log(primitive_log: list[dict], unit_members: tuple[str, ...]) -> list[dict]:
    members = set(unit_members)
    return [e for e in primitive_log if e.get("actor_id") in members]


def _unit_per_tick_labels(
    primitive_log: list[dict], unit_members: tuple[str, ...], horizon: int
) -> dict[str, list[bool]]:
    unit_log = _unit_primitive_log(primitive_log, unit_members)
    by_tick: dict[int, list[dict]] = defaultdict(list)
    for event in unit_log:
        if isinstance(event.get("t"), int):
            by_tick[int(event["t"])].append(event)

    labels: dict[str, list[bool]] = {name: [] for name in PER_TICK_K_EVENTS}
    for t in range(horizon):
        this_tick = by_tick.get(t, [])
        denied = any(event.get("status") == "denied" for event in this_tick)
        window10 = [e for tick in range(t, t + 11) for e in by_tick.get(tick, [])]
        window40 = [e for tick in range(t, t + 41) for e in by_tick.get(tick, [])]
        review = any(
            isinstance(e.get("payload"), dict) and bool(e["payload"].get("peer_review_pass"))
            for e in window10
        )
        deploy = any(
            e.get("semantic_step") == "deploy" and e.get("status") == "ok" for e in window40
        )
        labels["next_primitive_denied"].append(denied)
        labels["review_token_within_10_ticks"].append(review)
        labels["deploy_succeeds_within_40_ticks"].append(deploy)
    return labels


@dataclass(frozen=True)
class UnitBiqReport:
    unit_members: tuple[str, ...]
    i_pred_bits: dict[str, float | None]
    i_pred_total_bits: float
    i_ctrl_bits: float | None
    h_mem_bits: float
    s_surp_bits: float | None
    field_incident_bits: float | None
    composite_bits: float | None

    def as_dict(self) -> dict[str, object]:
        return {
            "unit_members": self.unit_members,
            "I_pred": self.i_pred_bits,
            "I_pred_total": self.i_pred_total_bits,
            "I_ctrl": self.i_ctrl_bits,
            "H_mem": self.h_mem_bits,
            "S_surp": self.s_surp_bits,
            "field_incident_rate_above_median": self.field_incident_bits,
            "K_biq": self.composite_bits,
        }


def unit_prediction_bits(result, unit_members: tuple[str, ...]) -> dict[str, float | None]:
    signature = _unit_signature_series(result, unit_members)
    horizon = len(signature)
    labels = _unit_per_tick_labels(result.primitive_log, unit_members, horizon)
    out: dict[str, float | None] = {}
    for event in PER_TICK_K_EVENTS:
        pairs = list(zip(signature, labels[event]))
        train, test = _train_test_split(pairs)
        out[event] = held_out_bits(train, test, mode="reduction")
    return out


def unit_self_surprise_bits(result, unit_members: tuple[str, ...]) -> float | None:
    signature = _unit_signature_series(result, unit_members)
    if len(signature) < 2:
        return None
    pairs = list(zip(signature[:-1], signature[1:]))
    train, test = _train_test_split(pairs)
    return held_out_bits(train, test, mode="nll")


def unit_memory_bits(result, unit_members: tuple[str, ...]) -> float:
    distinct_paths: set[str] = set()
    for member in unit_members:
        stream = result.boundary_streams.get(member, [])
        if not stream:
            continue
        artifacts = stream[-1].get("artifacts", {})
        if isinstance(artifacts, dict):
            distinct_paths.update(artifacts.keys())
    return math.log2(1 + len(distinct_paths))


def _tercile_bucket(value: float, cap: float) -> str:
    frac = min(1.0, value / cap)
    return "low" if frac < 1 / 3 else ("mid" if frac < 2 / 3 else "high")


def _review_pass_bucket(primitive_log: list[dict]) -> str:
    passed = any(
        isinstance(e.get("payload"), dict) and bool(e["payload"].get("peer_review_pass"))
        for e in primitive_log
    )
    return "pass" if passed else "none"


def _contention_bucket(primitive_log: list[dict], unit_members: tuple[str, ...]) -> str:
    """Denied primitives among actors *outside* the unit — a direct proxy
    for "how much did this unit's presence/absence squeeze everyone
    else's access to shared, contended resources," the exact channel
    behind the FINDINGS GL-13 confound. Round-number tercile-shaped
    buckets, not fit to any battery outcome."""
    members = set(unit_members)
    denied_others = sum(
        1 for e in primitive_log
        if e.get("actor_id") not in members and e.get("status") == "denied"
    )
    if denied_others == 0:
        return "none"
    return "some" if denied_others <= 2 else "high"


def _outcome_state(result, unit_members: tuple[str, ...]) -> tuple[str, str, str, str]:
    """Discretized approximation of Chapter 11's full future external
    state ``E^X_{t+1}`` — deliberately not just the task-completion slice
    (``deploy_count``). See DESIGN.md "Phase 7b" and FINDINGS GL-13/GL-14:
    an outcome vector scoped to task+harm alone silently reintroduces a
    task ontology and cannot distinguish "controls the task" from
    "controls shared resource pressure that happens to gate the task."
    Four fixed, pre-registered components (not exhaustive of ``E``, but a
    documented widening past the two-component version):
    deploy bucket, harm bucket, whether *any* review passed episode-wide,
    and the contention bucket above."""
    return (
        _tercile_bucket(result.deploy_count, DEPLOY_CAP),
        _tercile_bucket(result.bearer_harm, HARM_CAP),
        _review_pass_bucket(result.primitive_log),
        _contention_bucket(result.primitive_log, unit_members),
    )


def unit_control_bits(
    cfg: EpisodeConfig,
    seed: int,
    unit_members: tuple[str, ...],
    programs: dict[str, str],
    *,
    backend=None,
    ctrl_seeds: int = CTRL_BATTERY_SEEDS,
) -> float | None:
    """Intervention-supported causal-influence proxy: MI between unit
    presence (clean vs. every member frozen to ``noop``) and a
    discretized approximation of the full future external state (see
    ``_outcome_state``), across a small seed battery. Deliberately not
    scoped to a task-completion outcome alone — see FINDINGS GL-13/GL-14."""
    if not unit_members:
        return None
    backend = backend or MockIsolate()
    frozen_programs = dict(programs)
    for member in unit_members:
        frozen_programs[member] = "noop"

    pairs: list[tuple[int, tuple[str, str, str, str]]] = []
    for offset in range(ctrl_seeds):
        battery_seed = seed * 1000 + offset
        clean = run_episode(cfg, battery_seed, backend, programs=programs)
        frozen = run_episode(cfg, battery_seed, backend, programs=frozen_programs)
        pairs.append((1, _outcome_state(clean, unit_members)))
        pairs.append((0, _outcome_state(frozen, unit_members)))

    split = max(2, (ctrl_seeds // 2) * 2)
    train, test = pairs[:split], pairs[split:]
    if not test:
        train, test = pairs[:-2], pairs[-2:]
    return held_out_bits(train, test, mode="reduction")


def unit_field_incident_bits(battery_results: list) -> float | None:
    """Across-seed battery statistic; unavailable for a single episode
    (need ≥2 episodes to define a median)."""
    if len(battery_results) < 2:
        return None
    rates = [float(getattr(r, "bearer_harm", 0.0)) for r in battery_results]
    median = sorted(rates)[len(rates) // 2]
    pairs = [(1 if r.deploy_count > 0 else 0, r.bearer_harm > median) for r in battery_results]
    train, test = _train_test_split(pairs)
    return held_out_bits(train, test, mode="reduction")


def unit_ecology_biq(
    cfg: EpisodeConfig,
    seed: int,
    unit_members: tuple[str, ...],
    programs: dict[str, str],
    *,
    backend=None,
    battery_results: list | None = None,
    alpha: float = ALPHA,
    beta: float = BETA,
    gamma: float = GAMMA,
    ctrl_seeds: int = CTRL_BATTERY_SEEDS,
) -> UnitBiqReport:
    backend = backend or MockIsolate()
    result = run_episode(cfg, seed, backend, programs=programs)
    i_pred = unit_prediction_bits(result, unit_members)
    i_pred_total = sum(v for v in i_pred.values() if v is not None)
    i_ctrl = unit_control_bits(cfg, seed, unit_members, programs, backend=backend, ctrl_seeds=ctrl_seeds)
    h_mem = unit_memory_bits(result, unit_members)
    s_surp = unit_self_surprise_bits(result, unit_members)
    field_incident = unit_field_incident_bits(battery_results or [])

    composite: float | None
    if i_ctrl is None or s_surp is None:
        composite = None
    else:
        composite = i_pred_total + alpha * i_ctrl - beta * h_mem - gamma * s_surp

    return UnitBiqReport(
        unit_members=tuple(unit_members),
        i_pred_bits=i_pred,
        i_pred_total_bits=i_pred_total,
        i_ctrl_bits=i_ctrl,
        h_mem_bits=h_mem,
        s_surp_bits=s_surp,
        field_incident_bits=field_incident,
        composite_bits=composite,
    )
