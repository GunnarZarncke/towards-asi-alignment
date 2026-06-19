# 2026-06-18 — Session end: LW references, roadmap removal, status sync

## Trigger
User added `context/lw-references.md` to source-map reference instructions; removed outdated Roadmap chapter from the PDF; synced stale chapter status; session end and commit requested.

## Done
- **`context/lw-references.md`** — chapter-indexed LessWrong/external alignment references (new file).
- **`INSTRUCTIONS.md`** — §3.0 cross-ref; §11 subsection on LW references (manual `.bib` promotion); §5/§9/§25 updated (roadmap removed from book template and milestones).
- **`metadata/source-canon.md`**, **`README.md`**, **`scripts/import_source_map_refs.py`** — document `lw-references.md` workflow.
- **`book.tex`** — dropped `\input{frontmatter/roadmap}`.
- **`frontmatter/roadmap.tex`** — deprecation comment (no longer included in PDF).
- **`metadata/book.yml`**, **`tables/chapter-map.tex`**, **`README.md`** — synced draft status (Ch. 3–4, 6–10, 40 draft; Ch. 5 stub); milestone → third; chapter-map marked maintainer-only.

## Decisions
- Roadmap removed from PDF because status table was stale; `metadata/book.yml` is source of truth for chapter status.
- `lw-references.md` is human-edited curation, not auto-imported by `import_source_map_refs.py`.
- Session commit excludes unrelated edits in `ch40-lethality-stress-test-open-issues.tex` and `2026-06-17-ch03-dynamical-guarantee-draft.md`.

## Open / next
- Wire `\autocite` keys from `lw-references.md` into drafted chapters as citations are added.
- Finish Ch. 5 (Part I gap); preface and executive overview still stubs.
- Deferred: book-level epistemic-status pass (Ch. 1 WWCTV; standardize disconfirming sections).
- Branch ahead of `origin/main` (4 commits after this one); push when ready.

## Key paths
- `context/lw-references.md`
- `metadata/book.yml`, `tables/chapter-map.tex`
- `INSTRUCTIONS.md` §11

## Commits
- `aa02b61` Document LW references workflow and remove stale roadmap from the book.
