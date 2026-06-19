# Project TODO

Cross-cutting manuscript and tooling tasks. **Chapter-local work stays in the `.tex` file** (or `drafts/chapter-notes/` for deferred material).

Run `make todos` to list all inline `[STUB]`, `TODO`, and `FIXME` markers in the repo.

---

## Where TODOs live

| Kind | Location | When to use |
|------|----------|-------------|
| **Draft placeholder** | `[STUB]` in chapter `.tex` | Section not yet written; removed when chapter is drafted. |
| **Per-chapter cite seeds** | `% TODO(deep-research):` in stub `Chapter References` | Primary BibTeX keys to wire when *that* chapter is drafted. See `metadata/source-canon.md`. |
| **Per-chapter citation gap** | `% TODO[citation]:` in chapter `.tex` | One missing cite for a specific chapter (e.g. ch05 Turchin map, ch33 acausal trade). |
| **Per-chapter formalization** | `% TODO[formalize]:` / `% TODO[empirical-test]:` in chapter `.tex` | Math or test design owned by that chapter. |
| **Chapter-specific open crux** | `% TODO[open-crux]:` in chapter `.tex` | Philosophical or scope crux tied to one chapter (e.g. ch40 delegation). |
| **Research directions** | `metadata/open-problems.md` | Unresolved *research* questions, not editorial chores. |
| **Tracked uncertainties** | `metadata/uncertainty-ledger.md` | Book-level open uncertainties (numbered list). |
| **Cross-cutting chores** | *this file* | Work spanning chapters, build, structure, or citation passes. |
| **Deferred chapter drafts** | `drafts/chapter-notes/*.tex` | Superseded or split chapter material; local TODOs stay there until merged or deleted. |
| **Session handoff** | `drafts/conversation-summaries/` | Historical context only—not an active task list. |

---

## Manuscript (cross-cutting)

- [ ] **Complete citation review** — in-body `\autocite`/`\cite` coverage, missing BibTeX keys, `context/lw-references.md` crosswalk, chapter reference blocks. Part III ch12/ch13 known thin; deferred pending this pass.
- [ ] **§10 structure pass** — drafted chapters missing standard `\section{Summary}` bullets: ch12 (`\section*{Chapter summary}`), ch13 (prose + separate `Chapter Claims`). Optional: add WWCTV to ch01 if missing.
- [ ] **Claims / assumptions ledgers** — when drafting chapters, add major claims to `metadata/claims-ledger.md` and assumptions to `metadata/assumptions-ledger.md` (see `review/claim-checklist.md`).
- [ ] **ch05 partial draft** — complete scope/failure-coverage chapter; local `TODO[citation]` for Turchin AGI failure-mode map remains in `ch05-assumptions-scope-failure-coverage.tex`.

---

## Formalization tracks

Canonical home is the chapter that *owns* the object; other chapters should reference, not duplicate, inline TODOs.

| Track | Canonical chapter | Also referenced in |
|-------|-------------------|-------------------|
| Define $\mathrm{ICI}_{ij}$ (inferential coupling index) | ch33 | ch40 open-problem ledger |
| Coalition-collapse empirical tests | ch33 | ch40 |
| Pivotal process $\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}$ conditions | ch35 | ch40 |
| Transparency ↔ $\kappa_{ij}$ ↔ correction observability | ch33 only | — |
| ch40 open cruxes (reflective stability of correction; delegating superhuman plan evaluation) | ch40 only | `metadata/uncertainty-ledger.md` items 7–8 |

### Lean proof spine (`formal/`)

**Current state:** toy / separation proofs. Many results are finite `Bool` counterexamples, definitional restatements, or predicates over abstract `axiom` carriers. The spine checks the *logical shape* of the argument; it does not yet match full book information-theoretic definitions (CMI blankets, CCI penalties, bearer maps on world states, etc.).

- [ ] **Strengthen proof spine** — replace toy counterexamples with constructive finite models tied to bundle/bearer geometry; replace definitional theorems with non-trivial lemmas; tighten bridges (probabilistic `MB1`, qualified `MB7`).
- [ ] **Derive full certification chain** — ~~link BIQ ceiling (`P10`) to control via `Control_le_IctrlSys` / `BIQDerivedCapacitySlack`~~ *(done)*; ~~tie `CorrectionCapacity` to weakest-link graph capacity (`P24` / `CorrectionLinkCapacities`)~~ *(done: `CorrectionCapacity = ChainCapacity`, `WeakestLinkDerivedCapacitySlack`)*; extend with adversarial aliasing (`P34`/`MB7`), and safety-case support (`P40`). ~~Propagate bounds along successor-safe chains (`P27`/`SuccessorSafeChain`).~~ *(done)*
- [ ] **Wire spine into manuscript** — Ch. 39 safety case / appendix cites each theorem as *proof*, *counterexample*, or *bridge* per `formal/README.md`.

---

## Build / tooling

- [ ] Resolve duplicate LaTeX labels: `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.

---

## Leave local (do not centralize here)

- All `% TODO(deep-research):` blocks in stub chapters ch15–ch44 (and ch05) — per-chapter cite wiring on draft.
- All `[STUB]` section placeholders until each chapter is integrated.
- `frontmatter/dedication.tex` `[STUB]`.
- Appendix `[STUB]` markers in `appendices/app*.tex`.
- `drafts/chapter-notes/ch33-cooperation-percolation-deferred.tex` and sibling deferred notes.
