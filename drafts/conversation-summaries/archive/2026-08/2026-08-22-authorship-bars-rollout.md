# 2026-08-22 — Authorship bars rollout (chapters + appendices)

## Trigger
Roll `\authbar` to all chapters and wired appendices; special keys for ch.1/6/7/9, Summary/References, epistemic status; fix empty bars; tune spacing; rebuild and commit.

## Done
- Applied `\authbar` to 48 chapters + 9 appendices via `scripts/apply_authbars.py` (default `{AI}`; ch.1/6/7/9 `{GZ+AI}`).
- `scripts/patch_authbar_keys.py`: Summary + Chapter References → `{AI}`; all `epistemicstatus` → `{GZ+AI}` (chapters + appendices with status boxes).
- `scripts/strip_empty_authbars.py`: removed 33 empty section-shell bars (e.g. ch01 §1.4).
- `metadata/authorship-bars.tex`: `\authbarstrictneedspace` frontmatter-only; zero `blocksep`/split glue; pending-body logic in apply script.
- `book.tex`: `\authbarstrictneedspacetrue` / `false` at `\frontmatter` / `\mainmatter`.
- `./build.sh` → `book.pdf` / `dist/pdf/` (~1440 pp vs 1412 unmarked).
- `metadata/TODO.md`: companion-site rollout + pagination-parity optional item.

## Decisions
- Keep mdframed per-section formatting; accept ~+28 pp rather than margin-overlay rewrite now.
- `\Needspace` only in frontmatter (orphan section titles); main matter uses numbered `\section` without forced pre-breaks.

## Open / next
- Companion site authorship marking (partial): section/subsection chips + Notes toggle — see `2026-08-22-site-auth-chips.md`. Still open: image prompts `{AI}`; optional reader legend.
- Optional: margin-overlay bars if pagination must return to ~1412 pp.

## Verify
- `./build.sh` succeeds; PDF ~1440 pages.
- No empty `\begin{authbar}...\end{authbar}` blocks in chapters/appendices.
- Commit: `c866af5f`.
