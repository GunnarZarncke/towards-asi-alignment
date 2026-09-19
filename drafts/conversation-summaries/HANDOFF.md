# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and **`metadata/TODO.md`** (canonical work map). [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them.

Last updated: 2026-09-19 (field spring-map polish).

---

## Open work

**Canonical list:** [`metadata/TODO.md`](../../metadata/TODO.md) — lanes, boards, sizes, gates. Do not duplicate here.

**Active lanes:** [`backtest.md`](../plans/backtest.md) · [`field.md`](../plans/field.md) · [`spine.md`](../plans/spine.md) · [`construct.md`](../plans/construct.md) — checklists in each file. 2.0 coupled-system reading: [`embedded-v2.md`](../plans/embedded-v2.md). Reader contracts: [`bridge-first-use.md`](../plans/bridge-first-use.md) · front-door vocabulary policy in closed [`voice.md`](../plans/voice.md) §9. Bridge 2027 markets (criteria draft, not listed): [`bridge-prediction-markets.md`](../plans/bridge-prediction-markets.md).

Closed 2026-08-17–18 work: **Compressed history (Aug 2026)** and `drafts/attic/`.

**Field spec sheet:** marks in `product-comparison.yml` are a first pass — Gunnar may edit scores/`because` lines; regenerate with `cd site && npm run sync:product-comparison`.

---

## Recently shipped

- **2026-09-19:** **Field spring-map polish** — More curated org→bridge weights + snapshot regen; simplified UI (category + layout toggle); per-geometry scales, MB4/MB4a row align, 2× bridge-dep stroke, seeded weight jitter, unified zoom. Log: `2026-09-19-field-spring-map-polish.md`.
- **2026-09-18:** **Field crux spring-map demo (shipped)** — `demos/ch05-field-spring-map/`: dependency layout, bridge hover highlights, TSA pinned + full matrix inherit, curated weights (ACS/CSER/Yampolskiy/Team Shard), Byrnes→neglected approaches. Run: `./serve-demos.sh` → `/ch05-field-spring-map/`. Plan: [`field-spring-map.md`](../plans/field-spring-map.md). Log: `2026-09-18-field-spring-map-ship.md`.
- **2026-09-18:** **V2 named restorer** — snapshot cut ≠ who pays after damage ≠ ecology repair of \(z\). Family C fail if restorer is only ops or only selected self-repair of \(A\). Field inventory starts at MB1. Log: `2026-09-18-v2-boundary-restorer.md`.
- **2026-09-18:** **MB6 Lean rewrite** — Signed \(g_{\mathrm{CCI}}\) object: `CorrectionSupportingBasin` / `MB6a_gradient_estimator_soundness` / `MB6b_correction_supporting_basin`. Unsigned `BasinShockRobust` is not the consequent. App G/B, ch42/ch48 `LayeredAlignedDef`, cards, axiom ledger calibrated. Log: `2026-09-18-mb6-lean-rewrite.md`.
- **2026-09-18:** **Embedded V2 decisions** — 2.0 intro claim OK; \(P\) ≠ \(D_{\mathrm{joint}}\); lifecycle is a cycle (Preserve = property); matrix stays evidential; construction/convergence on the field hub; roster `fieldConstruction`; canonical grain map at [`reference/embedded-v2-grain-map.md`](../../reference/embedded-v2-grain-map.md) (M1–M3, no Lean covering tuple). Plan: [`embedded-v2.md`](../plans/embedded-v2.md). Log: `2026-09-18-embedded-v2-decisions.md`.
- **2026-09-18:** **Bridge prediction markets P0b** — Binary YES/NO (refuse→NO). MB6 retargeted at signed \(g_{\mathrm{CCI}}\); unsigned-basin §7a retracted; Lean rewrite queued on spine P2. Criteria `0.3`. Plan: [`bridge-prediction-markets.md`](../plans/bridge-prediction-markets.md). Log: `2026-09-18-bridge-markets-mb6-binary.md`.
- **2026-09-18:** **Bridge prediction markets P0** — Obvious contract fixes in working criteria (`0.2`): void, claim-strength, judgment stack (not lone judge), §3=MB3 / §4=MB4 with probes inside those rows, seven properties, **§7a MB6a**. Docx had no tracked changes. Plan: [`bridge-prediction-markets.md`](../plans/bridge-prediction-markets.md). Criteria: [`drafts/bridge-prediction-market-criteria.md`](../bridge-prediction-market-criteria.md). Log: `2026-09-18-bridge-prediction-markets-p0.md`.
- **2026-09-18:** **Anthropic pace-measurements field news** — Institute post on R&D automation, agent oversight, and safety compute share: public race metrics, not a showing that correction binds. Log: `2026-09-18-anthropic-pace-measurements.md`.
- **2026-09-18:** **Anthropic constitution field news** — January 2026 public constitution as specify text; “directly shapes Claude” is a construction claim, not shown. Goldstein “thousand constitutions” talk parked (adjacent Specify, not news). Log: `2026-09-18-anthropic-constitution-news.md`.
- **2026-09-13:** **Path construction paper** — spin-out on incremental realizability from a described present controller to a better principal; destination \(\neq\) path; Construct 2.0 Family E. Log: `2026-09-13-path-construction-paper.md`.
- **2026-09-11:** **Maintained-blanket paper** — imported *Discovering Maintained Agent Boundaries* from sibling `agency-detect` into `context/`. User correction: self-repair is selected, not definitional; wording pass on “maintain” (ch01/ch06/ch08) not drafted. Log: `2026-09-11-agency-detect-maintained-blanket.md`.
- **2026-09-10:** **Crux map S-curve** — Alignment Crux Map funding card now shows the original S-process U vs $ chart. Log: `2026-09-10-crux-map-s-curve.md`.
- **2026-09-10:** **Containment verification news** — GSAI-call card on Moon & Varshney (arXiv:2605.09045): proved whitelist on PocketFlow; world-state/sequence specs as residual; unbounded world ends the guarantee. Log: `2026-09-10-containment-verification-news.md`.
- **2026-09-08:** **What this map misses** — reverse-column card at `/cards/concept/what-tsa-fails-to-represent/`; front-door terms; Orthogonal/Resolution evidence remap; CIRIS leftover is construction. Log: `2026-09-08-what-tsa-fails-to-represent.md`.
- **2026-09-07:** **Voice lane closed** — ledgers fresh; C-012/C-013 renumber; WWCTV→chokepoint moved to optional TODO. Log: `2026-09-07-claim-id-renumber.md`.
- **2026-09-07:** **Claim ID renumber + ledger freshness** — `C-004a`→`C-012`, `C-044`→`C-013`; W-* bullets on claims ledger; U-ledger chokepoint note. Log: `2026-09-07-claim-id-renumber.md`.
- **2026-09-07:** **Witness → Backtest rename** — Third experiment class is **Backtests** (`experiments/backtest/`, `/cards/experiment/backtests/`, `/experiments/findings/backtest/`). YAML `bridgeHooks`; App N + site copy rewritten; no old URL redirects. Log: `2026-09-07-backtest-rename.md`.
- **2026-09-07:** **Appendix stubs retired + App N readings** — Deleted unused appH–K stubs; print-letter table in `INSTRUCTIONS.md` §14. App N: protocol note + host-trace safety-case readings (W-9, W-3/W-4, W-10, W-11, W-1/W-8). Plan: [`appendix-stubs.md`](../plans/appendix-stubs.md). Log: `2026-09-07-appendix-stubs-appn-readings.md`.
- **2026-09-07:** **Front-door vocabulary** — Plain English on first-contact surfaces; policy in [`voice.md`](../plans/voice.md) §9. Log: `2026-09-07-front-door-vocab.md`.
- **2026-09-07:** **Check + Lean required on `main`** — GitHub ruleset requires job names **Check** and **Lean**. Workflows: `check.yml`, `lean.yml`. Logs: `2026-09-07-check-ci.md`, `2026-09-07-lean-ci.md`.
- **2026-09-07:** **Real v1 bridge graph** — `/field/v1/` now uses the live-MB8 diagram from `c15ad815` (not the 2026-08-17 gravestone copy). Log: `2026-09-07-v1-bridge-graph.md`.
- **2026-09-07:** **Alignment Attractor Season draft** — Node-tempo audit (not a hub grant); not a site card yet. [`drafts/funding/alignment-attractor-season.md`](../funding/alignment-attractor-season.md). Log: `2026-09-05-attractor-season-draft.md`.
- **2026-09-05:** **v1.6.0 tagged** — Backtests W-1–W-17, problem-axis / four questions / bridge first-use, site product layers. Log: `2026-09-05-v1-6-0-release-notes.md`.
- **2026-09-05:** **Audit telemetry draft** — W-17 + sim audit-layer comparison as a v2-facing recording rec (not v1 MS). [`audit-telemetry.md`](../plans/audit-telemetry.md). Log: `2026-09-05-audit-telemetry-draft.md`.
- **2026-09-05:** **App B ontology-homograph link** — `/full/appB/` was not a route; cards now use `/cards/appendix/appb/#sec:ontology-homographs-appb` plus a `/full/appB/` redirect. Log: `2026-09-05-appb-homograph-link.md`.
- **2026-09-05:** **Field hub v2 consolidation** — `/field/` redirects to v2; preview-panel hub (coverage, bridge graph, programs, bridge assumptions, lifecycle, alignment target, consciousness/welfare, external maps); `field-map-starting-points` card; plain Alignment Target intro; bridge-assumptions table links in Bridge column only. Log: `2026-09-05-field-hub-v2-consolidation.md`.
- **2026-09-05:** **Field overview adjacent voice** — plain-language consciousness/welfare panel; research-programs panel moved to #3; concept card + v2 adjacent-work copy. Log: `2026-09-05-field-overview-adjacent-voice.md`.
- **2026-09-04:** **Crux map card voice** — funding card body follows the grant listing, not the generated expansion. Log: `2026-09-04-crux-map-card-voice.md`.
- **2026-09-04:** **Spec sheet footer trim** — one caption line with links; dropped redundant footer blocks. Log: `2026-09-04-spec-sheet-footer.md`.
- **2026-09-04:** **Funding page polish** — Cytoscape+dagre dependency graph; compact legend under graph; hero CTA; team FTE + roles on cards/list; 2-sig-fig asks; fixed funded/done icon fill; TSA $10k + site summary. Log: `2026-09-04-funding-offers-site.md`.
- **2026-09-04:** **Funding opportunities on companion site** (initial) — `funding` card type; nine cards; `/funding/`; About + funder-policy + Guided Tour links. Commit `512f2280`.

## Compressed history (Jun–Jul 2026)

Theme rollup only — per-session detail stays in `archive/` and recent logs in this folder.

- **Manuscript arc:** scaffold (Jun 17) → integrated ch01–ch48 drafts → chapter splits/renumber → epistemic-status pass → bridge crosswalk (App. B) + institutional histories (App. M/C) → field-news surgical cites (Jul 2026).
- **Lean spine:** proof skeleton → Mathlib adoption → field-agenda finite rederivations (ELK, debate, off-switch, Bellman) → hostile-critique fixes (MB4a, MB11, S10) → MB10 forgeability counterexample → Chokepoint.lean (shared steerability) → credibility plan P1–P4 (tiling contrast).
- **Experiments:** toy → embedded → goal-agent → lab-sim → graded-lab v4; external-transfer lines ET-1 (stopped), ET-2 (null), ET-3 (closed), ET-4 (hackathon); negatives honored in `NEGATIVE_RESULTS.md` / FINDINGS; sibling precursors **agency-detect** + **deployment-pipeline-simulator** indexed in `docs/EXPERIMENTS.md`.
- **Companion site:** Astro thin slice → concept cards + Lean playground → experiments/findings UX → field-news `/news/` layer + RSS + offline PWA.
- **Notation / voice:** canonical symbol pass (Jun 23) → update-operator envelope refactor → CCI vectorization → v1.1 terminology demotion (plain-first) → two-register narrative voice policy.

## Compressed history (Aug 2026)

Theme rollup — per-session detail in `archive/2026-08/`.

- **Architecture:** Krym Phases 1–6 (MB2 checkable, MB4 uptake/legitimacy, construction + MB8 gravestone, crux Props); `{leanbox}`; MB6b∨MB8 two-route prose retired; CEV as `AlignmentTarget`.
- **Consciousness / bearers:** ch18 Phases 0–5 closed (conservative exclusion inside MB3; no Rainbow).
- **Reader contract:** six-claims spine Phases 0–6; site `six-thesis-claims` card; `check_claim_spine.py`.
- **Field hub:** `/field/` → `/field/v2/` + `/field/coverage/`; stance SVG icons; specify/construct instances; MB7a–c cards; agenda merges + Kosoy/Iliad.
- **Site:** card-notes triage closed; offline PWA v9–v10; translation spine `/lean/`; field news (Black Hat, jailbreak, Anthropic risk report).
- **Papers / ch34:** feedback-horizon gap + verifier-construction spin-outs; selection ecology integration; constructing-alignment-attractors companion (explicit SB). **v1 Construction not in manuscript** — [`drafts/plans/construct.md`](../plans/construct.md) is the 2.0 plan (construction + constructibility); concrete chapters still gated on Backtest real stop.
- **Backtest / methodology:** W-1–W-16 scored (CIRIS, MM, SCDB, host traces); `docs/METHODOLOGY.md` (M1–M8). W-17 Moltbook **structure_stop** scored 2026-09-01.
- **Problem axis:** layer vs mechanism, four intro questions, `AlignmentRegime` — closed 2026-09-01.

## This week

See **Recently shipped** for 2026-09-04–07. Earlier this week, still load-bearing:

- **2026-09-04:** **Bergemann–Koh–Morris** as field implementation (ch10/11/14; ch35 possibility, not protocol). Log: `archive/2026-09/2026-09-04-bergemann-mechanism-plug.md`.
- **2026-09-02:** **Cousin spec-sheet** — `/start/spec-sheet/`. Log: `archive/2026-09/2026-09-02-cousin-product-comparison.md`.
- **2026-09-01:** **W-17** Moltbook MB7a **structure_stop**; **problem-axis** closed; **bridge first-use** at Ch. 10. Logs: `archive/2026-08/2026-08-31-witness-w17-moltbook.md`, `archive/2026-09/2026-09-01-problem-or-case-and.md`, `archive/2026-09/2026-09-01-bridge-first-use-impl.md`.

## Where durable state lives (do not re-derive from old logs)

| Topic | Canonical location |
|-------|-------------------|
| Cross-cutting tasks | `metadata/TODO.md` (boards + gates) |
| Lane checklists | `drafts/plans/` |
| Open uncertainties | `metadata/uncertainty-ledger.md` |
| Chapter status | `metadata/book.yml` |
| Experiment outcomes | `experiments/*/results/FINDINGS.md`, `NEGATIVE_RESULTS.md` |
| Field agenda crosswalk | `reference/field-agendas/field-agenda-index.md` |
| Bridge ↔ field map (manuscript) | `appendices/appB-bridge-crosswalk.tex` |
| Lean status | `formal/README.md`, Appendix G |
| Field news | `metadata/field-news.yml` |
| CIRIS cross-review | `~/repos/ciris/review/findings/` |

## Pruned sessions (superseded by later logs)

Only delete a session log when a **later conversation** explicitly supersedes it. See [RECOVERY.md](RECOVERY.md).

## Maintenance

- Update **This week** when a session changes load-bearing state.
- Write a new per-session log at session end (see [README.md](README.md)).
- Roll older logs: `python3 scripts/archive_conversation_summaries.py`.
