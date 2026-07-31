# 2026-06-25 — Research program appendix (appH)

## Trigger
User asked to write the research program appendix as a dense plan collecting bridge assumptions needing empirical validation and chapter ``What Would Change This View'' investigations, without milestones or timelines.

## Done
- Replaced stub `appendices/appF-research-program.tex` with full research plan:
  - § Bridge assumptions MB1–MB8 (+ MB7a–c) with validate/falsify items tied to Appendix I and book chapters
  - § Cross-cutting adversarial verification program (ch47 master crux)
  - § Chapter disconfirmation investigations by part (ch01–ch48), cross-referencing WWCTV sections where labeled
  - § Relation to other appendices
- `./clean.sh && ./build.sh` passed (pre-existing citation warnings only).

## Decisions
- Dense index format: consolidated WWCTV prose into investigation bullets, not duplicated full chapter text.
- No schedule, milestones, or funding structure.
- ch48 WWCTV referenced via `sec:what-would-change-ch48` (no `sec:wwctv-*` label in that chapter).

## Open / next
- Optional: sync `metadata/open-problems.md` bullets to appH or vice versa on next metadata pass.
- ch48 and ch46 remain stubs; their WWCTV items are included but may expand when chapters grow.

## Key paths
- `appendices/appF-research-program.tex`
- `appendices/appG-lean-proof-spine.tex` (MB assumptions)
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`

## Commits
- (none this session)
