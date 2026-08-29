# 2026-08-29 — Experiment site cards (GitHub, results, class overviews)

## Trigger
User asked that every specific experiment card have a marked GitHub source link and a results link; that simulations, external tests, and witness tests each have an overview card linked from `/experiments/`; and that those overviews use general technical language (glossary, not TSA jargon), with finding IDs only where they also link.

## Done
- Added class overview cards (`simulations`, `external-tests`, `witness-tests`) generated from `metadata/experiments.yml` `kinds.*.overview`.
- `/experiments/` hub cards link to those overviews; homepage tiles point at the same URLs.
- Line cards: `Source on GitHub` (git icon), site `Results`, `Results ledger` (git icon). ET annexes now resolve a parent findings ledger on GitHub.
- Restored `leanSpine` import on `cards/[...slug].astro` (it was dropped when adding `experiments.json`; that broke prerender of Lean playgrounds on cards such as adversarial-boundary-discovery).
- Public `summary` per line. Witness titled **Witness**; copy asks whether a check would have stopped a concrete stretch of what happened in histories we did not write.
- One card per Witness test (`w-1`–`w-16`) listed on the Witness overview; combined `/cards/experiment/witness/` redirects to the overview. Folder-per-test under `experiments/witness-<name>/` deferred (shared dumps).
- Per-test cards: Host / Setup / Analysis / Numbers / Outcome (numbers last) from FINDINGS.
- Negative-results hub (`/cards/concept/negative-results/`) lists simulations, external tests, and Witness tests via `ExperimentLedgersTable` (line title links to card). Coverage page links to that card instead of duplicating the table. Toy-simulation added to `ledgers`.
- Findings pages render markdown (Witness Host/Setup/Analysis/Numbers/Outcome on `/experiments/findings/{id}/`).

## Decisions
- Three class overviews, not one card per W-id. Numbered witness findings stay on the battery card and ledger, linked from the witness overview.
- Source URL is the sibling repo, in-repo tree, or annex plan file. Results are the on-site findings page plus the GitHub ledger.

## Open / next
- Line-card how-to-read still uses some project jargon.

## Key paths
- `metadata/experiments.yml`
- `metadata/experiments-witness-tests.yml`
- `site/scripts/sync-experiments.mjs`
- `site/src/components/ExperimentLedgersTable.astro`
- `metadata/concepts/bodies/negative-results.md`
- `site/src/pages/experiments/index.astro`
- `site/src/pages/experiments/findings/[id].astro`
- `site/src/lib/render-markdown.ts`

## Commits
- `361626b1` Add per-test Witness cards and a unified negative-results ledger hub.
