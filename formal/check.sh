#!/usr/bin/env bash
# Canonical Lean spine gate (local and CI).
#
#   ./formal/check.sh              # lake cache + lake build + python guards
#   ./formal/check.sh --no-build   # python guards only (after lake build / lean-action)
#
# Does not run the manuscript PDF/site pipeline.
# Prints a short markdown report. On GitHub Actions, also writes $GITHUB_STEP_SUMMARY.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FORMAL="$ROOT/formal"
NO_BUILD=0

usage() {
  sed -n '2,8p' "$0"
}

for arg in "$@"; do
  case "$arg" in
    --no-build) NO_BUILD=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

cd "$FORMAL"

section() {
  echo
  echo "=== $* ==="
}

run_named() {
  # $1 title; remaining args = command. Sets last_status / last_detail.
  local title="$1"
  shift
  section "$title"
  local out
  set +e
  out="$("$@" 2>&1)"
  last_status=$?
  set -e
  printf '%s\n' "$out"
  last_detail="$(printf '%s\n' "$out" | tail -n 1)"
}

BUILD_CELL="skipped (\`--no-build\`)"
AXIOM_CELL=""
SPINE_CELL=""
STATUS=0

if [[ "$NO_BUILD" -eq 0 ]]; then
  section "Mathlib olean cache"
  if lake exe cache get; then
    BUILD_CELL="lake exe cache get + lake build"
  else
    echo "warning: lake exe cache get failed; continuing with lake build" >&2
    BUILD_CELL="lake build (cache get failed)"
  fi
  section "lake build"
  lake build
fi

run_named "Axiom budget" python3 scripts/check_axiom_budget.py
if [[ "$last_status" -eq 0 ]]; then
  AXIOM_CELL="pass — ${last_detail}"
else
  AXIOM_CELL="FAIL — ${last_detail}"
  STATUS=1
fi

run_named "SpineModel" python3 scripts/check_spine_model.py
if [[ "$last_status" -eq 0 ]]; then
  SPINE_CELL="pass — ${last_detail}"
else
  SPINE_CELL="FAIL — ${last_detail}"
  STATUS=1
fi

TOOLCHAIN="$(tr -d '[:space:]' < lean-toolchain || true)"
LEAN_VER="(lean not on PATH)"
if command -v lean >/dev/null 2>&1; then
  LEAN_VER="$(lean --version 2>/dev/null | head -n 1 || true)"
fi
THEOREM_N="$(python3 -c 'import json; print(len(json.load(open("axiom-ledger.json"))["theorems"]))')"

if [[ "$STATUS" -eq 0 ]]; then
  OVERALL="pass"
else
  OVERALL="FAIL"
fi

REPORT="$(cat <<EOF
## Lean spine — ${OVERALL}

| | |
|---|---|
| Pin | \`${TOOLCHAIN}\` |
| \`lean --version\` | ${LEAN_VER} |
| Ledger theorems | ${THEOREM_N} |
| Build | ${BUILD_CELL} |
| Axiom budget | ${AXIOM_CELL} |
| SpineModel | ${SPINE_CELL} |

Same command locally: \`make lean\` or \`./formal/check.sh\`.
EOF
)"

echo
echo "$REPORT"

if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  printf '%s\n' "$REPORT" >> "$GITHUB_STEP_SUMMARY"
fi

exit "$STATUS"
