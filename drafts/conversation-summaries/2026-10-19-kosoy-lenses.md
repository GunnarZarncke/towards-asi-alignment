# 2026-10-19 — Kosoy lenses on TSA

kind: feedback
uptake: local

## Trigger
Apply Vanessa Kosoy's 18 October 2026 lenses where they inform TSA, add them to the review checklist, and update the App B crosswalk, which still excluded infra-Bayesianism after the Kosoy agenda card had been mapped onto bridges.
Prompts: paraphrase only (no prompt id)

## Done
- content: Ch. 10 quotes her side-channel case and leaves handle coverage open. Ch. 44 quotes her convergence lens on the first critical try, and points the deception row at the same side-channel case.
- content: App B splits logical induction (MB7d neighborhood) from the learning-theoretic agenda (mapped to MB1, MB2, MB3, MB5, MB7, MB9). PreDCA/PSI stays the outer-protocol row.
- content: `review/claim-checklist.md` gains the four lenses. Pointers in `review/reviewer-guide.md` and `REVIEWING_FOR_AGENTS.md`.
- bookkeeping: Bib `kosoy2026alignmentproblem` plus summary. Glossary, agenda hook, and the spine-translation example no longer say App B excludes infra-Bayesianism.
- bookkeeping: `scripts/check_bibliography_summaries.py` passed (557 summaries for 557 bib keys).

## Decisions
- Convergence and side channels are the lenses inserted into chapters. Hypercomplexity and grounding are checklist items only. They restate open bearer, value-change, and nonrealizability work.
- Logical induction stays a minimal cite. The stale combined row was the part that had not followed the agenda update.

## Open / next
- Site field-agenda card was not regenerated (`npm run sync:field-agendas`). The index and `field-agendas.json` spine-translation line were aligned by hand to `meta.yml`.
- The GDS / single-principal disagreement and the fixed-target regret point are not in the manuscript. They were in the comment draft only.

## Key paths
- `chapters/ch10-strategic-opacity.tex`
- `chapters/ch44-lethality-stress-test-open-issues.tex`
- `appendices/appB-bridge-crosswalk.tex`
- `review/claim-checklist.md`

## Commits
- none
