#!/usr/bin/env bash
# Render the criteria-relations map for the paper from the single DOT source
# (drafts/alignment-frames-relations.dot, the same graph the site and the
# Lean graph check use). Paper-only layout tweaks: no in-graph title (the
# caption carries the legend), smaller cluster labels and margins, larger
# node and edge text. The source file is not modified.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
repo="$(cd "$here/../.." && pwd)"
src="$repo/drafts/alignment-frames-relations.dot"
out="$here/figures/criteria-relations.pdf"
mkdir -p "$here/figures"
sed -e 's/fontsize=24;/fontsize=16;/' -e 's/margin=36;/margin=12;/' "$src" \
  | dot -Tpdf -Glabel="" -Gpad=0.1 -Efontsize=10 -Nfontsize=12 -o "$out"
echo "Rendered ${out#$repo/}"
