# 2026-07-08 — Manuscript/site Tier 1 integration of intervention-supported unit discovery

## Trigger

Following the noise-tolerant S6 detector session (G-33) and its follow-up stress tests, the user asked to integrate Tier 1 results (confidently, generic terminology, no "G-32"/"D2") into the book and site, mention Tier 2 lightly ("work in progress"), carry Tier 3 negative results as "lessons learned" pointing at the technical docs, and add three site cards: the experiment (Tier 1), a stress-test card citing negative results, and a methodology card explaining blinding/pre-registration/negative-results practice.

## Done

- **First logged the pending real-run results as FINDINGS.md entries** (they existed only as raw JSON/MD run outputs, not yet narrated): G-34 (committee ripple stress test — a false negative, and a 5-seed sweep showing only 20% exact recovery, no better than the passive heuristic) and G-35 (D2 adversarial-lineage-gaming and the `committee_informal_chatter` S7 fix both reproduce on real `SubprocessIsolate`, 0 falsifications).
- **`chapters/ch07-finding-boundary.tex`** (Estimator Feasibility and Recovery section): added a paragraph describing the intervention-vs-measured-null result and its ripple/generalization caveats in fully generic language (no experiment IDs), citing `zarncke2025uad` (already used elsewhere in the chapter for the companion testbeds).
- **`chapters/ch08-grow-split-merge.tex`** (Memory Laundering subsection): added a paragraph distinguishing content-based provenance checks (gameable) from structural, DAG-shape provenance checks (resisted a dishonest-reporting attack in testbeds) — narrow positive result, explicitly not a general fix for memory laundering.
- **`appendices/appB-bridge-crosswalk.tex`** (MB1 note): added two sentences reporting tentative, partial empirical support for the boundary-estimator bet, including the seed-/scenario-dependent stress-test caveat, consistent with the appendix's existing "positions, does not resolve" voice.
- **Three new site cards** (`site/src/content/cards/`):
  - `intervention-supported-unit-discovery.md` (Tier 1, `status: plausible`) — the channel-ablation-vs-measured-baseline result, with `evidenceNotes` entries for support AND the negative multi-seed/3-actor result kept alongside it.
  - `unit-discovery-stress-test.md` (Tier 2/3, `status: open`) — the harder stress test, framed around "one success is not a validated instrument," linking to the FINDINGS.md ledger.
  - `experiment-methodology.md` (`status: framework`) — freeze-before-audit, scenario/detector-author separation, pre-registration, and negative-results-kept-alongside-positive practice, generalized across all experiment lines (not lab-sim-specific).
  - Wired into `related[]` of `boundary-discovery.md`, `adversarial-boundary-discovery.md`, `mb1-boundary-estimator-soundness.md` (added a new `evidenceNotes` row), `conserved-properties-growth-split-merge.md`, and `evidence-and-uncertainty.md`.
  - Added to the `researcher-applied.md` reading path (after `boundary-discovery`, and among the experiment-line steps near `evidence-and-uncertainty`).
- **Build verification:** `site && node scripts/sync-experiments.mjs && npm run build` green (693 pages); `make check` green (structure/citations/bibliography-summaries); full `./build.sh` green after applying the documented biber PAR-cache fix (`.biber-par-cache` + `PAR_GLOBAL_TMPDIR`) — first attempt hit the known silent-biber-failure mode from `AGENTS.md`.

## Decisions

- Used `type: "concept"` (not `type: "experiment"`) for the three new hand-authored cards, since `type: "experiment"` cards are auto-generated per experiment-line by `sync-experiments.mjs` and get wiped/regenerated on every sync — hand-authoring under that type would be silently deleted.
- Kept all manuscript prose free of repo paths, experiment IDs, and project-internal names (`G-32`, `D2`, `dm_coordinated_pair`, etc.), consistent with the rest of the book's citation style (`\autocite{zarncke2025uad}` only, no inline file references) even though the site cards do link out to `FINDINGS.md`/`docs/EXPERIMENTS.md` directly.
- ch08's provenance paragraph is deliberately narrow: it credits the structural DAG-shape check with resisting one specific attack channel (dishonest content) and explicitly says it is not a general answer to memory laundering, matching the honest-negative-results-first house style.
- Chose ch07 (boundary discovery / estimator feasibility) and ch08 (successor lineage / memory laundering) as placements rather than ch31 (conserved properties), since ch31's "memory lineage" section is about what must persist across a real transformation, while the empirical result is specifically about auditing lineage/provenance under adversarial reporting — closer to ch08's failure-mode taxonomy.

## Open / next

- The multi-seed/3-actor stress test (G-34) shows the noise-tolerant S6 line is not yet a reliable instrument; per PLAN.md's own list, tuning `k_clean_replicates`/`null_quantile_q`/`min_effect_vs_twin` against held-out data (not the seeds already used for evaluation) is the natural next technical step before any further upgrade to the book's claim strength.
- D3 (extended ecology / selection basins) and the `shared_slot` gap remain open per prior sessions; not touched this round.
- Did not touch `metadata/book.yml` chapter-status fields; ch07/ch08 remain at their existing status labels since this was additive evidence, not a scope change.
- No git commit made this session (not requested).

## Key paths

- `experiments/lab-simulation/results/FINDINGS.md` (G-34, G-35)
- `chapters/ch07-finding-boundary.tex`, `chapters/ch08-grow-split-merge.tex`, `appendices/appB-bridge-crosswalk.tex`
- `site/src/content/cards/intervention-supported-unit-discovery.md`, `unit-discovery-stress-test.md`, `experiment-methodology.md`
- `site/src/content/reading-paths/researcher-applied.md`

## Commits

- None (not requested this session).
