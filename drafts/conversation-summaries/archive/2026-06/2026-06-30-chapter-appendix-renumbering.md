# 2026-06-30 — Chapter and appendix renumbering

> ## ★ FIRST OFFICIAL MAJOR RELEASE — v1.0.0 ★
>
> **This commit (`bd8f82f`, 2026-06-30) is tagged as the first official major release of the manuscript.**
> It establishes the stable, canonical numbering scheme that all later work builds on:
> **chapters `ch01`–`ch48`** in print order and **appendices A–G** matching their printed letters.
> Renames were done with `git mv` so file history follows across the renumber.
> See [`RELEASE_NOTES.md`](../../RELEASE_NOTES.md) for the full release entry.

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

### Post-commit follow-up (same session, continued)

- Regenerated PDF; fixed renumber cross-ref casualties:
  - `ch27`: 10 section `\label{...-ch26}` → `-ch27`.
  - `appG` (37), `appE` (7), `appF` (1): chained-replacement suffixes (`-ch46`/`-ch48`/etc.) remapped to real chapter labels.
  - `ch11`: `app:lean-proof-spine` → `appi-lean-proof-spine`; `appC`: `ch:detecting-goal-laundering` → `ch:goal-laundering`.
- Removed all `appe-assumptions` refs and prose implying a collated assumptions appendix (`preface`, `executive-overview`, `appB`, `appG`). Stub `appL-assumptions.tex` left unwired.
- Fixed `\leanspine` math-mode error in `ch31-conserved-properties.tex`.
- `./build.sh` now completes cleanly (no undefined refs).

## Open / follow-up

- Optional: run placeholder cross-ref fix on `metadata/*.md` ledgers where chapter numbers in prose still use old ids.
- Optional: wire `context/lw-references.md` renumber script to 48-chapter map.
- Optional: tag `v1.0.0` on `bd8f82f`; drop recovery stash / `.renumber-content-backup/` when confirmed.

## Key paths

- `INSTRUCTIONS.md` §14, `metadata/book.yml`, `parts/part*.tex`, `chapters/ch01`–`ch48`, `appendices/appA`–`appL`, `scripts/generate_tables.py`, `tables/chapter-map.tex`

## Release

- **Marked first official major release: v1.0.0** (commit `bd8f82f`). Release entry written to `RELEASE_NOTES.md`.
- Committed in a single commit (one clear, revertable point in history). All 40 path changes recorded as `git mv` renames (similarity 93–100%); `git log --follow` reaches pre-renumber history.
- Recovery points retained until confirmed: local `.renumber-content-backup/` (gitignored) and `stash@{0}` "pre-git-mv-renumber backup".

## Commits

- `bd8f82f` Renumber chapters and appendices to sequential print order
- `b99d08e` Fix post-renumber cross-refs, drop assumptions appendix refs, add release notes
