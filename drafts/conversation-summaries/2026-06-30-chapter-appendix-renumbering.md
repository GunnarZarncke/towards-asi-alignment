# 2026-06-30 — Chapter and appendix renumbering

## Trigger

User requested a big cleanup: align generated chapter/appendix numbers with print order, and record the scheme in `INSTRUCTIONS.md`.

## What was done

### Chapters (48 total)

Renamed split-insertion files and cascaded `ch20`–`ch44` → `ch21`–`ch48`:

| Old id | New id | Title (short) |
|--------|--------|----------------|
| ch19b | ch20 | Measuring and Stress-Testing Bundle Geometry |
| ch25b | ch27 | Correction Channels under Adversarial Pressure |
| ch35b | ch38 | Conductive Artifacts and Pivotal Processes |
| ch39b | ch43 | What Survives an Adversary |

- Updated `metadata/book.yml` keys (removed temporary `b`-suffix notes).
- Updated all `parts/part*.tex` `\input` paths and part-opener `\ref` suffixes.
- Restored chapter `.tex` from git, then applied in-file label suffix updates and a **placeholder-based** cross-ref pass (avoids `ch26` old/new collision).
- Fixed `scripts/generate_tables.py` to display `entry.order` (1–48) in `tables/chapter-map.tex`.

### Appendices

Built appendices renamed to match PDF letters A–G in `book.tex` include order:

| Letter | File |
|--------|------|
| A | `appA-notation` |
| B | `appB-bridge-crosswalk` (was `appBridge-crosswalk`) |
| C | `appC-institutional-translation` (was `appJ`) |
| D | `appD-worked-example` (was `appK`) |
| E | `appE-glossary` (was `appF`) |
| F | `appF-research-program` (was `appH`) |
| G | `appG-lean-proof-spine` (was `appI`) |

Stubs moved to H–L (`appH-boundary-worked-example`, `appI-value-bundle-inference`, `appJ-correction-channel-audit`, `appK-safety-case-template`, `appL-assumptions`).

Semantic `\label{appf-glossary}` etc. unchanged (label-based refs still work).

### Documentation

- **`INSTRUCTIONS.md` §14** — canonical numbering scheme (filename = YAML key = print number; appendix letter = filename prefix).
- **`README.md`**, **`formal/README.md`**, **`metadata/TODO.md`** — updated chapter references; marked renumbering TODOs done.
- **`scripts/init_scaffold.py`** — 48-chapter part map + appendix list.

### Tooling added

- `scripts/renumber_manuscript.py` — one-shot renamer (note: global text replace chains; use git restore + placeholder cross-ref pass for labels).
- `scripts/fix_chapter_paths.py` — repair `\input{chapters/...}` paths by slug.

## Verification

- `python3 scripts/generate_tables.py` — chapter map shows 1–48 (no `19b`/`25b`/…).
- `make check` — structure, citations, bibliography summaries pass.
- `./build.sh` / `latexmk -pdf -f` — PDF builds; ~48 undefined refs remain (mostly pre-existing: `appe-assumptions`, `app:lean-proof-spine`, etc.).

## Open / follow-up

- Optional: run placeholder cross-ref fix on `metadata/*.md` ledgers where chapter numbers in prose still use old ids.
- Optional: wire `context/lw-references.md` renumber script to 48-chapter map.
- Minor: fix `\leanspine` line in ch31 (simplified to avoid `$`/backtick issues in argument).

## Key paths

- `INSTRUCTIONS.md` §14, `metadata/book.yml`, `parts/part*.tex`, `chapters/ch01`–`ch48`, `appendices/appA`–`appL`, `scripts/generate_tables.py`, `tables/chapter-map.tex`
