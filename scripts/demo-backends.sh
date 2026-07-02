#!/usr/bin/env bash
# Start Python demo backends in the background. Sourced or called from serve-site.sh.
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SRC_DIR="$REPO_ROOT/src"
DEMO_BACKEND_PORT="${DEMO_BACKEND_PORT:-8766}"
DEMO_BACKEND_PID=""

stop_demo_backends() {
  if [[ -n "${DEMO_BACKEND_PID}" ]] && kill -0 "${DEMO_BACKEND_PID}" 2>/dev/null; then
    kill "${DEMO_BACKEND_PID}" 2>/dev/null || true
    wait "${DEMO_BACKEND_PID}" 2>/dev/null || true
  fi
  if lsof -ti :"${DEMO_BACKEND_PORT}" >/dev/null 2>&1; then
    lsof -ti :"${DEMO_BACKEND_PORT}" | xargs kill -9 2>/dev/null || true
  fi
}

start_demo_backends() {
  local demo_dir="$SRC_DIR/demos/ch09-uad-coalition-board"
  if [[ ! -f "$demo_dir/app.py" ]]; then
    return 0
  fi

  if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "Warning: uvicorn not installed — ch09 demo will show fallback at /chapter-demos/ch09-uad-coalition-board/ until you run:"
    echo "  pip install -r $demo_dir/requirements.txt"
    return 0
  fi

  stop_demo_backends

  local agency_root="${AGENCY_DETECT_PATH:-$REPO_ROOT/../agency-detect}"
  if [[ -d "$agency_root" ]]; then
    export PYTHONPATH="${agency_root}${PYTHONPATH:+:$PYTHONPATH}"
  fi

  if [[ -f "$demo_dir/requirements.txt" ]]; then
    python3 -m pip install -q -r "$demo_dir/requirements.txt" 2>/dev/null || true
  fi

  echo "Starting UAD coalition board backend on port ${DEMO_BACKEND_PORT}..."
  python3 -m uvicorn app:app \
    --app-dir "$demo_dir" \
    --host 127.0.0.1 \
    --port "${DEMO_BACKEND_PORT}" \
    >/tmp/towards-asi-demo-backend.log 2>&1 &
  DEMO_BACKEND_PID=$!
  export DEMO_BACKEND_PID
  sleep 0.4
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  start_demo_backends
  echo "Backend PID: ${DEMO_BACKEND_PID}"
  echo "Log: /tmp/towards-asi-demo-backend.log"
  wait "${DEMO_BACKEND_PID}"
fi
