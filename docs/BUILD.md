# Building the manuscript

**Requirements:** TeX distribution with `latexmk`, `pdflatex`, `biber`, and the `memoir` class.

```bash
make generate       # emit build-time .tex fragments (not in git)
./build.sh          # or: make pdf  (generate + full latexmk build)
make biber          # regenerate fragments + pdflatex → biber → pdflatex ×2
./clean.sh          # or: make clean
make check          # generate + structure + citation + bibliography-summary checks
make wordcount      # approximate chapter word counts
make bookstats      # markdown report → metadata/book-stats.md
make todos          # list [STUB] / TODO markers
```

Output: [`dist/pdf/towards-superintelligence-alignment.pdf`](../dist/pdf/towards-superintelligence-alignment.pdf)

## Generated `.tex` fragments (not in git)

`book.tex` `\input`s several files that are **generated at build time** and listed in `.gitignore`:

| Output | Generator |
|--------|-----------|
| `tables/part-roadmap.tex` | `scripts/generate_tables.py` |
| `metadata/global-nocite.tex` | `scripts/generate_global_nocite.py` |
| `metadata/notation-index.tex` | `scripts/generate_notation_appendix.py` |
| `metadata/axiom-budget-index.tex` | `formal/scripts/check_axiom_budget.py --no-lean` |

Run `make generate` (or any build/check target) before compiling if these files are missing.

All of the above are wrapped by `scripts/generate_manuscript_tex.sh`.

## Biber troubleshooting

If `biber` fails silently or stops after `Found BibTeX data source ...`, suspect stale/corrupt generated files or a missing/corrupt PAR cache before blaming bibliography syntax:

```bash
./clean.sh
make biber
```

`make biber` regenerates the manuscript `.tex` fragments, creates `.biber-par-cache/`, clears stale `references/*.bib.blg` logs, sets `PAR_GLOBAL_TMPDIR`, and runs `pdflatex → biber → pdflatex ×2`. For a full PDF after that, run `./build.sh`.

For diagnosis only: `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" biber book` (after at least one `pdflatex book.tex`).

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

`npm run sync` (and `prebuild`) runs `../scripts/generate_manuscript_tex.sh` first so gitignored build-time `.tex` fragments exist before chapter sync resolves `\label`/`\ref` targets (e.g. `tab:appi-axiom-budget` in Appendix G).

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
