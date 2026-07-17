#!/usr/bin/env bash
# Show a concise state summary for a log made by start_pytest_background.sh.
#
# Usage:
#   scripts/pytest_progress.sh runs/test-logs/pytest-slow-YYYYMMDD-HHMMSS.log
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_PATH="${1:?usage: $0 LOG_PATH}"
[[ "$LOG_PATH" = /* ]] || LOG_PATH="$ROOT/$LOG_PATH"
PID_PATH="${LOG_PATH}.pid"

if [[ -f "$PID_PATH" ]]; then
  PID="$(<"$PID_PATH")"
  if kill -0 "$PID" 2>/dev/null; then
    echo "status: running (PID $PID)"
  else
    echo "status: finished (PID $PID is no longer running)"
  fi
else
  echo "status: PID file unavailable"
fi

echo "log: $LOG_PATH"
if [[ ! -f "$LOG_PATH" ]]; then
  echo "log has not been created yet"
  exit 0
fi

echo "--- recent output ---"
tail -n 30 "$LOG_PATH"
echo "--- summary matches ---"
rg -n "FAILED|ERROR|[0-9]+ passed|[0-9]+ failed|exit=" "$LOG_PATH" || true
