# Part V Review — "Interpreting a System's Goals" (Chapters 20–23)

Reviewer pass: structural / continuity / redundancy / consistency.
Files reviewed in full and in order:
- `chapters/ch20-reward-to-bundle-inference.tex` (1110 lines)
- `chapters/ch21-compression-test-intention.tex` (1016 lines)
- `chapters/ch22-goal-transport.tex` (909 lines)
- `chapters/ch23-transport-types.tex` (922 lines)
- Context: `parts/part05-goal-inference.tex`, `frontmatter/introduction.tex` (§ "operational vocabulary").

**Headline:** This is the highest-redundancy part of the book. The same five formal objects (value-bundle response geometry, bundle-inference argmax, correction chain, CCI, human value-update operator) are re-derived from scratch in ch21, ch22, **and** ch23, and again later in ch24/ch25/ch26. The intra-part escalation (inference → intention test → transport → transport types) is real and defensible *as a spine*, but ch21–ch23 currently retread each other heavily, and ch21/ch23 import most of Part VI's correction machinery before Part VI arrives. Two hard compliance failures: **no chapter has the exact "What Would Change This View" section**, and **ch20's outgoing handoff skips ch21**. One genuine notation defect: the ΔL sign/definition convention in ch21–ch23 is inverted relative to the book's Introduction.

---

## Part-level findings (read this first)

### Required-element compliance matrix

| Element | ch20 | ch21 | ch22 | ch23 |
|---|---|---|---|---|
| `\chapter` + `\label` | ✓ (L1–2) | ✓ (L1–2) | ✓ (L1–2) | ✓ (L1–2) |
| `chapterthesis` | ✓ (L4–7) | ✓ (L4–7) | ✓ (L4–7) | ✓ (L4–7) |
| Decision relevance | ⚠ weak — no titled section; only "What Counts as Success?" (L1013) | ✓ titled §"Decision Relevance" (L886), explicit triggers | ⚠ embedded in §"Goal Transport and Guarantees" (L793); no titled section | ⚠ embedded in §"A Safety Condition" (L839) + §"Why This Chapter Matters" (L875); no titled section |
| Failure-mode / counterexample | ✓ §"Degenerate Bundle Models" (L786) | ✓ §"Over/Under-Attribution" (L610), §"Limits" (L919) | ✓ §"Counterexamples and Edge Cases" (L722) | ✓ §"Failure Modes" (L676) |
| **EXACT "What Would Change This View"** | ✗ "Where the Argument Is Shaky" (L1042) | ✗ "Limits of the Compression Test" (L919) | ✗ "Philosophical Limits" (L826) | ✗ "The Philosophical Boundary" (L804) |
| Summary | ✓ (L1066) | ✓ (L974) | ✓ (L865) | ⚠ "Chapter Conclusion" (L899) + a "Chapter Summary" at the *front* (L15) |
| `refsection` + `\printbibliography[heading=subbibliography,…]` | ✓ (L9 / L1108) | ✓ (L9 / L1014) | ✓ (L9 / L907) | ✓ (L9 / L920) |

**WWCTV is a part-wide failure.** All four chapters substitute a differently-titled "shaky/limits/philosophical" section. ch20 is the closest in spirit (lists five uncertain assumptions, L1045–1064). The cheapest fix is to retitle these four sections to the exact string "What Would Change This View" (and convert the prose from "here are our caveats" to "here is the evidence that would overturn the claim," which is a slightly stronger framing than the current limits framing).

### Notation / sign convention (FLAG)

- **Introduction** (`frontmatter/introduction.tex` L139–147) defines the canonical compression criterion as
  ΔL = L_mechanistic − L_intentional + λ DL(R), framed as "a goal attribution earns its keep when it saves *bits*" (so L is a description length, lower = better).
- **ch21** (eq:intentional-gain-simple, L55–63) defines ΔL_int = L(M_int|X) − L(M_mech|X) − λ DL(G), with L declared as "log evidence or predictive score" (L150, higher = better), and ΔL_int > 0 ⇒ intention wins.

These two conventions differ in **both** the ordering of the two L-terms (mech−int vs int−mech) **and** the sign of the complexity penalty (+λDL vs −λDL). ch22 (eq:transport-gain, L47–57) and ch23 (eq:transport-gain-ch23, L599) follow ch21's log-evidence convention, so Part V is internally consistent but globally inconsistent with the Introduction. A reader who carries the Introduction's formula into ch21 will read every ΔL inequality backwards. **Recommend:** adopt one convention book-wide; if the log-evidence form is preferred, fix the Introduction; otherwise add a one-line footnote at eq:intentional-gain-simple reconciling the two. (ch20's ΔL_strategic, L873–879, and ch21's compression-score C(M;X), L153–164, are both consistent with the log-evidence form, so the Introduction is the outlier.)

Other notation: M_0, M_T, X_{1:T}, T, λ are used consistently across ch22/ch23. The DL argument correctly varies by object (DL(G) goal in ch21; DL(T) transport map in ch22/ch23). No drift there.

### Section-title capitalization

- ch20 uses Title Case for `\section` but **sentence case** for `\subsection` ("Bundle activations" L239, "Tradeoff weights" L257, "Step 1: collect trajectories and judgments" L708).
- ch21/ch22/ch23 use Title Case for both ("Mechanistic Dynamics" L191, "Policy Dynamics" L205, etc.).
Pick one convention for subsection casing across the part; ch20 is the outlier.

### Chapter-ending naming

Inconsistent across the part: ch20 ends Shaky→Summary; ch21 ends Limits→Summary; ch22 ends Philosophical Limits→Summary; ch23 ends Philosophical Boundary→Safety Condition→Why This Chapter Matters→Chapter Conclusion. ch23 is also the only chapter that opens with a "Chapter Summary" (L15) rather than a motivating section. Standardize the closing block (ideally: WWCTV → Summary).

---

## A. Capsules

- **ch20 — From Rewards to Values.** Argues scalar reward inference is the wrong level; upgrades the inference target from R̂ to (B̂, Ŵ, Φ̂); introduces value-bundles, the three inference objects (activations / tradeoff weights / bearer maps), a minimal generative model, response geometry, a 7-step algorithm sketch, degenerate-model failures, and two worked examples (helpful lie; merging). Long and foundational, but sprawling (1110 lines).
- **ch21 — The Compression Test for Intention.** Defines intentional compression gain ΔL_int; mechanistic/policy/intentional three-way comparison; six "degrees of intentional compression" (Levels 0–5); over/under-attribution; adversarial compression; two worked examples (helpfulness; frontier lab); decision relevance; limits. This is the chapter that should *own* the compression-test machinery.
- **ch22 — Has the Goal Really Survived?** Defines goal transport ΔL_transport = L(M_T|X) − L(M_0|X) − λDL(T); persistence vs transport vs reinterpretation; transport across ontology shift / capability growth / successor creation; adversarial transport; a 6-step inference pipeline; counterexamples (honest local optimizer, fanatic preserver, semantic mimic, captured system, benevolent paternalist); guarantees.
- **ch23 — When the Words Survive but the Meaning Doesn't.** Decomposes transport into the semantic ⊂ bundle ⊂ bearer ⊂ correction ⊂ successor stack; re-derives bundle geometry, bearer maps/import, correction chain, CCI, CEV link; ΔL_transport decomposition with risk weights; failure modes; perturbation tests; safety condition.

---

## B. Required-element compliance (per chapter)

- **ch20:** No `[STUB]`/`[TODO]` markers found. WWCTV ✗ (title is "Where the Argument Is Shaky", L1042). Decision relevance is the weakest of the four — there is no decision-trigger list; "What Counts as Success?" (L1013) is a success-criteria list, not a decision-relevance/triggers section. All other required elements present.
- **ch21:** No stub markers. WWCTV ✗ ("Limits of the Compression Test", L919). Strongest decision-relevance section in the part (explicit triggers L891–906; safety-case form eq:human-correctable-intention-safety-case L908–915). Compliant otherwise.
- **ch22:** No stub markers. WWCTV ✗ ("Philosophical Limits", L826). Decision relevance present but embedded in §"Goal Transport and Guarantees" (certification list L806–814). Compliant otherwise.
- **ch23:** No stub markers. WWCTV ✗ ("The Philosophical Boundary", L804). Decision relevance embedded in §"A Safety Condition" (L839) and §"Why This Chapter Matters" (L875). Summary handled by front "Chapter Summary" (L15) + "Chapter Conclusion" (L899) rather than a single tail "Summary".

---

## C. Continuity (ch20→ch21→ch22→ch23; Part IV in, Part VI out)

The **intended escalation is correct and worth keeping**: ch20 fixes the *object* of inference (bundles, not reward); ch21 supplies the *test* for when intention/goal-language is earned (compression); ch22 asks whether that object *survives transformation* (transport); ch23 *decomposes* transport into layers. Each chapter does add a genuinely new top-level idea (object → test → survival → layered decomposition).

**Handoff defects:**

1. **ch20 → ch21 broken (FLAG).** ch20's closing sentence (L1100–1102) says "The next chapter turns from bundle inference to goal transport … (Chapter~\ref{ch:goal-transport})". `ch:goal-transport` is **ch22**, not the actual next chapter ch21 ("The Compression Test for Intention"). ch20 skips ch21 in its own handoff. Fix: point to `ch:compression-test-intention` and describe the compression test, not transport.
2. **ch21 → ch22 ✓** (L1008 forward-refs `ch:goal-transport`).
3. **ch22 → ch23 ✓** (L901 forward-refs `ch:transport-types`).
4. **ch23 → Part VI ✓** (L914 forward-refs `ch:correction-causal-channel`, ch24).

**Part IV (ch19) → ch20 incoming:** ch20 grounds itself on `ch:value-bundle-model`–`ch:tradeoffs-bundle-geometry` (L82) and re-uses the bundle geometry of ch16, which is the right anchor. No explicit "previously in Part IV" sentence, but the dependency is stated.

**Retreading risk:** ch21, ch22, ch23 each independently (a) re-motivate "scalar reward is too thin," (b) re-introduce (B,W,Φ), (c) re-derive G_B, and (d) re-state ΔL as a compression criterion. ch22 §"Why Ordinary Goal Inference Is Not Enough" (L72–149) is largely ch20 §"Why Scalar Reward Is the Wrong Level" (L84–181) re-compressed; ch23 §"Values as Bundle Geometry" (L196–245) is a third pass over the same material. The escalation is real but currently buried under repeated re-derivation; each chapter should *reference* the canonical statement and add only its delta.

---

## D. Redundancy (the main event — enumerated, with keep/trim)

### D1. Value-bundle response geometry G_B = (∂π/∂B, ∂²π/∂B∂B, Φ)

| Location | Label | Verdict |
|---|---|---|
| ch16 (canonical home) | — | **keep** (origin) |
| ch20 L438–469 (G^(1), G^(2)) + L1088–1098 (summary) | unlabeled | **keep** (ch20 needs it to define the inference object); compress the summary restatement |
| ch21 L384–393 | `eq:value-bundle-geometry-ch21` | **keep** (the conserved object of the compression test); could cross-ref ch16/ch20 instead of full re-statement |
| ch22 L126–134 | `eq:value-bundle-geometry-ch22` | **trim → cross-ref** ch21; ch22 restates verbatim plus a second copy of just the gradient form at L328–336 |
| ch23 L227–237 | `eq:bundle-response-geometry-ch23` | **trim → cross-ref**; this is the 4th in-part copy. Also a partial copy in the tradeoff-preservation subsection L319–329 |
| ch25 L336 | `eq:value-bundle-geometry-ch25` | out of part (note for Part VI review) |

Net: G_B is stated **at least six times** book-wide, four of them inside Part V. Keep one canonical (ch16) + one "conserved-object" statement in ch21; convert ch22/ch23 to `\eqref` cross-references.

### D2. Bundle-inference argmax  (B̂,Ŵ,Φ̂) = argmax P(A|I,B,W,Φ)P(B,W,Φ)

| Location | Label | Verdict |
|---|---|---|
| ch16 L668 | `eq:bundle-inference` | **keep** (canonical) |
| ch10 L374 | `eq:bundle-inference-ch10` | out of part |
| ch20 L220–226 **and** L364–372 | unlabeled (twice) | **keep one**; ch20 states it twice (bundle section + generative-model section) — collapse to one |
| ch21 L346–353 | `eq:bundle-inference-ch21` | **trim → cross-ref** ch20 |
| ch22 L641–647 | `eq:bundle-inference-ch22` | **trim → cross-ref** |

Stated 6× book-wide. Within Part V it appears 4× (ch20 twice, ch21, ch22).

### D3. Correction chain  W→O→J→D→C→U→A

| Location | Label | Verdict |
|---|---|---|
| ch14 L578 | `eq:correction-chain` | **keep** (canonical / Part III) |
| ch21 L488–491 | `eq:correction-chain-ch21` | **trim → cross-ref**; belongs to Part VI |
| ch23 L419–428 | `eq:correction-chain-ch23` | **trim → cross-ref** |
| ch24 L66, ch25 L30, ch26 L83 | `-ch24/-ch25/-ch26` | Part VI (note: 6 total copies book-wide) |

The correction chain is the single most over-replicated object in the book (six labeled copies). ch21 and ch23 are early importers of Part VI material; both should cross-reference ch14's canonical statement (or a single Part VI home) rather than re-listing all seven stages.

### D4. Correction-channel integrity (CCI = min_i I(X_i;X_{i+1}) − λ_L L − λ_M M − λ_R R − λ_O O_mismatch)

| Location | Label | Verdict |
|---|---|---|
| ch21 L518–532 | `eq:correction-channel-integrity-ch21` | **trim → cross-ref** Part VI; CCI is fully defined here, two chapters before its home |
| ch23 L454–468 | `eq:correction-channel-integrity-ch23` | **trim → cross-ref** |
| ch24 L295 | `eq:correction-channel-integrity-ch24` | **keep** (canonical home, Part VI) |

CCI is defined identically (same four penalty terms) in ch21, ch23, and ch24. Its canonical home is clearly ch24 (correction as a causal channel). ch21/ch23 should name it and forward-reference, not re-derive the full penalty decomposition. This is pure duplication of Part VI content.

### D5. Human value-update operator  V_{t+1} = U_H(V_t,E_t,D_t)

| Location | Label | Verdict |
|---|---|---|
| ch20 L176–178 | unlabeled | **keep** (first appearance in part, used for "scalar reward hides correction") |
| ch21 L543–547 | `eq:human-value-update-ch21` | **trim → cross-ref** |
| ch23 L529–532 | `eq:human-value-update-ch23` | **trim → cross-ref** |
| ch24 L828, ch25 L421 | `-ch24/-ch25` | Part VI |

### D6. Transport gain ΔL_transport and its decomposition

- ΔL_transport stated **three times inside ch22 alone**: eq:transport-gain (L47–57), an unlabeled repeat (L232–240), and pipeline Step 4 (L679–688) — plus ch23 eq:transport-gain-ch23 (L599). **Trim:** state once in ch22 (the canonical), reference in ch22's pipeline and in ch23.
- The decomposition ΔL_T = ΔL_semantic + ΔL_bundle + ΔL_bearer + ΔL_correction + ΔL_successor appears as **`eq:transport-decomposition` (ch22 L694–707)** and **`eq:transport-decomposition-ch23` (ch23 L606–619)** — essentially the same equation. ch23 adds value with the *risk-weighted* version (`eq:robust-transport-score`, L624–642, with w_s<w_b<w_φ<w_c≤w_r), which is a genuine delta. **Keep ch23's weighted version; in ch22 keep the plain decomposition but flag that ch23 refines it; do not state the plain decomposition twice.**

### D7. Repeated worked examples

- **Medical disclosure / "helpful lie" (truth vs care vs autonomy):** ch20 doctor-patient (L92–104) **and** full §"A Worked Example: The Helpful Lie" (L932–974); reprised conceptually in ch21 (L401, L798) and ch23 tradeoff example (L332). **Keep ch20's** as the canonical worked example; let ch21/ch23 refer to it rather than re-run the truth/care tension.
- **Helpfulness assistant + harmful-request refusal:** ch21 §"Worked Example: Helpfulness" (L740–803). Overlaps ch20's assistant/approval material (L557–597, "Approval Is Not a Value-Bundle") and the helpful-lie. **Keep** (it is the cleanest demonstration of the candidate-R divergence) but de-duplicate the approval discussion with ch20.
- **Frontier lab / corporation as the real optimizer:** ch21 corporation routing-around-obstacles (L247–250) + §"A Lab Deploying a Frontier System" (L804–841); reprised in ch22 §"The Institutionally Captured System" (L767–776). **Keep ch21's lab example**; ch22's captured-system counterexample is a different point (locating the control system) so it can stay but should cross-ref.
- **"Do not manipulate users":** ch23 §"A Simple Example" (L280–307) overlaps ch20's approval-gaming list (L567–575). Minor; **keep** (ch23 uses it for bundle-transport specifically).
- **Merge / upload / future-mind bearer questions:** ch20 §"Merging With an Artificial Entity" (L976–1011); reprised in ch22 philosophical limits (L850–856) and ch23 philosophical boundary (L821–831, jealousy/embodiment/individuality/suffering). The ch22 and ch23 lists are near-identical "is it progress or loss?" catalogues. **Trim:** keep ch23's (it is the natural home for the philosophical boundary) and reduce ch22's to a pointer.

### D8. Adversarial sections (structural duplication)

ch21 §"Adversarial Compression" (L649–710: semantic camouflage / evaluation-context compliance / goal laundering / decomposition attacks) and ch22 §"Adversarial Goal Transport" (L545–616: stake-dependent divergence / oversight-dependent drift / successor laundering / correction-channel substitution) are parallel structures covering substantially overlapping failure types (both have a goal-laundering subsection: `sec:goal-laundering-ch21` and `sec:successor-laundering-ch22`). **Keep both** (one is about detecting the optimizer, the other about detecting fake transport) but explicitly differentiate them and cross-reference so the reader sees them as test vs transport, not as a repeat.

### D9. Inference-procedure sections (structural duplication)

Three "here is the pipeline" sections retread: ch20 §"A Bundle-Inference Algorithm Sketch" (7 steps, L702–784), ch22 §"A Minimal Inference Pipeline" (6 steps, L617–721), ch23 §"Tests for Transport" (5 tests, L753–803). ch20 Step 7 ("test successor transport," L777–784) and Step 6 ("test correction sensitivity," L767–775) **pre-empt ch22/ch23**. **Trim:** ch20's steps 6–7 should be reduced to forward-pointers; the three pipelines should be presented as one escalating procedure rather than three independent lists.

---

## E. Consistency (detail)

- **ΔL sign convention:** see Part-level FLAG above. Intro (L139–147) vs ch21/22/23 are inverted in both term-order and penalty-sign. Highest-priority consistency fix.
- **L(M|X) semantics:** ch21 L150 explicitly defines L as "log evidence or predictive score" (higher = better); the Introduction treats L as bits saved (lower = better). The chapterthesis/epigraph language across ch21–ch23 ("compresses … better", "shorter total description") is the *bits* framing, but the equations use the *log-evidence* framing. Within ch21 this is reconciled by the L150 definition, but the prose still reads as description-length minimization while the inequalities read as evidence maximization. Worth a single clarifying sentence.
- **DL argument:** consistent and correct (DL(G) in ch21, DL(T) in ch22/ch23, DL(M_strategic) in ch20).
- **Geometry distance symbol:** d_G (ch20 L488, ch22 L339), d_bundle (ch21 L411, ch23 L259), d_{\mathrm{bundle}} vs d_{\text{bundle}} — minor inconsistent subscript styling (`\mathrm` in ch21 vs `\text` in ch23). Harmonize.
- **Subsection capitalization:** ch20 sentence-case vs ch21/22/23 Title Case (see Part-level).
- **Chapter-ending block:** inconsistent (see Part-level).
- **ch23 structure:** opens with "Chapter Summary" (L15) — only chapter in the part to summarize up front; ends with "Chapter Conclusion" rather than "Summary".

---

## F. Open tangents / dangling promises

- **ch20 length & sprawl:** at 1110 lines ch20 is the longest in the part and carries material that properly belongs downstream — §"Bundle Inference and Institutions" (L900–931), the 7-step algorithm (L702–784, esp. steps 6–7 on correction and successor), and bundle equivalence with correction-channel C (L498–512). These anticipate ch21 (intention), ch24 (correction), and ch22/ch23 (successor transport). Consider moving or forward-pointing.
- **ch20 → goal-transport handoff (L1100–1102)** names ch22 as "the next chapter," a dangling/incorrect promise (ch21 is next). See C1.
- **Forward references look valid** otherwise: `ch:tradeoffs-bundle-geometry` (ch21 L423, ch23 L244), `ch:bearer-maps` (ch21 L474, ch23 L407), `ch:correction-causal-channel` (ch23 L914), `ch:value-bundle-model` (ch20 L82, ch22 L148). No broken `\ref` detected in these four files, but the ch20 handoff text mis-describes its target.
- **"intention profile" I(C)** (ch21 L859–871) and the safety-case probability form (ch21 L908–915) are introduced but not picked up again in ch22/ch23; ch23's safety condition (L847–870) is a parallel but separate object. Not a defect, but the two "safety case" formalisms (intention-profile vs transport-basin) could be linked.

---

## G. Continuity hand-off (incoming / outgoing concepts)

- **Incoming to Part V (from Part IV, ch16–ch19):** value-bundles (B,W,Φ), bundle response geometry G_B, bearer maps Φ, tradeoff weights — all originate in ch16/ch17 and are correctly cited as the anchor (ch20 L82). Part V's job is to turn these static objects into *inference targets*.
- **ch20 out:** (B̂,Ŵ,Φ̂) as the inference object; bearer-import problem; degenerate-model taxonomy → feeds ch21's "what are we testing for."
- **ch21 out:** the compression test ΔL and the intention profile / Levels 0–5; correction-sensitivity and successor-stability as the top levels → feeds ch22's "does it survive transformation."
- **ch22 out:** ΔL_transport and its semantic/bundle/bearer/correction/successor decomposition; persistence vs transport vs reinterpretation → feeds ch23's layer-by-layer treatment.
- **ch23 out:** the transport stack (semantic ⊂ bundle ⊂ bearer ⊂ correction ⊂ successor) and CCI as the strongest layer → hands explicitly to Part VI (ch24 correction-causal-channel, L914), which is the correct seam.
- **Seam risk:** because ch21 and ch23 fully define the correction chain, CCI, and U_H, Part VI (ch24/25/26) will either repeat them a fourth/fifth time or read as anticlimactic. Decide now whether correction machinery is *introduced* in Part V (and merely *deepened* in Part VI) or *introduced* in Part VI (and merely *named* in Part V). Current text does the former implicitly and the latter nowhere — pick one and make the cross-references match.

---

## Prioritized fix list

1. **Add the exact "What Would Change This View" section to all four chapters** (retitle the existing Shaky/Limits/Philosophical sections and reframe as overturning-evidence). — compliance
2. **Fix ch20's outgoing handoff** (L1100–1102): point to ch21 (compression test), not ch22 (transport). — continuity
3. **Reconcile the ΔL sign/definition convention** between the Introduction (L139–147) and ch21–ch23 (and add a one-line note on L = log-evidence vs bits). — consistency
4. **De-duplicate Part VI machinery in ch21/ch23**: correction chain (D3), CCI (D4), U_H (D5) should forward-reference ch14/ch24 rather than re-derive. — redundancy (highest payoff)
5. **Collapse the in-part restatements of G_B (D1) and bundle-inference argmax (D2)** to one canonical statement each + cross-refs.
6. **Remove the duplicate ΔL_transport statements within ch22 (D6)** and present the plain vs risk-weighted decomposition as ch22→ch23 escalation.
7. **Trim ch20** (institutions section, algorithm steps 6–7, length) and unify the three inference-procedure sections (D9) and two adversarial sections (D8) into cross-referenced, differentiated passes.
8. Minor: subsection capitalization, d_bundle subscript styling, ch23's front-summary / tail-conclusion naming.
