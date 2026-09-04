# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and **`metadata/TODO.md`** (canonical work map). [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them.

Last updated: 2026-09-04 (spec sheet footer trim).

---

## Open work

**Canonical list:** [`metadata/TODO.md`](../../metadata/TODO.md) — lanes, boards, sizes, gates. Do not duplicate here.

**Active lanes:** [`voice.md`](../plans/voice.md) · [`witness.md`](../plans/witness.md) · [`field.md`](../plans/field.md) · [`spine.md`](../plans/spine.md) · [`construct.md`](../plans/construct.md) — checklists in each file. Bridge reader-contract: [`bridge-first-use.md`](../plans/bridge-first-use.md).

Closed 2026-08-17–18 work: **Compressed history (Aug 2026)** and `drafts/attic/`.

**Field spec sheet:** marks in `product-comparison.yml` are a first pass — Gunnar may edit scores/`because` lines; regenerate with `cd site && npm run sync:product-comparison`.

---

## Recently shipped

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
- **Papers / ch34:** feedback-horizon gap + verifier-construction spin-outs; selection ecology integration; constructing-alignment-attractors companion (explicit SB). **v1 Construction not in manuscript** — [`drafts/plans/construct.md`](../plans/construct.md) is the 2.0 plan (construction + constructibility); concrete chapters still gated on Witness real stop.

## This week

- **2026-09-04:** **Bergemann–Koh–Morris as field implementation** — arXiv:2609.01595 plugged into ch10 (verification order + honesty/obedience), ch11 (RSP-as-mechanism / monotone caps), ch14 (capability–misalignment covariance). ch35: peer scoring as possibility result; unbounded free rewards ⇒ benchmark not protocol. Construct keep-row. Log: `2026-09-04-bergemann-mechanism-plug.md`.

- **2026-09-02:** **Cousin spec-sheet shipped** — `/start/spec-sheet/` from `product-comparison.yml`; Start Here link + FAQ; agenda-card footers; MIRI/LW wiki on card. Plans: `cousin-product-comparison.md` (implemented), `iliad-communal-canon.md`, `lw-wiki-tags.md`. Log: `2026-09-02-cousin-product-comparison.md`.

- **2026-09-01:** **Witness W-17 Moltbook MB7a scored + committed** — H7 jscmp4/Moltbook: Tier A (Hackerclaw/thehackerman) joined, coactive Jan 31, not merged on `E_agent`; broadcast substrate → **structure_stop**. Interpretation: Jiang same-operator from burst/copy not reply graph; owner telemetry not in public pin. Log: `2026-08-31-witness-w17-moltbook.md`.
- **2026-09-01:** **Problem-axis plan closed** — §7 dormancy + §8 App F (causes OR / case AND / pause-correction); paragraph rewrite without coined terms. Plan: `drafts/plans/problem-axis-incorporation.md`. Log: `2026-09-01-problem-or-case-and.md`.
- **2026-09-01:** **Bridge first-use implemented** — genus at Ch. 10; freeze before; home-chapter `\leanspine{bridge}`. Plan: `drafts/plans/bridge-first-use.md`. Log: `2026-09-01-bridge-first-use-impl.md`.
- **2026-09-01:** **Capability dormancy (plan §7)** — ch05 transfer-breaker table; ch14 A-012 pointer; ch33 envelope one-liner; no `Safe` arrow. Log: `2026-09-01-capability-dormancy.md`.
- **2026-09-01:** **Bridge graph field hub** — `/field/` “Which problems depend on which” showed missing SVG (legacy default path); links pointed at 404 `/cards/concept/bridge-assumptions/`. Fixed v2 default + canonical `/cards/bridge/bridge-assumptions/`. Log: `2026-09-01-bridge-graph-field-hub.md`.
- **2026-09-01:** **AlignmentRegime consumers** — `AlignmentDeployment` in `Certification.lean`; ch05 footnote + accessible shift prose; ch33 CEV dunk shortened to ch28. Log: `2026-09-01-alignment-regime-wire.md`.
- **2026-08-31:** **Problem-axis through scope** — layer vs mechanism; object sort; four intro questions; Verify-oracle bag; pause/recovery-viable regime (no `Safe` arrow); Goodhart problem node; train/deploy scope classes. §§7–8 followed on 2026-09-01. Log: `2026-08-31-problem-axis-through-scope.md`.
- **2026-08-31:** **Ch17 site math render** — `stripComments` no longer treats escaped `\%` as a comment; fixes truncated “At 80%…” and downstream unrendered formulas on ch17 (also ch02, ch34, appN). Log: `2026-08-31-ch17-site-math-render.md`.
- **2026-08-29:** **Epistemic status site box** — `\begin{epistemicstatus}` converts to a lighter callout on book pages (neutral gray vs chapter-thesis accent). Log: `2026-08-29-epistemic-status-site-box.md`.
- **2026-08-29:** **Witness card bridge links** — W-1–W-16 `witnesses` sections; GitHub path linkify on experiment cards; W-1 CIRIS rename; memo removed; findings page split from experiment card. Log: `2026-08-29-witness-card-bridge-links.md`.
- **2026-08-29:** **Experiment site cards** — class overviews; W-1–W-16 cards; negative-results hub; findings pages render markdown. Log: `2026-08-29-experiment-site-cards.md`.
- **2026-08-29:** **Continuity & drift study** — union precision **366/366** (`results.tsv`; usable **260**). Log: `2026-08-29-continuity-drift-precision.md`. Earlier: packets frozen + first enumeration. Log: `2026-08-29-continuity-drift-orchestrator.md`.
- **2026-08-29:** **Witness W-16 SCDB** — justice-centered geometry acc 0.814 vs issueArea 0.623 vs intercept 0.616 (40 justices). [`witness-c004-scotus.md`](../plans/witness-c004-scotus.md). Log: `2026-08-29-witness-w16-scotus.md`.
- **2026-08-29:** **Methodology consolidation** — `docs/METHODOLOGY.md` (shared discipline + Witness M1–M8); deleted scattered copies; adversarial \(M\) + repro TODOs. Log: `2026-08-29-methodology-consolidation.md`.
- **2026-08-28:** **Witness site synthesis** — W-1–W-15 on `/experiments/#witness` and `/experiments/findings/witness/`; bounded sprint summary in `experiments.yml` and `docs/EXPERIMENTS.md`. Log: `2026-08-28-witness-site-end.md`.
- **2026-08-28:** **Witness W-15 CIRIS stack C2** — mock-LLM harness null P3 (stub 0 hits). [`witness-phase5.md`](../plans/witness-phase5.md). Log: `2026-08-28-witness-phase5-ciris.md`.
- **2026-08-28:** **Witness W-13 / W-14** — PDG refuse (no eligible adult table; 2020 adolescent SPSS not scored); CPC2015 Exp. 1 geometry acc 0.435 vs ΔEV 0.542 vs intercept 0.545 (null). [`witness-c004-pdg.md`](../plans/witness-c004-pdg.md), [`witness-c004-cpc.md`](../plans/witness-c004-cpc.md). Log: `2026-08-28-witness-w13-w14.md`.
- **2026-08-28:** **Witness W-12 raw MM + validation** — same-unit geometry acc 0.682 vs Number 0.576 vs intercept 0.529; bootstrap margins stay ≥0.05; Number collinear with type counts. [`witness-c004-raw.md`](../plans/witness-c004-raw.md). Log: `2026-08-28-witness-w12.md`.
- **2026-08-28:** **Coverage page slim** — experiment-line cards off `/experiments/coverage/` (hub link to `/experiments/`); build order folded; matrix column headers link to line cards; Witness stays a matrix column. Log: `2026-08-28-coverage-page-slim.md`.
- **2026-08-28:** **Witness C-004 raw MM freeze** — W-12 same-unit policy-effect protocol + predictions; dictator/CPC/SCOTUS/BBQ later. [`witness-c004-raw.md`](../plans/witness-c004-raw.md). Log: `2026-08-28-witness-c004-raw.md`.
- **2026-08-28:** **Witness Phase 4** — W-7 C-004 leftover refuses + HH skip; W-8 Lean C2 pin; W-9–W-11 H5 trees (FAA/GPL/Debian). Analogues do not lift Construct. Log: `2026-08-28-witness-phase4.md`.
- **2026-08-28:** **Witness next tests (plan)** — after Phase 3: Slices A–C; executed as Phase 4. W-12 recorded. Log: `2026-08-28-witness-next.md`.
- **2026-08-28:** **Witness Phase 3** — C-004 Moral Machine non-implication (W-5); C-007 Arena Elo×MASK honesty (W-6). Log: `2026-08-28-witness-phase3.md`.
- **2026-08-28:** **Witness in book/site** — App I W-1–W-4; `/experiments/` and homepage split sims / external tests / witness tests. Log: `2026-08-28-witness-book-site.md`.
- **2026-08-28:** **Witness Phase 2 richer sources** — Perceval×BIC; cpufreq revert re-entry; `-stable` hunks; SNAP+API; BetacommandBot; wiki-socks. W-3 fails C-004a/C-005/C-006; W-4 C-006 fail, causal RfA still refuse. Log: `2026-08-28-witness-phase2.md`.
- **2026-08-28:** **Witness Phase 0 frozen** — charter, pass/fail/refuse table, measurand sheet. [`drafts/plans/witness-phase0.md`](../plans/witness-phase0.md). Log: `2026-08-28-witness-phase0.md`.
- **2026-08-28:** **AI Village HF related observations** — no standalone news card; fold Tekofsky LessWrong comparison onto OpenAI HF postmortem card (setup contrast, poverty/no-despair). Log: `2026-08-28-ai-village-hf-related-observations.md`.
- **2026-08-28:** **Assumption key-only boxes + App B** — `bookassumption` (A-* key in heading); App B drops field-index/MIRI meta, landscape crosswalk; companion URLs frontmatter-only. Log: `2026-08-28-assumption-boxes-appb-cleanup.md`.
- **2026-08-28:** **Shipping benchmark** — git + 633 session logs → 62 work days / 496h, release velocity, 54 deliverables, parallel burst calendar. [`drafts/tsa-shipping-benchmark.md`](../tsa-shipping-benchmark.md). Log: `2026-08-28-shipping-benchmark.md`.
- **2026-08-28:** **Alignment Crux Map** — six crowded words; full **$50k** / 12 steps; MATS + BlueDot use tests + CHAI or Christiano; contractor `reviews` in YAML. Plan: [`drafts/plans/alignment-crux-map.md`](../plans/alignment-crux-map.md). Originals: `funding-applications/alignment-crux-map/` (local; gitignored). Log: `2026-08-28-alignment-crux-map.md`.
- **2026-08-28:** **Project identity** — README no longer leads with “research manuscript.” `INSTRUCTIONS.md` scoped to the book; PDF Current Status companion-site sentence is project-level. Log: `2026-08-28-project-not-manuscript.md`.
- **2026-08-27:** **A-* in home chapters** — named `assumption` boxes; `\akey{A-00x}` links; no App B lookup table. Log: `2026-08-27-manuscript-a-keys.md`.
- **2026-08-27:** Voice **bridge axioms vs book assumptions** — App G intro + `/lean/` + `/lean/spine/`: chapter A-rows ≠ Lean MB axioms. Log: `2026-08-27-voice-lean-axioms.md`.
- **2026-08-27:** **Quiz multi-correct** — split bundled keys; ≥5% floor in `check_quiz_bank.py` (12/211). Log: `2026-08-27-quiz-multi-correct.md`.
- **2026-08-27:** **Quiz length tell implemented** — `make check` runs `check_quiz_length_tell.py`; 0% margin-fail. Log: `2026-08-27-quiz-length-tell.md`.
- **2026-08-27:** **Blind quiz protocol** — solver chooses without keys; superagent scores. Full bank 211/211 (easy distractors). Log: `2026-08-27-quiz-blind-eval.md`.
- **2026-08-27:** Voice §5 **progress wording** — introduction + executive overview: refused/unsupported required evidence (or recorded negative) leads; artifacts are instruments. Log: `2026-08-27-voice-progress.md`.
- **2026-08-27:** Voice §2 **chapterthesis audit closed** — remainders ch20, ch27, ch31, ch33, ch38, ch42, ch43; rest skip. Log: `2026-08-27-voice-chapterthesis-ch21-48.md`.
- **2026-08-27:** Voice §2 **ch11–ch20 thesis audit** — ch20 remainder (toy-only tests); ch11–ch19 skip. Log: `2026-08-27-voice-chapterthesis-ch11-20.md`.
- **2026-08-27:** Voice §2 **ch01–ch10 thesis audit** — all skip (framing/necessity; no remainder clauses). Next: ch11. Log: `2026-08-27-voice-chapterthesis-ch01-10.md`.
- **2026-08-27:** **Scaling Trust** — *Without Intermediaries* noted on Construct v2 (not news). Log: `2026-08-27-scaling-trust-construct-note.md`.
- **2026-08-27:** **Eckersley citation** — arXiv:1901.00064 (`eckersley2019impossibility`) in ch. 4 fixed-utility + CIRL paragraphs. Log: `2026-08-27-eckersley-citation.md`.
- **2026-08-27:** **Quiz from news takeaways** — 21 manuscript claims from field news, on chapter quiz blocks only. Log: `2026-08-27-quiz-news-takeaways.md`.
- **2026-08-27:** **Site quiz Phase 2** — 131-question bank (essays, ch01–48, 15 agendas); draft merge + `check_quiz_bank.py`. Log: `2026-08-27-quiz-phase-2.md`.
- **2026-08-27:** **Site quiz Phase 1** — `/quiz/` stack player, retake-all, 2 MB1 questions. Log: `2026-08-27-quiz-phase-1.md`.
- **2026-08-26:** **FAQ rewrite** — answers match essays / Start Here / typed cards / on-site PDF / Field; translations hedge removed. Log: `2026-08-26-faq-update.md`.
- **2026-08-26:** **Card slug migration** — type-prefixed `/cards/{type}/…` URLs, 684 legacy redirects, continue-reading by card kind, path read-next on typed chapter URLs. Log: `2026-08-26-card-slug-migration.md`.
- **2026-08-26:** **Book contents + experiment coverage** — `/book/` full PDF-order map; `/book/map/` redirect; coverage hub jump cards. Log: `2026-08-26-book-contents-coverage.md`.
- **2026-08-26:** Generalist **essay path** — `/essay/` → first essay; Start Here teaser; 11 essay cards; generalist path spine. Nav unchanged. **Guided Tour read next** from last book chapter (path → graph → manuscript). Log: `2026-08-26-generalist-essay-path.md`.
- **2026-08-26:** OpenAI Hugging Face postmortem field news (`field-news-openai-hf-roadahead-aug-2026`). Log: `2026-08-26-openai-hf-roadahead-news.md`.
- **2026-08-26:** Site nav landings **remainder** — slim Cards/Book/News/Tour/Lean/Experiments/Demos + child routes + crumbs. Log: `2026-08-26-site-nav-landings-remainder.md`.
- **2026-08-26:** Site nav landings **steps 1–2** — 10-item header; `/start/`; homepage tiles + localStorage continue-reading; `/field/` six-panel hub (v2 briefing kept). Log: `2026-08-26-site-nav-landings.md`.
- **2026-08-26:** Early-chapter preview demotion **closed**. Durable E/G method + scores: [`review/chapter-formulation-groundedness.md`](../../review/chapter-formulation-groundedness.md). 2.0 G-rerun on Construct P4. Session: `2026-08-26-early-chapter-demotion.md`.
- **2026-08-26:** CIRIS field overview reevaluated against `~/repos/ciris/` + ciris.ai (CC 1.0-rc2 public vs rc3 checkout; four-claim fusion; MH-3 / HARM-1). Log: `2026-08-26-ciris-field-evidence.md`.
- **2026-08-26:** Bot-orientation housekeeping — `llms.txt`, `REVIEWING_FOR_AGENTS.md`, bridge ranges in `AGENTS.md`/`CONTRIBUTING.md`, README doc links, `notation.md` App G pointer, field-agenda `meta.yml` counts (24/30). Log: `2026-08-26-bot-orientation-housekeeping.md`.
- **2026-08-25:** Site glossary sync (13 terms, homograph links on Field hub); UAD name fix (Unit-attribution → Unsupervised Agent Discovery). Log: `2026-08-25-site-glossary-uad.md`.
- **2026-08-25:** Homograph hygiene (first-use + App E + App B ontology reverse-gaps). Not the Ngo per-agenda reverse column. Log: `2026-08-25-homograph-hygiene.md`.
- **2026-08-25:** Construct plan: usable-source list + reasoning from external lit review. Log: `2026-08-25-construct-lit-keep-list.md`.
- **2026-08-25:** Harm-path **v1 weave** (inert writes, envelope recert, Enable, named residuals) in ch05/12/30/33/36/42/44/46 + App F + `open-problems.md`. Nine-axis grammar stays in `drafts/adverse-process-generator/`; parked as 2.0 appendix/chapter in [`construct.md`](../plans/construct.md). Log: `2026-08-25-harm-path-v1-weave.md`.
- **2026-08-24:** External construction seed + lit-review prompt (institutions, mechanism design, DAO/TEE). [`drafts/plans/construct-external-lit.md`](../plans/construct-external-lit.md). Log: `2026-08-24-construct-external-lit.md`.
- **2026-08-24:** Construct lane plan — TSA 2.0 construction + constructibility; TODO work-map node; v1 MS still gated. Log: `2026-08-24-construct-2-0-plan.md`.
- **2026-08-24:** Physically grounded adverse-process **generator** (hybrid grammar + **design-conditioned bounds**: channel-cut vs output-quarantine; airgap including residual hardware coupling). Folder `drafts/adverse-process-generator/` (`REPORT.md`, `design-bounds.md`). Not a new spine ontology. Manuscript not edited. Log: `2026-08-24-adverse-process-generator.md`.
- **2026-08-23:** Ontology-source reviews (60 entries) vs TSA — `_synthesis.md` plus `_three-tests.md` (crack / better-fit / gen-vs-sibling; cite few, no spine expansion). Manuscript not edited. Log: `2026-08-23-ontology-reviews.md`.
- **2026-08-22:** PDF layout — Contents starts on a new page; part summaries on the part-title page. Log: `2026-08-22-part-pages-toc-break.md`.
- **2026-08-22:** **v1.5.0 tagged** — six-claims spine, Lean architecture revision, field hub v2, authorship bars. Log: `2026-08-22-v1-5-0-release-notes.md`.
- **2026-08-22:** Kosoy LTA agenda card rewritten in her terms (PSI ≠ precursor-via-bridge-transform). Log: `2026-08-22-kosoy-lta-card-rewrite.md`.
- **2026-08-22:** OpenAI pacing field news (pause + 20% monitor; three-voice, short). Log: `2026-08-22-openai-pacing-news.md`.
- **2026-08-22:** Companion site authorship chips — section/subsection chips from `\authbar` keys; Notes panel toggle. Log: `2026-08-22-site-auth-chips.md`.
- **2026-08-22:** Spine lane — [`drafts/plans/spine.md`](../plans/spine.md); open-work erasure (checklists in plans only). Log: `2026-08-22-spine-lane-erasure.md`.
- **2026-08-22:** Authorship bars — full rollout (48 chapters + wired appendices); Summary/References `{AI}`, epistemic status `{GZ+AI}`; empty-bar fix; spacing tuned (frontmatter-only Needspace); ~1440 pp. Log: `2026-08-22-authorship-bars-rollout.md`.
- **2026-08-21:** Authorship bars — `\authbar` on frontmatter only (dotted right bar + `AI`/`GZ` Kürzel). Log: `2026-08-21-authorship-bars.md`.
- **2026-08-21:** Program map — plans in `drafts/plans/` (`voice.md`, `witness.md`, `field.md`); Expectation 7 removed from Witness; HANDOFF compacted. Log: `2026-08-21-program-tracks-map.md`.
- **2026-08-21:** Executive overview rewritten for six-claim / three-question sync. Log: `2026-08-21-executive-overview-sync.md`.
- **2026-08-21:** Voice §1, §3, §4, §6–§8. Log: `2026-08-21-track-b-claim-strength-voice.md`.
- **2026-08-21:** Construction papers stay spin-outs (reviewer: unearned weight). Logs: `2026-08-21-constructing-alignment-attractors.md`, `2026-08-21-construction-manuscript-todo.md`.
- **2026-08-20:** ch21 Turner Reward≠OT hedge; README sync; erasure pass.
- **2026-08-19:** Anthropic Risk Report field news.

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
