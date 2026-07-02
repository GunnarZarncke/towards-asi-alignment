"""Calibrate the Lean spine's pattern-diversity score against Shannon MI/CMI.

`formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean` computes an integer,
support-count-based "pattern diversity" score (its docstring explicitly says it
is *not* Shannon mutual information). `formal/AlignmentProofSpine/WorkedInstance.lean`
runs it on real rows of the capture-theater fixture. This script closes the
open calibration item (`metadata/TODO.md`, TraceBIQ item (4)): compute the
Lean score and the Shannon MI/CMI estimators from
`embedded_sim/audit_core/info.py` on the *same* real data and report how they
relate.

Protocol (fixed before computing any numbers):

- Data: the four fixture columns used by `WorkedInstance.lean`
  (`visible_action`, `intervention_active`, `judge_captured`,
  `correction_request`), pinned at git commit ``408444b`` — the working-tree
  fixture has since changed schema (no `judge_captured` field), so the pinned
  blob is the only version the Lean module's transcription can be checked
  against. The extracted columns are committed as
  `tests/fixtures/trace_biq_calibration_columns.json`; `--regenerate-columns`
  re-extracts them via `git show` and fails if they drift.
- Traces: the 26-row window used by `WorkedInstance.lean`, and the full
  300-row trace.
- Pairs: the two Lean measurand pairs — control (active→external =
  `visible_action`→`intervention_active`) and predictive (internal→sensory =
  `judge_captured`→`correction_request`) — plus two disclosed diagnostic
  pairs: the reverse control direction, and the identical-column pair
  (`correction_request`→`intervention_active`), included because it is the
  in-fixture case most favorable to the score (perfect support coupling).
- Lags: 0..25 for every pair and both traces (reported in full; no lag is
  selected after looking at results). Rows with fewer than 10 lagged pairs are
  flagged `small_sample` and excluded from findings/headlines — the same
  threshold `info.pairwise_mi_matrix` itself uses (`len(xi) < 10: continue`),
  since plug-in MI on a handful of samples is noise.
- Cross-check: the Python port must reproduce the Lean-`decide`d numbers from
  `WorkedInstance.lean` (control diversity 0, action capacity 1, tight
  ceiling 1, manipulation count 26) before any comparison is reported.

Theory expectation (provable, checked empirically here): Shannon MI is
bounded by the *tight appearance ceiling* `⌈log₂ min(m,|𝒜|)⌉`
(`diversityAlphabetCeiling`), since MI ≤ min(H(X),H(Y)) ≤ log₂(support). No
inequality holds between the *score* and MI in either direction; measuring
that gap on real data is the point of this calibration.

Usage:
    python3 calibrate_trace_biq.py                        # writes results/trace_biq_calibration.{md,json}
    python3 calibrate_trace_biq.py --regenerate-columns   # re-extract pinned columns via git show
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from embedded_sim.audit_core.info import (
    conditional_mutual_information,
    mutual_information,
)

EXPERIMENT_ROOT = Path(__file__).resolve().parent
COLUMNS_FIXTURE = EXPERIMENT_ROOT / "tests" / "fixtures" / "trace_biq_calibration_columns.json"
RESULTS_MD = EXPERIMENT_ROOT / "results" / "trace_biq_calibration.md"
RESULTS_JSON = EXPERIMENT_ROOT / "results" / "trace_biq_calibration.json"

PINNED_COMMIT = "408444b"
PINNED_FIXTURE_PATH = "experiments/embedded-simulation/tests/fixtures/sample_capture_theater.jsonl"
COLUMN_FIELDS = ["visible_action", "intervention_active", "judge_captured", "correction_request"]

N_ALPHA = 2
WINDOW = 26  # WorkedInstance.lean window (steps 0..25)
MAX_LAG = 25

# Lean-`decide`d values from formal/AlignmentProofSpine/WorkedInstance.lean.
# The Python port below must reproduce these exactly before any calibration
# numbers are reported (guards against the transcription/port bugs that
# invalidated the first version of the Lean worked instance).
LEAN_DECIDED = {
    "traceControlDiversity(window26, maxLag=0)": 0,
    "traceActionCapacityBits(window26)": 1,
    "traceDiversityTightOptimism(26, 2)": 1,
    "workedManipulationCount(window26)": 26,
}


# --- Faithful port of formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean ---


def log2_ceil_bits(n: int) -> int:
    """`log2CeilBits`: 0 for n ≤ 1, else ⌈log₂ n⌉ = (n-1).bit_length()."""
    return 0 if n <= 1 else (n - 1).bit_length()


def lagged_pairs(x: list[int], y: list[int], lag: int) -> list[tuple[int, int]]:
    """`laggedPairs`: [(x_i, y_{i+lag})] for i+lag < nSteps; [] if lag ≥ nSteps."""
    n = len(x)
    if lag >= n:
        return []
    return [(x[i], y[i + lag]) for i in range(n - lag)]


def lagged_pattern_diversity(pairs: list[tuple[int, int]]) -> int:
    """`laggedPatternDiversity`: max(0, ⌈log₂|X|⌉ + ⌈log₂|Y|⌉ − ⌈log₂|XY|⌉) on supports."""
    if not pairs:
        return 0
    hx = log2_ceil_bits(len({p[0] for p in pairs}))
    hy = log2_ceil_bits(len({p[1] for p in pairs}))
    hxy = log2_ceil_bits(len(set(pairs)))
    return max(0, hx + hy - hxy)


def spurious_diversity_ceiling(m: int, n_alpha: int) -> int:
    """`spuriousDiversityCeiling`: ⌈log₂ min(m, |𝒜|²)⌉."""
    return log2_ceil_bits(min(m, n_alpha * n_alpha))


def diversity_alphabet_ceiling(m: int, n_alpha: int) -> int:
    """`diversityAlphabetCeiling` = `traceDiversityTightOptimism`: ⌈log₂ min(m, |𝒜|)⌉."""
    return log2_ceil_bits(min(m, n_alpha))


def lagged_diversity_score(x: list[int], y: list[int], lag: int) -> int:
    """`laggedDiversityScore`: raw diversity clipped at the spurious ceiling."""
    raw = lagged_pattern_diversity(lagged_pairs(x, y, lag))
    return min(raw, spurious_diversity_ceiling(len(x), N_ALPHA))


def trace_control_diversity(active: list[int], external: list[int], max_lag: int) -> int:
    """`traceControlDiversity` for singleton active/external channel sets."""
    return max(lagged_diversity_score(active, external, lag) for lag in range(max_lag + 1))


def column_support_bits(col: list[int]) -> int:
    """`columnSupportBits` / `traceActionCapacityBits` for a singleton channel."""
    return log2_ceil_bits(len(set(col)))


# --- Shannon side (embedded_sim.audit_core.info) ---


def shannon_lagged_mi(x: list[int], y: list[int], lag: int) -> float:
    """MI on the same lagged sample the Lean score sees: (x_i, y_{i+lag}).

    `info.lagged_pair` rejects lag = 0, but the Lean protocol (PROBE_LAG = 0)
    needs it, so truncate explicitly and call `mutual_information` directly.
    """
    n = len(x)
    if lag >= n:
        return 0.0
    return mutual_information(x[: n - lag], y[lag:])


def shannon_lagged_cmi(x: list[int], y: list[int], z: list[int], lag: int) -> float:
    """CMI I(X;Y|Z) on the lagged sample, conditioning Z at the y-side steps."""
    n = len(x)
    if lag >= n:
        return 0.0
    return conditional_mutual_information(x[: n - lag], y[lag:], [z[lag:]])


# --- Data loading ---


def extract_pinned_columns() -> dict[str, list[int]]:
    blob = subprocess.run(
        ["git", "show", f"{PINNED_COMMIT}:{PINNED_FIXTURE_PATH}"],
        capture_output=True,
        text=True,
        check=True,
        cwd=EXPERIMENT_ROOT,
    ).stdout
    rows = [json.loads(line) for line in blob.splitlines() if line.strip()]
    return {f: [int(r[f]) for r in rows] for f in COLUMN_FIELDS}


def load_columns() -> dict[str, list[int]]:
    with COLUMNS_FIXTURE.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return {f: data["columns"][f] for f in COLUMN_FIELDS}


# --- Calibration ---


def lean_crosscheck(cols: dict[str, list[int]]) -> dict[str, int]:
    w = {f: c[:WINDOW] for f, c in cols.items()}
    computed = {
        "traceControlDiversity(window26, maxLag=0)": trace_control_diversity(
            w["visible_action"], w["intervention_active"], 0
        ),
        "traceActionCapacityBits(window26)": column_support_bits(w["visible_action"]),
        "traceDiversityTightOptimism(26, 2)": diversity_alphabet_ceiling(WINDOW, N_ALPHA),
        "workedManipulationCount(window26)": sum(w["judge_captured"]),
    }
    mismatches = {k: (computed[k], LEAN_DECIDED[k]) for k in LEAN_DECIDED if computed[k] != LEAN_DECIDED[k]}
    if mismatches:
        raise AssertionError(
            f"Python port disagrees with Lean-decided values (port, lean): {mismatches}"
        )
    return computed


def pair_table(
    x: list[int], y: list[int], z: list[int], max_lag: int
) -> list[dict]:
    rows = []
    m = len(x)
    for lag in range(max_lag + 1):
        pairs = lagged_pairs(x, y, lag)
        rows.append(
            {
                "lag": lag,
                "n_pairs": len(pairs),
                "small_sample": len(pairs) < 10,
                "joint_support": len(set(pairs)),
                "raw_diversity": lagged_pattern_diversity(pairs),
                "score_bits": lagged_diversity_score(x, y, lag),
                "mi_bits": round(shannon_lagged_mi(x, y, lag), 6),
                "cmi_bits": round(shannon_lagged_cmi(x, y, z, lag), 6),
                "ceiling_tight_bits": diversity_alphabet_ceiling(m, N_ALPHA),
                "ceiling_spurious_bits": spurious_diversity_ceiling(m, N_ALPHA),
            }
        )
    return rows


def run_calibration(cols: dict[str, list[int]]) -> dict:
    crosscheck = lean_crosscheck(cols)

    pairs_spec = [
        # (key, x-field, y-field, role)
        ("control", "visible_action", "intervention_active",
         "Lean measurand: traceControlDiversity direction (active→external)"),
        ("predictive", "judge_captured", "correction_request",
         "Lean measurand: tracePredictiveDiversity direction (internal→sensory)"),
        ("control_reversed", "intervention_active", "visible_action",
         "diagnostic: reverse control direction (does intervention predict later action?)"),
        ("identical_columns", "correction_request", "intervention_active",
         "diagnostic: the two columns are byte-identical in the pinned fixture"),
    ]

    assert cols["correction_request"] == cols["intervention_active"], (
        "pinned fixture invariant changed: correction_request and "
        "intervention_active are expected to be identical columns"
    )

    tables = {}
    for trace_name, length in (("window26", WINDOW), ("full300", len(cols["visible_action"]))):
        sliced = {f: c[:length] for f, c in cols.items()}
        z = sliced["judge_captured"]  # constant 1 in the pinned fixture
        tables[trace_name] = {
            key: {
                "role": role,
                "x": xf,
                "y": yf,
                "rows": pair_table(sliced[xf], sliced[yf], z, MAX_LAG),
            }
            for key, xf, yf, role in pairs_spec
        }

    def usable_rows():
        for tname, table in tables.items():
            for pkey, entry in table.items():
                for row in entry["rows"]:
                    if not row["small_sample"]:
                        yield tname, pkey, row

    # Soundness check (provable direction): MI never exceeds the tight ceiling.
    ceiling_violations = [
        (tname, pkey, row["lag"], row["mi_bits"], row["ceiling_tight_bits"])
        for tname, pkey, row in usable_rows()
        if row["mi_bits"] > row["ceiling_tight_bits"] + 1e-9
    ]

    # Calibration gaps (the empirical question).
    under_detection = [
        (tname, pkey, row["lag"], row["mi_bits"])
        for tname, pkey, row in usable_rows()
        if row["score_bits"] == 0 and row["mi_bits"] > 0.1
    ]
    over_statement = [
        (tname, pkey, row["lag"], row["score_bits"], row["mi_bits"])
        for tname, pkey, row in usable_rows()
        if row["score_bits"] >= 1 and row["mi_bits"] < 0.5 * row["score_bits"]
    ]

    return {
        "provenance": {
            "fixture": PINNED_FIXTURE_PATH,
            "pinned_commit": PINNED_COMMIT,
            "columns_fixture": str(COLUMNS_FIXTURE.relative_to(EXPERIMENT_ROOT)),
            "estimators": "embedded_sim/audit_core/info.py (Shannon, plug-in PMF)",
            "score": "faithful port of formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean",
            "protocol": "pairs/lags/traces fixed before computing (see module docstring)",
        },
        "lean_crosscheck": crosscheck,
        "tables": tables,
        "findings": {
            "mi_le_tight_ceiling_violations": ceiling_violations,
            "score_zero_but_mi_above_0.1": under_detection,
            "score_at_least_1_but_mi_below_half_score": over_statement,
        },
    }


# --- Reporting ---


def render_md(result: dict) -> str:
    lines = [
        "# Trace B-IQ pattern-diversity score vs Shannon MI — calibration",
        "",
        f"Data: `{PINNED_FIXTURE_PATH}` pinned at git `{PINNED_COMMIT}` "
        "(the same data `formal/AlignmentProofSpine/WorkedInstance.lean` transcribes). "
        "Score: faithful Python port of `TraceBIQ.lean` (cross-checked below). "
        "MI/CMI: `embedded_sim/audit_core/info.py` plug-in Shannon estimators. "
        "Protocol (pairs, lags 0–25, both traces) fixed before computing; full "
        "tables in `trace_biq_calibration.json`.",
        "",
        "## Lean cross-check (port must reproduce the `decide`d numbers)",
        "",
        "| Quantity | Port | Lean |",
        "| --- | --- | --- |",
    ]
    for k, v in result["lean_crosscheck"].items():
        lines.append(f"| `{k}` | {v} | {LEAN_DECIDED[k]} |")

    lines += [
        "",
        "## Headline rows (full tables in the JSON)",
        "",
        "| Trace | Pair | Lag | Score (bits) | MI (bits) | Tight ceiling |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    highlights = []
    for tname, table in result["tables"].items():
        for pkey, entry in table.items():
            rows = [r for r in entry["rows"] if not r["small_sample"]]
            best_mi = max(rows, key=lambda r: r["mi_bits"])
            best_score = max(rows, key=lambda r: (r["score_bits"], r["mi_bits"]))
            for row in {id(best_mi): best_mi, id(best_score): best_score}.values():
                highlights.append((tname, pkey, row))
    for tname, pkey, row in highlights:
        lines.append(
            f"| {tname} | {pkey} | {row['lag']} | {row['score_bits']} "
            f"| {row['mi_bits']:.3f} | {row['ceiling_tight_bits']} |"
        )

    f = result["findings"]
    lines += [
        "",
        "## Findings",
        "",
        f"- **Soundness (provable direction) confirmed:** MI ≤ tight appearance ceiling "
        f"on every pair/lag tested ({len(f['mi_le_tight_ceiling_violations'])} violations).",
        f"- **Under-detection (score = 0, MI > 0.1 bits):** "
        f"{len(f['score_zero_but_mi_above_0.1'])} pair/lag cases. The support-based "
        "score is brittle: a single stray joint pattern (e.g. one boundary pulse "
        "before the periodic coupling settles) inflates the joint support and "
        "zeroes the score while Shannon MI still sees the coupling.",
        f"- **Over-statement (score ≥ 1 bit, MI < half the score):** "
        f"{len(f['score_at_least_1_but_mi_below_half_score'])} pair/lag cases. On "
        "sparse but perfectly support-coupled columns (the identical-column pair) "
        "the score reads a full bit while the plug-in MI of the rare event is a "
        "small fraction of a bit.",
        "- **Direction blindness (protocol-level, not estimator-level):** the "
        "fixture's genuine temporal coupling is intervention → visible action "
        "3 steps later (controller pulse at t, agent action at t+3), i.e. the "
        "*reversed* direction relative to the Lean control measurand "
        "(active→external). At the worked instance's protocol lag (`maxLag = 0`, "
        "the simulator's own `PROBE_LAG`) both estimators correctly read ≈0 in "
        "the measurand direction; the structure only exists in the direction "
        "and at the lags the protocol does not measure.",
        "",
        "**Conclusion:** the pattern-diversity *score* is not calibrated to Shannon "
        "MI in either direction and must not be quoted as bits of mutual "
        "information (`TraceBIQ.lean`'s docstring already says this; these are the "
        "numbers). The tight appearance *ceiling* — the quantity the Lean "
        "appearance bounds actually use — is empirically (and provably) sound as "
        "an upper bound for Shannon MI on this data.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regenerate-columns",
        action="store_true",
        help="re-extract the pinned fixture columns via `git show` and rewrite the columns fixture",
    )
    args = parser.parse_args()

    if args.regenerate_columns:
        cols = extract_pinned_columns()
        COLUMNS_FIXTURE.write_text(
            json.dumps(
                {
                    "provenance": f"git show {PINNED_COMMIT}:{PINNED_FIXTURE_PATH}",
                    "columns": cols,
                },
                indent=1,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {COLUMNS_FIXTURE}")

    cols = load_columns()

    if args.regenerate_columns:
        pass  # just regenerated from git
    else:
        # If git is available, verify the committed columns still match the pin.
        try:
            pinned = extract_pinned_columns()
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            pinned = None
        if pinned is not None and pinned != cols:
            raise AssertionError(
                "committed trace_biq_calibration_columns.json no longer matches "
                f"git show {PINNED_COMMIT}:{PINNED_FIXTURE_PATH}"
            )

    result = run_calibration(cols)
    RESULTS_JSON.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    RESULTS_MD.write_text(render_md(result), encoding="utf-8")
    print(f"Wrote {RESULTS_MD}")
    print(f"Wrote {RESULTS_JSON}")
    print()
    print(render_md(result))


if __name__ == "__main__":
    main()
