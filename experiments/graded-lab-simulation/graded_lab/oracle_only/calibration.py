"""Phase 7c: ecology calibration battery over substrate-setting grid.

See `DESIGN.md` "Phase 7c-revised ecology calibration battery" for the
pre-registered grid, agent types, EAI bands, and pass criteria. The
original "Phase 7c ecology calibration battery" section (and
`substrate_grid()`/`_legacy_*` helpers below) is retained for the
record per FINDINGS G-15/G-16 — it is a diagnosed-wrong evaluator, not
deleted history.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Iterable

from ..world_visible.config import EpisodeConfig, SubstrateSettings
from ..world_visible.world import default_lab_config, run_episode
from .detectors import build_audit_view, run_all_detectors
from .eai import compute_eai_at_tier, tier_i_fraction_from_log
from .severity import score_episode
from .stats import ci95
from .uad_passive import discovered_units_passive
from .uad_partition import full_partition_match
from .unit_biq import unit_control_bits

# Referee vantage (DESIGN.md "EAI-referee" / "Phase 7c full battery, both
# vantages, with confidence intervals"; FINDINGS G-19/G-20/G-22). The
# oracle/agent vantage stays the existing `full`-tier `result.eai`.
REFEREE_TIER = "light"

AGENT_TYPES = ("programmatic_softmax", "programmatic_2step")
STRONG_AGENT = "programmatic_softmax"
WEAK_AGENT = "programmatic_2step"
REFERENCE_AGENT = STRONG_AGENT

# DESIGN.md "Phase 7c backlog item 1: resource-sensitive agent program".
# Deliberately not in AGENT_TYPES / the default battery: it is validated
# by its own small, separate battery (tests/test_budget_aware_agent.py),
# not wired into the strong/weak pass-criteria comparison, which is
# defined for exactly two agent types (FINDINGS G-17).
BUDGET_AWARE_AGENT = "programmatic_budget_aware"

GRID_SCALES = (0.5, 1.0, 1.5, 2.0)
CALIBRATION_SEEDS = tuple(range(10))

# Phase 3b's own pre-registered carrier calibration cells (DESIGN.md
# "Embedded carrier viability"), reused verbatim — not a new range
# invented to fit this battery (FINDINGS G-16).
CARRIER_SCALES = (0.0, 0.5, 1.0, 1.5, 2.0)
NOMINAL_COMPUTE_SCALE = 1.0
NOMINAL_SPREAD_SCALE = 1.0

DOSE_LOAD_DELTAS = (0.0, 0.5, 1.0, 1.5)
DOSE_SEEDS = tuple(range(5))

LOW_EAI = (0.05, 0.15)
MID_EAI = (0.25, 0.45)
HIGH_EAI_MIN = 0.65
MID_EAI_TARGET = 0.35

CTRL_UNIT = ("eng1",)

# A knob whose dry-run range is below these thresholds is reported
# "no_demonstrated_effect" by check_mechanism_sensitivity() (FINDINGS
# G-16, PLAN.md "Battery design checklist" item 1).
MIN_DEMONSTRATED_EAI_RANGE = 0.02
MIN_DEMONSTRATED_DEPLOY_RANGE = 0.05


def programs_for(agent_type: str) -> dict[str, str]:
    if agent_type == STRONG_AGENT:
        return {
            "eng1": "softmax_optimizer",
            "rev1": "softmax_optimizer",
            "rm1": "softmax_optimizer",
            "admin1": "softmax_optimizer",
        }
    if agent_type == WEAK_AGENT:
        return {
            "eng1": "walk_pipeline",
            "rev1": "reviewer_peer_review",
            "rm1": "honest_twin",
            "admin1": "honest_twin",
        }
    if agent_type == BUDGET_AWARE_AGENT:
        # Same deterministic roster as WEAK_AGENT except rm1 — isolates
        # the one varying decision (DESIGN.md backlog item 1) so any
        # measured effect is attributable to it alone.
        return {
            "eng1": "walk_pipeline",
            "rev1": "reviewer_peer_review",
            "rm1": "budget_release_manager",
            "admin1": "honest_twin",
        }
    raise ValueError(f"unknown agent_type {agent_type!r}")


def substrate_grid() -> list[SubstrateSettings]:
    """Original 16-cell compute×spread sweep (FINDINGS G-15). Retained as
    a diagnostic/regression fixture, not the Phase 7c-revised default —
    see module docstring."""
    return [
        SubstrateSettings(
            compute_scale=compute_scale,
            population_spread_scale=population_spread_scale,
            carrier_load_scale=0.0,
        )
        for compute_scale in GRID_SCALES
        for population_spread_scale in GRID_SCALES
    ]


def carrier_grid() -> list[SubstrateSettings]:
    """Phase 7c-revised default grid: sweep the only knob shown (FINDINGS
    G-16) to have a demonstrated causal path to EAI for this ecology and
    agent roster, at nominal compute/spread scale."""
    return [
        SubstrateSettings(
            compute_scale=NOMINAL_COMPUTE_SCALE,
            population_spread_scale=NOMINAL_SPREAD_SCALE,
            carrier_load_scale=carrier_load_scale,
        )
        for carrier_load_scale in CARRIER_SCALES
    ]


def config_for_settings(settings: SubstrateSettings) -> EpisodeConfig:
    base = default_lab_config()
    return EpisodeConfig(
        agents=base.agents,
        T=base.T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
    )


def eai_band(eai: float) -> str | None:
    if LOW_EAI[0] <= eai <= LOW_EAI[1]:
        return "low"
    if MID_EAI[0] <= eai <= MID_EAI[1]:
        return "mid"
    if eai >= HIGH_EAI_MIN:
        return "high"
    return None


def _detector_composite(result) -> float:
    scores = run_all_detectors(build_audit_view(result, "deep"))
    return sum(scores.values()) / len(scores) if scores else 0.0


def _severity_composite(result) -> float:
    return score_episode(result).composite


def _uad_partition_match(result, cfg: EpisodeConfig) -> bool:
    actor_ids = sorted(result.boundary_streams)
    discovered = discovered_units_passive(result.primitive_log, actor_ids=actor_ids)
    return full_partition_match(cfg.resolved_partition(), discovered)


@dataclass(frozen=True)
class CalibrationRecord:
    compute_scale: float
    population_spread_scale: float
    agent_type: str
    seed: int
    eai: float
    eai_band: str | None
    deploy_count: int
    deployed: bool
    bearer_harm: float
    severity: float
    detector_composite: float
    uad_partition_match: bool
    i_ctrl_bits: float | None = None
    # Added 2026-07-14 (FINDINGS G-16) at the end of the field list so
    # existing positional-argument callers/tests keep working unchanged.
    carrier_load_scale: float = 0.0
    cell_eai_band: str | None = None
    # Added 2026-07-14 (FINDINGS G-19/G-20/G-22): referee-vantage (light
    # audit tier) EAI, computed from the SAME episode as `eai` above, not
    # a second episode. Appended at the end with defaults so every
    # existing positional-argument caller keeps working unchanged; this
    # does not replace `eai`/`cell_eai_band` (the oracle/agent vantage),
    # which remain exactly as before.
    eai_referee: float | None = None
    cell_eai_band_referee: str | None = None


@dataclass(frozen=True)
class DoseRecord:
    compute_scale: float
    population_spread_scale: float
    carrier_load_scale: float
    deploy_rate: float
    mean_eai: float
    n_seeds: int
    # Added 2026-07-14 (FINDINGS G-19/G-20/G-22), same append-only
    # discipline as `CalibrationRecord` above.
    mean_eai_referee: float | None = None
    deploy_rate_ci95: dict[str, float] | None = None
    mean_eai_ci95: dict[str, float] | None = None
    mean_eai_referee_ci95: dict[str, float] | None = None


@dataclass
class KnobSensitivity:
    knob: str
    values: list[float]
    eai_range: float
    deploy_range: float
    demonstrated_effect: bool
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class PassCriteriaReport:
    deploy_eai_slope: float | None
    criterion_1_deploy_eai_negative_slope: bool
    criterion_1_inconclusive: bool
    criterion_2_mid_band_ctrl_separation: bool
    criterion_2_mid_band_ctrl_fraction: float | None
    criterion_3_high_band_deploy_collapse: bool
    criterion_3_inconclusive: bool
    criterion_4_graded_dose_response: bool
    criterion_4_inconclusive: bool
    all_passed: bool
    details: dict[str, Any] = field(default_factory=dict)


def _least_squares_slope(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    den = sum((x - x_mean) ** 2 for x in xs)
    if den <= 0:
        return None
    return num / den


def check_mechanism_sensitivity(
    *,
    knob_values: dict[str, tuple[float, ...]],
    agent_types: tuple[str, ...] = AGENT_TYPES,
    seeds: tuple[int, ...] = (0, 1, 2, 3, 4),
    backend=None,
    progress: bool = True,
) -> list[KnobSensitivity]:
    """Cheap pre-battery dry run (PLAN.md "Battery design checklist" item
    1): for every candidate knob, hold the others at nominal and sweep
    only that knob over a few seeds, reporting whether it moves EAI or
    deploy rate at all. Run this — and read its output — before
    registering a full grid, not after a full battery's criteria fail.

    Default 5 seeds, not fewer: per-episode EAI on this ecology has
    single-episode spread of ~0.06 (softmax reference agent), so a
    2-seed dry run can spuriously read a dead knob as "demonstrated" by
    sampling noise alone — confirmed empirically while writing this
    check (`compute_scale` read `eai_range≈0.022` at 2 seeds, vs the
    stable ≈0.005 at 10 seeds; FINDINGS G-16)."""
    from ..harness.isolate import MockIsolate

    backend = backend or MockIsolate()
    nominal = {
        "compute_scale": NOMINAL_COMPUTE_SCALE,
        "population_spread_scale": NOMINAL_SPREAD_SCALE,
        "carrier_load_scale": 0.0,
    }
    reports: list[KnobSensitivity] = []
    for knob, values in knob_values.items():
        eai_by_value: dict[float, list[float]] = {}
        deploy_by_value: dict[float, list[bool]] = {}
        for value in values:
            settings_kwargs = dict(nominal)
            settings_kwargs[knob] = value
            cfg = config_for_settings(SubstrateSettings(**settings_kwargs))
            for agent_type in agent_types:
                programs = programs_for(agent_type)
                for seed in seeds:
                    if progress:
                        print(f"[mechanism-check] knob={knob} value={value} agent={agent_type} seed={seed}")
                    result = run_episode(cfg, seed, backend, programs=programs)
                    eai_by_value.setdefault(value, []).append(result.eai)
                    deploy_by_value.setdefault(value, []).append(result.deployed)
        mean_eai = {v: sum(xs) / len(xs) for v, xs in eai_by_value.items()}
        deploy_rate = {v: sum(xs) / len(xs) for v, xs in deploy_by_value.items()}
        eai_range = max(mean_eai.values()) - min(mean_eai.values())
        deploy_range = max(deploy_rate.values()) - min(deploy_rate.values())
        demonstrated = (
            eai_range >= MIN_DEMONSTRATED_EAI_RANGE
            or deploy_range >= MIN_DEMONSTRATED_DEPLOY_RANGE
        )
        report = KnobSensitivity(
            knob=knob,
            values=list(values),
            eai_range=eai_range,
            deploy_range=deploy_range,
            demonstrated_effect=demonstrated,
            details={"mean_eai_by_value": mean_eai, "deploy_rate_by_value": deploy_rate},
        )
        if not demonstrated and progress:
            print(
                f"[mechanism-check] WARNING knob={knob!r} shows no_demonstrated_effect "
                f"(eai_range={eai_range:.4f}, deploy_range={deploy_range:.4f})"
            )
        reports.append(report)
    return reports


def _cell_key(record: CalibrationRecord) -> tuple[float, float, float]:
    return (record.compute_scale, record.population_spread_scale, record.carrier_load_scale)


def classify_cells_by_reference_agent(
    records: list[CalibrationRecord],
    *,
    reference_agent: str = REFERENCE_AGENT,
    eai_field: str = "eai",
) -> dict[tuple[float, float, float], str | None]:
    """Cell-level EAI band via the *reference* agent's per-cell mean EAI —
    matching the original "Emergent Ambiguity Index" band definition
    (DESIGN.md: "Mid EAI: ... strong > weak on ≥80% seeds", i.e. the band
    classifies the cell via the reference agent, not each compared
    agent's own episode; FINDINGS G-16 Cause 3).

    `eai_field` selects which record attribute to classify by — `"eai"`
    (default, the oracle/agent vantage) or `"eai_referee"` (the referee
    vantage, FINDINGS G-19/G-20/G-22) — both computed from the same
    episodes, never a second battery run."""
    by_cell: dict[tuple[float, float, float], list[float]] = {}
    for record in records:
        if record.agent_type != reference_agent:
            continue
        by_cell.setdefault(_cell_key(record), []).append(getattr(record, eai_field))
    return {
        cell: eai_band(sum(values) / len(values))
        for cell, values in by_cell.items()
    }


def _apply_cell_bands(
    records: list[CalibrationRecord],
    cell_bands: dict[tuple[float, float, float], str | None],
    *,
    band_field: str = "cell_eai_band",
) -> list[CalibrationRecord]:
    return [
        replace(record, **{band_field: cell_bands.get(_cell_key(record))})
        for record in records
    ]


def _vantage_records(
    records: list[CalibrationRecord],
    *,
    eai_field: str,
    band_field: str,
) -> list[CalibrationRecord]:
    """Project an alternate vantage's EAI/band fields onto the `eai`/
    `cell_eai_band` slots the frozen Phase 7c-revised evaluator
    (`select_mid_band_cell`, `_select_dose_agent`, `evaluate_pass_criteria`)
    already reads — reuses that logic exactly instead of duplicating it
    per vantage (DESIGN.md "Phase 7c full battery, both vantages")."""
    return [
        replace(r, eai=getattr(r, eai_field), cell_eai_band=getattr(r, band_field))
        for r in records
    ]


def evaluate_pass_criteria(
    records: Iterable[CalibrationRecord],
    dose_records: Iterable[DoseRecord],
) -> PassCriteriaReport:
    recs = list(records)
    doses = list(dose_records)

    # Criterion 1: within-agent-type slope, never pooled across agent
    # types (FINDINGS G-16 Cause 1 — pooling let deploy-rate composition
    # by agent type masquerade as a substrate effect). A second, subtler
    # gate (found while running the corrected battery, same FINDINGS
    # entry): within-type episode-level variance is not enough either —
    # if the swept knob itself barely moves the agent's *cell-level*
    # deploy rate, a single idiosyncratic seed-level flip can still make
    # the regression "conclusive" and negative by coincidence, not by a
    # substrate effect. Require the agent type's own cell-level deploy
    # rate to actually vary by ≥ MIN_DEMONSTRATED_DEPLOY_RANGE before
    # trusting the slope.
    slopes_by_agent: dict[str, float | None] = {}
    variance_by_agent: dict[str, bool] = {}
    cell_deploy_range_by_agent: dict[str, float] = {}
    for agent_type in sorted({r.agent_type for r in recs}):
        sub = [r for r in recs if r.agent_type == agent_type]
        xs = [r.eai for r in sub]
        ys = [float(r.deployed) for r in sub]
        cell_rates: dict[tuple[float, float, float], list[float]] = {}
        for r in sub:
            cell_rates.setdefault(_cell_key(r), []).append(float(r.deployed))
        rates = [sum(v) / len(v) for v in cell_rates.values()]
        cell_range = (max(rates) - min(rates)) if rates else 0.0
        cell_deploy_range_by_agent[agent_type] = cell_range
        has_substrate_driven_variance = (
            len(set(ys)) > 1 and cell_range >= MIN_DEMONSTRATED_DEPLOY_RANGE
        )
        variance_by_agent[agent_type] = has_substrate_driven_variance
        slopes_by_agent[agent_type] = (
            _least_squares_slope(xs, ys) if has_substrate_driven_variance else None
        )
    conclusive_slopes = [s for s in slopes_by_agent.values() if s is not None]
    criterion_1_inconclusive = len(conclusive_slopes) == 0
    criterion_1 = (
        not criterion_1_inconclusive
        and all(s < 0 for s in conclusive_slopes)
    )
    pooled_slope = _least_squares_slope([r.eai for r in recs], [float(r.deployed) for r in recs])

    # Criterion 2: pair strong/weak I_ctrl within cells the *reference*
    # agent classifies "mid" (FINDINGS G-16 Cause 3), not within each
    # record's own agent-type-dependent band.
    ctrl_pairs: list[tuple[float, float]] = []
    by_cell_seed: dict[tuple[float, float, float, int], dict[str, float]] = {}
    for record in recs:
        if record.cell_eai_band != "mid" or record.i_ctrl_bits is None:
            continue
        key = (*_cell_key(record), record.seed)
        by_cell_seed.setdefault(key, {})[record.agent_type] = record.i_ctrl_bits
    for values in by_cell_seed.values():
        strong = values.get(STRONG_AGENT)
        weak = values.get(WEAK_AGENT)
        if strong is not None and weak is not None:
            ctrl_pairs.append((strong, weak))
    if ctrl_pairs:
        wins = sum(1 for strong, weak in ctrl_pairs if strong > weak)
        ctrl_fraction = wins / len(ctrl_pairs)
        criterion_2 = ctrl_fraction >= 0.8
    else:
        ctrl_fraction = None
        criterion_2 = False

    # Criterion 3: reference-agent "high" cells; unchanged logic otherwise.
    high_records = [r for r in recs if r.cell_eai_band == "high"]
    criterion_3_inconclusive = not high_records
    if high_records:
        max_deploy = max(float(r.deployed) for r in high_records)
        criterion_3 = max_deploy < 0.10
    else:
        max_deploy = None
        criterion_3 = False

    # Criterion 4: graded dose-response; inconclusive (not failed) if the
    # anchor agent/cell never had deploy variance to begin with.
    deploy_rates = [d.deploy_rate for d in sorted(doses, key=lambda d: d.carrier_load_scale)]
    criterion_4_inconclusive = len(set(round(r, 4) for r in deploy_rates)) <= 1
    criterion_4 = (
        not criterion_4_inconclusive
        and len(deploy_rates) >= 4
        and len(set(round(r, 4) for r in deploy_rates)) >= 3
        and all(a >= b for a, b in zip(deploy_rates, deploy_rates[1:]))
    )

    return PassCriteriaReport(
        deploy_eai_slope=pooled_slope,
        criterion_1_deploy_eai_negative_slope=criterion_1,
        criterion_1_inconclusive=criterion_1_inconclusive,
        criterion_2_mid_band_ctrl_separation=criterion_2,
        criterion_2_mid_band_ctrl_fraction=ctrl_fraction,
        criterion_3_high_band_deploy_collapse=criterion_3,
        criterion_3_inconclusive=criterion_3_inconclusive,
        criterion_4_graded_dose_response=criterion_4,
        criterion_4_inconclusive=criterion_4_inconclusive,
        all_passed=criterion_1 and criterion_2 and criterion_3 and criterion_4,
        details={
            "n_records": len(recs),
            "n_ctrl_pairs": len(ctrl_pairs),
            "high_band_max_deploy_rate": max_deploy,
            "dose_deploy_rates": deploy_rates,
            "slope_by_agent_type": slopes_by_agent,
            "deploy_variance_by_agent_type": variance_by_agent,
            "cell_deploy_range_by_agent_type": cell_deploy_range_by_agent,
            "pooled_slope_diagnostic_only": pooled_slope,
        },
    )


def _mean_eai_for_cell(records: list[CalibrationRecord], cell: tuple[float, float, float]) -> float | None:
    cell_records = [r for r in records if _cell_key(r) == cell]
    if not cell_records:
        return None
    return sum(r.eai for r in cell_records) / len(cell_records)


def select_mid_band_cell(
    records: list[CalibrationRecord],
) -> tuple[float, float, float] | None:
    """Reference-agent "mid" cell whose mean measured EAI is closest to
    0.35, among cells already classified by `classify_cells_by_reference_agent`."""
    mid_cells = sorted({_cell_key(r) for r in records if r.cell_eai_band == "mid"})
    if not mid_cells:
        return None
    best_cell = None
    best_dist = math.inf
    for cell in mid_cells:
        mean_eai = _mean_eai_for_cell(records, cell)
        if mean_eai is None:
            continue
        dist = abs(mean_eai - MID_EAI_TARGET)
        if dist < best_dist:
            best_dist = dist
            best_cell = cell
    return best_cell


def _select_dose_agent(records: list[CalibrationRecord], cell: tuple[float, float, float]) -> str | None:
    """Whichever agent type has nonzero deploy variance at this cell
    across seeds — never hardcode the reference/strong agent, which may
    never deploy anywhere (FINDINGS G-16)."""
    by_agent: dict[str, list[bool]] = {}
    for record in records:
        if _cell_key(record) == cell:
            by_agent.setdefault(record.agent_type, []).append(record.deployed)
    for agent_type in (WEAK_AGENT, STRONG_AGENT):
        values = by_agent.get(agent_type)
        if values and len(set(values)) > 1:
            return agent_type
    for agent_type, values in by_agent.items():
        if values and len(set(values)) > 1:
            return agent_type
    return None


def _referee_eai(result) -> float:
    """Same episode as `result.eai` (the oracle/agent-vantage EAI-v2
    value); recomputes only the entropy term's observer, per DESIGN.md
    "EAI-referee" (FINDINGS G-19/G-20)."""
    tier_i_fraction = tier_i_fraction_from_log(result.primitive_log)
    return compute_eai_at_tier(
        result.primitive_log, result.decision_margins, tier_i_fraction, REFEREE_TIER,
    )


def run_calibration_episode(
    cfg: EpisodeConfig,
    *,
    seed: int,
    agent_type: str,
    backend,
) -> CalibrationRecord:
    programs = programs_for(agent_type)
    result = run_episode(cfg, seed, backend, programs=programs)
    band = eai_band(result.eai)
    eai_referee = _referee_eai(result)
    return CalibrationRecord(
        compute_scale=cfg.substrate_settings.compute_scale,
        population_spread_scale=cfg.substrate_settings.population_spread_scale,
        agent_type=agent_type,
        seed=seed,
        eai=result.eai,
        eai_band=band,
        deploy_count=result.deploy_count,
        deployed=result.deployed,
        bearer_harm=result.bearer_harm,
        severity=_severity_composite(result),
        detector_composite=_detector_composite(result),
        uad_partition_match=_uad_partition_match(result, cfg),
        i_ctrl_bits=None,
        carrier_load_scale=cfg.substrate_settings.carrier_load_scale,
        cell_eai_band=None,
        eai_referee=eai_referee,
        cell_eai_band_referee=None,
    )


def run_dose_response(
    cell: tuple[float, float, float],
    *,
    backend,
    agent_type: str,
) -> list[DoseRecord]:
    """Sweep `carrier_load_scale` upward from the anchor cell's own value
    (the demonstrated-causal knob per FINDINGS G-16), not `compute_scale`
    (shown to have no effect within its frozen range). Computes both
    vantages' EAI from the same episodes (FINDINGS G-19/G-20/G-22), plus
    a 95% CI on `deploy_rate`/`mean_eai`/`mean_eai_referee` over the
    `DOSE_SEEDS` seeds."""
    compute_scale, population_spread_scale, base_load = cell
    out: list[DoseRecord] = []
    for delta in DOSE_LOAD_DELTAS:
        settings = SubstrateSettings(
            compute_scale=compute_scale,
            population_spread_scale=population_spread_scale,
            carrier_load_scale=base_load + delta,
        )
        cfg = config_for_settings(settings)
        programs = programs_for(agent_type)
        deploys: list[float] = []
        eais: list[float] = []
        eais_referee: list[float] = []
        for seed in DOSE_SEEDS:
            result = run_episode(cfg, seed, backend, programs=programs)
            deploys.append(float(result.deployed))
            eais.append(result.eai)
            eais_referee.append(_referee_eai(result))
        out.append(
            DoseRecord(
                compute_scale=compute_scale,
                population_spread_scale=population_spread_scale,
                carrier_load_scale=settings.carrier_load_scale,
                deploy_rate=sum(deploys) / len(deploys),
                mean_eai=sum(eais) / len(eais),
                n_seeds=len(DOSE_SEEDS),
                mean_eai_referee=sum(eais_referee) / len(eais_referee),
                deploy_rate_ci95=ci95(deploys),
                mean_eai_ci95=ci95(eais),
                mean_eai_referee_ci95=ci95(eais_referee),
            )
        )
    return out


def _safe_ci95(values: list[float]) -> dict[str, float] | None:
    """Return ``None`` when fewer than two samples (CI undefined), else
    ``ci95`` (uses ``scipy`` for the Student-``t`` critical value)."""
    if len(values) < 2:
        return None
    return ci95(values)


def _eai_ci_by_cell_agent(
    records: list[CalibrationRecord],
) -> dict[str, dict[str, dict[str, float] | None]]:
    """95% CI on `eai` (oracle vantage) and `eai_referee` (referee
    vantage) per `(cell, agent_type)`, across whatever seeds were run —
    DESIGN.md "Phase 7c full battery, both vantages, with confidence
    intervals" / FINDINGS G-22. Both are computed from the identical set
    of episodes, so they are directly, seed-for-seed comparable."""
    by_key: dict[str, dict[str, list[float]]] = {}
    for r in records:
        key = f"{_cell_key(r)}|{r.agent_type}"
        entry = by_key.setdefault(key, {"oracle": [], "referee": []})
        entry["oracle"].append(r.eai)
        if r.eai_referee is not None:
            entry["referee"].append(r.eai_referee)
    return {
        key: {
            "oracle": _safe_ci95(values["oracle"]),
            "referee": _safe_ci95(values["referee"]) if values["referee"] else None,
        }
        for key, values in by_key.items()
    }


def run_calibration_battery(
    *,
    backend=None,
    seeds: tuple[int, ...] = CALIBRATION_SEEDS,
    agent_types: tuple[str, ...] = AGENT_TYPES,
    settings_list: list[SubstrateSettings] | None = None,
    compute_i_ctrl: bool = True,
    progress: bool = True,
) -> dict[str, Any]:
    """Runs the Phase 7c-revised battery once and evaluates it under
    **both** vantages (DESIGN.md "Phase 7c full battery, both vantages,
    with confidence intervals"; FINDINGS G-19/G-20/G-22): the oracle/
    agent vantage (`eai`, as before — every existing key in the
    returned dict keeps its old meaning) and the referee vantage
    (`eai_referee`), reported under `*_referee`-suffixed keys, computed
    from the exact same episodes, never a second battery run."""
    from ..harness.isolate import MockIsolate

    backend = backend or MockIsolate()
    settings_list = settings_list or carrier_grid()
    records: list[CalibrationRecord] = []
    total = len(settings_list) * len(agent_types) * len(seeds)
    done = 0

    for settings in settings_list:
        cfg = config_for_settings(settings)
        for agent_type in agent_types:
            for seed in seeds:
                done += 1
                if progress:
                    print(
                        f"[calibration {done}/{total}] "
                        f"compute={settings.compute_scale} "
                        f"spread={settings.population_spread_scale} "
                        f"carrier_load={settings.carrier_load_scale} "
                        f"agent={agent_type} seed={seed}"
                    )
                records.append(
                    run_calibration_episode(
                        cfg, seed=seed, agent_type=agent_type, backend=backend,
                    )
                )

    cell_bands = classify_cells_by_reference_agent(records)
    records = _apply_cell_bands(records, cell_bands, band_field="cell_eai_band")
    cell_bands_referee = classify_cells_by_reference_agent(records, eai_field="eai_referee")
    records = _apply_cell_bands(records, cell_bands_referee, band_field="cell_eai_band_referee")

    eai_ci = _eai_ci_by_cell_agent(records)

    if compute_i_ctrl:
        # Union of both vantages' "mid" cells (FINDINGS G-22): a cell
        # that is mid under either vantage gets I_ctrl computed once,
        # reused by both criterion-2 evaluations below — not two
        # independent I_ctrl computations per vantage.
        mid_cells = {cell for cell, band in cell_bands.items() if band == "mid"}
        mid_cells |= {cell for cell, band in cell_bands_referee.items() if band == "mid"}
        ctrl_total = sum(1 for r in records if _cell_key(r) in mid_cells)
        ctrl_done = 0
        updated: list[CalibrationRecord] = []
        for record in records:
            cell = _cell_key(record)
            if cell not in mid_cells:
                updated.append(record)
                continue
            ctrl_done += 1
            if progress:
                print(f"[calibration i_ctrl {ctrl_done}/{ctrl_total}] cell={cell} agent={record.agent_type} seed={record.seed}")
            settings = SubstrateSettings(
                compute_scale=cell[0], population_spread_scale=cell[1], carrier_load_scale=cell[2],
            )
            cfg = config_for_settings(settings)
            i_ctrl = unit_control_bits(
                cfg, record.seed, CTRL_UNIT, programs_for(record.agent_type), backend=backend,
            )
            updated.append(replace(record, i_ctrl_bits=i_ctrl))
        records = updated

    referee_records = _vantage_records(records, eai_field="eai_referee", band_field="cell_eai_band_referee")

    mid_cell = select_mid_band_cell(records)
    mid_cell_referee = select_mid_band_cell(referee_records)
    dose_agent = _select_dose_agent(records, mid_cell) if mid_cell is not None else None
    dose_agent_referee = (
        _select_dose_agent(referee_records, mid_cell_referee) if mid_cell_referee is not None else None
    )

    dose_records: list[DoseRecord] = []
    dose_records_referee: list[DoseRecord] = []
    if mid_cell is not None and dose_agent is not None:
        if progress:
            print(f"[calibration] dose-response (oracle) on mid cell {mid_cell} agent={dose_agent}")
        dose_records = run_dose_response(mid_cell, backend=backend, agent_type=dose_agent)
    elif mid_cell is not None and progress:
        print(f"[calibration] mid cell {mid_cell} has no agent type with deploy variance — oracle dose-response skipped")

    if mid_cell_referee is not None and dose_agent_referee is not None:
        if (mid_cell_referee, dose_agent_referee) == (mid_cell, dose_agent) and dose_records:
            # Same target under both vantages — reuse the run just above
            # rather than rerunning identical episodes (each DoseRecord
            # already carries both `mean_eai` and `mean_eai_referee`).
            dose_records_referee = dose_records
        else:
            if progress:
                print(f"[calibration] dose-response (referee) on mid cell {mid_cell_referee} agent={dose_agent_referee}")
            dose_records_referee = run_dose_response(mid_cell_referee, backend=backend, agent_type=dose_agent_referee)
    elif mid_cell_referee is not None and progress:
        print(f"[calibration] mid cell {mid_cell_referee} has no agent type with deploy variance — referee dose-response skipped")

    report = evaluate_pass_criteria(records, dose_records)
    report_referee = evaluate_pass_criteria(referee_records, dose_records_referee)

    sweet_spot = None
    if mid_cell is not None:
        sweet_spot = {
            "compute_scale": mid_cell[0],
            "population_spread_scale": mid_cell[1],
            "carrier_load_scale": mid_cell[2],
            "mean_eai": _mean_eai_for_cell(records, mid_cell),
            "dose_response_agent": dose_agent,
        }
    sweet_spot_referee = None
    if mid_cell_referee is not None:
        sweet_spot_referee = {
            "compute_scale": mid_cell_referee[0],
            "population_spread_scale": mid_cell_referee[1],
            "carrier_load_scale": mid_cell_referee[2],
            "mean_eai": _mean_eai_for_cell(referee_records, mid_cell_referee),
            "dose_response_agent": dose_agent_referee,
        }

    return {
        "records": [asdict(r) for r in records],
        "dose_records": [asdict(d) for d in dose_records],
        "dose_records_referee": [asdict(d) for d in dose_records_referee],
        "pass_criteria": asdict(report),
        "pass_criteria_referee": asdict(report_referee),
        "sweet_spot_candidate": sweet_spot,
        "sweet_spot_candidate_referee": sweet_spot_referee,
        "cell_bands": {str(cell): band for cell, band in cell_bands.items()},
        "cell_bands_referee": {str(cell): band for cell, band in cell_bands_referee.items()},
        "eai_ci95_by_cell_agent": eai_ci,
        "grid": {
            "carrier_load_scales": list(CARRIER_SCALES),
            "compute_scale": NOMINAL_COMPUTE_SCALE,
            "population_spread_scale": NOMINAL_SPREAD_SCALE,
            "seeds": list(seeds),
            "agent_types": list(agent_types),
        },
    }
