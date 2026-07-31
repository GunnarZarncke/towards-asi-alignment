# 2026-06-25 — Assumptions ledger collation

## Trigger
User asked to collate all book assumptions including Lean into `metadata/assumptions-ledger.md` (not included in the book).

## Done
- Rewrote `metadata/assumptions-ledger.md`: manuscript A-001–A-010, Lean scaffold note, S01–S09, MB1–MB8 (+ MB7a–c), cross-reference maps to ch05, Executive Overview, claims/uncertainty ledgers.
- Updated `tables/assumptions-table.tex` summary (still not `\input` in `book.tex`).
- Updated `metadata/TODO.md` ledger item.

## Decisions
- Three layers: manuscript **A***, Lean imported **S***, Lean bridge **MB***; abstract Lean carriers documented as scaffold, not empirical assumptions.
- A-003 (societal correction capacity) stays outside MB* — scope gate, as in Appendix H.
- MB7 documented as chain MB7a→MB7b→MB7c matching Core.lean.

## Open / next
- Wire BibLaTeX keys into claims-ledger `References:` placeholders when revising chapters.
- Link new U-ledger rows to A-008–A-010 if those uncertainties get dedicated entries.

## Key paths
- `metadata/assumptions-ledger.md`, `tables/assumptions-table.tex`, `formal/AlignmentProofSpine/Core.lean`

## Commits
- none (not requested)
