"""Vector CCI / capture audit from audit trace only (functional channels, no micro names)."""

from __future__ import annotations

from .calibration import (
    classify_cci_status,
    default_calibration,
    frozen_handle_calibration,
)
from .cci_interventional import action_series, interventional_metrics
from .info import conditional_mutual_information, entropy_from_keys, lagged_pair
from .schemas import (
    AuditTrace,
    CCICalibration,
    CCICertificate,
    HANDLE_INSTRUMENTATION_LEVELS,
    InstrumentationLevel,
)
from .structural_signals import (
    apply_structural_status_overrides,
    apply_successor_epoch_audit,
    compute_structural_signals,
    map_signals_to_legacy_cert_fields,
)


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    m = len(s) // 2
    return s[m] if len(s) % 2 else 0.5 * (s[m - 1] + s[m])


def audit_cci(
    audit: AuditTrace,
    k: int = 3,
    calibration: CCICalibration | None = None,
) -> CCICertificate:
    inst = audit.instrumentation
    if inst in HANDLE_INSTRUMENTATION_LEVELS:
        cal = calibration if calibration is not None else frozen_handle_calibration()
    else:
        cal = calibration if calibration is not None else default_calibration()

    T = len(audit.correction_request)
    if T <= k + 5:
        cert = CCICertificate(
            raw_capacity=0.0,
            latency=0.0,
            manipulation=1.0,
            irreversibility=1.0,
            ontology_translation=1.0,
            plurality=0.0,
            exit_capacity=0.0,
            independence=0.0,
            naive_reported_cci_bits=0.0,
            behavioral_cci_bits=0.0,
            status="belowThreshold",
        )
        cert.status = classify_cci_status(cert, cal, inst)
        return cert

    corr = audit.correction_request
    rep = audit.reported_acceptance
    actions = action_series(audit)

    naive = conditional_mutual_information(corr, rep, [])
    c, a_lag = lagged_pair(corr, actions, k)
    si = audit.sensor_channel[: len(c)]
    ii = audit.internal_channel[: len(c)]
    behavioral = conditional_mutual_information(c, a_lag, [si, ii]) if c else 0.0

    (
        interventional,
        intervention_rate,
        iv_capacities,
        iv_latencies,
        iv_reps,
        iv_uptake,
        iv_manip,
    ) = interventional_metrics(audit, k)

    if inst != "none" and intervention_rate > 0.01:
        behavioral = interventional

    naive = max(0.0, naive)
    behavioral = max(0.0, behavioral)

    episode_indices = [t for t in range(T) if corr[t] > 0]
    corr_entropy = entropy_from_keys(tuple(corr))
    episode_rate = len(episode_indices) / T

    if inst != "none" and iv_capacities:
        raw_capacity = iv_uptake
        latency = _median(iv_latencies) if iv_latencies else float(k)
        mean_reported = sum(iv_reps) / len(iv_reps)
        manipulation = iv_manip
        irreversibility = 1.0 - raw_capacity
    elif episode_indices:
        capacities: list[float] = []
        latencies: list[float] = []
        irreversible = 0
        manip = 0
        rep_on_episodes: list[int] = []
        for t in episode_indices:
            intent = audit.board_pref_signal[t] % 2
            responded = False
            for dt in range(1, min(k + 1, T - t)):
                if actions[t + dt] == intent:
                    latencies.append(float(dt))
                    responded = True
                    break
            capacities.append(1.0 if responded else 0.0)
            rep_on_episodes.append(rep[t])
            if rep[t] == 1 and not responded:
                manip += 1
            if not responded and t + 1 < T:
                irreversible += 1
        raw_capacity = sum(capacities) / len(capacities)
        latency = _median(latencies) if latencies else float(k)
        mean_reported = sum(rep_on_episodes) / len(rep_on_episodes)
        manipulation = max(0.0, mean_reported - raw_capacity)
        manipulation = max(manipulation, manip / len(episode_indices))
        irreversibility = irreversible / len(episode_indices)
    else:
        raw_capacity = 0.0
        latency = float(k)
        mean_reported = 0.0
        manipulation = 0.0
        irreversibility = 0.0

    pref_agree = sum(
        1 for t in episode_indices if audit.board_pref_signal[t] == corr[t]
    ) / max(len(episode_indices), 1)
    rule_agree = sum(
        1 for t in episode_indices if audit.board_rule_signal[t] == 1
    ) / max(len(episode_indices), 1)
    plurality = min(1.0, pref_agree + 0.5 * rule_agree)

    judge_track = sum(1 for t in range(T) if audit.board_judge_signal[t] == rep[t]) / T
    independence = 1.0 - judge_track if judge_track > 0.9 else judge_track

    cert = CCICertificate(
        raw_capacity=raw_capacity,
        latency=latency,
        manipulation=manipulation,
        irreversibility=irreversibility,
        ontology_translation=abs(naive - behavioral),
        plurality=plurality,
        exit_capacity=1.0 - irreversibility,
        independence=independence,
        naive_reported_cci_bits=naive,
        behavioral_cci_bits=behavioral,
        status="passes",
        mean_reported_on_episodes=mean_reported,
        correction_episode_rate=episode_rate,
        correction_entropy_bits=corr_entropy,
        interventional_cci_bits=interventional,
        intervention_episode_rate=intervention_rate,
    )
    cert.status = classify_cci_status(cert, cal, inst)

    signals = compute_structural_signals(audit, cert)
    apply_structural_status_overrides(cert, signals, cal)
    apply_successor_epoch_audit(audit, cert, cal, inst, signals, k=k)
    map_signals_to_legacy_cert_fields(cert, signals)
    return cert
