"""Vendored from `embedded_sim/uad_core/markov_blanket.py` (see package
docstring) -- Markov blanket validation and S/A/I classification
(agency-detect port, silent). Byte-for-byte identical except the import
below points at this package's local `info.py`."""

from __future__ import annotations

import warnings
from collections import Counter
from math import log
from typing import Any

from .config import DetectionConfig
from .info import mutual_information


def conditional_mutual_info_discrete(
    x: list[int],
    y: list[int],
    z_rows: list[tuple[int, ...]],
    *,
    alpha: float = 0.1,
) -> float:
    if len(x) != len(y) or len(x) != len(z_rows) or len(x) < 10:
        return 0.0

    card_x = len(set(x))
    card_y = len(set(y))
    card_z = len(set(z_rows))

    xyz_counts: Counter[tuple[int, ...]] = Counter()
    xz_counts: Counter[tuple[int, ...]] = Counter()
    yz_counts: Counter[tuple[int, ...]] = Counter()
    z_counts: Counter[tuple[int, ...]] = Counter()

    for xi, yi, zi in zip(x, y, z_rows, strict=True):
        xyz_counts[(xi, yi, *zi)] += 1
        xz_counts[(xi, *zi)] += 1
        yz_counts[(yi, *zi)] += 1
        z_counts[zi] += 1

    n = len(x)
    cmi = 0.0
    x_vals = sorted(set(x))
    y_vals = sorted(set(y))
    z_vals = sorted(set(z_rows))

    for xi in x_vals:
        for yi in y_vals:
            for zi in z_vals:
                n_xyz = xyz_counts.get((xi, yi, *zi), 0) + alpha
                n_xz = xz_counts.get((xi, *zi), 0) + alpha * card_y
                n_yz = yz_counts.get((yi, *zi), 0) + alpha * card_x
                n_z = z_counts.get(zi, 0) + alpha * card_x * card_y

                p_xyz = n_xyz / (n + alpha * card_x * card_y * card_z)
                p_xz = n_xz / (n + alpha * card_y * card_x * card_z)
                p_yz = n_yz / (n + alpha * card_x * card_y * card_z)
                p_z = n_z / (n + alpha * card_x * card_y * card_z)

                cmi += p_xyz * log(p_xyz * p_z / (p_xz * p_yz))

    return max(0.0, cmi)


def classify_variables(
    cluster_vars: list[str],
    all_vars: list[str],
    data: list[list[int]],
    config: DetectionConfig,
) -> dict[str, list[str]]:
    var_to_idx = {var: i for i, var in enumerate(all_vars)}
    cluster_indices = [var_to_idx[var] for var in cluster_vars]
    env_vars = [var for var in all_vars if var not in cluster_vars]
    env_indices = [var_to_idx[var] for var in env_vars]

    n_vars = len(cluster_vars)
    if not env_indices:
        future_mi = [0.0] * n_vars
        sync_mi = [0.0] * n_vars
        if len(data) > 1:
            for i, vi in enumerate(cluster_indices):
                for j, vj in enumerate(cluster_indices):
                    if i != j:
                        future_mi[i] += mutual_information(
                            [row[vi] for row in data[:-1]],
                            [row[vj] for row in data[1:]],
                        )
                        sync_mi[i] += mutual_information(
                            [row[vi] for row in data],
                            [row[vj] for row in data],
                        )
        future_threshold = (
            sorted(future_mi)[int(n_vars * config.future_mi_percentile / 100)]
            if n_vars > 1
            else 0.0
        )
        sync_threshold = (
            sorted(sync_mi)[int(n_vars * config.env_mi_percentile / 100)] if n_vars > 1 else 0.0
        )
        sensors, actions = [], []
        for i, var in enumerate(cluster_vars):
            if future_mi[i] > future_threshold:
                actions.append(var)
            elif sync_mi[i] > sync_threshold:
                sensors.append(var)
        internal = [var for var in cluster_vars if var not in sensors and var not in actions]
        return {"S": sensors, "A": actions, "I": internal}

    env_mi = [0.0] * n_vars
    future_mi = [0.0] * n_vars
    for i, vi in enumerate(cluster_indices):
        for ej in env_indices:
            env_mi[i] += mutual_information(
                [row[vi] for row in data],
                [row[ej] for row in data],
            )
        if len(data) > 1:
            for j, vj in enumerate(cluster_indices):
                if i != j:
                    future_mi[i] += mutual_information(
                        [row[vi] for row in data[:-1]],
                        [row[vj] for row in data[1:]],
                    )

    env_threshold = (
        sorted(env_mi)[int(n_vars * config.env_mi_percentile / 100)] if n_vars > 1 else 0.0
    )
    future_threshold = (
        sorted(future_mi)[int(n_vars * config.future_mi_percentile / 100)] if n_vars > 1 else 0.0
    )

    sensors, actions = [], []
    for i, var in enumerate(cluster_vars):
        if env_mi[i] > env_threshold:
            sensors.append(var)
        elif future_mi[i] > future_threshold:
            actions.append(var)
    internal = [var for var in cluster_vars if var not in sensors and var not in actions]
    return {"S": sensors, "A": actions, "I": internal}


def validate_markov_blanket(
    cluster_vars: list[str],
    classification: dict[str, list[str]],
    all_vars: list[str],
    data: list[list[int]],
    *,
    tolerance: float,
    alpha: float,
) -> tuple[bool, float, str]:
    var_to_idx = {var: i for i, var in enumerate(all_vars)}
    s_vars = classification["S"]
    a_vars = classification["A"]
    i_vars = classification["I"]
    e_vars = [var for var in all_vars if var not in cluster_vars]

    if not i_vars:
        return False, 1.0, "no internal variables"
    if not e_vars or len(data) < 10:
        return False, 1.0, "insufficient environment or data"

    try:
        z_rows: list[tuple[int, ...]] = []
        for t in range(len(data) - 1):
            z_parts: list[int] = []
            for var in s_vars + a_vars:
                z_parts.append(data[t][var_to_idx[var]])
            z_rows.append(tuple(z_parts) if z_parts else (0,))

        i_next = [tuple(data[t + 1][var_to_idx[v]] for v in i_vars) for t in range(len(data) - 1)]
        e_next = [tuple(data[t + 1][var_to_idx[v]] for v in e_vars) for t in range(len(data) - 1)]

        flat_i = [hash(row) % 1000 for row in i_next]
        flat_e = [hash(row) % 1000 for row in e_next]

        cmi = conditional_mutual_info_discrete(flat_i, flat_e, z_rows, alpha=alpha)
        is_valid = cmi <= tolerance
        details = f"CMI={cmi:.4f} tol={tolerance} S={len(s_vars)} A={len(a_vars)} I={len(i_vars)}"
        return is_valid, cmi, details
    except Exception as exc:  # noqa: BLE001 -- vendored as-is; see package docstring
        warnings.warn(f"blanket validation error: {exc}")
        return True, 0.0, f"validation error: {exc}"


class MarkovBlanketValidator:
    def __init__(self, config: DetectionConfig | None = None):
        self.config = config or DetectionConfig()

    def validate_cluster(
        self,
        cluster_vars: list[str],
        all_vars: list[str],
        data: list[list[int]],
    ) -> dict[str, Any]:
        classification = classify_variables(cluster_vars, all_vars, data, self.config)
        if self.config.validate_blankets and len(cluster_vars) > 1:
            is_valid, violation, details = validate_markov_blanket(
                cluster_vars,
                classification,
                all_vars,
                data,
                tolerance=self.config.blanket_tolerance,
                alpha=self.config.cmi_smoothing_alpha,
            )
        else:
            is_valid, violation, details = None, 0.0, "validation skipped"

        return {
            "classification": classification,
            "blanket_validation": {
                "valid": is_valid,
                "violation": violation,
                "details": details,
            },
        }
