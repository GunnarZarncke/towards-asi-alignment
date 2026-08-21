# 2026-08-22 — Part pages and Contents break

## Trigger
User reported a missing page break before Contents, and that part summaries should sit on the same page as the part title.

## Done
- `\clearpage` before `\tableofcontents` in `book.tex` (memoir `\newlistof` TOC does not `\clearforchapter`).
- Memoir part opener: drop title-only `\vfil\newpage`; title at top, then summary on the same page (`metadata/preamble.tex`).
- Two `pdflatex` passes; PDF copied to `dist/pdf/`.

## Decisions
- Top-align part titles (not vertically centered) so the blurb reads as a part opener, not a footer under a centered title.

## Open / next
- None for this layout request. Full `./build.sh` (biber + latexmk) not required for the page-break change.

## Key paths
- `book.tex`
- `metadata/preamble.tex`

## Commits
- none
