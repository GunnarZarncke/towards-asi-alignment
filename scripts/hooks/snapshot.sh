#!/usr/bin/env bash
# Working-tree snapshot as a dangling commit under refs/snapshots/.
# Does not touch HEAD, the real index, or the working tree.
# Each call builds its own temporary index, so concurrent snapshots do not collide.
# Usage: snapshot.sh <label> <tool> <session> [generation]
set -euo pipefail

label="${1:?label}"
tool="${2:?tool}"
session="${3:?session}"
generation="${4:-}"

root="$(git rev-parse --show-toplevel)"
cd "$root"
git_dir="$(git rev-parse --git-dir)"
case "$git_dir" in
  /*) ;;
  *) git_dir="$root/$git_dir" ;;
esac

sanitize() {
  printf '%s' "$1" | tr -c 'A-Za-z0-9._-' '-' | cut -c1-80
}

ref_session="$(sanitize "$session")"
# Millisecond stamp: a fast turn's start and end must not share a sort key.
stamp="$(python3 -c 'from datetime import datetime, timezone; n = datetime.now(timezone.utc); print(n.strftime("%Y%m%dT%H%M%S") + ".%03dZ" % (n.microsecond // 1000))')"
ref="refs/snapshots/${stamp}-${label}-${tool}-${ref_session}"

idx="$(mktemp "$git_dir/snapshot-index.XXXXXX")"
trap 'rm -f "$idx" "$idx.lock"' EXIT
rm -f "$idx"  # git needs a missing or valid index file, not an empty one
export GIT_INDEX_FILE="$idx"
git read-tree HEAD
git add -u
git add -- chapters appendices frontmatter site/src 2>/dev/null || true
tree="$(git write-tree)"
# The stamp makes every snapshot commit unique: turns are keyed by start sha, and an
# identical tree+parent+message in the same second would otherwise give the same hash.
msg="snapshot ${label} ${tool} ${session} ${generation:--} ${stamp}"
c="$(git commit-tree "$tree" -p HEAD -m "$msg")"
git update-ref "$ref" "$c" ""  # create only; never overwrite another snapshot
mkdir -p "$git_dir/edit-attr"
printf '%s\n' "$c" >"$git_dir/edit-attr/last-snapshot"
printf '%s\n' "$c"
