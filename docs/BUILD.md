# Building the manuscript

**Requirements:** TeX distribution with `latexmk`, `pdflatex`, `biber`, and the `memoir` class.

```bash
./build.sh          # or: make pdf
./clean.sh          # or: make clean
make check          # structure + citation key checks
make wordcount      # approximate chapter word counts
make bookstats      # markdown report → metadata/book-stats.md
make todos          # list [STUB] / TODO markers
```

Output: [`dist/pdf/towards-superintelligence-alignment.pdf`](../dist/pdf/towards-superintelligence-alignment.pdf)

If `biber` fails after `Found BibTeX data source ...`, run `./clean.sh`, remove stale `references/*.bib.blg`, create `mkdir -p .biber-par-cache`, and retry with `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`.

## Lean proof spine

```bash
cd formal && lake exe cache get && lake build
```

See [`formal/README.md`](../formal/README.md) and [`formal/LeanProofSpineImplementationBrief.md`](../formal/LeanProofSpineImplementationBrief.md).

## Companion site

```bash
cd site && npm ci && npm run build
./serve-site.sh     # from repo root
```

See [`site/README.md`](../site/README.md).

## Repository map

```text
book.tex                    # root LaTeX file
INSTRUCTIONS.md             # editorial mission, style, source canon
AGENTS.md                   # agent behavior and handoff rules
metadata/book.yml           # chapter status (source of truth)
chapters/                   # ch01–ch48
formal/                     # Lean 4 proof spine
experiments/                # toy + embedded simulators
site/                       # Astro companion site
```
