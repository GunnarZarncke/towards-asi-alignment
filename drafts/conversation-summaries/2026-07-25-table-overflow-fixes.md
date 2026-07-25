# 2026-07-25 — Table overflow fixes

## Trigger
User reported the imported-ontology table on PDF page 17 (Term / Risk / Substitute / Simple example) was broken and overflowing; asked to check other tables too.

## Done
- Fixed ch01 ontology-audit table: replaced `tabularx` `{lllX}` (non-wrapping `l` columns crowding the page) with `\small` + `L{...}` wrapping columns + final `X` column.
- Converted three other plain `tabular` environments to `tabularx` with wrapping columns: ch12 boundary-expansion table, ch36 disclosure table, ch17 audit-question list.
- Rebuilt PDF; scanned `book.log` for overfull hboxes inside all chapter/appendix `tabular` / `tabularx` / `longtable` environments — no table overflows ≥5pt remain; ch01 line 615 warnings cleared.

## Decisions
- Matched the ch26 CCI table pattern (`\small`, `L{...}`, `X`) rather than introducing new table macros.
- Longtables in appendices already use `p`/`L` columns sized to `\textwidth`; no edits needed after log scan.

## Open / next
- Unstaged (not part of this commit): `RELEASE_NOTES.md` (v1.3.0 release notes draft), `site/.gitignore` (release-v1-3-0 card ignore line).
- Optional: copy refreshed `book.pdf` to `dist/pdf/` via full `./build.sh` if dist artifact timestamp matters for release workflow.

## Key paths
- `chapters/ch01-wrong-object.tex` (page ~17 table)
- `chapters/ch12-boundary-expansion.tex`, `chapters/ch36-parasites-correction-system.tex`, `chapters/ch17-low-dimensional-value-learning.tex`
- `metadata/preamble.tex` (`L` column type)

## Commits
- (this session)
