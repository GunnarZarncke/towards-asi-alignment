#!/usr/bin/env python3
"""Audit an external correction.jsonl through the artifact-only embedded path."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from embedded_sim.trace_ingest import audit_trace_bundle  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit ingested correction.jsonl")
    parser.add_argument("correction", type=Path, help="Path to correction.jsonl")
    parser.add_argument("--workflow", type=Path, default=None, help="Optional workflow.jsonl")
    parser.add_argument("--instrumentation", default="medium_handles")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--json", action="store_true", help="Print JSON result")
    args = parser.parse_args()

    result = audit_trace_bundle(
        args.correction,
        workflow_path=args.workflow,
        instrumentation=args.instrumentation,  # type: ignore[arg-type]
        seed=args.seed,
    )
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"source={result.source}")
        print(f"rows={result.n_correction_rows} instrumentation={result.instrumentation}")
        print(f"cci_status={result.cci_status} safety={result.safety_decision}")
        print(f"failed_bridge={result.failed_bridge}")
        print(f"flags={result.structural_flags}")


if __name__ == "__main__":
    main()
