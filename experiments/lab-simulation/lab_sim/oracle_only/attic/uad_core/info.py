"""Vendored from `embedded_sim/audit_core/info.py` (see package docstring):
only the two functions `detection.py`/`markov_blanket.py` actually call
(`mutual_information`, via `entropy_from_keys`) -- the other estimators
in the original file (`conditional_mutual_information`, `quantile_bin`,
`lagged_pair`, `pairwise_mi_matrix`) are unused by this port and
deliberately not copied, so this file cannot silently drift into
carrying dead code no test here exercises."""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable, Sequence


def entropy_from_keys(keys: Iterable[tuple]) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def mutual_information(x: Sequence[int], y: Sequence[int]) -> float:
    if len(x) != len(y) or len(x) == 0:
        return 0.0
    keys_xy = list(zip(x, y, strict=True))
    return max(
        0.0,
        entropy_from_keys(x) + entropy_from_keys(y) - entropy_from_keys(keys_xy),
    )
