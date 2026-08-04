#!/usr/bin/env bash
# Score a grower candidate and write orchestrator-only output (never grower-visible).
#
# Usage:
#   scripts/score_grower_round.sh CANDIDATE.json ROUND_LABEL
# Example:
#   scripts/score_grower_round.sh generated_ecology_v3_round1.json round1
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANDIDATE="${1:?usage: $0 CANDIDATE.json ROUND_LABEL}"
LABEL="${2:?usage: $0 CANDIDATE.json ROUND_LABEL}"
OUT_DIR="$ROOT/growth-orchestrator/v3"
OUT_PATH="$OUT_DIR/check_result_${LABEL}.json"
PYTHON="$ROOT/.venv/bin/python"

mkdir -p "$OUT_DIR"
cd "$ROOT"
export PYTHONPATH=.

"$PYTHON" - <<PY
import json
from pathlib import Path
from graded_lab.harness.ecology_complexity import run_complexity_check

candidate = Path("$CANDIDATE")
report = run_complexity_check(candidate, progress=True)
pf = report.pass_fail_only()
details = report.details
payload = {
    "ecology_path": str(candidate),
    "round_label": "$LABEL",
    "all_passed": report.all_passed,
    "pass_fail_only": pf,
    "details_summary": {
        "c4_deploy_rate": details.get("c4", {}).get("deploy_rate"),
        "c3_episode_contention_fraction": details.get("c3", {}).get("episode_contention_fraction"),
        "c1_v3_conflicts": [
            {
                "principals": c.get("principals"),
                "shared_metric": c.get("shared_metric"),
                "status": c.get("status"),
                "correlation": c.get("correlation"),
            }
            for c in details.get("c1_v3", {}).get("conflicts", [])
        ],
        "c2_failing_roles": details.get("c2_failing_roles"),
    },
}
out = Path("$OUT_PATH")
out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out}")
print(json.dumps({"all_passed": report.all_passed, "pass_fail_only": pf}, indent=2))
PY
