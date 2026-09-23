#!/usr/bin/env bash
# Render the Lean-checked Bayesian PRA figures from plain Graphviz sources.
#
#   ./render_pra_diagrams.sh           # both as png
#   ./render_pra_diagrams.sh svg
#   ./render_pra_diagrams.sh png event-tree
#   ./render_pra_diagrams.sh pdf assurance
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
FMT="${1:-png}"
PART="${2:-both}"

case "$FMT" in
  png|svg|pdf) ;;
  *)
    echo "error: format must be png, svg, or pdf (got '$FMT')" >&2
    exit 1
    ;;
esac

if ! command -v dot >/dev/null 2>&1; then
  echo "error: graphviz 'dot' not found" >&2
  exit 1
fi

render() {
  local stem="$1"
  local src="$DIR/${stem}.dot"
  local out="$DIR/${stem}.${FMT}"
  if [[ ! -f "$src" ]]; then
    echo "error: missing $src" >&2
    exit 1
  fi
  echo "rendering ${stem}.${FMT}"
  dot -T"$FMT" "$src" -o "$out"
  echo "wrote $out"
}

case "$PART" in
  event-tree)
    render lean_checked_bayesian_pra_event_tree
    ;;
  assurance)
    render lean_checked_bayesian_pra_assurance
    ;;
  both)
    render lean_checked_bayesian_pra_event_tree
    render lean_checked_bayesian_pra_assurance
    ;;
  *)
    echo "error: part must be event-tree, assurance, or both (got '$PART')" >&2
    exit 1
    ;;
esac
