#!/usr/bin/env bash
# Wrap long experiment CLIs so macOS does not sleep mid-run.
# Usage: ./experiments/run_long.sh python3 experiments/multiresolution_alignment_sim.py --instrumentation-curve ...
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/.."

if command -v caffeinate >/dev/null 2>&1; then
  echo "run_long: caffeinate -dims (prevent idle/system/disk sleep until command exits)"
  exec caffeinate -dims "$@"
fi

echo "run_long: caffeinate not found; running without sleep guard" >&2
exec "$@"
