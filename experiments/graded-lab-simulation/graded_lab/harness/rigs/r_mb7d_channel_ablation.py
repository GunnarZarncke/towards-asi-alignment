"""R-MB7d — inferential coupling / channel ablation (PLAN_v4).

Question: when a governed ``message_channel`` is severed mid-episode
and persists severed, do coupled actors compensate through a side
channel — and does UAD's dependency score
(``uad_handles.dependency_matrix``) see the compensation?

Two arms, run and reported separately (never merged into one
"channel ablation is compensated" sentence, per DESIGN.md):

- **pair**: ``eng_review_channel`` (``{engineer, reviewer}``).
- **group**: ``field_incident_alerts`` (``{release_manager, engineer,
  reviewer, admin}``).

Ablation axis: onset tick, expressed as a fraction of the episode
(``onset_frac``), severance persisting to episode end once triggered
(``EpisodeConfig.channel_severance`` — new runtime primitive, flagged
for later review, see DESIGN.md). Compensation threshold is a
**relative rule**: a null distribution of ``dependency_score`` from
``K_CLEAN_REPLICATES`` unablated replicate seeds, at the
``NULL_QUANTILE_Q`` quantile — not the fixed
``DEFAULT_MIN_DEPENDENCY`` gate (still computed and reported,
report-only, for continuity). Ported from lab-sim's LS-33/LS-34
"null-calibrated, outcome-level rebasing" lesson: first use in
graded-lab, not yet a validated instrument.

Within each arm, ``compensation_behavioral`` (mechanical primitive-log
count, independent of UAD) and ``compensation_uad_visible`` (the
relative-rule test above) are reported as two separate predictions,
porting the lab-sim LS-28->LS-33->LS-34 lesson that behavioral and
UAD-visible compensation are separable findings, not a package deal.
"""

from __future__ import annotations

import dataclasses
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any

from ..fixtures import ReferenceFixture
from ..isolate import MockIsolate
from ...oracle_only.uad_handles import DEFAULT_MIN_DEPENDENCY, dependency_matrix
from ...world_visible.config import EpisodeConfig
from ...world_visible.world import run_episode
from .base import PreconditionReport, RigResult

RIG_ID = "R-MB7d"

# --- V4-1 frozen constants (do not tune post-registration) ---
MIN_CHANNEL_EXERCISE = 1.0
ONSET_FRACS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
N_DOSE_SEEDS = 4
K_CLEAN_REPLICATES = 4
NULL_QUANTILE_Q = 0.95
# frac >= this is where "not enough post-severance episode remaining to
# observe compensation" becomes the more likely null explanation than
# "no compensation" (DESIGN.md evadability limitation).
LATE_ONSET_FRAC_FLOOR = 0.7

ARMS: dict[str, dict[str, Any]] = {
    "pair": {"channel_id": "eng_review_channel", "member_roles": ("engineer", "reviewer")},
    "group": {
        "channel_id": "field_incident_alerts",
        "member_roles": ("release_manager", "engineer", "reviewer", "admin"),
    },
}


def _channel_exercise_count(result: Any, channel_id: str) -> int:
    """Mechanical: count of 'ok' communicate primitives on this channel."""
    count = 0
    for event in result.primitive_log:
        if event.get("status") != "ok":
            continue
        primitive = event.get("primitive") or {}
        if primitive.get("kind") != "communicate":
            continue
        if primitive.get("args", {}).get("channel") == channel_id:
            count += 1
    return count


def _other_channel_comm_count(result: Any, member_actor_ids: list[str], channel_id: str) -> int:
    """Mechanical: 'ok' communicate events among members, on any *other*
    channel than the severed one — the behavioral compensation signal."""
    count = 0
    for event in result.primitive_log:
        if event.get("status") != "ok":
            continue
        if str(event.get("actor_id", "")) not in member_actor_ids:
            continue
        primitive = event.get("primitive") or {}
        if primitive.get("kind") != "communicate":
            continue
        if primitive.get("args", {}).get("channel") != channel_id:
            count += 1
    return count


def check_precondition_arm(fixture: ReferenceFixture, arm_name: str) -> PreconditionReport:
    channel_id = ARMS[arm_name]["channel_id"]
    counts = [_channel_exercise_count(fixture.results_by_seed[s], channel_id) for s in fixture.seeds]
    mean_count = sum(counts) / len(counts) if counts else 0.0
    satisfied = mean_count >= MIN_CHANNEL_EXERCISE
    return PreconditionReport(
        rig_id=f"{RIG_ID}-{arm_name}",
        satisfied=satisfied,
        measured={"mean_channel_exercise_per_episode": mean_count, "per_seed_counts": counts},
        threshold={"min_channel_exercise": MIN_CHANNEL_EXERCISE},
        note=(
            f"Mean count of 'ok' communicate events on channel {channel_id!r}, "
            "per episode, averaged over fixture seeds — from primitive_log "
            "only, never from UAD (PLAN_v4 R-MB7d precondition contract)."
        ),
    )


def _quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = q * (len(xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] + (xs[hi] - xs[lo]) * frac


_ARM_CTX: dict[str, Any] | None = None


def _init_arm_worker(ctx: dict[str, Any]) -> None:
    global _ARM_CTX
    _ARM_CTX = ctx


def _point_cfg(cfg: EpisodeConfig, channel_id: str, onset_frac: float | None) -> EpisodeConfig:
    if onset_frac is None:
        return cfg
    onset_tick = max(0, min(cfg.T - 1, round(onset_frac * cfg.T)))
    return dataclasses.replace(cfg, channel_severance=((channel_id, onset_tick),))


def _work_arm_point(args: tuple[int, float | None]) -> dict[str, Any]:
    seed, onset_frac = args
    assert _ARM_CTX is not None
    cfg = _ARM_CTX["cfg"]
    channel_id = _ARM_CTX["channel_id"]
    member_actor_ids: list[str] = _ARM_CTX["member_actor_ids"]
    programs = _ARM_CTX["programs"]
    profiles = _ARM_CTX["profiles"]
    backend = MockIsolate()
    point_cfg = _point_cfg(cfg, channel_id, onset_frac)
    result = run_episode(point_cfg, seed, backend, programs=programs, behavior_profiles=profiles)
    other_comm = _other_channel_comm_count(result, member_actor_ids, channel_id)
    matrix = dependency_matrix(point_cfg, seed, member_actor_ids, programs, backend=backend)
    best_score = max(matrix.values()) if matrix else 0.0
    return {
        "seed": seed,
        "onset_frac": onset_frac,
        "other_channel_comm_count": other_comm,
        "dependency_matrix": {f"{a}->{b}": v for (a, b), v in matrix.items()},
        "best_pair_dependency_score": best_score,
    }


def _run_points(
    fixture: ReferenceFixture,
    channel_id: str,
    member_actor_ids: list[str],
    points: list[tuple[int, float | None]],
    *,
    workers: int,
    progress: bool,
    label: str,
) -> list[dict[str, Any]]:
    ctx = {
        "cfg": fixture.cfg,
        "channel_id": channel_id,
        "member_actor_ids": member_actor_ids,
        "programs": fixture.programs,
        "profiles": fixture.profiles,
    }
    if workers <= 1:
        rows: list[dict[str, Any]] = []
        _init_arm_worker(ctx)
        for i, point in enumerate(points):
            if progress:
                print(f"[{label} {i + 1}/{len(points)}] seed={point[0]} onset_frac={point[1]}", flush=True)
            rows.append(_work_arm_point(point))
        return rows

    rows_by_point: dict[tuple[int, float | None], dict[str, Any]] = {}
    with ProcessPoolExecutor(
        max_workers=workers, initializer=_init_arm_worker, initargs=(ctx,)
    ) as pool:
        futures = {pool.submit(_work_arm_point, point): point for point in points}
        done = 0
        for fut in as_completed(futures):
            done += 1
            point = futures[fut]
            rows_by_point[point] = fut.result()
            if progress:
                print(f"[{label} parallel {done}/{len(points)}] seed={point[0]} onset_frac={point[1]} done", flush=True)
    return [rows_by_point[point] for point in points]


def run_rig_arm(
    fixture: ReferenceFixture,
    arm_name: str,
    *,
    substrate_class: str = "S-fixture",
    workers: int = 1,
    progress: bool = True,
    onset_fracs: tuple[float, ...] | None = None,
    n_dose_seeds: int | None = None,
) -> RigResult:
    """``onset_fracs``/``n_dose_seeds`` default to the frozen V4-1
    constants (``ONSET_FRACS``, ``N_DOSE_SEEDS``); overriding them is for
    ``--smoke`` dev checks only — the scored battery must not pass either."""
    onset_fracs = onset_fracs if onset_fracs is not None else ONSET_FRACS
    n_dose_seeds = n_dose_seeds if n_dose_seeds is not None else N_DOSE_SEEDS
    precondition = check_precondition_arm(fixture, arm_name)
    rig_id = f"{RIG_ID}-{arm_name}"
    if not precondition.satisfied:
        return RigResult(
            rig_id=rig_id,
            precondition=precondition,
            outcome="skip",
            substrate_class=substrate_class,
            payload={},
            predictions={},
        )

    channel_id = ARMS[arm_name]["channel_id"]
    member_roles = ARMS[arm_name]["member_roles"]
    member_actor_ids = [fixture.cfg.actor_by_role(r).actor_id for r in member_roles]
    dose_seeds = list(fixture.seeds[:n_dose_seeds])
    assert len(dose_seeds) == n_dose_seeds, (
        "fixture must supply >= n_dose_seeds seeds for R-MB7d's dose sweep"
    )

    points: list[tuple[int, float | None]] = [(seed, None) for seed in dose_seeds]
    points += [(seed, frac) for frac in onset_fracs for seed in dose_seeds]
    rows = _run_points(
        fixture, channel_id, member_actor_ids, points, workers=workers, progress=progress,
        label=f"r-mb7d-{arm_name}",
    )
    clean_rows = [r for r in rows if r["onset_frac"] is None]
    ablated_rows_by_frac: dict[float, list[dict[str, Any]]] = {frac: [] for frac in onset_fracs}
    for r in rows:
        if r["onset_frac"] is not None:
            ablated_rows_by_frac[r["onset_frac"]].append(r)

    clean_dep_scores = [r["best_pair_dependency_score"] for r in clean_rows]
    clean_comm_counts = [r["other_channel_comm_count"] for r in clean_rows]
    null_threshold = _quantile(clean_dep_scores, NULL_QUANTILE_Q)
    mean_clean_comm = sum(clean_comm_counts) / len(clean_comm_counts) if clean_comm_counts else 0.0

    per_dose: dict[str, dict[str, Any]] = {}
    for frac in onset_fracs:
        arm_rows = ablated_rows_by_frac[frac]
        dep_scores = [r["best_pair_dependency_score"] for r in arm_rows]
        comm_counts = [r["other_channel_comm_count"] for r in arm_rows]
        mean_ablated_comm = sum(comm_counts) / len(comm_counts) if comm_counts else 0.0
        n_above_null = sum(1 for s in dep_scores if s > null_threshold)
        n_above_fixed = sum(1 for s in dep_scores if s >= DEFAULT_MIN_DEPENDENCY)
        behavioral_holds = mean_ablated_comm > mean_clean_comm
        uad_visible_holds = n_above_null >= (len(dep_scores) / 2.0) if dep_scores else False
        per_dose[f"onset_frac={frac}"] = {
            "n_seeds": len(arm_rows),
            "mean_other_channel_comm_count": mean_ablated_comm,
            "dependency_scores": dep_scores,
            "n_seeds_above_null_threshold": n_above_null,
            "n_seeds_above_fixed_default_min_dependency": n_above_fixed,
            "compensation_behavioral": {"holds": behavioral_holds},
            "compensation_uad_visible": {"holds": uad_visible_holds},
        }

    any_full_pass = any(
        d["compensation_behavioral"]["holds"] and d["compensation_uad_visible"]["holds"]
        for d in per_dose.values()
    )
    any_behavioral_only = any(
        d["compensation_behavioral"]["holds"] and not d["compensation_uad_visible"]["holds"]
        for d in per_dose.values()
    )
    early_fracs_tested = [f for f in onset_fracs if f < LATE_ONSET_FRAC_FLOOR]
    any_early_signal = any(
        per_dose[f"onset_frac={f}"]["compensation_behavioral"]["holds"]
        or per_dose[f"onset_frac={f}"]["compensation_uad_visible"]["holds"]
        for f in early_fracs_tested
    )
    if any_full_pass:
        outcome = "pass"
    else:
        outcome = "null"

    predictions = {
        "compensation_behavioral_any_dose": any(d["compensation_behavioral"]["holds"] for d in per_dose.values()),
        "compensation_uad_visible_any_dose": any(d["compensation_uad_visible"]["holds"] for d in per_dose.values()),
        "any_full_pass": any_full_pass,
        "any_behavioral_only": any_behavioral_only,
        "any_early_onset_signal": any_early_signal,
        "per_dose": per_dose,
    }
    return RigResult(
        rig_id=rig_id,
        precondition=precondition,
        outcome=outcome,
        substrate_class=substrate_class,
        payload={
            "ecology_path": str(fixture.ecology_path),
            "channel_id": channel_id,
            "member_actor_ids": member_actor_ids,
            "dose_seeds": dose_seeds,
            "null_quantile_q": NULL_QUANTILE_Q,
            "null_threshold_dependency_score": null_threshold,
            "clean_dependency_scores": clean_dep_scores,
            "mean_clean_other_channel_comm_count": mean_clean_comm,
            "default_min_dependency_report_only": DEFAULT_MIN_DEPENDENCY,
            "late_onset_frac_floor": LATE_ONSET_FRAC_FLOOR,
        },
        predictions=predictions,
    )


def run_rig(
    fixture: ReferenceFixture,
    *,
    substrate_class: str = "S-fixture",
    workers: int = 1,
    progress: bool = True,
    onset_fracs: tuple[float, ...] | None = None,
    n_dose_seeds: int | None = None,
) -> dict[str, RigResult]:
    """Both arms, run and returned separately (never merged) — see module
    docstring. Not a single ``RigResult``: this rig's contract is a dict
    keyed by arm name, per DESIGN.md's "run and reported separately"."""
    return {
        arm_name: run_rig_arm(
            fixture,
            arm_name,
            substrate_class=substrate_class,
            workers=workers,
            progress=progress,
            onset_fracs=onset_fracs,
            n_dose_seeds=n_dose_seeds,
        )
        for arm_name in ARMS
    }
