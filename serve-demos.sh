#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$REPO_ROOT/src"
PORT="${PORT:-8765}"

usage() {
  cat <<EOF
Usage: $(basename "$0") [--port PORT] [--no-open]

Serve chapter demo toys from src/ and print launch URLs.

  --port PORT   Port for static file server (default: 8765)
  --no-open     Do not open a browser tab

Examples:
  $(basename "$0")
  PORT=8765 $(basename "$0") --no-open
EOF
}

OPEN=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      PORT="$2"
      shift 2
      ;;
    --no-open)
      OPEN=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "$SRC_DIR/demos" ]]; then
  echo "src/demos/ not found at $SRC_DIR/demos" >&2
  exit 1
fi

stop_previous() {
  if lsof -ti :"$PORT" >/dev/null 2>&1; then
    echo "Stopping previous server on port ${PORT}..."
    lsof -ti :"$PORT" | xargs kill -9 2>/dev/null || true
    sleep 0.2
  fi
  pkill -f "${SRC_DIR}/serve.py" 2>/dev/null || true
}

stop_previous

echo
echo "Chapter demo server:"
echo "  http://127.0.0.1:${PORT}/"
echo
echo "Demos:"
echo "  http://127.0.0.1:${PORT}/demos/ch09-uad-coalition-board/  (backend may use 8766)"
echo "  http://127.0.0.1:${PORT}/demos/ch16-value-bundle-simulator/"
echo "  http://127.0.0.1:${PORT}/demos/ch17-lhv-learnability/"
echo
echo "Site inventory: run ./serve-site.sh and open /demos/ or /chapter-demos/…"
echo

cd "$SRC_DIR"
ARGS=(python3 serve.py --port "$PORT")
if [[ "$OPEN" == "0" ]]; then
  ARGS+=(--no-open)
fi
exec "${ARGS[@]}"
