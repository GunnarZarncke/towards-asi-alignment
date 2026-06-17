# 2026-06-17 — Title alignment fix

## Trigger
User found a typo: the book title and PDF output should be **Towards Superintelligence Alignment** (singular), not *Alignments*. Requested a repo-wide replace in filenames and text, a semantic rewrite of the introduction section that had justified the plural title, PDF regeneration, then end-of-session commit.

## Done
- Renamed `chapters/ch44-towards-alignments.tex` → `chapters/ch44-towards-alignment.tex`; updated `\input`, labels, scaffold script, chapter map, `book.yml`.
- Updated title strings in `book.tex`, `titlepage.tex`, `README.md`, `INSTRUCTIONS.md`, `metadata/book.yml`.
- Updated build output path in `build.sh`, `AGENTS.md`, docs; PDF at `dist/pdf/towards-superintelligence-alignment.pdf` (regenerated, not committed).
- Rewrote introduction section: **Which Alignment?** — drops title-plural framing; keeps nested-relations argument and diagnostic questions.
- Patched historical path in `drafts/conversation-summaries/2026-06-17-init-scaffold.md`.
- `make check` passes; `./build.sh` succeeds.

## Decisions
- Kept conceptual plural “alignments” in `ch02-artificial-civilization.tex` (many loops), distinct from the book title.
- Did not stage `drafts/conversation-summaries/2026-06-17-ch03-dynamical-guarantee-draft.md` (unrelated commit-hash edit from another session).

## Open / next
- Optional: align `ch02` line “uses alignment in a plural sense” with new introduction framing if desired.
- Continue manuscript work per `metadata/book.yml` / latest ch03 log.

## Key paths
- `frontmatter/introduction.tex` — **Which Alignment?** section
- `build.sh`, `book.tex`, `chapters/ch44-towards-alignment.tex`
- `dist/pdf/towards-superintelligence-alignment.pdf`

## Commits
- `4d7007e` Fix book title typo: Alignments → Alignment.
