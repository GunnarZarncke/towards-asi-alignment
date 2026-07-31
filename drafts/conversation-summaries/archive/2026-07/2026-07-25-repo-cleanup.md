# 2026-07-25 — Repo cleanup, simplification, and archival

## Trigger
The user asked for a project review and cleanup according to the archival and erasure guidance in `AGENTS.md`, then authorized the cleanup plan and committing the finished untracked work.

## Done
- Repaired `drafts/conversation-summaries/INDEX.md`: all 442 log filenames on disk now have exactly one valid index link; corrected four renumber-corrupted log headings and removed phantom/duplicate rows.
- Retired the dead chapter-map and assumptions-index generation chains. The build now generates only the live part roadmap and remaining fragments; `make check` and `./build.sh` pass.
- Corrected appendix counts, experiment-line counts, stale appendix letters, release tag/path/recency language, and the assumptions-ledger documentation.
- Archived completed review plans, spent drafts, one-off context reports, orphaned tables, superseded roadmap, and one-off migration scripts under documented `attic/` directories.
- Added extracts for the two newly supplied context PDFs and corrected the archived `vision` pitch filename.
- Reclaimed the duplicate leak-proof Lean build (about 6.3 GiB) and cleared regenerable LaTeX outputs with `clean.sh`.
- Prepared the finished untracked artifacts for the requested scoped commit: hostile-review move, CIRIS reply, SOO benchmark note, concept-logo generator and SVGs, and the two context PDFs with extracts.

## Decisions
- `appL-assumptions.tex` was archived rather than wired into the PDF because it was orphaned and its documented Appendix E claim was false; `metadata/assumptions-ledger.md` remains maintained source material.
- `review/fix-plans-2026-06-22.md` remains active and was not archived.
- Closed TODO narrative compaction, anti-pattern synchronization in `llms.txt`, and generated symbol-graph SVG policy were left as deferred editorial/build work rather than silently rewriting broad history or breaking the site input contract.
- Unrelated concurrent working-tree changes in manuscript chapters, site, references, and field-news files were deliberately excluded from the cleanup commit.

## Open / next
- Consider compacting the 24 closed `metadata/TODO.md` narratives into one-line outcomes with session-log links.
- Synchronize the standalone `llms.txt` anti-pattern block with `REVIEWING_FOR_AGENTS.md`.
- If desired, add a reproducible render step before untracking `metadata/symbol-census/graphs/*.svg`.

## Key paths
- `drafts/repo-cleanup-plan.md`
- `drafts/conversation-summaries/INDEX.md`
- `review/attic/`, `drafts/attic/`, `scripts/attic/`, `context/attic/`
- `scripts/generate_tables.py`, `scripts/generate_manuscript_tex.sh`

## Commits
- Pending scoped cleanup commit.
