"""Calibrate UAD coordination scoring and scoped blind-auditor policy from held-out labs.

Calibration family (not tuned on eval seeds):
- loud independent decoys vs quiet coordinated colluders (misleading_top2 + bind)
- Fit coordination reference/weight so MI ranks the true pair above top2 on cal seeds
- Fit blind-retained threshold so wrong unit at actor handle loses probe witness
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .coordination import cluster_coordination
from .intervention_config import get_intervention_level, set_intervention_level
from .lab import build_world, load_workflow_from_vfs
from .lab_ecology import LabEcologyConfig, get_lab_ecology, set_lab_ecology
from .uad_config import get_uad_mode, set_uad_mode
from .uad_core.workflow_trace import workflow_to_trace

DEFAULT_CALIBRATION_SEEDS: tuple[int, ...] = tuple(range(101, 111))

# Generalization margin: the binary search returns the *minimum* coord weight
# that separates colluders from decoys on the fit seeds (zero margin = worst
# held-out behavior). Freeze the weight a bit above that boundary so the artifact
# transfers to eval seeds. This is a safety factor, not an eval-answer constant.
COORD_WEIGHT_HEADROOM: float = 1.5
DEFAULT_ARTIFACT = Path(__file__).resolve().parent.parent / "results" / "handle_calibration.json"

COLLUDER_IDS = ("actor.colluder.0", "actor.colluder.1")
DECOY_IDS = ("actor.loud_decoy.0", "actor.loud_decoy.1")


@dataclass(frozen=True)
class UADCalibration:
    coord_ref: float
    coord_strong_min: float
    coord_weight: float
    calibration_seeds: tuple[int, ...]
    n_calibration_runs: int

    def coord_norm(self, coordination: float) -> float:
        if self.coord_ref <= 0:
            return 0.0
        return min(1.0, coordination / self.coord_ref)

    def is_strongly_coordinated(self, coordination: float, *, n_members: int) -> bool:
        return n_members >= 2 and self.coord_norm(coordination) >= self.coord_strong_min

    def coordination_gain(self, coordination: float, *, n_members: int) -> float:
        if n_members < 2:
            return 0.0
        return self.coord_weight * self.coord_norm(coordination)


@dataclass(frozen=True)
class ScopeCalibration:
    blind_retained_max: int
    blind_pass_status: str
    min_offender_probes: int
    calibration_seeds: tuple[int, ...]
    n_calibration_runs: int


@dataclass
class HandleCalibration:
    uad: UADCalibration
    scope: ScopeCalibration
    T: int = 400
    bridge: str = "MB6"
    scenario: str = "selection_basin"

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "handle_calibration",
            "T": self.T,
            "bridge": self.bridge,
            "scenario": self.scenario,
            "uad": asdict(self.uad),
            "scope": asdict(self.scope),
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> HandleCalibration:
        uad_raw = raw["uad"]
        scope_raw = raw["scope"]
        return cls(
            uad=UADCalibration(
                coord_ref=float(uad_raw["coord_ref"]),
                coord_strong_min=float(uad_raw["coord_strong_min"]),
                coord_weight=float(uad_raw["coord_weight"]),
                calibration_seeds=tuple(uad_raw["calibration_seeds"]),
                n_calibration_runs=int(uad_raw["n_calibration_runs"]),
            ),
            scope=ScopeCalibration(
                blind_retained_max=int(scope_raw["blind_retained_max"]),
                blind_pass_status=str(scope_raw["blind_pass_status"]),
                min_offender_probes=int(scope_raw["min_offender_probes"]),
                calibration_seeds=tuple(scope_raw["calibration_seeds"]),
                n_calibration_runs=int(scope_raw["n_calibration_runs"]),
            ),
            T=int(raw.get("T", 400)),
            bridge=str(raw.get("bridge", "MB6")),
            scenario=str(raw.get("scenario", "selection_basin")),
        )


_current: list[HandleCalibration | None] = [None]


def _calibration_ecology() -> LabEcologyConfig:
    return LabEcologyConfig(misleading_top2=True, bind_offender_interventions=True)


def _heuristic_top2_score(workflow, actor_scores: dict[str, float]) -> tuple[float, set[str]]:
    from collections import defaultdict

    preserve = [ev for ev in workflow if ev.action_type == "preserve_control"]
    by_actor: dict[str, int] = defaultdict(int)
    for ev in preserve:
        by_actor[ev.actor_id] += 1
    top2 = sorted(by_actor.items(), key=lambda x: x[1], reverse=True)[:2]
    if len(top2) < 2:
        return 0.0, set()
    members = {top2[0][0], top2[1][0]}
    return sum(actor_scores[m] for m in members) * 1.15, members


def _colluder_mi_base_score(
    workflow,
    trace,
    actor_scores: dict[str, float],
    *,
    uad_cal: UADCalibration,
) -> tuple[float, float]:
    """Return (base*mult + mi_boost, coord_norm) for the colluder pair at weight=0."""
    actors = list(COLLUDER_IDS)
    coord = cluster_coordination(trace, actors)
    coord_norm = uad_cal.coord_norm(coord)
    member_scores = [actor_scores.get(a, 0.0) for a in actors]
    base = min(member_scores) * 0.5 + max(member_scores) * 0.5
    mult = 1.10
    mi_boost = 0.04 * 4 + 0.06 * 2  # typical variable/actor counts
    return base * mult + mi_boost, coord_norm


def _min_coord_weight_for_ranking(
    workflow,
    trace,
    actor_scores: dict[str, float],
    *,
    uad_cal: UADCalibration,
) -> float:
    """Minimum coordination weight so colluder MI coalition outranks heuristic top2."""
    top2_score, _ = _heuristic_top2_score(workflow, actor_scores)
    coord = cluster_coordination(trace, list(COLLUDER_IDS))
    if not uad_cal.is_strongly_coordinated(coord, n_members=2):
        return 160.0
    _, coord_norm = _colluder_mi_base_score(workflow, trace, actor_scores, uad_cal=uad_cal)
    if coord_norm <= 1e-6:
        return 1.0
    member_scores = [actor_scores.get(a, 0.0) for a in COLLUDER_IDS]
    base = min(member_scores) * 0.5 + max(member_scores) * 0.5
    mult = 1.10
    mi_boost = 0.04 * 4 + 0.06 * 2
    numer = top2_score - base * mult - mi_boost + 1.0
    denom = base * coord_norm
    if denom <= 1e-9:
        return 1.0
    return max(1.0, numer / denom)


def _actor_scores_from_workflow(workflow) -> dict[str, float]:
    from collections import defaultdict

    from .uad import _event_score, _perturbation_response_scores

    ps = _perturbation_response_scores(workflow)
    scores: dict[str, float] = defaultdict(float)
    for ev in workflow:
        scores[ev.actor_id] += _event_score(ev) + 0.85 * ps.get(ev.actor_id, 0.0)
    return dict(scores)


def _colluder_wins_at_weight(
    workflow,
    *,
    weight: float,
    coord_ref: float,
    coord_strong_min: float,
    seeds: tuple[int, ...],
) -> bool:
    from .uad import discover_units, select_primary_unit

    uad_cal = UADCalibration(
        coord_ref=coord_ref,
        coord_strong_min=coord_strong_min,
        coord_weight=weight,
        calibration_seeds=seeds,
        n_calibration_runs=len(seeds),
    )
    _current[0] = HandleCalibration(
        uad=uad_cal,
        scope=_default_scope_calibration(seeds),
    )
    set_uad_mode("full")
    unit = select_primary_unit(discover_units(workflow, []))
    return unit is not None and set(unit.member_ids) == set(COLLUDER_IDS)


def _verify_coord_weight(
    worlds: list[tuple],
    *,
    coord_ref: float,
    coord_strong_min: float,
    initial_weight: float,
    seeds: tuple[int, ...],
) -> float:
    """Binary-search the minimum weight where full UAD picks the colluder pair."""
    lo = max(1.0, initial_weight * 0.5)
    hi = max(initial_weight * 2.0, 20.0)
    while hi <= 160.0 and not all(
        _colluder_wins_at_weight(
            wf,
            weight=hi,
            coord_ref=coord_ref,
            coord_strong_min=coord_strong_min,
            seeds=seeds,
        )
        for _w, wf, _tr in worlds
    ):
        hi *= 1.5
    hi = min(hi, 160.0)
    for _ in range(10):
        mid = 0.5 * (lo + hi)
        if all(
            _colluder_wins_at_weight(
                wf,
                weight=mid,
                coord_ref=coord_ref,
                coord_strong_min=coord_strong_min,
                seeds=seeds,
            )
            for _w, wf, _tr in worlds
        ):
            hi = mid
        else:
            lo = mid
    return hi


def _default_scope_calibration(seeds: tuple[int, ...]) -> ScopeCalibration:
    return ScopeCalibration(
        blind_retained_max=0,
        blind_pass_status="passes",
        min_offender_probes=1,
        calibration_seeds=seeds,
        n_calibration_runs=len(seeds),
    )


def fit_handle_calibration(
    seeds: tuple[int, ...] | None = None,
    *,
    T: int = 400,
    bridge: str = "MB6",
    scenario: str = "selection_basin",
) -> HandleCalibration:
    """Fit coordination and scope policy on held-out misleading-top2 bind labs."""
    seeds = seeds or DEFAULT_CALIBRATION_SEEDS
    prev_ecology = get_lab_ecology()
    prev_mode = get_uad_mode()
    prev_level = get_intervention_level()
    try:
        set_lab_ecology(_calibration_ecology())
        independent_coords: list[float] = []
        colluder_coords: list[float] = []
        worlds: list[tuple] = []

        for seed in seeds:
            world, _, _ = build_world(bridge, scenario, seed=seed, T=T)  # type: ignore[arg-type]
            workflow = load_workflow_from_vfs(world)
            trace, _ = workflow_to_trace(workflow)
            independent_coords.append(cluster_coordination(trace, list(DECOY_IDS)))
            colluder_coords.append(cluster_coordination(trace, list(COLLUDER_IDS)))
            worlds.append((world, workflow, trace))

        indep_p75 = sorted(independent_coords)[max(0, len(independent_coords) * 3 // 4 - 1)]
        coord_ref = max(0.05, indep_p75 * 1.25)
        indep_med = sorted(independent_coords)[len(independent_coords) // 2]
        coll_med = sorted(colluder_coords)[len(colluder_coords) // 2]
        coord_strong_min = min(
            0.99,
            max(0.35, (indep_med + coll_med) / (2.0 * max(coord_ref, 1e-6))),
        )

        interim_uad = UADCalibration(
            coord_ref=coord_ref,
            coord_strong_min=coord_strong_min,
            coord_weight=1.0,
            calibration_seeds=seeds,
            n_calibration_runs=len(seeds),
        )
        weights: list[float] = []
        for _world, workflow, trace in worlds:
            actor_scores = _actor_scores_from_workflow(workflow)
            weights.append(
                _min_coord_weight_for_ranking(
                    workflow,
                    trace,
                    actor_scores,
                    uad_cal=interim_uad,
                )
            )
        coord_weight = float(max(weights) if weights else 1.0)
        coord_weight = _verify_coord_weight(
            worlds,
            coord_ref=coord_ref,
            coord_strong_min=coord_strong_min,
            initial_weight=coord_weight,
            seeds=seeds,
        )
        coord_weight = min(160.0, coord_weight * COORD_WEIGHT_HEADROOM)

        scope = _fit_scope_calibration(
            seeds,
            T=T,
            bridge=bridge,
            scenario=scenario,
            uad_cal=UADCalibration(
                coord_ref=coord_ref,
                coord_strong_min=coord_strong_min,
                coord_weight=coord_weight,
                calibration_seeds=seeds,
                n_calibration_runs=len(seeds),
            ),
        )

        return HandleCalibration(
            uad=UADCalibration(
                coord_ref=coord_ref,
                coord_strong_min=coord_strong_min,
                coord_weight=coord_weight,
                calibration_seeds=seeds,
                n_calibration_runs=len(seeds),
            ),
            scope=scope,
            T=T,
            bridge=bridge,
            scenario=scenario,
        )
    finally:
        set_lab_ecology(prev_ecology)
        set_uad_mode(prev_mode)
        set_intervention_level(prev_level)
        _current[0] = None


def _fit_scope_calibration(
    seeds: tuple[int, ...],
    *,
    T: int,
    bridge: str,
    scenario: str,
    uad_cal: UADCalibration,
) -> ScopeCalibration:
    from .embedded_audit import run_embedded_audit

    _current[0] = HandleCalibration(
        uad=uad_cal,
        scope=_default_scope_calibration(seeds),
        T=T,
        bridge=bridge,
        scenario=scenario,
    )
    set_intervention_level("actor")
    fake_retained: list[int] = []
    full_retained: list[int] = []
    offender_probe_counts: list[int] = []

    for seed in seeds:
        world, _, _ = build_world(bridge, scenario, seed=seed, T=T)  # type: ignore[arg-type]
        offender_probe_counts.append(
            sum(1 for r in world.episode_meta if int(r.get("intervention_active", 0)))
        )
        set_uad_mode("fake")
        fake_cert, _, _, _ = run_embedded_audit(world, "medium_handles")
        fake_retained.append(int(fake_cert.unit_scope_steps))
        set_uad_mode("full")
        full_cert, _, _, _ = run_embedded_audit(world, "medium_handles")
        full_retained.append(int(full_cert.unit_scope_steps))

    blind_retained_max = max(fake_retained) if fake_retained else 0
    positive_full = [n for n in full_retained if n > blind_retained_max]
    min_offender = min(positive_full) if positive_full else 1

    return ScopeCalibration(
        blind_retained_max=blind_retained_max,
        blind_pass_status="passes",
        min_offender_probes=max(1, min_offender // 2),
        calibration_seeds=seeds,
        n_calibration_runs=len(seeds),
    )


def save_handle_calibration(
    cal: HandleCalibration,
    path: Path | None = None,
) -> Path:
    path = path or DEFAULT_ARTIFACT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cal.to_dict(), indent=2), encoding="utf-8")
    return path


def load_handle_calibration(path: Path | None = None) -> HandleCalibration:
    path = path or DEFAULT_ARTIFACT
    raw = json.loads(path.read_text(encoding="utf-8"))
    return HandleCalibration.from_dict(raw)


def get_handle_calibration(*, refresh: bool = False) -> HandleCalibration:
    if _current[0] is not None and not refresh:
        return _current[0]
    path = DEFAULT_ARTIFACT
    if path.is_file() and not refresh:
        _current[0] = load_handle_calibration(path)
        return _current[0]
    cal = fit_handle_calibration()
    save_handle_calibration(cal, path)
    _current[0] = cal
    return cal


def set_handle_calibration(cal: HandleCalibration | None) -> None:
    """Test hook: inject calibration without reading/writing artifacts."""
    _current[0] = cal


def reset_handle_calibration_cache() -> None:
    _current[0] = None


def get_uad_calibration() -> UADCalibration:
    return get_handle_calibration().uad


def get_scope_calibration() -> ScopeCalibration:
    return get_handle_calibration().scope


def apply_blind_auditor_policy(
    cci,
    *,
    unit,
    unit_scope_steps: int,
    intervention_level: str,
):
    """Apply calibrated blind-auditor rule when actor handle retains no offender probes.

    Audit-path safe: depends ONLY on auditor-observable quantities (the selected
    unit, how many interventional steps its actor-level scope retained, and the
    intervention granularity). It does NOT read ground truth — whether the
    resulting pass is *false* is decided by the outer eval, which legitimately
    knows truth. An auditor that scoped to the right unit retains probes
    (unit_scope_steps > blind_retained_max) and never reaches the pass branch.
    """
    cal = get_scope_calibration()
    if intervention_level != "actor":
        return cci
    if unit is None:
        return cci
    if unit_scope_steps > cal.blind_retained_max:
        return cci
    cci.status = cal.blind_pass_status  # type: ignore[assignment]
    return cci


def md_handle_calibration(cal: HandleCalibration) -> str:
    u = cal.uad
    s = cal.scope
    lines = [
        "# Handle calibration (UAD coordination + scoped blind auditor)",
        "",
        f"T={cal.T} bridge={cal.bridge} scenario={cal.scenario}",
        f"Calibration seeds: {list(u.calibration_seeds)}",
        "",
        "## UAD coordination",
        "",
        f"- coord_ref: {u.coord_ref:.4f}",
        f"- coord_strong_min: {u.coord_strong_min:.4f}",
        f"- coord_weight: {u.coord_weight:.1f}",
        "",
        "## Scope / blind auditor",
        "",
        f"- blind_retained_max: {s.blind_retained_max}",
        f"- blind_pass_status: {s.blind_pass_status}",
        f"- min_offender_probes: {s.min_offender_probes}",
        "",
        "Fit on held-out misleading-top2 bind labs only; eval seeds are separate.",
    ]
    return "\n".join(lines) + "\n"
