# References

BibLaTeX sources loaded by `book.tex` (`references/*.bib`). Cited keys must exist in one of these files; run `make check` to verify citations and summary coverage.

## One-line bibliography summaries

Reader-facing glosses print **above each bibliography entry** in the PDF (global bibliography and per-chapter *Chapter References*). **DOI**, **URL**, and **eprint** lines print at the end of each entry when present in the `.bib` file (see `metadata/preamble.tex`).

| Artifact | Role |
|----------|------|
| `references/bibliography-summaries.tex` | `\bibsummary{key}{One sentence.}` map keyed by BibTeX entry key |
| `metadata/preamble.tex` | Hooks summaries via `\renewbibmacro*{begentry}` |

**Do not** put these glosses in `.bib` files. Keeping them in TeX avoids biber custom-field issues and matches the 2026-06-26 design.

### When adding or changing a `.bib` entry

1. Add the BibTeX entry to the appropriate category file (or `manuscript-citations.bib` until merged).
2. Add a matching `\bibsummary{same-key}{...}` line in `bibliography-summaries.tex`, alphabetically by key.
3. Write one sentence: what the source contributes to *this book* (not a restatement of the title).
4. Run `python3 scripts/check_bibliography_summaries.py` or `make check`.

### Check

```bash
python3 scripts/check_bibliography_summaries.py
```

Fails if any `.bib` key lacks a summary or any `\bibsummary` key has no `.bib` entry.
