# 2026-08-29 — Witness card bridge links and GitHub path linkify

## Trigger
Follow-up on experiment site cards: each Witness test card should link to the bridges/claims it witnesses and explain why; experiment paths in card copy should link to GitHub; end-of-session commit.

## Done
- Added required `witnesses` field (bridge/concept bullets + why) for all W-1–W-16 in `metadata/experiments-witness-tests.yml`; sync renders **Witnesses.** on experiment cards.
- W-1 renamed **CIRIS Named-identity mock**; CIRISAgent, Verify, Lens, Wise Authority, and fixture/checker files linked; removed `experiments/witness/memo-eric-named-identity.md` and its FINDINGS artifact line.
- Split experiment card vs findings page: cards carry setup + one-line finding; `/experiments/findings/{id}/` shows Numbers + Outcome (Witness) and key findings only, with lede link back to experiment card.
- `sync-experiments.mjs`: `linkifyExperimentPaths()` auto-links bare `experiments/...` and `python3 experiments/...` in card copy at sync time.
- `check-experiments.mjs`: requires `witnesses` for `kind: witness`.
- Re-synced `site/src/data/experiments.json`.

## Decisions
- Witnesses section sits after What/Why, before Host — general-audience one-line why per bridge/concept.
- Path linkify at sync time (not hand-editing every YAML path); skip paths already inside markdown links or GitHub URLs.
- Did not commit unrelated `chapter-reading-graph.json` timestamp or `drafts/alignment-crux-map/.mplconfig/`.

## Open / next
- Folder-per-test under `experiments/witness-<name>/` still deferred (shared kernel/OSF dumps).
- Line-card how-to-read still uses some project jargon.

## Key paths
- `metadata/experiments-witness-tests.yml`
- `site/scripts/sync-experiments.mjs`
- `site/scripts/check-experiments.mjs`
- `site/src/lib/render-markdown.ts`
- `site/src/pages/experiments/findings/[id].astro`

## Commits
- (this session)
