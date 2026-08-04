# 2026-06-19 — Chapter 15 values compressed control draft

## Trigger
User provided a full draft for Chapter 15 and asked to integrate it into `chapters/ch15-values-compressed-control.tex`.

## Done
- Replaced stub chapter with full draft (~25 sections): basic shift, compression, loop-bottleneck-policy architecture, distinctions (preferences/emotions/goals/labels), candidate value directions, conflict, social correction, three alignment implications, toy model, counterexamples, value criteria, superintelligence implications, summary.
- Normalized LaTeX: display math `\[...\]`, fixed equation typos (`======`, markdown `##`, asterisk subscripts), proper quotes, `\mathcal{I}`, `\mathrm{do}`.
- Matched book conventions: `chapterthesis`, `epigraph`, `refsection`, section labels, `\printbibliography` with `\autocite` for keys in repo (Abbeel/Ng, Tishby, Conant–Ashby, Friston, Panksepp, Zarncke loop-hub / value-bottleneck).
- Kept existing label `ch:values-compressed-control`.
- Updated `metadata/book.yml` ch15 status: `stub` → `draft`.
- `./build.sh` succeeds (424 pages).

## Decisions
- Did not add a separate “What Would Change This View” section; user draft did not include it and draft already has “Counterexamples and limits.”
- Chapter references use existing `.bib` keys only; Clark, Haidt, Kahneman, Tomasello from draft bullet list omitted until bib entries exist.
- Sparse inline citations at natural anchors (compression, salience, bottlenecks, loop-hub) per source-canon ch15 note.

## Open / next
- ch16 value-bundle model still stub; natural follow-on from ch15 closing paragraph.
- Optional: add WWCTV section for parity with other Part IV chapters.
- Optional: import missing chapter-reference bib entries (Clark 2013, Haidt 2012, etc.) from deep-research report.

## Key paths
- `chapters/ch15-values-compressed-control.tex`
- `chapters/ch16-value-bundle-model.tex`
- `chapters/ch04-fixed-values-wrong-target.tex` (prior value framing)
- `references/internal-project-sources.bib` (`zarncke2025loop-hub-value`, `zarncke2026value-bottleneck`)

## Commits
- (none — user did not request commit)
