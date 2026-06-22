# Review Pass — Part II: "Agents, Boundaries, and Real Optimizers" (Chapters 6–10)

Reviewer pass over `parts/part02-agents-boundaries.tex` and chapters ch06–ch10, read in full and in order.
Scope: required-element compliance, continuity, redundancy, consistency, dangling threads, and Part-level hand-off.
No manuscript files were edited.

Files reviewed:
- `chapters/ch06-agent-without-anthropomorphism.tex` (759 lines)
- `chapters/ch07-finding-boundary.tex` (1071 lines)
- `chapters/ch08-grow-split-merge.tex` (1161 lines)
- `chapters/ch09-composite-agent.tex` (774 lines)
- `chapters/ch10-strategic-opacity.tex` (886 lines)
- Context: `chapters/ch05-...` (end), `chapters/ch11-...` (start), `parts/part02-agents-boundaries.tex`

---

## PART-LEVEL SUMMARY

Part II is structurally sound and largely complete: all five chapters carry `\chapter` + `\label{ch:...}`, a `chapterthesis` environment, a `refsection` with a closing `\printbibliography[heading=subbibliography,...]`, at least one failure-mode/counterexample section, and a section titled **exactly** "What Would Change This View." There are **no `[STUB]`/`[TODO]`/`[Conjectural]` markers** in any of the five chapters (the only `% TODO` lives in ch05, out of scope).

The two systemic problems are:

1. **Notation drift for the single most important object in the Part** — the boundary-leakage / boundary-residual quantity gets a different symbol in every chapter (`\ell`, `\mathcal{R}`, `\mathcal{L}_B`), and `\mathcal{R}` is overloaded across chapters (residual / reproduction operator / responsibility capacity / control reach). See §E.
2. **ch10 front-runs four later chapters.** Goal laundering (ch37), value-bundle/bearer inference (ch20/21), self-modeling vs self-transparency (ch30), and parasite persistence (ch34) are each developed at length in ch10 with their own formal apparatus. This is exactly the premature-introduction risk flagged in the brief. See §D.

Section-title capitalization is inconsistent **across** chapters (ch07/08/10 Title Case; ch09 sentence case; ch06 internally mixed), and the chapter-ending section is named four different ways. See §E.

Flow ch06→ch10 is good and explicitly stitched; the hand-off into ch11 is clean. The hand-off from Part I (ch05) is thematic rather than explicit.

---

## CHAPTER 6 — `ch:agent-without-anthropomorphism` "What Is an Agent Without Anthropomorphism?"

### A. Capsule
An agent is not a person-like thing but a bounded control process: a partition of variables into internal/sensory/active/external states with approximate boundary closure, memory, action, and goal-as-compression. Establishes the operational agent definition and the core boundary inequality used throughout the book.

### B. Required-element compliance
- `\chapter` + `\label{ch:agent-without-anthropomorphism}`: present (lines 1–2). ✓
- `chapterthesis`: present (4–7). ✓
- Decision-relevance early: **thin early, strong late.** The opening is definitional; explicit decision content ("what to measure," the question list) only arrives at 643–651 and the agency-risk product at 388–400. Consider surfacing a decision cue earlier.
- Failure-mode/counterexample: "Boundary errors" (523, four sub-errors). ✓
- "What Would Change This View": present, exact title (718), label `sec:wwctv-agent-without-anthropomorphism`. ✓
- Summary: present but titled **"Chapter conclusion"** (732) — see §E naming inconsistency.
- `refsection` + `\printbibliography[...]`: present (9, 756). ✓
- Stub/TODO markers: none.

### C. Continuity
- Opens Part II cold (no explicit "previous chapter" link), which is acceptable for the first chapter of a Part. Connects back to Part I only via `\ref{ch:wrong-object}` in the references note (754).
- Ends with explicit forward refs to ch07 and ch08 (628–629) and to "later chapters" on value bundles/correction (630). ✓

### D. Redundancy
- The boundary inequality (149–153) and the four-part partition (131–141) are **re-derived** in ch07 (138–158), ch08 (70–84), ch09 (54–84), and recapped in ch10 (22–27). ch06 is the legitimate first home — **keep**; the later re-derivations are the duplication (see those chapters).
- Memory formula `\Delta_m(k)` (227–234) reappears nearly verbatim in ch07 (524–529) and ch08 (319–324). **First home; keep here.**
- "Selfhood and agency" (563–606) introduces recursive depth `d` and opacity `\tau` — these are **re-introduced almost identically in ch10** (524–533). See ch10 §D. Decide on a single home; given ch30 owns self-modeling, ch06's treatment should arguably be the short version and ch10 should cross-ref.

### E. Consistency
- **Section-title capitalization is internally mixed.** Title Case: "Building the Definition from Variables" (111), "Degrees and Scales of Agency" (343), "Two Examples: A Firm and an AI Service" (449). Sentence case: "The need for a colder definition" (16), "Boundary errors" (523), "Selfhood and agency" (563), "From agent detection to alignment target" (607), "Chapter conclusion" (732). This single chapter mixes both conventions.
- Leakage symbol introduced here as `\ell(C)` (365, 668) and the agency score as `\mathcal{A}(C)` (353). `\ell` for leakage is fine but is **not** the symbol ch07 (`\mathcal{R}`) or ch09 (`\mathcal{L}_B`) use for the same thing.
- Epigraph (12–14) duplicates the `chapterthesis` (5–6) almost word-for-word. Minor.

### F. Open tangents / dangling promises
- "Later chapters replace scalar goals with value-bundle geometry and replace obedience with correction-channel integrity" (630) — forward promise, resolved in Parts III/IV. Acknowledged.
- Wentworth agent-structure problem flagged as "left open here on purpose" (334) — intentional, fine.

---

## CHAPTER 7 — `ch:finding-boundary` "Finding the Boundary"

### A. Capsule
Boundary discovery is the first operational alignment step: from raw variables, infer a candidate partition whose boundary residual is low, then test predictive/control relevance, memory, continuity, and adversarial robustness. Establishes the boundary-residual objective, leaky/non-stationary boundaries, and a 7-step discovery procedure.

### B. Required-element compliance
- `\chapter` + `\label{ch:finding-boundary}` (1–2). ✓
- `chapterthesis` (4–7). ✓ Note: thesis "The first alignment error is often not a wrong value, but a wrong object" thematically **echoes ch01 "The Wrong Object"** — see §G.
- Decision-relevance: strong (stop conditions 982–1001, evidence grading 921–951, boundary-map artifact 953–980). ✓
- Failure-mode/counterexample: "Boundary Errors" (601, false positive/negative/too narrow/too wide/wrong scale). ✓
- "What Would Change This View": exact title (1028), label `sec:wwctv-finding-boundary`. ✓
- Summary: "Summary" (1042). ✓
- `refsection` + `\printbibliography` (9, 1068). ✓
- Stub/TODO markers: none.

### C. Continuity
- Opens with explicit link to ch06 (18–22). ✓
- No explicit forward-ref to ch08 at the close; the Summary (1042–1062) ends generically. Minor — ch08 picks up the thread itself.

### D. Redundancy
- **"Adversarial Boundary Discovery" (675–761) substantially pre-stages ch10.** Perturbation tests (695–710), stress windows (724–744), and control-locus continuity (746–761) are all developed again as the spine of ch10. Most striking: ch07's "declared rationale changes / control objective remains invariant" (716–719) is the **same idea and nearly the same wording** as ch10's "surface rationale changes, but control trajectory remains invariant" (269–272). **Trim/cross-ref:** ch07 should foreshadow adversarial discovery briefly and defer the machinery to ch10, or ch10 should explicitly build on this section rather than restate it.
- Control-locus continuity defined here (746–761), again in ch08 (761–772), again in ch10 (274–311). Three homes for one concept.
- Memory contribution `\Delta_m(k)` (524–529) duplicates ch06 (227–234). **Keep one; cross-ref the other.**
- "Boundary Discovery in Composite Systems" (552–599) overlaps ch09 (the dedicated composite chapter) and ch08's responsibility-gap material. Pedagogically defensible as a preview — **keep, but add an explicit "developed fully in ch09" pointer.**

### E. Consistency
- Section titles consistently Title Case throughout. ✓ (internally consistent)
- Boundary residual symbol is `\mathcal{R}(C)` (197, 463) — **clashes** with ch06 `\ell` and ch09 `\mathcal{L}_B` for the same quantity, and with ch08's `\mathcal{R}` (reproduction operator) / `\mathcal{R}_i` (responsibility) and ch09's `\mathcal{R}_C` (control reach). This is the central notation problem of the Part.
- `\epsilon` for tolerated leakage used consistently with ch06. ✓

### F. Open tangents / dangling promises
- "Later chapters will define competence as predictive and control information across the boundary..." (487–489) — **resolved in ch11** (chapterthesis 4–7). ✓ Good closed loop.
- "Later chapters will upgrade scalar goal inference to value-bundle inference" (796–799) — forward to ch20/21. Acknowledged.

---

## CHAPTER 8 — `ch:grow-split-merge` "Agents That Grow, Split, and Merge"

### A. Capsule
Agent identity is transport of conserved control-relevant properties across transformation, not a fixed variable set. Develops the identity vector, transport loss, growth/development/splitting/merging, and a transformation-aware certification schema.

### B. Required-element compliance
- `\chapter` + `\label{ch:grow-split-merge}` (1–2). ✓
- `chapterthesis` (4–7). ✓
- Decision-relevance: strong (certification schema 995–1046, safe-split condition 455–460). ✓
- Failure-mode/counterexample: "Failure Modes of Moving Boundaries" (853, seven modes) + "Counterexamples and Edge Cases" (1048). ✓
- "What Would Change This View": exact title (1113), label `sec:wwctv-grow-split-merge`. ✓
- Summary: "Summary" (1126). ✓
- `refsection` + `\printbibliography` (9, 1158). ✓
- Stub/TODO markers: none.

### C. Continuity
- Opens with explicit link to "previous chapters" (19). ✓
- Forward refs to "later chapters" for value/correction (168, 801, 1045, 1148). ✓
- The identity vector `\Xi` (143–166) is introduced here and **reused as the backbone of ch09's preliminary alignment condition** — good continuity.

### D. Redundancy
- Boundary inequality re-derived (70–84) — recap of ch06/ch07. **Keep (pedagogical), brief.**
- "Growth of Self-Modeling" (335–361), with the self-control-vs-correction asymmetry (354–359), **overlaps ch06's selfhood section and ch10's self-modeling-vs-transparency section.** Three statements of the same `d\uparrow/\tau\uparrow` danger and the same asymmetry inequality (ch08 354–359 ≈ ch10 552–559 ≈ ch06 588–602). **Trim/cross-ref.**
- "Composite Agents and Responsibility Gaps" (661–716) overlaps ch09's "Composite boundaries and responsibility" (414–456). ch08 frames it via `\mathcal{R}_i` responsibility capacity; ch09 via intervention leverage `\Lambda`. Related but not identical — **keep, but cross-ref to avoid the reader feeling the two chapters re-litigate responsibility.**
- Merge gain `\Gamma_{merge}` (571–582) and ch09 composite surplus `\Sigma(C)` (183–192) are close cousins (both MDL-difference "whole > parts" tests). Worth a one-line note that they are the same diagnostic in two notations.

### E. Consistency
- Section titles consistently Title Case. ✓ (internally consistent)
- Leakage symbol reverts to `\ell(C_t)` (78–84) — matches ch06, **differs from ch07/ch09.**
- `\mathcal{R}` is used for the **reproduction operator** (535) and `\mathcal{R}_i` for **responsibility capacity** (671), while ch07 used `\mathcal{R}` for the **boundary residual**. Symbol overload across the Part.
- Equation labels are clean and consistently `eq:...`.

### F. Open tangents / dangling promises
- "Later chapters will fill in value-bundle transport, correction-channel capacity, and adversarial measurement" (1044–1046) — forward to Parts III/IV. Acknowledged.
- Pando problem (521) and shutdown problem (834) cited as live tensions — appropriate, not dangling.

---

## CHAPTER 9 — `ch:composite-agent` "The Real Agent May Be Composite"

### A. Capsule
The effective optimizer may be a composite spanning models, tools, users, memory, institutions, and feedback. Defines composite agency via boundary closure + control relevance + intentional compression + composite surplus, shows six ways local alignment fails under embedding, and states a preliminary composite alignment condition.

### B. Required-element compliance
- `\chapter` + `\label{ch:composite-agent}` (1–2). ✓
- `chapterthesis` (4–7). ✓
- Decision-relevance: strong (intervention leverage 436–454, red flags 625–688, preliminary condition 458–500). ✓
- Failure-mode/counterexample: "Red flags for composite misalignment" (625) + "Counterexamples and boundary discipline" (689). ✓
- "What Would Change This View": exact title (750), label `sec:wwctv-composite-agent`. ✓
- Summary: titled **"Chapter summary"** and **unnumbered (`\section*`)** (763) — inconsistent with the numbered `\section{Summary}` of ch07/08/10 and the numbered `\section{Chapter conclusion}` of ch06. See §E.
- `refsection` + `\printbibliography` (9, 771). ✓
- Stub/TODO markers: none.

### C. Continuity
- No explicit "previous chapter" link in the opening section (15–49); the back-reference appears later at 722 ("The previous chapters developed agents as dynamically bounded systems that can grow, split, and merge"). **Weaker opening transition** than ch07/ch08/ch10 — consider a one-line bridge near the top.
- Uses ch08's transport relation `T_{t\to t+1}(C_t)\sim C_{t+1}` with explicit `\ref{ch:grow-split-merge}` (551–553). ✓
- Forward: "This principle will recur throughout the rest of the book" (741) + value/correction forward refs (742–745). ✓

### D. Redundancy
- Boundary closure + control + intentional compression (99–169) **re-derives the ch06/ch07 apparatus** a fourth time. The four-role partition (61–71) and boundary inequality (73–84) restate ch06/ch07. Because this is the dedicated composite chapter, **keep**, but the re-derivation could be compressed with a pointer to ch06.
- The detection procedure (568–616) parallels ch07's 7-step procedure (359–516) and ch10's adversarial decomposition (412–450). Three "first-pass procedures." ch09's is composite-specific — **keep, cross-ref ch07.**
- The four worked examples (215–313: assistant+tools, model+user, lab+benchmark, market+recommender) overlap ch10's three examples (661–714: bureaucracy, market, disposable-instance AI). The market/recommender example in particular appears in **both** ch09 (297–313) and ch10 (681–698). **Keep ch09's (value-shaping framing) and trim ch10's to a cross-ref**, or vice versa.
- Goodhart pressure `dm/dt>0` while `dB/dt<0` (359–365) anticipates ch20/21 value-bundle erosion; here it is appropriately brief. Keep.

### E. Consistency
- **Section titles are sentence case throughout** ("The object-level mistake," "From named objects to dynamical composites," "Composite agency," "Four examples," "Why local alignment is not enough"...). This is internally consistent but **opposite to ch07/ch08/ch10's Title Case.** One of the two conventions should win Part-wide.
- Leakage symbol is `\mathcal{L}_B(C)` (75–84) — a **third** symbol for the same quantity (`\ell` in ch06/ch08, `\mathcal{R}` in ch07).
- Control reach `\mathcal{R}_C(k)` (122–124) reuses `\mathcal{R}`, which ch07 used for residual and ch08 for reproduction/responsibility. Overload.
- "Chapter summary" is the **only** `\section*` (unnumbered) chapter-ending in the Part; all others are numbered.

### F. Open tangents / dangling promises
- `\mathrm{CCI}` (correction-channel integrity) used at 493–495 and labeled "defined later in the book." Forward-ref; **also used in ch10** (637–639) the same way. Both are honest forward refs, but two chapters use a symbol defined neither here nor in ch10 — worth a one-line "defined in ch[NN]" anchor once available. See §G.

---

## CHAPTER 10 — `ch:strategic-opacity` "Agency Under Strategic Opacity"

### A. Capsule
When a system can benefit from being overlooked, agency discovery becomes adversarial: alignment fails when control becomes more coherent than correction can see. Develops cooperativity `\kappa`, selective opacity, adversarial decomposition, a battery of adversarial tests, and decision triggers.

### B. Required-element compliance
- `\chapter` + `\label{ch:strategic-opacity}` (1–2). ✓
- `chapterthesis` (4–7). ✓
- Decision-relevance: very strong ("Decision Triggers" with stop/start/continue conditions, 772–812; adversarial tests 576–660). ✓
- Failure-mode/counterexample: "Failure Modes of This Chapter's Approach" (814, false pos/neg, ontology lock-in, Goodharting). ✓
- "What Would Change This View": exact title (716), **but label is `sec:evidence-against-opacity`** — breaks the `sec:wwctv-*` label convention used by ch06–ch09. Cosmetic but a real inconsistency. The content is framed as "negative indicators / when to decrease confidence" rather than "what would overturn the thesis"; valid, but stylistically diverges from the other four WWCTV sections.
- Summary: "Summary" (854). ✓
- `refsection` + `\printbibliography` (9, 883). ✓
- Stub/TODO markers: none.

### C. Continuity
- Opens with explicit link to "previous chapters" + recap of the boundary inequality (19–32). ✓
- **Excellent hand-off to ch11** (876–877): "The next chapters turn from opacity to capability... how fast its boundary can expand, how much predictive and control information it can route through that boundary" — ch11 opens by picking up exactly this (ch11 lines 18–20). ✓

### D. Redundancy — **the major Part-level concern; this chapter front-runs four later chapters**
Per the brief, the following are "more properly the territory of later chapters":

- **Goal Laundering (313–361), label `sec:goal-laundering-ch10`** — the three-layer model `G_inf/G_sem/G_norm` (319–323), divergence score (331–338), and laundering signature (345–350) are a substantial development of material the brief assigns to **ch37**. **Trim to the diagnostic needed here (opacity around control variables) and cross-ref ch37 for the full treatment.**
- **From Goal Inference to Value-Bundle Divergence (363–411), label `sec:value-bundle-divergence`** — full bundle-inference objective `\hat B,\hat W,\hat\Phi = argmax ...` (369–375), four laundering levels, bundle/bearer laundering detectors (386–401). This is **ch20/21 territory** (bundle inference, bearer maps). It is introduced here before bundles are formally defined anywhere — readers meet `B,W,\Phi` cold. **Strongest premature-introduction flag in the Part.** Recommend reducing to a forward pointer.
- **Host Capacity and Parasite Persistence (466–517), label `sec:host-capacity-parasite`** — parasite persistence inequality (476–483). The brief assigns **parasites to ch34**. **Trim/cross-ref.**
- **Self-Modeling Versus Self-Transparency (518–575), label `sec:self-modeling-transparency`** — re-introduces `d` and `\tau` (524–533) and the self-control-vs-correction inequality (552–559), already in **ch06 (588–602)** and **ch08 (354–359)**; the brief assigns self-modeling to **ch30**. Third occurrence. **Trim/cross-ref.**

Other internal duplication:
- Control-locus continuity (274–311) restates ch07 (746–761) and ch08 (761–772).
- Perturbation/stress framing (219–267) restates ch07's "Adversarial Boundary Discovery" (675–761). The "surface rationale changes / control trajectory invariant" line (269–272) ≈ ch07 (716–719).
- Market-optimizes-without-intending example (681–698) ≈ ch09 (297–313).

Net: ch10's distinctive, properly-owned contributions are the **adversarial framing**, `\kappa` cooperativity, **selective opacity** (`\Omega_Q`), **adversarial decomposition posterior**, the **adversarial test battery**, and **decision triggers**. The four front-run object-families above dilute that focus.

### E. Consistency
- Section titles consistently Title Case. ✓ (matches ch07/ch08, conflicts with ch09)
- `\kappa` cooperativity index **defined before use** (92–104). ✓ Used only within ch10.
- Boundary inequality written inline (24) with no dedicated leakage symbol — i.e., ch10 doesn't reuse `\ell`/`\mathcal{R}`/`\mathcal{L}_B` at all, a fourth treatment-by-omission.
- `\mathrm{CCI}` used (637) as in ch09, still "defined later."
- WWCTV label convention broken (`sec:evidence-against-opacity` vs `sec:wwctv-strategic-opacity`).

### F. Open tangents / dangling promises
- "In later chapters we will model this [correction] channel more fully" (746) — forward to Part IV. Acknowledged.
- `\mathrm{CCI}` (637) and value-bundle symbols `B,W,\Phi` (369) used before formal definition. The bundle symbols in particular are a real "used-before-defined" issue, not just a forward promise.

---

## CROSS-CUTTING FINDINGS

### D (Part-level redundancy ledger)
| Concept | Homes | Recommendation |
|---|---|---|
| Boundary inequality `MI(I;E\|S,A)≤ε` | ch06 149/668, ch07 154/268, ch08 77, ch09 73, ch10 24 | ch06/ch07 are first homes (keep). ch08/ch09/ch10 should recap in ≤2 lines + `\ref`. |
| Four-role partition (I,S,A,E) | ch06 131, ch07 137, ch08 70, ch09 61 | Keep ch06; later chapters cross-ref. |
| Memory `\Delta_m(k)` | ch06 227, ch07 524, ch08 319 | Keep one (ch06); cross-ref. |
| Control-locus continuity | ch07 746, ch08 761, ch10 274 | ch10 owns the adversarial version; ch07/ch08 cross-ref. |
| Self-modeling vs transparency (`d`,`\tau`) | ch06 588, ch08 354, ch10 552 | Owned by ch30; collapse to one short statement + forward ref. |
| Composite "whole>parts" test | ch08 `\Gamma_{merge}` 571, ch09 `\Sigma` 183 | Note they are the same diagnostic; unify notation. |
| Responsibility under composites | ch08 661, ch09 414 | Cross-ref; avoid re-litigating. |
| Market/recommender example | ch09 297, ch10 681 | Keep one, cross-ref the other. |
| Adversarial perturbation/stress | ch07 675, ch10 219 | ch10 owns it; ch07 should preview + defer. |

### E (Part-level consistency)
- **Boundary-leakage symbol is not standardized:** `\ell` (ch06, ch08) vs `\mathcal{R}` (ch07) vs `\mathcal{L}_B` (ch09) vs inline-only (ch10). Pick one symbol Part-wide.
- **`\mathcal{R}` is overloaded:** boundary residual (ch07), reproduction operator (ch08 535), responsibility capacity `\mathcal{R}_i` (ch08 671), control reach `\mathcal{R}_C` (ch09 122). Disambiguate.
- **Section-title case:** Title Case (ch07/ch08/ch10) vs sentence case (ch09) vs mixed (ch06). Standardize.
- **Chapter-ending section name & numbering:** "Chapter conclusion" numbered (ch06), "Summary" numbered (ch07/ch08/ch10), "Chapter summary" **unnumbered `\section*`** (ch09). Standardize name and `\section` vs `\section*`.
- **WWCTV label:** `sec:wwctv-*` (ch06–ch09) vs `sec:evidence-against-opacity` (ch10). Align ch10.
- Consistent good: `\epsilon` for tolerated leakage, `\MI(\cdot;\cdot\mid\cdot)` macro, `eq:`/`sec:` label prefixes, the identity vector `\Xi` carried ch08→ch09.

### F (Part-level dangling threads)
- `\mathrm{CCI}` (correction-channel integrity) used in ch09 (493) and ch10 (637) but "defined later" — no anchor chapter is named. Add the target chapter number once known.
- Value-bundle symbols `B, W, \Phi` used in ch10 (369–405) before any definition — the only genuine "used-before-defined" (as opposed to honest forward-promise) case in the Part.

### G (Continuity hand-off)

**Incoming — concepts Part II assumes already known (from Part I / ch05):**
- The "wrong object" framing: ch06 references `\ref{ch:wrong-object}` (754) and ch07's chapterthesis restates it ("a wrong object," 5) — verify this does not simply repeat ch01's thesis; if ch01 already argues "wrong object," ch07's framing should cite/defer rather than re-assert.
- The correction-capacity assumption and the value-bundle/bearer-map vocabulary appear already in ch05's summary ([Defined] items, ch05 106–112). Part II leans on "value-bundle geometry," "bearer maps," and "correction channels" as known vocabulary while their formal machinery is deferred to Parts III/IV.
- The `[Defined]/[Conjectural]` bracket-status convention used in ch05 is **not** used in ch06–ch10 (the Part instead uses prose calibration). Not a defect, but a stylistic discontinuity across the Part I→II seam worth noting.

**Outgoing — concepts Part II introduces for later parts:**
- Boundary inequality, boundary residual, `\epsilon`-boundary, leaky/non-stationary boundaries → used throughout the book.
- Identity-as-transport, conserved-property vector `\Xi`, transport loss, certification-over-transformations (ch08) → successor-alignment chapters.
- Composite agent, composite surplus `\Sigma`, intervention leverage `\Lambda`, "align the effective optimizer not the artifact" (ch09) → governance/correction chapters.
- Strategic opacity, cooperativity `\kappa`, selective opacity `\Omega_Q`, adversarial decomposition, decision triggers (ch10) → AI-control / safety-case chapters.
- Competence = predictive + control information across the boundary (promised ch07 487–489) → **delivered in ch11** (chapterthesis). Clean closed loop.

---

## PRIORITIZED ACTION LIST (no edits made)
1. **Standardize boundary-leakage notation** Part-wide and disambiguate `\mathcal{R}` (ch06 365, ch07 197/463, ch08 535/671, ch09 75/122). *(consistency, high)*
2. **De-duplicate ch10's four front-run object-families** (goal laundering 313–361→ch37; bundle/bearer inference 363–411→ch20/21; parasite persistence 466–517→ch34; self-modeling vs transparency 518–575→ch30): reduce to diagnostics + cross-refs. *(redundancy/premature, high)*
3. **Reconcile ch07 "Adversarial Boundary Discovery" (675–761) with ch10** so the adversarial machinery has one home. *(redundancy, med-high)*
4. **Standardize section-title case** (ch06 internal mix; ch09 sentence vs ch07/08/10 Title). *(consistency, med)*
5. **Standardize the chapter-ending section** name + numbering (ch06 "Chapter conclusion"; ch09 unnumbered "Chapter summary"). *(consistency, med)*
6. **Align ch10's WWCTV label** to `sec:wwctv-strategic-opacity`. *(consistency, low)*
7. **Anchor `\mathrm{CCI}` and value-bundle symbols** to their defining chapters where first used in ch09/ch10. *(dangling refs, med)*
8. **Add a one-line opening bridge to ch09** and a short forward-ref to ch08 at the close of ch07. *(continuity, low)*
9. Collapse the triple self-modeling/`d`,`\tau` treatment (ch06 588 / ch08 354 / ch10 552) to one canonical statement + cross-refs. *(redundancy, med)*
