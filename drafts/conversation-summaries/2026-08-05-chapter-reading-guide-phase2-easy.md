# 2026-08-05 — Chapter reading guide Phase 2 (easy audit + ch09)

## Trigger
Run the easy rollout audit (all zero- and one-edge chapters) and include ch09 on request.

## Verdict
**No new `readingguide` blocks.** The audit checked 30 chapters: 15 entry chapters with no incoming DAG edges, 15 one-edge chapters, plus ch09 (two edges).

- **Entry chapters:** all self-start or define their needed machinery locally.
- **One-edge chapters:** all direct prerequisites are either bridged in the prior chapter's close / current opening, or enter later in the local argument rather than at the chapter door.
- **ch09:** omit. Its opening restates the wrong-object problem, gives the dynamically coherent composite-agent criterion, and states the approximate boundary condition; neither ch01 nor ch06 remains an unbridged prerequisite.

Forward references were treated as roadmaps, not prerequisites: in particular ch19 → ch16/ch18, ch29 → ch26, ch35 → ch34, and ch37 → ch33/ch34/ch36.

## Decision
A direct reading-DAG edge is an audit prompt, not sufficient reason to add a reader-facing box. ch07 remains the sole `readingguide` after Phases 1–2.

## Follow-up
- **ch09 clarification:** removed Peter Kuhn's TODO and clarified, at the start of §`sec:object-level-mistake`, that the chapter concerns the **object of alignment** (the system whose future behaviour must be constrained), not the authority entitled to provide constraints. Added the component-alignment / system-alignment distinction before the composite claim.

## Open / next
- **Phase 3:** audit chapters with two or three direct edges, starting with ch11, ch17, ch24, ch31, ch34, ch38, ch40, ch47, and ch48.
- Re-run checklists only when openings or dependency edges change.
