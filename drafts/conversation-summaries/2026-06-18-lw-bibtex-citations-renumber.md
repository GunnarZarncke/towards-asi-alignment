# 2026-06-18 — LW BibTeX citations and lw-references renumber

## Trigger
User confirmed: add BibTeX entries for LessWrong references, cite them in drafted chapters with clear prose connection, and renumber `context/lw-references.md` to match `metadata/book.yml`.

## Done
- Added 18 LW/AF posts to `references/external-alignment.bib` (Critch boundaries, Christiano failure/corrigibility, Yudkowsky lethalities/wishes/CEV/fragile, Wentworth pointers/selection/agent-structure, Shlegeris AI control, Thornley shutdown, Hubinger model organisms, Kulveit Pando, Soares sharp left turn/hard bits).
- Mirrored the same block in `scripts/import_source_map_refs.py` `MANUAL_ENTRIES` so regeneration does not drop them.
- Wired `\autocite{...}` into drafted chapters ch01–04, 06–10, 40 with connecting prose (not bare citation drops).
- Resolved ch40 `TODO[citation]`; added `\printbibliography` to ch40.
- Renumbered `context/lw-references.md` to ch01–ch44 via `scripts/renumber_lw_references.py`; added ch05 placeholder, ch40 lethality section, merge notes for ch33/ch43/ch44, orphan note for former LW §39 (tripwires).
- Added BibTeX-key table at top of `lw-references.md` for drafted-chapter crosswalk.
- `./build.sh` succeeded (313 pages).

## Decisions
- LW manual entries live in both `external-alignment.bib` and `import_source_map_refs.py` because the import script overwrites category `.bib` files.
- Part VIII LW §32+§33 merged under book ch33 (Multi-Agent Superintelligence and Strategic Coupling); former LW §42 (Merging) placed under ch43 (Bearers); former LW §39 (Tripwires) kept as orphan under ch39.
- Pando Problem author confirmed as Jan Kulveit (2025).

## Open / next
- Expand ch05 LW curation when that chapter is drafted.
- Add BibTeX + prose citations for stub chapters as they are drafted (ch11+).
- Consider promoting orphan tripwire refs when ch39/ch40 safety-case text expands.

## Key paths
- `references/external-alignment.bib` — LW BibTeX keys
- `context/lw-references.md` — renumbered chapter index + key table
- `scripts/renumber_lw_references.py` — renumber helper (re-run after large lw-references edits)
- `chapters/ch01`–`ch04`, `ch06`–`ch10`, `ch40` — cited drafts

## Commits
- (none — user did not request commit)
