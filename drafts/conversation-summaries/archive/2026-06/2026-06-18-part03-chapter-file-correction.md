# 2026-06-18 — Part III chapter file correction

## Trigger
User: chapter 12 should be capability growth and chapter 13 should be coordination bottleneck per INSTRUCTIONS; drafts were in wrong files.

## Done
- Moved **Capability Growth Is Boundary Expansion** draft: `ch11` → `ch12-boundary-expansion.tex`.
- Moved **The Coordination Bottleneck** draft: `ch12` → `ch13-coordination-bottleneck.tex`.
- Restored `ch11-capability-without-task-ontology.tex` as stub (Measuring Capability Without Task Ontology).
- Updated ch12 opening bridge (from ch11 measurement, not ch10 opacity); added bridge to ch13 at conclusion.
- Updated `metadata/book.yml`, `tables/chapter-map.tex`.
- ch14 opening now cites `\ref{ch:coordination-bottleneck}`.
- `./build.sh` succeeds.

## Decisions
- ch11 left as scaffold stub; measurement draft not yet written (content was boundary-expansion draft).
- Labels unchanged: `ch:capability-growth-boundary-expansion` (ch12), `ch:coordination-bottleneck` (ch13).

## Open / next
- Draft ch11 Measuring Capability Without Task Ontology (BIQ / task-agnostic competence).
- ch12/ch13 may need WWCTV sections for full §10 parity.

## Key paths
- `chapters/ch11-capability-without-task-ontology.tex` (stub)
- `chapters/ch12-boundary-expansion.tex` (draft)
- `chapters/ch13-coordination-bottleneck.tex` (draft)
- `INSTRUCTIONS.md` lines 606–608

## Commits
- (none)
