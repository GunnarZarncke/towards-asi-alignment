# Review — PART VI: Correction Channels (ch24–ch27)

Reviewer pass. Read in full and in order: ch24, ch25, ch26, ch27. Cross-checked against ch21, ch23 (Part V), ch28 (Part VII), ch04, ch42. No manuscript files were edited.

Part file: `parts/part06-correction-channels.tex` (4 chapters, no part-level prose intro — just `\part{Correction Channels}` + four `\input`s).

---

## A. Capsules

- **ch24 `ch:correction-causal-channel` — "Correction Is a Causal Channel."** Introduces the chain `W→O→J→D→C→U→A` (eq:correction-chain-ch24, L52–67), distinguishes correction from obedience (process- vs action-level, L96–103), builds a minimal causal model (Θ,Z,U,I), defines CCI with five penalty terms (eq:correction-channel-integrity-ch24, L281–296), walks the bottlenecks (observability, comprehensibility, deliberation, authority, latency, manipulation, ontology, irreversibility), four-level correction (action/policy/weights/bearer, L674–686), defines the **strong correction channel** (L731–733), relates to corrigibility and CEV, gives four worked examples, seven failure modes, an audit profile, a necessity proposition (L1101), governance + civilizational framing, design rules. Foundational and the longest chapter (1244 lines). **Ends "Chapter Summary"; has NO "What Would Change This View."**

- **ch25 `ch:correction-channel-integrity` — "Correction-Channel Integrity."** Re-states the chain (eq:correction-chain-ch25, L28–31) and a CCI functional (eq:cci-ch25, L33–46) — note four penalty terms with `Ω` not five with `O_mis`/`G`. Adds the value-bundle version of correction, Coerced Correction (CCI_legit, eq:cci-legit, L256–267), extrapolative correction + extrapolation-capture, directional transparency / manipulation exposure / surveillance alignment (the genuinely novel material, L507–545), correction under ontology shift / capability growth / successor creation, self-modeling vs self-transparency, institutional correction, Goodharting, observable metrics, stop/start/continue criteria, two worked examples, a 6-claim safety-case template, a compact formal summary, 10 failure modes. **Ends "Chapter Conclusion"; has NO "What Would Change This View"** (the section "What Integrity Does Not Solve," L1083, is about scope limits, not falsification — not an equivalent).

- **ch26 `ch:extrapolative-correction` — "Beyond Following Instruction."** The obedience trap (3 reasons it breaks), re-states the chain (eq:correction-chain-ch26, L69–84) and CCI (eq:cci-ch26, L120–133), from commands to value updates, four legitimacy criteria as subsections (truth-contact, agency, plurality, reversibility, non-manipulation — actually five), value-bundle geometry, the **strong correction channel** with **six** levels (act/policy/model/bundle/bearer/successor, eq:strong-correction-levels-ch26, L358–369), civilizational self-governance, operational criteria, relation to CEV, the desired guarantee. **Has a proper "What Would Change This View" (L604) and "Summary" (L620).**

- **ch27 `ch:manipulation-false-consent` — "Manipulation, Domestication, and False Consent."** Service vs manipulation by causal pathway, re-states chain + CCI (L57–101), value bundles as manipulation target (4 levels incl. update-operator capture), a causal-mediation manipulation index (Bypass/Total, L201–222), persuasion/manipulation/paternalism/domestication subsections, agency-capacity formula 𝒜_H (L290–292), false consent as channel-condition failure (L334–390), preference laundering, domestication gradient, self-transparency asymmetry + corrigibility theater, the No-Bypass Principle (L514–515), relation to CEV, when value change is legitimate (7 criteria), 5 examples/counterexamples, institutional manipulation, 7 operational tests, red flags, design constraints, philosophical limit. **Has a proper "What Would Change This View" (L858) and "Summary" (L873).** Cleanest, most differentiated chapter in the part.

---

## B. Required-element compliance

| Element | ch24 | ch25 | ch26 | ch27 |
|---|---|---|---|---|
| `\chapter` + `\label` | ✓ L1–2 | ✓ L1–2 | ✓ L1–2 | ✓ L1–2 |
| `chapterthesis` env | ✓ L4–7 | ✓ L4–7 | ✓ L4–7 | ✓ L4–6 |
| Decision relevance | ✓ design rules L1182, governance L1119 | ✓ stop/start/continue L931, safety case L1109 | ✓ operational criteria L476, red flags L509 | ✓ operational tests L662, design constraints L778 |
| Failure-mode / counterexample | ✓ Failure Modes L925 | ✓ Failure Modes L1228 | ✓ red flags L509 + WWCTV | ✓ Examples & Counterexamples L595, Red Flags L758 |
| **EXACT "What Would Change This View"** | **✗ MISSING — flag** | **✗ MISSING — flag** | ✓ L604 | ✓ L858 |
| Summary | "Chapter Summary" L1216 | "Chapter Conclusion" L1263 | "Summary" L620 | "Summary" L873 |
| `refsection` + `\printbibliography` | ✓ L9 / L1242 | ✓ L9 / L1294 | ✓ L9 / L653 | ✓ L8 / L908 |

- **Two hard compliance gaps:** ch24 and ch25 both lack the mandated "What Would Change This View" section. They instead end on falsification-free summaries. ch24's "A Proposition" (L1098) states a necessity claim but gives no view-changing conditions; ch25's "What Integrity Does Not Solve" disclaims scope but lists no falsifiers. Both need a WWCTV added (ch26/ch27 supply good templates: each lists 5 conditions that would force revision).
- **No `[STUB]` / `[TODO]` markers** anywhere in the four chapters (grep clean).
- All four chapterthesis envs are substantive and on-spine. ch26's epigraph (L11–14) is a near-verbatim copy of its own chapterthesis first two sentences (L5–7) — minor self-duplication, cosmetic.

---

## C. Continuity / escalation (ch24→25→26→27; handoff from ch23, to ch28)

Intended escalation: **channel (ch24) → integrity measurement (ch25) → extrapolative target (ch26) → manipulation/false consent (ch27).** The escalation is conceptually real and the forward pointers are wired correctly:

- ch24 → ch25: L1236 "The next chapter develops correction-channel integrity as a measurable quantity (Chapter~\ref{ch:correction-channel-integrity})."
- ch25 → ch26: L1288 "The next chapter develops extrapolative correction in its own right (Chapter~\ref{ch:extrapolative-correction})."
- ch26 → ch27: L437 forward-refs ch27 as the place manipulation/domestication/false-consent are developed as channel attacks.
- Incoming from ch23 (`ch:transport-types`, Part V): ch23 §"Correction Transport" (L409–482) already introduces the **same chain (eq:correction-chain-ch23, L427)** and the **same CCI with the same five-term wording (eq:correction-channel-integrity-ch23, L455–467)**. So Part VI opens by re-deriving what Part V already stated. ch24 does not reference ch23's correction-transport section at all.
- Outgoing to ch28 (`ch:successor-central-test`): clean. ch28's thesis (L5) lists "correction integrity" among successor-preserved invariants and generalizes the ch25/ch26/ch27 successor-inheritance material. Good handoff; no missing bridge.

**The serious continuity problem is ch24 vs ch25.** They do not cleanly divide labor:

- Both define the chain (ch24 L52, ch25 L28 + again L99 + again L1162).
- Both define CCI (ch24 L281, ch25 L33 + again L162 + again L1184).
- Both do the per-bottleneck mutual-information walk (ch24 §Observability–§Irreversibility; ch25 §"The Correction Chain" L123–151 + §"Observable Metrics" L816–929).
- Both define a "strong correction channel" (ch24 L726/L731; ch26 L348 — see D).
- Both relate to CEV (ch24 §L810; ch25 §L397/L448).
- Both define the four-/six-level correction taxonomy (ch24 four levels L674; ch26 six levels L358).
- Both give worked examples (ch24 four; ch25 two).
- Both give a failure-mode catalogue (ch24 seven; ch25 ten — overlapping).
- Both give an audit/metric list (ch24 §Measuring CCI L1010; ch25 §Observable Metrics L816).

ch24 is billed as "what is a correction channel" and ch25 as "how to measure it," but ch24 already fully introduces and motivates the *measure* (CCI, the audit profile, the seven quantities, adversarial testing), and ch25 re-introduces the *concept* (chain, bottlenecks, strong version) before measuring. The boundary is blurred in both directions. See recommendation in D.

---

## D. Redundancy enumeration

### D1. The correction-chain equation `W→O→J→D→C→U→A`
Stated **six** times across the book, three within this part:
- ch21 L490 `eq:correction-chain-ch21`
- ch23 L427 `eq:correction-chain-ch23` (Part V)
- ch24 L52–67 `eq:correction-chain-ch24` (with full itemized letter glossary L68–77)
- ch25 L28–31 `eq:correction-chain-ch25` **and again** L99–112 (description-list glossary L114–122) **and again** L1162–1176 (compact summary)
- ch26 L69–84 `eq:correction-chain-ch26` (itemized glossary L86–94)
- ch27 L57–61 (itemized glossary L65–73)

**Verdict:** canonical statement should be **one** — recommend ch24 L52–77 as the canonical full definition (it is the chapter literally titled for it). **Trim/cross-ref (true duplication):** ch25 L28–31 and especially the *second* in-chapter restatement at L99–122, ch26 L69–94, ch27 L57–73 should be reduced to `\eqref{eq:correction-chain-ch24}` + a one-line reminder. ch25's *third* statement (L1162, in "A Compact Formal Summary") is **keep (pedagogical)** — a deliberate recap. The ch21/ch23 copies are out of Part VI's scope but worth noting: ch23 already owns a near-complete copy, so a single canonical home + cross-refs across the whole book is the right fix.

### D2. The CCI functional
- ch23 L455–467 `eq:correction-channel-integrity-ch23`: `min_i I − λ_L L − λ_M M − λ_R R − λ_O O_mismatch` (4 penalties)
- ch24 L281–296 `eq:correction-channel-integrity-ch24`: `C_raw − λ_L L − λ_M M − λ_R R − λ_O O_mis − λ_G G` (**5 penalties, adds Goodhart G**)
- ch25 L33–46 `eq:cci-ch25` and L162–173: `C_corr − λ_L L − λ_M M − λ_R R − λ_Ω Ω` (**4 penalties, ontology term renamed Ω**) — restated a third time at L1184.
- ch26 L120–133 `eq:cci-ch26`: `C_raw − λ_L L − λ_M M − λ_R R − λ_O O_mis` (4 penalties)
- ch27 L88–101: `C_corr − λ_L L − λ_M M − λ_R R − λ_O O_mismatch` (4 penalties)

**Verdict:** This is both redundancy **and** inconsistency (see E1). Canonical home should be ch25 (the chapter titled "Correction-Channel Integrity"). **Trim/cross-ref:** ch26 L120–133 and ch27 L88–101 restate the full functional unnecessarily — replace with `\eqref{eq:cci-ch25}` + the one penalty term each chapter actually uses. ch24's statement is defensible as the *introduction* of the quantity but should then be reconciled with ch25 (right now ch24's is the richest — 5 terms — yet the "measurement" chapter ch25 drops a term). ch26 L135 already cross-refs ch25 ("develops a closely related functional with additional operational detail"), which is the correct move; just apply it to the equation itself instead of restating.

### D3. The "strong correction channel" / multi-level correction taxonomy
- ch24 L656–686: **four** levels via `eq:four-level-correction` C=(C^A, C^π, C^W, C^Φ) — action / policy / bundle-weights / bearer.
- ch24 L726–768: `\begin{definition}[Strong correction channel]` + five requirements (sensitivity, specificity, depth, timeliness, self-preservation).
- ch26 L348–369: "The Strong Correction Channel" again, now **six** levels `eq:strong-correction-levels-ch26` C=(act, policy, model, bundle, bearer, successor) with a subsection per level (L376–428).

**Verdict:** **trim/partial duplication.** Two different arities (four vs six) for the same taxonomy is confusing (see E). The six-level version (ch26) is the superset and the better home for the *definition* (it adds model and successor levels). Recommend: ch24 keeps a brief four-→deeper-levels motivation but cross-refs ch26 for the canonical taxonomy, or ch24 adopts the six-level version up front. The "Strong correction channel" *definition box* appears once (ch24 L731) and the *section heading* "The Strong Correction Channel" appears in both ch24 (L726) and ch26 (L348) — duplicate section title within one part.

### D4. The CEV comparison — stated **four** times in this part
- ch24 §"Relation to Coherent Extrapolated Volition" L810–852.
- ch25 §"The Strong Version: Extrapolative Correction" L397–452 (CEV contrast L448).
- ch26 §"Relation to Coherent Extrapolated Volition" L532–558.
- ch27 §"Relation to Coherent Extrapolated Volition" L523–561.

All four make the **same point**: preserve the update process `V_{t+1}=U_H(V_t,E_t,D_t)` rather than compute-and-optimize a guessed fixed point `V*`/`V̂_∞`. ch26 and ch27 even use identical section titles. The `eq:human-value-update` equation recurs: ch24 L827 (`-ch24`), ch25 L417 (`-ch25`), ch26 L162 (`-ch26`), ch27 L539.

**Verdict:** the *full* CEV-contrast belongs once. **Keep (pedagogical):** one canonical treatment — recommend ch26 (the "Beyond Following Instruction" chapter is where extrapolation is the explicit subject) as canonical, with ch24/ch25/ch27 reduced to a one-sentence reminder + `\ref`. Currently ch24, ch26, ch27 each re-derive the V*-vs-process distinction nearly verbatim — **trim/cross-ref (true duplication).** This is the single most repeated argument in the part.

### D5. Legitimacy criteria (truth-contact, agency, plurality, reversibility, non-manipulation)
- ch25 L484–502: `Q(U)=q_T+q_A+q_R+q_P+q_D+q_C` (six quality terms).
- ch26 §"What Makes an Update Legitimate?" L217–293: five subsections (truth-contact, agency preservation, plurality, reversibility/option, non-manipulation), each with an inequality.
- ch27 §"When Value Change Is Legitimate" L562–593: seven-item legitimacy list + seven-item corruption list.
- Also recurs outside the part: ch04 and ch42 (per task brief).

**Verdict:** **keep (pedagogical) but de-duplicate the operational core.** ch26's five-criterion subsection set and ch27's seven-item list overlap heavily (truth-contact, agency, plurality, reversibility, non-manipulation appear in both). They serve different framings (ch26 = legitimate *update*; ch27 = legitimate *value change*), so total merge is not warranted, but they should cross-reference and avoid re-stating the same inequalities. Recommend one canonical criteria home (ch26) and have ch27's list cite it where it overlaps, keeping only ch27's distinct items (bearer-expansion-under-scrutiny, non-exploitation, continuity-of-correction).

### D6. Repeated worked examples (recommender / companion / medical / governance planner)
- **Recommender system:** ch24 §L893–909 ("avoid label x" vs "stop exploiting my anger"); ch27 §L598–604 ("Recommender That Makes Itself Necessary"). Same mechanism (engagement optimization corrupts the corrector). **Partial duplication** — keep both but they could cross-ref; ch27's is richer.
- **AI companion / dependency:** ch25 §"AI Companion Value Drift" L1044–1082; ch27 §"Companionship" L473–475 + woven through domestication. **Keep** — ch25 is quantitative (W_care,autonomy shift), ch27 is taxonomic; complementary.
- **Medical AI:** ch24 §L881–891; ch25 case 3 L71–73; ch27 design constraint L785. Light, complementary, **keep**.
- **Governance/city planner:** ch25 §"The Helpful Planner" L990–1042; ch27 §"Governance System That Ends Conflict" L614–618. Same scenario (city AI degrades political correction). **Partial duplication** — cross-ref; ch25 quantitative, ch27 illustrative.

**Verdict:** examples are mostly **keep (pedagogical)** because they illustrate different formal points, but recommender and governance-planner appear in two chapters with the same moral and should cross-reference rather than re-establish the setup.

### D7. Failure-mode catalogues
ch24 §Failure Modes (L925, 7 items) and ch25 §Failure Modes (L1228, 10 items) overlap substantially: decorative/ceremonial correction, surface/local compliance, ontology drift/laundering, preference capture/judge shaping, authority decay, successor escape/amnesia, self-control-outpaces-transparency. **Trim:** ch25's list is the superset (adds surveillance alignment, extrapolation capture, institutional narrowing). Recommend ch24 keep a short pointer and let ch25 own the canonical catalogue, or differentiate explicitly (ch24 = channel-mechanism failures, ch25 = integrity-measurement failures).

### Merge-vs-divide assessment (ch24 / ch25)
ch24 (1244 L) and ch25 (1296 L) together duplicate: the chain, CCI, the bottleneck MI walk, the strong-channel idea, CEV, failure modes, and the audit/metric list. Two viable fixes:
1. **Sharper division (recommended):** ch24 = *conceptual* ("correction is a causal channel; here is the chain, the bottlenecks, why it is not obedience, relation to corrigibility") and **stop before** introducing the CCI penalty functional, the audit profile, and adversarial testing. ch25 = *operational* (CCI functional, penalties, coerced correction, metrics, stop/start/continue, safety case, successor/ontology/capability stress). This requires moving ch24 §"Measuring CCI" (L1010), §"Adversarial Testing" (L1073), and the CCI equation (L281) out of ch24 into ch25, and demoting ch24's CEV section to a pointer.
2. **Merge** into one long "Correction Channels and Their Integrity" chapter. Not recommended — the part already has a clean 4-beat arc and ch25's extrapolative/surveillance material is distinct enough to keep ch26 separate; a single merged ch24+25 would be ~2000 lines and unbalance the part.

Net: **divide more sharply**, do not merge. The current overlap is ~30–40% conceptual duplication between ch24 and ch25.

---

## E. Consistency

### E1. CCI penalty-term inconsistency (substantive)
The CCI functional is **not** consistent across chapters:
- ch24 (L281): **five** penalties incl. Goodhart `λ_G G`; ontology term `O_mis`. Capacity term `C_raw`.
- ch25 (L162): **four** penalties; ontology term renamed `Ω` (`λ_Ω Ω`); **drops Goodhart G**; capacity term `C_corr`.
- ch26 (L120): four penalties; ontology `O_mis`; capacity `C_raw`.
- ch27 (L88): four penalties; ontology `O_mismatch`; capacity `C_corr`.
- ch23 (L455): four penalties; ontology `O_mismatch`; capacity `min_i I`.

Problems: (a) ch24 introduces a fifth term (Goodhart) that the dedicated measurement chapter ch25 silently drops, even though ch25 has a whole §"Goodharting the Correction Channel" (L769) — so Goodhart pressure is discussed but no longer a penalty term. (b) the ontology penalty is written four different ways: `O_mis`, `Ω`, `O_mismatch`. (c) the capacity term alternates `C_raw` / `C_corr` / `min_i I`. **Recommend** one canonical functional (pick ch25's home, decide whether Goodhart is a penalty term or folded into M/manipulation, and fix one symbol for the ontology term and one for capacity) and `\eqref` everywhere else.

### E2. Correction-chain letter definitions — consistent
The seven variables `W,O,J,D,C,U,A` are defined identically in ch24 (L68–77), ch25 (L114–122), ch26 (L86–94), ch27 (L65–73) and ch23 (L429–438). Good — no semantic drift in the letters. (Only redundancy, per D1, not inconsistency.) Minor: ch24 calls `W_t` "world state at time t" and later reuses `W` inside `Z_t=(B_t,W_t,Φ_t)` at L167 to mean **tradeoff weights**, then again `W_{ij}` as tradeoff weights in ch25 L302 — `W` is overloaded (world state vs tradeoff weights). Worth a notation note; the appendix `appA-notation` should disambiguate.

### E3. Multi-level correction arity — inconsistent
Four levels in ch24 (action/policy/weights/bearer, L674) vs six levels in ch26 (act/policy/model/bundle/bearer/successor, L358). Reconcile to one taxonomy (six-level is the superset). See D3.

### E4. Section-title capitalization — consistent within part
All four chapters use title case for `\section{...}` (e.g., "Why Correction Is Not Obedience," "The Strong Correction Channel"). ch28 (next part) switches to sentence case ("The local alignment fallacy," "What counts as a successor?") — a cross-part inconsistency to note for whoever owns global style, but within Part VI capitalization is uniform.

### E5. Chapter-ending naming — inconsistent (flagged in brief, confirmed)
Four different endings: ch24 "Chapter Summary," ch25 "Chapter Conclusion," ch26 "Summary," ch27 "Summary." Recommend standardizing to one (the part already leans "Summary" 2/4; ch26/ch27 are the WWCTV-compliant chapters, so "Summary" is the de-facto house style). Standardizing would also help because ch24/ch25's non-"Summary" endings coincide with the missing-WWCTV problem.

### E6. Epigraph style — consistent
All four use `\epigraph{...}{}` with empty attribution. Fine.

---

## F. Open tangents / dangling promises

- **ch25 L544** forward-refs `ch:value-change-at-stake` (ch41) and `ch:unconscious-value-drift` (ch42) for privacy/legibility — valid, those chapters exist.
- **ch25 L275** "Bargaining, blackmail, and coercion are treated here as correction-channel pathology---not as a separate book part." This is an editorial promise/justification for *not* having a part; fine but slightly meta. No dangling ref.
- **ch24 L85** refs `ch:transport-types` (ch23) — valid, but note ch24 never acknowledges that ch23 already defined the same chain+CCI (the incoming duplication in C is silent).
- **ch26 L437** promises ch27 will develop manipulation/domestication/false consent "as correction-channel attacks" — fulfilled.
- **ch26/ch27** both ref `christiano2018corrigibility`, `russell2019human` for "the system may assist deliberation" — consistent.
- No unresolved `\ref` placeholders, no "(forthcoming)", no `\todo` notes detected. No orphan equations labeled-but-unreferenced that are problematic (most labeled equations are referenced or are intentional display recaps).
- Mild tangent: ch24 §"Correction as Civilizational Self-Modification" (L1150) and ch26 §"Civilizational Self-Governance" (L439) and ch27 §"The Philosophical Limit" (L835) all three reach the same "governed vs ungoverned value change" coda (ch24 L1162–63, ch26 L644–47, ch27 L856 use near-identical phrasing: "The choice is between governed transformation and ungoverned drift"). Three chapters end on the same civilizational note — rhetorically repetitive; consider letting ch27 (part finale) own it.

---

## G. Continuity hand-off (incoming / outgoing concepts)

**Incoming (from Part V / ch23):**
- correction chain `W→O→J→D→C→U→A` — already present in ch23 L427 (and ch21 L490). Part VI inherits, then re-derives (see D1).
- CCI functional — already present in ch23 L455. Part VI inherits, then re-derives (see D2).
- value bundles `B`, bearer maps `Φ`, tradeoff weights `W` — from ch16 `ch:value-bundle-model` / `ch:bearer-maps` / `ch:tradeoffs-bundle-geometry`; ch24 L164–174, ch25 L286–304, ch26 L299–312 use them, correctly cross-referenced.
- goal transport / goal laundering — ch22, ch37; ch25 L587 ("goal laundering at the level of values") and ch26 echo it.

**Outgoing (to Part VII / ch28+):**
- successor-closure / correction inheritance — ch25 §"Correction Under Successor Creation" (L630, `eq:recursive-successor-cci` L671) and ch26 §"Successor Correction" (L421) and ch27 §"Successor Non-Manipulation" (L821) all set up ch28's central thesis. ch28 L5 explicitly carries "correction integrity" forward as a successor-preserved invariant. Clean baton-pass.
- CCI as a safety-case object → ch25's 6-claim safety-case template (L1109) and `eq:cci-safety-case` (L1213) feed Part IX (safety cases) and `appG-safety-case-template` / `appD-correction-channel-audit`.
- manipulation/legibility → ch41/ch42 (value change, drift), forward-referenced from ch25 L544.

**No missing bridges** into or out of the part; the only hand-off defect is that the **incoming** duplication from ch23 is unacknowledged (ch24 should open by referencing ch23's correction-transport section rather than redefining the chain and CCI from scratch).

---

## Priority fix list (for whoever edits)

1. **Add "What Would Change This View" to ch24 and ch25** (hard required-element gap). Use ch26 L604 / ch27 L858 as templates.
2. **Reconcile the CCI functional** (E1): one canonical equation, decide Goodhart-term in/out, fix `O_mis`/`Ω`/`O_mismatch` to one symbol and `C_raw`/`C_corr` to one. Canonical home = ch25.
3. **De-duplicate the CEV contrast** (D4): canonical in ch26, reduce ch24/ch25/ch27 to a sentence + `\ref`.
4. **Divide ch24/ch25 more sharply** (C, D-merge): move CCI measurement/audit/adversarial-testing out of ch24 into ch25; ch24 stays conceptual.
5. **Unify the strong-channel taxonomy** to six levels (D3, E3) and avoid the duplicate "The Strong Correction Channel" section title across ch24/ch26.
6. **Standardize chapter endings** to "Summary" (E5) and the recurring "governed vs ungoverned" coda to a single chapter (F).
7. Single canonical home for the correction-chain equation (D1) + legitimacy criteria (D5); cross-ref the rest.
