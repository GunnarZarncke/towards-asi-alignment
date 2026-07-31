# 2026-06-17 — Session end: introduction draft

## Trigger
User supplied an old introduction draft and asked to use it as the basis for the book introduction. Session closed with handoff.

## Done
- **`frontmatter/introduction.tex`** — Full introduction from user draft: thesis, loop diagram, standard-picture failure, operational vocabulary, five claims, progress/shaky sections, reading guide, practical hope.
- **`book.tex`** — Include introduction after preface.
- **`metadata/preamble.tex`** — `\MI`, `\Correctable`, `introclaim` environment.
- **`INSTRUCTIONS.md`** — Frontmatter list and include order updated.
- **Build verified** — `./build.sh` succeeds; PDF 141 pages (was 133).

## Decisions
- Introduction uses local `refsection` with three citations (Russell, Dennett); most draft prose kept verbatim with LaTeX/math fixes.
- Five claims use unnumbered `introclaim` (not chapter-numbered `claim`).
- Part VI reading guide says “extrapolative correction” (not “CEV-like”) to match chapter titles.
- Preface and executive overview remain stubs; introduction is substantive front matter.

## Open / next
- **Second milestone** (`INSTRUCTIONS.md` §25): preface, executive overview, roadmap, Chapters 1–2, appendices A and F.
- Consider deduplicating overlap between introduction and executive overview when drafting the latter.
- Optional: add more introduction citations; expand claims ledger from intro claims.
- **Uncommitted:** introduction + wiring (4 files).

## Key paths
- `frontmatter/introduction.tex`
- `book.tex` (include order)
- `metadata/preamble.tex` (notation macros)

## Commits
- Prior session: `babfe57` (44-chapter restructure + bibliography).
- This session: (none — user did not request commit).
