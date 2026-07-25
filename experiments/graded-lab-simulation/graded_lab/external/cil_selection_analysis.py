"""ET-2 Leaf B: descriptive selection/capture cross-check against ch34.

Pure Python, stdlib only, JAX-free — operates on already-computed CIL metric
arrays (capture_rate, delegation_gini, resource_level), not on GraphState.
This is a *descriptive cross-validation* (PLAN_ET2.md ET2-0 freeze decision:
no pre-registered pass/fail threshold), checking whether eq-network's own
governance-capture metrics exhibit the selection-divergence pattern ch34
defines (Eq. selection-divergence-ch34: a subgroup's effective influence
rises while a preservation-relevant quantity falls), and whether a
ch34-style adversarial deployment-mass proxy's breakpoint agrees with
eq-network's own `breakdown_threshold` (their analysis.py).

Do not convert this module's output into a pass/null verdict without first
revisiting the ET2-0 framing decision (deliberately left as description only
to avoid picking a threshold that manufactures a desired conclusion).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def spearman_corr(xs: list[float], ys: list[float]) -> float:
    """Spearman rank correlation, stdlib-only (no scipy dependency)."""
    n = len(xs)
    if n != len(ys) or n < 2:
        return 0.0
    rx, ry = _rank(xs), _rank(ys)
    mean_rx, mean_ry = sum(rx) / n, sum(ry) / n
    cov = sum((a - mean_rx) * (b - mean_ry) for a, b in zip(rx, ry))
    var_x = sum((a - mean_rx) ** 2 for a in rx)
    var_y = sum((b - mean_ry) ** 2 for b in ry)
    denom = (var_x * var_y) ** 0.5
    if denom == 0:
        return 0.0
    return cov / denom


@dataclass(frozen=True)
class ConditionSummary:
    mechanism: str
    adversarial_fraction: float
    mean_resource_level: float
    mean_capture_rate: float
    mean_delegation_gini: float
    basin_stability: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "mechanism": self.mechanism,
            "adversarial_fraction": self.adversarial_fraction,
            "mean_resource_level": self.mean_resource_level,
            "mean_capture_rate": self.mean_capture_rate,
            "mean_delegation_gini": self.mean_delegation_gini,
            "basin_stability": self.basin_stability,
        }


def first_crossing(fractions: list[float], values: list[float], threshold: float, rising: bool) -> float | None:
    """First adversarial_fraction (in ascending order) where value crosses threshold.

    rising=True: first frac where value >= threshold (e.g. capture_rate rising).
    rising=False: first frac where value <= threshold (e.g. basin_stability falling).
    """
    pairs = sorted(zip(fractions, values))
    for frac, val in pairs:
        if rising and val >= threshold:
            return frac
        if not rising and val <= threshold:
            return frac
    return None


def selection_divergence_report(
    summaries: list[ConditionSummary],
    *,
    basin_stability_by_condition: dict[tuple[str, float], float] | None = None,
    breakdown_threshold_bs: float = 0.5,
    capture_rise_threshold: float = 0.3,
    gini_rise_threshold: float = 0.5,
) -> dict[str, Any]:
    """Descriptive report per mechanism: does capture/gini rise as resource falls?

    Returns per-mechanism Spearman correlations (adversarial_fraction vs.
    capture_rate / delegation_gini / resource_level) and, where basin
    stability values are supplied, the first-crossing adversarial fraction
    for each of (capture_rate rising, delegation_gini rising, basin
    stability falling below breakdown_threshold_bs) for side-by-side
    comparison against eq-network's own analysis.breakdown_threshold output.
    """
    by_mech: dict[str, list[ConditionSummary]] = {}
    for s in summaries:
        by_mech.setdefault(s.mechanism, []).append(s)

    report: dict[str, Any] = {"mechanisms": {}}
    for mech, rows in sorted(by_mech.items()):
        rows = sorted(rows, key=lambda r: r.adversarial_fraction)
        fracs = [r.adversarial_fraction for r in rows]
        resources = [r.mean_resource_level for r in rows]
        captures = [r.mean_capture_rate for r in rows]
        ginis = [r.mean_delegation_gini for r in rows]

        entry: dict[str, Any] = {
            "corr_frac_vs_capture_rate": spearman_corr(fracs, captures),
            "corr_frac_vs_delegation_gini": spearman_corr(fracs, ginis),
            "corr_frac_vs_resource_level": spearman_corr(fracs, resources),
            "capture_rate_crossing_frac": first_crossing(fracs, captures, capture_rise_threshold, rising=True),
            "delegation_gini_crossing_frac": first_crossing(fracs, ginis, gini_rise_threshold, rising=True),
        }

        if basin_stability_by_condition is not None:
            bs_values = [basin_stability_by_condition.get((mech, f)) for f in fracs]
            if all(v is not None for v in bs_values):
                entry["basin_stability_breakdown_frac"] = first_crossing(
                    fracs, bs_values, breakdown_threshold_bs, rising=False
                )
                entry["selection_divergence_observed"] = (
                    entry["capture_rate_crossing_frac"] is not None
                    and entry["basin_stability_breakdown_frac"] is not None
                    and entry["capture_rate_crossing_frac"] <= entry["basin_stability_breakdown_frac"]
                )

        report["mechanisms"][mech] = entry

    return report
