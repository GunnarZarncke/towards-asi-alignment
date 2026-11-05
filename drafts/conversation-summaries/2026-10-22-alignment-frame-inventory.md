# 2026-10-22 — Alignment frame inventory and spinout

kind: new-work
uptake: status

## Trigger

User requested a complete object-by-measure inventory from TSA references and mentioned overviews, plus a spinout paper.
Prompts: paraphrase-only

## Done

- content: Created `drafts/alignment-frames-by-object-and-measure.md`, a typed inventory separating alignment objects, assessments or guarantees, quantifiers, and warrants.
- content: Created `drafts/alignment-frames-spinout-paper.md`, a paper draft using TSA as a running example without treating neighboring frames as rival guarantees.
- content: Both deliverables were independently reviewed; the resulting corrections and claim-strength calibrations were incorporated.
- content: LaTeX spin-out at `papers/alignment-frames/` (`alignment-frames.tex`, `.bib`, `build.sh`). `./papers/alignment-frames/build.sh` wrote `alignment-frames.pdf` (18 pages).
- content: Relation note `drafts/alignment-frames-relations.md` and graph `drafts/alignment-frames-relations.dot`. `dot -Tsvg` accepted the graph.
- bookkeeping: Linked both deliverables from the Construct plan and the open Frame of the target item in `metadata/TODO.md`.
- bookkeeping: No manuscript files were edited.

## Decisions

- Hallgren's *Process Alignment* remains a private draft and must not be treated as public literature.
- The principal unresolved issue is an operational legitimacy test that distinguishes learning from capture.
- The Frame of the target item remains open because the planned manuscript revisions are not done.

## Open / next

- Define and test the operational legitimacy criterion for learning versus capture.
- Under the 2.0 manuscript gate, revise the inventoried chapters to label neighboring frames explicitly.

## Key paths

- `drafts/alignment-frames-by-object-and-measure.md`
- `drafts/alignment-frames-spinout-paper.md`
- `drafts/plans/construct/construct.md` § Frame of the target
- `metadata/TODO.md` § Construct
- `drafts/conversation-summaries/2026-10-22-frame-of-the-target.md` (plan decision log)

## Commits

- None.
