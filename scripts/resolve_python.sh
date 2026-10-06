#!/usr/bin/env bash
# Print the repo Python interpreter (prefer .venv with PyYAML). Exit 1 with setup hint if missing.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PY="$ROOT/.venv/bin/python"

has_yaml() {
  "$1" -c "import yaml" 2>/dev/null
}

if [[ -x "$VENV_PY" ]] && has_yaml "$VENV_PY"; then
  echo "$VENV_PY"
  exit 0
fi

if command -v python3 >/dev/null && has_yaml python3; then
  echo python3
  exit 0
fi

cat >&2 <<EOF
PyYAML required for manuscript generation and metadata checks.

One-time setup (repo root):

  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt

Then re-run, or: source .venv/bin/activate

EOF
exit 1
