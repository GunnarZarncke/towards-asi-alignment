#!/usr/bin/env bash
# Start Python demo backends in the background. Sourced or called from serve-site.sh.
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
DEMOS_DIR="$REPO_ROOT/demos"
DEMO_BACKEND_PORT="${DEMO_BACKEND_PORT:-8766}"
SCAFFOLD_MISUSE_BACKEND_PORT="${SCAFFOLD_MISUSE_BACKEND_PORT:-8767}"
DEMO_BACKEND_PID=""
SCAFFOLD_MISUSE_BACKEND_PID=""

stop_demo_backends() {
  if [[ -n "${DEMO_BACKEND_PID}" ]] && kill -0 "${DEMO_BACKEND_PID}" 2>/dev/null; then
    kill "${DEMO_BACKEND_PID}" 2>/dev/null || true
    wait "${DEMO_BACKEND_PID}" 2>/dev/null || true
  fi
  if [[ -n "${SCAFFOLD_MISUSE_BACKEND_PID}" ]] && kill -0 "${SCAFFOLD_MISUSE_BACKEND_PID}" 2>/dev/null; then
    kill "${SCAFFOLD_MISUSE_BACKEND_PID}" 2>/dev/null || true
    wait "${SCAFFOLD_MISUSE_BACKEND_PID}" 2>/dev/null || true
  fi
  for p in "${DEMO_BACKEND_PORT}" "${SCAFFOLD_MISUSE_BACKEND_PORT}"; do
    if lsof -ti :"${p}" >/dev/null 2>&1; then
      lsof -ti :"${p}" | xargs kill -9 2>/dev/null || true
    fi
  done
}

_start_uvicorn() {
  local demo_dir="$1"
  local port="$2"
  local log_label="$3"
  python3 -m uvicorn app:app \
    --app-dir "$demo_dir" \
    --host 127.0.0.1 \
    --port "${port}" \
    >"/tmp/towards-asi-demo-${log_label}.log" 2>&1 &
  echo $!
}

start_demo_backends() {
  if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "Warning: uvicorn not installed — backend demos will show fallbacks until you install requirements under demos/ch*/"
    return 0
  fi

  stop_demo_backends

  local ch09_dir="$DEMOS_DIR/ch09-uad-coalition-board"
  if [[ -f "$ch09_dir/app.py" ]]; then
    local agency_root="${AGENCY_DETECT_PATH:-$REPO_ROOT/../agency-detect}"
    if [[ -d "$agency_root" ]]; then
      export PYTHONPATH="${agency_root}${PYTHONPATH:+:$PYTHONPATH}"
    fi
    if [[ -f "$ch09_dir/requirements.txt" ]]; then
      python3 -m pip install -q -r "$ch09_dir/requirements.txt" 2>/dev/null || true
    fi
    echo "Starting UAD coalition board backend on port ${DEMO_BACKEND_PORT}..."
    DEMO_BACKEND_PID=$(_start_uvicorn "$ch09_dir" "$DEMO_BACKEND_PORT" "ch09-backend")
    export DEMO_BACKEND_PID
  fi

  local ch01_dir="$DEMOS_DIR/ch01-scaffold-misuse"
  if [[ -f "$ch01_dir/app.py" ]]; then
    if [[ -f "$ch01_dir/requirements.txt" ]]; then
      python3 -m pip install -q -r "$ch01_dir/requirements.txt" 2>/dev/null || true
    fi
    echo "Starting scaffold-misuse LLM backend on port ${SCAFFOLD_MISUSE_BACKEND_PORT}..."
    SCAFFOLD_MISUSE_BACKEND_PID=$(_start_uvicorn "$ch01_dir" "$SCAFFOLD_MISUSE_BACKEND_PORT" "ch01-backend")
    export SCAFFOLD_MISUSE_BACKEND_PID
  fi

  sleep 0.4
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  start_demo_backends
  echo "UAD backend PID: ${DEMO_BACKEND_PID:-none}"
  echo "Scaffold-misuse backend PID: ${SCAFFOLD_MISUSE_BACKEND_PID:-none}"
  wait
fi
