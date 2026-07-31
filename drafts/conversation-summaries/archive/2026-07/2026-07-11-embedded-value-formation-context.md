# Embedded value formation added to context

## Trigger

User asked to add the new `brain-to-values` sibling paper to book context.

## What was done

- Copied `../brain-to-values/papers/embedded-value-formation/embedded-value-formation.pdf` → `context/embedded-value-formation.pdf`.
- Generated `context/extracts/embedded-value-formation.md` (20 pages) via `scripts/extract_pdf_to_md.py`.
- Updated `metadata/source-canon.md` source map row and sibling-repo blurb.
- Extended `scripts/import_source_map_refs.py`: `embedded-value-formation.bib` in `SOURCE_BIBS`, internal entry `zarncke2026embedded-value-formation`; ran import (296 unique entries).
- Added `\bibsummary{zarncke2026embedded-value-formation}{...}` in `references/bibliography-summaries.tex`.
- Updated pointers in `docs/MANUSCRIPT.md`, `llms.txt`, `REVIEWING_FOR_AGENTS.md`, `site/src/data/author-profile.json`.

## Paper

**Viability-Constrained Value Formation in Embedded Agents** (July 2026). Citation key: `zarncke2026embedded-value-formation`. Thesis: embedded agents cannot treat learned values as arbitrary free parameters; value-bundle architecture must remain compatible with the process that forms and maintains it under competition, degradation, and finite resources.

## Open / next

- No manuscript cites wired yet; natural homes include Ch15 (value formation / LHCV) and embedded-agency chapters.
- Entropic Ecology Transfer Test (paper §) may connect to graded-lab / lab-simulation lines later.

## Key paths

- `context/embedded-value-formation.pdf`
- `context/extracts/embedded-value-formation.md`
- `../brain-to-values/papers/embedded-value-formation/embedded-value-formation.tex`
