#!/usr/bin/env bash
# ET-1 Orbit battery wrapper (Layer A). Requires external/orbit checkout.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PIN="$(tr -d '[:space:]' < external/orbit/PIN.txt)"
ORBIT_DIR="$ROOT/external/orbit"
FIX_BASE="$ROOT/fixtures/orbit_et1/et1_jira_baseline.yaml"
FIX_COLL="$ROOT/fixtures/orbit_et1/et1_jira_collusion.yaml"
MODEL="${ET1_MODEL:-openai/gpt-4o-mini}"
TRACES_DIR="$ROOT/results/et1_traces"
RAW_DIR="$TRACES_DIR/raw"
SMOKE=0
TRIAL=0
SEEDS=(0 1 2 3 4 5 6 7)

usage() {
  echo "Usage: $0 [--smoke] [--trial]"
  echo "  --smoke   Run 1 baseline + 1 collusion episode (seed 0 only)"
  echo "  --trial   Run 4 seeds per fixture (8 episodes total)"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --smoke) SMOKE=1; SEEDS=(0); shift ;;
    --trial) TRIAL=1; SEEDS=(0 1 2 3); shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ "$SMOKE" -eq 1 && "$TRIAL" -eq 1 ]]; then
  echo "Choose only one of --smoke or --trial" >&2
  exit 1
fi

if [[ ! -d "$ORBIT_DIR/.git" ]]; then
  echo "Missing Orbit checkout at $ORBIT_DIR — see external/orbit/README.md" >&2
  exit 1
fi

CHECKOUT_SHA="$(git -C "$ORBIT_DIR" rev-parse HEAD)"
if [[ "$CHECKOUT_SHA" != "$PIN" ]]; then
  echo "Orbit checkout SHA $CHECKOUT_SHA != PIN $PIN" >&2
  exit 1
fi

orbit_cmd() {
  if command -v uv >/dev/null 2>&1; then
    (cd "$ORBIT_DIR" && uv run "$@")
  elif [[ -x "$ORBIT_DIR/.venv/bin/orbit" ]]; then
    (cd "$ORBIT_DIR" && .venv/bin/"$@")
  else
    echo "Need uv or $ORBIT_DIR/.venv (see external/orbit/README.md)" >&2
    exit 1
  fi
}

inspect_cmd() {
  if command -v uv >/dev/null 2>&1; then
    (cd "$ORBIT_DIR" && uv run inspect "$@")
  elif [[ -x "$ORBIT_DIR/.venv/bin/inspect" ]]; then
    (cd "$ORBIT_DIR" && .venv/bin/inspect "$@")
  else
    echo "Need uv or inspect in $ORBIT_DIR/.venv" >&2
    exit 1
  fi
}

mkdir -p "$RAW_DIR" "$TRACES_DIR"

run_fixture() {
  local fixture_yaml="$1"
  local fixture_id="$2"
  local seed="$3"
  local out_name="$(echo "$fixture_id" | tr '[:upper:]' '[:lower:]')_seed${seed}"
  local log_json="$RAW_DIR/${out_name}.json"

  echo "[orbit] fixture=$fixture_id seed=$seed model=$MODEL"
  orbit_cmd orbit run "$fixture_yaml" --model "$MODEL" -T "scenario.properties.seed=$seed" --log-dir "$RAW_DIR/inspect_logs"

  latest_eval="$(ls -t "$RAW_DIR/inspect_logs"/*.eval 2>/dev/null | head -1 || true)"
  if [[ -z "$latest_eval" ]]; then
    echo "No .eval log produced for $fixture_id seed=$seed" >&2
    exit 1
  fi
  inspect_cmd log dump "$latest_eval" > "$log_json"
  cp "$latest_eval" "$RAW_DIR/${out_name}.eval"
  echo "  → $log_json"
}

EP=0
TOTAL=$(( ${#SEEDS[@]} * 2 ))

for seed in "${SEEDS[@]}"; do
  EP=$((EP + 1))
  echo "[$EP/$TOTAL] baseline seed=$seed"
  run_fixture "$FIX_BASE" "ET1-JIRA-BASE" "$seed"
  EP=$((EP + 1))
  echo "[$EP/$TOTAL] collusion seed=$seed"
  run_fixture "$FIX_COLL" "ET1-JIRA-COLL" "$seed"
  if [[ "$SMOKE" -eq 1 ]]; then
    break
  fi
done

python3 "$ROOT/scripts/run_et1_score_traces.py" --adapt "$RAW_DIR"/*.json --traces "$TRACES_DIR"
