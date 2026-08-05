# 2026-08-05 — Chapter reading guide Phase 1 pilots

## Trigger
Implement the easy, medium, and hard `readingguide` pilots after the Phase 0 infrastructure commit.

## Bridge-audit verdicts
- **ch25 (easy): omit.** Chapter 24's closing points directly to correction as a causal channel, while ch25's opening and canonical causal-model section rebuild the correction chain from first principles. The only direct graph symbol (`\pi`) is introduced as ordinary policy notation in ch25 rather than a load-bearing imported concept.
- **ch40 (medium): omit.** Its opening defines goal laundering, its four goal layers, and the relevant transport stack. The remaining direct DAG providers (`ch41`, `ch43`) are later chapters, so they cannot be entry prerequisites; their material remains later validation/context rather than an assumed starting point.
- **ch07 (hard): add.** Its opening already restates the wrong-object framing and the agent definition, but not the book's scope condition from ch05. Added one prerequisite item for correction capacity, followed by names-only `Defines here`.

## Done
- **`chapters/ch07-finding-boundary.tex`:** added the first `readingguide` block after `chapterthesis`.
- Regenerated checklists and synced chapter content to the companion site.
- `make check` passed: manuscript structure, citations, and bibliography summaries.

## Decision
The pilot validates that the bridge audit can end in an intentional omission. A graph edge alone is not sufficient reason to add a reader-facing block.

## Open / next
- Phase 2 easy audit: remaining zero- and one-edge chapters.
- Do not wire checklists into `make generate` until their regeneration cadence is deliberately decided.
