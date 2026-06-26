# 2026-06-25 — Frontmatter moves, acknowledgements, WWCTV shaky points

## Trigger
User: acknowledgements not shown; finish planned frontmatter moves (Diagram/Standard Picture/Which Alignment → early chapters; shaky points → WWCTV; dedupe How to Read; remove Introduction references); check against original plan.

## Done
- **`book.tex`:** Acknowledgements moved to after dedication (before preface) so they appear early in frontmatter and in TOC.
- **`frontmatter/introduction.tex`:** Removed Diagram, Standard Picture, Which Alignment, Where the Argument Is Shaky, `refsection`, sub-bibliography, and `\autocite`. Kept hook, five `introclaim`s, progress artifacts, part roadmap (How to Read), practical hope; added pointer to Part I and to per-chapter WWCTV.
- **`frontmatter/preface.tex`:** Updated Introduction entry-point blurb (no “where it is shaky”).
- **`chapters/ch01-wrong-object.tex`:** Added §The Standard Picture and Its Failure and §Which Alignment? before §The First Mistake.
- **`chapters/ch02-artificial-civilization.tex`:** Added §A Diagram in Words (`sec:diagram-in-words`) with book-scale loop; narrowed inline engineering loop to subsection of that section.
- **WWCTV:** Distributed intro shaky bullets to ch07, ch16, ch27, ch28, ch42.
- `./build.sh` passes.

## Decisions
- User request overrides session-end plan item “keep shaky in Introduction”; shaky content lives in chapter WWCTV sections instead.
- Part roadmap stays **Introduction-only**; Preface keeps brief entry-point routing (not the full `part-roadmap` table).
- ch01 Which Alignment forward refs: `ch:composite-agent` and Part V (not a nonexistent `ch:goal-inference` label).

## Open / next
- Read-through Intro + Part I for any remaining reframing duplication (ch01 Standard Picture vs First Mistake).
- Optional: trim Preface Part I bullet if still feels redundant with Introduction roadmap.
- ch44 opening-promise discharge when synthesis chapter lands.

## Key paths
- `book.tex`, `frontmatter/{acknowledgements,preface,introduction}.tex`
- `chapters/ch01-wrong-object.tex`, `chapters/ch02-artificial-civilization.tex`
- WWCTV: ch07, ch16, ch27, ch28, ch42

## Commits
- `a8b58b7` — Split frontmatter from Part I and move reframing into early chapters.
- `02b6716` — Correct Alignment Attractor organization name.

## Session end (2026-06-25)
- Lean proof spine: **no frontmatter change** (user confirmed calibrated Preface pointer not needed now).
- Ready to commit frontmatter reorder, acknowledgements placement, ch1/ch2 moves, WWCTV shaky bullets, session logs.
- **Not staged:** `context/Alignment Attractor.md` (2-line edit unrelated to this task); LaTeX `book.bbl-SAVE-ERROR` / `book.bcf-SAVE-ERROR` build artifacts.
