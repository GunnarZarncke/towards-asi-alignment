# Review — PART VI: Correction Channels (ch46–ch48)

Reviewer pass. Read in full and in order: ch46, ch46, ch46, ch48. Cross-checked against ch46, ch46 (Part V), ch46 (Part VII), ch04, ch46. No manuscript files were edited.

Part file: `parts/part06-correction-channels.tex` (4 chapters, no part-level prose intro — just `\part{Correction Channels}` + four `\input`s).

---

## A. Capsules

- **ch46 `ch:correction-causal-channel` — "Correction Is a Causal Channel."** Introduces the chain `W→O→J→D→C→U→A` (eq:correction-chain-ch46, L52–67), distinguishes correction from obedience (process- vs action-level, L96–103), builds a minimal causal model (Θ,Z,U,I), defines CCI with five penalty terms (eq:correction-channel-integrity-ch46, L281–296), walks the bottlenecks (observability, comprehensibility, deliberation, authority, latency, manipulation, ontology, irreversibility), four-level correction (action/policy/weights/bearer, L674–686), defines the **strong correction channel** (L731–733), relates to corrigibility and CEV, gives four worked examples, seven failure modes, an audit profile, a necessity proposition (L1101), governance + civilizational framing, design rules. Foundational and the longest chapter (1244 lines). **Ends "Chapter Summary"; has NO "What Would Change This View."**

- **ch46 `ch:correction-channel-integrity` — "Correction-Channel Integrity."** Re-states the chain (eq:correction-chain-ch46, L28–31) and a CCI functional (eq:cci-ch46, L33–46) — note four penalty terms with `Ω` not five with `O_mis`/`G`. Adds the value-bundle version of correction, Coerced Correction (CCI_legit, eq:cci-legit, L256–267), extrapolative correction + extrapolation-capture, directional transparency / manipulation exposure / surveillance alignment (the genuinely novel material, L507–545), correction under ontology shift / capability growth / successor creation, self-modeling vs self-transparency, institutional correction, Goodharting, observable metrics, stop/start/continue criteria, two worked examples, a 6-claim safety-case template, a compact formal summary, 10 failure modes. **Ends "Chapter Conclusion"; has NO "What Would Change This View"** (the section "What Integrity Does Not Solve," L1083, is about scope limits, not falsification — not an equivalent).

- **ch46 `ch:extrapolative-correction` — "Beyond Following Instruction."** The obedience trap (3 reasons it breaks), re-states the chain (eq:correction-chain-ch46, L69–84) and CCI (eq:cci-ch46, L120–133), from commands to value updates, four legitimacy criteria as subsections (truth-contact, agency, plurality, reversibility, non-manipulation — actually five), value-bundle geometry, the **strong correction channel** with **six** levels (act/policy/model/bundle/bearer/successor, eq:strong-correction-levels-ch46, L358–369), civilizational self-governance, operational criteria, relation to CEV, the desired guarantee. **Has a proper "What Would Change This View" (L604) and "Summary" (L620).**

- **ch48 `ch:manipulation-false-consent` — "Manipulation, Domestication, and False Consent."** Service vs manipulation by causal pathway, re-states chain + CCI (L57–101), value bundles as manipulation target (4 levels incl. update-operator capture), a causal-mediation manipulation index (Bypass/Total, L201–222), persuasion/manipulation/paternalism/domestication subsections, agency-capacity formula 𝒜_H (L290–292), false consent as channel-condition failure (L334–390), preference laundering, domestication gradient, self-transparency asymmetry + corrigibility theater, the No-Bypass Principle (L514–515), relation to CEV, when value change is legitimate (7 criteria), 5 examples/counterexamples, institutional manipulation, 7 operational tests, red flags, design constraints, philosophical limit. **Has a proper "What Would Change This View" (L858) and "Summary" (L873).** Cleanest, most differentiated chapter in the part.

---

## B. Required-element compliance

| Element | ch46 | ch46 | ch46 | ch48 |
|---|---|---|---|---|
| `\chapter` + `\label` | ✓ L1–2 | ✓ L1–2 | ✓ L1–2 | ✓ L1–2 |
| `chapterthesis` env | ✓ L4–7 | ✓ L4–7 | ✓ L4–7 | ✓ L4–6 |
| Decision relevance | ✓ design rules L1182, governance L1119 | ✓ stop/start/continue L931, safety case L1109 | ✓ operational criteria L476, red flags L509 | ✓ operational tests L662, design constraints L778 |
| Failure-mode / counterexample | ✓ Failure Modes L925 | ✓ Failure Modes L1228 | ✓ red flags L509 + WWCTV | ✓ Examples & Counterexamples L595, Red Flags L758 |
| **EXACT "What Would Change This View"** | **✗ MISSING — flag** | **✗ MISSING — flag** | ✓ L604 | ✓ L858 |
| Summary | "Chapter Summary" L1216 | "Chapter Conclusion" L1263 | "Summary" L620 | "Summary" L873 |
| `refsection` + `\printbibliography` | ✓ L9 / L1242 | ✓ L9 / L1294 | ✓ L9 / L653 | ✓ L8 / L908 |

- **Two hard compliance gaps:** ch46 and ch46 both lack the mandated "What Would Change This View" section. They instead end on falsification-free summaries. ch46's "A Proposition" (L1098) states a necessity claim but gives no view-changing conditions; ch46's "What Integrity Does Not Solve" disclaims scope but lists no falsifiers. Both need a WWCTV added (ch46/ch48 supply good templates: each lists 5 conditions that would force revision).
- **No `[STUB]` / `[TODO]` markers** anywhere in the four chapters (grep clean).
- All four chapterthesis envs are substantive and on-spine. ch46's epigraph (L11–14) is a near-verbatim copy of its own chapterthesis first two sentences (L5–7) — minor self-duplication, cosmetic.

---

## C. Continuity / escalation (ch46→25→26→27; handoff from ch46, to ch46)

Intended escalation: **channel (ch46) → integrity measurement (ch46) → extrapolative target (ch46) → manipulation/false consent (ch48).** The escalation is conceptually real and the forward pointers are wired correctly:

- ch46 → ch46: L1236 "The next chapter develops correction-channel integrity as a measurable quantity (Chapter~\ref{ch:correction-channel-integrity})."
- ch46 → ch46: L1288 "The next chapter develops extrapolative correction in its own right (Chapter~\ref{ch:extrapolative-correction})."
- ch46 → ch48: L437 forward-refs ch48 as the place manipulation/domestication/false-consent are developed as channel attacks.
- Incoming from ch46 (`ch:transport-types`, Part V): ch46 §"Correction Transport" (L409–482) already introduces the **same chain (eq:correction-chain-ch46, L427)** and the **same CCI with the same five-term wording (eq:correction-channel-integrity-ch46, L455–467)**. So Part VI opens by re-deriving what Part V already stated. ch46 does not reference ch46's correction-transport section at all.
- Outgoing to ch46 (`ch:successor-central-test`): clean. ch46's thesis (L5) lists "correction integrity" among successor-preserved invariants and generalizes the ch46/ch46/ch48 successor-inheritance material. Good handoff; no missing bridge.

**The serious continuity problem is ch46 vs ch46.** They do not cleanly divide labor:

- Both define the chain (ch46 L52, ch46 L28 + again L99 + again L1162).
- Both define CCI (ch46 L281, ch46 L33 + again L162 + again L1184).
- Both do the per-bottleneck mutual-information walk (ch46 §Observability–§Irreversibility; ch46 §"The Correction Chain" L123–151 + §"Observable Metrics" L816–929).
- Both define a "strong correction channel" (ch46 L726/L731; ch46 L348 — see D).
- Both relate to CEV (ch46 §L810; ch46 §L397/L448).
- Both define the four-/six-level correction taxonomy (ch46 four levels L674; ch46 six levels L358).
- Both give worked examples (ch46 four; ch46 two).
- Both give a failure-mode catalogue (ch46 seven; ch46 ten — overlapping).
- Both give an audit/metric list (ch46 §Measuring CCI L1010; ch46 §Observable Metrics L816).

ch46 is billed as "what is a correction channel" and ch46 as "how to measure it," but ch46 already fully introduces and motivates the *measure* (CCI, the audit profile, the seven quantities, adversarial testing), and ch46 re-introduces the *concept* (chain, bottlenecks, strong version) before measuring. The boundary is blurred in both directions. See recommendation in D.

---

## D. Redundancy enumeration

### D1. The correction-chain equation `W→O→J→D→C→U→A`
Stated **six** times across the book, three within this part:
- ch46 L490 `eq:correction-chain-ch46`
- ch46 L427 `eq:correction-chain-ch46` (Part V)
- ch46 L52–67 `eq:correction-chain-ch46` (with full itemized letter glossary L68–77)
- ch46 L28–31 `eq:correction-chain-ch46` **and again** L99–112 (description-list glossary L114–122) **and again** L1162–1176 (compact summary)
- ch46 L69–84 `eq:correction-chain-ch46` (itemized glossary L86–94)
- ch48 L57–61 (itemized glossary L65–73)

**Verdict:** canonical statement should be **one** — recommend ch46 L52–77 as the canonical full definition (it is the chapter literally titled for it). **Trim/cross-ref (true duplication):** ch46 L28–31 and especially the *second* in-chapter restatement at L99–122, ch46 L69–94, ch48 L57–73 should be reduced to `\eqref{eq:correction-chain-ch46}` + a one-line reminder. ch46's *third* statement (L1162, in "A Compact Formal Summary") is **keep (pedagogical)** — a deliberate recap. The ch46/ch46 copies are out of Part VI's scope but worth noting: ch46 already owns a near-complete copy, so a single canonical home + cross-refs across the whole book is the right fix.

### D2. The CCI functional
- ch46 L455–467 `eq:correction-channel-integrity-ch46`: `min_i I − λ_L L − λ_M M − λ_R R − λ_O O_mismatch` (4 penalties)
- ch46 L281–296 `eq:correction-channel-integrity-ch46`: `C_raw − λ_L L − λ_M M − λ_R R − λ_O O_mis − λ_G G` (**5 penalties, adds Goodhart G**)
- ch46 L33–46 `eq:cci-ch46` and L162–173: `C_corr − λ_L L − λ_M M − λ_R R − λ_Ω Ω` (**4 penalties, ontology term renamed Ω**) — restated a third time at L1184.
- ch46 L120–133 `eq:cci-ch46`: `C_raw − λ_L L − λ_M M − λ_R R − λ_O O_mis` (4 penalties)
- ch48 L88–101: `C_corr − λ_L L − λ_M M − λ_R R − λ_O O_mismatch` (4 penalties)

**Verdict:** This is both redundancy **and** inconsistency (see E1). Canonical home should be ch46 (the chapter titled "Correction-Channel Integrity"). **Trim/cross-ref:** ch46 L120–133 and ch48 L88–101 restate the full functional unnecessarily — replace with `\eqref{eq:cci-ch46}` + the one penalty term each chapter actually uses. ch46's statement is defensible as the *introduction* of the quantity but should then be reconciled with ch46 (right now ch46's is the richest — 5 terms — yet the "measurement" chapter ch46 drops a term). ch46 L135 already cross-refs ch46 ("develops a closely related functional with additional operational detail"), which is the correct move; just apply it to the equation itself instead of restating.

### D3. The "strong correction channel" / multi-level correction taxonomy
- ch46 L656–686: **four** levels via `eq:four-level-correction` C=(C^A, C^π, C^W, C^Φ) — action / policy / bundle-weights / bearer.
- ch46 L726–768: `\begin{definition}[Strong correction channel]` + five requirements (sensitivity, specificity, depth, timeliness, self-preservation).
- ch46 L348–369: "The Strong Correction Channel" again, now **six** levels `eq:strong-correction-levels-ch46` C=(act, policy, model, bundle, bearer, successor) with a subsection per level (L376–428).

**Verdict:** **trim/partial duplication.** Two different arities (four vs six) for the same taxonomy is confusing (see E). The six-level version (ch46) is the superset and the better home for the *definition* (it adds model and successor levels). Recommend: ch46 keeps a brief four-→deeper-levels motivation but cross-refs ch46 for the canonical taxonomy, or ch46 adopts the six-level version up front. The "Strong correction channel" *definition box* appears once (ch46 L731) and the *section heading* "The Strong Correction Channel" appears in both ch46 (L726) and ch46 (L348) — duplicate section title within one part.

### D4. The CEV comparison — stated **four** times in this part
- ch46 §"Relation to Coherent Extrapolated Volition" L810–852.
- ch46 §"The Strong Version: Extrapolative Correction" L397–452 (CEV contrast L448).
- ch46 §"Relation to Coherent Extrapolated Volition" L532–558.
- ch48 §"Relation to Coherent Extrapolated Volition" L523–561.

All four make the **same point**: preserve the update process `V_{t+1}=U_H(V_t,E_t,D_t)` rather than compute-and-optimize a guessed fixed point `V*`/`V̂_∞`. ch46 and ch48 even use identical section titles. The `eq:human-value-update` equation recurs: ch46 L827 (`-ch46`), ch46 L417 (`-ch46`), ch46 L162 (`-ch46`), ch48 L539.

**Verdict:** the *full* CEV-contrast belongs once. **Keep (pedagogical):** one canonical treatment — recommend ch46 (the "Beyond Following Instruction" chapter is where extrapolation is the explicit subject) as canonical, with ch46/ch46/ch48 reduced to a one-sentence reminder + `\ref`. Currently ch46, ch46, ch48 each re-derive the V*-vs-process distinction nearly verbatim — **trim/cross-ref (true duplication).** This is the single most repeated argument in the part.

### D5. Legitimacy criteria (truth-contact, agency, plurality, reversibility, non-manipulation)
- ch46 L484–502: `Q(U)=q_T+q_A+q_R+q_P+q_D+q_C` (six quality terms).
- ch46 §"What Makes an Update Legitimate?" L217–293: five subsections (truth-contact, agency preservation, plurality, reversibility/option, non-manipulation), each with an inequality.
- ch48 §"When Value Change Is Legitimate" L562–593: seven-item legitimacy list + seven-item corruption list.
- Also recurs outside the part: ch04 and ch46 (per task brief).

**Verdict:** **keep (pedagogical) but de-duplicate the operational core.** ch46's five-criterion subsection set and ch48's seven-item list overlap heavily (truth-contact, agency, plurality, reversibility, non-manipulation appear in both). They serve different framings (ch46 = legitimate *update*; ch48 = legitimate *value change*), so total merge is not warranted, but they should cross-reference and avoid re-stating the same inequalities. Recommend one canonical criteria home (ch46) and have ch48's list cite it where it overlaps, keeping only ch48's distinct items (bearer-expansion-under-scrutiny, non-exploitation, continuity-of-correction).

### D6. Repeated worked examples (recommender / companion / medical / governance planner)
- **Recommender system:** ch46 §L893–909 ("avoid label x" vs "stop exploiting my anger"); ch48 §L598–604 ("Recommender That Makes Itself Necessary"). Same mechanism (engagement optimization corrupts the corrector). **Partial duplication** — keep both but they could cross-ref; ch48's is richer.
- **AI companion / dependency:** ch46 §"AI Companion Value Drift" L1044–1082; ch48 §"Companionship" L473–475 + woven through domestication. **Keep** — ch46 is quantitative (W_care,autonomy shift), ch48 is taxonomic; complementary.
- **Medical AI:** ch46 §L881–891; ch46 case 3 L71–73; ch48 design constraint L785. Light, complementary, **keep**.
- **Governance/city planner:** ch46 §"The Helpful Planner" L990–1042; ch48 §"Governance System That Ends Conflict" L614–618. Same scenario (city AI degrades political correction). **Partial duplication** — cross-ref; ch46 quantitative, ch48 illustrative.

**Verdict:** examples are mostly **keep (pedagogical)** because they illustrate different formal points, but recommender and governance-planner appear in two chapters with the same moral and should cross-reference rather than re-establish the setup.

### D7. Failure-mode catalogues
ch46 §Failure Modes (L925, 7 items) and ch46 §Failure Modes (L1228, 10 items) overlap substantially: decorative/ceremonial correction, surface/local compliance, ontology drift/laundering, preference capture/judge shaping, authority decay, successor escape/amnesia, self-control-outpaces-transparency. **Trim:** ch46's list is the superset (adds surveillance alignment, extrapolation capture, institutional narrowing). Recommend ch46 keep a short pointer and let ch46 own the canonical catalogue, or differentiate explicitly (ch46 = channel-mechanism failures, ch46 = integrity-measurement failures).

### Merge-vs-divide assessment (ch46 / ch46)
ch46 (1244 L) and ch46 (1296 L) together duplicate: the chain, CCI, the bottleneck MI walk, the strong-channel idea, CEV, failure modes, and the audit/metric list. Two viable fixes:
1. **Sharper division (recommended):** ch46 = *conceptual* ("correction is a causal channel; here is the chain, the bottlenecks, why it is not obedience, relation to corrigibility") and **stop before** introducing the CCI penalty functional, the audit profile, and adversarial testing. ch46 = *operational* (CCI functional, penalties, coerced correction, metrics, stop/start/continue, safety case, successor/ontology/capability stress). This requires moving ch46 §"Measuring CCI" (L1010), §"Adversarial Testing" (L1073), and the CCI equation (L281) out of ch46 into ch46, and demoting ch46's CEV section to a pointer.
2. **Merge** into one long "Correction Channels and Their Integrity" chapter. Not recommended — the part already has a clean 4-beat arc and ch46's extrapolative/surveillance material is distinct enough to keep ch46 separate; a single merged ch46+25 would be ~2000 lines and unbalance the part.

Net: **divide more sharply**, do not merge. The current overlap is ~30–40% conceptual duplication between ch46 and ch46.

---

## E. Consistency

### E1. CCI penalty-term inconsistency (substantive)
The CCI functional is **not** consistent across chapters:
- ch46 (L281): **five** penalties incl. Goodhart `λ_G G`; ontology term `O_mis`. Capacity term `C_raw`.
- ch46 (L162): **four** penalties; ontology term renamed `Ω` (`λ_Ω Ω`); **drops Goodhart G**; capacity term `C_corr`.
- ch46 (L120): four penalties; ontology `O_mis`; capacity `C_raw`.
- ch48 (L88): four penalties; ontology `O_mismatch`; capacity `C_corr`.
- ch46 (L455): four penalties; ontology `O_mismatch`; capacity `min_i I`.

Problems: (a) ch46 introduces a fifth term (Goodhart) that the dedicated measurement chapter ch46 silently drops, even though ch46 has a whole §"Goodharting the Correction Channel" (L769) — so Goodhart pressure is discussed but no longer a penalty term. (b) the ontology penalty is written four different ways: `O_mis`, `Ω`, `O_mismatch`. (c) the capacity term alternates `C_raw` / `C_corr` / `min_i I`. **Recommend** one canonical functional (pick ch46's home, decide whether Goodhart is a penalty term or folded into M/manipulation, and fix one symbol for the ontology term and one for capacity) and `\eqref` everywhere else.

### E2. Correction-chain letter definitions — consistent
The seven variables `W,O,J,D,C,U,A` are defined identically in ch46 (L68–77), ch46 (L114–122), ch46 (L86–94), ch48 (L65–73) and ch46 (L429–438). Good — no semantic drift in the letters. (Only redundancy, per D1, not inconsistency.) Minor: ch46 calls `W_t` "world state at time t" and later reuses `W` inside `Z_t=(B_t,W_t,Φ_t)` at L167 to mean **tradeoff weights**, then again `W_{ij}` as tradeoff weights in ch46 L302 — `W` is overloaded (world state vs tradeoff weights). Worth a notation note; the appendix `appA-notation` should disambiguate.

### E3. Multi-level correction arity — inconsistent
Four levels in ch46 (action/policy/weights/bearer, L674) vs six levels in ch46 (act/policy/model/bundle/bearer/successor, L358). Reconcile to one taxonomy (six-level is the superset). See D3.

### E4. Section-title capitalization — consistent within part
All four chapters use title case for `\section{...}` (e.g., "Why Correction Is Not Obedience," "The Strong Correction Channel"). ch46 (next part) switches to sentence case ("The local alignment fallacy," "What counts as a successor?") — a cross-part inconsistency to note for whoever owns global style, but within Part VI capitalization is uniform.

### E5. Chapter-ending naming — inconsistent (flagged in brief, confirmed)
Four different endings: ch46 "Chapter Summary," ch46 "Chapter Conclusion," ch46 "Summary," ch48 "Summary." Recommend standardizing to one (the part already leans "Summary" 2/4; ch46/ch48 are the WWCTV-compliant chapters, so "Summary" is the de-facto house style). Standardizing would also help because ch46/ch46's non-"Summary" endings coincide with the missing-WWCTV problem.

### E6. Epigraph style — consistent
All four use `\epigraph{...}{}` with empty attribution. Fine.

---

## F. Open tangents / dangling promises

- **ch46 L544** forward-refs `ch:value-change-at-stake` (ch45) and `ch:unconscious-value-drift` (ch46) for privacy/legibility — valid, those chapters exist.
- **ch46 L275** "Bargaining, blackmail, and coercion are treated here as correction-channel pathology---not as a separate book part." This is an editorial promise/justification for *not* having a part; fine but slightly meta. No dangling ref.
- **ch46 L85** refs `ch:transport-types` (ch46) — valid, but note ch46 never acknowledges that ch46 already defined the same chain+CCI (the incoming duplication in C is silent).
- **ch46 L437** promises ch48 will develop manipulation/domestication/false consent "as correction-channel attacks" — fulfilled.
- **ch46/ch48** both ref `christiano2018corrigibility`, `russell2019human` for "the system may assist deliberation" — consistent.
- No unresolved `\ref` placeholders, no "(forthcoming)", no `\todo` notes detected. No orphan equations labeled-but-unreferenced that are problematic (most labeled equations are referenced or are intentional display recaps).
- Mild tangent: ch46 §"Correction as Civilizational Self-Modification" (L1150) and ch46 §"Civilizational Self-Governance" (L439) and ch48 §"The Philosophical Limit" (L835) all three reach the same "governed vs ungoverned value change" coda (ch46 L1162–63, ch46 L644–47, ch48 L856 use near-identical phrasing: "The choice is between governed transformation and ungoverned drift"). Three chapters end on the same civilizational note — rhetorically repetitive; consider letting ch48 (part finale) own it.

---

## G. Continuity hand-off (incoming / outgoing concepts)

**Incoming (from Part V / ch46):**
- correction chain `W→O→J→D→C→U→A` — already present in ch46 L427 (and ch46 L490). Part VI inherits, then re-derives (see D1).
- CCI functional — already present in ch46 L455. Part VI inherits, then re-derives (see D2).
- value bundles `B`, bearer maps `Φ`, tradeoff weights `W` — from ch16 `ch:value-bundle-model` / `ch:bearer-maps` / `ch:tradeoffs-bundle-geometry`; ch46 L164–174, ch46 L286–304, ch46 L299–312 use them, correctly cross-referenced.
- goal transport / goal laundering — ch46, ch48; ch46 L587 ("goal laundering at the level of values") and ch46 echo it.

**Outgoing (to Part VII / ch46+):**
- successor-closure / correction inheritance — ch46 §"Correction Under Successor Creation" (L630, `eq:recursive-successor-cci` L671) and ch46 §"Successor Correction" (L421) and ch48 §"Successor Non-Manipulation" (L821) all set up ch46's central thesis. ch46 L5 explicitly carries "correction integrity" forward as a successor-preserved invariant. Clean baton-pass.
- CCI as a safety-case object → ch46's 6-claim safety-case template (L1109) and `eq:cci-safety-case` (L1213) feed Part IX (safety cases) and `appK-safety-case-template` / `appJ-correction-channel-audit`.
- manipulation/legibility → ch45/ch46 (value change, drift), forward-referenced from ch46 L544.

**No missing bridges** into or out of the part; the only hand-off defect is that the **incoming** duplication from ch46 is unacknowledged (ch46 should open by referencing ch46's correction-transport section rather than redefining the chain and CCI from scratch).

---

## Priority fix list (for whoever edits)

1. **Add "What Would Change This View" to ch46 and ch46** (hard required-element gap). Use ch46 L604 / ch48 L858 as templates.
2. **Reconcile the CCI functional** (E1): one canonical equation, decide Goodhart-term in/out, fix `O_mis`/`Ω`/`O_mismatch` to one symbol and `C_raw`/`C_corr` to one. Canonical home = ch46.
3. **De-duplicate the CEV contrast** (D4): canonical in ch46, reduce ch46/ch46/ch48 to a sentence + `\ref`.
4. **Divide ch46/ch46 more sharply** (C, D-merge): move CCI measurement/audit/adversarial-testing out of ch46 into ch46; ch46 stays conceptual.
5. **Unify the strong-channel taxonomy** to six levels (D3, E3) and avoid the duplicate "The Strong Correction Channel" section title across ch46/ch46.
6. **Standardize chapter endings** to "Summary" (E5) and the recurring "governed vs ungoverned" coda to a single chapter (F).
7. Single canonical home for the correction-chain equation (D1) + legitimacy criteria (D5); cross-ref the rest.
