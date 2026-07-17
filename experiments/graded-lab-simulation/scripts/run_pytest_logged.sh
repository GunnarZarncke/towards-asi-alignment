#!/usr/bin/env bash
# Run one pytest profile while streaming and preserving a greppable log.
#
# Usage:
#   scripts/run_pytest_logged.sh [--log PATH] {smoke|fast|slow} [pytest args...]
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/runs/test-logs"
LOG_PATH=""

if [[ "${1:-}" == "--log" ]]; then
  LOG_PATH="${2:?--log requires a path}"
  shift 2
fi

if [[ -z "${1:-}" ]]; then
  echo "usage: $0 [--log PATH] smoke|fast|slow [pytest args...]" >&2
  exit 2
fi
PROFILE="$1"
shift
case "$PROFILE" in
  smoke|fast|slow) ;;
  *) echo "profile must be smoke, fast, or slow: $PROFILE" >&2; exit 2 ;;
esac

PYTHON="$ROOT/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  echo "missing $PYTHON; create the experiment virtual environment first" >&2
  exit 2
fi

if [[ -z "$LOG_PATH" ]]; then
  mkdir -p "$LOG_DIR"
  LOG_PATH="$LOG_DIR/pytest-${PROFILE}-$(date +%Y%m%d-%H%M%S).log"
else
  mkdir -p "$(dirname "$LOG_PATH")"
fi

echo "[pytest] profile=$PROFILE log=$LOG_PATH"
set +e
(
  cd "$ROOT"
  "$PYTHON" -m pytest tests/ --profile "$PROFILE" "$@"
) 2>&1 | tee "$LOG_PATH"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

echo "[pytest] exit=$PYTEST_STATUS log=$LOG_PATH"
exit "$PYTEST_STATUS"
