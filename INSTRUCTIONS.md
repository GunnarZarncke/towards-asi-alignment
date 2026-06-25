# Instructions for Writing and Maintaining the Book

*Towards Superintelligence Alignment: Boundaries, Values, and Correction*

**Role of this file:** Mission, audience, source canon, and editorial rules. 

| Need | Canonical home |
|------|----------------|
| Chapter list, status, word targets | `metadata/book.yml` |
| Build, layout, agent handoff | `AGENTS.md` |
| Reader-facing status and quick start | `README.md` |
| Symbol index (generated) and §C reconciliation | `metadata/notation.md` → Appendix A |
| Assumptions index (generated) | `metadata/assumptions-ledger.md` → Appendix E |
| Operational terms | `metadata/terminology.md` → Appendix F |
| Source PDFs, TeX paths, extracts | `metadata/source-canon.md` |
| Continuity and deduplication plans | `review/fix-plans-2026-06-22.md` |
| Lean predicates and bridges | `formal/README.md`, Appendix I |

---

## 0. Mission

Write a full book-length manuscript titled **Towards Superintelligence Alignment: Boundaries, Values, and Correction**.

The book must be self-contained. It must not assume the reader already knows the author's previous project names, papers, conversations, or internal terminology. Concepts originating in prior work may be cited in chapter references, but the body text must introduce them from first principles. Other authors' related work must be explained sufficiently for the intended audience to follow, including key formulas where needed (derivations optional).

**Central thesis:**

> Superintelligence alignment is the problem of preserving human-correctable value-bearing processes across capability growth, ontology shift, successor creation, and strategic multi-agent selection pressure, under the assumption that civilization still has enough correction capacity to participate in the process.

**Organizing frame:**

\[
\text{superintelligence alignment}
=
\text{value-bundle transport}
+
\text{bearer persistence}
+
\text{correction-channel integrity}
+
\text{successor stability}
+
\text{socio-technical attractor control}.
\]

Do not let external doom arguments (Yudkowsky-style lethalities, Turchin-style failure maps, or general AGI catastrophe taxonomies) become a second organizing ontology. Use them only as adversarial checklists or coverage audits late in the manuscript (especially Chapter 40).

The book must explain the thesis at three levels:

1. **Plain-language overview** for capable generalists, funders, engineers, and policy-adjacent readers.
2. **Conceptual theory** of agents, values, boundaries, correction channels, successors, and attractor basins.
3. **Formal treatment** using information theory, dynamical systems, causal channels, value-bundle geometry, and safety-case logic.

Use the voice and calibration in `context/writing-style-gunnar.md`. See `AGENTS.md` for agent behavior, Lean spine review, and session logging.

---

## 1. Intended Audience

Write for four overlapping audiences:

1. **AI alignment researchers** who need a precise technical framework.
2. **AI safety engineers and eval builders** who need operational artifacts.
3. **Funders and policy-adjacent decisionmakers** who need to know what decisions change.
4. **Capable generalists** who need a self-contained conceptual map.

The book must not depend on the reader accepting unusual ontology. Every central term must either be operationally defined or translated into simpler language.

When introducing a technical term, ask:

* What decision does this term enable?
* What measurement does it make possible?
* What failure mode does it clarify?
* What would be lost if we used ordinary language instead?

If the term does not earn its keep, simplify it.

---

## 2. Writing Style

See `context/writing-style-gunnar.md`.

Prefer short declarative sentences for core claims. Use longer, qualified sentences when handling uncertainty, counterexamples, or formal dependencies.

Use examples and counterexamples as stress tests, not decoration.

Avoid hype and culture-war framing.

**Legibility-first constraints** (`context/legible-alignment-messageing.md`): in introductions, summaries, chapter openings, and policy-facing sections, make clear what could go wrong, why it matters before deployment, what observable artifacts would reduce risk, what decision changes if the claim is true, and where the argument is weak.

---

## 3. Source Canon

Do not assume the reader knows internal sources. Introduce every concept independently in the manuscript.

**Durable reference data:**

* **`metadata/source-canon.md`** — book-local PDFs, `context/extracts/` markdown, sibling-repo TeX/PDF paths.
* **`context/lw-references.md`** — chapter-indexed LessWrong and external alignment posts (manual promotion to `.bib`; see §7).

PDF extracts live under `context/extracts/` (regenerate with `python3 scripts/extract_pdf_to_md.py`). Prefer extracts for agent reading; verify formulas against TeX or PDF when stakes are high.

**Thematic clusters** (detail and file paths in `source-canon.md`):

* agent-boundary discovery and access (UAD tradition),
* predictive-compression intentionality,
* value bundles, bearer maps, loop-hub / free-energy value models,
* capability as boundary information (BIQ tradition),
* attractor basins, cooperation, parasites, selection,
* metacognition, self-opacity, construction without understanding,
* Alignment Attractor / artifact conductivity framing.

The body must not use project acronyms as explanatory shortcuts (e.g. "As UAD says…"). Cite traditions in chapter references; define objects in prose.

Do not include the BITS or affective-module approach in the main line unless explicitly requested.

---

## 4. Structural Consolidation (editorial)

These rules are fixed; do not re-open them when drafting:

* No separate chapters for AI–AI war, blackmail-only chapters, paternalism-only chapters, or general bug/virus taxonomies as book structure.
* Turchin-style failure maps: **coverage audit in Chapter 5 only**, not a second ontology.
* Yudkowsky lethalities: **stress-test checklist in Chapter 40 only**.
* Cooperation, privacy, opacity, and percolation: **subsections of Chapter 33**, not standalone chapters.
* Former standalone topics deferred to `drafts/chapter-notes/*-deferred.tex` (reference only).

When a formal object is re-used in a later chapter, follow `review/fix-plans-2026-06-22.md` §A: one **home** chapter with full definition and `\label`; elsewhere use **reminder**, **simple-reference**, or **elide**—do not re-derive.

---

## 5. Terminology, Notation, and Formal Spine

**Do not duplicate definitions in this file.** Maintain a single canonical surface per layer:

| Layer | Maintain in | Reader sees |
|-------|-------------|-------------|
| Operational terms | `metadata/terminology.md` | Appendix F (glossary) |
| Symbols and canonical eq homes | `metadata/notation.md` | Appendix A (generated index; points to chapters) |
| Formal predicates and bridges | `formal/AlignmentProofSpine/*.lean` | Appendix I |

Edit `metadata/assumptions-ledger.md` only; run `./build.sh` to refresh Appendix E. Edit `metadata/notation.md` only for Appendix A.

**Capability** is \(K\); **value bundle** is \(B\). **Correction capacity** is \(C_{\text{raw}}\); **correction-channel integrity** is \(\mathrm{CCI}\)—never interchange them. **Fitness** is handle-based deployment mass in Chapter 32, not revenue or benchmark score as primitive terms.

Calibrate manuscript claims to Lean status: **proof**, **counterexample**, or **bridge** (`AGENTS.md`). Do not write that Lean proves ASI alignment.

---

## 6. Chapter Requirements

Every chapter must include:

1. `\chapter{...}` + `\label{ch:...}`.
2. A `chapterthesis` environment (one paragraph core claim).
3. Decision relevance early—why the chapter matters for alignment work.
4. At least one **failure mode / counterexample**.
5. **`\section{What Would Change This View}`** — skimmable disconfirmers for *this chapter's* central claim (exact title for consistency).
6. A summary (roughly 5–8 bullets or equivalent).
7. BibLaTeX citations; per-chapter `refsection` + `\printbibliography[heading=subbibliography,title={Chapter References}]`.

**Shape A (new stub):** optional scaffold sections (Why This Matters, Plain-Language Model, Formal Model, Worked Example, …).

**Shape B (integrated draft):** keep native narrative structure; do not force Shape A splits. Still satisfy all required elements above.

Before finishing chapter integration, review the matching Lean module per `AGENTS.md` and record prose–spine gaps in the session log or `metadata/TODO.md`.

---

## 7. References and Citations

Use BibLaTeX with `biber`. Category files under `references/` are loaded from `book.tex`. `references/manuscript-citations.bib` holds cited keys not yet merged into categories. The global bibliography is built via `metadata/global-nocite.tex` (generated by `scripts/generate_global_nocite.py` at build time).

Refresh category bibs from sibling repos when available:

```bash
python3 scripts/import_source_map_refs.py
```

Promote LessWrong and forum posts from `context/lw-references.md` manually into the appropriate `references/*.bib` file.

**Citation policy:** body text explains concepts in plain language; chapter references may cite internal project sources. Never use internal project names as unexplained primitives in the body.

Each chapter should draw from at least three reference categories where relevant: alignment/agent foundations, information theory or dynamical systems, and values/neuroscience/philosophy/governance.

---

## 8. Ledgers

Track major claims, assumptions, and open problems in:

* `metadata/claims-ledger.md`
* `metadata/assumptions-ledger.md`
* `metadata/uncertainty-ledger.md`
* `metadata/open-problems.md` (research directions; overlaps Appendix H)

Update ledgers when a chapter adds or changes a load-bearing claim. Mark status: established, plausible, speculative, or open.

---

## 9. Conceptual Spine

The manuscript should maintain this progression (details live in the drafted chapters):

1. We may be aligning the wrong object.
2. The real object may be a composite optimizer.
3. Operational agent-boundary discovery is required.
4. Capability is information flow through boundaries.
5. Capability growth changes boundaries.
6. Human values are compressed value bundles, not fixed utilities.
7. Alignment requires transporting bundle geometry, bearer maps, and correction processes.
8. Goal inference must become bundle and bearer inference.
9. Correction is a causal channel, not obedience.
10. Strong correction resembles an extrapolative civilizational update process.
11. Successor creation is the central alignment test.
12. Better self-modeling can worsen self-transparency.
13. Local alignment can be destroyed by socio-technical selection pressure.
14. Adversarial measurement is needed at frontier capability.
15. Technical systems can preserve conditions for legitimate value change but cannot fully decide what legitimate change is.
16. Society must govern value-bundle change and bearer persistence through transformation, or change will occur unconsciously through markets and technology.

---

## 10. Things to Avoid

Do not write as if:

* "alignment" means only obedience,
* "human values" means a utility function,
* "agent" means a person-like mind,
* "AI system" means only model weights,
* "transparency" is always good or "privacy" always bad,
* "capability" is just benchmark performance,
* "successor" means only explicit self-replication,
* CEV is a final utility target rather than a correction process,
* technical alignment solves all civilizational questions,
* external doom maps define the book's chapter structure.

---

## 11. Chapter Writing Process

For each new or revised chapter:

1. Read `metadata/book.yml` entry and dependent prior chapters.
2. Outline concepts that must be introduced before use.
3. Draft plain language, then formalism where needed.
4. Review Lean spine module (`formal/README.md`); calibrate claim strength.
5. Add worked example and counterexample.
6. Add `\section{What Would Change This View}`.
7. Add references; update ledgers if load-bearing.
8. Run `./build.sh` and `make check`.

See `AGENTS.md` for session logs, git rules, and surgical-edit constraints.

---

## 12. Acceptance Criteria

**Chapter:** readable by a smart non-specialist; introduces concepts before use; includes formal object, example, failure mode, weakest link, references; compiles; no unexplained internal project jargon.

**Whole book:** all chapters compile; executive overview and introduction discharge front-matter promises; glossary and notation appendices populated; ledgers and bibliography support technical review; safety-case and closing synthesis chapters complete; established vs plausible vs open claims are marked; `./build.sh` succeeds from a clean checkout.

Status and remaining gaps: `metadata/book.yml`, `metadata/TODO.md`, `README.md`.

---

## 13. Review Passes (when requested)

1. **Technical** — equations, definitions, assumptions, references, Lean spine alignment.
2. **Legibility** — non-specialist can see what could go wrong, why it matters, what to measure, what to do next.
3. **Adversarial** — strongest objections, duplicate derivations, glossary/notation drift, claim strength vs evidence.

Use `review/reviewer-guide.md` and `review/_pass/` notes for structured continuity review.
