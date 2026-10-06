#!/usr/bin/env bash
# Emit build-time artifacts not checked into git:
#   - .tex fragments that book.tex \input{s}
#   - symbol-census / concept-graph outputs (markdown link check expects these)
# Run via ./build.sh, make generate, or make check (before markdown link check).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PYTHON="$("$ROOT/scripts/resolve_python.sh")"

echo "[generate] manuscript .tex fragments..."
"$PYTHON" scripts/generate_tables.py
"$PYTHON" scripts/generate_global_nocite.py
"$PYTHON" scripts/generate_notation_appendix.py
"$PYTHON" formal/scripts/check_axiom_budget.py --no-lean

echo "[generate] symbol census + concept graphs (may take ~2 min)..."
"$PYTHON" scripts/extract_symbol_formula_graph.py
"$PYTHON" scripts/build_section_reference_graph.py
"$PYTHON" scripts/build_chapter_symbol_dependency.py --all-modes
echo "[generate] done."
