#!/usr/bin/env bash
# Score a v4 R-MB6b ambiguity-growth candidate (orchestrator-only EAI gate).
#
# Usage:
#   scripts/score_v4_ambiguity_growth_round.sh CANDIDATE.json ROUND_LABEL
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANDIDATE="${1:?usage: $0 CANDIDATE.json ROUND_LABEL}"
LABEL="${2:?usage: $0 CANDIDATE.json ROUND_LABEL}"
OUT_DIR="$ROOT/growth-orchestrator/v4-r-mb6b"
OUT_PATH="$OUT_DIR/check_result_${LABEL}.json"
PYTHON="$ROOT/.venv/bin/python"

mkdir -p "$OUT_DIR"
cd "$ROOT"
export PYTHONPATH=.

"$PYTHON" - <<PY
from pathlib import Path
from graded_lab.harness.v4_ambiguity_growth import write_growth_check_result

write_growth_check_result(
    Path("$CANDIDATE"),
    "$LABEL",
    Path("$OUT_PATH"),
    progress=True,
)
PY
