#!/usr/bin/env bash
# Physical isolation for v3 grower rounds (BLIND_GENERATION.md / FINDINGS GL-35).
#
# Usage:
#   scripts/grower_stash.sh stash   # move rubric-adjacent files out
#   scripts/grower_stash.sh restore # move them back
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP_FILE="$ROOT/runs/.grower_stash_path"
ACTION="${1:?usage: $0 stash|restore}"

stash_paths() {
  cat <<EOF
PLAN_v3.md
DESIGN.md
BLIND_GENERATION.md
results
graded_lab/harness/ecology_complexity.py
tests/test_ecology_complexity.py
tests/fixtures/ecology_v3_slice_a_reference.json
tests/fixtures/ecology_v3_slice_a_knowledge_base.md
tests/fixtures/ecology_v3_c2_v3_causal_engineer_alt.json
tests/fixtures/ecology_v3_part_b_retarget_alt_ids.json
tests/fixtures/ecology_v3_supplementary_detector_suite.json
tests/fixtures/ecology_v3_supplementary_uad_channel_suite.json
oracle_only
EOF
}

if [[ "$ACTION" == stash ]]; then
  if [[ -f "$STAMP_FILE" ]]; then
    echo "stash already active: $(<"$STAMP_FILE")" >&2
    exit 2
  fi
  STASH="/tmp/graded_lab_grower_stash_$(date +%Y%m%d%H%M%S)"
  mkdir -p "$STASH"
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    src="$ROOT/$rel"
    if [[ -e "$src" ]]; then
      mkdir -p "$STASH/$(dirname "$rel")"
      mv "$src" "$STASH/$rel"
      echo "stashed $rel"
    fi
  done < <(stash_paths)
  printf '%s\n' "$STASH" >"$STAMP_FILE"
  echo "stash_dir=$STASH"
elif [[ "$ACTION" == restore ]]; then
  STASH="$(<"$STAMP_FILE")"
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    src="$STASH/$rel"
    if [[ -e "$src" ]]; then
      mkdir -p "$ROOT/$(dirname "$rel")"
      mv "$src" "$ROOT/$rel"
      echo "restored $rel"
    fi
  done < <(stash_paths)
  rm -f "$STAMP_FILE"
  echo "restored from $STASH"
else
  echo "unknown action: $ACTION" >&2
  exit 2
fi
