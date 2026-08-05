# Building the manuscript

**Requirements:** TeX distribution with `latexmk`, `pdflatex`, `biber`, and the `memoir` class.

## Build map (read this first)

This repo has **separate build roots**. There is **no** root `package.json`; npm commands belong in subdirectories only.

| What | Working directory | Command | Output |
|------|-------------------|---------|--------|
| **PDF (manuscript)** | repo root | `./build.sh` or `make pdf` | `dist/pdf/towards-superintelligence-alignment.pdf` |
| **Manuscript checks** | repo root | `make check` | (stdout) |
| **Companion site** | repo root *or* `site/` | `./serve-site.sh` (dev) · `./serve-site.sh --preview` (prod-like) | `site/dist/` |
| **Site build only** | `site/` | `npm ci && npm run build` | `site/dist/` |
| **Chapter demos** | repo root *or* `demos/` | `./serve-demos.sh` | static server on `:8765` |
| **Demo TS rebuild** | `demos/` | `npm ci && npm run build` | `demos/chNN-*/` compiled `.js` |
| **Lean spine** | `formal/` | `lake exe cache get && lake build` | `.lake/` build cache |

**`node_modules` locations (gitignored, never committed):**

- `site/node_modules/` — Astro companion site (**expected** after `cd site && npm ci`)
- `demos/node_modules/` — esbuild/vitest for demo bundles (**optional** unless editing TypeScript)
- **Repo-root `node_modules/`** — **not expected**. Usually created by mistake (`npm install`, `npm exec`, or `npx` run from the repo root). Safe to delete; nothing in this project uses it.

**Common mistakes**

- Running `npm install` or `npm exec astro …` from the repo root → creates stray root `node_modules/`
- Running `npm run build` without `cd site` first
- Opening `site/dist/index.html` directly — use `./serve-site.sh` or `npm run preview` in `site/`

From repo root, prefer wrapper scripts: `./build.sh` (PDF), `./serve-site.sh` (site), `./serve-demos.sh` (demos).

---

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

From repo root (recommended — installs `site/node_modules` if missing):

```bash
./serve-site.sh              # dev server
./serve-site.sh --preview    # production-like preview
```

Manual equivalent (`site/` only — do **not** run npm from repo root):

```bash
cd site && npm ci && npm run build
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
