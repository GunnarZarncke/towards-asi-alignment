# 2026-06-26 — Bibliography summaries

## Trigger
The user asked for one-line summaries on all bibliography references so readers can see what each reference is about beyond its title.

## Done
- Added `references/bibliography-summaries.tex`, a key-based map with 317 one-line summaries matching the loaded bibliography entries.
- Updated `metadata/preamble.tex` so each bibliography entry prints its summary before the normal BibLaTeX entry.
- Set `pagetracker=false` in `book.tex` to avoid a non-converging BibLaTeX page-break rerun loop after the bibliography grew substantially.
- Added an `AGENTS.md` note for silent biber failures: clean generated files, remove stale `references/*.bib.blg`, create `.biber-par-cache`, and run with `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache"`.
- Preserved pre-existing `.bib` `annote` fields; rendered summaries live separately so biber does not need custom fields.
- Verification passed: `make check` and `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh`.

## Decisions
- Kept summaries outside `.bib` files because earlier direct `annotation`/`annote` experiments made biber troubleshooting harder and the TeX-side map avoids custom biber data-model concerns.
- Disabled BibLaTeX page tracking because this authoryear bibliography does not need page-tracking behavior, and the new bibliography length made page-break tracking fail to converge.

## Open / next
- The one-line summaries are useful but mechanically generated from titles, existing notes, and broad category rules; high-value references may deserve a later editorial tightening pass.
- The working tree already contained unrelated manuscript, Lean, and figure changes from earlier work; do not stage them as part of a bibliography-only commit unless explicitly authorized.

## Key paths
- `references/bibliography-summaries.tex`
- `metadata/preamble.tex`
- `book.tex`
- `AGENTS.md`

## Commits
- None.
