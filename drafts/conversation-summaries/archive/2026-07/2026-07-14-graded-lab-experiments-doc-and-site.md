# 2026-07-14 — Graded lab: added as line 5 to docs/EXPERIMENTS.md, metadata/experiments.yml, and the site

## Trigger

User, after the manuscript-harvest session: "Beside the chapters, where
should we update/add the findings? The README obviously. We should also
regenerate the site, but should we add anything to the site?"

## Done

Audited every place the four prior in-repo experiment lines are indexed
and found `graded-lab-simulation` — despite being explicitly named "the
fifth in-repo simulation line" in its own `PLAN.md` since Phase 0 — was
**entirely absent** from the two canonical cross-line documents:

- **`docs/EXPERIMENTS.md`** (canonical narrative): added a full "5.
  Graded-capability lab simulation" section (build order, phases 0–8
  narrative, G-11 through G-24 highlights, manuscript-harvest note) plus
  a `graded-lab-simulation` column across the entire feature-coverage
  matrix, including a new dedicated row ("Emergent ambiguity /
  boundary-information competence (BIQ/EAI)") since no prior line
  covers that axis at all.
- **`metadata/experiments.yml`** (structured index, synced to the
  site): added a `ledgers` entry, a full `lines` entry (order 5, role,
  6 headline findings through G-24), a `coverageColumns`/`howToRead`
  entry, and the `graded-lab-simulation` cell on every
  `coverageFeatures` row (16 existing rows + 1 new row).
- **`experiments/graded-lab-simulation/README.md`**: appended the G-24
  review note to the status line and the Phase 8 table row (was current
  through G-23 only).
- **Top-level `README.md`**: confirmed no edit needed — it only links
  to `docs/EXPERIMENTS.md`, doesn't enumerate lines itself.

**Site:** no separate hand-written content was needed — the site's
`/experiments/` page and per-line experiment cards are generated
entirely from `metadata/experiments.yml` via
`site/scripts/sync-experiments.mjs`. Ran the sync (wrote
`site/src/data/experiments.json` + 6 experiment cards, including the
new `graded-lab-simulation.md`), ran `site/scripts/check-experiments.mjs`
(passed), and did a full `npm run build` (700 pages, clean) to confirm
the new line renders correctly on both the `/experiments/` index and
its own card page.

## Decisions

- Treat the metadata/YAML update as *the* site content — no bespoke
  site copy beyond what already exists for the other four lines.
- Gave the graded-lab line its own dedicated feature-matrix row
  (BIQ/EAI) rather than overloading an existing MB-numbered row, since
  none of the existing rows name what this line actually measures.

## Open / next

- None outstanding from this pass; `dist/`/`.astro/` build output is
  gitignored, nothing to clean up.

## Key paths

- `docs/EXPERIMENTS.md` — new §5, build-order table, coverage matrix
- `metadata/experiments.yml` — new line 5, ledger, coverage cells
- `experiments/graded-lab-simulation/README.md` — G-24 note
- `site/src/data/experiments.json`, `site/src/content/cards/experiments/graded-lab-simulation.md` — generated, not hand-edited

## Commits

- Not committed this session; user has not yet asked.
