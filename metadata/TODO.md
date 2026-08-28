# Project TODO

Cross-cutting tasks. **Chapter-local work stays in the `.tex` file** (or `drafts/chapter-notes/`).

Run `make todos` for inline `[STUB]`, `TODO`, and `FIXME` markers in chapters.

**Canonical map (this file).** Session handoff: [`drafts/conversation-summaries/HANDOFF.md`](../drafts/conversation-summaries/HANDOFF.md) points here — do not maintain a parallel open-work list.

**Lane checklists** live only in [`drafts/plans/`](../drafts/plans/) (`voice`, `witness`, `field`, `spine`, `construct`). Below: work map, gates, and non-lane boards.

Size: **S** <1 session · **M** 1–3 sessions · **L** multi-week.

---

## Work map

| Lane / board | Verb or role | Plan | Size | Depends on |
|--------------|--------------|------|------|------------|
| **Voice** | Dropping the strong wording still leaves factoring | [`drafts/plans/voice.md`](../drafts/plans/voice.md) | L (in progress) | — |
| **Witness** | This process, as it is, can fail a named leaf | [`drafts/plans/witness.md`](../drafts/plans/witness.md) | L (Phase 0 frozen) | Phase 1: H1 C2 + H4 MASK |
| **Field** | Same matrix noun, different formal object | [`drafts/plans/field.md`](../drafts/plans/field.md) | M–L | — |
| **Construct** | Named \(I\) moved geometry toward a frozen \(D\), or fail/refuse; **constructibility** = willing/able to build, not narrate | [`drafts/plans/construct.md`](../drafts/plans/construct.md) | L (plan open; v1 MS parked) | Concrete chapters: Witness Exp. 4. Process-condition outline: not gated |
| **Spine** | Chapter formalism matches Lean structure | [`drafts/plans/spine.md`](../drafts/plans/spine.md) | ongoing | Witness Exp. 2 (fixture only) |
| **Cite / Wait** | Blocked on external publish or author call | — | S each | — |
| **Site** | Companion-site chores | — | S–M | De-center PDF → Voice |
| **Outreach** | External artifacts | — | M+ | optional Witness negatives |
| **Housekeeping** | Manuscript/tooling hygiene | — | S | — |
| **Experiments** | Local sim lines | [`experiments/TODO.md`](../experiments/TODO.md) | — | CIRIS Ph.1 = Witness H1 |

**Gates:** Witness Phase 0 frozen ([`drafts/plans/witness-phase0.md`](../drafts/plans/witness-phase0.md)) · Witness real stop → Construct *concrete* manuscript revisit · Construct *plan* / constructibility outline is not gated · Voice does not mention Witness in reader copy.

**Do not centralize here:** chapter `[STUB]`s; appH–K stubs; `% TODO[formalize]:` in chapters; wait-for-external cites.

---

## Where TODOs live

| Kind | Location |
|------|----------|
| **Draft placeholder** | `[STUB]` in chapter `.tex` |
| **Per-chapter gaps** | `% TODO[citation]:`, `% TODO[formalize]:`, `% TODO[open-crux]:` in chapter `.tex` |
| **Research directions** | `metadata/open-problems.md` |
| **Tracked uncertainties** | `metadata/uncertainty-ledger.md` |
| **Cross-cutting chores** | *this file* (boards only) |
| **Lane plans (checklists)** | `drafts/plans/*.md` |
| **Experiment lines** | `experiments/*/TODO.md`, `REPRODUCTION.md` |
| **Session history** | `drafts/conversation-summaries/` (not an active task list) |

---

## Construct (plan open; v1 manuscript parked)

Plan: [`drafts/plans/construct.md`](../drafts/plans/construct.md) (TSA **2.0**: technical construction + social/technical **constructibility**). Papers stay spin-outs. Lean: `ConstructionCrux` / Target Realization in `AlignmentConstruction.lean`. v1 book path remains certification/preservation (ch33), not attractor construction.

- [ ] **Do not include Construction chapters in the v1 manuscript yet.** Site specify/construct cards and the lifecycle card stay. 2.0 outline may proceed; concrete Family B chapters wait on Witness.

  Reviewer bar (2026-08-21) — *concrete* integration requires a Witness-style **fail/refuse**, not denser definitions:

  > the formal apparatus … currently outruns what it can do. … The main vulnerability is not error but unearned weight … a well-organized restatement of the difficulty, plus a correct but small formal toolkit … not yet a contribution to solving it.

  **Later candidates** (after Witness stop; not Witness phases): H5 construction vs certification stop (same episode, two trees); H3/H4 wrong-vacuum / enforcement-collapse protocols. v1 homes if bar met: ch34, ch38, ch48, App. F — **not** a sixth intro claim. 2.0 homes: Part XI / companion per construct plan (Families A–D).

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

Card-notes triage **closed** 2026-08-17 — [`drafts/attic/site-card-notes-triage.md`](../drafts/attic/site-card-notes-triage.md).

- [x] **Guided Tour “read next” from last book page (M).** `/paths/` offers a continue target from the last visited book chapter (visit history + chapter card URLs). Maps onto the active reading path when the chapter matches; otherwise chapter graph, then manuscript order.
- [ ] **Per-part chapter renumbering (display only) (L, high risk).** Do not rename `chNN` files or `\label`s without migration pass.
- [ ] **Submit page notes to site (S).**
- [ ] **Standalone claims publishability review (S).** Cross-ref Outreach.
- [ ] **Add companion site to Substack (S).**
- [ ] **Book map: generate “Also on the site” from book order (S).**
- [ ] **Part hub cards (S).**
- [ ] **ch10 alignment-faking experiment line (M).**
- [ ] **Chapter-end exercises + online quiz (M).**
- [ ] **Quiz distractors too easy (M).** Many wrong options remain near-jokes or obvious misses even after the length-tell pass. Later: rewrite as concept near-misses, then re-run the blind solver protocol (`site/src/content/quiz/BLIND_EVAL.md`) and the length gate. Do not treat the current 211/211 solve as a difficulty certificate.

---

## Outreach board

- [ ] **Standalone publish — agent-discovery / negative-results line (M).** UAD, embedded/lab sims, or negatives methodology piece.
- [ ] **Pairwise researcher-interest matching — Bubble Connector (M+).** Details TBD.

---

## Housekeeping board

- [ ] **Authorship bars — companion site (M).** PDF: `\authbar` on frontmatter, all 48 chapters, and wired appendices. **Site (partial):** section/subsection heading chips synced from `\authbar` keys (`AI` / `GZ+AI` / `GZ`); toggled via Notes panel button (`localStorage`). Still open: image prompts `{AI}`; optional reader legend.

- [ ] **Authorship bars — pagination parity (M, optional).** Per-section mdframed wrappers add ~+30 pp vs unmarked build (1412 → ~1442 after tuning `\Needspace` to frontmatter-only). Accept for now; revisit with margin-overlay approach (bars without boxing text) if page count must match baseline.

- [ ] **`\symbolref` leftovers (S).** RiskGap and unlabeled blocks. Log: `2026-08-05-symboldef-macro.md`.
- [ ] **Eq-chain / informal reading DAG (S).** C12 basin operationalization (ch38); `chapter-informal-edges.yml`; `p_\theta` vs MI `\theta`. `drafts/editorial-guidance-eq-chain-placement.md`.
- [ ] **Consider claims/assumptions ledger automation (S).** Decide YAML source vs manual.
- [ ] **Review U-shaped coordination claim (S).** ch11/ch13 conjectural until downgrade or evidence.
- [ ] **Grounding/safety-case layer completeness review (S).** ch46 eighth layer: derived vs provisional checklist.
- [ ] **Perturbation-recognition crux (S).** ch47 `% TODO[open-crux]:` — bounded answer or downgrade.
- [~] **ch48 inferential coupling / acausal trade (research).** Drafted; threshold calibration and probe-local coordination open.
- [ ] **Inferential-coupling threshold calibration (research).** ch47/ch48 \(\tau_{\mathrm{ac}}\).
- [ ] **Probe-local inferential coordination (research).** ch48 vs ch46 gap or mark unresolved.
- [~] **Notation reconciliation (S).** ⟳ rows in `metadata/notation.md`; C12 basins → also [`spine.md`](../drafts/plans/spine.md) P3; confirm `C_H` vs `C^H_t`.
- [~] **Update-operator ontology audit (M).** Partial 2026-06-28 envelope refactor.
- [~] **Terminology demotion follow-through (M).** `drafts/glossary-term-audit.md`, `drafts/glossary-prose-pass/THIN.md`.
- [~] **Narrative voice consistency (S).** Optional; wire `check_voice.py` into `make check` if desired.
- [ ] **Part-opener illustrations (S).**
- [ ] **Optional: LaTeX PDF CI build test (S).** `.github/workflows/book-pdf.yml`; compile gate only.
- [x] **Strategic advice follow-through — closed.** Remainders in lane plans (`review/strategic-advice-2026-06-28.md`).

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
