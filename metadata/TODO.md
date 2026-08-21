# Project TODO

Cross-cutting tasks. **Chapter-local work stays in the `.tex` file** (or `drafts/chapter-notes/`).

Run `make todos` for inline `[STUB]`, `TODO`, and `FIXME` markers in chapters.

**Canonical map (this file).** Session handoff: [`drafts/conversation-summaries/HANDOFF.md`](../drafts/conversation-summaries/HANDOFF.md) points here — do not maintain a parallel open-work list.

Size: **S** <1 session · **M** 1–3 sessions · **L** multi-week.

---

## Work map

| Lane / board | Verb or role | Plan | Size | Depends on |
|--------------|--------------|------|------|------------|
| **Voice** | Dropping the strong wording still leaves factoring | [`drafts/plans/voice.md`](../drafts/plans/voice.md) | L (in progress) | — |
| **Witness** | This process, as it is, can fail a named leaf | [`drafts/plans/witness.md`](../drafts/plans/witness.md) | L (not frozen) | Measurand sheet (Phase 0) |
| **Field** | Same matrix noun, different formal object | [`drafts/plans/field.md`](../drafts/plans/field.md) | M–L | — |
| **Construct** | Named \(I\) moved geometry toward a frozen \(D\), or fail/refuse | *no plan file* | parked | Witness: one real stop (Exp. 4) |
| **Spine** | Lean follow-through not in `formal/README.md` | — | ongoing | Witness Exp. 2 (fixture only) |
| **Cite / Wait** | Blocked on external publish or author call | — | S each | — |
| **Site** | Companion-site chores | — | S–M | De-center PDF → Voice |
| **Outreach** | External artifacts | — | M+ | optional Witness negatives |
| **Housekeeping** | Manuscript/tooling hygiene | — | S | — |
| **Experiments** | Local sim lines | [`experiments/TODO.md`](../experiments/TODO.md) | — | CIRIS Ph.1 = Witness H1 |

**Gates:** Measurand sheet → Witness Phase 0 · Witness real stop → Construct manuscript revisit · Voice does not mention Witness in reader copy.

**Do not centralize here:** chapter `[STUB]`s; appH–K stubs; `% TODO[formalize]:` in chapters; wait-for-external cites.

---

## Where TODOs live

| Kind | Location |
|------|----------|
| **Draft placeholder** | `[STUB]` in chapter `.tex` |
| **Per-chapter gaps** | `% TODO[citation]:`, `% TODO[formalize]:`, `% TODO[open-crux]:` in chapter `.tex` |
| **Research directions** | `metadata/open-problems.md` |
| **Tracked uncertainties** | `metadata/uncertainty-ledger.md` |
| **Cross-cutting chores** | *this file* |
| **Experiment lines** | `experiments/*/TODO.md`, `REPRODUCTION.md` |
| **Session history** | `drafts/conversation-summaries/` (not an active task list) |

---

## Voice (L)

Plan: [`drafts/plans/voice.md`](../drafts/plans/voice.md). **In progress** — §1, §3, §4, §6–§8 done; §2 `chapterthesis` boxes and §5 progress deferred.

- [ ] **De-center the book PDF as the flagship artifact (S).** Site first; demote page-count hook. Cross-ref: `hostile-review.md`.
- [ ] **Separate bridge axioms from book assumptions in reader-facing Lean (M).** Dependency spine naming; bridges are hypotheses to check. Homes: App G, site Lean, `formal/README.md`, `REVIEWING_FOR_AGENTS.md`.
- [ ] **Claims ledger freshness / numbering / completeness (M).** Status vocabulary, C-044, chapter pointers. `review/claim-checklist.md`.
- [ ] **Per-chapter WWCTV → chokepoint forward refs (S).** Residue from correlated steerability review; Chokepoint Lean done. Source: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.
- [ ] **U-ledger reconciliation for chokepoint review (S).** U-03/U-05/U-14/U-16 vs shared-instrument hypothesis.
- [~] **Terminology demotion follow-through (M).** Only if it blocks first-screen honesty; else defer. Inventory: `drafts/glossary-term-audit.md`, `drafts/glossary-prose-pass/THIN.md`.
- [~] **Narrative voice consistency (S).** Optional body pass; wire `check_voice.py` into `make check` if desired.

---

## Witness (L)

Plan: [`drafts/plans/witness.md`](../drafts/plans/witness.md). **Not frozen.** Independent of Voice.

Deliverables below live **in the Witness plan**, not as duplicate rows here:

- Phase 0 freeze sheet = measurand table + verifiability labels + scalar residues (GLI, \(\mathcal{K}\))
- Real worked example (non-fictional); toy/Lean `WorkedInstance` fixture; cornerstone value-bundle test (C-004)
- CIRIS Phase 1 (H1) + later `PositiveMeasuredPath → CorrectionIntegrity`
- Expectation 6 standalone-claim replications; hardware `hardware_tag` as candidate C-003 instrument only

- [ ] **Freeze Witness Phase 0** — charter + pre-register pass/fail/refuse; measurand sheet as the freeze artifact.

---

## Field (M–L)

Plan: [`drafts/plans/field.md`](../drafts/plans/field.md). Independent of Witness.

- [ ] **Field crux divergence.** Homograph table + App B notes + field-local Lean where load-bearing; no new `MB*`. Precedent: [`drafts/attic/field-claim-formalization-and-bridge-review-plan.md`](../drafts/attic/field-claim-formalization-and-bridge-review-plan.md).
- [ ] **MB7a–c field-facing nouns (S).** Optional aliases to field-standard labels without collapsing MB7 split. `reference/field-agendas/inter-agenda-term-glossary.md`.
- [ ] **App B vs merged field-agenda row names (S).** Secondary App B prose deferred.
- [~] **External AI-safety report review — IASP cluster (S).** Interventions index done 2026-08-01; still open: International AI Safety Report → Field when read.

---

## Construct (parked)

**No plan file.** Papers stay spin-outs until Witness records at least one **real stop** (Expectation 4).

- [ ] **Do not include Construction in the manuscript yet.** Companion papers *Alignment Under Selection* and *Constructing Alignment Attractors* (`papers/`). Lean: `ConstructionCrux` / Target Realization in `AlignmentConstruction.lean`. Book path = certification/preservation (ch33), not attractor construction.

  Reviewer bar (2026-08-21) — integration requires a Witness-style **fail/refuse**, not denser definitions:

  > the formal apparatus … currently outruns what it can do. … The main vulnerability is not error but unearned weight … a well-organized restatement of the difficulty, plus a correct but small formal toolkit … not yet a contribution to solving it.

  **Later candidates** (after Witness stop; not Witness phases): H5 construction vs certification stop (same episode, two trees); H3/H4 wrong-vacuum / enforcement-collapse protocols. Manuscript homes if bar met: ch34, ch38, ch48, App. F — **not** a sixth intro claim.

---

## Spine board

Canonical follow-through: [`formal/README.md`](../formal/README.md) + chapter `% TODO[formalize]:`. This section lists **only** items not already tracked there.

Krym architecture revision **closed** 2026-08-17 — [`drafts/attic/krym-architecture-revision-plan.md`](../drafts/attic/krym-architecture-revision-plan.md).

- [~] **`{leanbox}` at remaining `\leanspine` sites (S).** 17 chapters done; ~26 without box — add only where elaboration beats margin note.
- [ ] **Lean Chokepoint identifier rename (S, optional).** Gravestone clarity for retired two-route packaging.
- [ ] **Wire experiment scripts to `BundleEvidenceAdequate` (M).** Deferred from Krym; graded-lab / value-detect hook.
- [ ] **App G translation spine opener (S, author).** Mirror site `/lean/`; manuscript pass author-owned.
- [ ] **MB10 non-enumerability across capability jumps (M).** Conserved set may change at capability jump (ch08/ch30/ch31); unify with `Chokepoint.AdversariallyVerifiableUpTo`; toy red-team of audit forgeability. `Forgeability.lean`.
- [ ] **MB10 chokepoint interface axiom — prove or type (S).** `ConservedPropertySignatureVerifiable_of_chokepoint` in `Forgeability.lean`.
- [ ] **Positive measured path → `CorrectionIntegrity` (M).** After Witness CIRIS consumer; see `Field/Finite/CompositePathBypass.lean`, `experiments/TODO.md`.
- [ ] **Field agenda generated artifacts — build-time only (deferred).** `sync:field-agendas` when schema stable.
- [ ] **App B ↔ field agenda sync — secondary (M).** Spine-translation table, MB9 split, Kosoy footnote, MB11/MB4a site cards.
- [ ] **Regret / numeric harm leaf (deferred).** Side channel only; see `Field/Finite/RegretSafety.lean`.

Hostile-critique / field rederivation / strengthen-spine / Mathlib batches: **partial** — see git logs 2026-06–07 and App G; no separate umbrella TODO.

---

## Cite / Wait board

One queue; pick up when trigger fires.

- [ ] **Turner Reward≠OT follow-up post** — when full post appears; ch21 `% TODO[citation]:`.
- [ ] **MacKinlay *Agency WTF*** — when published; bib + glossary homograph.
- [ ] **Chris Pang boundary ontology** — author call; ch06–07 or `open-problems.md`.
- [ ] **Wire `zarncke2026embedded-value-formation`** — ch15/ch03/ch33; graded-lab §8 touchpoint.
- [ ] **Citation review queue** — complete in-body cites; Part III ch12/ch13 thin; leftover keys from `2026-06-30-deep-research-top10-citations.md`; App C sector empirics (consent decrees, coordinated effects, incident reporting).
- [~] **Logical-induction markets (S).** ch48 WWCTV cites `garrabrant2017logical`; App F paragraph still open.

---

## Site board

De-center PDF → **Voice**. Card-notes triage **closed** 2026-08-17 — [`drafts/attic/site-card-notes-triage.md`](../drafts/attic/site-card-notes-triage.md).

- [ ] **Per-part chapter renumbering (display only) (L, high risk).** Do not rename `chNN` files or `\label`s without migration pass.
- [ ] **Submit page notes to site (S).**
- [ ] **Standalone claims publishability review (S).** Cross-ref Outreach.
- [ ] **Add companion site to Substack (S).**
- [ ] **Book map: generate “Also on the site” from book order (S).**
- [ ] **Part hub cards (S).**
- [ ] **ch10 alignment-faking experiment line (M).**
- [ ] **Chapter-end exercises + online quiz (M).**

---

## Outreach board

- [ ] **Standalone publish — agent-discovery / negative-results line (M).** UAD, embedded/lab sims, or negatives methodology piece.
- [ ] **Pairwise researcher-interest matching — Bubble Connector (M+).** Details TBD.

---

## Housekeeping board

- [ ] **`\symbolref` leftovers (S).** RiskGap and unlabeled blocks. Log: `2026-08-05-symboldef-macro.md`.
- [ ] **Eq-chain / informal reading DAG (S).** C12 basin operationalization (ch38); `chapter-informal-edges.yml`; `p_\theta` vs MI `\theta`. `drafts/editorial-guidance-eq-chain-placement.md`.
- [ ] **Consider claims/assumptions ledger automation (S).** Decide YAML source vs manual.
- [ ] **Review U-shaped coordination claim (S).** ch11/ch13 conjectural until downgrade or evidence.
- [ ] **Grounding/safety-case layer completeness review (S).** ch46 eighth layer: derived vs provisional checklist.
- [ ] **Perturbation-recognition crux (S).** ch47 `% TODO[open-crux]:` — bounded answer or downgrade.
- [~] **ch48 inferential coupling / acausal trade (research).** Drafted; threshold calibration and probe-local coordination open.
- [ ] **Inferential-coupling threshold calibration (research).** ch47/ch48 \(\tau_{\mathrm{ac}}\).
- [ ] **Probe-local inferential coordination (research).** ch48 vs ch46 gap or mark unresolved.
- [~] **Notation reconciliation (S).** ⟳ rows in `metadata/notation.md`; C12 basins; confirm `C_H` vs `C^H_t`.
- [~] **Lean spine ↔ notation review (M).** Partial 2026-06-29; bundle geometry, ch13 P12, ch48 basins remain.
- [~] **Update-operator ontology audit (M).** Partial 2026-06-28 envelope refactor.
- [ ] **Part-opener illustrations (S).**
- [ ] **Optional: LaTeX PDF CI build test (S).** `.github/workflows/book-pdf.yml`; compile gate only.
- [x] **Strategic advice follow-through — closed.** Remainders absorbed into Voice / Spine / Outreach (`review/strategic-advice-2026-06-28.md`).

Residues formerly under **BIG REVIEW** headings: MB10 forgeability → Spine; chokepoint WWCTV refs → Voice; forgeability budget / hindsight caveat → ch48 score when author passes ch31.

---

## Experiments / demos

Major graded-lab backlog: [`experiments/graded-lab-simulation/REPRODUCTION.md`](../experiments/graded-lab-simulation/REPRODUCTION.md) — not itemized here.

- [ ] **Graded-lab v3 — audit vocabulary drift (M).**
- [ ] **Graded-lab v3 — review Q1 failure cascade from v1 freeze (S).**
- [ ] **Review SOO relation to book adversarial scenarios (S).** `drafts/soo-benchmark-scenarios-from-book.md`.
- [ ] **D3 selection-ecology toy demo (M).** lab-sim G-36/G-37; `demos/ch08-selection-ecology/` candidate.

CIRIS composite / boundary_decouple: **Witness H1** — charter in sibling `ciris/review/`; [`experiments/TODO.md`](../experiments/TODO.md).

---

## Appendix follow-through

- [~] **Built in PDF:** appA–G, appM, appD, appE, appF, appN.
- [~] **Still `[STUB]` (not in `book.tex`):** appH, appI, appJ, appK.

---

## Closed (one-liners — do not reopen)

Narratives in git / `drafts/conversation-summaries/`. Plans in `drafts/attic/`.

- [x] Krym architecture revision · MB6b∨MB8 prose retirement · Field v2 hub · Field matrix bridge nouns (2026-08-02) · Consciousness/MB3 extension · Six-claims spine · Pivotal act BIG REVIEW · Chapter splits/renumber · App B core sync · Translation spine Ph.1–2 · Epistemic markers · Frontmatter gaps · Native Debate/ELK matching · Guard axiom budget · Clickable badges · Duplicate LaTeX labels / hyperref `page.i` fix · *(see git for full list)*

---

## Leave local (do not centralize here)

- Per-chapter `% TODO(deep-research):`, `% TODO[citation]:`, `% TODO[formalize]:`, `% TODO[open-crux]:` in chapter `.tex`.
- All `[STUB]` placeholders until chapter integrated.
- Appendix `[STUB]` in appH–appK only.
- `drafts/chapter-notes/*.tex` deferred notes.
