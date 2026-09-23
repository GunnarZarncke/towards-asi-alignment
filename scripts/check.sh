#!/usr/bin/env bash
# Canonical manuscript/metadata gate (local and CI). Same as `make check`.
# Does not build the Astro site, Lean spine, or PDF.
# Prints a short markdown report. On GitHub Actions, also writes $GITHUB_STEP_SUMMARY.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

usage() {
  sed -n '2,5p' "$0"
}

for arg in "$@"; do
  case "$arg" in
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

section() {
  echo
  echo "=== $* ==="
}

run_named() {
  local title="$1"
  shift
  section "$title"
  local out
  set +e
  out="$("$@" 2>&1)"
  last_status=$?
  set -e
  printf '%s\n' "$out"
  last_detail="$(printf '%s\n' "$out" | tail -n 1 | tr '\n' ' ' | cut -c1-160)"
}

ROWS=()
STATUS=0

add_check() {
  local title="$1"
  shift
  run_named "$title" "$@"
  if [[ "$last_status" -eq 0 ]]; then
    ROWS+=("| ${title} | pass — ${last_detail} |")
  else
    ROWS+=("| ${title} | FAIL — ${last_detail} |")
    STATUS=1
  fi
}

add_check "generate" ./scripts/generate_manuscript_tex.sh
add_check "structure" python3 scripts/check_structure.py
add_check "markdown links" python3 scripts/check_markdown_links.py
add_check "citations" python3 scripts/check_citations.py
add_check "bibliography summaries" python3 scripts/check_bibliography_summaries.py
add_check "claim spine" python3 scripts/check_claim_spine.py
add_check "evidence stance" python3 reference/field-agendas/scripts/check-evidence-stance.py
add_check "open spine interfaces" python3 formal/scripts/check_open_spine_interfaces.py
add_check "specify/construct instances" python3 formal/scripts/check_specify_construct_instances.py
add_check "field-v2 sync" npm --prefix site run sync:field-v2 -- --check
add_check "quiz bank" python3 scripts/check_quiz_bank.py
add_check "quiz length" python3 scripts/check_quiz_length_tell.py
add_check "field matrix tests" node --test reference/field-agendas/scripts/matrix-cell.test.mjs
add_check "site lib tests" node --test --experimental-strip-types \
  site/src/lib/field-matrix-cell.test.ts \
  site/src/lib/visit-history.test.ts \
  site/src/lib/read-next.test.ts \
  site/src/lib/quiz/quiz.test.ts \
  site/src/lib/fix-graph-svg-hrefs.test.ts \
  site/src/lib/predictions/assurance-demo.test.ts

if [[ "$STATUS" -eq 0 ]]; then
  OVERALL="pass"
else
  OVERALL="FAIL"
fi

REPORT="$(
  echo "## Check — ${OVERALL}"
  echo
  echo "| Check | Result |"
  echo "|---|---|"
  printf '%s\n' "${ROWS[@]}"
  echo
  echo "Same command locally: \`make check\` or \`./scripts/check.sh\`. No Astro, Lean, or PDF."
)"

echo
echo "$REPORT"

if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  printf '%s\n' "$REPORT" >> "$GITHUB_STEP_SUMMARY"
fi

exit "$STATUS"
