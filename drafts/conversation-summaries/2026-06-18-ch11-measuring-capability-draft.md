# 2026-06-18 — Chapter 11 measuring capability draft

## Trigger
User provided full draft for chapter 11 and asked to integrate into `chapters/ch11-capability-without-task-ontology.tex`.

## Done
- Replaced ch11 stub with integrated draft (~5,500 words): *Measuring Capability Without Task Ontology*.
- Book conventions: `chapterthesis`, `refsection`, epigraph, `\MI`, `B_X` notation aligned with ch12, BibLaTeX refs, section labels.
- Opening bridge from ch10 (strategic opacity); closing bridge to ch12 (boundary expansion).
- Renamed draft's "The shaky points" → `\section{What Would Change This View}`; Summary as 6 bullets + bridge.
- Fixed duplicate label `sec:example-firm` → `sec:example-firm-capability`.
- Updated `metadata/book.yml` and `tables/chapter-map.tex` (ch11 → draft).
- `./build.sh` succeeds.

## Decisions
- Used Shape B (native narrative); kept draft section structure rather than forcing Plain-Language/Formal split.
- Horizon notation `h` (not `\tau`) per draft note on opacity collision.
- Added funding-gap and percolation cites per `metadata/source-canon.md` suggestions.

## Open / next
- Resolve remaining duplicate labels: `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- ch12/ch13 WWCTV sections if full §10 parity desired.

## Key paths
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch12-boundary-expansion.tex` (downstream; already bridges from ch11)

## Commits
- (none)
