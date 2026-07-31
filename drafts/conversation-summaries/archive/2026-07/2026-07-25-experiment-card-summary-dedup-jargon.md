# 2026-07-25 — Experiment card summary/body dedup and jargon cleanup

## Trigger
User: "The experiment cards have duplication now because the summary at the start is almost identical to the start of the experiment line. Let's drop the summary." Then: "The experiment descriptions are partly jargon heavy. Do not use abbreviations and link to the relevant glossary." Then: "reserve the site" (interpreted as "serve the site"). Then: end of session.

## Done
- First pass: hand-edited the 6 generated `.md` files under `site/src/content/cards/experiments/` to drop the duplicate leading sentence. This was silently reverted by the next sync/build — those files are gitignored and regenerated from `metadata/experiments.yml` by `site/scripts/sync-experiments.mjs`.
- Traced the real source and fixed it there instead:
  - Rewrote `role` and `howToRead.text` for all 6 experiment lines in `metadata/experiments.yml` (agency-detect, toy-simulation, embedded-simulation, goal-agent-simulation, lab-simulation, graded-lab-simulation): spelled out abbreviations (UAD, CCI, BIQ, EAI, VFS, MBn) in plain language, and linked `correction-channel integrity`, `boundary discovery`, and `bridge assumptions` to their existing glossary/concept cards (`/cards/correction-channel-integrity/`, `/cards/boundary-discovery/`, `/cards/bridge-assumptions/`).
  - Fixed a latent bug in `lab-simulation`'s `role`: the auto-derived summary (first sentence up to a period) was truncating mid-word at `lab-sim-0.` because the version string `0.3.0+` contains periods; moved the version detail out of the first sentence.
  - Fixed the actual duplication bug at its root in `site/scripts/sync-experiments.mjs`: added `bodyWithoutDuplicateSummary()` so the card body strips the leading sentence already used as the frontmatter `summary`, instead of repeating it. This persists across future `npm run sync:experiments` / `npm run sync` runs.
- Regenerated cards (`node scripts/sync-experiments.mjs`) and did a clean `rm -rf dist .astro && npm run build` to confirm: no stale content, glossary links resolve to real card routes, no more truncation or duplication.
- Ran `./serve-site.sh` (full `npm run sync` pipeline + dev server) at the user's "reserve the site" request, confirmed it serves on `http://localhost:4321/`.

## Decisions
- Left the "Headline findings" bullets on each experiment card as-is (still contain UAD/GL-xx/LS-xx/D1-D4/S6-S7 style codes). Those are auto-extracted from `**Key finding:**` tags in each line's `experiments/*/results/FINDINGS.md` / `NEGATIVE_RESULTS.md` — a separate, more sensitive canonical research ledger that the site explicitly treats as "curated but still terse; full ledger on GitHub." Rewriting those would mean editing the tagged sentences directly in the ledgers, which I flagged to the user rather than doing unprompted.
- Did not touch other in-flight untracked work from parallel sessions (ET-2/CIL adapter files, PR #1 rebase, hostile-review.md) — out of this task's scope per AGENTS.md staging discipline.

## Open / next
- If the user wants the "Headline findings" jargon reduced too, that requires editing the `**Key finding:**` tagged sentences in `experiments/{embedded,graded-lab}-simulation/results/*.md` (and re-running `sync:experiments`), not just `metadata/experiments.yml`.
- Consider adding a UAD/BIQ/EAI glossary entry to `metadata/concepts.yml` if these terms keep recurring across experiment cards — currently only `boundary-discovery` and `correction-channel-integrity` have matching glossary cards.

## Key paths
- `metadata/experiments.yml` — source of truth for all 6 experiment-line summaries/bodies/how-to-read text.
- `site/scripts/sync-experiments.mjs` — generator; do not hand-edit `site/src/content/cards/experiments/*.md` directly, it's regenerated and gitignored.
- `site/src/data/glossary.json` / `metadata/concepts.yml` — existing glossary entries available to link from experiment prose.

## Commits
- (none yet — pending user's "commit" request in this same turn)
