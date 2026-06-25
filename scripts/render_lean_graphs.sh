#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/context/lean_proof_graphs"
OUT="$ROOT/figures/lean_proof"
FULL_SRC="$ROOT/context/lean_proof_dependency_graph.dot"
FULL_OUT="$ROOT/context/lean_proof_dependency_graph.png"

mkdir -p "$OUT"

if ! command -v dot >/dev/null 2>&1; then
  echo "error: graphviz 'dot' not found" >&2
  exit 1
fi

render() {
  local dotfile="$1"
  local pngfile="$2"
  dot -Tpng "$dotfile" -o "$pngfile"
  echo "wrote $pngfile"
}

for f in "$SRC"/*.dot; do
  base="$(basename "$f" .dot)"
  render "$f" "$OUT/${base}.png"
done

render "$FULL_SRC" "$FULL_OUT"
