#!/usr/bin/env bash
# Start a detached pytest profile and record its PID and live log.
#
# Usage:
#   scripts/start_pytest_background.sh {smoke|fast|slow} [pytest args...]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNNER="$ROOT/scripts/run_pytest_logged.sh"
LOG_DIR="$ROOT/runs/test-logs"
if [[ -z "${1:-}" ]]; then
  echo "usage: $0 smoke|fast|slow [pytest args...]" >&2
  exit 2
fi
PROFILE="$1"
shift

case "$PROFILE" in
  smoke|fast|slow) ;;
  *) echo "profile must be smoke, fast, or slow: $PROFILE" >&2; exit 2 ;;
esac

mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG_PATH="$LOG_DIR/pytest-${PROFILE}-${STAMP}.log"
PID_PATH="${LOG_PATH}.pid"
LAUNCHER_LOG="${LOG_PATH}.launcher"

nohup "$RUNNER" --log "$LOG_PATH" "$PROFILE" "$@" >"$LAUNCHER_LOG" 2>&1 &
PID=$!
printf '%s\n' "$PID" >"$PID_PATH"

echo "started pytest PID $PID"
echo "live log: $LOG_PATH"
echo "status: scripts/pytest_progress.sh $LOG_PATH"
