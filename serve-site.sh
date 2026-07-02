#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$REPO_ROOT/site"
PORT="${PORT:-4321}"
MODE="dev"

usage() {
  cat <<EOF
Usage: $(basename "$0") [--preview] [--port PORT]

Serve the Astro companion site and print the local URL.

  --preview   Build site/dist/ first, then serve a production-like preview
  --port PORT Port number (default: 4321)

Examples:
  $(basename "$0")
  $(basename "$0") --preview
  PORT=3000 $(basename "$0")
EOF
}

stop_previous_serves() {
  local p
  for p in "$PORT" 4321 4322 4323 4324 4325 8765 8766; do
    if lsof -ti :"$p" >/dev/null 2>&1; then
      echo "Stopping previous server on port ${p}..."
      lsof -ti :"$p" | xargs kill -9 2>/dev/null || true
    fi
  done
  pkill -f "${SITE_DIR}.*astro (dev|preview)" 2>/dev/null || true
  sleep 0.2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --preview)
      MODE="preview"
      shift
      ;;
    --port)
      PORT="$2"
      shift 2
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

if [[ ! -d "$SITE_DIR" ]]; then
  echo "site/ directory not found at $SITE_DIR" >&2
  exit 1
fi

cd "$SITE_DIR"

if [[ ! -d node_modules ]]; then
  echo "Installing site dependencies..."
  npm install
fi

stop_previous_serves

# Chapter demo backends (UAD coalition board) for /chapter-demos/ proxy
# shellcheck source=scripts/demo-backends.sh
source "$REPO_ROOT/scripts/demo-backends.sh"
cleanup() {
  stop_demo_backends
}
trap cleanup EXIT INT TERM
start_demo_backends

# Local serve uses site root so URLs are http://localhost:PORT/book/ch06/
# GitHub Pages CI keeps the default base /towards-asi-alignment
export ASTRO_BASE="${ASTRO_BASE:-/}"
export ASTRO_TELEMETRY_DISABLED=1

URL="http://localhost:${PORT}/"

echo
echo "Companion site URL:"
echo "  ${URL}"
echo "Example chapter:"
echo "  ${URL}book/ch06/"
echo "Chapter demos (integrated):"
echo "  ${URL}demos/"
echo "  ${URL}chapter-demos/ch16-value-bundle-simulator/"
echo "  ${URL}chapter-demos/ch09-uad-coalition-board/  (proxied to backend :8766)"
echo

if [[ "$MODE" == "preview" ]]; then
  npm run build
  exec npx astro preview --port "$PORT" --host 127.0.0.1
fi

npm run sync
exec npx astro dev --port "$PORT" --host 127.0.0.1
