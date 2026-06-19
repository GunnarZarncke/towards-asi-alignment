# 2026-06-18 — Deep research report in source map

## Trigger
User asked to include `context/towards-asi-alignment-deep-research-report.md` in the source map and suggest additions to chapters.

## Done
- Extended `metadata/source-canon.md` with:
  - book-local note entry for the deep research report
  - "External literature syntheses" section (file metadata, usage note on placeholder citations)
  - report-section → chapter mapping table
  - per-chapter addition suggestions (Parts I–X)
  - bibliography candidates table (works named in report but missing or under-cited in `.bib`)

## Decisions
- Kept report in `context/` only (no extract; markdown is already agent-readable).
- Placeholder `cite turn…` markers documented as non-BibTeX; named Kernliteratur used for import list.
- Chapter suggestions prioritized drafted chapters (surgical) vs stubs (outline seeds); ch11 additions scoped to avoid duplicating content already drafted.

## Open / next
- Import bibliography candidates into appropriate `.bib` files when drafting target chapters.
- Resolve ch11/ch12 overlap before applying ch12-specific suggestions.
- Optional: add English summary crosswalk in report or `lw-references.md`.

## Key paths
- `context/towards-asi-alignment-deep-research-report.md`
- `metadata/source-canon.md`
