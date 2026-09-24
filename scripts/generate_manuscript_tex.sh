#!/usr/bin/env bash
# Emit build-time artifacts not checked into git:
#   - .tex fragments that book.tex \input{s}
#   - symbol-census / concept-graph outputs (markdown link check expects these)
# Run via ./build.sh, make generate, or make check (before markdown link check).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "[generate] manuscript .tex fragments..."
python3 scripts/generate_tables.py
python3 scripts/generate_global_nocite.py
python3 scripts/generate_notation_appendix.py
python3 formal/scripts/check_axiom_budget.py --no-lean

echo "[generate] symbol census + concept graphs (may take ~2 min)..."
python3 scripts/extract_symbol_formula_graph.py
python3 scripts/build_section_reference_graph.py
python3 scripts/build_chapter_symbol_dependency.py --all-modes
echo "[generate] done."
