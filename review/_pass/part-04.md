# Part IV Review — "Human Values as Needs Smoothed over Time" (ch15–ch19)

Reviewer pass. Read in full and in order: ch15, ch16, ch17, ch18, ch19, plus context (ch11 Part III, end of ch14, start of ch20, `parts/part04-value-bundles.tex`). No manuscript files were edited.

Line numbers refer to the current `chapters/chNN-*.tex` files.

---

## 0. Part-level headline findings (read first)

1. **EVERY chapter in Part IV is MISSING the section titled exactly `What Would Change This View`.** Confirmed by grep across `chapters/`: ch15, ch16, ch17, ch18, ch19 are the only five chapters *not* in the set of files containing that heading (18 other chapters do have it — e.g. ch02, ch03, ch04, ch07–ch14, ch26, ch27, ch33, ch39, ch43, ch44). This is the single largest compliance gap and it is uniform across the part. See per-chapter §B for the closest renamed equivalents.
2. **Symbol clash on `B`.** In Part III (ch11) `B` is the *boundary-information / capability* measure (BIQ): `$B_X$`, `$B_{C_t}^{(h)}$`, `$\Delta B$` (ch11 lines 349–352, 380–383, 459–493). In Part IV `B` is the *value-bundle activation vector* `$B(t)\in\mathbb{R}^k$`. Same letter, two unrelated core quantities, in adjacent parts. Flagged in §E.
3. **`G_B` (bundle response geometry) is defined three different ways** across ch16/ch17/ch19 (gradient+Hessian pair vs. gradient field only vs. 4-tuple `(J,H,C,Φ)`). Detail in §D.4 / §E.
4. **The sample-complexity argument appears three times** (ch15, ch16, ch17), not twice as the brief anticipated. Detail in §D.1.
5. No `[STUB]`/`[TODO]`/`\todo`/placeholder markers in any of the five files (grep clean). All five have `chapterthesis`, `refsection`, and per-chapter `\printbibliography[heading=subbibliography,...]`.
6. Continuity (Part III→IV→V) is clean and well-staged; the chapter-to-chapter forward references resolve. Detail in §C / §G.

Compliance matrix:

| Element | ch15 | ch16 | ch17 | ch18 | ch19 |
|---|---|---|---|---|---|
| `\chapter` + `\label{ch:...}` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chapterthesis` env | ✓ (4–7) | ✓ (4–7) | ✓ (4–7) | ✓ (4–8) | ✓ (4–8) |
| Decision relevance early | ~ (late, ~606) | ✓ (16–28) | ✓ (16–43) | ✓ (38–61) | ✓ (17–59) |
| Failure-mode / counterexample | ✓ (807) | ✓ (887) | ✓ (705) | ✓ (255+, 731+) | ✓ (916) |
| `What Would Change This View` (exact) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Summary | ✓ (936) | ✓ (1211) | ✓ (775) | ✓ (1219) | ✓ (1172) |
| `refsection` + subbibliography | ✓ (9/981) | ✓ (9/1241) | ✓ (9/801) | ✓ (10/1230) | ✓ (10/1204) |

---

## ch15 — Values Are Compressed Control Signals (`ch:values-compressed-control`)

### A. Capsule
Thesis: values are not propositions but *compressed control signals* produced by feedback loops, stabilized by body/culture/social correction, read out as reasons for action. Establishes the `error loops → compressed salience → policy shaping → value labels` direction, the loop–bottleneck–policy architecture (`ε → s → B → π`), the value≠preference/emotion/goal/label distinctions, and the first alignment lesson (align to the control process, not stated preferences). This is the foundational chapter of the value model.

### B. Required-element compliance
- `\chapter` + `\label` (1–2), `chapterthesis` (4–7), epigraph, `refsection` (9), subbibliography (977–981): all present.
- **MISSING `What Would Change This View`.** The chapter ends `... Why this matters for superintelligence` (906) → `Summary` (936) → `Chapter References`. Closest content is `Counterexamples and limits` (807–866) and `What makes a compressed control signal a value?` (868–904), but neither is framed as falsification/"what would change this view," and neither uses the required exact title. Flag as missing; the limits section is the natural anchor to add it.
- No STUB/TODO markers.
- **Minor:** explicit *decision relevance* is deferred to `The first/second/third alignment implication` (606–732); the first ~600 lines are descriptive model-building. The cockpit analogy (59–67) gives early motivation, but a reader looking for "why this changes a decision" waits a long time.

### C. Continuity
Incoming handoff from ch14 is clean: ch14's closing (lines 988–991) explicitly says "The next chapter turns to the structure of human values themselves… a compressed bundle geometry." ch15 opens on exactly that. Outgoing: 974–975 promises ch16's value-bundle model. Staging vs. ch16/ch17 is non-circular: ch15 introduces `B` as control coordinate; ch16 formalizes the 4-part definition; ch17 supplies the learnability argument. Good division in principle.

### D. Redundancy (this chapter's contributions to part-wide duplication)
- **Sample-complexity argument appears here too** (sec `value-learning-bottlenecks`, 437–479), as an *unlabeled* display equation `m = O(k/(ε²(1-γ)²) log(k/δ))` (449–456) — identical in form to ch16 eq:sample-complexity (566–574) and ch17 eq:sample-complexity-ch17 (237–243). This is the **third** copy. **Recommendation: trim/cross-ref.** ch15's version is the most cursory; it should state the result in one sentence and cross-reference ch17 (the canonical home) rather than re-deriving the bound. Mark as *true duplication*.
- **Candidate value-direction list** (sec `candidate-value-directions`, 481–498): `\begin{description}` of Protection, Non-suffering, Care, Truth, Autonomy, Justice, Loyalty, Dignity, Beauty, Learning, Legacy. Overlaps ch16's `candidate-bundle-examples` (308–407). ch15's list is one-line-per-item; ch16's is a full subsection each. **Keep (pedagogical):** the ch15 list is a teaser; ch16 is the elaboration. But the two lists are *not identical* (ch15 adds Learning + Legacy; ch16 omits both and adds nothing equivalent) — see §E consistency note.
- Tradeoff second-derivative `∂²π/∂Bᵢ∂Bⱼ` (543–547) previews ch16's `T_ij` (264–269) and ch19's `H_ij` (179–184). Keep (pedagogical preview), but it is the same object under three names — see §E.

### E. Consistency
- `B_k(t)` control coordinate (203–214), `Φ_t` bearer map (623–630), `U_t` update process (630). Note ch15 names the update operator `U_t`; ch17/ch18 rename it `U_H` (ch17 610–616; ch18 466). Minor symbol drift — flag.
- The target triple `(B_t, Φ_t, U_t)` (619–631) is the same triple ch17 writes as `(B, Φ, U_H)` (607–616). Align the naming.
- Section-title capitalization: ch15 uses sentence case throughout (`The basic shift`, `Why compression is necessary`). ch16/ch17/ch18/ch19 are inconsistent with this (mixed Title Case) — see part-wide note in §E-global below.

### F. Open tangents / dangling promises
- "Later chapters will introduce `Φ_t` and `U_t` in detail" (634) → ch18 (Φ) ✓; `U` (correction/update) is treated in ch17/ch18 and Part beyond — acceptable.
- "later chapters will distinguish `B_k` from `u_k`" (392–398): the label-vs-signal distinction recurs (ch16 `why-labels-insufficient`; ch18 throughout). Resolved.
- "This is the beginning of bearer import" (723) → ch18 `bearer-import` (318+). Resolved.

### G. Hand-off
Incoming assumed concepts: correction channel / corrigibility basin from Part III (used loosely at 558–604). Outgoing: `B` coordinate + manifold `M_B` (511–514), bearer map, update process → feed ch16–ch18.

---

## ch16 — The Value-Bundle Model (`ch:value-bundle-model`)

### A. Capsule
Thesis: values are low-dimensional latent control variables (bundles) defined by four functional properties — **activation, policy effect, tradeoff geometry, bearer map**. Establishes the canonical 4-part definition (213–307), distinguishes values from needs/preferences/goals/norms, gives the candidate-bundle catalogue, the `Q`-expansion (eq:q-bundle-expansion), the sample-efficiency/low-dim hypothesis, bundle inference (eq:bundle-inference), failure modes, audit protocol, worked examples. This is the structural core of the part.

### B. Required-element compliance
- `\chapter`+`\label` (1–2), `chapterthesis` (4–7), `refsection` (9), subbibliography (1237–1241): present.
- **MISSING `What Would Change This View`.** Chapter ends `Open technical questions` (1154–1210) → `Summary` (1211). **`Open technical questions` is a partial renamed-equivalent** (it lists `How many bundles?`, `Are bundles universal?`, `Can artificial systems learn bundle geometry?`, `How do we distinguish moral progress from manipulation?`) but it is framed as *open research questions*, not as *falsification conditions for the chapter's thesis*. Flag as missing exact-titled section; note the partial equivalent.
- No STUB/TODO markers.
- Decision relevance: present early (`Why a value model is needed`, 16–28; `Why flat reward models fail`, 510–549).
- Failure-mode/counterexample: `Failure modes` (887–973) — strong (semantic-without-geometric, bundle collapse, bearer narrowing, tradeoff inversion, context laundering, reflective capture).

### C. Continuity
Builds explicitly on ch15 (line 67 "building on the compressed-control framing introduced in Chapter~\ref{ch:values-compressed-control}"). Outgoing (1226–1229) names "one chapter analyzes why low-dimensionality matters" (ch17), "another examines bearer maps" (ch18), and later correction/successor chapters. Clean staging. No circularity: ch16 *asserts* the low-dim hypothesis and uses it; ch17 *argues for* it. That is the intended order, but see §D.1 — the actual sample-complexity *derivation* is duplicated rather than deferred.

### D. Redundancy
1. **Sample-complexity (eq:sample-complexity, 566–574)** vs. ch17 eq:sample-complexity-ch17 (237–243) and ch15 (449–456). ch16's and ch15's forms are identical (`O(k/(ε²(1-γ)²) log(k/δ))`); ch17's is `≳ 2k/(ε²(1-γ)²) log(2k/δ)` (constants differ, same scaling). **This is true duplication across three chapters.** Division of labor should be: **ch17 is the canonical home** (it has the full statistical treatment, the numeric table 259–269, and the horizon discussion). Recommend ch16 keep only a one-line statement + `\ref{eq:sample-complexity-ch17}` cross-ref, and drop the duplicate `itemize` gloss of `m,k,ε,γ,δ` (575–582) which is verbatim-equivalent to ch17's (244–251). Mark **trim/cross-ref**.
2. **Candidate-bundle catalogue** (`candidate-bundle-examples`, 308–407): 9 full subsections (Protection…Beauty). Overlaps ch15's list (481–498) and is re-listed again in ch19 (27, 46) and ch18 (76–86). **Keep here (pedagogical canonical catalogue)** — ch16 is the right home for the full descriptions. But cross-references from ch15/ch18/ch19 back to this section would reduce re-statement. Mark ch16 = **keep (canonical)**; the *re-listings elsewhere* = trim/cross-ref.
3. **Four-part definition restated as audit** (`minimal-audit-protocol`, 1026–1086: activation/policy-effect/tradeoff/bearer audits) closely mirrors ch18 `auditing-bearer-maps` (764–858) and ch19 `measuring-bundle-geometry` (835–915). The audit idea recurs in all three. **Partly keep** (ch16's is a generic 4-part audit; ch18's is bearer-specific; ch19's is geometry-measurement). But the *bearer audit* (1071–1082) is fully subsumed by ch18 — recommend ch16 cross-ref ch18 for that sub-item. Mark **trim/cross-ref** for the bearer-audit sub-item.
4. **`G_B` first definition** (`bundle-policy-geometry`, 450–459): `G_B(s) = (∇_B log π, ∇²_B log π)` — i.e. gradient *and* Hessian. This collides with ch17's and ch19's different definitions (see §E). The `d_bundle` preservation measure (858–877) uses `G_B^A(s)`; this is re-derived more fully in ch19 as `d_G` over `(J,H,C,Φ)`. Mark the preservation-distance as **trim/cross-ref to ch19** (ch19 `bundle-metrics`, 511–567 is the canonical, richer treatment).

### E. Consistency
- **`G_B` definitional drift (key finding):** ch16 line 452 = `(gradient, Hessian)`; ch19 line 213/518 = `(J, H, C, Φ)` 4-tuple; ch17 line 341 = gradient field only. Same symbol, three referents. Recommend the part adopt ch19's `(J,H,C,Φ)` as canonical and have ch16/ch17 forward-reference it (or use a distinct symbol for the partial objects).
- Number of bundles: ch16 uses `k` (`B(t)∈ℝ^k`, 99). ch18 uses `m` (`B_t∈ℝ^m`, 74). Flag dimension-symbol inconsistency `k` vs `m`.
- Tradeoff object: ch16 `T_ij = ∂²log π/∂Bᵢ∂Bⱼ` (264–269) vs. ch19 `H_ij = ∂²μ_π/∂Bᵢ∂Bⱼ` (179–184) — ch16 differentiates `log π`, ch19 differentiates the action-feature mean `μ_π`. Related but *not the same operator*; both call it "the interaction." Worth a one-line note reconciling them.
- `W` tradeoff weights: ch16 uses capital `W` (context-dependent weight vector, 534) consistent with ch17/ch18; ch19 uses lowercase `w_i(c)` (255, 574). Minor case inconsistency.
- Section-title capitalization is internally mixed: sentence case (`Why a value model is needed`, 16) and Title Case (`What Makes Value Learning Possible`, 551; `Values Across Cultures, Institutions, and Time`, 720; `Worked Examples`, 1087). Inconsistent within the chapter and with ch15.

### F. Open tangents / dangling promises
- "A later chapter treats bearer import and ontology shift in detail" (306) → ch18 ✓.
- "must later connect to correction-channel integrity" (1152), "A later chapter will argue that legitimacy depends on correction-channel integrity…" (1209) → Part beyond (correction chapters). Acceptable forward promise.
- `how-many-bundles` (1159–1172): leaves `k` unspecified — intentional open question, but note ch17 §empirical-signatures and §rank-of-value also promise the "elbow" test; same promise made twice (ch16 1166–1172 and ch17 391–393, 679–681). Consolidate.

### G. Hand-off
Incoming: ch15's `ε→s→B→π` and value≠preference framing (re-stated 145–211). Outgoing: 4-part bundle definition + `G_B` + `Φ` + tradeoff geometry → ch17 (learnability), ch18 (Φ), ch19 (geometry).

---

## ch17 — Why Low Dimensionality Makes Value Learning Possible (`ch:low-dimensional-value-learning`)

### A. Capsule
Thesis: human values are learnable only if policy-relevant valuation factors through a low-dimensional bottleneck; low-dim makes learning *statistically possible*, correction makes it *legitimate*. Establishes: simple≠low-dimensional, flat reward model, the bottleneck model with the conditional-independence/MI sufficiency definition, the sample-complexity argument (canonical), the evolutionary rationale, local vs. global low rank, the bearer problem (preview), and the four learnability→alignment gaps.

### B. Required-element compliance
- `\chapter`+`\label` (1–2), `chapterthesis` (4–7), `refsection` (9), subbibliography (797–801): present.
- **MISSING `What Would Change This View`.** Ends `Why This Matters for Superintelligence` (744) → `Summary` (775). **`Empirical Signatures` (674–703) is the strongest renamed-equivalent in the whole part** — it lists six falsifiable predictions (diminishing returns / elbow, clustered perturbation effects, cross-context generalization, residual-driven discovery, cultural modulation, developmental staging) whose failure would undermine the thesis. This is functionally "what would change this view" but is mis-titled. **Recommend either rename to the exact heading or add the exact-titled section referencing it.**
- No STUB/TODO markers.
- Decision relevance: immediate (16–43). Failure-mode: `Failure Modes` (705–742) with audit-question table.

### C. Continuity
Explicit build on ch15+ch16 (line 58). Forward to ch18 named (`Chapter~\ref{ch:bearer-maps}` at 478; "The next chapter turns to the second: the problem of bearers," 773). Staging vs. ch16: ch16 *uses* low-dim as a premise; ch17 *defends* it — order is right, but the duplicated derivation (below) blurs the division of labor. No circularity in the argument itself.

### D. Redundancy
1. **Sample-complexity (eq:sample-complexity-ch17, 237–243): canonical home.** This is the fullest version (numeric table 259–269, horizon discussion 255–258). The duplicates are ch15 (449–456) and ch16 (566–574). Keep ch17; trim the other two to cross-refs. The `itemize` defining `m,k,ε,γ,δ` (244–251) is verbatim-equivalent to ch16's (575–582) — only one copy is needed.
2. **`G_B` definition (340–348): gradient field only** `(∂π/∂B_1,…,∂π/∂B_k)`. This is narrower than ch16 (gradient+Hessian, 452) and ch19 (4-tuple, 213). "The book will use this object repeatedly" (349) — but the object it names is not the same one ch19 names `G_B`. True inconsistency, not mere duplication. See §E.
3. **Bearer problem (`bearer-problem-ch17`, 443–478)** is a preview of ch18; explicitly defers ("Chapter~\ref{ch:bearer-maps} develops bearer import in detail," 478). **Keep (pedagogical preview)** — it is short and correctly cross-referenced.
4. **Simple-vs-low-dimensional / color & thermodynamics analogies** (60–105): the "low-dimensional ≠ simple" point and the color analogy duplicate ch15 `low-dimensional-not-simple` (403–435) and ch16 `sample-efficiency-low-dim` (590–597, also color). The color analogy appears in **both ch16 (594–597) and ch17 (90–95)**. **Trim/cross-ref:** pick one home for the color analogy (ch17 is the natural one since this is the dimensionality chapter); ch15's temperature/creditworthiness version (411–413) can stay as the teaser.
5. **`(B,Φ,U_H)` alignment target** (607–616) restates ch15's `(B_t,Φ_t,U_t)` (619–631). Keep (it is the running thesis object) but unify the symbol (`U_t` vs `U_H`).

### E. Consistency
- **`Φ` is overloaded *within ch17*.** `\phi(x,a)` lowercase = feature vector (110); **capital `Φ` (no subscript) = feature matrix** in `rank-of-value` ("Let `$\Phi\in\mathbb{R}^{N\times n}$` be a matrix of high-dimensional features," 358); but **`Φ_j` = bearer map** in `bearer-problem-ch17` (449–452) and the alignment target (610–616). The same capital `Φ` denotes a feature matrix in one section and the bearer map in another. **This is a genuine intra-chapter clash — flag and recommend renaming the feature matrix (e.g. to `X` or `F`).**
- `G_B` defined inconsistently with ch16/ch19 (see §D.2 above and §E-global).
- `U_H` vs ch15's `U_t` (naming drift).
- Section titles are Title Case here (`The Bottleneck Model`, `The Sample Complexity Argument`, `The Rank of Value`), differing from ch15's sentence case.

### F. Open tangents / dangling promises
- `rank-of-value` research program (394–401) and `empirical-signatures` (674–703) both promise the "elbow"/effective-rank test; same promise also in ch16 (1166–1172). Triplicated empirical promise — consolidate.
- "Recent work on language models sometimes finds low-dimensional directions… (sparse-directions-not-enough, 480–509)": healthy caveat, well-scoped, resolved in-section.
- Four gaps (identifiability/bearer/optimization/legitimacy, 588–605): bearer gap → ch18; optimization gap → later (Goodhart, ch19 §goodhart + Part beyond); legitimacy gap → correction chapters. Forward promises tracked.

### G. Hand-off
Incoming: `B`, bundle, `Φ`, `(B,Φ,U)` target from ch15/ch16. Outgoing: bottleneck sufficiency, effective-rank, learnability gaps → ch18 (bearer) and correction chapters.

---

## ch18 — What Values Apply To / Bearer Maps (`ch:bearer-maps`)

### A. Capsule
Thesis: a value is also a claim about *where it applies*; alignment must preserve bearer maps `Φ` connecting bundles to entities/processes/relations/histories under a changing world. Establishes: bundle vs. bearer two-sidedness, bundle-drift vs. bearer-drift, bearer maps as moral sufficient statistics, false-neg/false-pos asymmetry with weighted loss, **bearer import** + commutation condition, commutation failure / measurement capture, bearer uncertainty → caution, self-sealing maps, relational bearers + comparison classes, substrate change / merging, bearer exploits, audit protocol, preservation loss `L_BP`, design principles. The most thorough chapter in the part.

### B. Required-element compliance
- `\chapter`+`\label` (1–2), `chapterthesis` (4–8), `refsection` (10), subbibliography (1226–1230): present.
- **MISSING `What Would Change This View`.** Ends `What This Chapter Adds` (1178–1218) → `Summary` (1219). `Philosophical Limits` (1086–1112) discusses the boundary of what technical means can settle, but is not a falsification section. `Auditing Bearer Maps` (764–858) is a test battery, not "what would change this view." No renamed equivalent; **flag as missing.**
- No STUB/TODO markers.
- Decision relevance: immediate and strong ("one of the central alignment problems," 56).
- Failure-mode/counterexample: extensive — false neg/pos (255–317), commutation failure (374–406), self-sealing (490–522), bearer exploits (731–763).

### C. Continuity
Builds on ch16/ch17 (line 58 "If value bundles are the few knobs that make value learning tractable (Chapter~\ref{ch:low-dimensional-value-learning})"). Outgoing (1213–1214) names ch19 (`ch:tradeoffs-bundle-geometry`) and `ch:goal-transport` + "later transport chapters." Forward ref `\ref{ch:goal-transport}` should be verified to resolve (a goal-transport chapter must carry that label — out of scope here but flag for build check). Clean staging.

### D. Redundancy
- **Auditing Bearer Maps (764–858)** overlaps ch16 `minimal-audit-protocol` bearer-audit (1071–1082) and ch19 `measuring-bundle-geometry` (835–915). ch18's is bearer-specific and the most detailed (activation/borderline/ontology-shift/adversarial-reframing/manipulation/successor tests). **Keep (canonical for bearer audits);** recommend ch16's bearer-audit sub-item cross-ref here instead of restating.
- **Bearer-map definition restated** vs. ch19 §value-lists-bundle-coordinates: ch18 `Φ_t: Z_t×C_t→[0,1]^m` (90–93) and ch19 `Φ_i: Z×C→[0,1]` (93–97) define the same object; ch19 re-introduces it. **Keep ch18 as canonical bearer-map home; ch19 should cross-ref** rather than re-define (minor — ch19's re-intro is brief).
- **Bundle coordinate vector re-listed** (76–86): `(B^care, B^truth, …)` — same catalogue as ch16. Trim/cross-ref to ch16.
- `L_BP` preservation loss (859–902) and the successor-test condition `L_BP<ε` (1174–1176) is the bearer analogue of ch16 `d_bundle` (858–877) and ch19 `d_G` (524–567). Three preservation metrics for three sub-objects — **keep (each is a distinct measure)**, but a single cross-referencing paragraph noting "bundle distance (ch16/ch19) + bearer-preservation loss (here) are components of one successor-certification metric" would prevent the reader seeing them as redundant.

### E. Consistency
- **Bundle dimension symbol `m`** here (`B_t∈ℝ^m`, 74; `Φ_t: …→[0,1]^m`, 91) vs. `k` in ch16/ch17/ch19. Flag.
- `Φ` usage is consistent with ch15/ch16/ch19 (bearer map) — good; but note ch17's capital-`Φ`-as-feature-matrix clash means cross-part `Φ` is *only* clean if ch17's feature matrix is renamed.
- `U_H` update operator (466–477) consistent with ch17; differs from ch15's `U_t`.
- Section titles Title Case (`The Bearer Problem`, `Why Bearers Are Harder Than Labels`).
- `z` is carefully redefined as "any represented structure" not "object" (240–242) — good internal discipline.

### F. Open tangents / dangling promises
- "Chapters~\ref{ch:goal-transport} and later transport chapters" (1214): forward promise — verify label exists in build.
- Merging problem (674–730): rich, possibly the seed of a later dedicated treatment; self-contained here, no dangling promise.
- Digital-mind / moral-patienthood thread (433, 503–505, 1057–1068, 1096–1102): recurs but is resolved into "preserve correction conditions"; no loose end, though it overlaps ch43 (`ch43-bearers-of-value.tex` exists — a *second* bearer-of-value chapter in a later part). **Flag potential cross-part redundancy ch18 ↔ ch43** for whoever reviews Part with ch43 (out of scope for this pass, but the titles strongly overlap).

### G. Hand-off
Incoming: bundle geometry + `(B,Φ,U_H)` target. Outgoing: `Φ_k(z,c,h)`, bearer import/commutation, self-sealing, `L_BP` → ch19 (tradeoffs) and goal-transport/correction chapters.

---

## ch19 — Tradeoffs and Bundle Geometry (`ch:tradeoffs-bundle-geometry`)

### A. Capsule
Thesis: the hard part is that we care about many things whose *meanings change when traded against one another*; bundle geometry `G_B=(J,H,C,Φ)` encodes gradients, interaction curvature, protected/lexical regions, and bearer-dependent context weights. Establishes the canonical `G_B` 4-tuple, the value triple `(B_i,Φ_i,χ_i)`, tradeoffs-as-curvature, worked bundle interactions (truth/care, autonomy/non-suffering incl. the **Paternalism Boundary**, justice/mercy, loyalty/truth, beauty/utility), Pareto/feasible sets, lexical/protected regions with barrier term, bundle metrics `d_G`, contextual-weight failure modes, uncertainty/reversibility, ontology-shift transport, substrate transfer, cross-agent invariants, measurement methods, Goodhart pressure, social-choice aggregation, moral learning as geometry revision.

### B. Required-element compliance
- `\chapter`+`\label` (1–2), `chapterthesis` (4–8), `refsection` (10), subbibliography (1200–1204): present.
- **MISSING `What Would Change This View`.** Ends `Why This Matters for Superintelligence` (1119) → `Summary` (1172). The `seven invariants` (788–830) and `Goodhart Pressure` (916–963) are robustness/failure content, not a falsification section. No renamed equivalent; **flag as missing.**
- No STUB/TODO markers.
- Decision relevance: immediate (17–59). Failure-mode: `Goodhart Pressure on Bundle Geometry` (916–963) + contextual-weight failure modes (569–625).
- **Paternalism Boundary** is present (the brief's expected element): `autonomy-non-suffering` §, lines 306–342, with the explicit paternalism-failure pattern `ΔB_care>0 but ΔB_autonomy, ΔB_agency, ΔC_corr<0` (326–331). Not titled "Paternalism Boundary" but the content is here and correct.

### C. Continuity
Builds on ch16+ch18 (line 59). Forward to ch20 named (`Chapter~\ref{ch:reward-to-bundle-inference}`, 1198) — confirmed: ch20 carries that exact label and opens on reward→value/goal inference (verified). Clean IV→V handoff. Also forwards to correction-channel and successor-certification chapters (833, 1197–1198).

### D. Redundancy
- **`G_B` canonical 4-tuple `(J,H,C,Φ)`** (213–223, 518): this is the richest and should be the **canonical definition** for the part. ch16's `(gradient,Hessian)` (452) and ch17's gradient field (341) are earlier, thinner, *and named the same symbol*. **Recommend ch16/ch17 cross-ref this definition** (or use different symbols for their partial objects). Mark ch16/ch17 G_B = trim/relabel; ch19 = keep (canonical).
- **Bearer map re-definition** (`Φ_i: Z×C→[0,1]`, 93–97): duplicates ch18 (90–93). Brief; recommend cross-ref ch18. Minor.
- **Candidate bundle list re-listed** (27, 46): trim/cross-ref ch16.
- **Substrate transfer chain** (`ε→s→B→χ→C_social`, 722–759) restates ch15's loop–bottleneck–policy chain (`ε→s→B→π`, the ch15 Summary diagram 946–953) with `χ` and social correction appended. Keep (it is the transport-framed version), but the overlap with ch15's architecture is worth a cross-ref.
- **Measuring Bundle Geometry** (835–915: behavioral perturbation / representation probing / correction-channel testing) overlaps ch16 `minimal-audit-protocol` and ch18 `auditing-bearer-maps`. **Keep (geometry-measurement is distinct from the bearer audit),** but the three audit/measurement sections across ch16/ch18/ch19 would benefit from one shared framing sentence so the reader sees them as one toolkit rather than three.

### E. Consistency
- `G_B = (J,H,C,Φ)` (canonical) vs ch16/ch17 variants — the central `G_B` inconsistency lands here; recommend this be declared canonical.
- `H_ij` interaction differentiates `μ_π` (action-feature mean, 183) whereas ch16 `T_ij` differentiates `log π` (264). Same intuitive object ("interaction curvature"), different operators and different symbols (`H` vs `T`). Reconcile or note the relationship.
- `w_i(c)` lowercase context weights (255, 574) vs `W` capital in ch16/ch17/ch18. Case inconsistency.
- Value triple `(B_i,Φ_i,χ_i)` (110–118) introduces `χ_i` (policy-response pattern) — a new symbol not used in ch15–ch18, which spoke of policy *effect* `E_k` (ch16 240–243). `χ_i` ≈ ch16's `E_k`/`q_k`. Flag new-symbol-for-old-concept.
- Section titles Title Case.

### F. Open tangents / dangling promises
- "later chapters on goal transport, correction-channel integrity, and successor certification" (833, 1197–1198): forward promises into Part V+. Tracked.
- Social-choice aggregation (1027–1072) opens a large topic (Arrow/impossibility) and resolves it to "aggregation must be part of the correction channel" — adequately closed for this chapter, but flags a forward dependency on a correction/social-choice chapter.

### G. Hand-off
Incoming: bundles, `Φ`, tradeoff intuition from ch15–ch18. Outgoing: `G_B=(J,H,C,Φ)`, `d_G`, invariants, geometry-revision legitimacy criterion → ch20 (`From Rewards to Values`, goal inference) and correction/successor chapters. ch20 picks up directly: its thesis ("infer not only what is optimized but which value-bundles are active, what they apply to, how tradeoffs change") is the inference-side mirror of ch19's representation-side geometry.

---

## E-global — Notation & style consistency summary (part-wide)

| Symbol / item | Usage & issue |
|---|---|
| `B` | **Cross-part clash:** capability/boundary-info (BIQ) in Part III ch11 vs. value-bundle vector in Part IV. High-priority flag. |
| `G_B` | **Three definitions:** ch16 `(∇,∇²)` (452); ch17 gradient field (341); ch19 `(J,H,C,Φ)` (213/518). Declare ch19 canonical. |
| bundle dim | `k` in ch15/ch16/ch17/ch19; `m` in ch18 (74,91). Unify to `k`. |
| interaction | `∂²π/∂Bᵢ∂Bⱼ` (ch15 544) / `T_ij` on `log π` (ch16 264) / `H_ij` on `μ_π` (ch19 183). Three names/operators for "interaction curvature." |
| update operator | `U_t` (ch15 630) vs `U_H` (ch17 610–616, ch18 466). Unify to `U_H`. |
| `Φ` | bearer map throughout ch15/16/18/19 (consistent) **but** also = feature matrix in ch17 `rank-of-value` (358). Rename ch17's feature matrix. |
| `W`/`w` | capital `W` (ch16 534, ch17 637, ch18 934) vs lowercase `w_i(c)` (ch19 255,574). Pick one. |
| `χ_i` | new in ch19 (110–118) for policy-response pattern ≈ ch16 `E_k`/`q_k`. Reconcile. |
| section titles | ch15 = sentence case; ch16–ch19 = mixed/Title Case (and ch16 mixes both internally). Pick one convention. |

---

## Top recommendations (priority order)

1. **Add the exact-titled `What Would Change This View` section to all five chapters.** ch17 already has the material (`Empirical Signatures`) — rename or wrap it. ch16's `Open technical questions` is a partial base. ch15/ch18/ch19 need new ones (anchor on counterexamples/limits, bearer-exploit reversibility, and geometry-revision legitimacy respectively).
2. **Resolve the `B` cross-part clash** (Part III capability vs. Part IV bundles) — either rename one, or add an explicit "note on notation" reconciling them at the start of Part IV.
3. **Pick one canonical `G_B` definition** (ch19's `(J,H,C,Φ)`); make ch16/ch17 cross-reference it or use distinct symbols.
4. **De-duplicate the sample-complexity argument**: canonical = ch17 (eq:sample-complexity-ch17). Reduce ch15 (449–456) and ch16 (566–582) to one-line cross-refs.
5. **Rename ch17's feature matrix `Φ`** (357–376) to avoid the bearer-map collision inside the same chapter.
6. Minor: unify bundle-dimension symbol (`k`), update operator (`U_H`), weight case (`W`), and section-title capitalization; add cross-refs for the recurring candidate-bundle catalogue (canonical in ch16) and the three audit/measurement sections (ch16/ch18/ch19).
7. Out-of-scope but worth raising: **ch18 (`bearer-maps`) ↔ ch43 (`bearers-of-value`)** likely overlap; verify division of labor when reviewing the later part. Verify forward refs `\ref{ch:goal-transport}` (ch18) and `\ref{ch:reward-to-bundle-inference}` (ch19) resolve in the build.
