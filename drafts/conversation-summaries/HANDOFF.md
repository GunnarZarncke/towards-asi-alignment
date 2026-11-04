# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and **`metadata/TODO.md`** (canonical work map). [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them.

Last updated: 2026-11-04 (housekeeping: compact HANDOFF/TODO, plan lanes, value-detect pointer, llms anti-pattern sync).

---

## Open work

**Ch. 7 after Ch. 1 stopping rule:** Review `chapters/ch07-finding-boundary.tex` so the score and examples match the rule Ch. 1 now states (score deferred to Ch. 7). Plan note: [`claim-extract/claim-extract.md`](../plans/claim-extract/claim-extract.md) § Ch. 1 rollout. Log: `2026-11-02-ch01-stopping-rule.md`.

**§3.16 stop (Nov packet):** Human pass on `chapters/ch15-values-compressed-control.tex` (author scored 3/4 priority labels; E1 miss). Log: `2026-11-02-self-audit-instruments.md`.

**CIRIS field catalog (Eric PR):** Inbound [#3](https://github.com/GunnarZarncke/towards-asi-alignment/pull/3) (`emooreatx:ciris-rc8-update`) not merged as-is. TSA editorial on `origin/ciris-rc8-review` (`525d5e572`); reverse PR to Eric’s branch sent 2026-10-14. Blocked on Eric merge/reply; then merge to `main` and `cd site && npm run sync:field-agendas`. Log: `2026-10-14-ciris-rc8-pr-editorial.md`.

**Canonical list:** [`metadata/TODO.md`](../../metadata/TODO.md) — lanes, boards, sizes, gates. Do not duplicate here.

**Active lanes:** [`backtest.md`](../plans/backtest/backtest.md) · [`field.md`](../plans/field/field.md) · [`spine.md`](../plans/spine/spine.md) · [`construct.md`](../plans/construct/construct.md) · [`claim-extract.md`](../plans/claim-extract/claim-extract.md) — checklists in each file. Claim-extract: **Ch. 1** stopping-rule revision shipped (author pass on prose); extract checker-clean. **Next:** review **Ch. 7** against Ch. 1 (plan § Ch. 1 rollout). Ch. 5 when author asks. Logs: `2026-10-16-ch01-claim-extract.md`, `2026-10-20-ch01-claim-extract-author-decisions.md`. 2.0 coupled-system reading: [`embedded-v2.md`](../plans/construct/embedded-v2.md). Reader contracts: [`bridge-first-use.md`](../plans/spine/bridge-first-use.md) · front-door vocabulary policy in `INSTRUCTIONS.md` §2 (Voice lane closed; plan in `drafts/attic/voice-plan.md`). Bridge 2027 markets: [`bridge-prediction-markets.md`](../plans/predictions/bridge-prediction-markets.md) (`0.4`) · [`prediction-interface.md`](../plans/predictions/prediction-interface.md) · [`assurance-risk-modelling.md`](../plans/predictions/assurance-risk-modelling.md) (Phase 3 shipped; three-way YES/NO/OTHER; **next:** [`eval-registry-split.md`](../plans/predictions/eval-registry-split.md) — catalog 1–13 & 15–18 point to versioned registry pages; `snapshotTag: snapshot-0` pinned (claims repo `3563a88`); Market 14 full box; Markets 19–21 full appendix boxes until Phase 4; **next:** Metaculus listing, independent host transfer, Zenodo; workbench `aintelope/ai-safety-claims-workbench`); then Phase 4.

Closed 2026-08-17–18 work: **Compressed history (Aug 2026)** and `drafts/attic/`.

**Field spec sheet:** marks in `product-comparison.yml` are a first pass — Gunnar may edit scores/`because` lines; regenerate with `cd site && npm run sync:product-comparison`.

---

## Recently shipped

Per-session detail lives in [INDEX.md](INDEX.md) (15 newest in root) and [archive/](archive/README.md). Below: load-bearing themes only.

**2026-11-04:** Markdown-link gate (draft-to-draft warn; baseline for other broken links). Graded-lab PLAN v3 closure (prior commit). Ch. 25 human-fallibility conventions + institutional-control translation draft. **Housekeeping:** compact HANDOFF; lane plan folders; SJ-Beard/value-detect as external source (removed local bundles); matched `llms.txt` / `REVIEWING_FOR_AGENTS.md` anti-patterns; TODO closed one-liners. Log: `2026-11-04-llms-sync-todo-compaction.md`.

**2026-11-03:** Ch. 25 failure-mode sources (committed); Scott autograntor LW comment extract.

**2026-11-02:** FutureSearch Markets 1 & 4 snapshots; self-audit instruments (§3.1, §3.8, §3.16 stop on ch15); section-vintage packet; Ch. 1 stopping rule; blind status re-derivation; sandboxed sub-agent MCP + `BLINDING.md`; self-audit 2026-10; parenting ↔ alignment translation + `FrameDisclosure.lean`.

**2026-10-22 – 2026-10-26:** Alignment-frame inventory and spinout paper; lens cards and clickable frame map; frame relations in Lean; Turner/Soares integration (chapter patches + [`spine/turner-soares-integration.md`](../plans/spine/turner-soares-integration.md)); bare vs record-carrying state; frame edge classes and `check_frame_graph.py`.

**2026-10-13 – 2026-10-21:** Last Safety Review implementation lane (engine, 3D UI, campaigns plan); PostHog on site/game/demos; Replit unified demos; predictions hub and registry split scaffolding; eval-registry / Appendix P contract work (see Oct archive index).

**2026-09-18 – 2026-10-12:** Field spring-map demo; drafts folder restructure; voice/site-notes passes; edit-attribution hooks; predictions Phases 0–3; v1.7.0 release — see [`archive/2026-10-INDEX.md`](archive/2026-10-INDEX.md) and [`archive/2026-09-INDEX.md`](archive/2026-09-INDEX.md).

---

## Compressed history (Jun–Jul 2026)

Theme rollup only — per-session detail stays in `archive/` and recent logs in this folder.

- **Manuscript arc:** scaffold (Jun 17) → integrated ch01–ch48 drafts → chapter splits/renumber → epistemic-status pass → bridge crosswalk (App. B) + institutional histories (App. M/C) → field-news surgical cites (Jul 2026).
- **Lean spine:** proof skeleton → Mathlib adoption → field-agenda finite rederivations (ELK, debate, off-switch, Bellman) → hostile-critique fixes (MB4a, MB11, S10) → MB10 forgeability counterexample → Chokepoint.lean (shared steerability) → credibility plan P1–P4 (tiling contrast).
- **Experiments:** toy → embedded → goal-agent → lab-sim → graded-lab v4; external-transfer lines ET-1 (stopped), ET-2 (null), ET-3 (closed), ET-4 (hackathon); negatives honored in `NEGATIVE_RESULTS.md` / FINDINGS; sibling precursors **agency-detect** + **deployment-pipeline-simulator** and related **value-detect** (SJ Beard) indexed in `docs/EXPERIMENTS.md`.
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

---

## Where durable state lives (do not re-derive from old logs)

| Topic | Canonical location |
|-------|-------------------|
| Cross-cutting tasks | `metadata/TODO.md` (boards + gates) |
| Lane checklists | `drafts/plans/` |
| Open uncertainties | `metadata/uncertainty-ledger.md` |
| Chapter status | `metadata/book.yml` |
| Experiment outcomes | `experiments/*/results/FINDINGS.md`, `NEGATIVE_RESULTS.md`; siblings + related sources in `docs/EXPERIMENTS.md` |
| Field agenda crosswalk | `reference/field-agendas/field-agenda-index.md` |
| Bridge ↔ field map (manuscript) | `appendices/appB-bridge-crosswalk.tex` |
| Lean status | `formal/README.md`, Appendix G |
| Field news | `metadata/field-news.yml` |
| CIRIS cross-review | `~/repos/ciris/review/findings/` |

## Pruned sessions (superseded by later logs)

Only delete a session log when a **later conversation** explicitly supersedes it. See [RECOVERY.md](RECOVERY.md).

## Maintenance

- Add a one-line theme here only when a session changes **load-bearing** state; put detail in a dated log + INDEX row.
- Roll older logs: `python3 scripts/archive_conversation_summaries.py`.
- Log template: [README.md](README.md).
