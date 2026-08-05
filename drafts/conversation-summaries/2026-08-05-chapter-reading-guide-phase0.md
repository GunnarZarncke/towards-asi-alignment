# 2026-08-05 — Chapter reading guide Phase 0 (infrastructure)

## Trigger
Execute Phase 0 of the chapter `readingguide` plan: LaTeX env, Introduction copy, INSTRUCTIONS §6, site tex-convert, checklist generator.

## Done
- **`metadata/preamble.tex`:** `readingguide` tcolorbox (Before You Read).
- **`frontmatter/introduction.tex`:** How to Read paragraph on when to skip vs use the box.
- **`INSTRUCTIONS.md` §6:** conditional `readingguide` template + bridge-audit rules.
- **`site/scripts/lib/tex-convert.mjs`:** `<details class="reading-guide">` + site-only link to `/paths/chapter-reading-graph/`.
- **`site/src/pages/cards/[...slug].astro`:** reading-guide styles on book pages.
- **`scripts/build_chapter_symbol_dependency.py`:** `--emit-reading-checklists` → `metadata/concept-graph/chapter-reading-checklists/` (per-chapter MD + README; likely-bridged heuristic on opening + prior closing).
- **`metadata/concept-graph/README.md`:** documented checklist command.

## Open / next
- **Phase 1 pilots:** ch25 (easy), ch40 (medium), ch07 (hard) — hand-write `readingguide` after bridge audit.
- Optional: wire `--emit-reading-checklists` into `make generate` if desired.

## Key paths
- `metadata/preamble.tex`, `frontmatter/introduction.tex`, `INSTRUCTIONS.md`
- `metadata/concept-graph/chapter-reading-checklists/`
