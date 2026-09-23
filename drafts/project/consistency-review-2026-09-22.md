# Project consistency review — 2026-09-22

> **Decisions and execution record (2026-09-23).** After reading this report the author decided: word targets are removed rather than reset; full funding applications stay out of the repo by design (only the anonymised site funding cards are public material); `ch46` corrections are tabulated but not applied; the Lean implementation route is taken and prose brought in line with code; visible manuscript TODOs are moved to comments with resolutions suggested, not implemented; a consistent backtest outcome vocabulary is proposed, not imposed; docs, links, closed plans, TODO.md, and orphans are fixed. What was executed is in §0 below; the original findings (§1–§10) are kept as written so the before/after is legible. Items still open are marked **open** in §0.

## 0. Executed 2026-09-23

| Decision | Done | Where |
|----------|------|-------|
| Remove size targets | `word_target`/`word_target_total` deleted from `metadata/book.yml`; `status: draft-reviewed`, `milestone: sixth`; "~350k"/"word targets" lines removed from `docs/MANUSCRIPT.md`, `INSTRUCTIONS.md` | `metadata/book.yml`, `docs/MANUSCRIPT.md`, `INSTRUCTIONS.md` |
| Funding applications | No change; recorded as intentional here and in `metadata/TODO.md` Outreach (crux-map line). Card-vs-application drift (§3 row) is therefore not a defect to fix in-repo | — |
| `ch46` corrections | Table with every occurrence, pre-image, correct chapter, evidence, and apply order: [`ch46-corrections.md`](ch46-corrections.md). 65 occurrences, 61 to fix, 2 correct as-is, 2 human calls; ~40 adjacent `ch45/47/48` cascade errors in its appendix; `claims-ledger.md` C-012 block also affected. **Applied 2026-09-23** by hand (decisions recorded at the top of the table; content-based homes overrode the map for `κ_ij`/`φ`/`φ_c` → ch13 and `S_certified` → ch30). Two legitimate `ch46` rows survive | `drafts/project/ch46-corrections.md` |
| Lean implementation + prose | All seven App G "P-node" labels now exist as theorems (`P34A`, `P34K`, `P35M`, `P35Mplus` in `Boundaries.lean`; `P12W`, `P10H`, `P38H` in `Capability.lean`), no `sorry`, no new axiom; App G cites them via `\leanid`; phantom `risk_bound_successor_safe_step` replaced; "all nine" → "all eleven Core bridge axioms"; `MB6a/b`, `MB7a–d` crux names; README/REVIEWING/CONTRIBUTING now say `BridgeAssumptions` packages eleven axioms under seven ids, `MB2` is a Prop crux, MB4a/10/11 threaded, P38/P39 not carried. Ledger extended to 48 headline theorems (`ofReduceBool` dependency of the C2 pin documented). `assurance-model.yml` gained the `filterCoverage` node; `sync-lean-spine.mjs` derives its module list (10 → 30). `lake build` green; `formal/check.sh` passes | `formal/`, `appendices/appG-lean-proof-spine.tex`, `formal/README.md`, `REVIEWING_FOR_AGENTS.md`, `CONTRIBUTING.md`, `metadata/assurance-model.yml`, `site/scripts/sync-lean-spine.mjs` |
| Visible TODOs moved, then resolved | Moved to comments first; resolutions in §0.1 applied the same day: ch01 framing paragraph and concrete-example rewrite; ch39 episode-floor paragraph with ch35 pointer; ch43 cruxes posed as named open problems in App G §`sec:master-crux` (+ `open-problems.md`); ch44 audit shape in the table; ch42 checklist-not-derivation sentence; ch45 six-bullet summary | `chapters/ch35`, `ch43`, `ch44`, `appendices/appG` |
| Backtest inconsistency | §0.2 scheme implemented 2026-09-23 in `docs/METHODOLOGY.md` § Backtests (vocabulary table, `stop` field, compound-as-lines, Appendix J rule keyed on the primary measurand so existing W-3 Pos./W-4 Ambig. verdicts stand, M2 freeze-hash rule), `backtest.md` template, and App J preamble; W-11 relabelled `pass (stop bit)` and W-16 split into two lines in ledger, `docs/EXPERIMENTS.md`, and YAML. Misreading audit: only the `docs/EXPERIMENTS.md` W-11 row had read as an inversion | `docs/METHODOLOGY.md`, `experiments/backtest/results/FINDINGS.md`, `docs/EXPERIMENTS.md`, `metadata/experiments-backtests.yml`, `appendices/appN` |
| Docs match structure | Parts table, bib count, version strings, appendix letter, `review/` pointers, AGENTS conversation-log section, CONTRIBUTING pointers, BUILD repo map, site README counts/route example, `experiments/README.md` link, `experiments/TODO.md`, `papers/README.md` (+ `institutions-and-construction` draft row), root README (papers list, Predictions row), `book-stats.md` regenerated with the appendix title offset fixed in `scripts/book_stats.py` | as named |
| Broken links | New `scripts/check_markdown_links.py` (report/`--fix`; resolves by unique basename or path suffix, directories included; skips site-routed markdown, dated session logs, sibling-repo paths). 49 links auto-fixed after the earlier depth batch; sibling-repo links re-pointed one level up; renamed attic files re-pointed by hand. Wired into `make check` | `scripts/check_markdown_links.py`, `scripts/check.sh` |
| Backtest naming | "Witness" → "Backtest" in all plan H1s and bodies, `drafts/plans/README.md`, `CONTRIBUTING.md`, `RELEASE_NOTES.md` (paths/anchors corrected, historical name noted once), `experiments-backtests.yml` (W-7 card regenerated), `docs/METHODOLOGY.md` heading capitalised so "§ Backtests" pointers resolve. Folders were already named `backtest/` | as named |
| Closed plans → attic | Voice (policy §9 lifted into `INSTRUCTIONS.md` §2), problem-axis, field spring-map, spec sheet, construct lit-review seed + prompt, backtest-next, predictions v0/incentives/Lean-improvements, epistemic census, residuals map, quiz length-tell outputs, June `review/` fix plan + continuity review (→ `review/attic/`); two 3-line stubs and the 5-word predictions redirect deleted; `sandboxed-agent-mcp.md` moved to `drafts/plans/` root as an unscheduled tooling draft. Attic READMEs updated; `strategic-advice` and `adversarial-steerability` carry a "historical record" header | `drafts/attic/`, `review/attic/`, `drafts/plans/README.md` |
| TODO.md | Lane list corrected (predictions in, voice out); Predictions row added to the work map; Site board: quiz marked shipped with residual, 215 questions, ch10 item moved to Experiments, three new site hygiene items; Outreach: crux-map (funding-gated) and the two sketches; Housekeeping: `ch46` corrections, manuscript TODO resolutions, backtest vocabulary, audit-telemetry placement; ⟳ item respecified; closed list extended | `metadata/TODO.md` |
| Lean honesty-of-structure in prose (June item 4, requested 2026-09-23) | Reader-facing name is now *dependency spine* everywhere (App G chapter and section titles, ch26/ch32/ch42/ch48, App E worked example, `docs/BUILD.md`, `formal/README.md`, site book index; file names and labels unchanged). App G opening gains *How to read the axiom count and the top theorem*: 172 `axiom` declarations = 15 bridges + 2 imports (the epistemic commitments) + ~90 Core carriers/predicates + 19 certificate adapters + 16 defeater signals + 10 field handles + typed measurands; the top theorem is named as packaging; separations/counterexamples named as the results that hold with no `MB*` footprint; ledger and satisfiability model cited. ch42 no longer calls MB2 an axiom. `book-stats.md` carries the same framing line | `appendices/appG`, `chapters/ch42`, `scripts/book_stats.py` |
| Stale status strings (requested 2026-09-23) | README status row and `docs/MANUSCRIPT.md` chapter row no longer state "48 reviewed / 0 draft"; "~250+ entries", "~350k", "v1.5.0 current", and "nine appendices" were already gone after the docs pass; the only remaining "v1.5.0" is the historical themes paragraph | `README.md`, `docs/MANUSCRIPT.md` |
| WWCTV openers (§8 item, requested 2026-09-23) | `INSTRUCTIONS.md` §2 now states the rule as one impersonal framing line then the list (two accepted shapes), never `we argue`, never a bare list; ch35, ch42, ch43, ch47, ch48 received a chapter-specific framing line (ch28 already had one). The 19 chapters using "This chapter treats/models/defines …" variants are within the rule as restated | `INSTRUCTIONS.md`, five chapters |
| `INSTRUCTIONS.md` ↔ Appendix H (requested 2026-09-23) | New "Appendix H — scope" paragraph in §14 and a canonical-home row: prediction-first order, 18 stable IDs, listing-status vocabulary, Markets 19–20 draft until Phase 4, the two assurance sections and their manifest, the price/YES invariants, site-only interactive model, sync command and the expected 20-vs-18 warning. This accepts the PRA layer as App H scope (report §8 option a) | `INSTRUCTIONS.md` §14 |
| Orphans | Eight scripts → `scripts/attic/` with README lines; root `node_modules/` and `.astro/` deleted. `REPRODUCING.md` is a distinct v1 closure record (GL-0–31), not a duplicate, and stays (§5.6 was wrong on that point). `value-detect-*` trees untouched (untracked local data) | `scripts/attic/README.md` |

### 0.1 Manuscript TODOs: suggested resolutions (applied 2026-09-23 except ch38 and ch21, which stay open by design; ch01 was not downgraded because both notes were resolved)

| Site | What it says | Suggested resolution | Effort |
|------|--------------|---------------------|--------|
| `ch01` line 36 (`%TODO`) | "Needs a structuring intro" with a proposed object/subject/content triad | Add one framing paragraph before "The Standard Picture and Its Failure" naming the three things the standard picture fixes (the optimised object, who does the aligning, what content is transported) and saying the chapter argues the first is misidentified. Do not adopt the triad as chapter structure; it is a reading aid | S |
| `ch01` line 79 (`%…TODO: rewrite`) | Paragraph flagged as AI-slop | Rewrite the paragraph in the author's voice (`context/writing-style-gunnar.md`): one concrete example of a "visible model" that was not the optimizer, then the claim. Until done, downgrade ch01 to `status: draft` in `book.yml` so the first chapter a reader sees is not marked reviewed with an open rewrite note | S |
| `ch35` `% TODO[probe-local-inferential]` | Local episodic coupling vs graph-level detection | Bounded answer in ch39 (passive observation): state that graph-level detection needs ≥k repeated episodes and that one-shot coordination below that count is undetectable by construction; then ch35 cites that bound and marks the residual as an open crux in `metadata/open-problems.md`. Do not extend ch35 | M |
| `ch43` `% TODO[open-crux]` ×2 | Perturbation a superintelligence cannot recognise as a test; measure of decisive-yet-undetectable controllers | Convert both into named open problems in App G research program with a one-line "what would count as an answer" each; keep the ch43 WWCTV pointer. This is the ELK-style posed-problem move the June advice asked for | M |
| `ch44` `% TODO[update-operator-audit]` | Gradient hacking row: no audit specified | Cross-reference the ch25/ch26 update-operator objects (\(U_H\), \(U_S\)) and state the audit as a two-sided test: measured CCI under a frozen \(U_H\) vs after the system has influenced training data. Ties to the "update-operator ontology audit" Housekeeping item; resolve together | M |
| `ch42` `% TODO[grounding-layer-completeness]` | Whether the eight layers derive from a completeness argument | Keep as an explicit "ad-hoc checklist; not derived" sentence in the chapter (already the honest status) and close the TODO; the completeness question is Construct 2.0 material | S |
| `ch38` `% TODO[formalize]` | Race/certified basins not tied to percolation predicates | Leave open; belongs to Spine P3 "ch48 basins" item. Add a `{bridge}` tag only if a Lean object exists | — |
| `ch21` `% TODO[citation]` | Turner Reward≠OT full post | Cite/Wait board already tracks it; nothing to do until published | — |
| `ch45` (no §6 summary) | Ends with a prose conclusion | Add a 6-bullet `\section{Summary}` before the conclusion (the conclusion stays); bullets can be lifted from the chapterthesis and WWCTV | S |

### 0.2 Backtest outcome vocabulary: proposed consistent scheme

The declared set (`pass|fail|refuse|null`) no longer covers what the ledger records, and "fail" is used with two meanings. Proposal, to be adopted in `docs/METHODOLOGY.md` § Backtests, the `backtest.md` finding template, and Appendix J's how-to-read note, then applied to the 17 entries:

1. **Two separate fields, never one word.** `outcome` says what the frozen protocol returned about the *layer under test*; `stop` says whether a stop condition fired on the host. Today W-11's "fail" means the stop worked (good for the host, bad for the "green-with-no-stop" hypothesis), while W-9's "fail" means green-with-no-stop. One word cannot carry both.
2. **`outcome` vocabulary (closed set):** `fail` (layer failed: the named leaf was green while the referent moved, or the checklist passed and an unlisted invariant broke), `pass` (layer held on this host: frozen instrument predicted held-out behaviour), `refuse` (the measurand cannot be verified on this host; valid stop for Expectation 3), `null` (protocol ran, no signal either way), `structure_stop` (the protocol could not be applied because the host's structure does not fit the access model; distinct from `refuse`, which is about adversarial verifiability). Add `structure_stop` and `null` to both documents.
3. **`stop` vocabulary:** `yes` / `no` / `n/a`, as the template already has; W-11 becomes `outcome: pass (stop bit)` with `stop: yes`, W-9/W-10 stay `fail` with `stop: no`.
4. **Compound outcomes are two rows, not one string.** W-3, W-4, W-16 record layer-fail plus a second result (refuse or detection-pass); record each as its own line in the ledger and in `experiments-backtests.yml` (`outcomes: [...]`), so the YAML cannot drop half of the verdict as it does for W-16.
5. **Appendix J classification rule (state it once):** Pos. = at least one `fail` on a book layer or a `structure_stop`; Neg. = `pass` only, or `null`; Ambig. = `refuse` only. Under that rule W-3 and W-4 both become Pos. (both have a layer fail); if the author prefers W-4 as Ambig., the rule must name why (causal RfA refuse dominates), and the same rule then applies to W-3.
6. **Freeze-order evidence (M2).** For W-1–W-17, add one honest sentence in METHODOLOGY that freeze files and checkers were co-committed; for W-18 onward, commit the freeze first and record its commit hash in the ledger's "Frozen protocol" line and in the preregistration JSON.

Effort: S for the vocabulary and rule; S for relabelling 4 entries and regenerating cards. *(Implemented 2026-09-23; see §0 row.)*

### 0.3 Progress and findings after the review (2026-09-23)

State of the original §3 scorecard after execution:

| Area | Now |
|------|-----|
| Manuscript | Contract fully met (ch45 summary added; no reader-visible TODOs; ch01 notes resolved). PDF builds with zero undefined references. Remaining `% TODO` comments: ch21 citation (waits on external post), ch38 formalize (Spine P3) |
| Lean spine | Code and prose agree: App G identifiers all resolve (175 distinct, 26 modules), one stale `\texttt{}` name fixed, seven appendix-only labels are now theorems, ledger 48 theorems, honesty-of-structure paragraph in App G |
| Experiments / backtests | Vocabulary closed; W-11 and W-16 relabelled; naming rename complete; freeze files marked as records |
| Site / demos | Unchanged except regenerated cards; three hygiene items on the Site board (`check:concepts` timestamp, demo back-links, predictions sync regex) |
| Predictions / papers / funding | Papers README complete (7 dirs); funding cards are the public record by decision; predictions drafts atticed |
| Plans / TODO / HANDOFF | Ten closed or spent plans atticed; all links resolve; link check in `make check`; TODO.md boards current |
| Ledgers / reviewer docs | `ch46` cascade corrected (61 rows plus ~40 adjacent); no word targets; `book.yml` header current |
| Docs | Version strings, parts table, appendix letters, pointers all match the tree |

Findings that surfaced only during execution:

- The renumber cascade was wider than the five files first named: it also hit `claims-ledger.md` C-012 (believed clean) and five Housekeeping lines in `metadata/TODO.md`; all corrected. Content overrode the map twice (`κ_ij`/`φ`/`φ_c` live in ch13, `S_certified` in ch30).
- `docs/EXPERIMENTS.md` presented W-11 as the same "Fail" shape as W-9/W-10 although the Debian stop worked; the manuscript and site card were right. This was the only genuine misreading the vocabulary drift produced.
- App G cited one theorem name that no longer exists (`debate_truth_not_correction_preservation`); everything else in App G resolves. The scan needed `alias` declarations to be counted; 31 field names are aliases.
- `REPRODUCING.md` is not a duplicate of `REPRODUCTION.md` (v1 closure record); the original §5.6 was wrong on that point.
- Pre-existing and untouched: 104 `\nocite` keys in the generated `metadata/global-nocite.tex` have no matching bib entry (LaTeX warnings only; `check_citations` covers cited keys, not the nocite list). Worth a look at `scripts/generate_global_nocite.py`.
- A concurrent session archived logs and regenerated `INDEX.md` while this work ran; `site/src/data/chapter-reading-graph.json` dirties on every build because of a `generatedAt` stamp (Site board item).

---

**Scope.** Whole repository at HEAD `784d89aa` (2026-09-22): manuscript, Lean spine, experiments and backtests, companion site and demos, papers, predictions lane, funding and outreach, plans, ledgers, docs, scripts. Old conversation logs and `attic/` folders were not read. The question asked: how well does the project meet its stated and implied expectations, and where should expectations or implementation be adapted to reach a consistent state quickly.

**Method.** Six read-only area reviews (manuscript, Lean, experiments, site/demos, predictions+papers+funding, plans+metadata+docs) plus direct checks: `make check`, site and demo builds, `lake build`, git cadence, link and naming greps. Every finding below names a file; counts were re-derived, not copied from docs.

---

## 1. Verdict

The project is in better shape than its own documentation says, and in worse shape than its own documentation *layer* implies.

- **The built artifacts are green.** `make check` passes all 13 gates. `lake build` is sorry-free with the axiom-budget guard passing (40 headline theorems, no drift). The site builds 1,113 pages; all documented routes exist. All 48 chapters satisfy the §6 structural contract except one missing summary section. All 17 backtest findings are present and ID-consistent across five surfaces.
- **The instruction layer has drifted in three specific, dateable ways** and that drift is what makes the project feel inconsistent:
  1. The 2026-06-30 chapter renumber collapsed many old chapter ids onto `ch46` in ledgers and reviewer-facing docs, and those rows were never re-derived. This is silently wrong content in `metadata/notation.md`, `metadata/assumptions-ledger.md`, `metadata/uncertainty-ledger.md`, `REVIEWING_FOR_AGENTS.md`, `llms.txt`, and the June `review/` files.
  2. The 2026-09-07 "Witness" to "Backtest" rename was applied to the directory and the manuscript but not to the plan titles, `RELEASE_NOTES.md`, `experiments/README.md` (broken link), `CONTRIBUTING.md`, `metadata/book-stats.md`, and one YAML row that feeds a site card.
  3. The 2026-09-19 `drafts/` restructure moved lane plans one folder deeper without rewriting relative links. About 135 links in the planning layer now point at nonexistent paths.
- **Expectations that no longer describe the book:** the 375k-word per-chapter targets (actual 238k, 64%), the "~350k" and "~250+ bib entries" lines, `book.yml` still saying `milestone: third`, `docs/MANUSCRIPT.md` still carrying the pre-renumber parts table with a phantom `39b`, and `llms.txt` advertising v1.5.0.
- **Velocity has shifted from breadth to one lane.** Commits per active day fell to roughly a third of the June–August rate. September work is almost entirely the predictions lane (13 of 19 September session logs), which grew Appendix H by 43% in four days. Nothing is wrong with that lane, but the rest of the plan layer has not been consolidated while attention moved.

**Recommendation in one line:** spend one short consolidation session (mostly S items, listed in §6) before the next content lane, and reset the handful of expectations that the artifacts have outgrown rather than trying to grow the artifacts to meet them.

---

## 2. What the project promises

Stated expectations come from `README.md`, `INSTRUCTIONS.md` (§6 chapter contract, §12 acceptance, §14 numbering), `AGENTS.md` (Erasure rule, session logs, Lean calibration), `docs/METHODOLOGY.md` (freeze, prereg, outcome vocabulary), `formal/README.md`, `metadata/TODO.md` (work map and gates), and the five lane plans.

Implied expectations come from the June 2026 external strategic advice (`review/strategic-advice-2026-06-28.md`), the hostile review (`drafts/editorial/hostile-review.md`), and the backtest plan's own framing ("meet the implied reader expectations for real, not by stronger disclaimers"). Those set the bar as: one real measurement that can fail, extracted standalone claims, a posed open problem, honest Lean framing, and external contact.

Section 7 scores the project against that external yardstick. Sections 3–5 score it against its own rules.

---

## 3. Scorecard by area

| Area | Stated contract met? | Main gap | Fix type |
|------|---------------------|----------|----------|
| Manuscript (48 ch, 10 app) | Yes, mechanically (47/48 full pass; checkers green; appendix map exact) | Word targets and meta-status stale; TODO text leaks into reader prose; Lean calibration absent in 8 `formal_density: high` chapters | Mostly reset expectations; 3 small implementation fixes |
| Lean spine | Yes (green, sorry-free, CI-gated) | README/App G say "nine bridges in `BridgeAssumptions`" and MB2 "declared as axiom"; neither is true. One phantom `\leanid`, seven appendix-only "P-node" labels | Reset wording; one M item |
| Experiments + backtests | Yes in substance (17/17 consistent; template followed) | Rename debt; outcome vocabulary outgrew the declared set (`structure_stop`, `null`); 11 closed freeze files indistinguishable from live plans | Small implementation batch; one M reorganisation |
| Site + demos | Yes (builds, routes exist, generated files in sync) | `check:concepts` always fails and is not in CI; one tracked file churns each build; demos unreachable from chapters | Two S fixes; one M |
| Predictions lane | Yes for Phases 0–3 as declared | Permanent sync warning 20≠18; dead card extractor; four superseded drafts not atticed; no enforced YAML validation despite the log claiming it | S batch |
| Papers | Partly | 7 dirs vs 6 in `papers/README.md` vs 4 in root README; one paper unbuilt and undocumented; two PDFs older than their source | S |
| Funding / outreach | Untracked by design (folder gitignored; confirmed intentional 2026-09-23) | Site cards are the only public record; they differ from the local applications in two durations and two amounts | None in-repo; author may align cards when convenient |
| Plans + TODO + HANDOFF | No | ~10 closed or spent plans still look live; 135 broken links; TODO lane list omits predictions; `review/` labelled "active" but frozen since June | Attic batch (S–M) |
| Ledgers + reviewer docs | No | ch46 collapse (see §4.1) | M, content re-derivation |
| Docs (README, BUILD, MANUSCRIPT, CONTRIBUTING, llms.txt, AGENTS) | Partly | Version, parts table, appendix letter, section pointers stale; AGENTS.md conversation-log section contradicts itself | S batch |

---

## 4. Findings that change content correctness

These are the items where a reader or agent following the docs would be told something false. They outrank the hygiene items.

### 4.1 The `ch46` collapse (highest severity)

Commit `bd8f82f` (2026-06-30 renumber) rewrote many distinct old ids to `ch46`. Current counts of `ch46` references, most of them wrong:

| File | ch46 refs | Example error |
|------|-----------|---------------|
| `review/fix-plans-2026-06-22.md` | 142 | whole document |
| `review/full-book-continuity-review-2026-06-22.md` | 51 | whole document |
| `metadata/assumptions-ledger.md` | 31 | line 23 "ch46–27 correction channel" |
| `metadata/notation.md` | 14 | lines 91–95 put `L`, `DL`, ΔL homes at ch46; they live in ch22 |
| `REVIEWING_FOR_AGENTS.md` (+ site mirror) | 10 | gem map: "Value bundles: ch15–ch46", "Transport hierarchy: ch46", "Vector/status CCI: ch46" |
| `metadata/uncertainty-ledger.md` | 8 | |
| `llms.txt` | 1 | line 68 |

`metadata/claims-ledger.md` was re-verified content by content (its header says so) and is clean. The others were not. `REVIEWING_FOR_AGENTS.md` is the file external reviewers are told to read first, so this is reader-facing.

**Fix (M, implementation):** re-derive each ch46 row from `bd8f82f^` plus the renumber map in `RELEASE_NOTES.md` (v1.0.0 section). For the two `review/` files, attic rather than fix (§5.4).

### 4.2 Lean framing wording

`formal/README.md` lines 26 and 233–236, `REVIEWING_FOR_AGENTS.md` line 27, and `CONTRIBUTING.md` line 13 say MB1–MB9 are packaged in `BridgeAssumptions` and that MB1–MB11 are "declared as `axiom`". In source, MB2 is `def MB2Crux` (a Prop hypothesis, `MB2Identifiability.lean:67`), and `BridgeAssumptions` (`Core.lean:621–632`) holds MB1, MB3, MB4, MB5, MB6a, MB6b, MB7a–d, MB9: eleven axioms, seven numbered ids, neither MB2 nor MB8. `appG` line 1915 says the headline theorem "depends on all nine". `appG` line 1489 cites `risk_bound_successor_safe_step`, which does not exist (nearest: `true_harm_bound_of_successor_safe_step`). `appG` lines 920–1149 typeset `P34A`, `P34K`, `P35M`, `P35M+`, `P10H`, `P12W`, `P38H` as Lean node ids; none exist in `.lean`, the graph, or the site registry.

This matters because Lean honesty-of-structure was the June advice's item 4 and the hostile review's §3. The spine itself is fine; the prose overstates its packaging.

**Fix (S, expectation):** reword the three docs and App G line 1915 and 1489. **Fix (M, implementation, preferred):** add the seven small theorems under those names or drop the `\texttt{}` node styling and mark them appendix-only.

### 4.3 Reader-visible TODO leaks and repo paths in the book

`ch35` line 415 has a `\textbf{TODO[probe-local-inferential]}` bullet in body text; `ch44` line 346 has "explicit TODO" in a table cell; `ch43` line 137 and `appG` line 1482 cite `metadata/TODO.md` by repo path inside the PDF. `ch01` lines 36 and 79 carry raw editorial comments ("Needs a structuring intro", "reads like super-AI-slop, rewrite") while the chapter is marked `reviewed`. `ch45` has no `\section{Summary}` (§6.6).

**Fix (S, implementation):** move the two visible TODOs into `% TODO[...]` comments, replace path mentions with "open problem (research program appendix)", add a bullet summary to ch45. **ch01 (M):** resolve the two notes or downgrade the chapter to `draft`; it is the first thing a reader sees.

### 4.4 Backtest outcome vocabulary

`docs/METHODOLOGY.md` allows `pass|fail|refuse|null`; the `backtest.md` template allows `pass|fail|refuse`; W-17 is `structure_stop`. W-11 uses "fail" to mean "the stop worked", inverted relative to W-9/W-10 where fail means green-with-no-stop. W-3 and W-4 have the same ledger outcome (fail+refuse) but map to Pos. and Ambig. in Appendix J with no stated rule. W-16's YAML drops the "fail (layer)" half of its ledger verdict.

**Fix (S, expectation + implementation):** add `null` and `structure_stop` to both vocabularies; add a one-line Pos./Neg./Ambig. mapping rule to Appendix J; relabel W-11 as "pass (stop bit)"; add the fail label to W-16's YAML.

### 4.5 Docs stating wrong structure

- `docs/MANUSCRIPT.md` lines 38–49: parts table is pre-renumber (IV 15–19 … IX "36–40 plus 39b", X 41–48). Actual: IV 15–20, V 21–24, VI 25–29, VII 30–33, VIII 34–38, IX 39–44, X 45–48. `39b` exists nowhere else.
- `INSTRUCTIONS.md` line 219: "open-problems.md overlaps Appendix H" — H is now predictions; the research program prints as G.
- `llms.txt` lines 20 and 39: "current: v1.5.0"; line 27 links `/demos/all/`, removed 2026-09-19.
- `experiments/README.md` line 25: links `witness/`, which does not exist.
- `CONTRIBUTING.md` line 19: "`metadata/TODO.md` (§ Lean proof spine)" — no such section.
- `INSTRUCTIONS.md` line 298: `review/_pass/` is now `review/attic/_pass/`.
- `AGENTS.md` lines 201–210: lists INDEX.md and README.md twice and says "Per-session `.md` log files are retired", contradicting line 127 and the folder README (a leftover of the reverted 2026-07-31 experiment).
- `metadata/book.yml` lines 4–6: `status: scaffold`, `milestone: third`, `word_target_total: 350000` (per-chapter sum is 375,000). The file also fails PyYAML `safe_load` at line 302 (`\h` in a double-quoted string); the build uses a custom parser so nothing breaks today.
- `metadata/book-stats.md`: generated 2026-09-07, says 9 appendices (now 10), names `WitnessC2Instance.lean` (now `BacktestC2Instance.lean`), and its appendix table pairs each file with the *next* file's title (appD row shows appM's title, and so on) — a generator offset bug worth one look in `scripts/book_stats.py`.

**Fix (S, expectation):** one docs pass. Regenerate the parts table from `tables/part-roadmap.tex`; regenerate `book-stats.md` after fixing the title offset.

---

## 5. Findings about the instruction layer (Erasure-rule violations)

`AGENTS.md` says spent work that still looks live is worse than missing detail. By that rule:

### 5.1 Broken links after the drafts restructure

About 135 broken relative links, almost all in `drafts/plans/{field,spine,construct}/` (moved one level deeper, kept `../../` for repo root and flat sibling names), plus `HANDOFF.md` line 64 (`../plans/construct.md`), `construct.md` (links to `../ontology-reviews-2021-2026/`, actual folder `drafts/ontology/reviews/`), and several root plans pointing at session logs since archived. Verified example: `drafts/plans/field/field.md` line 3 → `../../reference/field-agendas/data/bridges.yml` resolves to `drafts/reference/...`, which does not exist.

**Fix (S–M, implementation):** one link-fix pass, then add a markdown link check to `scripts/check.sh` so the next move cannot break silently.

### 5.2 Rename debt ("Witness" → "Backtest")

Beyond §4.5: all 15 `drafts/plans/backtest/*.md` H1 titles still say "Witness"; `backtest.md` lines 16 and 311 and `backtest-next.md` line 19 cite "`docs/METHODOLOGY.md` § Witness", a heading that does not exist; `construct.md` (8 places), `spine.md`, `drafts/plans/README.md`, `CONTRIBUTING.md` line 27, `RELEASE_NOTES.md` v1.6.0 section (wrong dir, wrong site anchor `#witness`, "Appendix I"), and `metadata/experiments-backtests.yml` line 332 ("Witness host", which propagates to the generated W-7 site card). The manuscript proper is already consistent (`appN` uses "backtest").

**Fix (S, implementation):** sed pass, then re-run `sync-releases` and `sync-experiments`.

### 5.3 Closed or spent plans still presented as live

In `drafts/plans/`: `voice.md` (closed 09-07, 245 lines; still the only home of the front-door policy §9), `problem-axis-incorporation.md` (closed), `appendix-stubs.md` and `front-door-vocab.md` (3-line closed stubs with dead links), `field/field-spring-map.md` (built), `construct/cousin-product-comparison.md` (implemented, misfiled), `construct/construct-lit-review-prompt.md` and `construct-external-lit.md` (spent inputs, verdict already folded into `construct.md`), `construct/sandboxed-agent-mcp.md` (no status, no inbound references), `backtest/backtest-next.md` (fully duplicated by `backtest.md` lines 16–18), `backtest/backtest-v2-moltbook-inventory.md` (folded into the mb7a freeze). Eleven backtest freeze files are the preregistration record per `METHODOLOGY.md` and must be kept, but they sit beside the live plan with nothing marking them frozen at a glance.

In `drafts/predictions/`: `predictions-improvements.md` (5-word redirect), `predictions-improvements-v0.md` (4,096 words, self-labelled archive), `predictions-improvements-incentives.md` (absorbed), `bridge-predictions-Lean-improvements.md` (self-declared historical), and an unreferenced `lean_checked_bayesian_pra_diagram.py` under `plans/predictions/`.

In `drafts/project/`: `epistemic-status-field-census.md` (2026-07-17 one-off, applied) and `what-tsa-fails-to-represent-residuals.md` (assembled into `metadata/concepts/bodies/` on 09-08); neither has inbound references. `tsa-shipping-benchmark.md` is a velocity baseline, not a definition of done, and was not re-run after v1.6.0.

Untracked-but-open: `field/alignment-crux-map.md` (12 unchecked grant deliverables, "not funded yet"), `iliad-communal-canon.md`, `lw-wiki-tags.md`, `audit-telemetry.md` (five items awaiting an author decision) appear on no TODO board.

**Fix (S–M, expectation):** attic the closed and spent files with a session-log note; move `voice.md` §9 into `INSTRUCTIONS.md` and attic the rest; move the 11 freeze files to `experiments/backtest/protocols/` (which `backtest-v2.md` line 107 already anticipates) so `drafts/plans/backtest/` holds only `backtest.md` and `backtest-v2.md`; add one Outreach-board line each for crux-map and the two sketches or attic the sketches; give `audit-telemetry` its own TODO line.

### 5.4 `review/` folder labelled active

`AGENTS.md` line 191 and `INSTRUCTIONS.md` lines 17 and 145 call `review/fix-plans-2026-06-22.md` the "active fix list". Its last content edit is 2026-06-23; it is ch46-corrupted; its open items (§A dedup, §C9, §C16, §G, §H7, §H8) appear nowhere in `metadata/TODO.md`. `full-book-continuity-review-2026-06-22.md` scopes "ch01–ch48 + ch47, appendices A–H" (pre-renumber). `strategic-advice-2026-06-28.md` and `adversarial-steerability-*.md` are frozen external feedback that other files cite; they should stay but be marked as records.

**Fix (M, expectation):** attic the two June working files; lift the §A "one home chapter, elsewhere reminder/reference/elide" rule into `INSTRUCTIONS.md` §4 inline; add a "historical record" header line to the two advice files; repoint `AGENTS.md` and `INSTRUCTIONS.md`; decide in one TODO Housekeeping line whether any §A/§C9/§C16/§G item survives.

### 5.5 TODO.md internal drift

Line 9 lists lanes as `voice, backtest, field, spine, construct` (voice is closed; predictions is missing) while line 46 and `plans/README.md` list predictions. Line 119 refers to "⟳ rows in `metadata/notation.md`"; there are none (either done or lost). The Site board's quiz item is stale (quiz shipped; chapter-page blocks remain), "211/211" is now 215 questions, and the ch10 alignment-faking item is an experiments item on the Site board. `experiments/TODO.md` line 15 says "W-1–W-15 recorded".

**Fix (S, expectation).**

### 5.6 Orphan scripts and root hygiene

Eight scripts have no reference outside `scripts/` and logs: `apply_authbars.py`, `patch_authbar_keys.py`, `strip_empty_authbars.py`, `fix_conversation_log_references.py`, `init_scaffold.py`, `make_chapter_stub.py`, `write_takeaway_quiz.py`, `write_news_takeaway_quiz.py`. `scripts/attic/` already exists with a README. Root `node_modules/.vite` and `.astro/dev.json` show `astro dev` was run from the repo root on 09-22 despite the AGENTS.md rule; both are gitignored and harmless. `graded-lab-simulation/` has both `REPRODUCTION.md` and `REPRODUCING.md` (correction 2026-09-23: these are distinct documents, the latter being the v1 closure record for GL-0–31; not a duplicate). `value-detect-v1-master/` and `-v2-master/` are untracked log-only trees referenced by one README line.

**Fix (S):** move the eight scripts to attic; delete root `node_modules/` and `.astro/`; either index or delete value-detect and drop the README line.

---

## 6. Consolidation program

Ordered so that the first batch can be one session and leaves the repo internally consistent. Effort: S under a session, M one to three sessions.

### Batch A — expectation resets (all S, one session)

1. `docs/MANUSCRIPT.md`: regenerate parts table; "~500 bib entries"; drop "~350k".
2. `metadata/book.yml`: `milestone: sixth`, `status: draft-reviewed`, `word_target_total: 375000` or lower per-chapter targets to current+10% (see §8); quote the `\h` string.
3. `INSTRUCTIONS.md`: line 219 letter; line 298 path; §2 voice rule reworded to what `check_voice.py` enforces (impersonal "This chapter …" opener, never `we argue`); §4 inline the fix-plans §A rule; §11.4 "calibrate where a Lean module exists; otherwise say so in WWCTV".
4. `AGENTS.md`: delete lines 207–210; repoint line 191.
5. `CONTRIBUTING.md` lines 19 and 27; `llms.txt` version and `/demos/all/`; `docs/BUILD.md` line 116 repo map; `site/README.md` route table, counts, curl example.
6. `formal/README.md` lines 26 and 233–236, `REVIEWING_FOR_AGENTS.md` line 27, `appG` lines 1489 and 1915: correct MB2 form and "eleven axioms / seven ids".
7. `metadata/TODO.md`: lane list, ⟳ item, Site board quiz item, move ch10 item, 215 questions; `experiments/TODO.md` line 15.
8. `docs/METHODOLOGY.md` and `backtest.md` template: add `null`, `structure_stop`; capitalise the "backtests" heading so the "§ Witness" pointers can become "§ Backtests".
9. `drafts/project/tsa-shipping-benchmark.md`: header "velocity baseline, not definition of done; as-of 2026-08-28".

### Batch B — hygiene implementation (all S, same or next session)

10. Rename sed pass (§5.2), then `cd site && npm run sync:releases && npm run sync:experiments`.
11. Link-fix pass (§5.1); add a markdown link check to `scripts/check.sh`.
12. Attic list (§5.3, §5.4, §5.6) with one session-log note; move freeze files to `experiments/backtest/protocols/`.
13. Manuscript leaks (§4.3): two visible TODOs, two repo paths, ch45 summary.
14. Site: drop `generatedAt` from `search-index.json` and `chapter-reading-graph.json` (or ignore in `--check`), then wire `npm --prefix site run check:concepts` into `scripts/check.sh`; downgrade the 20≠18 prediction warning to info while 19–20 are draft; retarget the `extractPriorTest` regex in `sync-predictions.mjs` to "Closest existing work" so cards regain that section; add `--check` enum validation for `marketStatus`.
15. Papers: add `institutions-and-construction` to `papers/README.md` or attic it; add a status column; rebuild the two stale PDFs; fix root README "4 papers".
16. Funding cards: align Foresight duration and crux-map/SAIGE amounts with the applications; add outcome notes for the three past-deadline applications; delete `__pycache__` in the local folder.
17. Backtest verdict labels (§4.4): W-11, W-16 YAML, Appendix J mapping rule; fix Appendix J line-meta ranges (LS-49, GL-88); cite toy `NEGATIVE_RESULTS.md`; FINDING_IDS toy note.
18. `scripts/book_stats.py` appendix title offset; regenerate `book-stats.md`.

### Batch C — content correctness (M)

19. Re-derive the ch46 rows in `notation.md`, `assumptions-ledger.md`, `uncertainty-ledger.md`, `REVIEWING_FOR_AGENTS.md` (regenerate site mirror), `llms.txt` (§4.1).
20. App G phantom node labels: add the seven theorems or demark them (§4.2).
21. ch01 editorial notes (§4.3).
22. Add `leanspine`/`leanbox` to the eight `formal_density: high` chapters that have none (ch07, 12, 19, 20, 22, 23, 24, 40) or lower their density tag.
23. Demo back-links: render a "Demo" chip on `book/[id]` and chapter cards from `demos.json`; fix `serve-demos.sh` to list all seven.

### Batch D — do not do now

- Do not grow chapters toward the 375k target in general (§8).
- Do not attic the eleven backtest freeze files; relocate them.
- Do not add Construction chapters, `PathRealizable`, or an `AlignmentContext` tuple (all correctly gated in the plans).
- Do not fold the ch46 fix into the June `review/` files; attic those instead.

---

## 7. Against the June 2026 external yardstick

`review/strategic-advice-2026-06-28.md` set eight items. Status as of today:

| # | Advice | Status | Evidence |
|---|--------|--------|----------|
| 1 | One end-to-end worked measurement with a capture case | **Substantially met, differently.** The backtests (W-1–W-17) are frozen fail/refuse protocols on histories the project did not write, which is a stronger class than the toy pipeline asked for. The in-book "worked example" (App E BioShield) is still fictional. | `experiments/backtest/results/FINDINGS.md`; `appD-worked-example.tex` |
| 2 | Extract 3–4 original claims as standalone notes | **Partly.** Six spin-out papers exist, but not on the four named claims (anti-capture validity, bearer-map commutation, Goodhart-as-selector, CCI-as-channel). Those remain "Expectation 6" in the backtest plan and unpublished. | `papers/README.md`; `backtest.md` §Expectation 6 |
| 3 | Pose the central open problem ELK-style | **Reframed.** Appendix H turns bridges into 18 dated, resolvable questions, which is a legitimate substitute for a single posed problem, but the single-sentence "certifying correction integrity against a manipulator" problem is still diffused across ch27/ch43. | `appP-bridge-predictions.tex` |
| 4 | Fix Lean honesty-of-structure | **Met (code and prose, 2026-09-23).** Axiom ledger, `#print axioms` guard, satisfiability model, "dependency spine" naming now used in the manuscript and App G title; App G states the axiom accounting, names the top theorem as packaging, and gives separations top billing (§0 row). | `formal/axiom-ledger.json`; `appendices/appG` opening |
| 5 | Engage Löbian tiling and Hubinger | **Met.** `Field/Finite/LobTiling.lean`; ch44 owns the mesa-optimization stress test. | |
| 6 | Make ledgers load-bearing | **Partly.** Claims ledger re-verified; A-* keyed assumption boxes in chapters. But three ledgers carry ch46-corrupted rows (§4.1), which is exactly the "credibility liability" the advice warned about. | |
| 7 | Deliberate adversarial review | **Started.** 25 named contributors; one substantive LW Lean critique (Harfe) answered; Kosoy corrected an agenda summary; Krym drove an architecture revision. No named engagement with a specific bridge on the backtest results yet. Independent reproduction (M8) is still open. | `metadata/feedback-contributors.md` |
| 8 | Repo and authorship hygiene | **Met.** "What this is and is not", authorship bars, AI-drafting disclosure. | `README.md`; `frontmatter/preface.tex` |

Net: items 1, 4, 5, 8 done; 2, 3, 6, 7 half done. The half-done items are all "exposure" items. The predictions lane is a plausible vehicle for 2, 3, and 7 at once (external listing forces named engagement), which is a reason to finish its Phase 4 listing gate rather than to extend its appendix further.

---

## 8. Expectations to reset rather than meet

These are places where the honest move is to change the stated bar.

- **Word targets.** 238k actual against 375k targets, with all 48 chapters `reviewed`, means the targets describe a book that was never written. Eleven chapters are under 50%: ch47 (21%), ch48 (25%), ch42 (26%), ch20, ch05, ch37, ch44, ch43, ch24, ch28, ch38. Reset targets to current+10% except three: ch42 (safety case, 2.6k words, named as "complete" in §12), ch47 and ch48 (closing synthesis, still Shape-A scaffolds at ~2k words). Those three are load-bearing and merit an L item on a future board; the rest are fine as they are.
- **"48 reviewed, 0 draft."** True but flat. Add a maturity signal (word-target %, TODO count) per chapter in `book.yml` or list the sub-50% chapters in `docs/MANUSCRIPT.md`, so "reviewed" stops implying uniformity.
- **WWCTV opener.** *(Done 2026-09-23: rule restated; five bare-list chapters given a framing line.)* 24/48 chapters use "This chapter treats/models/defines…" instead of "This chapter argues". Same register, often better.
- **Lean calibration per chapter (§11.4).** 27 chapters carry no `leanspine`/`leanbox`; most are legitimately non-formal. Amend the rule to "where a module exists".
- **"~250+ bib entries", "~350k words", "v1.5.0", "nine appendices".** Numbers that were true once. Replace with current or with pointers to generated files.
- **Appendix H scope.** *(Decided 2026-09-23: option a; `INSTRUCTIONS.md` §14 now describes App H including the assurance sections.)* The plan says "keep the predictions appendix prediction-first", yet the PRA derivation now lives inside it and the appendix is the second-largest.
- **`fix-plans-2026-06-22.md` as "active".** It is not. See §5.4.
- **`tsa-shipping-benchmark.md`.** A baseline, not a target. Label it.

---

## 9. What is working and should not be touched

- The chapter contract (§6) and its checkers. 47/48 full passes with no stubs in a 48-chapter book is unusual; keep the checker-first discipline.
- The Lean guard set (`check.sh`, axiom ledger, independence theorems, CI skip-if-untouched).
- The backtest ledger template and freeze discipline. The only methodological caveat is that freeze files and fixtures were co-committed (no independent git-order evidence for M2); record the freeze commit hash in future W-entries and add a one-line honest note for W-1–W-17.
- The generated-site pipeline. Everything regenerates; the tracked generated files are byte-identical to fresh output.
- The gating logic in `TODO.md` (Backtest real stop → Construct concrete chapters; no sixth intro claim in v1). It has held for a month under pressure to add chapters.

---

## 10. Not verified

- Whether external funding applications received outcomes (folder is gitignored; only site cards are versioned).
- Whether the "211/211" blind quiz solve still holds for the four questions added since (no re-run logged).
- Whether the sibling repositories (`agency-detect`, `brain-to-values`, `ciris`) still match the paths cited in `docs/MANUSCRIPT.md` and `backtest.md` (not on this machine's review path).
- PDF build (`./build.sh`) was not re-run in this session; `book.pdf` at root is from 2026-09-22 03:56 and the checkers that do not need LaTeX all pass.

---

## Appendix: per-area detail pointers

The six area reviews that fed this report were read-only agent passes. Their specific line-level findings are folded into §4–§6 above; no separate files were written. If a line number here has moved, grep the quoted text.
