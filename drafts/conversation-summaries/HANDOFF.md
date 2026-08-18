# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and `metadata/TODO.md`. [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them (git recovery).

Last updated: 2026-08-18 (field stance SVG icons).

---

## Open work (load-bearing)

- **Field v2 split + stance icons** — **Done** (2026-08-18): slim `/field/v2/` hub; `/field/coverage/` matrix + catalog; seven SVG stance marks replace Unicode. Log: `2026-08-18-field-stance-icons.md`.

- **Consciousness / bearer-inference (ch18)** — **Closed** 2026-08-17 (Phases 0–5). Plan [`drafts/consciousness-tsa-extension.md`](../../drafts/consciousness-tsa-extension.md) marked **CLOSED**. Logs: `2026-08-17-consciousness-tsa-phase*.md`.

- **Field v2 split** — **Done** (2026-08-17): slim `/field/v2/` hub + `/field/coverage/`; lifecycle / graph / specify-construct / adjacent on concept cards. Log: `2026-08-17-field-v2-split.md`.

- **Specify / construct instances** — **Done** (2026-08-17): Lean named instances + alignment-target card table + 9 concept cards. Log: `2026-08-17-specify-construct-instances.md`.

- **Field hub v2 cutover** — **Done** (2026-08-17): `/field/` → `/field/v2/`; `/field/v1/` archive + v1 bridge graph; v2 graph with MB1→MB3. Log: `2026-08-17-field-v2-cutover.md`.

- **Krym architecture revision** — **Closed** 2026-08-17 (Phases 1–6 + `{leanbox}` + MB6b∨MB8 retirement). Follow-ups: `metadata/TODO.md` § Krym architecture revision (closed).

- **Six-claims spine (Phases 3–6)** — Phases 0–2 shipped: `drafts/claim-spine.md`, intro `\label{claim:…}`, `sec:how-claims-unfold`, part openers, ch48/ch30/exec-overview sync. Next: dedupe ch03/ch33/ch42 enumerations (Phase 3), chapter tagging (4), ch48 table + second-tier subsection (5). Plan: `.cursor/plans/six_claims_spine_d589004e.plan.md`. Log: `2026-08-17-six-claims-spine-phase0-2.md`.

- **MB7a–c bridge cards (field nouns)** — Explicit site cards shipped with book terminology; TODO to consider field-standard noun aliases without collapsing the split. Log: `2026-08-06-mb7a-c-bridge-cards.md`.

- **Modular chapter orientation** — The reading-DAG audit found only two unmet prerequisites, now integrated into the prose: ch07 introduces correction capacity as its scope condition, and ch38 names the artificial-civilizational control loop. The separate `readingguide` environment, converter support, and checklist generator were removed because two boxes did not justify the standing infrastructure; the Phase 0–4 bridge-audit snapshots live in `metadata/concept-graph/attic/chapter-reading-checklists/`. ch09 disambiguates the object of alignment from the authority that supplies constraints, and distinguishes component from deployed-system alignment. Treat informal DAG edges (which can run backward in PDF order, e.g. ch38 → ch34) as audit prompts rather than automatic entry prerequisites. Re-audit prose when an opening, prior close, or DAG edge changes. Log: `2026-08-05-chapter-reading-guide-removal.md`.

- **Eq-chain editorial** — island pass + spine connections (2026-08-05): K_coll, ICI→κ̃→κ, ε/UAD screen, SelfControlGap post-def bridge, 𝓡_i/K_X; **2 graph components** (main ~226 + basins). **Chapter reading DAG** — symbol (24 ch) + informal YAML + combined **48/48 ch** (`chapter-reading-dependency.md`). Remaining: **C12 basin operationalization** (ch38 loose set defs); refine `chapter-informal-edges.yml`; latent `p_\theta` vs MI `\theta` hub collision. Logs: `2026-08-05-chapter-informal-reading-dag.md`, `2026-08-05-chapter-symbol-dependency-dag.md`, `drafts/editorial-guidance-eq-chain-placement.md`.

- **`\symbolref` (partial)** — use-site markers shipped for C_t tuple sites; more unlabeled blocks (e.g. RiskGap) still open. Log: `2026-08-05-symboldef-macro.md`.

- **App G translation spine opener (author)** — Mirror site `/lean/` projections table in Appendix G; deferred from translation spine Phase 2 close-out. Site companion done; manuscript pass is author-owned.

- **Field matrix evidence quality** — Homepage prune **complete** (passes 1–3). Kosoy row upgraded 2026-08-05 (merged PreDCA into LTA; primary sources ev 154–157). Log: `2026-08-05-kosoy-evidence-merge.md`.
- **Field agenda matrix (post-restructure)** — 24 matrix rows / 31 agenda records (2026-08-05; +Iliad/TftF off-matrix). Prior independence merges and neglected-report folds. TSA row links to companion home (no card). App B crosswalk not updated for merged row names. Source: `reference/field-agendas/data/`. Log: `2026-08-02-field-agenda-restructure-merges.md`, `2026-08-05-kosoy-evidence-merge.md`, `2026-08-05-iliad-textbook-from-the-future-agenda.md`.
- **Field crux divergence (Track 2)** — matrix nouns locked in `reference/field-agendas/data/bridges.yml`; agree/differ/homograph notes on MB1–MB11 bridge cards; hub crux legend removed 2026-08-02. Plan: `drafts/field-crux-divergence-plan.md`. Track 1 done 2026-08-02.
- **Field-claim formalization** — Phase 3 decided; App B core sync **done 2026-08-02** (MB4a/MB11 + field-index pointer). Secondary App B prose deferred (`metadata/TODO.md`). Plan: `drafts/field-claim-formalization-and-bridge-review-plan.md`.
- **Field agenda matrix (MB11 pass)** — Index matrix MB1–MB11 incl. MB4a; Field hub shipped. App B crosswalk core sync 2026-08-02. Log: `2026-08-02-appb-field-agenda-sync.md`.
- **Terminology demotion follow-through** — v1.1 plain-first + App E + site `concepts.yml` **shipped** (2026-08-02). Remaining: thin glossary leftovers (`drafts/glossary-prose-pass/THIN.md`), residual appendices grep. Inventory: `drafts/glossary-term-audit.md`.
- **CIRIS composite / boundary_decouple counterexample** — Eric-facing key task: Verify+Lens green while WA-blind composite fails (named-identity bet). **Phase 1 next:** C2 tool-scout narrative + trace mock + Eric memo; optional sibling sim bite. **Phase 2:** CIRISAgent harness. **Phase 3 deferred:** Lens cohort (≥3×≥10 traces) + Coherence Ratchet battery — not a gate for logical falsifier. Charter: `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`. Pointer: `experiments/TODO.md`. Log: `2026-08-04-ciris-falsifier-phased-plan.md`.
- **Correlated steerability chokepoint** — MB6b∨MB8 two-route prose retired; Chokepoint.lean gravestone instance remains. Still open: WWCTV forward refs, U-ledger reconciliation (`metadata/TODO.md` BIG REVIEW).
- **Conserved-property forgeability (MB10)** — finite counterexample in Lean; prose wired. Still open: non-enumerability of conserved set across capability jumps; toy red-team of audit forgeability. Pointer: `metadata/TODO.md`, `Forgeability.lean`.
- **Measurand instantiation table** — composite indices bottom out in deferred estimators; needs mapping to experiment scripts. Pointer: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.
- **Presentation / site-first** — de-center PDF as flagship; per-part display renumbering (high risk). Pointer: `metadata/TODO.md` § Presentation.
- **Outreach (Florian Dietz, 2026-08-08)** — standalone publish for one agent-discovery / negative-results line; pairwise researcher-interest matching (Bubble Connector). Details TBD. Pointer: `metadata/TODO.md` § Outreach. Log: `2026-08-08-florian-dietz-outreach-todos.md`.

## Compressed history (Jun–Jul 2026)

Theme rollup only — per-session detail stays in `archive/` and recent logs in this folder.

- **Manuscript arc:** scaffold (Jun 17) → integrated ch01–ch48 drafts → chapter splits/renumber → epistemic-status pass → bridge crosswalk (App. B) + institutional histories (App. M/C) → field-news surgical cites (Jul 2026).
- **Lean spine:** proof skeleton → Mathlib adoption → field-agenda finite rederivations (ELK, debate, off-switch, Bellman) → hostile-critique fixes (MB4a, MB11, S10) → MB10 forgeability counterexample → Chokepoint.lean (shared steerability) → credibility plan P1–P4 (tiling contrast).
- **Experiments:** toy → embedded → goal-agent → lab-sim → graded-lab v4; external-transfer lines ET-1 (stopped), ET-2 (null), ET-3 (closed), ET-4 (hackathon); negatives honored in `NEGATIVE_RESULTS.md` / FINDINGS; sibling precursors **agency-detect** + **deployment-pipeline-simulator** indexed in `docs/EXPERIMENTS.md`.
- **Companion site:** Astro thin slice → concept cards + Lean playground → experiments/findings UX → field-news `/news/` layer + RSS + offline PWA.
- **Notation / voice:** canonical symbol pass (Jun 23) → update-operator envelope refactor → CCI vectorization → v1.1 terminology demotion (plain-first) → two-register narrative voice policy.

## Recently shipped (Jul–Aug 2026 themes)

- **Manuscript (2026-08-17):** Retired MB6b∨MB8 two-route language from live-path surfaces; CEV is an `AlignmentTarget` special case (ch28, App G). Log: `2026-08-17-retire-mb6b-mb8-disjunction.md`.
- **Manuscript (2026-08-17):** ch21 § reward as evidence, not optimization target (Turner); shards out of inference target via ch05/App B internals limit; Byrnes as construction alternative (ch15+ch21); Pihlakas concave/BioBlue. Log: `2026-08-17-reward-not-optimization-target.md`.
- **Companion site (2026-08-17):** Offline PWA v10 — fix `Failed to construct 'URL'` on relative assets; enable partial offline after home+CSS; always-on status in the footer button. Log: `2026-08-17-offline-caching-v10.md`.
- **Manuscript + site (2026-08-17):** Six-claims spine **complete** (Phases 0–6) — layer map, ch03 dedup, ch48 status + C-008–C-011; `six-thesis-claims` companion card; homepage/reading-path/FAQ/`llms.txt` links; `scripts/check_claim_spine.py` in `make check`. Plan: `drafts/six-claims-spine-plan.md`. Logs: `2026-08-17-six-claims-spine-phase0-2.md`.
- **Lean / App G (2026-08-17):** Krym revision **Phase 6** — `BridgeCruxes.lean`; `*Crux` Props for MB1/MB3/MB5–MB11; formal-contract pilot (ch21/25/26/28/33/43); field v2 preview `/field/v2/`. Log: `2026-08-17-krym-phase6-crux-props-field-v2.md`.
- **Lean / App G (2026-08-17):** Krym revision **Phase 5** — `AlignmentConstruction.lean`; MB8 gravestone; `mb8` removed from `BridgeAssumptions`. Log: `2026-08-17-krym-phase5-construction-mb8-gravestone.md`.
- **Lean / App G (2026-08-17):** Krym revision **Phase 4** — MB4 legitimacy/uptake/persistence decomposition; `MB4_correction_integrity` rename. Log: `2026-08-17-krym-phase4-mb4-uptake-legitimacy.md`.
- **Lean / App G (2026-08-17):** Krym revision **Phase 3b** — MB2 as checkable `Prop`s on finite `PolicyProfile`s; removed `MB2_bundle_identifiability` / `BridgeAssumptions.mb2`; `bundle_aligned_from_mb2_chain`; axiom budget shrank. Log: `2026-08-17-krym-phase3b-mb2-checkable.md`.
- **Lean / App G (2026-08-17):** Krym revision **Phase 3** — MB2a/b/c chain in `MB2Identifiability.lean` (superseded by 3b). Log: `2026-08-17-krym-phase3-mb2-lean.md`.
- **Manuscript / metadata (2026-08-16):** Krym revision **Phase 2** — App E pointing-problem headword (identification / realization / preservation); MB2/App B/bridge cards lead with value/bundle identifiability; new `/cards/pointing-problem/` glossary entry. Log: `2026-08-16-krym-phase2-pointing-glossary.md`.
- **Companion site (2026-08-17):** Site card notes triage **closed** (Phases 0–6 complete; deferred items in `metadata/TODO.md` § Site). Log: `2026-08-17-site-card-notes-close.md`.
- **Companion site (2026-08-17):** Site card notes **Phase 6** — local chapter illustration assets; PageNotes SVG icons; mobile highlight tap, expand, keyboard-safe actions. Log: `2026-08-17-site-card-notes-phase6-mobile-ux.md`.
- **Companion site (2026-08-17):** Site card notes **Phase 5** — `tex-convert` symboldef/align fixes; mobile KaTeX scroll; book resync. Log: `2026-08-17-site-card-notes-phase5-sync-math.md`.
- **Manuscript (2026-08-17):** Site card notes **Phase 4** — ch10 strategic-opacity readability (Hubinger alignment, filter-family gloss, trimmed bundle preview, oversight vs dangerous opacity, correction capacity refs). Log: `2026-08-17-site-card-notes-phase4-ch10.md`.
- **Manuscript (2026-08-17):** Site card notes **Phase 3** — ch09 composite-agent readability (ch06/ch07 cross-refs, Hanson grabby cite, consolidated disambiguation). Log: `2026-08-17-site-card-notes-phase3-ch09.md`.
- **Manuscript (2026-08-17):** Site card notes **Phase 2** — frontmatter status copy, removed External Doom exec-overview section, plain-first exec overview lead, GI comparison (ch01 + dynamical-guarantee card), glossary site links. Log: `2026-08-17-site-card-notes-phase2-frontmatter.md`.
- **Companion site (2026-08-17):** Card notes triage Phase 0–1 — tracker `drafts/site-card-notes-triage.md`; book map IA (front matter first, drop status cols); homepage standalone-claims order; chapter source GitHub links; `tex-convert` hyperref + titlepage brace fix. Log: `2026-08-17-site-card-notes-phase0-1.md`.
- **Companion site (2026-08-16):** Offline PWA caching — resumable asset-first service worker (CSS/fonts before pages); partial progress survives retries and SW updates. Log: `2026-08-16-offline-caching-resume.md`.
- **Metadata (2026-08-16):** Feedback contributors ledger — `metadata/feedback-contributors.md` (acknowledgements + Harfe / Eric Moore / Krym; LW profile links); Jonas **Hallgren** spelling fix in acknowledgements. Log: `2026-08-16-feedback-contributors-ledger.md`.
- **Manuscript (2026-08-16):** Three alignment questions moved from ch01 to the **introduction**; ch01 is a short handoff into the wrong-object argument; glossary-level wording. Log: `2026-08-16-krym-intro-three-questions.md`.
- **Manuscript (2026-08-15):** Krym revision **Phase 1** — early determine / construct / certify scope (later moved to introduction); ch03 legitimacy/authority/uptake preview; ch02/ch33 cross-refs. Log: `2026-08-15-krym-phase1-early-scope.md`.
- **Companion site / CI (2026-08-15):** Unresolved `zaman2014` in chapter sync — entry copied from the alignment-under-selection paper bib into `references/manuscript-citations.bib`. Log: `2026-08-15-zaman2014-site-cite.md`.
- **Companion site (2026-08-15):** **ET external transfer** concept card — `/cards/et-external-transfer/` now covers ET-1 through ET-4 (status table, per-annex narrative, five evidence notes, plan links); metadata source in `metadata/concepts/bodies/et-external-transfer.md`. Log: `2026-08-15-et-external-transfer-card.md`.
- **Companion site (2026-08-15):** **Unsupervised Agent Discovery** concept card — `/cards/unsupervised-agent-discovery/`; links Boundary Discovery, LW post, agency-detect + embedded/lab/graded-lab experiment lines; bidirectional related on mb1, inferential-coupling, boundary-discovery. Log: `2026-08-15-uad-concept-card.md`.
- **Lean debate / Harfe response (2026-08-15):** General `exists_claim_judge_differs_from_truth`; renamed κ_C debate-slot witnesses (`local_truth_capacity_*`); Field ledger `separationOnly` fixes; three-bucket axiom guide in Core/README; App G + ch29 leanids; axiom budget 40 theorems. Log: `2026-08-15-debate-lean-harfe-response.md`.
- **Papers (2026-08-15):** Feedback horizon gap split into companions — `papers/feedback-horizon-gap/` and `papers/verifier-construction/`; count symbol unified as **`N_{\mathrm{proxy}}`** (retired `K`). **Manuscript ch34:** selection spin-out integration — `N_proxy`, `InvFit`, adversarial selection/coevolution, hierarchy, fast/slow ecology paragraph; **census vs ecology size** (labs, open-weight, fine-tunes, scaffolds, UAD count); ch27 reward tampering; **symbolref wiring** (`CCI`, `M_sel`, `AdvVerif`, `InvFit`, `RiskGap`, `Control`, `K_X`) → raw `ch26→ch34` (7 CCI sites), reduced graph adds **`ch33→ch34` (RiskGap)**. Log: `2026-08-15-ch34-selection-spin-out-integration.md`. Earlier: verifier split `2026-08-15-verifier-construction-split.md`; FH gap spin-out `2026-08-15-feedback-horizon-gap-paper.md`. **Alignment under selection:** ecology/singleton scope limit. Log: `2026-08-15-alignment-under-selection-ecology-limit.md`.
- **Companion site (2026-08-07):** Page notes overlay — ✎ panel + ▦ highlight (in panel); per-note `path`; `#:~:text=` export; mobile overlay teleported to body + visual-viewport layout. Log: `2026-08-07-page-notes-overlay.md`.
- **Companion site / CI (2026-08-07):** Lean `/lean/` index — inline LaTeX in HTML caused Astro `Invalid Unicode escape sequence` (`\mathrm`, `\vec`, etc.); fixed in `150f406b` via `String.raw` frontmatter strings. Diagnosis-only session; rebuild verified. Log: `2026-08-07-lean-astro-unicode-escape.md`.
- **Companion site (2026-08-07):** Field news — Black Hat USA talk full kill chain for OpenAI cyber-eval → Hugging Face intrusion; security/IT framing; cross-links July HF card, AISI/METR; MB7a/UAD hooks. Log: `2026-08-07-openai-hf-blackhat-news.md`.
- **Lean DebateGame negation (2026-08-06):** `Claim.neg` with defender/challenger role-swap; joint `honest_optimal`; App G + LW draft sync. Optional leftover: site projection wording if any stale "∧/∨ only" prose. Log: `2026-08-06-debategame-negation.md`.
- **Informal + combined reading DAG (2026-08-05):** `chapter-informal-edges.yml`; symbol/informal/combined modes; 48/48 chapters in combined graph. **Site:** `/paths/chapter-reading-graph/` (clickable SVG) + card. Log: `2026-08-05-chapter-reading-graph-site.md`, `2026-08-05-chapter-informal-reading-dag.md`.
- **Chapter symbol dependency DAG (2026-08-05):** Vertical eq-chain variants (TB); `build_chapter_symbol_dependency.py`; transitively thinned 26-edge chapter prereq graph + topo layers for reading paths. Log: `2026-08-05-chapter-symbol-dependency-dag.md`.
- **Eq-chain spine connections (2026-08-05):** ε/UAD screen; κ_ij→κ̃+ICI; SelfControlGap ch32 bridge; def-relation extractor; 2 graph components. Log: `2026-08-05-eq-chain-island-fixes.md` (follow-up section).
- **Eq-chain island fixes (2026-08-05):** K_coll spine (ch13); ICI def-before-κ (ch35); 𝓡_i/K_X bridge (ch09/ch11); CCI_λ + symbolref-in-eq extractor fixes; SelfControlGap on `eq:risk-gap`; C_raw `\mathrm{raw}` pass; basins TODO (ch38). Log: `2026-08-05-eq-chain-island-fixes.md`.
- **Eq-chain graph cleanup (2026-08-05):** Optional `--cooccur`; layout ranksep/nodesep; canonical `C_t` (ch25 `\symboldef`, `\mathcal{C}_t` boundary); `\theta_{\mathrm{reach}}` vs MI `\theta`. Log: `2026-08-05-eq-chain-graph-cleanup.md`.
- **Eq-chain editorial (2026-08-05):** Extractor subscript basins; Control/D_G/Omega_Q placement; ch08→ch09 responsibility; ch10→ch40 D_G; ch26 CCI split; notation homes; site dependency spines. Log: `2026-08-05-eq-chain-editorial-placement.md`.
- **Metadata graphs (2026-08-05):** `\symboldef` macro + eq-chain integration — opt-in definition anchors (`symdef:chNN:line` note nodes); pilot marks for CCI, Control, epsilon, mu_E, RiskGap. Log: `2026-08-05-symboldef-macro.md`.
- **Metadata graphs (2026-08-05):** Eq-chain node labels — fix literal `\n`; eq/sym/chapter nodes show `chNN · Lline`, `eq:label`, def site. Log: `2026-08-05-equation-chain-node-labels.md`.
- **Metadata graphs (2026-08-05):** Equation-chain **chapters variant** — one `unit:chNN→eq` anchor per chapter (layout-constraining); shared `EqChainCore` refactor. Log: `2026-08-05-equation-chain-chapters-variant.md`.
- **Reference + site (2026-08-05):** Anthropic / Goodfire agenda — gloss **MI stack** on first use (mechanistic interpretability link + Goodfire/Transluce/Neuronpedia); contributes line links DeepMind MI lineage. Log: `2026-08-05-anthropic-lab-mi-stack-gloss.md`.
- **Metadata graphs (2026-08-05):** Section/chapter ref DAG (`scripts/build_section_reference_graph.py` → `metadata/concept-graph/`); equation-chain graph with **def vs use** edges (`eq→sym` define, `sym→eq` use) in `extract_symbol_formula_graph.py`; generated `.dot`/`.svg` gitignored. Log: `2026-08-05-equation-chain-def-use-graphs.md`.
- **Reference + site (2026-08-05):** Iliad / Textbook from the Future — new off-matrix field agenda; TSA `bookSeparates` contrast; Resolution Timaeus/Iliad cross-link; Field hub intro bullet; clustering roll-up. Log: `2026-08-05-iliad-textbook-from-the-future-agenda.md`.
- **Companion site (2026-08-05):** Field news — jailbreak disclosure commentary (AI Frontiers); CASP Boko Haram + Anthropic Fable 5 examples linked to primary sources and Zvi writeups; RSS subscribe CTA on `/news/`. Log: `2026-08-05-jailbreak-disclosure-news.md`.
- **Reference + site (2026-08-05):** GSAI agenda card — davidad LW profile + GSAI Google Group mailing list links (YAML source + sync). Log: `2026-08-05-davidad-profile-mailing-list.md`.
- **Reference + site (2026-08-05):** Field agenda generated outputs now carry `GENERATED FILE` banners (sync script + 28 cards + index); deferred TODO for build-time-only generation. Log: `2026-08-05-field-agenda-generated-banners.md`.
- **Companion site / CI (2026-08-05):** Fixed Astro build — `subsumption-debate` leanNode used Lean ledger status `separationOnly` instead of schema kind; set to `bridge`, ledger note kept in summary. Log: `2026-08-05-subsumption-debate-lean-kind-fix.md`.
- **Reference + companion site (2026-08-05):** Kosoy field agenda — merged PreDCA into infra-Bayesianism & LTA after literature review; upgraded evidence (ev 154–157); fixed AF profile URLs; 29 agenda cards. Log: `2026-08-05-kosoy-evidence-merge.md`.
- **CIRIS falsifier plan (2026-08-04):** Phased named-identity / composite-agency counterexample — Phase 1 mock + memo; Lens cohort deferred to Phase 3; C2 tool-scout locked; cross-agent divergence documented as negative-control not kill signal. Charter updated in sibling `ciris/review/`; `experiments/TODO.md` synced. Log: `2026-08-04-ciris-falsifier-phased-plan.md`.
- **Reference + companion site (2026-08-04):** Field matrix — moved evidence **#82** (UAD / agency-detect, MB1 support) from Neglected approaches row to **TSA** `MB1`; re-synced index + site JSON (`evidence.yml` agenda was already TSA). Log: `2026-08-04-field-matrix-uad-tsa.md`.
- **Companion site (2026-08-04):** Site wording — use **“this project”** for TSA framework/site/Lean/experiments; keep **“book”** for PDF, chapters, book map, and manuscript-specific references. Sync sources + scripts updated. Log: `2026-08-04-site-book-to-project-wording.md`.
- **Reference + companion site (2026-08-04):** Wentworth agenda profile link → `lesswrong.com/users/johnswentworth` (YAML source + sync). Log: `2026-08-04-wentworth-profile-link.md`.
- **Companion site (2026-08-04):** Lean overview ledger column — field projections table shows `FieldResultStatus` badges (`rederivedFinite`, `separationOnly`, `importedAssumption`) instead of flat `proof`; Debate headline leads with claim-tree soundness/completeness/judge-error-flip. Log: `2026-08-04-lean-overview-ledger-status.md`.
- **Companion site / CI (2026-08-04):** Site PDF fetch — direct release download + authenticated API fallback + retries; fixes GitHub Actions `403 rate limit exceeded` on `copy:pdf`. Optional LaTeX PDF CI compile gate deferred to `metadata/TODO.md`. Log: `2026-08-04-site-pdf-fetch-rate-limit.md`.
- **Companion site (2026-08-04):** Debate visibility — `FINITE → DEB (DebateGame)` in field graph; DEB node surfaces game theorems; `/lean/check/debate/`; ELK alias/graph alignment; regenerated `05-field-subsumptions.png`. Log: `2026-08-04-debate-graph-site-visibility.md`.
- **Reference + companion site (2026-08-04):** Field evidence catalog renumber (131–156 → 130–153; closes gaps 130/144/146); duplicate agenda suffixes fixed; benchmark canary on every HTML page via `BenchmarkCanary.astro`. Log: `2026-08-04-field-evidence-housekeeping-canary.md`.
- **Companion site (2026-08-04):** Translation spine **Phase 2 closed** — bridge dependency map on `/field/#bridge-dependencies` (`sync-bridge-graph.mjs`); links from bridge-assumptions + MB bridge cards; CIRL/ELK checks; hidden-BIQ projection. App G opener deferred to author. Log: `2026-08-04-translation-spine-on-ramp.md`.
- **Companion site (2026-08-04):** Translation spine Phase 1 — question-first `/lean/`; `/lean/check/corrigibility/`; 13 field projection rows; graph→card wiring; reverse term-links. Log: `2026-08-04-translation-spine-on-ramp.md`.
- **Manuscript + site (2026-08-04):** Renamed **B-IQ** → **BIQ** across appendices, metadata/concepts, formal spine comments, field glossary, site JSON, and lean-spine sync; `context/extracts/` left as source canon. Log: `2026-08-04-biq-terminology-rename.md`.
- **Companion site + reference (2026-08-04):** All field agenda cards rewritten for general alignment readers — full sentences, concept/bridge links, field nouns instead of MB* on the page; sync labels + sidebar nouns; `term-links.yml` + `link-agenda-terms.py` for signature/prose linking. Log: `2026-08-04-agenda-cards-reader-prose.md`.
- **Companion site + reference (2026-08-03):** Explicit **MB4a** / **MB7d** bridge cards; matrix column links disambiguated; sibling links from MB4/MB7. Log: `2026-08-03-mb4a-mb7d-bridge-cards.md`.
- **Companion site + reference (2026-08-06):** Explicit **MB7a–c** bridge cards (Access-Model Soundness, Filter Coverage, Bounded Hidden Capability) linked from MB7 overview; book terminology; crosswalk + Lean slug wiring. Log: `2026-08-06-mb7a-c-bridge-cards.md`.
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
