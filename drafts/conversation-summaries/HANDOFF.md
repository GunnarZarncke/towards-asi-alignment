# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and **`metadata/TODO.md`** (canonical work map). [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them.

Last updated: 2026-09-25 (field news memes).

---

## Open work

**Canonical list:** [`metadata/TODO.md`](../../metadata/TODO.md) — lanes, boards, sizes, gates. Do not duplicate here.

**Active lanes:** [`backtest.md`](../plans/backtest/backtest.md) · [`field.md`](../plans/field/field.md) · [`spine.md`](../plans/spine/spine.md) · [`construct.md`](../plans/construct/construct.md) — checklists in each file. 2.0 coupled-system reading: [`embedded-v2.md`](../plans/construct/embedded-v2.md). Reader contracts: [`bridge-first-use.md`](../plans/spine/bridge-first-use.md) · front-door vocabulary policy in `INSTRUCTIONS.md` §2 (Voice lane closed; plan in `drafts/attic/voice-plan.md`). Bridge 2027 markets: [`bridge-prediction-markets.md`](../plans/predictions/bridge-prediction-markets.md) (`0.4`) · [`prediction-interface.md`](../plans/predictions/prediction-interface.md) · [`assurance-risk-modelling.md`](../plans/predictions/assurance-risk-modelling.md) (Phase 3 shipped; **next:** Phase 4 pilot/listing for Markets 19–20, external funding submission, preset slots when artifacts resolve).

Closed 2026-08-17–18 work: **Compressed history (Aug 2026)** and `drafts/attic/`.

**Field spec sheet:** marks in `product-comparison.yml` are a first pass — Gunnar may edit scores/`because` lines; regenerate with `cd site && npm run sync:product-comparison`.

---

## Recently shipped

- **2026-09-25:** **Field news memes** — Minimal Pillow workflow (`scripts/meme_workflow/`); five newest news cards embed memes via `sync-field-news-memes`. Log: `2026-09-25-field-news-memes.md`.
- **2026-09-25:** **Glossary CI fix** — VFS/BIQ/EAI experiment-methodology terms anchored at `sec:experimental-methodology-shorthand`; `make check` generate step passes. Log: `2026-09-25-glossary-ci-fix.md`.
- **2026-09-25:** **Huang / Klein / Zvi field news** — Jensen Huang's release-rule quotes cashed against Zvi and Ch. 2 / Ch. 38 gates. Log: `2026-09-25-huang-klein-zvi-news.md`.
- **2026-09-24:** **Quiz math-misalignment takeaway** — News card now has `news-takeaway-math-misalignment-sep-2026`. Log: `2026-09-24-quiz-math-takeaway.md`.
- **2026-09-24:** **Mathematics misalignment field news** — Fields-medallist declaration: a solved problem is a landmark, not the goal. Log: `2026-09-24-math-misalignment-news.md`.
- **2026-09-24:** **Related Metaculus links** — Hub lists 38190, 38597, and 31707 as related forecasts. Metaculus 6509 is listed only as an underspecified-question example (Appendix H judgment section and the hub). Log: `2026-09-24-related-metaculus.md`.
- **2026-09-24:** **Ban ASI Act field news** — Senate text of the Sanders bill: training pause ends when the department is staffed; lasting ban still needs a checkable finding. Log: `2026-09-24-ban-asi-act-news.md`.
- **2026-09-23:** **Markdown links CI fix** — `generate_manuscript_tex.sh` now emits symbol-census / concept-graph artifacts; link check verifies those after generate (exempt only PDF + toy-sim JSON). Log: `2026-09-23-markdown-links-ci-fix.md`.
- **2026-09-23:** **PRA Graphviz diagrams** — Split event tree and assurance model into `.dot` sources + `render_pra_diagrams.sh`; Lean-aligned assurance composition; scope gates for `f_M,multi` (Market 11) and `c_novel` (Market 17) on the event tree. Log: `2026-09-23-pra-diagram-lean.md`.
- **2026-09-22:** **OpenAI RSI standards news** — Field-news card on the 21 September “next phase” standards post: a shared RSI ruler is not a stop. Log: `2026-09-22-openai-rsi-standards-news.md`.
- **2026-09-22:** **Predictions Phase 3** — Assurance manifest, draft Markets 19–20, extended assurance/consequence prose, `/predictions/assurance/` demo. Log: `2026-09-22-predictions-phase-3.md`.
- **2026-09-22:** **Predictions funding gate** — Funding application card; seven draft and eleven funding-gated contracts; YAML validation, site badges, and funding links. Log: `2026-09-22-predictions-funding-gate.md`.
- **2026-09-22:** **App P editorial pass** — Prose cleanup; Market 3/11 conceptual clarification; forecasts separated from deployment evidence; stronger contract designs retained as preferences rather than YES gates; PDF-compatible spine figure. Log: `2026-09-22-app-p-editorial-pass.md`.
- **2026-09-22:** **App P PRA vocabulary** — Named PRA; Kaplan–Garrick + NRC cites; glosses for \(F/R/U\), \(\kappa\), \(S_R/S_U\), consequence. Log: `2026-09-22-predictions-pra-vocab.md`.
- **2026-09-22:** **Predictions gap analysis + App H voice** — CIRIS-informed resolution gaps for all 18; opening and resolution section rewritten; Markets 15/18 asides expanded. Log: `2026-09-22-predictions-gap-ciris.md`.
- **2026-09-22:** **Predictions Phases 0–2** — Replaced product-of-prices \(P(\mathrm{doom})\) with \(F/R/U\) odds update; 18-market contract audit in appendix + YAML. Log: `2026-09-22-predictions-phase-0-2.md`.
- **2026-09-22:** **Predictions App H + site polish** — Appendix H reader pass; proper market questions; spine SVG in aggregation; site Gauss icon, list title/question split, App P `/full/` routes, tex-convert callout/glossary fixes. Log: `2026-09-22-predictions-apph-site-polish.md`.
- **2026-09-22:** **Predictions assurance-risk plan** — Reviewed PRA/appendix improvement plan; Markets 19–20 integrated for site demo; canonical assurance-model manifest; resolution incentives; lane plan at `drafts/plans/predictions/assurance-risk-modelling.md`. Log: `2026-09-22-predictions-assurance-plan.md`.
- **2026-09-19:** **Appendix H ↔ predictions catalog** — Per-box resolve-by; “Published method for…” question leads; 13/14 → 30 June 2027. Log: `2026-09-19-predictions-apph-alignment.md`.
- **2026-09-19:** **Cut persistence (ch07 home)** — `\ref{par:cut-persistence-restoration}` in Leaky Boundaries; ch06/ch08 cross-refs; ch01 unchanged. Log: `2026-09-19-housekeeping.md`.
- **2026-09-19:** **Predictions catalog cleanup** — unified `bridgeCardSlugs` keys in `metadata/predictions.yml`; proposed resolvers M7/M16/M18; [`drafts/predictions/README.md`](../predictions/README.md). Log: `2026-09-19-housekeeping.md`.
- **2026-09-19:** **Housekeeping / erasure** — compact HANDOFF; reference-only headers; log archive/prune; `.worktrees/` gitignore. Same log.
- **2026-09-19:** **Predictions positive titles + aggregation** — Positive market framing; Appendix H §aggregation; `marketQuestion` tier; Metaculus Q44423 embed. Log: `2026-09-19-predictions-positive-aggregation.md`.
- **2026-09-19:** **Predictions lane (P0c → ship)** — Criteria `0.4`; print H; `/predictions/` hub + cards; `Evidence.lean` adapters. Logs: `2026-09-19-prediction-interface-p0c.md` through `-predictions-positive-aggregation.md`.
- **2026-09-19:** **App B field spring-map** — Demo at `demos/appB-field-spring-map/`; polish + interactive UI; App B card integration. Plan closed: [`field-spring-map-plan.md`](../attic/field-spring-map-plan.md). Logs: `2026-09-18-field-spring-map-ship.md` through `2026-09-19-field-crux-map-ui.md`.
- **2026-09-19:** **Demos landing list** — `/demos/` single hub; `/demos/all/` removed. Log: `2026-09-19-demos-landing-list.md`.
- **2026-09-19:** **Drafts folder restructure** — Topic subfolders + lane plans under `plans/{backtest,field,spine,construct,predictions}/`. Log: `2026-09-19-drafts-folder-restructure.md`.
- **2026-09-19:** **Mapping AI pointer** · **Quiz news-takeaways CI fix** — Logs: `2026-09-19-mapping-ai-pointer.md`, `2026-09-19-quiz-news-takeaways-fix.md`.
- **2026-09-18:** **V2 named restorer** · **MB6 Lean rewrite** · **Embedded V2 decisions** · **Bridge markets P0/P0b** — Logs in `archive/2026-09/` and root `2026-09-18-*.md`.
- **2026-09-18:** **Field news** — Anthropic pace-measurements + constitution cards. Logs: `archive/2026-09/2026-09-18-anthropic-*.md`.

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
- **Papers / ch34:** feedback-horizon gap + verifier-construction spin-outs; selection ecology integration; constructing-alignment-attractors companion (explicit SB). **v1 Construction not in manuscript** — [`drafts/plans/construct/construct.md`](../plans/construct/construct.md) is the 2.0 plan (construction + constructibility); concrete chapters still gated on Backtest real stop.
- **Backtest / methodology:** W-1–W-16 scored (CIRIS, MM, SCDB, host traces); `docs/METHODOLOGY.md` (M1–M8). W-17 Moltbook **structure_stop** scored 2026-09-01.
- **Problem axis:** layer vs mechanism, four intro questions, `AlignmentRegime` — closed 2026-09-01.

## This week

See **Recently shipped** for 2026-09-18–19. Early Sep still load-bearing — detail in `archive/2026-09/`:

- **2026-09-04–07:** Funding site, field hub v2, backtest rename, voice lane closed, Check+Lean CI, v1.6.0 — see `archive/2026-09/2026-09-INDEX.md`.
- **2026-09-01:** W-17 structure_stop; problem-axis closed; bridge first-use at Ch. 10.

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
