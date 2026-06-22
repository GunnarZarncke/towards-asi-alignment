# Full-Book Review — Continuity, Redundancy, Consistency, Completeness

**Date:** 2026-06-22
**Scope:** Whole manuscript (`book.tex`): frontmatter, Parts I–X (ch01–ch44), appendices A–H.
**Status of this document:** Issue list + suggestions only. **No manuscript files were changed.** Nothing here has been executed; this is for human review and editing.

Per-part deep-read working notes (with full line-referenced detail) live in `review/_pass/part-01.md … part-10.md`. This file is the consolidated synthesis. Where an item says "see Part N notes," the granular line numbers are in `review/_pass/part-0N.md`.

---

## 0. Method, and limitations of this review

- **What was read.** `INSTRUCTIONS.md` (the intended formal spine §18, conceptual spine §19, required chapter elements §10, consolidation rules §4.1), `metadata/book.yml`, `frontmatter/*`, `metadata/notation.md`, `metadata/terminology.md`, `metadata/preamble.tex`, all 44 chapter files, all part files, and the appendix stubs. Structural indexes were built for every `\chapter`/`\section`/`\subsection`, every `\label`/`\ref`, every `eq:` label, every `\index`, and the `chapterthesis`/`epigraph`/`decisionbox`/`failurebox` usage.
- **How chapters were read.** Each part (4–5 consecutive chapters) was read in full, in order, by a dedicated reviewer pass so that intra-part flow could be judged on the actual prose, not just headings. The lead pass additionally read every part-to-part boundary (closing + opening passages of adjacent chapters) directly, and did the cross-part formula/notation reconciliation that no single part-pass can see.
- **Known limitations.** (1) The book is ~35,700 lines; this pass prioritized structure, cross-references, formal-object consistency, and narrative flow over line-by-line copy-editing (typos, grammar, citation completeness were only noted opportunistically). (2) `\ref`/`\label` resolution was checked by name-matching, not by a full LaTeX build — a `make pdf` + `make check` is still recommended to catch broken refs and undefined citations mechanically. (3) Bibliographic correctness (whether each `\autocite` key exists and is the right work) was not exhaustively verified. (4) Claims/assumptions/uncertainty ledgers in `metadata/` were not cross-checked against chapter claims.

---

## 1. Executive summary (the few things that matter most)

1. **The book has no written conclusion, and its central synthesis chapter is empty.** ch44 ("Towards Superintelligence Alignment", the final chapter) is a bare template with even its `chapterthesis` left as `[STUB]`. ch39 ("A Safety Case for Superintelligence Alignment"), the chapter the entire Parts I–IX arc converges on, is a 49-line skeleton with every section `[STUB]`. ch43 (bearer persistence / merger / "what cannot be solved technically") and ch33 (multi-agent strategic coupling) are also stubs. See §2.
2. **All eight appendices (A–H) are 4-line stubs**, including the notation reference (appA) and glossary (appF) that the body text repeatedly leans on, and the safety-case template (appG) that ch39 is supposed to instantiate. Several frontmatter pieces are stubs too (preface, dedication, acknowledgements), and the Executive Overview has multiple `[STUB]` blocks. See §2.
3. **The required "What Would Change This View" section is missing or mis-titled in ~26 of 44 chapters** — a systematic required-element gap, concentrated in Parts IV, V, VII, VIII, X and in ch01/ch05/ch24/ch25. The exact heading currently exists *only* in chapters that are otherwise stubs (ch33/ch39/ch43/ch44) plus the Part I–III/VI compliant ones. See §3.
4. **A small set of formal objects is re-derived many times across chapters** instead of being stated once and cross-referenced. The correction chain `W→O→J→D→C→U→A` appears with ~6 chapter-suffixed labels; CCI ~5×; value-bundle response geometry `G_B` ~6×; bundle-inference argmax ~6×; the "seven conserved properties" 3–5×; the CEV contrast 4× in Part VI alone. This is the dominant redundancy theme. See §4.
5. **Several genuine cross-chapter inconsistencies** (not just duplication): the `ΔL` intentional-gain sign convention is inverted between the Introduction and ch21–23; `B` means *capability* in Part III but *value bundle* in Part IV; `G_B` has three different definitions; the "seven conserved properties" lists do not match across ch28/29/31; the parasite-persistence criterion differs between ch10 and ch34; `κ = bpρ/c` is reused for both *cooperativity* and *artifact conductivity*; the pivotal-process notation ch40 attributes to ch35 is absent from ch35. See §5.

The conceptual spine itself is sound and the chapter-to-chapter narrative (where chapters are drafted) generally flows well with explicit "previous/next" transitions. The problems are (a) unfinished landing chapters/appendices, (b) a recurring required-section omission, and (c) duplication/notation drift from chapters being drafted independently without a final reconciliation pass.

---

## 2. Narrative completeness — stubs and undelivered material (highest priority)

### 2.1 Stub chapters (placeholder skeletons)

| Chapter | Lines | `book.yml` | State |
|---|---|---|---|
| **ch44 Towards Superintelligence Alignment** (book conclusion) | 49 | stub | **Empty.** Every section `[STUB]`, including the `chapterthesis`. Only real content is 3 reference citations. The book's closing synthesis does not exist. |
| **ch39 A Safety Case for Superintelligence Alignment** (Part IX synthesis) | 49 | stub | **Empty.** All sections `[STUB]`. This is the convergence point of Parts I–IX; three chapters forward-reference it (ch35 L1009, ch36 L1055, ch38 L709) and they land on a blank page. Does not cite appG. |
| **ch43 Who Still Counts After Transformation** | 94 | stub | Skeleton. Mandated absorbed sections present *by title* ("Merging With Artificial Entities" L34, "What Cannot Be Solved Technically" L48) but bodies are `[STUB]` except ~8 real lines (L53–61). Receives unpaid promises from ch41 (L213, L436) and ch42 (L589). |
| **ch33 Multi-Agent Superintelligence and Strategic Coupling** | 145 | stub | Formal Model (L25–114) is substantive and does absorb cooperation/privacy/opacity + percolation. But Worked Example (L118), Counterexample (L122), and "What Would Change This View" (L126) are bare `[STUB]`s; decision relevance is absent (only `% TODO` L114); inline `[STUB]` at L45. Sits as a near-orphan between ch32 and ch34 (see §6). |

### 2.2 Thin / partially drafted chapters

- **ch05 Assumptions, Scope, and Failure Coverage** (120 lines): meets its Chapter-5-specific mandate (scope, correction-capacity assumption, Turchin audit) but is list-driven and borderline-stub for a manuscript chapter. No failure-mode section, no "What Would Change This View", inline `[Defined]` markers (L56, L109–111), and an unresolved `% TODO[citation]` for the Turchin map (L104) whose attribution is never delivered in the references.
- **ch40 Lethality Stress Test and Open Issues** (160 lines, target 9000 words ≈ ~1,500 words actual): content is real (13-row lethality checklist + 10-item open-problem ledger) and correctly confines Yudkowsky to a checklist, but each table cell is a single phrase with no per-lethality prose; two `% TODO[open-crux]` markers left in committed source (L119, L121); no forward bridge to ch41.

### 2.3 Stub appendices (all eight)

`appA-notation`, `appB-worked-example-agent-boundary`, `appC-value-bundle-inference`, `appD-correction-channel-audit`, `appE-successor-certification`, `appF-glossary`, `appG-safety-case-template`, `appH-research-program` are each 4 lines (`\chapter{...}` + `[STUB]`). High-impact gaps:
- **appA (Notation)** — the body has genuine cross-part symbol clashes (see §5) that an appendix notation table is the natural place to reconcile; it is empty.
- **appF (Glossary)** — INSTRUCTIONS §23.3 requires every core term to be in the glossary; it is empty. (Operational definitions exist in `metadata/terminology.md` and could seed it.)
- **appG (Safety-case template)** — ch39 is meant to instantiate this; both are unwritten (compound gap).

### 2.4 Frontmatter gaps

- **Stub files:** `preface.tex`, `dedication.tex`, `acknowledgements.tex` (4 lines each).
- **`executive-overview.tex`** has `[STUB]` blocks: "Diagram in Words" (L27), the Assumptions list (L32–34), and "What This Book Tries to Establish" (L58). So the up-front synthesis promise is incomplete on the front end, mirroring the empty ch44 on the back end.
- `roadmap.tex` exists but is not included in `book.tex` (intended per INSTRUCTIONS §25 — chapter status moved to `current-status.tex`/`book.yml`). Not a defect; noted to avoid confusion.

### 2.5 Opening promises not paid off by the ending

The Introduction makes five named `introclaim`s (boundary L217, value-bundle L223, correction L231, successor L239, basin L246) and a six-point "Practical Hope" regime (L331–339); the Executive Overview lists five linked preservation problems. **None of these is gathered and discharged at the end**, because ch44 is empty. When ch44 is written it should explicitly revisit and close these five claims.

---

## 3. "What Would Change This View" — systematic required-element gap

INSTRUCTIONS §10 requires every chapter to contain a section titled **exactly** "What Would Change This View" (a renamed equivalent is explicitly only acceptable if retitled). Current state:

**Compliant (exact title, real content):** ch02, ch03 (stale `\label` `sec:shaky-points-...`), ch04, ch06, ch07, ch08, ch09, ch10 (non-standard `\label` `sec:evidence-against-opacity`), ch11, ch12, ch13, ch14, ch26, ch27.

**Exact title but STUB body:** ch33, ch39, ch43, ch44.

**Missing entirely:** ch01, ch05, ch15, ch16, ch17, ch18, ch19, ch22, ch24, ch25, ch28, ch29, ch30, ch31, ch32, ch34, ch35, ch38, ch42.

**Present but mis-titled (rename needed):**
- ch20 "Where the Argument Is Shaky" (L1042)
- ch21 "Limits of the Compression Test" (L919)
- ch23 "The Philosophical Boundary" (L804)
- ch36 "What evidence would update us?" (L1017)
- ch37 "A steelman critic" (L802)
- ch41 "What would update this chapter?" (L490)

This is ~26 chapters missing or mis-titled. Several already contain the right *material* under a different heading (ch17 "Empirical Signatures" is essentially a falsification list; ch29 "Why These Properties Are Not Enough"; ch36/ch37/ch41 as above) and only need retitling/reframing. **Decision needed:** either enforce the exact heading book-wide, or formally bless the prose substitutes as house style and fix the stubs — currently the exact heading exists mostly in the unwritten chapters, which is the worst of both worlds.

---

## 4. Redundancy — over-replicated material and formulas

The book restates a small set of spine objects in many chapters, usually with chapter-suffixed equation labels (`...-chNN`). Some restatement is legitimately pedagogical (chapters are meant to be somewhat self-contained); the items below are where it crosses into true duplication that should be reduced to one canonical statement + `\eqref` cross-references.

### 4.1 The most-replicated formal objects (book-wide)

| Object | Appears in (labels) | Suggested canonical home | Verdict |
|---|---|---|---|
| **Correction chain** `W→O→J→D→C→U→A` | ch02, ch03, ch12, ch14 (`eq:correction-chain`), ch21, ch23, ch24, ch25 (3×), ch26, ch27, ch28, ch29, ch30, ch31 | ch24 (the chapter named for it) | ~10 statements; most should be a one-line reminder + cross-ref. Single biggest duplication in the book. |
| **CCI** `min_i I(X_i;X_{i+1}) − λ_L L − λ_M M − λ_R R − λ_O O` | ch02, ch03, ch21, ch23, ch24, ch25 (3×), ch26, ch27, ch36, ch37, ch38 | ch25 | Also *inconsistent* (see §5.4). |
| **Value-bundle response geometry** `G_B` | ch03, ch14, ch16, ch17, ch19, ch20, ch21, ch22, ch23, ch25, ch28, ch29, ch30, ch31 | ch19 (richest, the `(J,H,C,Φ)` 4-tuple) | Also *inconsistent* (3 definitions, see §5.2). |
| **Bundle-inference argmax** `(B̂,Ŵ,Φ̂)=argmax …` | ch10, ch16, ch20 (2×), ch21, ch22 | ch16 / ch20 | 6×; ch21/ch22 should cross-ref. |
| **Human value-update operator** `V_{t+1}=U_H(V_t,E_t,D_t)` | ch02, ch04, ch15, ch20, ch21, ch23, ch24, ch25, ch26, ch28, ch29, ch31, ch41, ch42 | ch26 | Plus symbol drift `U_t`/`U_H`/`U^H_t` (see §5.7). |
| **Boundary inequality** `I(I_{t+1};E_{t+1}|S_t,A_t)≤ε` | ch01, ch03, ch06, ch07, ch08, ch09, ch10, ch28, ch29, ch31 | ch06/ch07 | Later chapters should recap in ≤2 lines + ref. |
| **Sample-complexity bound** `m = O(k/(ε²(1−γ)²)·log(k/δ))` | ch15, ch16, ch17 | ch17 (fullest treatment) | Stated 3×; ch15/ch16 → cross-ref. |
| **Transport decomposition** `ΔL_T = ΔL_sem+ΔL_bundle+ΔL_bearer+ΔL_corr+ΔL_succ` | ch22, ch23 | ch22 (plain), ch23 (risk-weighted refinement) | Present near-identically twice; keep ch23's weighted version as the delta. |

### 4.2 Repeated taxonomies / argument blocks

- **Seven conserved properties** enumerated in ch28 (§"Conserved properties"), ch29 (canonical), and ch31 (certification domains) — plus a 4th sub-list inside ch31. Also *inconsistent* (see §5.3). Canonical = ch29; ch28/ch31 should quote or explicitly re-package.
- **CEV contrast** ("preserve the update process, don't optimize a guessed `V*`") stated 4× in Part VI alone (ch24, ch25, ch26, ch27 — ch26/ch27 share the section title) and again in ch41/ch42. Canonical = ch26; reduce the rest to a sentence + ref.
- **Legitimacy / governed-change criteria** (truth-contact, agency, plurality, reversibility, non-manipulation, …) in ch04, ch26, ch27, ch41, ch42. Canonical = ch26; ch27/ch41/ch42 keep only their distinct items.
- **Goal-laundering four layers** (semantic/bundle/bearer/correction) in ch10, ch23 (as transport), and ch37 (canonical). ch10's `eq:bundle-laundering`/`eq:bearer-laundering` re-derivation should become a preview + cross-ref to ch37. NB ch36 uses a *competing* four-STAGE model (see §5.9).
- **Self-modeling vs self-transparency** (`d↑, τ↑`, `τ = 1−I(M;M̂)/H(M)`) previewed in ch06, ch08, ch10, ch12, ch14, ch22, ch25, ch28, ch29 before its home chapter ch30. Derive once in ch30; reduce earlier mentions to one-line pointers.
- **False-attractor taxonomy** in ch32 (selection environment) and ch35 (alignment field) — overlapping (compliance/benchmark/reputation) but different referents; ch35 cross-refs ch32 but not vice-versa.
- **Collective-competence / U-shaped coordination** developed in both ch11 (§"Competence and Coordination", §"The U-Shaped Coordination Pattern") and ch13 (canonical). ch11's 402–531 should compress to a forward pointer.
- **Successor-certification schema / safety case** appears in ch28 (six questions + eight-claim case) and ch31 (seven domains + ten-claim case) — same artifact twice; consolidate into ch31.
- **"Local-first path"** preamble repeated in ch31, ch32, ch34, ch35 (distinct lists, but the "global coordination is hard, act where you have leverage" framing is repeated).
- **Composite-agent / "align the loop not the component"** maxim in ch09 and restated as ch38's closing line; ch38 should cite ch09 at its thesis.

### 4.3 Repeated worked examples

Recurring example scenarios used in multiple chapters with the same moral: the **helpful lie / truth-vs-care medical disclosure** (ch04, ch16, ch20, ch21, ch23), the **recommender that makes itself necessary** (ch09, ch10, ch24, ch27), the **market/recommender composite** (ch09, ch10), the **frontier-lab-as-optimizer** (ch07, ch09, ch21, ch22, ch32, ch38), and the **merge/upload "is it progress or loss?" catalogue** (ch18, ch20, ch22, ch23, ch41, ch42, ch43). Keep one canonical instance of each and have the others cross-reference rather than re-establish the setup.

### 4.4 Intra-chapter / structural duplication worth noting

- **ch12** carries both a "Conclusion" (L1199) and a "Chapter summary" (L1235); **ch42** likewise (Conclusion L680 + Chapter summary L697).
- **ch23** opens with a "Chapter Summary" section at the *top* (L15) and ends with a "Chapter Conclusion" (L899) — the only chapter that summarizes up front.
- **ch22** states `ΔL_transport` three times within the single chapter (L47, L232, L679).
- **ch25** states the correction chain three times and CCI three times within the chapter.
- **Epigraph duplicates `chapterthesis` verbatim** in several chapters (e.g. ch06, ch15, ch20, ch26) — the boxed thesis and the epigraph beneath it are the same words.
- **`decisionbox`/`failurebox`/`assumptionbox`/`formalbox`/`examplebox`** environments are defined in `metadata/preamble.tex` but **used by no chapter** (chapters use plain `\section`s). Either adopt them or drop them; meanwhile "Decision relevance" as a required element is satisfied via prose, and is genuinely thin/late in a few chapters (ch06, ch15, ch20).

---

## 5. Consistency — genuine cross-chapter inconsistencies (not just duplication)

These are correctness issues a careful reader will trip over; they should be reconciled (ideally pinned down once in `appA-notation`).

1. **`ΔL` intentional-gain sign/convention is inverted.** Introduction (L139–147): `ΔL = L_mechanistic − L_intentional + λ DL(R)`, framed as "earns its keep when it saves bits" (L = description length, lower better). ch21 (`eq:intentional-gain-simple`, L55–63): `ΔL_int = L(M_int|X) − L(M_mech|X) − λ DL(G)` with L declared "log evidence/predictive score" (higher better) and `ΔL_int>0` = intention wins. ch22/ch23 follow ch21. INSTRUCTIONS §18.7 gives yet a third ordering. The two L-term order *and* the sign of the `λDL` penalty differ; a reader carrying the Intro formula into ch21 reads every inequality backwards. **Pick one convention book-wide** (state whether L is bits or log-evidence) and fix the Introduction or add a reconciling footnote at `eq:intentional-gain-simple`.
2. **`G_B` defined three ways:** ch16 `(∇_B log π, ∇²_B log π)` (gradient+Hessian); ch17 gradient field only; ch19 `(J,H,C,Φ)` 4-tuple. Same symbol, three referents. Declare ch19 canonical; have ch16/ch17 cross-ref or use distinct symbols for their partial objects. Related: the "interaction curvature" is `∂²π/∂B∂B` (ch15), `T_ij` on `log π` (ch16), `H_ij` on `μ_π` (ch19) — three names/operators.
3. **"Seven conserved properties" lists do not match.** ch29 (canonical): boundary closure · memory lineage · value-bundle response geometry · bearer-map continuity · correction-channel capacity · transparency/self-transparency · control-locus continuity. ch28's invariant profile splits correction into two members (`U_H` and CCI) and *drops* control-locus. ch31's certification domains *add* competence/growth-rate and successor-closure and *drop* memory-lineage and control-locus (and a 4th sub-list in ch31 swaps in operating-envelope inheritance). The text calls all of these "the seven." Declare ch29 canonical and make ch28/ch31 quote it or explicitly state they re-package it.
4. **CCI penalty terms inconsistent.** ch24: five penalties incl. Goodhart `λ_G G`, ontology `O_mis`, capacity `C_raw`. ch25 (the "integrity" chapter): four penalties, drops Goodhart, renames ontology `Ω`, capacity `C_corr` — even though ch25 has a whole "Goodharting the Correction Channel" section. ch26/ch27/ch23/ch36/ch37/ch38 each pick a 4-term variant with the ontology term written `O_mis`/`Ω`/`O_mismatch` and capacity `C_raw`/`C_corr`/`min_i I`. Pick one canonical functional (decide Goodhart in/out; one symbol for ontology; one for capacity).
5. **`B` symbol clash across parts.** `B` = capability/boundary-information (the "bitwise-IQ" competence functional) in Part III (ch11–13), but `B` = value-bundle activation vector in Part IV+. ch14 already side-steps this by renaming the functional `K`, which then breaks consistency with ch11–13 and the spine. Fix once (rename one of the two objects, or add a prominent notation note at the Part IV opening).
6. **Residual-surprise glyph drift:** `S_X` (ch11/12) vs `S^(i)` (ch13) vs `\mathcal{S}` (ch14). And `η` is overloaded in ch11 (growth efficiency *and* coordination efficiency). And collective-competence gain/loss is `B_coord`/`C_friction` (ch11) vs `G_coord`/`Ω_coord` (ch13).
7. **Value-update operator + value-state tuple have ~4 forms each.** Operator: `U_t` (ch15), `U_H` (ch17/18/26/42), `U^H_t` (ch41/Intro). Value-state tuple: `(B_t,Φ_t,U^H_t)` (Intro), `V_t=(B,W,Φ,U^H,C^H)` (ch04, 5-tuple), `V_t=(B_t,W_t,Φ_t)` (ch41, 3-tuple roman), `𝒱_t=(B_t,W_t,Φ_t,U_t)` (ch42, 4-tuple calligraphic). Reconcile.
8. **`Φ` overloaded inside ch17:** bearer map `Φ_j` (L449, L610) vs feature matrix `Φ∈ℝ^{N×n}` (L358) in the same chapter. Rename the feature matrix. Bundle dimension symbol also drifts: `k` (ch16/17/19) vs `m` (ch18).
9. **Goal-laundering: four LAYERS vs four STAGES.** ch37 layers = semantic / **bundle** / bearer / correction; ch36 stages = semantic preservation / **proxy substitution** / bearer narrowing / correction capture. Both are presented as "the four", second item differs. Align ch36 to ch37's names (or drop ch36's competing list). Also the laundering index (ch37 GLI) vs goal-laundering signature (ch10) are never reconciled.
10. **Parasite-persistence criterion differs.** ch10 (matches the spine): `C_X < H(A_Y) − λ_Y H(I_Y)/β`. ch34: `C_H < H(A_Y) + K_Y − L_Y` (camouflage `K_Y`, maintenance `L_Y`). Two non-matching formalizations of the same phenomenon; also host-capacity symbol `C_X` vs `C_H`. Pick one or add a bridging note.
11. **`κ = bpρ/c` overloaded.** Used for *cooperativity index* (ch10/ch13 canonical/ch33) and for *artifact conductivity* `κ_ij(a)` (ch35). Meanwhile ch34 defines artifact conductivity a *different* way: `χ(A,H)=I(R;D_H|A)−I(R;D_H)`. So "artifact conductivity" itself has two formal definitions (ch34 χ vs ch35 κ(a)), and κ means two different things. Reconcile or cross-ref explicitly. (Also: ch13 re-derives κ without crediting ch10's earlier definition; ch33 cites Hamilton but not ch13's canonical `eq:kappa-coordination`.)
12. **Pivotal-process notation `B_race → B_certified-deployment` is in ch40 but not ch35.** ch40 (L56, comment L117) attributes the formalization to ch35, but ch35 uses `B_align`/`S_align`/`C_certified` and never states `B_race → B_certified-deployment`. Add it to ch35 or fix ch40's pointer.
13. **Bundle example-list drift.** The candidate-bundle roster gains/loses members across chapters: +Learning/Legacy (ch15), +legitimacy (ch28), +prudence (ch29), +protection (ch30), +truth-contact (ch31), vs the ch16 catalogue. Align to ch16's canonical roster.
14. **Bib-key inconsistency:** Critch "boundaries" cited as `critch2022boundaries` (ch28) and `critch2022boundaries3a` (ch29/ch31). Verify `.bib` and unify.
15. **`\MI` macro not used uniformly:** ch02 writes raw `I(...)` for mutual information where the rest of Part I uses the `\MI` macro.
16. **Capacity vs integrity used loosely:** "correction-channel capacity" (`C_corr`) and "correction-channel integrity" (CCI = capacity − penalties) are sometimes used interchangeably (ch28/ch29/ch31).

### 5.1 Style consistency (lower severity but pervasive)

- **Section-title capitalization is split book-wide.** Title Case: most of Parts I–III/VI/VII-ch29, ch33/34. Sentence case: ch02, ch04, ch06 (internally mixed), ch09, ch12, ch15, ch28, ch30, ch31, ch35, ch36–38, ch41, ch42. Pick one convention.
- **Chapter-ending heading is named ≥6 ways:** "Summary", "Chapter Summary", "Chapter summary", "Conclusion", "Chapter Conclusion", "Chapter conclusion" — and some chapters carry both a Conclusion and a Chapter summary (ch12, ch42). Standardize (the de-facto majority is "Summary").
- **`\section` vs `\section*` for the summary** is inconsistent (e.g. ch09 uses unnumbered `\section*{Chapter summary}`).
- **Epigraph style/usage:** `\epigraph{...}{}` (most), `\begin{quote}` (ch02), none (ch05, ch33, ch39, ch40). Empty attribution braces throughout (cosmetic). Several epigraphs duplicate the chapterthesis (see §4.4).
- **WWCTV `\label` convention** broken in places even where the title is right: ch03 `sec:shaky-points-...`, ch10 `sec:evidence-against-opacity` vs the `sec:wwctv-*` convention elsewhere.
- **Inline editorial markers left in manuscript prose:** `[STUB]`, `[Defined]`, `[Conjectural]`, `[Philosophical limit]`, `[Claim]`, `[Open]` appear in body text in ch05, ch33, ch40, ch43, ch44 (and as a deliberate maturity-label convention in ch40/ch33 summaries). Decide whether the bracket-status convention is book-wide or should be removed from prose.

---

## 6. Continuity — flow and cross-references

**What works:** The conceptual spine (INSTRUCTIONS §19) is followed, and most chapters carry explicit "the previous chapter… / the next chapter…" transitions. The part boundaries I→II, II→III, III→IV, IV→V, V→VI, VI→VII, VII→VIII, VIII→IX all have clean, explicit hand-offs (verified directly). Percolation is handled well: ch13 is canonical and ch33/ch35 explicitly inherit it rather than re-deriving.

**Continuity defects:**

1. **ch33 is a narrative near-orphan.** It has no outgoing "next chapter" sentence and ch34 opens from the correction chapters, not from ch33; combined with ch33's stub sections, a reader going ch32→ch33→ch34 hits a dense-but-skeletal interlude with no bridges on either side. (Completeness + continuity.)
2. **ch20 → ch21 hand-off is wrong.** ch20's closing (L1100–1102) says the next chapter is goal transport (`ch:goal-transport` = ch22), skipping ch21 ("The Compression Test for Intention"). Point it at ch21.
3. **ch12 L20 broken/mis-pointed `\ref`.** "Chapter~\ref{ch:finding-boundary} introduced predictive and control information across the boundary, discounted by memory cost and residual surprise" — that competence functional is introduced in ch11 (immediately previous), not ch7. Almost certainly should be `\ref{ch:capability-without-task-ontology}`.
4. **ch40 → ch41 (Part IX→X) has no bridge.** ch40 ends at references with no forward sentence; ch41 opens cold. Add a bridge (properly, from a written ch39 summary).
5. **ch24 silently re-derives ch23's material.** ch23's "Correction Transport" already states the same chain + CCI; ch24 opens by redefining them without acknowledging ch23. Decide whether correction machinery is *introduced* in Part V (and deepened in VI) or *named* in V and *introduced* in VI, and make the cross-refs match. Related: the ch24/ch25 division of labor is blurred (~30–40% conceptual overlap — both define the chain, CCI, the bottleneck MI walk, the strong channel, CEV, failure modes, the audit list). Recommend a sharper split (ch24 conceptual, ch25 operational) rather than a merge.
6. **Value machinery used before defined.** ch10 uses `B, W, Φ` (bundle/bearer) before any definition (Part IV); ch12/13/14 use `Φ`, `B_k`, the correction chain before Part IV/VI. Mostly acknowledged at chapter ends, but a forward `\ref` at first use would stop a sequential reader being stranded.
7. **`ch:goal-transport` self/forward refs** in ch28 (L413) and ch18 (L1214) should be verified to resolve to ch22 in a build (goal transport is also developed *inside* ch28, so the cross-ref risks looking self-referential).
8. **Parts have no introductory prose.** Each `parts/partNN-*.tex` is just `\part{...}` + `\input`s. A 1-paragraph part opener (what this part adds, which chapters, what it assumes) would smooth the larger arc; optional but worth a decision.
9. **Orphaned construct:** ch30's selfhood bottleneck `β_self = I(G_t;S_t)/H(G_t)` is introduced and cited but not used downstream (ch31 doesn't consume it). Either tie it into certification or mark it exploratory.
10. **Missing one-directional cross-refs:** ch38 thesis should cite ch09 (composite agent); ch36 §"Cross-scale measurement" should forward-ref ch38; ch37 should cite ch10's laundering signature and ch23's transport stack; ch32 should forward-ref ch35's false attractors.

---

## 7. Per-part pointers (detail lives in `review/_pass/`)

- **Part I (ch01–05)** — `review/_pass/part-01.md`. Arc coherent; ch03 is a heavy preview that re-derives downstream objects; ch01 & ch05 lack WWCTV; ch05 thin + Turchin citation undelivered; `I_t/E_t/D_t/C_t` symbol clashes; ch02 sentence-case + raw `I(...)`.
- **Part II (ch06–10)** — `part-02.md`. Structurally strong; boundary-leakage symbol differs per chapter (`\ell`/`\mathcal{R}`/`\mathcal{L}_B`) and `\mathcal{R}` is overloaded; **ch10 front-runs four later chapters** (goal laundering→ch37, bundle/bearer inference→ch20/21, parasites→ch34, self-modeling→ch30).
- **Part III (ch11–14)** — `part-03.md`. Well-sequenced; `B`→`K` functional rename, `B` capability-vs-bundle clash, residual-surprise glyph drift; ch11 coordination sections duplicate ch13; ch12 L20 broken ref; "correction vs coordination" denominator drift in the key claim.
- **Part IV (ch15–19)** — `part-04.md`. **All five lack WWCTV**; sample-complexity argument 3×; `G_B` three definitions; `B` cross-part clash; `Φ` feature-matrix-vs-bearer clash in ch17; candidate-bundle catalogue re-listed; flags ch18↔ch43 overlap.
- **Part V (ch20–23)** — `part-05.md`. **Highest-redundancy part**; ΔL sign inconsistency vs Intro; correction chain/CCI/`U_H` imported from Part VI; G_B and bundle-inference restated 4× in-part; ch20→ch21 broken hand-off; three near-duplicate inference pipelines; ch23 front-summary + tail-conclusion.
- **Part VI (ch24–27)** — `part-06.md`. ch24 & ch25 lack WWCTV; CCI penalty-term inconsistency; CEV contrast 4×; ch24/ch25 blurred division of labor; six-vs-four-level correction taxonomy; "governed vs ungoverned" coda repeated in 3 chapters.
- **Part VII (ch28–31)** — `part-07.md`. **All four lack WWCTV**; the "seven conserved properties" disagree across ch28/29/31; B/Φ re-introduced 4×; ch28 over-previews ch29; ch28 & ch31 carry duplicate certification safety-cases; `critch2022boundaries` bib-key split; bundle example-list drift.
- **Part VIII (ch32–35)** — `part-08.md`. **ch33 is a stub** (orphan seam ch32→ch33→ch34); ch32/ch34/ch35 lack WWCTV; parasite-persistence criterion diverges (ch10 vs ch34); artifact conductivity defined two ways (ch34 χ vs ch35 κ(a)); pivotal-process notation missing from ch35; false-attractor overlap ch32↔ch35; ch35 sentence-case outlier.
- **Part IX (ch36–40)** — `part-09.md`. **ch39 stub is the load-bearing failure** (+ appG stub); ch40 thin with inline TODOs; WWCTV only in the stub ch39; goal-laundering triplicated (ch10/ch23/ch37) and ch36 uses a competing four-stage model; CCI base term differs across ch36/37/38; ch40→ch41 seam unmarked. (ch40 *does* correctly confine Yudkowsky to a checklist.)
- **Part X (ch41–44)** — `part-10.md`. **ch43 stub, ch44 empty — the book has no real conclusion**; ch41↔ch42 heavily duplicate (value-state tuple, CEV section, `S_correctable`, minimal safety principle, failure-mode list, two 7-item criteria lists); ch41 mis-titles WWCTV, ch42 lacks it; value-state tuple has 4 notations; intro's five claims never discharged.

---

## 8. Prioritized action list (suggestions — not executed)

**Tier 1 — completeness (the book is not finishable without these):**
1. Write **ch44** (conclusion) — synthesize and discharge the Introduction's five claims + Executive Overview preservation problems + "Practical Hope" regime.
2. Write **ch39** (safety-case synthesis) and **appG** (safety-case template) together; have ch39 ingest ch36/37/38 + Parts I–VIII claims.
3. Write **ch43** (bearer persistence; deliver the two absorbed sections) and build out **ch33** (worked example, counterexample, WWCTV, decision relevance, bridges).
4. Flesh out **ch05** and **ch40** to manuscript depth; resolve their inline `% TODO`s and the Turchin citation.
5. Write the **appendices A–H** (at minimum appA notation and appF glossary, seeded from `metadata/notation.md` and `metadata/terminology.md`) and the **frontmatter stubs** (preface, dedication, acknowledgements) and the Executive-Overview `[STUB]` blocks.

**Tier 2 — required-element + correctness:**
6. Add/retitle the exact **"What Would Change This View"** section in the ~26 chapters that miss or mis-title it (decide the policy first; §3).
7. Reconcile the **cross-chapter inconsistencies** in §5 — especially the ΔL sign convention (1), `G_B` (2), the seven conserved properties (3), CCI penalty terms (4), the `B` capability/bundle clash (5), the parasite-persistence criterion (10), and the κ/artifact-conductivity overload (11). Record the canonical notation in **appA**.
8. Fix the broken/mis-pointed cross-refs: **ch20→ch21** hand-off, **ch12 L20** ref, **ch40→ch41** bridge, **ch40↔ch35** pivotal-process pointer. Run `make pdf` + `make check` to catch any remaining undefined refs/citations mechanically.

**Tier 3 — redundancy + style:**
9. De-duplicate the over-replicated objects in §4: pick a canonical home for the correction chain (ch24), CCI (ch25), `G_B` (ch19), bundle inference (ch16), the seven properties (ch29), CEV (ch26), sample complexity (ch17), and the self-modeling derivation (ch30); reduce the rest to one-line reminders + `\eqref`/`\ref`. Sharpen the ch24/ch25 and ch28/ch31 divisions; trim ch11's coordination sections into ch13; consolidate the merger treatment into ch43.
10. Standardize style: section-title capitalization, chapter-ending heading name (→ "Summary"), `\section` vs `\section*`, epigraph usage (and stop epigraphs duplicating the chapterthesis), the `sec:wwctv-*` label convention; decide on/remove the unused `decisionbox`/`failurebox` environments and the inline `[Defined]`/`[STUB]` bracket markers in prose; consider 1-paragraph part openers.
