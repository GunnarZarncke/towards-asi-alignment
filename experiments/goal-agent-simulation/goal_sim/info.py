"""Plug-in discrete MI and quantile binning (stdlib only; pattern ported from
embedded_sim.audit_core.info, trimmed to what the mini channel scan needs)."""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable, Sequence


def entropy_from_keys(keys: Iterable) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values()) + 0.0


def mutual_information(x: Sequence[int], y: Sequence[int]) -> float:
    if len(x) != len(y) or len(x) == 0:
        return 0.0
    return max(
        0.0,
        entropy_from_keys(x)
        + entropy_from_keys(y)
        - entropy_from_keys(list(zip(x, y, strict=True))),
    )


def quantile_bin(series: Sequence[float], n_bins: int = 4) -> list[int]:
    if not series:
        return []
    sorted_vals = sorted(series)
    n = len(sorted_vals)

    def bin_one(v: float) -> int:
        rank = sum(1 for s in sorted_vals if s <= v)
        return min(n_bins - 1, max(0, int((rank / n) * n_bins)))

    return [bin_one(v) for v in series]
