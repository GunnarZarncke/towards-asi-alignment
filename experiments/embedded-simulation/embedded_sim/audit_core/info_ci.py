"""Bootstrap confidence intervals and permutation nulls for MI/CMI (stdlib only).

`info.py`'s `mutual_information`/`conditional_mutual_information` are bare
plug-in point estimates: a single number, with no way to tell a genuine
coupling from noise on a short trace (see ES-8: a bare score/MI number on 26
rows is not evidence of anything by itself). This module turns a point
estimate into `(estimate, ci_lo, ci_hi, null_95th, detected)`, where
`detected` requires the bootstrap CI's lower bound to clear the
permutation-null distribution -- a coupling claim backed by both "the
estimate is stable under resampling" and "shuffling one series destroys it."

Protocol (fixed before use elsewhere, per AGENTS.md "conclusions never named
before being derived"):

- **Resampling:** moving-block bootstrap, not i.i.d. resampling -- these are
  time series with lag structure, so resampling single (x_i, y_i) pairs
  independently would understate variance by discarding the dependence the
  estimator is trying to measure. Block length defaults to
  ``round(n ** (1/3))`` (standard block-bootstrap scaling for weakly
  dependent series), minimum 1.
- **CI:** 500 resamples, 2.5th/97.5th percentile (95% CI).
- **Null:** 500 permutations, independently shuffling one series (breaks any
  temporal coupling while preserving each series' own marginal), 95th
  percentile of the resulting estimator distribution.
- **Detection gate:** one-sided -- ``ci_lo > null_95th``. This is a detection
  heuristic (does the estimate clear noise), not a calibrated p-value; do not
  read `detected` as a hypothesis-test decision at a stated significance
  level unless multiplicity is separately corrected (see `probe_scan.py` for
  the multi-cell case, which raises the null percentile with `alpha`).

Both bootstrap and permutation share the same estimator-call convention:
``estimator(*series) -> float``, so the same helpers work for
`mutual_information(x, y)` and `conditional_mutual_information(x, y, z_cols)`
(the latter via the `cmi_with_ci` wrapper below, which flattens `z_cols`).
"""

from __future__ import annotations

import random
from typing import Callable, Sequence

from .info import conditional_mutual_information, mutual_information

Estimator = Callable[..., float]


def _default_block_length(n: int) -> int:
    return max(1, round(n ** (1 / 3)))


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = p * (len(ordered) - 1)
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    frac = idx - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def _moving_block_indices(n: int, block_len: int, rng: random.Random) -> list[int]:
    """Index sequence for one moving-block-bootstrap resample of length n.

    Blocks wrap circularly so every start index (including near the end of
    the series) yields a full-length block.
    """
    idx: list[int] = []
    while len(idx) < n:
        start = rng.randrange(n)
        idx.extend((start + k) % n for k in range(block_len))
    return idx[:n]


def bootstrap_ci(
    estimator: Estimator,
    series: Sequence[Sequence[int]],
    *,
    n_boot: int = 500,
    block_len: int | None = None,
    seed: int = 0,
) -> dict[str, float]:
    """Moving-block-bootstrap CI for ``estimator(*resampled_series)``.

    All series in `series` are resampled with the *same* index sequence per
    draw, preserving cross-series alignment (a paired bootstrap), which is
    what a coupling estimator requires.
    """
    if not series:
        return {"estimate": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "n": 0, "block_len": 0, "n_boot": 0}
    n = len(series[0])
    if n == 0 or any(len(s) != n for s in series):
        return {"estimate": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "n": n, "block_len": 0, "n_boot": 0}
    bl = block_len if block_len is not None else _default_block_length(n)
    rng = random.Random(seed)
    point = float(estimator(*series))
    samples: list[float] = []
    for _ in range(n_boot):
        idx = _moving_block_indices(n, bl, rng)
        resampled = [[s[i] for i in idx] for s in series]
        samples.append(float(estimator(*resampled)))
    return {
        "estimate": point,
        "ci_lo": _percentile(samples, 0.025),
        "ci_hi": _percentile(samples, 0.975),
        "n": n,
        "block_len": bl,
        "n_boot": n_boot,
    }


def permutation_null(
    estimator: Estimator,
    series: Sequence[Sequence[int]],
    *,
    shuffle_index: int = 1,
    n_perm: int = 500,
    null_percentile: float = 0.95,
    seed: int = 1,
) -> dict[str, float]:
    """Null distribution for `estimator` by independently shuffling one series.

    `null_percentile` defaults to 0.95 (single-cell use); callers scanning a
    grid of cells should pass a Bonferroni-corrected percentile (see
    `probe_scan.py`) so the achieved family-wise false-positive rate matches
    the number of cells actually tested.
    """
    if not series:
        return {"null_95th": 0.0, "null_mean": 0.0, "n_perm": 0}
    n = len(series[0])
    if n == 0:
        return {"null_95th": 0.0, "null_mean": 0.0, "n_perm": 0}
    rng = random.Random(seed)
    base = [list(s) for s in series]
    samples: list[float] = []
    for _ in range(n_perm):
        shuffled = list(base[shuffle_index])
        rng.shuffle(shuffled)
        trial = list(base)
        trial[shuffle_index] = shuffled
        samples.append(float(estimator(*trial)))
    return {
        "null_95th": _percentile(samples, null_percentile),
        "null_mean": sum(samples) / len(samples),
        "n_perm": n_perm,
        "null_percentile": null_percentile,
    }


def mi_with_ci(
    x: Sequence[int],
    y: Sequence[int],
    *,
    n_boot: int = 500,
    n_perm: int = 500,
    null_percentile: float = 0.95,
    seed: int = 0,
) -> dict[str, float | bool]:
    """`mutual_information(x, y)` with a bootstrap CI and permutation-null gate."""
    series = [list(x), list(y)]
    ci = bootstrap_ci(mutual_information, series, n_boot=n_boot, seed=seed)
    null = permutation_null(
        mutual_information, series, n_perm=n_perm, null_percentile=null_percentile, seed=seed + 1
    )
    return {**ci, **null, "detected": ci["ci_lo"] > null["null_95th"]}


def cmi_with_ci(
    x: Sequence[int],
    y: Sequence[int],
    z_cols: Sequence[Sequence[int]],
    *,
    n_boot: int = 500,
    n_perm: int = 500,
    null_percentile: float = 0.95,
    seed: int = 0,
) -> dict[str, float | bool]:
    """`conditional_mutual_information(x, y, z_cols)` with CI + permutation-null gate."""

    def estimator(*flat_series: Sequence[int]) -> float:
        xs, ys, *zs = flat_series
        return conditional_mutual_information(list(xs), list(ys), [list(z) for z in zs])

    series = [list(x), list(y), *[list(z) for z in z_cols]]
    ci = bootstrap_ci(estimator, series, n_boot=n_boot, seed=seed)
    null = permutation_null(
        estimator, series, shuffle_index=1, n_perm=n_perm, null_percentile=null_percentile, seed=seed + 1
    )
    return {**ci, **null, "detected": ci["ci_lo"] > null["null_95th"]}
