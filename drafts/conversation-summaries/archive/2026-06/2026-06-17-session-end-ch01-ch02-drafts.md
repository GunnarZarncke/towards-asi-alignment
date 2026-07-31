# 2026-06-17 — Session end: Chapters 1–2 drafts + commit

## Trigger
User supplied Chapter 1 draft (incorporated earlier in session); Chapter 2 draft in non-canonical filename; session end with commit.

## Done
- **`chapters/ch01-wrong-object.tex`** — Full draft: boundary error, operational definitions, composite systems, boundary discovery, perturbation, ontology audit table, 8 citations.
- **`chapters/ch02-artificial-civilization.tex`** — Incorporated from `chapter02_from_ai_to_artificial_civilization.tex`; chapterthesis, refsection, 7 citations; removed non-canonical duplicate file.
- **`book.tex`** — `tabularx` for ch01 table.
- **`metadata/preamble.tex`** — `\DL` macro.
- **`references/external-alignment.bib`** — Bostrom, Goodhart; fixed `ngo2022alignment` entry.
- **`metadata/book.yml`**, **`tables/chapter-map.tex`** — ch01–ch02 status → draft.
- **Build/check** — `./build.sh` and `make check` pass (237 bib keys).

## Decisions
- Kept user section structures rather than forcing generic INSTRUCTIONS stub sections.
- Ch02 placeholder `\parencite` block replaced with inline `\autocite` + existing/canonical bib keys only.
- Epigraph on ch01 left unattributed (author working principle).

## Open / next
- Expand ch02 bibliography (CEV, Ostrom, Perrow, etc.) when drafting references pass runs.
- Preface, executive overview, roadmap still stubs; reconcile exec overview with introduction/ch02 overlap.
- **Second milestone:** appendices A and F.

## Key paths
- `chapters/ch01-wrong-object.tex`
- `chapters/ch02-artificial-civilization.tex`

## Commits
- This session commit (see git log).
