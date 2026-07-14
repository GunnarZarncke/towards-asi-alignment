"""Pre-registered lag/direction scan for real vs. spurious probe couplings.

Companion to `calibrate_trace_biq.py` (which asks "is the Lean
pattern-diversity *score* calibrated to Shannon MI?" -- answer: no, ES-8) and
`embedded_sim/audit_core/info_ci.py` (which gives MI/CMI a bootstrap CI and a
permutation null). This script asks a different, protocol-level question:
scanning a *grid* of (pair, direction, lag) cells -- not just the one
direction/lag the worked instance's own protocol measures -- does the
CI+null gate rediscover the fixture's real coupling, and does it stay quiet
everywhere it should?

Protocol (fixed before computing any numbers, per AGENTS.md "conclusions
never named before being derived"):

- **Pairs:** the same two Lean measurand pairs `calibrate_trace_biq.py` uses
  -- `control` (`visible_action`, `intervention_active`) and `predictive`
  (`judge_captured`, `correction_request`).
- **Directions:** forward (x -> y as named above) and reverse (y -> x) for
  each pair.
- **Lags:** 0..10 inclusive (L=10; the historical fixture's one known
  coupling is at lag 3, comfortably inside this range without the range
  being fitted to it).
- **Datasets:** four, run through the identical grid --
  - the pinned historical `capture_theater`/`honest_baseline` fixtures
    (git `408444b`, full 300-row trace -- the ES-8 rediscovery target);
  - the dense `dense_capture_theater`/`dense_honest_baseline` profiles
    (`embedded_sim/dense_probe_profiles.py`, T=1200) -- enough probe events
    per lag cell for a tight CI (companion finding: the historical fixture's
    26-row window under-samples the *same* real coupling enough that the
    CI+null gate can't call it even though the point estimate clears ES-8's
    naive 0.1-bit threshold; see
    `tests/unit/test_info_ci.py::test_n8_reversed_coupling_not_reliably_detected_on_26row_window`).
- **Multiplicity correction:** 44 cells per dataset (2 pairs x 2 directions x
  11 lags). The per-cell null uses percentile `1 - 0.05/44` (Bonferroni,
  family-wise alpha 0.05 per dataset) with `n_perm=2000` permutations, which
  resolves that percentile (`1 - 1/2000 = 0.9995 > 1 - 0.05/44 ~= 0.99886`).
  Every cell is reported, not just the ones that clear the bar, so no lag is
  silently dropped after looking at results.
- **Acceptance** (checked in `tests/contract/test_probe_scan.py`, not
  enforced here): the scan must flag `(control, reverse, lag=3)` significant
  on both `capture_theater`-family datasets, and must not flag any other
  cell on either `honest_baseline`-family dataset except the real, expected
  `(control, forward, lag=0)` control-channel response (the honest
  controller's immediate reaction to its own probe, not a hidden coupling).

Usage:
    python3 probe_scan.py   # writes results/probe_scan.{md,json}
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from embedded_sim.audit_core.info_ci import mi_with_ci
from embedded_sim.dense_probe_profiles import dense_capture_theater, dense_honest_baseline

EXPERIMENT_ROOT = Path(__file__).resolve().parent
RESULTS_MD = EXPERIMENT_ROOT / "results" / "probe_scan.md"
RESULTS_JSON = EXPERIMENT_ROOT / "results" / "probe_scan.json"
PINNED_COLUMNS_FIXTURE = EXPERIMENT_ROOT / "tests" / "fixtures" / "trace_biq_calibration_columns.json"
PINNED_HONEST_FIXTURE = EXPERIMENT_ROOT / "tests" / "fixtures" / "sample_honest_baseline.jsonl"
PINNED_COLUMN_FIELDS = ["visible_action", "intervention_active", "judge_captured", "correction_request"]

LAGS = list(range(0, 11))
PAIRS = [
    ("control", "visible_action", "intervention_active"),
    ("predictive", "judge_captured", "correction_request"),
]
DIRECTIONS = ["forward", "reverse"]
N_CELLS_PER_DATASET = len(PAIRS) * len(DIRECTIONS) * len(LAGS)
FAMILYWISE_ALPHA = 0.05
NULL_PERCENTILE = 1.0 - FAMILYWISE_ALPHA / N_CELLS_PER_DATASET
N_PERM = 2000
N_BOOT = 500
SEED = 0


def load_pinned_capture_theater() -> dict[str, list[int]]:
    data = json.loads(PINNED_COLUMNS_FIXTURE.read_text(encoding="utf-8"))
    return {f: data["columns"][f] for f in PINNED_COLUMN_FIELDS}


def load_pinned_honest_baseline() -> dict[str, list[int]]:
    rows = [
        json.loads(line)
        for line in PINNED_HONEST_FIXTURE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return {f: [int(r[f]) for r in rows] for f in PINNED_COLUMN_FIELDS}


def scan_grid(cols: dict[str, list[int]], *, seed: int) -> list[dict]:
    cells = []
    for pair_name, xf, yf in PAIRS:
        for direction in DIRECTIONS:
            x_field, y_field = (xf, yf) if direction == "forward" else (yf, xf)
            x, y = cols[x_field], cols[y_field]
            for lag in LAGS:
                n = len(x)
                if lag >= n:
                    continue
                xs = x[: n - lag] if lag else x
                ys = y[lag:] if lag else y
                result = mi_with_ci(
                    xs, ys, n_boot=N_BOOT, n_perm=N_PERM, null_percentile=NULL_PERCENTILE, seed=seed
                )
                cells.append(
                    {
                        "pair": pair_name,
                        "direction": direction,
                        "x_field": x_field,
                        "y_field": y_field,
                        "lag": lag,
                        "n_pairs": len(xs),
                        **result,
                    }
                )
    return cells


def run() -> dict:
    t0 = time.perf_counter()
    datasets = {
        "capture_theater_pinned": load_pinned_capture_theater(),
        "honest_baseline_pinned": load_pinned_honest_baseline(),
        "capture_theater_dense": dense_capture_theater(seed=SEED),
        "honest_baseline_dense": dense_honest_baseline(seed=SEED),
    }
    result: dict = {
        "protocol": {
            "pairs": [p[0] for p in PAIRS],
            "directions": DIRECTIONS,
            "lags": LAGS,
            "n_cells_per_dataset": N_CELLS_PER_DATASET,
            "familywise_alpha": FAMILYWISE_ALPHA,
            "null_percentile": NULL_PERCENTILE,
            "n_perm": N_PERM,
            "n_boot": N_BOOT,
            "seed": SEED,
        },
        "datasets": {},
    }
    for name, cols in datasets.items():
        cells = scan_grid(cols, seed=SEED)
        significant = [c for c in cells if c["detected"]]
        result["datasets"][name] = {
            "n_rows": len(next(iter(cols.values()))),
            "cells": cells,
            "significant_cells": [
                {
                    "pair": c["pair"],
                    "direction": c["direction"],
                    "lag": c["lag"],
                    "estimate": c["estimate"],
                    "ci_lo": c["ci_lo"],
                    "null_corrected": c["null_95th"],
                }
                for c in significant
            ],
        }
    result["runtime_seconds"] = round(time.perf_counter() - t0, 2)
    return result


def render_md(result: dict) -> str:
    lines = [
        "# Probe scan: lag/direction grid with Bonferroni-corrected detection",
        "",
        f"Protocol: {len(PAIRS)} pairs x {len(DIRECTIONS)} directions x "
        f"{len(LAGS)} lags = {N_CELLS_PER_DATASET} cells/dataset; corrected "
        f"null percentile {NULL_PERCENTILE:.5f} (Bonferroni, family-wise "
        f"alpha {FAMILYWISE_ALPHA}), n_perm={N_PERM}, n_boot={N_BOOT}. Full "
        "cell tables in `probe_scan.json`.",
        "",
    ]
    for name, d in result["datasets"].items():
        lines.append(f"## {name} (n={d['n_rows']})")
        lines.append("")
        if d["significant_cells"]:
            lines.append("| Pair | Direction | Lag | Estimate (bits) | CI lo | Corrected null |")
            lines.append("| --- | --- | --- | --- | --- | --- |")
            for c in d["significant_cells"]:
                lines.append(
                    f"| {c['pair']} | {c['direction']} | {c['lag']} | {c['estimate']:.4f} "
                    f"| {c['ci_lo']:.4f} | {c['null_corrected']:.4f} |"
                )
        else:
            lines.append("No cell cleared the Bonferroni-corrected null.")
        lines.append("")
    lines.append(f"Runtime: {result['runtime_seconds']}s")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    result = run()
    RESULTS_JSON.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    RESULTS_MD.write_text(render_md(result), encoding="utf-8")
    print(f"Wrote {RESULTS_MD}")
    print(f"Wrote {RESULTS_JSON}")
    print()
    print(render_md(result))


if __name__ == "__main__":
    main()
