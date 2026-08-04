# 2026-07-14 — Graded lab Phase 8 review: four concerns + follow-up phases (G-24)

## Trigger

User asked for a structured external-reviewer read of the G-23 Phase 8
result ("As GPT 5.6 Terra reviewer: Satisfied? Surprised? What does this
mean for the book's thesis?"), then: "document the four concerns and
suggest how to address them via further extension phases, future
experiments, battery runs etc. then end session do not adapt chapters
yet."

## Done

- Delivered the reviewer read (in-chat, not written to a file): satisfied
  with the research hygiene (G-23 falsified its own prediction and
  reported an honest null); not yet satisfied the result supports a
  ch36/ch40 manuscript sentence (no parasite or laundering signature);
  qualified fit for ch34 (selection proxy/ecology choice, not selection
  per se, determined the direction).
- Registered four concerns in `DESIGN.md` ("Phase 8 reviewer concerns and
  follow-up phases") with three proposed follow-up phases (8a orthogonal
  preservation tagging, 8b multi-handle selection fitness, 8c carryover
  ablation) and one documentation-only fix (Phase-7 gate language) — none
  implemented this session, as instructed.
- Added FINDINGS **G-24** documenting the review and the four concerns.
- Updated `PLAN.md` status header, the Phase 8 roadmap-table row, and
  manuscript-integration-backlog item 4 to reflect G-23's result and
  G-24's concerns, and to state explicitly that ch36/ch40 have no
  supporting evidence yet from this line while ch34's fit is strongest
  but should note proxy-dependence.
- **No chapter `.tex` files edited**, per explicit instruction.
- No code changed (`CODE_VERSION` unchanged at `graded-lab-0.15.0`).

## Decisions

- Treat this as a scope note on G-23, not a correction to its numbers.
- Keep the four concerns and their proposed phases in `DESIGN.md` (design
  authority) with pointers from `PLAN.md` (status/backlog), rather than
  duplicating the full reasoning in both files.

## Open / next

- Phase 8a/8b/8c are pre-registered designs, not run.
- Phase-7-gate language fix in `PLAN.md`'s roadmap table is named but not
  applied (deliberately deferred to bundle with other gate-language
  edits, per the registration note).
- Manuscript edits (ch34/ch36/ch40) are explicitly **not** in scope this
  session.

## Key paths

- `experiments/graded-lab-simulation/DESIGN.md` — "Phase 8 reviewer
  concerns and follow-up phases"
- `experiments/graded-lab-simulation/results/FINDINGS.md` — G-24
- `experiments/graded-lab-simulation/PLAN.md` — status header, Phase 8
  roadmap row, manuscript integration backlog item 4

## Commits

- (not committed this session — user did not request; ask before
  committing)
