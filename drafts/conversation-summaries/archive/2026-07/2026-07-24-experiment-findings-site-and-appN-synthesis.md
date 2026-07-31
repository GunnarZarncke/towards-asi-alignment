# 2026-07-24 — Experiment findings site UX, key-finding extraction, appN chapter synthesis

## Trigger
Follow-on after ET-1 site cards commit: user found site findings unreadable (terse full ledgers, everything linking to GitHub). Requested auto-extractable key findings in source ledgers, on-site short summaries, experiment cards as primary destinations, and a chapter-language synthesis at the top of the experiments page — then the same synthesis in `appN`. Ended with "end of session and commit this".

## Done
- **`**Key finding:**` convention** in `experiments/graded-lab-simulation/results/FINDINGS.md` (7 anchor entries: GL-12, GL-14, GL-22, GL-27, GL-79, GL-85, GL-86); `site/scripts/sync-experiments.mjs` auto-extracts these into `headlineFindings`; manual duplicate list removed from `metadata/experiments.yml` for graded-lab.
- **Removed full ledger mirror on site** — deleted `site/src/pages/experiments/ledgers/[id].astro`, dropped `experiment-ledgers` content collection, stopped syncing multi-thousand-line ledger copies; GitHub is canonical for full history.
- **On-site key findings pages** — new `site/src/pages/experiments/findings/[id].astro` (curated bullets + link to full ledger).
- **Experiments hub refactor** — `/experiments/` is now an index: card grid linking to `/cards/experiments/{line}/`, build-order and negative-results callouts point to cards + key-findings pages; per-line inline duplicate sections removed.
- **Link plumbing** — `sync-experiments.mjs` adds `cardPath`/`cardUrl` and splits external links into "Key findings" (site) vs "Full ledger (GitHub)"; reading paths and negative-results card updated.
- **Chapter synthesis (4 paragraphs)** — added to top of `/experiments/` and to `appendices/appN-experimental-evidence.tex` as `\section{What the lines say about the chapters}` (`sec:appn-chapter-synthesis`), in chapter/WWCTV language not experiment-line jargon.
- Documented extraction convention in `site/README.md`.

## Decisions
- **`**Key finding:**` over YAML duplication** — site headline bullets are extracted from tagged paragraphs in each line's ledger; `headlineFindings:` in `experiments.yml` is fallback only for lines not yet retrofitted.
- **Three-tier findings UX** — experiment card (primary) → `/experiments/findings/{line}/` (curated) → GitHub ledger (complete); removed redundant on-site full-ledger mirror.
- **Chapter synthesis is hand-authored** in page template + appN (judgment layer, not auto-generated from tags); mapped to appN's existing chapter citations and WWCTV `\ref`s.

## Commit scope note
Not included: ET-2 (CIL) line, root `.gitignore` ET-2 lines, `AGENTS.md` erasure section, unrelated drafts/context, hostile-review edits.

## Open / next
- Retrofit `**Key finding:**` tags in other lines' FINDINGS/NEGATIVE_RESULTS (toy, embedded, goal-agent, lab) so site bullets auto-sync from source.
- Consider single-sourcing chapter synthesis (appN ↔ site) if it drifts.

## Key paths
- `site/scripts/sync-experiments.mjs`, `site/src/pages/experiments/index.astro`, `site/src/pages/experiments/findings/[id].astro`
- `experiments/graded-lab-simulation/results/FINDINGS.md`, `metadata/experiments.yml`
- `appendices/appN-experimental-evidence.tex`, `metadata/concepts/bodies/negative-results.md`

## Commits
- See repository log for this session's commit.
