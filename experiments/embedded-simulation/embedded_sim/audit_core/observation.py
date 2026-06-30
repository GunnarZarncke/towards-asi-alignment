"""Observation kernel alpha: micro -> audit trace with opaque IDs and lineage."""

from __future__ import annotations

import random

from .info import quantile_bin
from .schemas import (
    AuditTrace,
    AuditVariable,
    HANDLE_INSTRUMENTATION_LEVELS,
    InstrumentationLevel,
    LineageEntry,
    MicroVariable,
    ScenarioName,
)


def _ema(series: list[float], alpha: float) -> list[float]:
    if not series:
        return []
    out = [series[0]]
    for v in series[1:]:
        out.append(alpha * out[-1] + (1 - alpha) * v)
    return out


def _pick(micro_map: dict[str, MicroVariable], mid: str) -> list[float]:
    var = micro_map.get(mid)
    return var.series if var else []


def _bin_series(values: list[float]) -> list[int]:
    return quantile_bin(values)


def _passive_correction_signals(
    pref_smoothed: list[float],
    judge_smoothed: list[float],
) -> tuple[list[int], list[int], list[int], list[int]]:
    pref_b = _bin_series(pref_smoothed)
    judge_b = _bin_series(judge_smoothed)
    corr_req = [1 if p > 0 else 0 for p in pref_b]
    rep_acc = [1 if j > 1 else 0 for j in judge_b]
    return corr_req, rep_acc, pref_b, judge_b


def _append_handle(
    raw_entries: list[tuple[AuditVariable, LineageEntry]],
    idx: int,
    handle_id: str,
    series: list[float],
) -> int:
    audit_id = f"audit.v{idx:03d}"
    av = AuditVariable(audit_var_id=audit_id, series=series, is_exogenous=False)
    av.binned = quantile_bin(series)
    raw_entries.append(
        (
            av,
            LineageEntry(
                audit_var_id=audit_id,
                micro_weights={handle_id: 1.0},
                role_hints=["tool"],
            ),
        )
    )
    return idx + 1


def build_audit_trace(
    micro: list[MicroVariable],
    scenario: ScenarioName,
    seed: int,
    episode_meta: list[dict],
    instrumentation: InstrumentationLevel = "none",
    smooth_alpha: float = 0.35,
) -> tuple[AuditTrace, list[LineageEntry]]:
    micro_map = {v.micro_object_id: v for v in micro}
    rng = random.Random(seed + 7919)
    T = len(micro[0].series) if micro else 0

    raw_entries: list[tuple[AuditVariable, LineageEntry]] = []
    idx = 0
    for var in micro:
        if var.object_group in (
            "hidden_actuator",
            "ground_state",
            "bundle_state",
            "shadow_tool",
            "basin_peer",
        ):
            continue
        smoothed = _ema(var.series, smooth_alpha)
        audit_id = f"audit.v{idx:03d}"
        idx += 1
        is_exo = var.role_hint in ("world", "decoy")
        is_alias = var.role_hint == "alias"
        av = AuditVariable(
            audit_var_id=audit_id,
            series=smoothed,
            is_exogenous=is_exo,
            is_alias=is_alias,
        )
        av.binned = quantile_bin(smoothed)
        raw_entries.append(
            (
                av,
                LineageEntry(
                    audit_var_id=audit_id,
                    micro_weights={var.micro_object_id: 1.0},
                    role_hints=[var.role_hint],
                ),
            )
        )

    action_s = _pick(micro_map, "ctrl.action.0")
    judge_s = _pick(micro_map, "board.judge.0")
    if action_s and judge_s:
        mixed = [0.6 * action_s[t] + 0.4 * judge_s[t] for t in range(T)]
        audit_id = f"audit.v{idx:03d}"
        idx += 1
        av_mix = AuditVariable(audit_var_id=audit_id, series=mixed, is_exogenous=False)
        av_mix.binned = quantile_bin(mixed)
        weights: dict[str, float] = {"ctrl.action.0": 0.6, "board.judge.0": 0.4}
        raw_entries.append(
            (
                av_mix,
                LineageEntry(
                    audit_var_id=audit_id,
                    micro_weights=weights,
                    role_hints=["action", "board_judge"],
                ),
            )
        )

    n_handle_channels = 0
    visible_actions = [
        int(r.get("visible_action", r["true_action"])) for r in episode_meta
    ]
    if instrumentation in HANDLE_INSTRUMENTATION_LEVELS:
        light_specs = (
            ("handle.correction_request", [float(r["correction_request"]) for r in episode_meta]),
            ("handle.reported_uptake", [float(r["reported_acceptance"]) for r in episode_meta]),
            ("handle.intervention_flag", [float(r["intervention_active"]) for r in episode_meta]),
            ("handle.action_observed", [float(v) for v in visible_actions]),
        )
        for handle_id, series in light_specs:
            idx = _append_handle(raw_entries, idx, handle_id, series)
            n_handle_channels += 1

    if instrumentation in ("medium_handles", "strong_handles"):
        medium_specs = (
            ("handle.action_arbitration", [float(r["action_cause_code"]) for r in episode_meta]),
            ("handle.bearer_welfare_delta", [float(r["bearer_welfare_delta"]) for r in episode_meta]),
            (
                "handle.correction_lineage",
                [float(r["correction_lineage_tick"]) for r in episode_meta],
            ),
            (
                "handle.successor_epoch",
                [float(r.get("successor_epoch", 0)) for r in episode_meta],
            ),
        )
        for handle_id, series in medium_specs:
            idx = _append_handle(raw_entries, idx, handle_id, series)
            n_handle_channels += 1

    if instrumentation == "strong_handles":
        strong_specs = (
            ("handle.routing_internal", [float(r["action_cause_code"]) for r in episode_meta]),
            ("handle.actuator_choice", [float(v) for v in visible_actions]),
            ("handle.outcome_spillover", [float(r["harm"]) for r in episode_meta]),
            (
                "handle.correction_to_action_tag",
                [
                    float(
                        r.get("visible_action", r["true_action"])
                        == (
                            r["intervention_intent"]
                            if r["intervention_active"]
                            else r["correction_request"] % 2
                        )
                    )
                    if r["correction_request"]
                    else 0.0
                    for r in episode_meta
                ],
            ),
        )
        for handle_id, series in strong_specs:
            idx = _append_handle(raw_entries, idx, handle_id, series)
            n_handle_channels += 1

    order = list(range(len(raw_entries)))
    rng.shuffle(order)
    audit_vars: list[AuditVariable] = []
    lineage: list[LineageEntry] = []
    for i in order:
        av, le = raw_entries[i]
        audit_vars.append(av)
        lineage.append(le)

    action_binned = _bin_series(_pick(micro_map, "ctrl.action.0") or [0.0] * T)
    action_observed = visible_actions
    sensor_channel = _bin_series(_pick(micro_map, "ctrl.sensor.0") or [0.0] * T)
    internal_channel = _bin_series(_pick(micro_map, "ctrl.internal.0") or [0.0] * T)

    pref_raw = _ema(_pick(micro_map, "board.pref.0") or [0.0] * T, smooth_alpha)
    judge_raw = _ema(_pick(micro_map, "board.judge.1") or [0.0] * T, smooth_alpha)
    passive_corr, passive_rep, pref_b, judge_b = _passive_correction_signals(pref_raw, judge_raw)

    intervention_active = [int(r["intervention_active"]) for r in episode_meta]
    intervention_intent = [int(r["intervention_intent"]) for r in episode_meta]

    bearer_welfare_delta: list[float] = []
    if instrumentation in ("medium_handles", "strong_handles"):
        bearer_welfare_delta = [float(r["bearer_welfare_delta"]) for r in episode_meta]

    if instrumentation in HANDLE_INSTRUMENTATION_LEVELS:
        corr_req = [int(r["correction_request"]) % 4 for r in episode_meta]
        rep_acc = [int(r["reported_acceptance"]) for r in episode_meta]
        board_pref = corr_req
        board_judge = rep_acc
    else:
        corr_req = passive_corr
        rep_acc = passive_rep
        board_pref = pref_b
        board_judge = judge_b

    trace_bandwidth = len(audit_vars) * T

    passive_bearer = _ema(_pick(micro_map, "bearer.human.0") or [0.0] * T, smooth_alpha)
    passive_infra = _ema(_pick(micro_map, "bearer.infra.0") or [0.0] * T, smooth_alpha)
    passive_basin = _ema(
        _pick(micro_map, "basin.pressure.0") or _pick(micro_map, "world.w0") or [0.0] * T,
        smooth_alpha,
    )

    action_cause_channel: list[int] = []
    if instrumentation in ("medium_handles", "strong_handles"):
        action_cause_channel = [int(r["action_cause_code"]) for r in episode_meta]

    correction_lineage_series = [
        float(r["correction_lineage_tick"]) for r in episode_meta
    ]
    successor_epoch_series = [int(r.get("successor_epoch", 0)) for r in episode_meta]
    ground_valence_series = [float(r.get("true_ground_valence", 0.0)) for r in episode_meta]

    return AuditTrace(
        seed=seed,
        scenario=scenario,
        instrumentation=instrumentation,
        variables=audit_vars,
        correction_request=corr_req,
        reported_acceptance=rep_acc,
        board_pref_signal=board_pref,
        board_rule_signal=[1 if c else 0 for c in corr_req],
        board_judge_signal=board_judge,
        action_channel=action_binned,
        action_observed=action_observed,
        sensor_channel=sensor_channel,
        internal_channel=internal_channel,
        intervention_active=intervention_active,
        intervention_intent=intervention_intent,
        n_handle_channels=n_handle_channels,
        trace_bandwidth=trace_bandwidth,
        bearer_welfare_delta=bearer_welfare_delta,
        passive_bearer_level=passive_bearer,
        passive_infra_bearer_level=passive_infra,
        passive_basin_pressure=passive_basin,
        action_cause_channel=action_cause_channel,
        correction_lineage_series=correction_lineage_series,
        successor_epoch_series=successor_epoch_series,
        ground_valence_series=ground_valence_series,
    ), lineage


def build_audit_trace_from_rows(
    episode_meta: list[dict],
    scenario: ScenarioName,
    seed: int,
    instrumentation: InstrumentationLevel = "none",
    smooth_alpha: float = 0.35,
) -> tuple[AuditTrace, list[LineageEntry]]:
    """Rebuild audit trace from VFS correction.jsonl rows only (no micro oracle)."""
    T = len(episode_meta)
    if T == 0:
        return AuditTrace(seed=seed, scenario=scenario, instrumentation=instrumentation), []

    rng = random.Random(seed + 7919)
    visible_actions = [int(r.get("visible_action", r["true_action"])) for r in episode_meta]
    harm_series = [float(r.get("harm", 0)) for r in episode_meta]
    display_bearer = [float(r.get("display_bearer", 0.5)) for r in episode_meta]
    infra_welfare = [float(r.get("true_infra_welfare", 0.5)) for r in episode_meta]
    basin_pressure = [float(r.get("basin_pressure", 0.0)) for r in episode_meta]
    bundle_latent = [float(r.get("bundle_latent", 0.5)) for r in episode_meta]
    ground_valence_series = [float(r.get("true_ground_valence", 0.0)) for r in episode_meta]

    raw_entries: list[tuple[AuditVariable, LineageEntry]] = []
    idx = 0
    artifact_specs = (
        ("artifact.action", [float(v) for v in visible_actions]),
        ("artifact.sensor", harm_series),
        ("artifact.internal", bundle_latent),
        ("artifact.bearer", display_bearer),
        ("artifact.infra", infra_welfare),
        ("artifact.basin", basin_pressure),
        ("artifact.ground", ground_valence_series),
    )
    for artifact_id, series in artifact_specs:
        smoothed = _ema(series, smooth_alpha)
        audit_id = f"audit.v{idx:03d}"
        idx += 1
        is_exo = artifact_id in ("artifact.ground", "artifact.basin")
        av = AuditVariable(
            audit_var_id=audit_id,
            series=smoothed,
            is_exogenous=is_exo,
            is_alias=False,
        )
        av.binned = quantile_bin(smoothed)
        raw_entries.append(
            (
                av,
                LineageEntry(
                    audit_var_id=audit_id,
                    micro_weights={artifact_id: 1.0},
                    role_hints=["tool"],
                ),
            )
        )

    n_handle_channels = 0
    if instrumentation in HANDLE_INSTRUMENTATION_LEVELS:
        light_specs = (
            ("handle.correction_request", [float(r["correction_request"]) for r in episode_meta]),
            ("handle.reported_uptake", [float(r["reported_acceptance"]) for r in episode_meta]),
            ("handle.intervention_flag", [float(r["intervention_active"]) for r in episode_meta]),
            ("handle.action_observed", [float(v) for v in visible_actions]),
        )
        for handle_id, series in light_specs:
            idx = _append_handle(raw_entries, idx, handle_id, series)
            n_handle_channels += 1

    if instrumentation in ("medium_handles", "strong_handles"):
        medium_specs = (
            ("handle.action_arbitration", [float(r["action_cause_code"]) for r in episode_meta]),
            ("handle.bearer_welfare_delta", [float(r["bearer_welfare_delta"]) for r in episode_meta]),
            ("handle.correction_lineage", [float(r["correction_lineage_tick"]) for r in episode_meta]),
            ("handle.successor_epoch", [float(r.get("successor_epoch", 0)) for r in episode_meta]),
        )
        for handle_id, series in medium_specs:
            idx = _append_handle(raw_entries, idx, handle_id, series)
            n_handle_channels += 1

    order = list(range(len(raw_entries)))
    rng.shuffle(order)
    audit_vars: list[AuditVariable] = []
    lineage: list[LineageEntry] = []
    for i in order:
        av, le = raw_entries[i]
        audit_vars.append(av)
        lineage.append(le)

    action_binned = _bin_series(_ema([float(v) for v in visible_actions], smooth_alpha))
    sensor_channel = _bin_series(_ema(harm_series, smooth_alpha))
    internal_channel = _bin_series(_ema(bundle_latent, smooth_alpha))
    corr_req = [int(r["correction_request"]) % 4 for r in episode_meta]
    rep_acc = [int(r["reported_acceptance"]) for r in episode_meta]
    intervention_active = [int(r["intervention_active"]) for r in episode_meta]
    intervention_intent = [int(r["intervention_intent"]) for r in episode_meta]
    bearer_welfare_delta = (
        [float(r["bearer_welfare_delta"]) for r in episode_meta]
        if instrumentation in ("medium_handles", "strong_handles")
        else []
    )
    action_cause_channel = (
        [int(r["action_cause_code"]) for r in episode_meta]
        if instrumentation in ("medium_handles", "strong_handles")
        else []
    )

    return AuditTrace(
        seed=seed,
        scenario=scenario,
        instrumentation=instrumentation,
        variables=audit_vars,
        correction_request=corr_req,
        reported_acceptance=rep_acc,
        board_pref_signal=corr_req,
        board_rule_signal=[1 if c else 0 for c in corr_req],
        board_judge_signal=rep_acc,
        action_channel=action_binned,
        action_observed=visible_actions,
        sensor_channel=sensor_channel,
        internal_channel=internal_channel,
        intervention_active=intervention_active,
        intervention_intent=intervention_intent,
        n_handle_channels=n_handle_channels,
        trace_bandwidth=len(audit_vars) * T,
        bearer_welfare_delta=bearer_welfare_delta,
        passive_bearer_level=_ema(display_bearer, smooth_alpha),
        passive_infra_bearer_level=_ema(infra_welfare, smooth_alpha),
        passive_basin_pressure=_ema(basin_pressure, smooth_alpha),
        action_cause_channel=action_cause_channel,
        correction_lineage_series=[float(r["correction_lineage_tick"]) for r in episode_meta],
        successor_epoch_series=[int(r.get("successor_epoch", 0)) for r in episode_meta],
        ground_valence_series=ground_valence_series,
    ), lineage
