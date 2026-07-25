#!/usr/bin/env bash
# Emit all build-time .tex fragments that book.tex \input{s}.
# Not checked into git — run via ./build.sh, make generate, or make check.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/generate_tables.py
python3 scripts/generate_global_nocite.py
python3 scripts/generate_notation_appendix.py
python3 formal/scripts/check_axiom_budget.py --no-lean
