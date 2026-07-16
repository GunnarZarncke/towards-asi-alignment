"""PLAN_v3 slice D — causal C2-v3 engineering gate (GL-59).

Accounting ``check_c2_v3`` only verifies compiled contribution floors.
This module ablates a *qualifying* principal's dominant compute flow and
requires measurable reference-battery divergence — same shape as the slice
A flow ablation gate, but tied to C2-v3's qualifying principals.

Engineering-only: does not replace ``check_c2_v3`` in ``ComplexityReport``.
Episodes use plain ``WEAK_AGENT`` programs **without** host
``mechanism_exercise`` profiles so the gate isolates principal-flow
effects from Part B host choreography (same discipline as slice A's
ablation gate).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from ..agent_visible.behavior_features import classify_primitive
from ..harness.ecology_complexity import (
    C2_MIN_REACHABLE_PRINCIPALS,
    C2_V3_MIN_CONTRIBUTION_FRACTION,
    V3_REFERENCE_T,
)
from ..harness.isolate import MockIsolate
from ..oracle_only.calibration import WEAK_AGENT, programs_for
from ..world_visible.config import EpisodeConfig
from ..world_visible.ecology_agents import reference_roster_from_ecology
from ..world_visible.institutional_compiler import role_principal_compute_contributions
from ..world_visible.substrate import load_substrate
from ..world_visible.world import EpisodeResult, default_lab_config, run_episode

_DEFAULT_SEEDS = (0, 2, 4)
_DEFAULT_L1 = 0.10
_DEFAULT_MIN_PASS = 2
_DEFAULT_LOAD = 1.5


@dataclass(frozen=True)
class C2V3CausalGateSpec:
    focal_role: str
    focal_actor_id: str
    ablation_flow_id: str
    seeds: tuple[int, ...]
    histogram_l1_threshold: float
    min_seeds_passing: int
    carrier_load_scale: float
    T: int


def _histogram_l1(a: Counter[str], b: Counter[str]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    total_a = sum(a.values()) or 1
    total_b = sum(b.values()) or 1
    return sum(abs(a.get(k, 0) / total_a - b.get(k, 0) / total_b) for k in keys)


def _pattern_hist(result: EpisodeResult, *, actor_id: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for entry in result.primitive_log:
        if entry.get("actor_id") != actor_id:
            continue
        prim = entry.get("primitive")
        if isinstance(prim, dict):
            counts[classify_primitive(prim)] += 1
    return counts


def pick_c2_v3_ablation_flow_id(data: dict, *, role: str) -> str | None:
    """Dominant qualifying principal's largest compute flow for ``role``."""
    by_principal = role_principal_compute_contributions(data).get(role, {})
    total = sum(by_principal.values())
    if total <= 0:
        return None
    qualifying = sorted(
        pid
        for pid, amt in by_principal.items()
        if amt / total >= C2_V3_MIN_CONTRIBUTION_FRACTION
    )
    if len(qualifying) < C2_MIN_REACHABLE_PRINCIPALS:
        return None
    dominant = max(qualifying, key=lambda pid: by_principal[pid])
    best_id = ""
    best_amt = -1.0
    for flow in data.get("resource_flows", []):
        if not isinstance(flow, dict):
            continue
        if flow.get("role") != role or str(flow.get("principal_id", "")) != dominant:
            continue
        if "compute" not in str(flow.get("resource_type", "")):
            continue
        amount = float(flow["amount_per_tick"])
        if amount > best_amt:
            best_amt = amount
            best_id = str(flow["id"])
    return best_id or None


def resolve_c2_v3_causal_gate_spec(data: dict) -> C2V3CausalGateSpec | None:
    meta = data.get("v3_fixture_metadata")
    if not isinstance(meta, dict):
        return None
    raw = meta.get("c2_v3_causal_gate")
    if not isinstance(raw, dict):
        return None
    focal_role = str(raw.get("focal_role", "engineer"))
    ablation_flow_id = str(raw.get("ablation_flow_id", ""))
    if not ablation_flow_id:
        ablation_flow_id = pick_c2_v3_ablation_flow_id(data, role=focal_role) or ""
    if not ablation_flow_id:
        return None
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    default_actor = next(
        (a.actor_id for a in roster.agents if a.role == focal_role),
        "eng1",
    )
    seeds_raw = raw.get("seeds", _DEFAULT_SEEDS)
    seeds = tuple(int(s) for s in seeds_raw)
    return C2V3CausalGateSpec(
        focal_role=focal_role,
        focal_actor_id=str(raw.get("focal_actor_id", default_actor)),
        ablation_flow_id=ablation_flow_id,
        seeds=seeds,
        histogram_l1_threshold=float(raw.get("histogram_l1_threshold", _DEFAULT_L1)),
        min_seeds_passing=int(raw.get("min_seeds_passing", _DEFAULT_MIN_PASS)),
        carrier_load_scale=float(raw.get("carrier_load_scale", _DEFAULT_LOAD)),
        T=int(raw.get("T", V3_REFERENCE_T)),
    )


def _episode_cfg(
    ecology_path: Path,
    *,
    spec: C2V3CausalGateSpec,
    ablate: bool,
    load_scale: float | None = None,
) -> EpisodeConfig:
    data = load_substrate(ecology_path).data
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    base = default_lab_config()
    scale = spec.carrier_load_scale if load_scale is None else load_scale
    settings = replace(base.substrate_settings, carrier_load_scale=scale)
    ablation = (spec.ablation_flow_id,) if ablate else ()
    return EpisodeConfig(
        agents=roster.agents,
        T=spec.T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=ecology_path,
        flow_ablation_ids=ablation,
    )


def seed_diverged(
    *,
    full: EpisodeResult,
    ablated: EpisodeResult,
    spec: C2V3CausalGateSpec,
) -> bool:
    deploy_diff = full.deploy_count != ablated.deploy_count
    hist_diff = _histogram_l1(
        _pattern_hist(full, actor_id=spec.focal_actor_id),
        _pattern_hist(ablated, actor_id=spec.focal_actor_id),
    ) >= spec.histogram_l1_threshold
    return deploy_diff or hist_diff


def evaluate_c2_v3_causal_gate(
    ecology_path: Path | str,
    *,
    backend=None,
) -> tuple[bool, dict[str, Any]]:
    """Return (passed, details) for one fixture's pre-registered causal gate."""
    ecology_path = Path(ecology_path)
    data = load_substrate(ecology_path).data
    spec = resolve_c2_v3_causal_gate_spec(data)
    if spec is None:
        return False, {"error": "missing c2_v3_causal_gate metadata or ablation flow"}
    expected = pick_c2_v3_ablation_flow_id(data, role=spec.focal_role)
    if expected and expected != spec.ablation_flow_id:
        return False, {
            "error": "frozen ablation_flow_id disagrees with C2-v3 picker",
            "expected": expected,
            "frozen": spec.ablation_flow_id,
        }
    programs = programs_for(WEAK_AGENT)
    iso = backend if backend is not None else MockIsolate()
    per_seed: list[dict[str, Any]] = []
    passing = 0
    for seed in spec.seeds:
        full = run_episode(
            _episode_cfg(ecology_path, spec=spec, ablate=False),
            seed,
            iso,
            programs=programs,
        )
        ablated = run_episode(
            _episode_cfg(ecology_path, spec=spec, ablate=True),
            seed,
            iso,
            programs=programs,
        )
        diverged = seed_diverged(full=full, ablated=ablated, spec=spec)
        if diverged:
            passing += 1
        per_seed.append(
            {
                "seed": seed,
                "diverged": diverged,
                "deploy_full": full.deploy_count,
                "deploy_ablated": ablated.deploy_count,
                "pattern_l1": _histogram_l1(
                    _pattern_hist(full, actor_id=spec.focal_actor_id),
                    _pattern_hist(ablated, actor_id=spec.focal_actor_id),
                ),
            }
        )
    passed = passing >= spec.min_seeds_passing
    return passed, {
        "focal_role": spec.focal_role,
        "focal_actor_id": spec.focal_actor_id,
        "ablation_flow_id": spec.ablation_flow_id,
        "seeds_passing": passing,
        "seeds_total": len(spec.seeds),
        "min_seeds_passing": spec.min_seeds_passing,
        "per_seed": per_seed,
    }
