# 2026-07-24 — ET-1 site cards, experiments-page simplification, and commit

## Trigger
Follow-on to the same-day ET-1 conclusion session
(`2026-07-24-et1-lockstep-fsm-root-cause.md`): user asked (1) whether the
ET-1 result is viewable on the site and which card, (2) to add cards for
the experiment and its results and simplify the main experiments page, and
(3) for a dedicated card listing the ET line of experiments. Ended with
"end of session and commit".

## Done
- Answered the "which card" question: the ET-1 result had no `GL-` id and
  was absent from `metadata/experiments.yml` / the synced
  `graded-lab-simulation` experiment card.
- Assigned **GL-86** (the id `PLAN_ET1.md` had reserved) and wrote the full
  findings entry in `experiments/graded-lab-simulation/results/FINDINGS.md`.
- Updated `metadata/experiments.yml`: added the GL-86 headline finding,
  refreshed the `role`/`howToRead` text and the `mb1` coverage-table cell,
  and **consolidated** the `graded-lab-simulation` headline-findings list
  from 10 verbose bullets to 7 (merged the GL-18–22 ambiguity-band
  sequence into one, the GL-23–27 Phase-8 selection sequence into one, and
  the GL-80/81/84/85 PLAN_v4 rigs into one), replacing the stale "scope
  ceiling... decisive next validation is transfer" bullet with the GL-86
  result — this is what "simplify the main experiments page" resolved to,
  since that page (`site/src/pages/experiments/index.astro`) renders
  `headlineFindings` verbatim from this file with no template change
  needed.
- Regenerated `site/src/data/experiments.json` and the synced
  `graded-lab-simulation` card via `node scripts/sync-experiments.mjs`;
  validated with `node scripts/check-experiments.mjs`.
- Added a new concept card, **`et-external-transfer`** ("ET Line:
  External-Substrate Transfer Tests"), naming the ET line as a concept in
  its own right with GL-86 as its first `evidenceNotes` entry
  (`finding: bound` — a substrate-suitability limit, not a support/negative
  on UAD itself). Initially wrote this as a standalone file directly under
  `site/src/content/cards/`, then **corrected it**: that directory (for
  hand-authored concept cards) is generated from `metadata/concepts.yml` +
  `metadata/concepts/bodies/*.md` via `sync-concepts.mjs` and is gitignored
  per-file — a raw drop-in there would be silently lost or drift from the
  yaml roster. Moved the content into a proper `metadata/concepts.yml`
  roster entry + `metadata/concepts/bodies/et-external-transfer.md`, added
  the generated path to `site/.gitignore`, and regenerated.
- Cross-linked the new card from `related:` on the four cards that should
  point to it — again correcting an initial mistake of editing the
  *generated* `.md` cards directly instead of their `metadata/concepts/
  bodies/*.md` (or `metadata/bridges/...`) sources:
  `intervention-supported-unit-discovery`, `unit-discovery-stress-test`,
  `mb1-boundary-estimator-soundness`, `experiment-methodology`,
  `evidence-and-uncertainty`. Added `et-external-transfer` to appN's
  `related` list in `site/scripts/sync-chapter-cards.mjs`.
- Validated the whole change with `node scripts/sync-concepts.mjs`,
  `sync-chapter-cards.mjs`, `sync-experiments.mjs`, and `npx astro sync`
  (content-collection schema check) — all clean.
- Noticed and reverted an unrelated regenerated artifact
  (`metadata/symbol-census/graphs/symbol-formula-graph.svg`, ~31k line
  diff) that one of the site scripts touched as a side effect; not part of
  this task, reverted via `git checkout --`.

## Decisions
- Assigned GL-86 to ET-1's conclusion rather than leaving it unnumbered,
  since `PLAN_ET1.md`/`PLAN_IA1.md` had already reserved it and the site
  pipeline keys headline findings off numbered ids.
- Used `finding: bound` (not `negative`) for the ET-1 `evidenceNotes` entry
  on the new card, matching the corrected framing from the same-day
  reframing session: this is a substrate-suitability limit on where the
  instrument can be tested, not a detector defect.
- Kept the experiments-page simplification data-only (trimmed
  `metadata/experiments.yml`); did not touch
  `site/src/pages/experiments/index.astro`, since it already renders
  `headlineFindings` generically and the bloat was in the data, not the
  template.

## Commit scope note
This session's changes were committed. The following untracked material
in the working tree at commit time was **not** part of this conversation
and was left uncommitted:
- ET-2 (CIL) line: `experiments/graded-lab-simulation/PLAN_ET2.md`,
  `graded_lab/external/cil_*.py`, `external/cil/`,
  `scripts/run_et2_uad_battery.py`, `tests/external/test_cil_adapter_golden.py`
  + its fixture, and the matching `.gitignore` lines — appears to be a
  separate, parallel session's work (`drafts/conversation-summaries/
  2026-07-23-et2-cil-adapter-build.md`, already indexed in `INDEX.md`
  though its own log file is still untracked).
- Unrelated drafts and context files already dirty/untracked at the start
  of this conversation: `context/*`, `drafts/ciris-accord-reply-eric-moore.md`,
  `drafts/foresight-secure-sovereign-ai-workshop-slides.md`,
  `drafts/soo-benchmark-scenarios-from-book.md`, `drafts/ai-salon-uad-demo-slides.md`,
  `book.bcf-SAVE-ERROR`, `AGENTS.md`, `hostile-review.md`, and several
  `drafts/conversation-summaries/2026-07-19-*.md` /
  `2026-07-20-riskgap-*.md` edits from other sessions.

## Open / next
- ET-2 (CIL) work is uncommitted and unmentioned in this conversation's
  scope; flag to the user for a separate review/commit pass.
- No further ET-1 Orbit work planned (see prior log); GL-86 and the
  `et-external-transfer` card are the closing artifacts for this line.

## Key paths
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-86 entry)
- `metadata/experiments.yml`, `site/src/data/experiments.json`
- `metadata/concepts.yml`, `metadata/concepts/bodies/et-external-transfer.md`
- `metadata/concepts/bodies/{evidence-and-uncertainty,experiment-methodology,intervention-supported-unit-discovery,mb1-boundary-estimator-soundness,unit-discovery-stress-test}.md`
- `site/scripts/sync-chapter-cards.mjs`, `site/.gitignore`

## Commits
- See repository log for this session's commit (ET-1 conclusion + site
  cards); ET-2 line intentionally excluded.
