# Release Notes

*Towards Superintelligence Alignment: Boundaries, Values, and Correction*

Most recent release first. Versions follow a simple `MAJOR.MINOR.PATCH` scheme:

- **MAJOR** — structural milestones (numbering scheme, part/chapter architecture, or a manuscript milestone declared complete).

- **MINOR** — new or substantially rewritten chapters, appendices, or framework objects.
- **PATCH** — fixes, calibration, citations, and editorial passes.
---

## v1.4.0 — 2026-08-02 — Field crosswalk hub, legibility pass, and external-transfer ET-3/ET-4

Commit: `471cc503` · Tag: `v1.4.0`

**Field agenda crosswalk** maps 32 named agendas to MB1–MB11 on a companion **Field hub**; a **plain-first legibility pass** retires coined jargon in the manuscript and syncs Appendix E with a 152-headword inter-agenda glossary; **external transfer** closes the AI 2027 annex (ET-3) and ships the Secret Loyalties hackathon line (ET-4); and **field-claim Lean** adds finite defeaters and interface certificates without new bridge numbers.

### Field agenda crosswalk (`reference/field-agendas/`)

- **32 agenda cards** with sourced evidence catalog (132 rows), AISafety.com clustering, and an agenda × bridge **coverage matrix** (MB1–MB11 incl. MB4a).
- **YAML source of truth** under `data/` — agendas, matrix, evidence, clustering — with `sync-field-agendas.mjs` generating the index markdown and site cards; `field-agenda-index.md` is generated output, not hand-edited.
- **Inter-agenda term glossary** (~152 headwords): Definition / why-not-same / cross-agenda tags; source-backed prose pass; **`anthropic`** homograph hub (acausal/ECL disambiguation).
- **Spine-translation rules** replace a missing-bridge-candidates table: coverage in the matrix ≠ book treatment; Kosoy LTA vs PreDCA split; public CIRIS and companion-site catalog URLs.
- **Sibling precursor indexed:** [deployment-pipeline-simulator](https://github.com/GunnarZarncke/deployment-pipeline-simulator) as pipeline-lab / ET-4 methodological precursor (`DP-` findings in Appendix I).

### Companion site — Field hub (`site/`)

- **`/field/` hub:** coverage matrix (MB columns → bridge cards), evidence catalog, agenda list with map clustering; nav reordered (**Field** before Cards, **Book** before PDF).
- **Bridge cards field-first:** each MB1–MB10 (+ index) card opens with the field crux in ordinary technical language, then the precise book bet, with concept-card links — written for Field-hub readers, not proof-spine insiders.
- **`concepts.yml` synced with Appendix E:** glossaryTerms + CCI/MB6/strategic-opacity bodies; homograph parity (CCI, selection, BIQ).
- **Offline PWA:** opt-in site caching with hourly refresh; combined **RSS** feed for news and updates; auto-generated field-news chapter footers with expanded titles.

### Reader-facing language and glossary

- **v1.1 terminology demotion (manuscript):** load-bearing coined terms lead with operational paraphrases; **`deployment mass` retired → `deployment leverage`** everywhere in prose (equation/Lean names unchanged for cross-ref stability).
- **Plain-first selection vocabulary:** `selection environment` → `deployment environment` outside ch34 home; `selection handle` → `point of control over deployment` outside ch34/App E.
- **Appendix E operational glossary** synced with the inter-agenda glossary — homographs (CCI, selection, BIQ), new headwords (strategic opacity, ICI, adversarial verifiability, certification-under-manipulation, selection environment).

### Manuscript

- **Appendix B bridge crosswalk synced with field index:** range **MB1–MB11** incl. **MB4a**; table split **MB4 / MB4a / MB8** + new **MB11** row; field-index pointer with spine-translation caveat.
- **Intervention coverage map** (`sec:intervention-coverage-map`): LessWrong AI Safety Interventions index mapped to book scope — explicit exclusions, borderline agendas (shard theory), LLM-opacity rule; surgical cites in ch05, ch07, ch14, ch17, ch27, ch43, ch48, App C.
- **AFFINE field coverage:** outer-alignment peers, Meta substitution hazards, predictor-loop genesis (App F preparadigmatic Meta vs object-level hazards); CEV/CBV; CCC→corrigibility.
- **Calibrated passive baselines:** CCD / cyclic causal discovery and Sterman systems-dynamics CLDs cited in ch02/ch07 as feedback-structure baselines, not substitutes for interventional discovery.
- **Scenario and field cites:** AI 2040 Plan A (ch13, ch31, ch34, ch37, ch38, App C); MIRI agent-foundations writeups on bridge rows; thousand-dimensional persona structure (Africa/Irving) in ch17 with hedges vs control-rank.
- **Appendix N:** AI 2027 / Plan A / ET-3 epistemic split — scenario illustrations vs stress-tested mechanisms vs unsupported forecast validation.

### Lean proof spine — field-claim formalization (`formal/`)

- **Phase 1 — finite defeaters and toys:** `Defeaters.lean` (misspec signals, MB4a/MB10/MB11 defeaters); `Field/Finite/{Nonrealizability,RegretSafety,CompositePathBypass}.lean` — realizability gaps, regret-alone blocked export, composite-path bypass vs correction integrity.
- **Phase 2 — interfaces:** `FieldInterfaces.lean` — epistemic-coverage evidence, positive measured-path certificate, regret safety as non-consumer side channel.
- **Phase 3 — bridge dispositions (no new `MB*`):** misspec ambient MB1/MB9 + defeaters; regret kept as side channel; reflection split in `LobTiling`; positive path → integrity structure with CIRIS TODO; MB10 chokepoint interface kept with prove/type TODO.
- **`FieldInterfaces.lean` + `Forgeability.lean`:** TODO anchors for deferred harm leaf, CIRIS positive path, chokepoint typing.

### Experimental findings — external transfer ET-3 and ET-4

- **ET-3 closed (LS-48):** AI 2027 capability-schedule transfer annex — macro takeoff cues drove micro bridge stress tests on a pinned sibling fork; foster trajectory sensitivity plots; **no calendar-validation claims**. Deferred follow-ups in `lab-simulation/TODO.md`.
- **ET-4 Secret Loyalties (hackathon):** simulated pipeline-embedded secret-loyalty organism with principal-directed policy, graded affordance audit (A0–A4), confirmatory battery, and audit-visible remediation holds; spin-out paper under `papers/et4-secret-loyalties/`; **case-brief replay demo** at `/ch07-lab-sim-replay/?mode=et4` with exported trace bundle.
- **Field news for transfer lines:** plain-language ET-2 CIL card; ET-4 card with paper/replay links; AI 2040 Plan A, pacing-the-frontier, insurance-incentives, Microsoft open-weights cards added since v1.3.0.

---

## v1.3.0 — 2026-07-25 — Field news, chapter art, external transfer, and graded-lab v4

Commit: `6cd34dcf` · Tag: `v1.3.0`

**Field news** ties 2026 alignment incidents to manuscript chapters; **chapter-opening illustrations** cover Part I–II (ch01–ch16); **graded-lab v4** restructures the empirical program as independent per-bridge rigs; **external transfer** (ET-1 and ET-2) adds the first cross-codebase instrument runs; and the **experimental evidence spine** now states what the lines say about the book's chapter claims — in the manuscript, on the companion site, and in the ledgers.

### Field news (`metadata/field-news/` + manuscript cites)

- **Nine-card `/news/` layer** synced from `metadata/field-news.yml` and body files via `sync-field-news.mjs`; chapter cards show a **Related news** sidebar; nav links to `/news/`.
- **Tier A (six incidents):** OpenAI/Hugging Face hack, long-horizon sandbox, AISI cheating, METR Frontier Risk report, Mythos withheld, accidental chain-of-thought opt-out — site cards plus surgical `\autocite{}` in ch11–ch43 and Appendix B.
- **Tier B (four clusters):** CLTR + Claude Code (site); METR Anthropic red-team (ch42); OpenClaw (site + ch26); OpenAI/HF card rewritten with entity-attribution / UAD framing and graded-lab cross-link.
- **Bibliography:** ten new 2026 keys + summaries.

### Chapter-opening illustrations (ch01–ch16)

- **Sixteen figures** in `figures/illustrations/` inserted into ch01–ch16 `.tex` (title-only caption); web JPEG pipeline for the site; PDF keeps source PNGs.

### Graded-lab v4 — per-bridge rig architecture (`experiments/graded-lab-simulation/`)

- **Portfolio, not gate chain.** Each bridge assumption MBx gets its own rig R-MBx with a declared precondition, substrate policy, and pre-registered predictions. A failed precondition yields **SKIP-with-finding for that rig only**; other rigs keep running. This is the ch42 safety-case argument — leaves must not collapse into one "machinery transferred" checkbox — as experiment architecture.
- **Precondition, not gate.** Every rig runs a mechanical precondition check on its substrate first; SKIP records measured values ("substrate lacks property X at level Y") as a reportable finding, not a program failure.
- **Substrate policy (S-blind / S-fixture / S-inherited).** Three pre-registered substrate classes with decreasing claim strength; the anti-developed-to-the-test rule is fixed at freeze, not chosen after seeing results.
- **Shared fixture layer.** Substrate and reference episode traces are produced once per tuple and cached; rigs consume traces rather than re-simulating the full ecology.
- **`channel_severance` runtime primitive** added for R-MB7d channel-ablation tests.
- **One rig, one results file, one FINDINGS entry** per battery; cross-rig synthesis is a separate, explicitly weaker artifact that names each rig's substrate.
- **v3 line closed (GL-78);** v4 supersedes the single-ecology gate chain that terminated when V2-3's transfer null cascaded into descoped downstream stages.

### Experimental findings — what the lines now say

- **Appendix N chapter synthesis** (`sec:appn-chapter-synthesis`): four paragraphs in chapter/WWCTV language stating what each experiment line supports, qualifies, or leaves unresolved for the book's claims — not experiment-line jargon.
- **ET-1 closed (GL-86):** Orbit external-transfer line concluded; **lockstep FSM aliasing** identified as root cause (not superstep timing); pre-registration ET1-0 frozen. Finding: on a benchmark where every participant executes the same script, reporting them as one process is correct and tells us nothing about hidden coordination — directly testing ch07's finite-data recovery worry.
- **ET-2 on CIL (GL-87/88):** first instrument runs on a system this project did not build. **Passive UAD null** on `basin_stability` at every mechanism × adversarial-fraction cell (GL-87). **Handle-UAD pilot** finds nonzero but **diffuse** cross-agent coupling via a shared common-pool resource (GL-88), named as the **variable-smoothing case** of recoverability theory (`zarncke2026smoothing`); the prescribed fix is a coarse-grained candidate test, not a better pairwise statistic.
- **Graded-lab v4 first scored rigs (GL-79–85):** per-bridge pass / null / SKIP results now wired into ch07, ch16, ch33, ch34, ch41, ch42, and Appendix N — e.g. co-activity-present null (R-MB1), R-MB9 dual-arm pass with R-MB7d pair null, variation-operator harness sanity (R-MB6a), selectable Goodhart tension without proxy purchase (R-MB2), mid-band non-transfer after probe + growth (R-MB6b SKIP).
- **Site and ledgers aligned:** `**Key finding:**` tags in all five experiment lines; auto-extracted headline bullets; curated `/experiments/findings/{line}/` pages; experiment cards as primary destinations; negative-results card.

### Companion site (`site/`)

- **Link-type indicators** (PDF, GitHub, demo, external) standardized via `LinkIndicator.astro` across nav, cards, demos, Lean, experiments, and updates.
- **Concept card logos** (41 minimalist SVGs) synced to `public/concept-logos/` and rendered on card pages and indexes.
- **UX polish:** standalone-claims hub card; nav order; viewport QR modal; Calendly on About; bot orientation and exposed `/search-index/` for tools; ch07 plane-replay and ch35 percolation demos wired in; and many other small fixes.

### Manuscript

- **Appendix M:** religious-orders paragraph (Rost et al. Benedictine-abbey data, Cluny/Cîteaux, Jesuit suppression) and tacit-knowledge paragraph (Polanyi, Collins TEA laser, Burja).
- **Field agenda rederivation:** ELK, debate, off-switch, quantilizer, amplification, Thornley dynamic choice, shutdown/interruptibility cores — finitely restated in bridge-crosswalk language.
- **Correction framing:** "in the small" vs "in the large" named in ch25/ch26; catchy accessible leads on five glossary entries; and other smaller changes in the manuscript

### Lean proof spine (`formal/`)

- **Evidence ladder (P1–P4):** trace-calibrated risk-gap certification from finite episode profiles (P1); concrete frozen-validation battery gate without false deployment discharge (P2); spine satisfiability plus local bridge non-implication witnesses for MB1–MB11 (P3); **Löbian tiling contrast** — self-certifying successor acceptance obstructed, external measured audit path contrasted (P4, ch30 + Appendix G).
- **`RiskGap` as sole name** for the numeric risk-gap quantity (`Control − CCI`); duplicate `Risk`-named theorems removed.
- **Appendix G integration:** bridge-independence table, formal statement summaries for P4, axiom-ledger regenerated (38 headline theorems).

### Housekeeping

- **Repo cleanup:** stale generation chains retired; completed plans archived; regenerable binary outputs untracked; experiment READMEs restructured with self-contained intros and per-line `CHANGELOG.md` files; `AGENTS.md` erasure/cleanup guidance added.

---

## v1.2.0 — 2026-07-17 — Site publication layer, evidence index, and graded-lab v3

Commit: `14cf0fd` · Tag: `v1.2.0`

The **companion site** moves from a static mirror to a **YAML-synced publication layer** on **towards-alignment.com**, with search and cookieless analytics; the manuscript gains **Appendix I** (experimental evidence index), an **epistemic-status review pass**, and **graded-lab v3** work through the first **Q1 transfer null** harvest.

### Companion site (`site/`)

- **Custom domain and SEO.** Site configured for `towards-alignment.com`; sitemap (`@astrojs/sitemap`), `robots.txt`, canonical URLs, Open Graph / Twitter cards, and a default social preview image. Repo links migrated from the old GitHub Pages URL where appropriate.
- **YAML-roster content sync.** Hand-authored root concept/bridge/projection cards replaced by generators from `metadata/concepts.yml`, `metadata/bridges.yml`, `metadata/projections.yml`, and `metadata/concepts/bodies/`. Retired `terminology.md` and field-subsumption JSON in favour of generated glossary cards and a **`/glossary/`** hub; **`/notation/`** from `notation.yml`; bridge cards synced from Appendix B overrides.
- **Releases hub.** **`/updates/`** page and release cards generated from this file via `sync-releases.mjs` (newest first).
- **Search.** `build-search-index.mjs` → `search-index.json` (~214 entries: concepts, bridges, chapters, experiments, notation symbols; bibliography cards excluded). Header **`SiteSearch`** component: type-aware matching and multi-word fallback (up to 20 one-line results).
- **Analytics and disclosure.** Cookieless **Cloudflare Web Analytics** beacon (production builds only; disabled in dev). **Impressum** *Web-Analyse* section documents aggregated, cookie-free traffic measurement.
- **Optional `claimId` links** from six Introduction-aligned concepts to `metadata/claims-ledger.md` (warn-only validation).

### Manuscript and evidence spine

- **Appendix I — Experimental evidence index** (`appN-experimental-evidence.tex`): global finding IDs (`G-*`, `gl-*`) across experiment lines; wired into chapters and companion site.
- **Epistemic-status review pass** across chapters and appendices (reviewed status boxes; high/medium duplication trims in dense chapters).
- **Symbol census** promoted to `metadata/symbol-census/` with text-ref edges and readability fixes to the formula graph.
- **Citations and calibration:** Xi 2026 WAIC keynote (intergovernmental dual-mandate instance); Hassabis Frontier AI Standards Body proposal (ch33); Byrnes social-drive distinctions (ch15); embedded value formation cross-refs (ch15, ch45).
- **Graded-lab Q1 null harvest (GL-76/77):** V2-3 machinery-transfer battery on blinded-grown ecology — UAD mechanism recovery and EAI mid-band nulls recorded in ch07, ch33, ch41, ch42, and Appendix N; BIQ harness fix for singleton inferred units.

### Empirical spine — graded-lab simulation (`experiments/graded-lab-simulation/`)

- **v1 program closed** (GL-31): terminal summary, reproduction guide, `PLAN_v2`.
- **v2 / V2-2b closed** without a passing ecology; **v3 institutional runtime** (`PLAN_v3.md`) through slice **D criteria freeze** (GL-53, reference battery at T=200).
- **v3 grower** rounds (GL-70–72), **v3_grown ecology freeze** (GL-73), pre-Q1 batteries (GL-74), **V2-3 transfer battery** harness and parallel runs (GL-75–76).
- Proper UAD + access-UAD (GL-51); supplementary detector and ACL gates through GL-63; package version stepped through 0.32.x–0.38.x on recorded milestones.

### Other experiment lines (selected)

- **Lab-simulation:** D3 selection ecology (G-36/G-37), user-population vote-channel capture; batteries and findings G-38–G-41; graded-lab successor line proposed and built.
- **Site PDF policy** documented (PDF de-emphasised on homepage; remains canonical long-form artifact).

### Housekeeping

- `npm run check:concepts` validates generated cards and search index (check-only mode).
- Conversation logs and session handoffs under `drafts/conversation-summaries/` for graded-lab and site work.

---

## v1.1.0 — 2026-07-08 — Legibility, companion site, and empirical spine

A consolidation release focused on **external legibility** (making the framework readable and checkable by outside researchers, funders, and policy readers), a full **companion website**, a new **institutional-histories appendix**, and four **empirical experiment lines** that stress-test bridge cruxes. 

### Reader-facing language and legibility

- **Cleaned up vocabulary** Load-bearing jargon now leads with an operational paraphrase and keeps coined terms only as shorthand. Symbols, equations, and Lean predicate names are unchanged.
- **Operational glossary (Appendix E) rewritten and expanded.** Each entry is paraphrase-first with a *nearest field term* delta and a concrete (often non-AI) example. 
- Front-matter orientation, README split, guided reading paths, and the About authorship note tightened for outside readers.

### New appendix — Institutional histories (Appendix D / `appM`)

- Mechanism-led historical case studies of institutional genesis, stabilization, entrenchment, and failure, with prior AI-governance literature credited; 24 sources in `references/institutional-histories.bib`; cross-refs in Appendix C and Chapters 27, 31, 34, 37.
- Site overview hub with eleven case-study cards, a non-technical intro, and a full synced-text subroute; wired into the Funder/Policy and Philosopher guided paths.

### Companion website (`site/`)

- Astro publication layer: guided paths, concept and standalone-claim cards, chapter pages, a Lean-spine web layer with graph navigation, badges, an experiments page (YAML-synced), and in-browser PDF.

### Empirical spine (`experiments/`)

- Five in-repo simulation lines (toy, embedded, goal-agent, lab, graded-lab) that stress-test bridge cruxes with **tentative, partial** support only.
- Lab-simulation line added and taken through multiple phases (graded red-team access tiers, unattributed-drift detection, blind detector generation, LLM red-team adapter, test batteries, adversarial-lineage gaming); goal-agent and embedded-sim lines extended; Lean spine gained Shannon entropy / mutual-information bounds and a successor-forgeability (MB10) formalization.

### Housekeeping

- `src/` renamed to `demos/`; 
- bibliography enriched with canonical DOI/URL fields.
- `make check` (structure, citations, bibliography summaries) passes.

---

## v1.0.0 — 2026-06-30 — First official major release

Commit: `bd8f82f` · Tag: `v1.0.0`

The first official release of the manuscript. It freezes a **stable, canonical
numbering scheme** for chapters and appendices, so all cross-references, tooling,
and external links have a fixed target from here on.

### Highlights

- **Sequential chapters `ch01`–`ch48`.** The temporary split chapters
  (`ch19b`, `ch25b`, `ch35b`, `ch39b`) are absorbed into the main sequence.
  Filename prefix, `metadata/book.yml` key, generated table column, and the
  printed `\chapter{...}` number now all agree.
- **Appendices A–G** match their printed letters in `book.tex` include order
  (Notation, Bridge Crosswalk, Institutional Translation, Worked Example,
  Glossary, Research Program, Lean Proof Spine). Stub appendices are parked at
  H–L.
- **History preserved.** All 40 path changes were committed as `git mv` renames
  (similarity 93–100%), so `git log --follow` traces each file through the
  renumber into its pre-release history.
- **Numbering scheme documented** as a canonical rule in `INSTRUCTIONS.md` §14
  (no more `b`-suffix file ids; tables derive numbers from manuscript order).

### Manuscript state at release

- 10 parts, **48 chapters** (all with first drafts and at least one review pass).
- **7 built appendices** (A–G) plus 5 stubs (H–L).
- Bibliography of ~235 categorized entries with one-line summaries.
- Self-contained Lean proof spine (`formal/`) calibrating manuscript claims to
  proof / counterexample / bridge status.
- Build: `./build.sh` → `dist/pdf/towards-superintelligence-alignment.pdf`;
  `make check` passes (structure, citations, bibliography summaries).

### Renumbering map

Chapters (split chapters shown; ch01–ch19 unchanged):

| Old id | New id |
|--------|--------|
| ch19b  | ch20   |
| ch20–ch24 | ch21–ch25 |
| ch25b  | ch27   |
| ch26–ch35 | ch28–ch37 |
| ch35b  | ch38   |
| ch36–ch39 | ch39–ch42 |
| ch39b  | ch43   |
| ch40–ch44 | ch44–ch48 |

Built appendices:

| Old file | New file (letter) |
|----------|-------------------|
| appBridge-crosswalk | appB-bridge-crosswalk (B) |
| appJ-institutional-translation | appC-institutional-translation (C) |
| appK-worked-example | appD-worked-example (D) |
| appF-glossary | appE-glossary (E) |
| appH-research-program | appF-research-program (F) |
| appI-lean-proof-spine | appG-lean-proof-spine (G) |

### Known issues

- ~48 undefined LaTeX references remain in the build, mostly pre-existing
  (`appe-assumptions`, `app:lean-proof-spine`, and similar); they are unrelated
  to the renumber.
- Some historical conversation logs and review notes still mention old chapter
  numbers in prose; these are archival and were left as-is.

### Upgrade / linking notes

- External links and citations should target the new `chNN` / appendix letters.
- Tag this release: `git tag -a v1.0.0 -m "First official major release" bd8f82f`.

---
