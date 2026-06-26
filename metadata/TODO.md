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

## Big reviews (cross-cutting cruxes)

These are substantial review passes, not single edits. Each spans several chapters and should end with either a reconciled claim-strength decision or an explicit downgrade + open-crux entry in `metadata/uncertainty-ledger.md`.

- [ ] **BIG REVIEW — Conserved-property transport decoupled from safety (Grow/Split/Merge).** Span: **ch08** (grow/split/merge), **ch28** (successor central test), **ch29** (seven conserved properties). The transport-of-conserved-properties approach is decoupled from safety in *two* directions, and neither is currently bounded:
  1. **Forgeable.** A capable predecessor can engineer a successor to pass every conserved-property check (boundary closure, memory lineage, value-bundle geometry, bearer-map continuity, correction-channel capacity, transparency policy, control-locus continuity) while defecting on whatever was *not* conserved. Passing the seven-property score is then evidence of nothing against an adversarial predecessor — the properties become the successor's optimization constraints.
  2. **Non-enumerable.** Across a real capability jump the *relevant* conserved set changes (new action channels, new self-model), and the now-critical invariant could not have been listed beforehand — the same shape as ch03's unprojectable safe set.
  Task: decide whether conserved-property transport can be made *adversarially verifiable* via the ch39b cost relation (bound the cost of forging the signature) or must be labelled a comfort metric; add an explicit **forgeability budget** and a **hindsight-completeness caveat** to ch29's score; reconcile claim strength across ch08/ch28/ch29; cross-reference ch39b. Owner node: ch29 (the score). Mirror the residue into `metadata/uncertainty-ledger.md`.

- [ ] **BIG REVIEW — The pivotal-act reframe ("pivotal process") may rename rather than dissolve the lethality.** Span: **ch35** (alignment attractor / pivotal process), **ch40** (lethality stress test, "Pivotal act" row), `formal/` (`P35` basin). ch40 reframes Yudkowsky's pivotal act as a socio-technical basin transition $\mathcal{B}_{\text{race}}\to\mathcal{B}_{\text{certified}}$. Hostile reading: the reframe *relocates* the lethality. Either (a) some actor can *force* the basin flip against competitive incentives — that is a pivotal act by another name, carrying the same unilateralism and capability-concentration Yudkowsky flagged — or (b) no actor can, and the race basin is a stable attractor we have just conceded we cannot exit. "Process" smuggles in *incremental and steerable*, which is the disputed claim. Task: in ch35, either **specify the conditions** under which a basin transition is achievable *without* a unilateral, capability-concentrating act (and prove/bound them against `P35`), or **downgrade** ch40's status for this row from "Reframed" to "Renamed, open" and state the unilateralism residue explicitly. Mirror to `metadata/uncertainty-ledger.md` (pivotal-process item).

## Manuscript (cross-cutting)

- [ ] **Complete citation review** — in-body `\autocite`/`\cite` coverage, missing BibTeX keys, `context/lw-references.md` crosswalk, chapter reference blocks. Part III ch12/ch13 known thin; deferred pending this pass.
- [ ] **Bundle catalogue terminology drift** — the ch16 value-bundle *catalogue* (care, non-suffering, truth, autonomy, justice, loyalty, dignity, beauty, protection, etc.) is the canonical roster of *bundle types*. Later chapters sometimes add adjacent terms (legitimacy, prudence, truth-contact, Learning/Legacy) in *governed-change criteria*, *conserved-property audits*, or example lists without updating ch16 or stating they are not new bundle dimensions. Task: audit ch15/28/29/30/31 (and ch08 preview lists) for terms that look like bundle-catalogue additions; either add them to ch16's catalogue with justification or relabel them explicitly (e.g.\ as legitimacy *criteria*, certification *domains*, or bundle *activations* under an existing dimension). See `review/fix-plans-2026-06-22.md` §C13.
- [ ] **Chapter numbering cleanup** — decide whether to switch to part-relative chapter numbering or globally renumber chapters after the insertion of `ch39b`; then update filenames, `metadata/book.yml`, chapter labels/references, generated tables, and any prose references that assume the current numbering.
- [ ] **§10 structure pass** — chapter-ending headings normalized to `\section{Summary}` (2026-06-22). Remaining: ch12 and ch42 still carry **both** a `Conclusion` and a `Chapter summary` (merge into one Summary); ch23 has a front `Chapter Summary` + tail `Chapter Conclusion` (drop/condense the front, rename the tail). See `review/fix-plans-2026-06-22.md` §B12. **2026-06-23:** ch12/ch42/ch23 B12 merges done in redundancy pass.
- [ ] **Review U-shaped coordination claim (conjectural)** — the mid-scale coordination-efficiency U-shape appears in ch11 (forward-ref only) and ch13 (Section~\ref{sec:mid-scale-collapse-ch13}). Treat as conjectural until empirical backing or explicit downgrade; decide claim strength, add uncertainty-ledger entry if needed, and reconcile with `context/extracts/bitwise-iq.md` sampling-bias caveats.
- [~] **Claims / assumptions ledgers** — `claims-ledger.md` and `assumptions-ledger.md` are manually maintained maintainer ledgers. `assumptions-ledger.md` also generates Appendix E; `claims-ledger.md` is not generated and was header-refreshed 2026-06-26 after `ch39b`/main-draft completion. **Ongoing:** when drafting/revising a chapter, keep C-/A-/U- entries in sync. See `review/claim-checklist.md`.
- [ ] **Consider claims/assumptions ledger automation** — decide whether to move claims and assumptions to structured metadata (`claims.yml`, `assumptions.yml`, or chapter-local markers) and generate `metadata/claims-ledger.md`, `metadata/assumptions-ledger.md`, Appendix E, and reviewer-facing tables from that source. Goal: reduce drift between chapter prose, WWCTV sections, Lean bridge assumptions, and maintainer ledgers.
- [x] **ch05 partial draft** — completed 2026-06-26: expanded scope/failure-coverage chapter, added correction-capacity failure mode, resolved inline markers, retained WWCTV, and added the Turchin/Denkenberger citation.
- [ ] **Frontmatter gaps** — write the stub front-matter and finish the executive overview: `frontmatter/preface.tex`, `frontmatter/dedication.tex`, `frontmatter/acknowledgements.tex` (all `[STUB]`), and the three `[STUB]` blocks in `frontmatter/executive-overview.tex` (Diagram in Words L27, Assumptions L32–34, What This Book Tries to Establish L58).
- [x] **Opening-promise reconciliation** — completed 2026-06-26 in ch44: explicitly revisits the five Introduction claims, the six progress artifacts, the Practical Hope regime, and the Executive Overview preservation problems; unresolved bridges are softened as conditional/open rather than left dangling.
- [ ] **Verifiability-label pass** — for each core measurand (boundary residual, B-IQ/boundary information, value-bundle geometry, bearer maps, correction-channel integrity, conserved successor properties, laundering index), label it *observable*, *i.i.d.-robust*, or *adversarially verifiable up to $\kappa$* and propagate the label into the safety case (ch39). Framework + definitions owned by **ch39b** (`What Survives an Adversary`). The lethality stress test (ch40) should be cross-referenced as "metrics sorted by adversarial-verifiability failure."
- [ ] **Perturbation-recognition crux** — resolve the open question seeded in ch39b/ch36: *name a perturbation a superintelligence cannot recognize as a test.* If none exists, active-measurement remedies (ch36) collapse to the system's chosen story and the cost relation (below) is the only handle. Lives inline as `% TODO[open-crux]` in `ch39b`; ch36 now states the blunt challenge in prose — still needs a bounded answer or an explicit downgrade.
- [~] **ch33 acausal trade section (`sec:acausal-trade-review`)** — drafted to manuscript depth 2026-06-26: separates decision-theoretic basis from empirical detector, wires \(\widehat{\mathrm{IC}}_{ij}\) / \(\mathrm{ICI}_{ij}\) to \(\tilde{\kappa}_{ij}\), calibrates adversarial evasion through ch39b, and resolves remaining `[STUB]`s. Still open as research: large-scale ICI dynamics, noisy-prior mitigations, and adversarially verifiable coalition detection.
- [~] **Notation reconciliation** — apply the cross-chapter symbol/formula resolutions in `review/fix-plans-2026-06-22.md` §C, then record canonical forms in `metadata/notation.md` (Appendix A is generated from it).
  - **Done 2026-06-23 (build verified):** C1 ΔL sign; C2 `g_B`/`H_B`/`G_B`+retire `T_{ij}`; C4/C16 `C_raw`/`CCI`+retire `C_corr` (ch05 `$C_{\text{corr}}^{\text{society}}$` kept); C5 `K` capability in ch11–13; C6 `η_g`/`η_c`+`G_coord`/`Ω_coord`; C7 `U_H`+roman `V_t`; C8 `F`+`k`; C10 `C_X`; C11 `χ_{ij}(a)`; C15 `\MI`; **U_S** (ch24/29/38). See `drafts/conversation-summaries/2026-06-23-notation-propagation.md`.
  - **Remaining:** propagate ⟳ rows in `metadata/notation.md`; **C12 pivotal-process basins:** formalized in ch35 (`sec:pivotal-process-ch35`); Lean `P35` basin narrative still open.
  - **Confirm with author:** `C_H` vs time-indexed `C^H_t` convention.
- [~] **Lean spine ↔ notation review** — sync 2026-06-23 (`drafts/conversation-summaries/2026-06-23-lean-spine-notation-sync.md`): `U_H`/`U_S`; **`CCI` only** in Lean (no `C_raw` export; weakest link internal to `CCI`); typed `CorrectionPath`; `SuccessorSafeWitness` (`CCIPreserved` + `U_S`); spine citations in ch03/24–26/29/31/39. **Still open:** bundle geometry in `Bundles.lean`; ch13 `P12`; ch35 basins; strengthen `Bool` counterexamples; more chapter citations.
- [ ] **Update-operator ontology audit** — review update operators across Lean, notation, and manuscript prose for hidden ontology imports. In particular, check whether value/correction/successor update maps assume a fixed ontology, privileged state variables, or semantic coordinates that should instead be represented through transport, bearer maps, or bridge assumptions; then revise the formal signatures and chapter claims accordingly.

---

## Blocked on unwritten chapters

Dependency map: tasks formerly blocked on stub chapters. As of 2026-06-26, ch05, ch33, ch39, ch43, and ch44 are drafted; remaining items below are research or appendix follow-through rather than blockers on unwritten chapters.

- [x] **Formerly blocked on ch33** — drafted 2026-06-26. Ch33 now pays the multi-agent coupling role for the basin claim, defines privacy islands, calibrates \(\kappa\)/\(\mathrm{ICI}\)/\(\tilde{\kappa}\), and states coalition-collapse limits. U-12 remains open as empirical/adversarial detection work.
- [~] **Formerly blocked on ch39** — drafted 2026-06-26. Ch39 now assembles the conditional safety-case graph, cites `P30`/`P40` and bridges, and introduces verifiability labels. Remaining follow-through: write appG safety-case template and continue the full measurand-by-measurand verifiability-label pass.
- [x] **Formerly blocked on ch43** — drafted 2026-06-26. Ch43 now houses merger/upload treatment, the selfhood bottleneck \(\beta_{\mathrm{self}}\), and the `P41`–`P45` philosophical-limit framing.
- [x] **Formerly blocked on ch44** — drafted 2026-06-26. Ch44 now performs opening-promise reconciliation and closes C-044 at manuscript-draft strength.
- [x] **Formerly blocked on ch05** — drafted 2026-06-26.
- [ ] **Appendices gated on their chapters** — B (boundary, ch07), C (value-bundle inference, ch16/20), D (correction-channel audit, ch25), G (safety-case template, ch39). **appA** is generated from `metadata/notation.md`; **appF** from `metadata/terminology.md`. appH research program drafted (2026-06-25); folds ch40 + `open-problems.md` themes (`review/fix-plans-2026-06-22.md` §E). Successor certification lives in ch28–31 (no separate appendix).

---

## Formalization tracks

Canonical home is the chapter that *owns* the object; other chapters should reference, not duplicate, inline TODOs.

| Track | Canonical chapter | Also referenced in |
|-------|-------------------|-------------------|
| Define $\mathrm{ICI}_{ij}$ (inferential coupling index) | ch33 | ch40 open-problem ledger |
| Coalition-collapse empirical tests | ch33 | ch40 |
| Pivotal process $\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}$ conditions | ch35 (`sec:pivotal-process-ch35`) | ch40 |
| Transparency ↔ $\kappa_{ij}$ ↔ correction observability | ch33 only | — |
| Cost-of-opacity / budget verifiability $c_{\mathrm{fake}}(M,\Delta)$ vs affordable surplus | ch39b | ch10, ch11, ch22, ch36, ch38 |
| Prove/bound measure of decisive-yet-undetectable effective controllers (representability vs detection-latency) | ch39b | ch07, ch09, ch38 |
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
- [ ] **Derive full certification chain** — ~~link BIQ ceiling (`P10`) to control via `Control_le_IctrlSys` / `BIQDerivedCapacitySlack`~~ *(done)*; ~~tie `CCI` to weakest effective handle capacity (`P24` / `CorrectionLinkCapacities`)~~ *(done)*; extend with adversarial aliasing (`P34`/`MB7` structural layer), and safety-case support (`P40`). ~~Propagate bounds along successor-safe chains (`P27`/`SuccessorSafeChain`).~~ *(done)*
- [ ] **Wire spine into manuscript** — Ch. 39 safety case / appendix cites each theorem as *proof*, *counterexample*, or *bridge* per `formal/README.md`.

#### Chapter ↔ Lean mapping gaps (**drafted chapters only**)

| Critic gap | Draft chapter(s) | Lean module / nodes | TODO |
|------------|------------------|---------------------|------|
| ch24/ch29 system correction-update vs human value-update | **ch24**, **ch29** | `Core.lean`, `Correction.lean` | **Partial (2026-06-23):** `ValueUpdateOperator`/`SystemUpdateOperator`, `PreservesValueUpdateOperator`/`PreservesSystemUpdateOperator`, `SystemUpdateOperatorPreserved`. Still: structured `(Θ,Z)` state, derive successor audit from ch28–29. |
| `CorrectionLinkCapacities` is still an abstract integer profile, though now attached to controlled handles | **ch24**, **ch25** | `Correction.lean` (`P23`, `P24`) | **Partial (2026-06-25):** `CorrectionPath A` now records a correcting agent, access model, controlled handles, reach, persistence, and non-capture. Still: define effective handle capacity \(\kappa_i\) from concrete observation/operation data rather than abstract integers. |
| Only raw `min` capacity; no CCI penalties `L,M,R,Ω` from ch25 | **ch25** | `Correction.lean` | **Partial (2026-06-23):** `CCI`, `CCIPenaltyTerms`/`CCIPenaltyWeights`, `CCIPenaltiesSys`. Still: tie certification primary slack to `CCI` threshold θ. |
| Slack certificates (`BIQDerivedCapacitySlack`, `WeakestLinkDerivedCapacitySlack`) are not tied to chapter measurands | **ch11**, **ch13**, **ch25** | `Capability.lean`, `Certification.lean` | **Partial:** fields renamed `cact_le_craw`; `SpineCCIWitness`. Still: map ch13 coordination loss into certificates. |
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
| **ch31**, **ch39** | `Certification.lean` (`P40`, safety case) | `Claim`/`Supported`/`ProvenDef` from ch39 safety-case graph. |
| **ch32**, **ch35** | `Certification.lean` (`P01`, `P35`, basin) | Basin invariance and attractor narrative vs `BasinStableSys` / `P35`. |
| **ch33** | `Capability.lean` (`P32`), `Adversarial.lean` (`P33`) | Cooperativity `\kappa`, `ICI_{ij}`, open-edge graphs vs `KappaNumerator` / `CoopGraph`. |
| **ch34**, **ch36**, **ch37** | `Adversarial.lean` (`P34`, `P37`) | Host-capacity aliasing and goal-laundering detection beyond `finPigeonhole` toy. |
| **ch38** | `Boundaries.lean` / `Core` | Multi-scale decomposition vs boundary/graph scaffolding. |
| **ch41**–**ch44** | `Philosophy.lean` (`P41`–`P45`) | Legitimacy orderings, bearer persistence, closing synthesis vs current `Bool` separations. |

---

## Build / tooling

- [x] Resolve duplicate LaTeX labels: `sec:self-modeling-transparency`, `sec:example-helpful-assistant` — both now carry unique `-chNN` suffixes; no `multiply defined` warnings.
- [x] Fix duplicate hyperref destination `page.i` (title page collided with dedication): switched title page to `titlingpage*` (no page-counter reset).

---

## Leave local (do not centralize here)

- All `% TODO(deep-research):` blocks in stub chapters ch15–ch44 (and ch05) — per-chapter cite wiring on draft.
- All `[STUB]` section placeholders until each chapter is integrated.
- `frontmatter/dedication.tex` `[STUB]`.
- Appendix `[STUB]` markers in `appendices/app*.tex`.
- `drafts/chapter-notes/ch33-cooperation-percolation-deferred.tex` and sibling deferred notes.
