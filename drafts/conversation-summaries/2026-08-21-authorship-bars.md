# 2026-08-21 — Authorship bars (frontmatter)

## Trigger
Mark AI-assisted book content with dotted right-margin bars and small Kürzel (`AI`, `GZ`, combinations). First step: macro + frontmatter only.

## Done
- Added `\begin{authbar}{keys}` in `metadata/authorship-bars.tex` (mdframed + TikZ dotted east bar; stacked labels to the **right** of the bar; `+` or comma). Loaded from `metadata/preamble.tex`.
- Applied **per section body** (titles unmarked): dedication `{GZ}`; acknowledgements `{AI+GZ}`; preface `{GZ+AI}`; introduction `{GZ+AI}`; executive overview `{AI+GZ}` (epigraph unmarked); current status `{AI}`. Title page unmarked.
- Housekeeping TODO for chapters/appendices and the companion site.
- `pdflatex book.tex` succeeds. tcolorbox skins were not used (`tikzfill.image` missing on TeX Live basic).

## Decisions
- Dotted bar for every marked block; Kürzel order is the key order (`GZ+AI` vs `AI+GZ`).
- Chapter/section titles, epigraphs, and the title page stay unmarked. Figures later: do not bar the image; bar the prompt as `{AI}`.
- Wrap each section (and subsection) body; Kürzel sit to the right of the dotted bar.
- **2026-08-21 follow-up:** `\authbarsection` / `\authbarneedspace` (Needspace before titles); consecutive-block `\authbarblocksep`; mdframed `skipabove/below=0` + explicit `\vspace` between back-to-back authbars; `nobreak=false`, tighter split skips.

## Open / next
- Roll out to chapters/appendices (default `{AI}`).
- Companion site marking.
- Optional reader legend (preface authorship note).

## Session end
- Layout fixes verified: `\authbarsection`, consecutive-block sep, line styles (solid AI-only, sparse dotted mixed, Kürzel-only human).

## Key paths
- `metadata/authorship-bars.tex`
- `frontmatter/*.tex`
- Prototype: `dashed-right-bars.tex`

## Commits
- `f728c696` Add frontmatter authorship margin bars with AI/GZ Kürzel.
