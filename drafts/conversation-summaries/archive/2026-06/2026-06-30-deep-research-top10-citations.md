# 2026-06-30 — Deep-research top-10 citations (minus ARA)

## Trigger
User asked to implement the top 10 priority citations from `context/full-book-deep-research-report.md`, excluding #9 (Kinniment ARA).

## Done
- Added 9 BibTeX entries: `kelly2004gsn`, `gsn2021standard`, `leveson2011esw`, `schwartz2012refining`, `wen2024mislead`, `shah2022goalmisgeneralization`, `langosco2022goalmisgeneralization`, `pan2024rewardhacking`, `greenblatt2024alignmentfaking`.
- Surgical `\autocite{}` inserts and chapter-reference updates in ch03, ch14, ch17, ch19, ch46–ch46, ch48–ch48, ch46, ch48, ch46.
- Replaced mis-aimed `kelly1998safety` safety-case cites with `kelly2004gsn` (+ GSN standard / Leveson where appropriate).
- Added `references/bibliography-summaries.tex` glosses for new keys.
- `./build.sh` succeeds (pre-existing undefined ref `ch:detecting-goal-laundering` unchanged).

## Skipped
- Kinniment et al. (2023) ARA evals (#9) per user request.

## Open
- Wire NIST/EU AI Act into core chapters (already in `.bib`, cited in appJ only).
- Remaining deep-research list (Cyert, Rosenblueth, Constitutional AI, etc.).
- Optional: retire or relabel orphan `kelly1998safety` entry (Kevin Kelly 1998 philosophy paper).

## Key paths
- `references/manuscript-citations.bib`, `references/external-alignment.bib`
- `chapters/ch03-dynamical-guarantee.tex`, `ch46-safety-case.tex`, `ch14-intelligence-deepens-misalignment.tex`, `ch46-transport-types.tex`, `ch46-correction-channel-integrity.tex`
