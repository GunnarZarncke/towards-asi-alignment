#!/usr/bin/env python3
"""Adapt Inspect logs and/or score ET-1 ExternalTrace JSON (Layer B/C).

Usage:
  cd experiments/graded-lab-simulation
  python3 scripts/run_et1_score_traces.py --traces results/et1_traces/
  python3 scripts/run_et1_score_traces.py --adapt results/et1_traces/raw/*.json
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.external.inspect_adapter import adapt_inspect_log_to_trace  # noqa: E402
from graded_lab.external.passive_uad_score import (  # noqa: E402
    score_traces_dir,
    write_et1_results,
)
from graded_lab.external.trace_schema import (  # noqa: E402
    FIXTURE_BASELINE,
    FIXTURE_COLLUSION,
    FROZEN_MODEL,
    save_external_trace,
)

PIN_PATH = ROOT / "external" / "orbit" / "PIN.txt"
TRACES_DEFAULT = ROOT / "results" / "et1_traces"
OUT_DEFAULT = ROOT / "results" / "et1_orbit_collusion.json"


def _read_pin() -> str:
    return PIN_PATH.read_text(encoding="utf-8").strip()


def _fixture_id_from_name(name: str) -> str:
    lower = name.lower()
    if "collusion" in lower or "coll" in lower:
        return FIXTURE_COLLUSION
    if "baseline" in lower or "base" in lower:
        return FIXTURE_BASELINE
    raise ValueError(f"cannot infer fixture_id from path name: {name}")


def _seed_from_name(name: str, *, fallback: int) -> int:
    match = re.search(r"_seed(\d+)", name)
    if match:
        return int(match.group(1))
    return fallback


def adapt_logs(
    paths: list[Path],
    *,
    traces_dir: Path,
    pin: str,
    model: str,
    coalition_kind: str | None = None,
) -> list[Path]:
    traces_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, log_path in enumerate(sorted(paths), start=1):
        fixture_id = _fixture_id_from_name(log_path.name)
        seed = _seed_from_name(log_path.name, fallback=i - 1)
        print(f"[adapt {i}/{len(paths)}] fixture={fixture_id} seed={seed} log={log_path.name}")
        trace = adapt_inspect_log_to_trace(
            log_path,
            fixture_id=fixture_id,
            orbit_commit=pin,
            seed=seed,
            model=model,
            coalition_kind=coalition_kind,
        )
        out = traces_dir / f"{fixture_id.lower()}_seed{seed}.json"
        save_external_trace(trace, out)
        stats = trace.adapter_stats or {}
        unmapped = stats.get("unmapped", 0)
        mapped = stats.get("mapped", len(trace.events))
        total = mapped + unmapped
        rate = (unmapped / total) if total else 0.0
        print(f"  → {out.name} events={len(trace.events)} unmapped_rate={rate:.3f}")
        written.append(out)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--traces",
        type=Path,
        default=TRACES_DEFAULT,
        help="Directory of ExternalTrace JSON files to score",
    )
    parser.add_argument(
        "--adapt",
        nargs="*",
        type=Path,
        default=None,
        help="Inspect .json/.eval logs to adapt before scoring",
    )
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    parser.add_argument(
        "--model",
        default=FROZEN_MODEL,
        help="Model id to record on adapted traces (must match the eval run)",
    )
    parser.add_argument(
        "--coalition-kind",
        default=None,
        help="Override ground-truth coalition_kind label on collusion traces "
        "(e.g. colosseum_attack_simple); defaults to colosseum_control_sc",
    )
    args = parser.parse_args()

    pin = _read_pin()
    if args.adapt:
        adapt_logs(
            list(args.adapt),
            traces_dir=args.traces,
            pin=pin,
            model=args.model,
            coalition_kind=args.coalition_kind,
        )

    results = score_traces_dir(args.traces)
    write_et1_results(results, args.out)

    preds = results["predictions"]
    print(
        f"ET-1 outcome={results['outcome']} "
        f"P1={preds['P1']['hits']}/{preds['P1']['required']} "
        f"P2={preds['P2']['hits']}/{preds['P2']['required']} "
        f"P3_unmapped={preds['P3']['mean_unmapped_rate']:.3f}"
    )
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
