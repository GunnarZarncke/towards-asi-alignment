# 2026-08-20 — README accuracy sync

## Trigger
User asked whether `README.md` was still accurate after work since its last edit (2026-08-15 title tweak; last content pass 2026-08-03). Requested corrections and end-of-session commit.

## Done
- Audited README against Introduction six claims, field-agenda counts, Lean MB8 status, appendix lettering, and post–v1.4.0 repo state.
- Updated `README.md`: six-claims thesis wording; field crosswalk counts (30 records / 24 matrix rows / 29 cards); MB8 retired note; status/release snapshot; Appendix I vs `appN` source; formal-spine and symbol-census wording; papers list; prose typos in “What this is.”
- Synced `docs/MANUSCRIPT.md` to match (field counts, post–v1.4.0 themes, MB8 note, field hub v2).
- Trimmed redundant Part I preview paragraph from `frontmatter/introduction.tex` (covered in “How these claims unfold” and part roadmap).
- Session log + HANDOFF + INDEX updated.

## Decisions
- Kept release tag at v1.4.0 with a note that the repo has shipped further since (no new tag).
- Did not commit unrelated unstaged work (Anthropic field news, experiment zips, etc.).

## Open / next
- Other unstaged work in the tree (not committed here): Anthropic Risk Report field-news YAML/card, `2026-08-18-field-stance-icons.md` commit hash, assorted drafts and experiment zips.

## Key paths
- `README.md`
- `frontmatter/introduction.tex` (canonical six claims)
- `reference/field-agendas/data/matrix.yml`
- `docs/MANUSCRIPT.md` (follow-up sync)

## Commits
- `d527f2a3` Sync README with current six-claims spine and field state.
