# 2026-11-05 — Alignment-frames paper review against the lens model

kind: new-work
uptake: local

## Trigger

User: review the alignment-frames paper; since the draft many changes were done to the lens modeling. What should be incorporated, what is invalidated, what is missing, other comments.
Prompts: paraphrase-only

## Done

- content: Review at `drafts/project/alignment-frames-paper-review-2026-11-05.md`. It covers:
  - 7 invalidated or under-qualified items. Main ones: robust invariance vs correction (rigidity), the CCI list that is the ch25 audit list and not the ch26 vector, and three meanings of state utility;
  - 9 incorporate items. Main one: `FrameCorrector.blind_constraint_cannot_separate` as the formal counterpart of the learning-vs-rewiring case;
  - 5 general gaps: no tables or figures, unused schema, missing debate/ELK/assistance-game frames;
  - editorial notes.
- bookkeeping: verification. Every Lean name cited in the review was found by `grep` for its `theorem`/`def`/`instance` declaration under `formal/AlignmentProofSpine/` (24 names, none missing).
- bookkeeping: No edits to the paper, Lean, site or manuscript.

## Restructure (second request)

Trigger: the user asked to demote TSA from the running case and to cite strong precedents (esp. Turner) from the main bib. Proofs are to be referenced in the text, with extracts and links in an appendix. The paper is to use the four-class structure, apply the corrections, add a table and the SVG, and clean the editorial notes. The abstract is to be revisited after the rest.

- content: `papers/alignment-frames/alignment-frames.tex` rewritten:
  - TSA demoted; one discriminating case (§7);
  - relations §5 with Figure 1; four classes §6 with Table 2; inventory Table 1; case verdicts Table 3;
  - composition with orderings stated symmetrically and design rules by class;
  - Appendix A of Lean extracts.
  - Decisions and the item-by-item execution table are in review §0.
- content: `alignment-frames.bib`. The 38 entries from the main bib (count of `% from references` lines) are copied verbatim. 20 local entries were kept from the old paper bib. 15 are new: the 14 written for this paper (DOIs and page numbers left out where uncertain) plus `zarncke2026selection` copied from the alignment-under-selection bib. They should be checked before going into `references/`.
- content: `scripts/lean_extracts.py` generates `lean-extracts.tex` and `lean-pin.tex`. It extracts 63 declarations (docstring plus signature), links them pinned to `origin/main` when `formal/` matches it, and has a `--check` mode. `scripts/render_figure.sh` renders `figures/frame-relations.pdf` from `drafts/alignment-frames-relations.dot`. `build.sh` now uses LuaLaTeX (Menlo, falling back to DejaVu Sans Mono).
- bookkeeping: `drafts/alignment-frames-spinout-paper.md` atticed (superseded), with a note in `drafts/attic/README.md`. Links updated in `metadata/TODO.md`, `drafts/plans/construct/construct.md` and `drafts/alignment-frames-relations.md`. `papers/README.md` has a row and a note for the paper.
- bookkeeping: verification.
  - `./papers/alignment-frames/build.sh` → "Built alignment-frames.pdf" (36 pages). The log has 0 overfull hboxes and 0 undefined references. Biber's only warning is an invalid ISBN on main-bib `aubin1991viability`.
  - `lean_extracts.py --check` → "lean_extracts: up to date".
  - `lake build AlignmentProofSpine` → "Build completed successfully (2274 jobs)."
  - `#print axioms` on the three Soares aliases → `[propext, Classical.choice, Quot.sound]`.
  - The ledger shows extra (spine vocabulary) axioms only for `scalar_floor_blind_to_process`, and the appendix says so.

## Revision (third request)

Trigger: the user asked to split the epistemic/novelty statement into standard places, make "bearer" explicit, drop the argument against a running example, make §7 readable (why this case, why two routes, the non-implications), and rework §8 so that orderings, design rules and interface obligations are argued. The four external posts were to be discussed with suggestions only, without paper edits.

- content: the epistemic statement is split:
  - confidence line → title footnote;
  - contributions and non-claims → end of §1;
  - prior-art credits → §2 (Soares/Turner split, Hodge, a new "Constraints and scalarization" paragraph citing han1979exact and roijers2013multiobjective);
  - search scope and inventory coverage → §9 "Coverage and priority".
- content: "bearer" is defined at its first use in §1.
- content: §7 rewritten:
  - the case is framed by matched endpoints (a minimal pair) and by the two routes as the channel working vs captured (Turner's manipulation horn);
  - "two questions" (assessment = representability; objective = shared resource, choice, rigidity) organize 7.1–7.4.
  - The non-implications list was removed. Its unique items moved: `shutdown_bit_loses_relation` to 7.1, `viable_not_robust`/`robust_strengthens_viable` to §3, and "correction does not decide content" to §8. The two items that had no witness were dropped.
- content: §8 rewritten:
  - six stages, with forced edges F1–F5 (Figure 2, TikZ) and Table 4 giving each edge's kind and support;
  - "What is chosen" (floors, ranking order, growth/allocation, floors alone don't rank);
  - Table 5 of requirements by class, merging design rules and interface obligations, each tagged P/E/A.
- content: the extractor adds `floorMenu_scalar_violates` and `gate_bounds_scalar_gap`. The bib adds `greenblatt2024alignmentfaking` and `schoen2025antischeming`, verbatim from `references/external-alignment.bib`.
- bookkeeping: verification. `./papers/alignment-frames/build.sh` → "Built alignment-frames.pdf" (39 pages); `grep -c Overfull alignment-frames.log` → 0; no undefined references. No Lean changes.

## Revision (fourth request, 2026-11-06)

Trigger: the user asked to add Hallgren (taxonomy of agents) and Beard & Zarncke (lenses of agency) to §2 Taxonomies, without citing the open-problems post but aligning the evidence letters with it. No claim-type column. The user also asked for a discussion of whether the typed schema pays rent.

- content: §2 Taxonomies has a new paragraph on the two agent taxonomies. It ties memory to the record frames, theory of mind to the rewiring route, and the living-systems lens to the shared-resource class. The bib gains local entries `hallgren2026taxonomy` (eq-network PDF) and `beard2026lenses` (LessWrong).
- content: the Table 5 support tags now use the field-matrix letters from `reference/field-agendas/data/meta.yml`: T theory (finite Lean proof), D empirical (software), C conceptual. The matrix itself is not cited.
- bookkeeping: verification. `./papers/alignment-frames/build.sh` exit 0; `grep -c Overfull alignment-frames.log` → 0; no undefined references.
- Schema question: the 9-tuple's T and S fields were unused, and the bearer H clashed with the situation-class H.
- content (fifth request): applied the recommended fix.
  - §3 "Typing a frame" is prose with five names: standing, object, assessment (which absorbs the temporal and uncertainty rule), quantifiers, warrant. The solution concept was dropped, along with all tuple symbols; H now means only the situation class.
  - The intro has four questions matching the five names.
  - Each class in §6 is defined by which name its resolution changes.
  - The §8 stages are named by the same terms: (a) Standing and quantifiers … (f) Assurance = the warrant.
  - The terms are used consistently in the abstract, contributions, lens paragraph, Table 1 headers, relations, §7.1, Table 5, §9, and the conclusion.
  - Table 4's Kind column uses the T/D/C letters.
- bookkeeping: verification. `build.sh` exit 0, 39 pages, 0 overfull, 0 undefined; `lean_extracts.py --check` → "lean_extracts: up to date".
- content (sixth request): the abstract was rewritten.
  - The opener "often compared as if they were rival objective functions" was judged overbroad and uncited. It is replaced by two observable habits: mixed-type lists of approaches, and proposals added as reward terms.
  - The abstract now covers the five names, classes defined by what a resolution changes, the case and its small model, the forced and chosen orderings, and Lean calibration.
  - `build.sh` exit 0, 0 overfull, 0 undefined.

- content (ninth request): the body now matches the abstract's terminology.
  - "weights/weighting/weighted scalar" → "exchange rates", "fixed-rate sum"; "penalty weight" → "penalty coefficient"; "menu" → "choice set" ("option set" is already an object type). This covers §2, §3, Table 1, the relations, §6, Table 2, §7, §8 (including Tables 4 and 5), §9 and the appendix intro.
  - The appendix notes that the Lean code says weights and menu.
  - The extractor glosses were updated.
  - `render_figure.sh` relabels "Weighted scalar" and its two edges at render time; the shared DOT source is unchanged.
  - Lean names are unchanged.
- bookkeeping: verification. `build.sh` exit 0, 0 overfull, 0 undefined; `lean_extracts.py --check` up to date; the figure PDF text contains "Fixed-rate sum" and not "Weighted".

- content (tenth request): retitled.
  - Title: *Combining Alignment Criteria: Four Kinds of Conflict and the Design Order They Force*, with the PDF metadata updated.
  - §3 is now headed "What does alignment secure?".
  - §1 defines "frame" and states the combination question; there are now five contributions, with §8 as the destination.
  - Abstract: "by what a combination needs".
  - §6: classes read constructively, and Table 2's column is now "Combine when".
  - §8 is titled "Combining frames".
  - §9 has a new "Necessary, not sufficient" paragraph.
  - The conclusion ends on the partly forced design order.
  - "crosswalk" was removed as a self-description.
  - `papers/README.md` title and paragraph updated.
- bookkeeping: verification. `build.sh` exit 0, 0 overfull, 0 undefined; PDF metadata title confirmed; abstract 247 words.

- content (eleventh request):
  - §1: the opener gains a bridge sentence ("To combine them, a proposal has to say what each one answers."), and "The same error appears…" became "More formal frames differ in the same way."
  - Contributions 1 and 2 were merged, so there are now four.
  - The Figure 1 caption now describes the green edges as one correction-first way of combining frames (checked against the DOT green edges) and points to the chosen orderings of §8.
  - `build.sh` exit 0, 0 overfull, 0 undefined.

- content (twelfth request, 2026-11-06): the term is now "criterion" throughout.
  - Every word-form "frame/frames" in the paper text became "criterion/criteria". §1 defines a criterion broadly, as anything a proposal requires or offers about a system: target, constraint, guarantee or protocol. Lean module names are unchanged.
  - §2 Taxonomies was rewritten around a new table (`tab:taxonomies`) of how each taxonomy or lens uses criteria, explicitly or implicitly, and which part of the typing it fixes. It is followed by four short groups: sources of standards, target taxonomies, maps of proposals and failures, and agent lenses.
- bookkeeping: renamed `papers/alignment-frames/` → `papers/alignment-criteria/`, with the files `alignment-criteria.{tex,bib,pdf}` and `figures/criteria-relations.pdf`.
  - `build.sh`, `render_figure.sh`, `lean_extracts.py` and the appendix path were updated, and the stale old-named build outputs deleted.
  - The shared `drafts/alignment-frames-relations.{dot,md}` keep their names (the site and the Lean graph check use them).
  - Links updated in `papers/README.md`, `drafts/attic/README.md`, `drafts/alignment-frames-relations.md`, `metadata/TODO.md`, `drafts/plans/construct/construct.md`, HANDOFF and review §0.
  - Removed the now-stale `construct.md` line from `scripts/markdown-link-baseline.txt`; this session had edited that source line, which made the baseline line block.
- bookkeeping: verification.
  - `./papers/alignment-criteria/build.sh` → "Built alignment-criteria.pdf"; 0 overfull, 0 undefined.
  - `lean_extracts.py --check` → up to date.
  - `scripts/check_markdown_links.py` → 6 blocking. Five are links to the untracked `papers/alignment-criteria/` (they clear when it is committed). One is another session's untracked `drafts/outreach/kosoy-alignment-problem-lw-comment.md`.

- content (thirteenth request): the taxonomy table moved from §2.1 to a new §3 subsection, "Where existing taxonomies sit" (`sec:taxonomies-placed`), and §3 now lists four places the typing is used.
  - §2.1 is trimmed to about 300 words: the explicit/implicit observation plus four comparisons used later (Baum, Jha, Hallgren, the lenses).
  - The cells were checked against the sources by a subagent; the result is a single read, not independent confirmation.
  - Fixed: Baum (three dimensions plus a graded degree), Jha (ideals fix what is aligned and to what; positive/negative alignment), Harris (seven distinct subproblems; the old "dependencies" claim was unconfirmed and dropped, also in §2.1), Beard & Zarncke (no "power" or "legitimacy").
  - Sharpened: Gabriel (fairness protocol), Zhi-Xuan (contractualist protocol; rejects a single EU ordering), Hubinger (competitiveness outside the typing), Krakovna (a chain of specifications), Ji (intermediate objectives; backward = assures and governs), Amodei (the paper's own three groups), Hallgren (against model complexity).
  - The patterns paragraph was rewritten so it no longer contradicts Baum's row. The Jha bib entry gained arXiv 2606.14315.
  - Harris resolved (fifteenth request): the author downloaded the AIES PDF, an image-only browser print. I read pp. 1223–1228, 1230 (their Table 1) and 1231 as page images.
    - They say the subproblems are distinct ("a solution to one subproblem does not solve the other subproblems") and not exhaustive, so the dropped "dependencies" claim was indeed wrong.
    - Row rewritten: diagnostic question, failure and solutions per subproblem; maps to standing, referent, assessment, bearers, quantifiers and warrant, not the object.
    - Added to §2.1 their point that solutions get "misconstrued … as rival candidates" when aimed at different subproblems (p. 1228), and to the patterns paragraph.
    - Added to §7 that their subproblem 6, inverse alignment ("Does the system reshape human values?"), is the general case of the rewiring route.
    - `build.sh` exit 0, 0 overfull, 0 undefined.
  - `ji2025survey` resolved (fourteenth request). Crossref `api.crossref.org/works/10.1145/3770749` gives "AI Alignment: A Contemporary Survey", ACM Computing Surveys 58(5), pp. 1–38, online 2025-11-21. The bib entry had `pages = {132}` (unverified, possibly an article number); it now says 1--38 and notes the arXiv preprint title.
  - The Crossref abstract calls RICE "the key objectives" and backward alignment "gain evidence … and govern", so the cell now follows the published abstract instead of the arXiv body ("intermediate objectives").
  - The author pasted the ACM page, which shows "Article No.: 132, Pages 1 - 38" and the same abstract wording. `eid = {132}` was added.
- bookkeeping: verification. `build.sh` exit 0, 0 overfull, 0 undefined.

- content (sixteenth request): Harris et al. are now cited where they overlap.
  - §1: the parallel "rival candidates" point.
  - The bearer definition: anthropocentrism, with Gabriel.
  - §2.1 positioning: "They type the problem; we type the criteria … and classify the conflicts".
  - "Warrant is not property": their provability challenge.
  - §6 choice conflict: their prioritizing subproblem, plus our addition that a fixed exchange rate is not an available answer once one criterion is a floor.
  - §8 "Which criteria are floors": their argument that parts of alignment are normative.
  - Nothing of ours was removed: no section is made obsolete (see chat).
  - `build.sh` exit 0, 0 overfull, 0 undefined.

- content (seventeenth request, 2026-11-06):
  - Lean: no change needed. My side finding was wrong: `FrameCorrector.lean` declares `namespace FrameRelations`, so the docstring's `FrameRelations.blind_constraint_cannot_separate` is correct.
  - Paper bib: 14 entries checked by a subagent against Crossref, arXiv, NeurIPS, PMLR, OpenReview, FHI and the repo (a single read; DBLP was blocked). No wrong authors or titles were found.
    - Added: pages (Abel, Bacchus, Toro Icarte, Ouyang), DOIs (Hammond, Jiang, Lim, Han), "Grove, Adam J.", PMLR volume and URL, Ouyang's full author list, Shah "LessWrong / AI Alignment Forum".
    - Lightman et al. upgraded to ICLR 2024.
    - DeepSeek kept as the arXiv report; the Nature 2025 version has a different title.
  - Book: `kasirzadeh2024beyondpreferences` (wrong author, Atoosa Kasirzadeh) renamed to `zhixuan2025beyondpreferences` (Zhi-Xuan, Carroll, Franklin, Ashton). Changed in `references/philosophy.bib`, `references/bibliography-summaries.tex` and `chapters/ch04-fixed-values-wrong-target.tex` (2 cites). `site/astro.config.mjs` got a redirect from the old reference-card URL, and the paper bib now copies the main entry verbatim.
  - Tooling: `scripts/check_citations.py` and `scripts/generate_global_nocite.py` now skip `.worktrees/`. They had scanned the local `.worktrees/v1-inspect` checkout, whose ch04 still cites the old key.
  - Terminology outside the paper:
    - `drafts/alignment-frames-relations.{md,dot}`, `-b/-c/-x.dot`, `alignment-frames-by-object-and-measure.md` (8-tuple → the paper's five names), `alignment-frames-turner-comparison.md` and `state-utility-in-practice.md`: frame→criterion, weights→exchange rates, menu→choice set. Excluded: inline code, Lean names, paths, Graphviz `weight=`, Turner's "weightings", quantilizer base masses, and "frame" meaning the shared decision-problem form.
    - The DOT label is "Fixed-rate sum (fixed exchange rates)", so the relabel `sed` was removed from `render_figure.sh`.
    - Draft SVGs regenerated (`render_alignment_frames_x.py` for a and x; `dot` for b and c).
    - File names unchanged (the site and the Lean check read them).
  - Site, terminology only:
    - `lenses-data.mjs`: the weighted-scalar card is titled "Fixed-rate sum" (slug kept), plus three bodies and one paraphrased quote. Quotes from the attic spinout draft were left verbatim.
    - `sync-lenses.mjs` overview text: criteria, object and assessment, the paper's four clusters, and the green edges as one correction-first reading.
    - `FieldLensGraph.astro` / `FieldPreviewHub.astro`: "Criteria map", "Alignment criteria".
    - Ran `sync:lens-graph`, `sync:lenses` (5 cards written), `sync:reference-cards`, `sync:chapters` and `generate:card-redirects`.
- bookkeeping: verification.
  - `check_frame_graph.py` → "Frame graph check passed (19 compose, 9 incompatible, 18 morphism …)".
  - `check_bibliography_summaries.py` → "passed (574 summaries for 574 bib keys)".
  - `check_citations.py` → "Citation check passed (516 keys cited, 718 keys in bib)".
  - Paper `build.sh` exit 0, 0 overfull, 0 undefined.
  - `make check` otherwise fails only on the 6 known untracked-file markdown links.
  - Book `./build.sh` → exit 0, "Built dist/pdf/towards-superintelligence-alignment.pdf" (1565 pages). A PyMuPDF text scan finds "Zhi-Xuan" on pp. 104, 119, 122, 1242, 1519, 1564 and "Kasirzadeh" on 0 pages.

- bookkeeping (eighteenth request): deleted `drafts/alignment-frames-turner-comparison.md` (superseded by the paper §§2, 3, 7). Its inbound links in the relations note, the state-utility note and the turner-soares plan, plus the `FrameDecision.lean` module docstring, now point to the paper. `lake build AlignmentProofSpine.FrameDecision` → "Build completed successfully (938 jobs)." Fixed the plan's broken draft-to-draft link to `state-utility-in-practice.md`.

- content (twentieth request): follow-up plan [`drafts/plans/construct/correction-under-embedding.md`](../plans/construct/correction-under-embedding.md). It covers the convergence limits (A1–A4) and the embedded, user-modelling and adversarial case. The core is "outside the system" restated as cut conditions O1–O5, with a map from each finite result to the conditions it needs; Lean items L1–L3 and E1–E6; logical induction only for bounded O2 and reflection, as a flagged analogy. Kill criterion in the file. v2 checklist item and Related link in `construct.md`; index link in `drafts/plans/README.md`. Lean names in the file checked by grep against `formal/AlignmentProofSpine/`; bib keys checked against `references/*.bib`.
- content (twenty-second request): 2.0 phase P-LI, [`drafts/plans/construct/logical-induction-phase.md`](../plans/construct/logical-induction-phase.md). Where logical induction enters; reified bets as an economic O2; no static outside (settlement race, weakest link); LMSR derivations (manipulation loss = b·KL, decision markets with importance-weighted exploration, audit lottery, combinatorial subsidy); ways-out table; Lean M1–M11 proposed, not implemented. Phase row and checklist item in `construct.md`; pointer from `correction-under-embedding.md`; plans index. Seven market references checked by web search (pages listed in the file); the rest marked "from memory, verify".

## Decisions

- One discriminating case, not a running example; a full worked deployment would add detail but no separations.
- Follow-up: logical induction is a later step, not part of the first follow-up (author, 2026-11-09).
- Figure uses graph **a** unchanged; the caption marks the green edges as one (correction-first) composition reading. A neutral variant without green edges was not made.

## Open / next

- Push: not pushed. The Lean appendix links in the paper pin `778ac42f26`, and the site's lens-card pins point at local commits; they resolve on GitHub once pushed.
- Bib: the 14 paper entries are checked; moving local entries into `references/` still needs `\bibsummary` lines.
- Terminology: drafts and site adapted (seventeenth request). File names `drafts/alignment-frames-*`, Lean `Frame*` modules and lens-card slugs (`weighted-scalar`) keep the old words.
- Offered, not decided: a hedge that the four classes are not shown exhaustive (candidate fifth: a warrant conflict, F3′); the choice-set vs carrier `C` clash.
- Not for this paper: the instrumental-convergence limits and the embedded case go to a follow-up; plan in `drafts/plans/construct/correction-under-embedding.md` (author decisions listed there, § G).
- Book plan: the `metadata/TODO.md` Frame-of-the-target item still says TSA is the running example (book 2.0, not the paper).

## Key paths

- `drafts/project/alignment-frames-paper-review-2026-11-05.md`
- `papers/alignment-criteria/alignment-criteria.tex`

## Commits

- `778ac42f26` Point the FrameDecision docstring at the alignment-criteria paper.
- `fe9220df35` Add the alignment-criteria paper (Combining Alignment Criteria).
- `e3bd766726` Adopt the paper's criteria terminology in the frame drafts; drop the Turner draft.
- `1f5feb32b2` Fix the misattributed Beyond Preferences citation (ch04).
- `83b57d5d9d` Skip .worktrees/ in the citation check and global-nocite generator.
- `ef7159347b` Match the site's criteria map and lens cards to the paper's terminology.
- This log, HANDOFF and INDEX: the commit after these.
