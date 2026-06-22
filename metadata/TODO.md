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
- [ ] **§10 structure pass** — chapter-ending headings normalized to `\section{Summary}` (2026-06-22). Remaining: ch12 and ch42 still carry **both** a `Conclusion` and a `Chapter summary` (merge into one Summary); ch23 has a front `Chapter Summary` + tail `Chapter Conclusion` (drop/condense the front, rename the tail). See `review/fix-plans-2026-06-22.md` §B12.
- [ ] **Claims / assumptions ledgers** — when drafting chapters, add major claims to `metadata/claims-ledger.md` and assumptions to `metadata/assumptions-ledger.md` (see `review/claim-checklist.md`).
- [ ] **ch05 partial draft** — complete scope/failure-coverage chapter to manuscript depth: add a failure-mode section and a `What Would Change This View` section, resolve inline `[Defined]` markers (L56, L109–111), and deliver the `TODO[citation]` Turchin AGI failure-mode map citation in `ch05-assumptions-scope-failure-coverage.tex`.
- [ ] **ch40 flesh-out** — `ch40-lethality-stress-test-open-issues.tex` is ~1,500 words vs a 9,000 target: add per-lethality prose to the 13-row checklist (each cell is currently a single phrase), resolve the two `% TODO[open-crux]` markers (L119, L121; reflective stability of correction; delegating superhuman plan evaluation — mirror `metadata/uncertainty-ledger.md` items 7–8), and add a forward bridge to ch41.
- [ ] **Frontmatter gaps** — write the stub front-matter and finish the executive overview: `frontmatter/preface.tex`, `frontmatter/dedication.tex`, `frontmatter/acknowledgements.tex` (all `[STUB]`), and the three `[STUB]` blocks in `frontmatter/executive-overview.tex` (Diagram in Words L27, Assumptions L32–34, What This Book Tries to Establish L58).
- [ ] **Opening-promise reconciliation** — when ch44 (conclusion) and ch39 (safety case) are written, **explicitly discharge or explicitly soften** each opening promise: the Introduction's five `introclaim`s (boundary, value-bundle, correction, successor, basin), its six "What Counts as Progress" artifacts, its six-point "Practical Hope" regime, and the Executive Overview's five preservation problems. Any promise the finished chapters cannot back must be weakened in `frontmatter/introduction.tex` / `executive-overview.tex` rather than left dangling. Payability analysis (claims 1–4 already backed; claim 5 needs ch33; safety-case + synthesis are the gaps) is in `review/fix-plans-2026-06-22.md` §D.
- [ ] **Notation reconciliation** — apply the cross-chapter symbol/formula resolutions in `review/fix-plans-2026-06-22.md` §C, then record canonical forms in `appendices/appA-notation.tex`, `metadata/notation.md`, and INSTRUCTIONS §18 (keep all three in sync). Key decisions: capability functional `B→K`; `G_B` = ch19 4-tuple; CCI penalty set (Goodhart out); `U_H` operator + 5-tuple `V_t`; parasite criterion = ch10 form; `κ` = cooperativity only, artifact conductivity = `χ`; ΔL log-evidence convention.

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

**Scope (for critics).** Bridges `MB1`–`MB8` and any step that requires substantial empirical
work (estimator soundness, identifiability under sampling, institutional basin stability,
adversarial robustness in the wild, CEV convergence evidence, etc.) are **intentionally
out of scope** for both the book’s proof obligations and Lean. Lean checks the logical
shape *if* those bridges are granted. The items below are **in scope**: places where a
**drafted chapter already defines formal objects** but Lean still uses integer proxies,
axiom lists, `Bool` toys, or definitional stubs instead of that chapter’s structure.

**Current state:** toy / separation proofs. Many results are finite `Bool` counterexamples,
definitional restatements, or predicates over abstract `axiom` carriers. The spine checks
the *logical shape* of the argument; it does not yet match full book information-theoretic
definitions (CMI blankets, CCI penalties, bearer maps on world states, etc.).

- [ ] **Strengthen proof spine** — replace toy counterexamples with constructive finite models tied to bundle/bearer geometry; replace definitional theorems with non-trivial lemmas; tighten bridges (probabilistic `MB1`, qualified `MB7`) *only where the book supplies a formal definition, not where the step is empirical*.
- [ ] **Derive full certification chain** — ~~link BIQ ceiling (`P10`) to control via `Control_le_IctrlSys` / `BIQDerivedCapacitySlack`~~ *(done)*; ~~tie `CorrectionCapacity` to weakest-link graph capacity (`P24` / `CorrectionLinkCapacities`)~~ *(done)*; extend with adversarial aliasing (`P34`/`MB7` structural layer), and safety-case support (`P40`). ~~Propagate bounds along successor-safe chains (`P27`/`SuccessorSafeChain`).~~ *(done)*
- [ ] **Wire spine into manuscript** — Ch. 39 safety case / appendix cites each theorem as *proof*, *counterexample*, or *bridge* per `formal/README.md`.

#### Chapter ↔ Lean mapping gaps (**drafted chapters only**)

| Critic gap | Draft chapter(s) | Lean module / nodes | TODO |
|------------|------------------|---------------------|------|
| `CorrectionLinkCapacities` is a free `List Int`, not the ch24 causal chain `W→O→J→D→C→U→A` | **ch24**, **ch25** | `Correction.lean` (`P23`, `P24`) | Typed correction path (nodes + edges) aligned with `\eq{correction-raw-capacity}` / `\eq{correction-bottleneck-capacity}`; derive link list from `Edge`/`Reachable` or a structured `CorrectionPath` record, not a bare axiom list. |
| Only raw `min` capacity; no CCI penalties `L,M,R,Ω` from ch25 | **ch25** | `Correction.lean` | Add `EffectiveCorrectionCapacity` (or `CCI`) = weakest-link raw capacity minus penalty terms; keep measurement of penalties as bridges, but match chapter **definition** in Lean. |
| Slack certificates (`BIQDerivedCapacitySlack`, `WeakestLinkDerivedCapacitySlack`) are not tied to chapter measurands | **ch11**, **ch13**, **ch25** | `Capability.lean`, `Certification.lean` | Map book symbols (`C_act`, `C_corr`, coordination loss, `\eq{correction-channel-capacity}`) to certificate fields; prose should name the same fields Lean certifies. |
| `Control` vs `I_ctrl` / BIQ profile linkage is axiom-only | **ch11**, **ch12** | `Capability.lean` (`P10`, `Control_le_IctrlSys`) | Replace bare `Control_le_IctrlSys` with a chapter-aligned definition of `Control` from blanket IO / B-IQ terms (still integer proxy OK if notation matches ch11–12). |
| `P12` coordination bottleneck is one line of `omega`; ch13 has richer structure | **ch13** | `Capability.lean` (`P12`) | Formalize effective vs raw capability and coordination loss as in ch13; connect to risk/cooperativity narrative. |
| Boundary / ε-blanket in ch07 not aligned with `Boundary`/`BoundaryCondition` scaffolding | **ch07** | `Core.lean`, `Boundaries.lean` (`P05`–`P09`) | Align `EpsilonBoundary`, leakage proxy, and blanket predicates with ch07 notation; separate **definition** from `MB1` estimator soundness. |
| ch23 transport hierarchy vs abstract `SemanticTransport`/`FullTransport` axioms | **ch23** | `Bundles.lean` (`P22a`, `P22b`) | Define transport predicates from ch23’s semantic / bundle / bearer / correction layers; keep separations (`P22b`) off `Bool` toys where possible. |
| Bundle/bearer/tradeoff separations are `Bool` toys vs ch15–19 geometry | **ch15**–**ch19**, **ch22** | `Bundles.lean` (`P15`, `P17`, `P18`, `P22b`) | Finite models using bundle codes, bearer maps, or tradeoff vectors from ch16–19—not `ToySameMarginals := True`. |
| `P25`/`P26` obedience vs update-operator toys vs ch26 extrapolative correction | **ch26** | `Correction.lean` (`P25`, `P26`) | Match ch26’s extrapolative / process-preserving correction predicates; link to `UpdateOperator`/`PreservesUpdateOperator` structure (not `MB8` evidence). |
| ch27 manipulation / false consent vs one-line `MB4_correction_legitimacy` | **ch27** | `Core.lean` (`MB4`), `Correction.lean` | Add **structural** predicates (legitimate vs manipulated endorsement, domestication) implied by ch27; keep `MB4` as the bridge “real systems satisfy legitimacy,” not as the whole formalization. |
| ch03 dynamical guarantee / certified class vs `Certified`/`Risk` axioms | **ch03**, **ch04** | `Certification.lean` (`P01`, `P30`) | Connect `Certified`, `Safe`, and certification conclusion to ch03–04 vocabulary; avoid orphan abstract `Certified A` in hypotheses. |
| ch40 lethality / open issues vs spine taxonomy | **ch40** | `formal/README.md`, all modules | Crosswalk ch40 stress tests to *proof* / *counterexample* / *bridge* labels; flag which open issues are empirical (out of scope) vs formalizable. |

#### Stub chapters — formalize when drafted (not blocking now)

| Chapter | Spine module | Formalize when chapter exists |
|---------|--------------|--------------------------------|
| **ch05** | `Certification`, scope | Assumption/failure-coverage objects tied to `SatisfiesInvariants` / scope predicates. |
| **ch28**–**ch29** | `Successors.lean` (`P27`–`P28`, `SuccessorSafeChain`) | Derive `SuccessorSafe_risk_monotone` / `CorrectionCapacityPreserved` from ch28–29 successor audit; tie weakest-link capacity across successors. |
| **ch30** | `Successors.lean` (`P29`) | Ground `SelfControl` / `CorrectionVisibility` in ch30 self-modeling notation. |
| **ch31**, **ch39** | `Certification.lean` (`P39`, `P40`, safety case) | `Claim`/`Supported`/`ProvenDef` from ch39 safety-case graph; tripwire logic from ch31. |
| **ch32**, **ch35** | `Certification.lean` (`P01`, `P35`, basin) | Basin invariance and attractor narrative vs `BasinStableSys` / `P35`. |
| **ch33** | `Capability.lean` (`P32`), `Adversarial.lean` (`P33`) | Cooperativity `\kappa`, `ICI_{ij}`, open-edge graphs vs `KappaNumerator` / `CoopGraph`. |
| **ch34**, **ch36**, **ch37** | `Adversarial.lean` (`P34`, `P37`) | Host-capacity aliasing and goal-laundering detection beyond `finPigeonhole` toy. |
| **ch38** | `Boundaries.lean` / `Core` | Multi-scale decomposition vs boundary/graph scaffolding. |
| **ch41**–**ch44** | `Philosophy.lean` (`P41`–`P45`) | Legitimacy orderings, bearer persistence, closing synthesis vs current `Bool` separations. |

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
