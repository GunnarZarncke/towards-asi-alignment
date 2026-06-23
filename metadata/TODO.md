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
- [ ] **§10 structure pass** — chapter-ending headings normalized to `\section{Summary}` (2026-06-22). Remaining: ch12 and ch42 still carry **both** a `Conclusion` and a `Chapter summary` (merge into one Summary); ch23 has a front `Chapter Summary` + tail `Chapter Conclusion` (drop/condense the front, rename the tail). See `review/fix-plans-2026-06-22.md` §B12. **2026-06-23:** ch12/ch42/ch23 B12 merges done in redundancy pass.
- [ ] **Review U-shaped coordination claim (conjectural)** — the mid-scale coordination-efficiency U-shape appears in ch11 (forward-ref only) and ch13 (Section~\ref{sec:mid-scale-collapse-ch13}). Treat as conjectural until empirical backing or explicit downgrade; decide claim strength, add uncertainty-ledger entry if needed, and reconcile with `context/extracts/bitwise-iq.md` sampling-bias caveats.
- [ ] **Claims / assumptions ledgers** — full cross-check done 2026-06-23: `claims-ledger.md` now holds C-001–C-011 + C-044 (mapped to the 5 `introclaim`s, 44 chapter theses, and the spine), `assumptions-ledger.md` holds A-001–A-007, `uncertainty-ledger.md` holds U-01–U-15 (each linked to the claim/assumption it threatens). **Ongoing:** when drafting/revising a chapter, keep the relevant C-/A-/U- entries in sync (status, chapter refs, references) and wire BibLaTeX keys into the `References:` placeholders. See `review/claim-checklist.md`.
- [ ] **ch05 partial draft** — complete scope/failure-coverage chapter to manuscript depth: add a failure-mode section and a `What Would Change This View` section, resolve inline `[Defined]` markers (L56, L109–111), and deliver the `TODO[citation]` Turchin AGI failure-mode map citation in `ch05-assumptions-scope-failure-coverage.tex`.
- [ ] **ch40 flesh-out** — `ch40-lethality-stress-test-open-issues.tex` is ~1,500 words vs a 9,000 target: add per-lethality prose to the 13-row checklist (each cell is currently a single phrase), resolve the two `% TODO[open-crux]` markers (L119, L121; reflective stability of correction; delegating superhuman plan evaluation — mirror `metadata/uncertainty-ledger.md` items 7–8), and add a forward bridge to ch41.
- [ ] **Frontmatter gaps** — write the stub front-matter and finish the executive overview: `frontmatter/preface.tex`, `frontmatter/dedication.tex`, `frontmatter/acknowledgements.tex` (all `[STUB]`), and the three `[STUB]` blocks in `frontmatter/executive-overview.tex` (Diagram in Words L27, Assumptions L32–34, What This Book Tries to Establish L58).
- [ ] **Opening-promise reconciliation** — when ch44 (conclusion) and ch39 (safety case) are written, **explicitly discharge or explicitly soften** each opening promise: the Introduction's five `introclaim`s (boundary, value-bundle, correction, successor, basin), its six "What Counts as Progress" artifacts, its six-point "Practical Hope" regime, and the Executive Overview's five preservation problems. Any promise the finished chapters cannot back must be weakened in `frontmatter/introduction.tex` / `executive-overview.tex` rather than left dangling. Payability analysis (claims 1–4 already backed; claim 5 needs ch33; safety-case + synthesis are the gaps) is in `review/fix-plans-2026-06-22.md` §D.
- [ ] **Part-opener prose** — each `parts/partNN-*.tex` is currently just `\part{...}` + chapter `\input`s. Add a 1-paragraph opener per part (what the part adds, which chapters it contains, what it assumes from earlier parts) to smooth the larger arc. See `review/fix-plans-2026-06-22.md` §H6 / review §6.8.
- [ ] **Verifiability-label pass** — for each core measurand (boundary residual, B-IQ/boundary information, value-bundle geometry, bearer maps, correction-channel integrity, conserved successor properties, laundering index), label it *observable*, *i.i.d.-robust*, or *adversarially verifiable up to $\kappa$* and propagate the label into the safety case (ch39). Framework + definitions owned by **ch39b** (`What Survives an Adversary`). The lethality stress test (ch40) should be cross-referenced as "metrics sorted by adversarial-verifiability failure."
- [ ] **Perturbation-recognition crux** — resolve the open question seeded in ch39b/ch36: *name a perturbation a superintelligence cannot recognize as a test.* If none exists, active-measurement remedies (ch36) collapse to the system's chosen story and the cost relation (below) is the only handle. Lives inline as `% TODO[open-crux]` in `ch39b`; ch36 now states the blunt challenge in prose — still needs a bounded answer or an explicit downgrade.
- [ ] **ch33 acausal trade section (`sec:acausal-trade-review`)** — Round-2 seeded a review subsection from `\autocite{zarncke2025acausal}`; promote to drafted depth. Tasks: (1) separate what TDT/FDT/LDT prove from what the UAD/$\widehat{\mathrm{IC}}_{ij}$ detector empirically estimates; (2) specify probe-set construction, threshold calibration ($\tau_{\mathrm{ac}}$), and adversarial evasion bounds via ch39b $c_{\mathrm{fake}}$; (3) wire $\widehat{\mathrm{IC}}_{ij}$ / $\mathrm{ICI}_{ij}$ explicitly to the $\tilde{\kappa}_{ij}$ percolation claim (giant-component conditions); (4) add mitigations under noisy meta-priors (deferred in source); (5) reconcile the worked example's acausal vignette with ch39b adversarial reading; (6) resolve remaining ch33 `[STUB]`s (privacy islands L45, counterexample L150). Source canon: `context/extracts/acausal-trade-uad-formalization.md`. Promote `book.yml` ch33 from `stub` when done.
- [~] **Notation reconciliation** — apply the cross-chapter symbol/formula resolutions in `review/fix-plans-2026-06-22.md` §C, then record canonical forms in `appendices/appA-notation.tex`, `metadata/notation.md`, and INSTRUCTIONS §18 (keep all three in sync).
  - **Done 2026-06-23 (build verified):** C1 ΔL sign; C2 `g_B`/`H_B`/`G_B`+retire `T_{ij}`; C4/C16 `C_raw`/`CCI`+retire `C_corr` (ch05 `$C_{\text{corr}}^{\text{society}}$` kept); C5 `K` capability in ch11–13; C6 `η_g`/`η_c`+`G_coord`/`Ω_coord`; C7 `U_H`+roman `V_t`; C8 `F`+`k`; C10 `C_X`; C11 `χ_{ij}(a)`; C15 `\MI`; **U_S** (ch24/29/38). See `drafts/conversation-summaries/2026-06-23-notation-propagation.md`.
  - **Remaining:** sync `appendices/appA-notation.tex` + INSTRUCTIONS §18; **Lean spine ↔ notation review** (below). **C12 pivotal-process basins:** formalized in ch35 (`sec:pivotal-process-ch35`); Lean `P35` still open.
  - **Confirm with author:** `C_H` vs time-indexed `C^H_t` convention.
- [ ] **Lean spine ↔ notation review** — review `formal/AlignmentProofSpine/*.lean` (and `formal/README.md`) for identifiers/comments that diverge from the propagated canonical notation: capability `K` (vs `B`), value bundle `B`, **`U_H` (human value-update) vs `U_S` (system correction-update)** — Lean currently has a single axiom `UpdateOperator` / `PreservesUpdateOperator` mapped to $U_H$ only; add `SystemUpdateOperator` (or rename/split) for $U_S$ and ch24's $(\Theta,Z)\mapsto(\Theta',Z')$ under correction; ch29 successor tuple should carry both operators where relevant, `g_B`/`H_B`/`G_B`, feature matrix `F`, bundle dim `k`, host capacity `C_X`, artifact conductivity `χ` vs cooperativity `κ`, residual surprise `S_X`, `η_g`/`η_c`, `G_coord`/`Ω_coord`, `ΔL` sign convention, and `C_raw`/`CCI` (retire `C_corr`). Reconcile names so the proof spine and manuscript use the same symbols; note any gaps in the session log + this file. (Pairs with the C5 `B→K` and C4/C16 `C_corr` passes above.)

---

## Blocked on unwritten chapters

Dependency map: tasks that **cannot be completed until a stub chapter is drafted**. When a chapter below is written, discharge its gated items here (and update the relevant C-/A-/U- ledger entries). Stub set per `metadata/book.yml`: ch05 (partial), ch33, ch39, ch43, ch44.

- [ ] **Blocked on ch33** (Multi-Agent Superintelligence and Strategic Coupling — partial stub):
  - Intro **basin claim (claim 5)** stays only *mostly* payable until ch33 firms up multi-agent coupling (`review/fix-plans-2026-06-22.md` §D); discharge in ch44 reconciliation depends on it.
  - Formalize `ICI_{ij}` (inferential coupling index) and coalition-collapse tests (see Formalization tracks; also cited in ch40's open ledger).
  - **ch32→ch33→ch34 narrative seam** — add the missing bridges once ch33 exists (currently an orphan seam).
  - U-12 (coalition/coupling detection) in `uncertainty-ledger.md` stays open until drafted.
  - Resolve the ch33 `% TODO(deep-research)` cite seeds. (Acausal-trade `% TODO[citation]` discharged in Round-2; section depth tracked under Manuscript → **ch33 acausal trade section**.)
- [ ] **Blocked on ch39** (A Safety Case for Superintelligence Alignment — stub):
  - Discharges the 6th "What Counts as Progress" artifact (safety case) and closes **C-044** / U-14 (with ch44).
  - **Verifiability-label pass** (above) lands its labels in the safety case; framework owned by ch39b.
  - **appG** safety-case template — write coupled with ch39 (`review/fix-plans-2026-06-22.md` §E).
  - Lean: `P40` safety-case support + "Wire spine into manuscript" (cite each theorem as proof/counterexample/bridge).
- [ ] **Blocked on ch43** (Who Still Counts After Transformation / bearers of value — stub):
  - Canonical **home for the selfhood bottleneck `β_self`** (ch30 already forward-refs here) — define it here.
  - Consolidate the **merger/upload "progress or loss?"** treatment scattered across ch18, ch20, ch22, ch23, ch41, ch42 into one canonical instance + cross-refs (review §4 / §B-merger).
  - Lean `P41`–`P45`: legitimacy orderings, bearer persistence.
- [ ] **Blocked on ch44** (Towards Superintelligence Alignment / conclusion — stub):
  - **Opening-promise reconciliation** (above): explicitly discharge or soften the 5 `introclaim`s, 6 progress artifacts, and 6 "Practical Hope" points.
  - Closes **C-044** (intro-claim discharge) and U-14; closing-synthesis Lean (`Philosophy.lean` `P41`–`P45`).
- [ ] **Blocked on ch05** (Assumptions, Scope, Failure Coverage — partial): tracked separately under *Manuscript (cross-cutting)* → "ch05 partial draft."
- [ ] **Appendices gated on their chapters** — B (boundary, ch07), C (value-bundle inference, ch16/20), D (correction-channel audit, ch25), E (successor certification, ch31), G (safety-case template, ch39). appA (notation) + appF (glossary) are **not** blocked — write from `metadata/notation.md` / `terminology.md` now; appH folds into ch40 + `open-problems.md` (`review/fix-plans-2026-06-22.md` §E).

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
- [ ] **Derive full certification chain** — ~~link BIQ ceiling (`P10`) to control via `Control_le_IctrlSys` / `BIQDerivedCapacitySlack`~~ *(done)*; ~~tie `CorrectionCapacity` to weakest-link graph capacity (`P24` / `CorrectionLinkCapacities`)~~ *(done)*; extend with adversarial aliasing (`P34`/`MB7` structural layer), and safety-case support (`P40`). ~~Propagate bounds along successor-safe chains (`P27`/`SuccessorSafeChain`).~~ *(done)*
- [ ] **Wire spine into manuscript** — Ch. 39 safety case / appendix cites each theorem as *proof*, *counterexample*, or *bridge* per `formal/README.md`.

#### Chapter ↔ Lean mapping gaps (**drafted chapters only**)

| Critic gap | Draft chapter(s) | Lean module / nodes | TODO |
|------------|------------------|---------------------|------|
| ch24/ch29 system correction-update vs human value-update | **ch24**, **ch29** | `Core.lean`, `Correction.lean` | Split Lean carriers: `UpdateOperator` / `PreservesUpdateOperator` → $U_H$ (human value revision); add `SystemUpdateOperator` (or equivalent) → $U_S$ for $(\Theta,Z)\mapsto(\Theta',Z')$ under correction; ch29 successor tuple should name both. Manuscript now uses $U_S$ (not `\mathcal U`). |
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

- [x] Resolve duplicate LaTeX labels: `sec:self-modeling-transparency`, `sec:example-helpful-assistant` — both now carry unique `-chNN` suffixes; no `multiply defined` warnings.
- [x] Fix duplicate hyperref destination `page.i` (title page collided with dedication): switched title page to `titlingpage*` (no page-counter reset).

---

## Leave local (do not centralize here)

- All `% TODO(deep-research):` blocks in stub chapters ch15–ch44 (and ch05) — per-chapter cite wiring on draft.
- All `[STUB]` section placeholders until each chapter is integrated.
- `frontmatter/dedication.tex` `[STUB]`.
- Appendix `[STUB]` markers in `appendices/app*.tex`.
- `drafts/chapter-notes/ch33-cooperation-percolation-deferred.tex` and sibling deferred notes.
