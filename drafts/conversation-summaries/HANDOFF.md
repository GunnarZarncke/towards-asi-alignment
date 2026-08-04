# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and `metadata/TODO.md`. [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them (git recovery).

Last updated: 2026-08-04 (Lean overview ledger status column).

---

## Open work (load-bearing)

- **App G translation spine opener (author)** — Mirror site `/lean/` projections table in Appendix G; deferred from translation spine Phase 2 close-out. Site companion done; manuscript pass is author-owned.

- **Field matrix evidence quality** — Homepage prune **complete** (passes 1–3). No root-URL sources left in `evidence.yml`; org links on agenda cards. Log: `2026-08-03-field-matrix-homepage-evidence-prune.md`.
- **Field agenda matrix (post-restructure)** — 25 matrix rows / 30 agenda records after independence merges and neglected-report folds; TSA row links to companion home (no card). Stale search index until next site build. App B crosswalk not updated for merged row names. Source: `reference/field-agendas/data/`. Log: `2026-08-02-field-agenda-restructure-merges.md`.
- **Field crux divergence (Track 2)** — matrix nouns locked in `reference/field-agendas/data/bridges.yml`; agree/differ/homograph notes on MB1–MB11 bridge cards; hub crux legend removed 2026-08-02. Plan: `drafts/field-crux-divergence-plan.md`. Track 1 done 2026-08-02.
- **Field-claim formalization** — Phase 3 decided; App B core sync **done 2026-08-02** (MB4a/MB11 + field-index pointer). Secondary App B prose deferred (`metadata/TODO.md`). Plan: `drafts/field-claim-formalization-and-bridge-review-plan.md`.
- **Field agenda matrix (MB11 pass)** — Index matrix MB1–MB11 incl. MB4a; Field hub shipped. App B crosswalk core sync 2026-08-02. Log: `2026-08-02-appb-field-agenda-sync.md`.
- **Terminology demotion follow-through** — v1.1 plain-first + App E + site `concepts.yml` **shipped** (2026-08-02). Remaining: thin glossary leftovers (`drafts/glossary-prose-pass/THIN.md`), residual appendices grep. Inventory: `drafts/glossary-term-audit.md`.
- **CIRIS composite / boundary_decouple counterexample** — Eric-facing key task: Verify+Lens can read green while WA-blind composite fails (named-identity bet vs real intervening unit). Charter: `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`. Reuse: toy T-9 `boundary_decouple`, lab LS-28, MB1/composite-agency cards. Pointer: `experiments/TODO.md`.
- **Correlated steerability chokepoint** — WWCTV surfaces share adversarial-verifiability antecedent; disjunctive MB6b/MB8 routes may be one failure point. Formalized in `Chokepoint.lean`; still need per-chapter WWCTV forward refs and U-ledger reconciliation. Pointer: `metadata/TODO.md` BIG REVIEW.
- **Conserved-property forgeability (MB10)** — finite counterexample in Lean; prose wired. Still open: non-enumerability of conserved set across capability jumps; toy red-team of audit forgeability. Pointer: `metadata/TODO.md`, `Forgeability.lean`.
- **Measurand instantiation table** — composite indices bottom out in deferred estimators; needs mapping to experiment scripts. Pointer: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.
- **Presentation / site-first** — de-center PDF as flagship; per-part display renumbering (high risk). Pointer: `metadata/TODO.md` § Presentation.

## Compressed history (Jun–Jul 2026)

Theme rollup only — per-session detail stays in `archive/` and recent logs in this folder.

- **Manuscript arc:** scaffold (Jun 17) → integrated ch01–ch48 drafts → chapter splits/renumber → epistemic-status pass → bridge crosswalk (App. B) + institutional histories (App. M/C) → field-news surgical cites (Jul 2026).
- **Lean spine:** proof skeleton → Mathlib adoption → field-agenda finite rederivations (ELK, debate, off-switch, Bellman) → hostile-critique fixes (MB4a, MB11, S10) → MB10 forgeability counterexample → Chokepoint.lean (shared steerability) → credibility plan P1–P4 (tiling contrast).
- **Experiments:** toy → embedded → goal-agent → lab-sim → graded-lab v4; external-transfer lines ET-1 (stopped), ET-2 (null), ET-3 (closed), ET-4 (hackathon); negatives honored in `NEGATIVE_RESULTS.md` / FINDINGS; sibling precursors **agency-detect** + **deployment-pipeline-simulator** indexed in `docs/EXPERIMENTS.md`.
- **Companion site:** Astro thin slice → concept cards + Lean playground → experiments/findings UX → field-news `/news/` layer + RSS + offline PWA.
- **Notation / voice:** canonical symbol pass (Jun 23) → update-operator envelope refactor → CCI vectorization → v1.1 terminology demotion (plain-first) → two-register narrative voice policy.

## Recently shipped (Jul–Aug 2026 themes)

- **Companion site (2026-08-04):** Lean overview ledger column — field projections table shows `FieldResultStatus` badges (`rederivedFinite`, `separationOnly`, `importedAssumption`) instead of flat `proof`; Debate headline leads with claim-tree soundness/completeness/judge-error-flip. Log: `2026-08-04-lean-overview-ledger-status.md`.
- **Companion site / CI (2026-08-04):** Site PDF fetch — direct release download + authenticated API fallback + retries; fixes GitHub Actions `403 rate limit exceeded` on `copy:pdf`. Optional LaTeX PDF CI compile gate deferred to `metadata/TODO.md`. Log: `2026-08-04-site-pdf-fetch-rate-limit.md`.
- **Companion site (2026-08-04):** Debate visibility — `FINITE → DEB (DebateGame)` in field graph; DEB node surfaces game theorems; `/lean/check/debate/`; ELK alias/graph alignment; regenerated `05-field-subsumptions.png`. Log: `2026-08-04-debate-graph-site-visibility.md`.
- **Reference + companion site (2026-08-04):** Field evidence catalog renumber (131–156 → 130–153; closes gaps 130/144/146); duplicate agenda suffixes fixed; benchmark canary on every HTML page via `BenchmarkCanary.astro`. Log: `2026-08-04-field-evidence-housekeeping-canary.md`.
- **Companion site (2026-08-04):** Translation spine **Phase 2 closed** — bridge dependency map on `/field/#bridge-dependencies` (`sync-bridge-graph.mjs`); links from bridge-assumptions + MB bridge cards; CIRL/ELK checks; hidden-BIQ projection. App G opener deferred to author. Log: `2026-08-04-translation-spine-on-ramp.md`.
- **Companion site (2026-08-04):** Translation spine Phase 1 — question-first `/lean/`; `/lean/check/corrigibility/`; 13 field projection rows; graph→card wiring; reverse term-links. Log: `2026-08-04-translation-spine-on-ramp.md`.
- **Manuscript + site (2026-08-04):** Renamed **B-IQ** → **BIQ** across appendices, metadata/concepts, formal spine comments, field glossary, site JSON, and lean-spine sync; `context/extracts/` left as source canon. Log: `2026-08-04-biq-terminology-rename.md`.
- **Companion site + reference (2026-08-04):** All field agenda cards rewritten for general alignment readers — full sentences, concept/bridge links, field nouns instead of MB* on the page; sync labels + sidebar nouns; `term-links.yml` + `link-agenda-terms.py` for signature/prose linking. Log: `2026-08-04-agenda-cards-reader-prose.md`.
- **Companion site + reference (2026-08-03):** Explicit **MB4a** / **MB7d** bridge cards; matrix column links disambiguated; sibling links from MB4/MB7. Log: `2026-08-03-mb4a-mb7d-bridge-cards.md`.
- **Reference (2026-08-03):** Field matrix homepage evidence prune — removed org landing pages from catalog; agenda cards enriched; Orthogonal MB1 → Demski & Garrabrant (ev-150). Log: `2026-08-03-field-matrix-homepage-evidence-prune.md`.
- **Companion site (2026-08-03):** Full-width layout toggle — bottom-left `<->` overlay button; `localStorage` persistence; expands `--max-wide` shell. Log: `2026-08-03-site-full-width-toggle.md`.
- **Companion site (2026-08-03):** Projection phrasing on Lean spine + field projection cards (not “subsumption”); graph badges `[PROJECTED]`; Lean index table section **“Overview of existing formalizations”** (Field hub owns crosswalk matrix). Log: `2026-08-03-site-projection-phrasing.md`.
- **Reference + site (2026-08-03):** MB bridge dependency graph (`reference/field-agendas/graphs/mb-bridge-dependencies.*`, field nouns); dedicated **MB11** bridge card (`mb11-deployment-safety`) — field matrix + crosswalk + Lean spine links; dynamical-guarantee concept points to MB11 card. Log: `2026-08-03-mb-bridge-graph-and-mb11-card.md`.
- **Companion site (2026-08-03):** TSA logo SVG — circular transparent `logo-circle.svg` in header (navbar height); favicon/PWA icons; theme `#161E2B`. README trimmed (standalone-claims block removed; “What this is” revised). Log: `2026-08-03-site-logo-favicon-readme.md`.
- **Reference (2026-08-02):** Field agenda restructure — neglected-report folds; 4 independence merges (GovAI+UK AISI, Apollo+Truthful, CHAI+FAR, Anthropic+Goodfire); Neglected approaches + Safeguarded AI + MAI+CIP rows; TSA matrix-only home link; AE essay overview on portfolio card; short matrix labels. Log: `2026-08-02-field-agenda-restructure-merges.md`.
- **Reference (2026-08-02):** Field matrix bridge nouns — `bridges.yml` source; noun matrix headers; agree/differ on MB1–MB10 bodies + MB11 on `dynamical-guarantee`; hub crux legend removed; Track 2 plan `drafts/field-crux-divergence-plan.md`. Log: `2026-08-02-field-matrix-bridge-nouns.md`.
- **Companion site (2026-08-02):** Offline PWA cache fix — network-first when offline mode not enabled; removed 1-hour stale cache-first; shell-only install pre-cache; SW v8. Log: `2026-08-02-site-offline-pwa-cache-fix.md`.
- **Reference (2026-08-02):** Field evidence catalog + agenda card link audit — fixed wrong arXiv IDs (Embedded Agency, alignment faking, deception survey, logical induction), companion appendix casing, AE Studio/MIRI/CHAI/CIRIS/ControlAI URLs; canonical redirects synced across YAML + clustering. Log: `2026-08-02-field-evidence-agenda-link-audit.md`.
- **Manuscript (2026-08-02):** App B bridge crosswalk synced with field agenda index — MB4a/MB11 table rows + notes; MB4/MB8 split; field-index pointer with spine-translation caveat. Log: `2026-08-02-appb-field-agenda-sync.md`.
- **Companion site (2026-08-02):** Bridge cards field-first — each MB1–MB10 (+ index) opens with field crux in ordinary technical language, then precise book bet, with concept-card links; summaries softened for Field-hub readers. Log: `2026-08-02-bridge-cards-field-first.md`.
- **Companion site (2026-08-02):** Field hub at `/field/` — coverage matrix (MB columns → bridge cards), evidence catalog, 32 agenda cards; nav Field / Badges reorder; YAML source `reference/field-agendas/data/`. Log: `2026-08-02-site-field-hub-agendas.md`.
- **Manuscript (2026-08-02):** Site `concepts.yml` synced with App E — glossaryTerms + CCI/MB6/strategic-opacity bodies; `sync:concepts`. Terminology demotion track complete. Log: `2026-08-02-site-concepts-glossary-sync.md`.
- **Manuscript (2026-08-02):** App E operational glossary synced with inter-agenda glossary — homographs (CCI, selection, BIQ), new headwords (strategic opacity, ICI, adversarial verifiability, certification-under-manipulation, selection environment). Log: `2026-08-02-appE-glossary-sync.md`.
- **Reference (2026-08-02):** Inter-agenda glossary hub **`anthropic`** — homograph disambiguation + why acausal/ECL is co-bucketed (observer-relative reasoning). Log: `2026-08-02-anthropic-glossary-hub.md`.
- **Formal (2026-08-02):** Field-claim Phase 3 decisions — no new `MB*`; prose dispositions in field index + plan; deferred TODOs (CIRIS positive path, numeric harm leaf, chokepoint prove/type). Log: `2026-08-02-field-claim-phase3-decisions.md`.
- **Formal (2026-08-02):** Field-claim Phase 2 Lean — `FieldInterfaces.lean`; MB10↔Chokepoint `SystemTransition`; regret non-consumer decision; no new bridges. Log: `2026-08-02-field-claim-lean-phase2.md`.
- **Formal (2026-08-02):** Field-claim Phase 1 Lean — defeater signals/toys; `Field/Finite/{Nonrealizability,RegretSafety,CompositePathBypass}.lean`; no new bridges; book/matrix untouched. Log: `2026-08-02-field-claim-lean-phase1.md`.
- **Reference (2026-08-02):** Field agenda index — MB4a/MB8/MB11 matrix columns; Kosoy LTA vs PreDCA split; missing-bridge-candidates table; coverage≠book-treatment rule; public CIRIS + companion-site catalog URLs. Log: `2026-08-02-field-agenda-mb11-matrix.md`.
- **Manuscript (2026-08-02):** v1.1 terminology demotion — plain-first `deployment environment` / points of control outside ch34; retire **deployment mass** → **deployment leverage**; ch10 anthropic capture cite fix. Log: `2026-08-02-glossary-demotion-pass.md`.
- **Reference (2026-08-01):** Source-backed prose pass on inter-agenda glossary (152 headwords; Definition / why-not-same / tagged Cross-agenda). Batches in `drafts/glossary-prose-pass/`. Log: `2026-08-01-glossary-prose-pass.md`.
- **Context (2026-08-01):** Field agenda index (32 agendas); inter-agenda glossary + anthropic taxonomy under `reference/field-agendas/`. Log: `2026-08-01-agenda-glossary-index.md`.
- **Experiments (2026-08-01):** Indexed sibling repo [deployment-pipeline-simulator](https://github.com/GunnarZarncke/deployment-pipeline-simulator) as pipeline-lab / ET-4 methodological precursor (`DP-` findings in App. I). Log: `2026-08-01-deployment-pipeline-simulator-precursor.md`.
- **Manuscript (2026-08-01):** AFFINE curriculum archived; App. F preparadigmatic Meta (problem substitution) vs object-level substitution hazards; CEV/CBV; CCC→corrigibility; perils of predictors; NAH with shard theory; field-term usage preferred over glossary dual section; Lean PredictorLoop TODO.
- **Manuscript:** AI Safety Interventions coverage map (App. B §`sec:intervention-coverage-map`); intervention index archived to `context/`; shard theory / Cartesian frames / adversarial-training WWCTV / generalization-control / RSP / hardware_tag cross-refs wired.
- **Manuscript:** Ch. 2/7/34 cite Sterman (systems-dynamics CLDs); Ch. 7 adds CCD / cyclic causal discovery as calibrated passive baseline for feedback coupling (not full agent discovery). Bib: Richardson CCD, Zanga survey, Sterman *Business Dynamics*.
- **Manuscript (Jul):** Ch. 17 cites Africa/Irving thousand-dimensional persona structure (with hedges vs control-rank). App. B links MIRI agent-foundations writeups on bridge rows. App. C note on MIRI hard-pause vs Plan A spectrum. AI 2040 Plan A surgical cites + news card.
- **Companion site:** Field-news layer (`metadata/field-news.yml`); “Read more in” chapter footers; RSS; offline PWA; link-type indicators; concept logos; experiment findings UX (`**Key finding:**` extraction).
- **Experiments:** ET-1 Orbit line **stopped** (passive UAD detects scripted macro-agent; channel independence). ET-2 CIL **null** (150/150 zero passive UAD edges). ET-3 AI 2027 **closed** (LS-48). ET-4 Secret Loyalties hackathon organism + replay demo + paper under `papers/`. Graded-lab v4 + v1.3.0 tag.
- **Formal:** MB10 forgeability; Chokepoint.lean; field rederivation batch (ELK, debate, off-switch, etc.); RiskGap rename; credibility plan P1–P4 (tiling contrast).
- **Repo hygiene:** Conversation logs restored from git (2026-07-31); selective prune of superseded sessions only; archive roll keeps ~15 recent logs in root.

## Where durable state lives (do not re-derive from old logs)

| Topic | Canonical location |
|-------|-------------------|
| Cross-cutting tasks | `metadata/TODO.md` |
| Open uncertainties | `metadata/uncertainty-ledger.md` |
| Chapter status | `metadata/book.yml` |
| Experiment outcomes | `experiments/*/results/FINDINGS.md`, `NEGATIVE_RESULTS.md` |
| Field agenda crosswalk | `reference/field-agendas/field-agenda-index.md` |
| Bridge ↔ field map (manuscript) | `appendices/appB-bridge-crosswalk.tex` |
| Lean status | `formal/README.md`, Appendix I |
| Field news | `metadata/field-news.yml` |
| CIRIS cross-review | `~/repos/ciris/review/findings/` |

## Pruned sessions (superseded by later logs)

Only delete a session log when a **later conversation** explicitly supersedes it (e.g. partial field-news rollout → full tier A/B log; ET-1 intermediate Colosseum runs → line-stopped conclusion). **Do not** delete chapter-draft, session-end, or micro-logs merely because the work landed in the repo — those logs remain historical context.

Examples pruned 2026-07-31: tier-B field-news partial → `2026-07-25-field-news-tier-ab`; ET-1 Colosseum intermediates → `2026-07-24-et1-lockstep-fsm-root-cause`; lab-sim freeze-review → handles-freeze. See [RECOVERY.md](RECOVERY.md).

## Maintenance

- Update **Open work** and **Recently shipped** when a session changes load-bearing state.
- Write a new per-session log at session end (see [README.md](README.md)).
- Roll older logs: `python3 scripts/archive_conversation_summaries.py`.
- Prune superseded logs: `python3 scripts/prune_superseded_conversation_logs.py --apply` (dry-run without `--apply`).
