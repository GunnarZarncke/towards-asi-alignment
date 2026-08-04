#!/usr/bin/env python3
"""CLI for the V2-2b non-scoring ecology pilot harness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from graded_lab.harness.ecology_pilot import DEFAULT_PILOT_SEEDS, run_pilot_episodes
from graded_lab.harness.ecology_pilot import pilot_report_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run sensor-plausible pilot episodes on a draft ecology JSON."
    )
    parser.add_argument(
        "ecology_path",
        type=Path,
        help="Path to draft generated_ecology_v2*.json",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=list(DEFAULT_PILOT_SEEDS),
        help=f"Episode seeds (default: {' '.join(map(str, DEFAULT_PILOT_SEEDS))})",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress lines",
    )
    args = parser.parse_args(argv)
    observations = run_pilot_episodes(
        args.ecology_path,
        seeds=tuple(args.seeds),
        progress=not args.quiet,
    )
    sys.stdout.write(pilot_report_json(observations))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
