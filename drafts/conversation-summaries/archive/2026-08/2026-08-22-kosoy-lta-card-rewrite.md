# 2026-08-22 — Kosoy LTA card rewrite

## Trigger
Vanessa Kosoy found the research-agenda summary hard to parse: it phrased LTA through book vocabulary, lumped unlike objects, misstated PSI/bridge-transform/precursor, and used opaque “type” / “survive simulation” / bundle-transport language.

## Done
- Rewrote `reference/field-agendas/data/agendas/kosoy-infra-bayesianism-lta.yml` in LTA’s own terms (theory of intelligent agents; regret as a standard; nonrealizability/daemons as problems; IB then IBP/bridge transform; PSI as superimitation after agent/user identification; PreDCA precursor as the 2022 formulation).
- Book mapping moved to “how this project treats it”: translate value-bundle-transport / bearer-persistence / correction, and treat sufficiency as an open disagreement rather than a verdict that PSI is missing those pieces.
- Updated glossary PreDCA/PSI row, evidence 123, specify/construct peer row, alignment-target instance line, App B table label, maintainer diagnostic.
- Regenerated site cards / field JSON.
- Added Vanessa Kosoy to `metadata/feedback-contributors.md` (also restored the missing `[` on the Krym row).

## Decisions
- Follow 2023 LTA status for PSI (superimitation, agent detection, user identification), not 2022 PreDCA as if it were current.
- Mention FCR/COSI renames once; keep PSI/PreDCA as the names Kosoy used in the feedback.
- “Survive simulation” → whether user identification works under simulation hypotheses.

## Open / next
- Optional: send Kosoy the revised card for a second pass. Correction-channel remaining-open is still a book question she may reject.
- Not staged this commit: `RELEASE_NOTES.md` (v1.5.0 draft, not tagged), `site/.gitignore` (v1.5.0 card ignore), `site/src/data/chapter-reading-graph.json`, untracked `2026-08-22-v1-5-0-release-notes.md`.

## Key paths
- `reference/field-agendas/data/agendas/kosoy-infra-bayesianism-lta.yml`
- `site/src/content/cards/field-agendas/kosoy-infra-bayesianism-lta.md`

## Commits
- `b5bb11f7` Rewrite the Kosoy LTA agenda summary in her terms.
