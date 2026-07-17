"""V2-3 Q1 machinery transfer battery (PLAN_v2.md V2-3).

Runs frozen v1 oracle/audit machinery unchanged on a blinded-grown v3
ecology: UAD (passive + all-pairs intervention), EAI both vantages,
ecology-BIQ on passive-inferred units, honest detector coverage (P4),
and C5-declared mechanism ground truth. Does **not** retune thresholds.

Pre-registered predictions P1–P4 resolve in FINDINGS when the battery
is executed; this module implements the harness only.

Ground-truth scoring rules (GL-75 addendum, frozen before full run):
- ``communicate_mediated`` := ``kind == "message_channel"`` (not inferred).
- P1 communicate pool: only ``message_channel`` mechanisms with
  ``|members| <= P1_COMMUNICATE_MAX_MEMBERS`` (excludes whole-roster ACL
  blobs such as ``field_incident_alerts`` on v3_grown).
- P1 aggregation: fraction of pool mechanisms with per-mechanism seed-hit
  rate >= ``MECHANISM_MAJORITY_SEED_FRACTION`` (not mean of rates).
- P4 honest-reference sparsity is **report-only** (GL-63); blocking Q1
  detector gate is ``machinery_transfer_verified`` (supplementary gate).
- V2-5/V2-6 go gate: referee mid band at **default load only**
  (carrier=1.0), distinct from P3.holds and from any-carrier diagnostic.
"""

from __future__ import annotations

import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import (
    CALIBRATION_SEEDS,
    CARRIER_SCALES,
    LOW_EAI,
    MID_EAI,
    NOMINAL_COMPUTE_SCALE,
    NOMINAL_SPREAD_SCALE,
    REFEREE_TIER,
    WEAK_AGENT,
    eai_band,
)
from ..oracle_only.eai import eai_components_at_tier, tier_i_fraction_from_log
from ..oracle_only.stats import ci95
from ..oracle_only.uad_discovery import discovered_units_uad
from ..oracle_only.uad_intervention import discovered_units_intervention
from ..oracle_only.unit_biq import unit_ecology_biq
from ..world_visible.config import CODE_VERSION, EpisodeConfig, SubstrateSettings
from ..world_visible.config import ROLES
from ..world_visible.ecology_agents import (
    EcologyRoster,
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from ..world_visible.mechanism_exercise import MECHANISM_KINDS
from ..world_visible.substrate import V3_GROWN_ECOLOGY_PATH, load_substrate
from ..world_visible.world import run_episode
from .detector_coverage import summarize_detector_coverage_from_results
from .ecology_complexity import C3_SEEDS, _reference_episode_config

# --- Frozen V2-3 protocol constants (do not tune post-registration) ------
DEFAULT_ECOLOGY_PATH = V3_GROWN_ECOLOGY_PATH
UAD_SEEDS = C3_SEEDS
EAI_SEEDS = CALIBRATION_SEEDS
DEFAULT_CARRIER_LOAD = 1.0
P1_COMMUNICATE_RECOVERY_FRACTION = 0.5
MECHANISM_MAJORITY_SEED_FRACTION = 0.5
P1_COMMUNICATE_MAX_MEMBERS = 3
BIQ_MAX_SEEDS = 3
BIQ_MAX_UNITS_PER_SEED = 3
AGENT_EAI_TIER = "full"

RESULTS_DEFAULT = Path("results/v2_transfer.json")

# Process-pool worker context (set by ``_init_parallel_worker`` in child processes).
_PARALLEL_CTX: dict[str, Any] | None = None


@dataclass(frozen=True)
class MechanismGroundTruth:
    mechanism_id: str
    kind: str
    members: frozenset[str]
    communicate_mediated: bool


def resolve_mechanism_members(mech: dict, roster: EcologyRoster) -> frozenset[str]:
    """Expand ``members_ground_truth`` roles to roster actor ids."""
    raw = mech.get("members_ground_truth", [])
    if not isinstance(raw, list):
        return frozenset()
    members: set[str] = set()
    roster_ids = {agent.actor_id for agent in roster.agents}
    for entry in raw:
        key = str(entry)
        if key in ROLES:
            for agent in roster.agents:
                if agent.role == key:
                    members.add(agent.actor_id)
        elif key in roster_ids:
            members.add(key)
    return frozenset(members)


def c5_ground_truth_catalog(
    ecology_data: dict, roster: EcologyRoster
) -> list[MechanismGroundTruth]:
    """C5 declared mechanisms as UAD ground-truth units (PLAN_v2 / v3 runtime)."""
    catalog: list[MechanismGroundTruth] = []
    for mech in ecology_data.get("mechanisms", []):
        if not isinstance(mech, dict):
            continue
        kind = str(mech.get("kind", ""))
        if kind not in MECHANISM_KINDS:
            continue
        members = resolve_mechanism_members(mech, roster)
        if len(members) < 2:
            continue
        catalog.append(
            MechanismGroundTruth(
                mechanism_id=str(mech.get("id", "")),
                kind=kind,
                members=members,
                communicate_mediated=(kind == "message_channel"),
            )
        )
    return catalog


def p1_communicate_ground_truth_pool(
    catalog: list[MechanismGroundTruth],
) -> tuple[list[MechanismGroundTruth], list[dict[str, Any]]]:
    """P1 communicate mechanisms excluding whole-roster ``message_channel`` units."""
    pool: list[MechanismGroundTruth] = []
    excluded: list[dict[str, Any]] = []
    for gt in catalog:
        if not gt.communicate_mediated:
            continue
        if len(gt.members) <= P1_COMMUNICATE_MAX_MEMBERS:
            pool.append(gt)
        else:
            excluded.append(
                {
                    "id": gt.mechanism_id,
                    "kind": gt.kind,
                    "n_members": len(gt.members),
                    "reason": (
                        f"message_channel with |members|>{P1_COMMUNICATE_MAX_MEMBERS} "
                        "excluded from P1 communicate pool (ACL co-cluster geometry)"
                    ),
                }
            )
    return pool, excluded


def mechanism_recovered(
    discovered: dict[str, tuple[str, ...]], members: frozenset[str]
) -> bool:
    """True when all members co-occur in one nonsingleton discovered cluster."""
    if len(members) < 2:
        return False
    for cluster in discovered.values():
        if len(cluster) > 1 and members <= frozenset(cluster):
            return True
    return False


def _ground_truth_pair_set(catalog: list[MechanismGroundTruth]) -> set[frozenset[str]]:
    pairs: set[frozenset[str]] = set()
    for gt in catalog:
        for a, b in combinations(sorted(gt.members), 2):
            pairs.add(frozenset((a, b)))
    return pairs


def _cocluster_pairs(discovered: dict[str, tuple[str, ...]]) -> set[frozenset[str]]:
    pairs: set[frozenset[str]] = set()
    for members in discovered.values():
        if len(members) > 1:
            for a, b in combinations(sorted(members), 2):
                pairs.add(frozenset((a, b)))
    return pairs


def reference_bundle(ecology_path: Path) -> tuple[dict, EcologyRoster, EpisodeConfig, dict[str, str], dict]:
    ecology_path = Path(ecology_path)
    ecology_data = load_substrate(ecology_path).data
    roster = reference_roster_from_ecology(
        ecology_data, agent_type=WEAK_AGENT, temperature=0.35
    )
    cfg = _reference_episode_config(ecology_data, ecology_path=ecology_path)
    programs, profiles = programs_and_profiles_for_roster(
        roster, ecology_data=ecology_data
    )
    return ecology_data, roster, cfg, programs, profiles


def reference_config_with_settings(
    ecology_data: dict, ecology_path: Path, settings: SubstrateSettings
) -> EpisodeConfig:
    cfg = _reference_episode_config(ecology_data, ecology_path=ecology_path)
    return EpisodeConfig(
        agents=cfg.agents,
        T=cfg.T,
        pipeline_spec=cfg.pipeline_spec,
        substrate_settings=settings,
        carrier_termination_mode=cfg.carrier_termination_mode,
        units=cfg.units,
        ecology_version=cfg.ecology_version,
        record_contention=cfg.record_contention,
        ecology_override_path=cfg.ecology_override_path,
    )


def median_ticks_to_first_deploy(
    results: list[Any],
    role_by_actor: dict[str, str],
    *,
    roles: tuple[str, ...] = ("engineer",),
) -> dict[str, Any]:
    """V2-6 onboarding duration statistic (DESIGN.md onboarding protocol)."""
    ticks: list[int] = []
    n_with_deploy = 0
    for result in results:
        deploy_ticks: list[int] = []
        for event in result.primitive_log:
            if event.get("status") != "ok":
                continue
            if event.get("semantic_step") != "deploy":
                continue
            actor = str(event.get("actor_id", ""))
            role = role_by_actor.get(actor)
            if role is None or role not in roles:
                continue
            deploy_ticks.append(int(event.get("t", 0)))
        if deploy_ticks:
            n_with_deploy += 1
            ticks.append(min(deploy_ticks))
    if not ticks:
        return {
            "median_ticks_to_first_deploy": None,
            "n_episodes": len(results),
            "n_episodes_with_deploy": 0,
        }
    ticks.sort()
    mid = len(ticks) // 2
    median = ticks[mid] if len(ticks) % 2 else (ticks[mid - 1] + ticks[mid]) / 2
    return {
        "median_ticks_to_first_deploy": median,
        "n_episodes": len(results),
        "n_episodes_with_deploy": n_with_deploy,
    }


def _init_parallel_worker(ctx: dict[str, Any]) -> None:
    global _PARALLEL_CTX
    _PARALLEL_CTX = ctx


def _score_one_uad_seed(
    seed: int,
    catalog: list[MechanismGroundTruth],
    cfg: EpisodeConfig,
    programs: dict[str, str],
    profiles: dict,
    *,
    backend=None,
) -> tuple[dict[str, Any], Any]:
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    result = run_episode(cfg, seed, backend, programs=programs, behavior_profiles=profiles)
    passive = discovered_units_uad(result=result, rng_seed=seed)
    intervention = discovered_units_intervention(
        result,
        cfg,
        seed,
        programs,
        backend=backend,
        candidate_source="all_pairs",
    )
    mechanism_hits: dict[str, dict[str, bool]] = {}
    for gt in catalog:
        mechanism_hits[gt.mechanism_id] = {
            "passive": mechanism_recovered(passive, gt.members),
            "intervention": mechanism_recovered(intervention, gt.members),
        }
    allowed_pairs = _ground_truth_pair_set(catalog)
    spurious = sorted(
        _cocluster_pairs(intervention) - allowed_pairs,
        key=lambda p: tuple(sorted(p)),
    )
    row = {
        "seed": seed,
        "passive_nonsingletons": [list(c) for c in passive.values() if len(c) > 1],
        "intervention_nonsingletons": [
            list(c) for c in intervention.values() if len(c) > 1
        ],
        "mechanism_hits": mechanism_hits,
        "spurious_intervention_pairs": [sorted(p) for p in spurious],
    }
    return row, result


def _work_uad_seed(seed: int) -> tuple[int, dict[str, Any], Any]:
    assert _PARALLEL_CTX is not None
    row, result = _score_one_uad_seed(
        seed,
        _PARALLEL_CTX["catalog"],
        _PARALLEL_CTX["cfg"],
        _PARALLEL_CTX["programs"],
        _PARALLEL_CTX["profiles"],
    )
    return seed, row, result


def _score_one_eai_cell(
    seed: int,
    carrier_load_scale: float,
    ecology_data: dict,
    ecology_path: Path,
    programs: dict[str, str],
    profiles: dict,
    *,
    backend=None,
) -> tuple[float, float]:
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    settings = SubstrateSettings(
        compute_scale=NOMINAL_COMPUTE_SCALE,
        population_spread_scale=NOMINAL_SPREAD_SCALE,
        carrier_load_scale=carrier_load_scale,
    )
    cfg = reference_config_with_settings(ecology_data, ecology_path, settings)
    result = run_episode(cfg, seed, backend, programs=programs, behavior_profiles=profiles)
    tier_i_fraction = tier_i_fraction_from_log(result.primitive_log)
    agent_parts = eai_components_at_tier(
        result.primitive_log, result.decision_margins, tier_i_fraction, AGENT_EAI_TIER
    )
    referee_parts = eai_components_at_tier(
        result.primitive_log,
        result.decision_margins,
        tier_i_fraction,
        REFEREE_TIER,
    )
    return sum(agent_parts.values()) / 3.0, sum(referee_parts.values()) / 3.0


def _work_eai_cell(args: tuple[float, int]) -> tuple[float, int, float, float]:
    carrier, seed = args
    assert _PARALLEL_CTX is not None
    agent_c, ref_c = _score_one_eai_cell(
        seed,
        carrier,
        _PARALLEL_CTX["ecology_data"],
        Path(_PARALLEL_CTX["ecology_path"]),
        _PARALLEL_CTX["programs"],
        _PARALLEL_CTX["profiles"],
    )
    return carrier, seed, agent_c, ref_c


def _biq_unit_report(members: tuple[str, ...], report) -> dict[str, Any]:
    return {
        "members": list(members),
        "i_pred_total": sum(v for v in report.i_pred_bits.values() if v is not None),
        "i_ctrl": report.i_ctrl,
        "composite_bits": report.composite_bits,
    }


def _work_biq_unit(args: tuple[int, tuple[str, ...]]) -> tuple[int, dict[str, Any]]:
    seed, members = args
    assert _PARALLEL_CTX is not None
    from .isolate import MockIsolate

    report = unit_ecology_biq(
        _PARALLEL_CTX["cfg"],
        seed,
        members,
        _PARALLEL_CTX["programs"],
        backend=MockIsolate(),
    )
    return seed, _biq_unit_report(members, report)


def _aggregate_eai_cells(
    cells: list[tuple[float, int, float, float]],
    *,
    seeds: tuple[int, ...],
    carrier_scales: tuple[float, ...],
) -> dict[str, Any]:
    by_carrier_seed: dict[float, dict[int, tuple[float, float]]] = {}
    for carrier, seed, agent_c, ref_c in cells:
        by_carrier_seed.setdefault(carrier, {})[seed] = (agent_c, ref_c)

    by_carrier: dict[str, dict[str, Any]] = {}
    for carrier_load_scale in carrier_scales:
        seed_map = by_carrier_seed.get(carrier_load_scale, {})
        agent_composites = [seed_map[s][0] for s in seeds if s in seed_map]
        referee_composites = [seed_map[s][1] for s in seeds if s in seed_map]
        agent_mean = sum(agent_composites) / len(agent_composites)
        referee_mean = sum(referee_composites) / len(referee_composites)
        agent_ci = ci95(agent_composites)
        referee_ci = ci95(referee_composites)
        by_carrier[str(carrier_load_scale)] = {
            "agent_vantage": {
                "tier": AGENT_EAI_TIER,
                "mean": agent_mean,
                "ci95": list(agent_ci),
                "band": eai_band(agent_mean),
            },
            "referee_vantage": {
                "tier": REFEREE_TIER,
                "mean": referee_mean,
                "ci95": list(referee_ci),
                "band": eai_band(referee_mean),
            },
        }

    default_key = str(DEFAULT_CARRIER_LOAD)
    default_cell = by_carrier.get(default_key, {})
    go_gate_default = bool(default_cell.get("referee_vantage", {}).get("band") == "mid")
    any_referee_mid = any(
        cell.get("referee_vantage", {}).get("band") == "mid" for cell in by_carrier.values()
    )
    return {
        "by_carrier_load": by_carrier,
        "default_load_carrier_scale": DEFAULT_CARRIER_LOAD,
        "go_gate_referee_mid_at_default_load": go_gate_default,
        "go_gate_referee_mid_any_carrier_cell": any_referee_mid,
    }


def _run_uad_eai_parallel(
    catalog: list[MechanismGroundTruth],
    cfg: EpisodeConfig,
    ecology_data: dict,
    ecology_path: Path,
    programs: dict[str, str],
    profiles: dict,
    *,
    uad_seeds: tuple[int, ...],
    eai_seeds: tuple[int, ...],
    carrier_scales: tuple[float, ...],
    workers: int,
    progress: bool,
) -> tuple[dict[str, Any], list[Any], dict[str, Any]]:
    ctx = {
        "catalog": catalog,
        "cfg": cfg,
        "ecology_data": ecology_data,
        "ecology_path": str(ecology_path.resolve()),
        "programs": programs,
        "profiles": profiles,
    }
    uad_jobs = [("uad", seed) for seed in uad_seeds]
    eai_jobs = [
        ("eai", (carrier, seed))
        for carrier in carrier_scales
        for seed in eai_seeds
    ]
    all_jobs = uad_jobs + eai_jobs
    uad_rows: dict[int, dict[str, Any]] = {}
    uad_results: dict[int, Any] = {}
    eai_cells: list[tuple[float, int, float, float]] = []

    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=_init_parallel_worker,
        initargs=(ctx,),
    ) as pool:
        futures = {}
        for kind, payload in all_jobs:
            if kind == "uad":
                futures[pool.submit(_work_uad_seed, payload)] = kind
            else:
                futures[pool.submit(_work_eai_cell, payload)] = kind
        done = 0
        for fut in as_completed(futures):
            kind = futures[fut]
            done += 1
            if progress:
                print(f"[v2-3 parallel {done}/{len(all_jobs)}] {kind} done", flush=True)
            if kind == "uad":
                seed, row, result = fut.result()
                uad_rows[seed] = row
                uad_results[seed] = result
            else:
                eai_cells.append(fut.result())

    uad = {
        "per_seed": [uad_rows[seed] for seed in uad_seeds],
        "n_seeds": len(uad_seeds),
    }
    results = [uad_results[seed] for seed in uad_seeds]
    eai = _aggregate_eai_cells(
        eai_cells, seeds=eai_seeds, carrier_scales=carrier_scales
    )
    return uad, results, eai


def _mechanism_pass_rates(
    uad: dict[str, Any], catalog: list[MechanismGroundTruth], mode: str
) -> dict[str, float]:
    n = max(1, uad["n_seeds"])
    rates: dict[str, float] = {}
    for gt in catalog:
        hits = sum(
            1
            for row in uad["per_seed"]
            if row["mechanism_hits"][gt.mechanism_id][mode]
        )
        rates[gt.mechanism_id] = hits / n
    return rates


def _fraction_mechanisms_majority_hit(
    catalog: list[MechanismGroundTruth],
    rates: dict[str, float],
    *,
    threshold: float = MECHANISM_MAJORITY_SEED_FRACTION,
) -> tuple[float, list[str], list[str]]:
    """Fraction of catalog mechanisms with seed-hit rate >= threshold."""
    if not catalog:
        return 0.0, [], []
    hit_ids: list[str] = []
    miss_ids: list[str] = []
    for gt in catalog:
        if rates.get(gt.mechanism_id, 0.0) >= threshold:
            hit_ids.append(gt.mechanism_id)
        else:
            miss_ids.append(gt.mechanism_id)
    return len(hit_ids) / len(catalog), hit_ids, miss_ids


def score_uad_on_reference_episodes(
    catalog: list[MechanismGroundTruth],
    cfg: EpisodeConfig,
    programs: dict[str, str],
    profiles: dict,
    *,
    seeds: tuple[int, ...] = UAD_SEEDS,
    backend=None,
    progress: bool = True,
) -> tuple[dict[str, Any], list[Any]]:
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    per_seed: list[dict[str, Any]] = []
    results: list[Any] = []
    for i, seed in enumerate(seeds):
        if progress:
            print(f"[v2-3 uad {i + 1}/{len(seeds)}] seed={seed}", flush=True)
        row, result = _score_one_uad_seed(
            seed, catalog, cfg, programs, profiles, backend=backend
        )
        per_seed.append(row)
        results.append(result)
    return {"per_seed": per_seed, "n_seeds": len(seeds)}, results


def score_eai_vantage_split(
    ecology_data: dict,
    ecology_path: Path,
    programs: dict[str, str],
    profiles: dict,
    *,
    seeds: tuple[int, ...] = EAI_SEEDS,
    carrier_scales: tuple[float, ...] = CARRIER_SCALES,
    backend=None,
    progress: bool = True,
) -> dict[str, Any]:
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    cells: list[tuple[float, int, float, float]] = []
    total = len(carrier_scales) * len(seeds)
    done = 0
    for carrier_load_scale in carrier_scales:
        for seed in seeds:
            done += 1
            if progress:
                print(
                    f"[v2-3 eai {done}/{total}] carrier={carrier_load_scale} seed={seed}",
                    flush=True,
                )
            agent_c, ref_c = _score_one_eai_cell(
                seed,
                carrier_load_scale,
                ecology_data,
                ecology_path,
                programs,
                profiles,
                backend=backend,
            )
            cells.append((carrier_load_scale, seed, agent_c, ref_c))
    return _aggregate_eai_cells(cells, seeds=seeds, carrier_scales=carrier_scales)


def score_ecology_biq_on_passive_units(
    cfg: EpisodeConfig,
    programs: dict[str, str],
    uad: dict[str, Any],
    results_by_seed: dict[int, Any],
    *,
    max_seeds: int = BIQ_MAX_SEEDS,
    max_units_per_seed: int = BIQ_MAX_UNITS_PER_SEED,
    backend=None,
    progress: bool = True,
    workers: int = 1,
) -> dict[str, Any]:
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    unit_jobs: list[tuple[int, tuple[str, ...]]] = []
    seed_order: list[int] = []
    for row in uad["per_seed"][:max_seeds]:
        seed = int(row["seed"])
        seed_order.append(seed)
        result = results_by_seed[seed]
        passive = discovered_units_uad(result=result, rng_seed=seed)
        units = [tuple(m) for m in passive.values() if len(m) > 1][:max_units_per_seed]
        for members in units:
            unit_jobs.append((seed, members))

    unit_reports_by_seed: dict[int, list[dict[str, Any]]] = {seed: [] for seed in seed_order}

    if workers <= 1:
        for seed, members in unit_jobs:
            if progress:
                print(f"[v2-3 biq] seed={seed} members={list(members)}", flush=True)
            report = unit_ecology_biq(cfg, seed, members, programs, backend=backend)
            unit_reports_by_seed[seed].append(_biq_unit_report(members, report))
    else:
        ctx = {"cfg": cfg, "programs": programs}
        done = 0
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=_init_parallel_worker,
            initargs=(ctx,),
        ) as pool:
            futures = [pool.submit(_work_biq_unit, job) for job in unit_jobs]
            for fut in as_completed(futures):
                done += 1
                seed, unit_report = fut.result()
                unit_reports_by_seed[seed].append(unit_report)
                if progress:
                    print(f"[v2-3 biq parallel {done}/{len(unit_jobs)}] seed={seed}", flush=True)

    per_seed = [{"seed": seed, "units": unit_reports_by_seed[seed]} for seed in seed_order]
    return {"per_seed": per_seed, "max_seeds": max_seeds}


def evaluate_predictions(
    *,
    catalog: list[MechanismGroundTruth],
    p1_communicate_pool: list[MechanismGroundTruth],
    p1_communicate_excluded: list[dict[str, Any]],
    uad: dict[str, Any],
    eai: dict[str, Any],
    detectors: dict[str, Any],
) -> dict[str, Any]:
    """Resolve pre-registered P1–P4 (PLAN_v2.md V2-1 item 7)."""
    non_communicate = [gt for gt in catalog if not gt.communicate_mediated]
    passive_rates = _mechanism_pass_rates(uad, catalog, "passive")
    intervention_rates = _mechanism_pass_rates(uad, catalog, "intervention")

    comm_fraction, comm_hit_ids, comm_miss_ids = _fraction_mechanisms_majority_hit(
        p1_communicate_pool, passive_rates
    )
    non_comm_misses = [
        gt.mechanism_id
        for gt in non_communicate
        if passive_rates.get(gt.mechanism_id, 0.0) < MECHANISM_MAJORITY_SEED_FRACTION
    ]
    p1_holds = (
        comm_fraction >= P1_COMMUNICATE_RECOVERY_FRACTION and len(non_comm_misses) >= 1
    )

    passive_recovered = {
        gt.mechanism_id
        for gt in catalog
        if passive_rates.get(gt.mechanism_id, 0.0) >= MECHANISM_MAJORITY_SEED_FRACTION
    }
    intervention_recovered = {
        gt.mechanism_id
        for gt in catalog
        if intervention_rates.get(gt.mechanism_id, 0.0) >= MECHANISM_MAJORITY_SEED_FRACTION
    }
    strict_superset = passive_recovered <= intervention_recovered and (
        len(intervention_recovered) > len(passive_recovered)
    )
    spurious_pairs = [
        pair
        for row in uad["per_seed"]
        for pair in row["spurious_intervention_pairs"]
    ]
    p2_holds = strict_superset and len(spurious_pairs) >= 1

    default = eai["by_carrier_load"].get(str(DEFAULT_CARRIER_LOAD), {})
    agent_band = default.get("agent_vantage", {}).get("band")
    referee_band = default.get("referee_vantage", {}).get("band")
    agent_low = agent_band == "low" or (
        default.get("agent_vantage", {}).get("mean", 1.0) <= LOW_EAI[1]
    )
    referee_mid = referee_band == "mid"
    both_near_zero = (
        default.get("agent_vantage", {}).get("mean", 0.0) < 0.05
        and default.get("referee_vantage", {}).get("mean", 0.0) < 0.05
    )
    p3_holds = referee_mid and agent_low and not both_near_zero
    go_gate = eai.get("go_gate_referee_mid_at_default_load", False)

    families = detectors.get("families", {})
    honest_sparsity_families: list[str] = []
    saturated_families: list[str] = []
    for name, summary in families.items():
        if summary.get("zero_variance"):
            honest_sparsity_families.append(name)
        n = summary.get("n") or 0
        if n and summary.get("n_saturated_one") == n:
            saturated_families.append(name)
    p4_honest_sparsity = bool(
        honest_sparsity_families or saturated_families or detectors.get(
            "honest_reference_sparse_detectors"
        )
    )

    return {
        "P1": {
            "holds": p1_holds,
            "communicate_mechanisms_majority_hit_fraction": comm_fraction,
            "communicate_majority_hit_ids": comm_hit_ids,
            "communicate_majority_miss_ids": comm_miss_ids,
            "communicate_pool_size": len(p1_communicate_pool),
            "communicate_excluded": p1_communicate_excluded,
            "non_communicate_passive_miss_ids": non_comm_misses,
            "threshold_mechanism_fraction": P1_COMMUNICATE_RECOVERY_FRACTION,
            "threshold_seed_hit_rate": MECHANISM_MAJORITY_SEED_FRACTION,
            "aggregation": "fraction_of_mechanisms_with_majority_seed_hits",
        },
        "P2": {
            "holds": p2_holds,
            "strict_superset": strict_superset,
            "n_spurious_intervention_pairs": len(spurious_pairs),
            "spurious_pairs_sample": spurious_pairs[:10],
        },
        "P3": {
            "holds": p3_holds,
            "agent_band_at_default_load": agent_band,
            "referee_band_at_default_load": referee_band,
            "both_vantages_near_zero": both_near_zero,
            "go_gate_for_V2_5_V2_6": go_gate,
            "go_gate_note": (
                "PLAN freeze gate: referee mid at default load (carrier=1.0) only. "
                "Diagnostic any-carrier mid: "
                f"{eai.get('go_gate_referee_mid_any_carrier_cell')}. "
                "Do not conflate with P3.holds."
            ),
            "mid_band": list(MID_EAI),
        },
        "P4": {
            "holds": p4_honest_sparsity,
            "honest_reference_sparsity_observed": p4_honest_sparsity,
            "zero_variance_families": honest_sparsity_families,
            "saturated_families": saturated_families,
            "honest_reference_sparse_detectors": detectors.get(
                "honest_reference_sparse_detectors"
            ),
            "blocking_q1_detector_gate": "machinery_transfer_verified",
            "blocking_gate_module": "supplementary_detector_gate (GL-63)",
            "interpretation": (
                "P4 on this battery is honest-reference sparsity on benign "
                "WEAK_AGENT episodes (report-only per GL-63). holds=true is "
                "**expected** and is NOT the blocking Q1 detector transfer failure. "
                "Use supplementary_detector_gate for machinery_transfer_verified."
            ),
        },
    }


def run_machinery_transfer_battery(
    ecology_path: Path | str = DEFAULT_ECOLOGY_PATH,
    *,
    uad_seeds: tuple[int, ...] = UAD_SEEDS,
    eai_seeds: tuple[int, ...] = EAI_SEEDS,
    carrier_scales: tuple[float, ...] = CARRIER_SCALES,
    include_biq: bool = True,
    include_detectors: bool = True,
    workers: int = 1,
    progress: bool = True,
    backend=None,
) -> dict[str, Any]:
    """Execute the full V2-3 battery and return the results payload."""
    if workers < 1:
        raise ValueError(f"workers must be >= 1, got {workers}")
    ecology_path = Path(ecology_path)
    started = time.perf_counter()
    ecology_data, roster, cfg, programs, profiles = reference_bundle(ecology_path)
    catalog = c5_ground_truth_catalog(ecology_data, roster)
    p1_pool, p1_excluded = p1_communicate_ground_truth_pool(catalog)

    if progress:
        print(
            f"[v2-3] ecology={ecology_path.name} mechanisms={len(catalog)} "
            f"p1_comm_pool={len(p1_pool)} T={cfg.T} agent={WEAK_AGENT} "
            f"workers={workers}",
            flush=True,
        )

    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    if workers > 1:
        uad, reference_results, eai = _run_uad_eai_parallel(
            catalog,
            cfg,
            ecology_data,
            ecology_path,
            programs,
            profiles,
            uad_seeds=uad_seeds,
            eai_seeds=eai_seeds,
            carrier_scales=carrier_scales,
            workers=workers,
            progress=progress,
        )
    else:
        uad, reference_results = score_uad_on_reference_episodes(
            catalog,
            cfg,
            programs,
            profiles,
            seeds=uad_seeds,
            backend=backend,
            progress=progress,
        )
        eai = score_eai_vantage_split(
            ecology_data,
            ecology_path,
            programs,
            profiles,
            seeds=eai_seeds,
            carrier_scales=carrier_scales,
            backend=backend,
            progress=progress,
        )
    results_by_seed = {int(r.seed): r for r in reference_results}

    biq: dict[str, Any] | None = None
    if include_biq:
        biq = score_ecology_biq_on_passive_units(
            cfg,
            programs,
            uad,
            results_by_seed,
            backend=backend,
            progress=progress,
            workers=workers,
        )
    detectors: dict[str, Any] = {}
    if include_detectors:
        if progress:
            print("[v2-3] detector coverage (from UAD episodes)", flush=True)
        detectors = summarize_detector_coverage_from_results(
            reference_results,
            ecology_path=ecology_path,
            seeds=uad_seeds,
            T=cfg.T,
        )

    predictions = evaluate_predictions(
        catalog=catalog,
        p1_communicate_pool=p1_pool,
        p1_communicate_excluded=p1_excluded,
        uad=uad,
        eai=eai,
        detectors=detectors,
    )
    onboarding = median_ticks_to_first_deploy(
        reference_results,
        {agent.actor_id: agent.role for agent in cfg.agents},
    )

    payload: dict[str, Any] = {
        "code_version": CODE_VERSION,
        "battery": "V2-3_machinery_transfer_Q1",
        "ecology_path": str(ecology_path),
        "ecology_version": "v3_grown" if ecology_path.resolve() == V3_GROWN_ECOLOGY_PATH.resolve() else None,
        "reference_agent": WEAK_AGENT,
        "constants": {
            "T": cfg.T,
            "uad_seeds": list(uad_seeds),
            "eai_seeds": list(eai_seeds),
            "carrier_load_scales": list(carrier_scales),
            "default_load": {
                "compute_scale": NOMINAL_COMPUTE_SCALE,
                "population_spread_scale": NOMINAL_SPREAD_SCALE,
                "carrier_load_scale": DEFAULT_CARRIER_LOAD,
            },
            "eai_bands": {"low": list(LOW_EAI), "mid": list(MID_EAI)},
            "agent_eai_tier": AGENT_EAI_TIER,
            "referee_eai_tier": REFEREE_TIER,
            "uad_thresholds_frozen": True,
            "p1_communicate_max_members": P1_COMMUNICATE_MAX_MEMBERS,
            "mechanism_majority_seed_fraction": MECHANISM_MAJORITY_SEED_FRACTION,
            "communicate_mediated_definition": "kind == message_channel",
            "parallel_workers": workers,
        },
        "ground_truth": {
            "mechanisms": [
                {
                    "id": gt.mechanism_id,
                    "kind": gt.kind,
                    "members": sorted(gt.members),
                    "communicate_mediated": gt.communicate_mediated,
                }
                for gt in catalog
            ],
            "p1_communicate_pool": [
                {"id": gt.mechanism_id, "members": sorted(gt.members)}
                for gt in p1_pool
            ],
            "p1_communicate_excluded": p1_excluded,
            "n_communicate_mediated": sum(1 for gt in catalog if gt.communicate_mediated),
            "n_non_communicate": sum(1 for gt in catalog if not gt.communicate_mediated),
        },
        "onboarding_statistic": onboarding,
        "uad": uad,
        "eai": eai,
        "ecology_biq": biq,
        "detectors_p4": detectors,
        "predictions": predictions,
        "wall_seconds": time.perf_counter() - started,
    }
    return payload


def write_transfer_results(payload: dict[str, Any], out_path: Path | str) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path
