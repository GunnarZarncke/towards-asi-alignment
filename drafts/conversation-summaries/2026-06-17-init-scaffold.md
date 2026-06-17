# 2026-06-17 — First milestone: full book scaffold

## Trigger

User asked to **start the project** per `INSTRUCTIONS.md` (first milestone, §24).

## Done

- Created full LaTeX book scaffold: `book.tex`, `metadata/preamble.tex`, 10 part files, 45 chapter stubs, 8 appendix stubs, front matter.
- Added metadata ledgers (`claims`, `assumptions`, `uncertainty`, `notation`, `terminology`, `book.yml`), skeleton `.bib` files, review templates, and utility scripts (`check_structure.py`, `check_citations.py`, `wordcount.py`, `extract_todos.py`, `init_scaffold.py`, `make_chapter_stub.py`).
- Added build tooling: `build.sh`, `clean.sh`, `Makefile`, `latexmkrc`; expanded `README.md`, `LICENSE`, `.gitignore`, `.editorconfig`.
- Updated `AGENTS.md` build/README sections (were TBD).
- Verified build: 128-page PDF at `dist/pdf/towards-superintelligence-alignments.pdf`; `make check` passes.

### Build adjustments (TeX Live 2025 basic)

- Dropped `cleveref` (package not installed; stubs do not use `\cref` yet).
- Used `tcolorbox` without `[most]` (avoids missing `tikzfill.image.sty`).
- Replaced `titlepage` with memoir's `titlingpage` in `frontmatter/titlepage.tex`.

## Decisions

- **Milestone scope:** Scaffold only — all chapters remain `[STUB]`; no manuscript drafting in this session.
- **Class:** `memoir` (available in local TeX install).
- **Bibliography:** `biblatex` + `biber`, split `.bib` files per `INSTRUCTIONS.md` §11.
- **PDF outputs:** Not committed; regenerated via `./build.sh` (per `.gitignore`).

## Open / next

- **Second milestone** (`INSTRUCTIONS.md` §25): preface, executive overview, roadmap, chapters 1–2, appendices A (notation) and F (glossary).
- Optional: install `cleveref` in TeX distribution if cross-references with `\cref` are wanted later.
- Branch is 1 commit ahead of `origin/main` (push not requested).

## Key paths

- `INSTRUCTIONS.md` — milestones and chapter template
- `metadata/book.yml` — per-chapter status
- `book.tex` — root LaTeX
- `context/` + `context/extracts/` — source canon for drafting

## Commits

- `init: create full book scaffold` on `main` (initial scaffold + conversation logging; use `git log -1` for hash)
