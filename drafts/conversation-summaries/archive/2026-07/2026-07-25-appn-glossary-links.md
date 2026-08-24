# 2026-07-25 — Appendix N jargon: glossary entries + links instead of inline explanation

## Trigger
Follow-up to the same day's experiment-card jargon cleanup: user asked whether `appendices/appN-experimental-evidence.tex` was in sync with the site-side wording changes. It was not (same old abbreviation-heavy phrasing). User chose to keep the appendix's own wording but add first-use expansions/footnotes for UAD/CCI/BIQ/MBn there — then refined that to: (a) put the abbreviation definitions in the Operational Glossary (Appendix E) instead of inline, and (b) have Appendix N link to those definitions rather than re-explain them.

## Done
- Added a new "Experimental-methodology shorthand" section to `appendices/appE-glossary.tex` defining `UAD` (Unsupervised Agent Discovery), `VFS` (virtual filesystem), and `BIQ`/`EAI` (boundary-information quality / emergent-ambiguity index), each with a `\label{gloss:...}` anchor, in the glossary's existing paraphrase-first voice. Added `\label{gloss:cci}` to the pre-existing `Correction-channel integrity` entry so it can be linked to as well.
- In `appendices/appN-experimental-evidence.tex`: replaced the standalone "Abbreviations used below" paragraph (from the prior turn) with a one-line pointer to the glossary and to Appendix B's bridge crosswalk, and added `\hyperref[gloss:...]{...}` links at each abbreviation's *first* prose occurrence per experiment-line section (agency-detect → UAD; toy-simulation → CCI + MB range; embedded-simulation → VFS; graded-lab-simulation → BIQ/EAI). Later occurrences and table cells stay plain, per normal convention.
- Verified with a clean two-pass `pdflatex -halt-on-error book.tex` compile: no undefined-reference/undefined-hyperref warnings for any of the new labels after the second pass (first-pass warnings are the normal LaTeX "labels not yet known" artifact). Ran `./clean.sh` afterward to remove build byproducts.

## Decisions
- Chose `\hyperref[label]{text}` (not `\ref`) for the in-appendix links, since the glossary uses unnumbered `\section*{}` entries — `\ref` alone would just print the enclosing chapter number, not a useful anchor; `\hyperref` gives a working PDF jump-to-anchor regardless.
- Left the "Bridge and feature coverage" section's own tables/subsection headings unlinked — that section already spells out each bridge's full name per table row, so it's self-explanatory without further links.
- Did not touch parallel in-flight work from other sessions in the same tree (ET-2/CIL adapter files, the `hostile-review.md` → `drafts/` rename, `FINDINGS.md` edits) — out of this task's scope.

## Open / next
- If new experiment-methodology abbreviations get introduced later (e.g. in a future line), add them to the same "Experimental-methodology shorthand" glossary section rather than inlining explanations in Appendix N again.
- `docs/EXPERIMENTS.md` (the full narrative doc) still uses these abbreviations without links/expansions — out of scope for this pass since it's plain Markdown prose for developers, not manuscript-facing, but worth a similar pass if it's ever surfaced to a general audience.

## Key paths
- `appendices/appE-glossary.tex` — Operational Glossary; new "Experimental-methodology shorthand" section near the end.
- `appendices/appN-experimental-evidence.tex` — per-line intro paragraphs now link out instead of explaining inline.

## Commits
- (pending — see this session's commit)
