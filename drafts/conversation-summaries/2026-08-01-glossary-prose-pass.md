# 2026-08-01 — Inter-agenda glossary source-backed prose pass

## Trigger
User asked for the deferred prose pass: consult each source; replace one-line stubs with genuine translation and explicit why-not-the-same disambiguation; use subagents.

## Done
- Quality bar + merge tooling under `drafts/glossary-prose-pass/` (`QUALITY.md`, `merge_batches.py`, `THIN.md`).
- Four parallel rewrite batches (152/152 headwords):
  - A–C (49) → `batch-A-C.md`
  - D–I (35) → `batch-D-I.md`
  - K–R (34) → `batch-K-R.md`
  - S–W (34) → `batch-S-W.md`
- Merged into `reference/field-agendas/inter-agenda-term-glossary.md`; restored Terms-by-agenda index + Maintenance; fixed entry spacing.
- Entry format upgraded (2–4 sentence Definitions; mechanism-level Not the same as; tagged Cross-agenda with explanation).

## Decisions
- Book remains one agenda among others (not translation target).
- App E / manuscript integration still deferred.
- Thin/contested leftovers tracked in `THIN.md` rather than blocking merge.

## Open / next
- Second accuracy pass on `THIN.md` entries when better primaries exist.
- Manuscript terminology demotion per `drafts/glossary-term-audit.md`.
- Optional App E ↔ glossary mapping pass.

## Key paths
- `reference/field-agendas/inter-agenda-term-glossary.md`
- `drafts/glossary-prose-pass/`

## Commits
- (pending user request)
