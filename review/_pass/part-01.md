# Part I review — "The Alignment Problem Reframed" (ch01–ch05)

Reviewer pass: read-only structural/continuity review. No manuscript files edited.
Scope: `chapters/ch01-wrong-object.tex`, `ch02-artificial-civilization.tex`, `ch03-dynamical-guarantee.tex`, `ch04-fixed-values-wrong-target.tex`, `ch05-assumptions-scope-failure-coverage.tex`.
Part file: `parts/part01-reframing.tex` (confirms order ch01→ch05).

Spine context used: alignment = preserving human-correctable value-bearing processes across capability growth, ontology shift, successor creation, strategic multi-agent selection, assuming civilization retains correction capacity.

---

## Part-level summary table (required-element compliance)

| Element | ch01 | ch02 | ch03 | ch04 | ch05 |
|---|---|---|---|---|---|
| `\chapter` + `\label{ch:...}` | yes | yes | yes | yes | yes |
| `chapterthesis` env | yes | yes | yes | yes | yes |
| decision-relevance early | partial (late, L527) | partial (L368) | partial (late, L708) | partial (late, L668) | yes (L10 "Why This Matters", thin) |
| failure-mode/counterexample | yes | yes | yes | yes | **missing** (only audit table) |
| section EXACTLY "What Would Change This View" | **MISSING** | yes (L384) | yes (L728, label mismatch) | yes (L725) | **MISSING** |
| summary | yes ("Summary" L652) | yes ("Chapter summary" L397) | yes ("Summary" L754) | yes ("Chapter summary" L739) | yes ("Summary" L106) |
| `refsection` + `\printbibliography[heading=subbibliography...]` | yes (L8/L669) | yes (L8/L405) | yes (L9/L784) | yes (L9/L764) | yes (L8/L118) |

**Most important compliance gaps:** ch01 and ch05 are both missing the required, exactly-titled "What Would Change This View" section. ch05 also lacks a real failure-mode/counterexample and carries placeholder scaffolding (`[Defined]` markers, an unresolved Turchin `% TODO[citation]`).

---

## A. Capsules

- **ch01 — The Wrong Object of Alignment** (`ch:wrong-object`). Before asking if a system is aligned, locate the bounded process whose dynamics drive the risk; aligning the model while missing the composite optimizer is a "boundary error." Establishes operational boundary discovery (MI screening, memory, intentional compression), perturbation testing, and the alignment-target-as-moving-equivalence-class idea.
- **ch02 — From Artificial Intelligence to Artificial Civilization** (`ch:artificial-civilization`). The real alignment object is often a human–machine–institutional control loop whose selection pressure can outrun human correction. Establishes the civilizational loop model `X_t=(H,M,I,K,R,E)`, delegation transition, tool-picture failure conditions, correction chain + CCI, and "failures without villains."
- **ch03 — Alignment as a Dynamical Guarantee** (`ch:dynamical-guarantee`). Alignment is not a momentary property but a dynamical guarantee that alignment-relevant structure stays in a safe basin inside a certified class of systems/transformations. Establishes safe/bad set/basin geometry, the seven invariants, certification-not-construction, safety-case shape, non-stationarity, and four failure classes.
- **ch04 — Why Fixed Values Are the Wrong Target** (`ch:fixed-values-wrong-target`). Human values are compressed, socially mediated, changing control structures; the target is a human-correctable value *process*, not a static utility. Establishes the three senses of "value," value-bundles `B_t`, tradeoff geometry, bearer maps `Φ`, value-change vs corruption, and value-process preservation `V_t=(B,W,Φ,U^H,C^H)`.
- **ch05 — Assumptions, Scope, and Failure Coverage** (`ch:assumptions-scope-failure-coverage`). The framework holds only if civilization still has correction capacity; broader pre-ASI risks are assumption-threats, not the object. Establishes in/out-of-scope lists, the correction-capacity assumption `C_corr^society(t0)>θ`, and a Turchin coverage audit.

---

## B. Required-element compliance (detail)

**ch01**
- **MISSING "What Would Change This View."** The closest section is `\section{Limits and What This Chapter Establishes}` (L588) with failure-mode subsections (L590–L617). This is not a renamed WWCTV; it is a different (limits/establishes) section, so the required falsification section is simply absent. This is the most serious ch01 gap.
- Structural nit: `\subsection{Failure Modes of Boundary Framing}` (L590) has no body before the next `\subsection{Overfitting Boundaries}` (L594); the failure modes should likely be subsubsections under it.
- Empty epigraph attribution `{}` (L10–L12). Cosmetic.

**ch02**
- Compliant. WWCTV present and exactly titled (L384, label `sec:wwctv-artificial-civilization`). Uses `\begin{quote}` (L10) instead of `\epigraph` used elsewhere — style inconsistency, not a missing element.

**ch03**
- WWCTV present and exactly titled (L728), **but the `\label` is `sec:shaky-points-dynamical-guarantee`** (L729) — a residue of the disallowed "Where the Argument Is Shaky" naming. Title is correct; the stale label should be flagged/renamed for consistency.

**ch04**
- Compliant. WWCTV exactly titled (L725, label `sec:wwctv-fixed-values`).

**ch05**
- **MISSING "What Would Change This View"** entirely (chapter ends Turchin audit → Summary).
- **No failure-mode/counterexample** beyond the audit table.
- **Placeholder/scaffolding markers:** `\textbf{[Defined]}` at L56, L109, L110, L111 — editorial annotations left inline in manuscript prose.
- **Unresolved TODO + dangling citation:** `% TODO[citation]: Cite Turchin AGI failure-mode map` (L104). The entire section is "Turchin Coverage Audit" (L66) and the thesis names Turchin, yet Chapter References (L116) cite only `iaisr2025` and `casper2023rlhflimits` — **no Turchin citation anywhere**. The promised attribution is undelivered.
- Chapter-5-specific requirements ARE met: scope (L16–L52), correction-capacity assumption `C_corr^society(t0)>θ` (L56–L61), Turchin coverage audit "audit only" framing (L66–L69). Content is thin/list-driven (121 lines total) — borderline stub for a manuscript chapter.

---

## C. Continuity (ch01→ch02→ch03→ch04→ch05)

- Overall the arc is coherent: **wrong object/boundary (ch01) → that object is a civilizational loop (ch02) → safety about such a loop must be a dynamical guarantee (ch03) → the thing the guarantee must preserve is a value *process*, not fixed values (ch04) → scope/assumptions bounding all of it (ch05).** Transitions are mostly explicit (ch01 L649–L650 "The next chapters build…"; ch02 L382 "The next chapters will build the machinery…"; ch03 L776–L778 "This reframes the rest of the book").
- **ch03 placement vs the stated 16-item spine.** The spine's conceptual progression does not contain a standalone "dynamical guarantee" node; ch03 is a meta-framing chapter inserted between the object chapters (ch01/ch02) and the values chapter (ch04). It reads well, but note that ch03 front-loads the *entire* book machinery (all seven invariants, value bundles, bearer maps, CCI, successor certification) before their dedicated chapters/parts — see Redundancy (D). This makes ch03 a heavy preview rather than a new step in the spine.
- **ch01→ch02 jump:** smooth (boundary error → composite loop). ch02 re-derives the "agent without personhood" argument ch01 already made (see D7); a back-reference would tighten the transition.
- **ch02→ch03:** smooth (need to certify the loop over time).
- **ch03→ch04:** smooth; ch03 §"Value-Bundle Geometry" (L201) and §"Bearer Maps" (L233) explicitly tee up ch04. But ch04 then re-introduces the same constructs from scratch with little back-reference (abrupt-ish re-setup rather than "as previewed in ch03").
- **ch04→ch05:** acceptable but the tone shifts sharply from full manuscript prose to a scaffold/list chapter; no explicit bridging sentence from ch04's close (L758) into ch05's "Why This Matters."

---

## D. Redundancy (cite + classify)

1. **Boundary screening `MI(I_{t+1};E_{t+1}|S_t,A_t)≤ε`** — ch01 L124–126, restated ch01 L407–409 (audit form), and ch03 L166–168. *ch01 internal pair: pedagogical restatement (keep).* *ch03 vs ch01: true duplication of the formula — ch03 should cross-ref ch01 rather than redefine.*
2. **Correction chain `W→O→J→D→C→U→A`** — ch02 L220–223 vs ch03 L271–274. *True duplication; ch03 (the formal invariants chapter) should cross-ref ch02's introduction.*
3. **CCI formula `min_i I(X_i;X_{i+1}) − λ_L L − λ_M M − λ_R R − λ_O O`** — ch02 L234–237 vs ch03 L278–285. *True duplication (ch03 adds `O_mismatch` detail); trim one, cross-ref.*
4. **Value-bundle response geometry `G_B=(∂π/∂B_i, ∂²π/∂B_i∂B_j)`** — ch03 L217–223 vs ch04 L222–229. *Borderline: ch03 is preview, ch04 is the dedicated treatment. Pedagogical (keep) but ch04 should say "as previewed in ch03."*
5. **Bearer map `Φ_i: z_world ↦ relevance`** — ch03 L239–242 vs ch04 L185–190. *Same as #4: keep ch04 as canonical, cross-ref from/within ch03.*
6. **Value-update operator `V_{t+1}=U_H(V_t,E_t,D_t)`** — ch02 L250–253, ch04 L172–173, L440–441, L566–570. *Within ch04: pedagogical restatement (keep). ch02 introduction → fine. No trim needed, but a single canonical statement + reuse would help.*
7. **"Agency/optimization without personhood/consciousness" argument (bureaucracy, market, thermostat)** — ch01 L289–326 (bureaucracy) + ontology-audit table L570–583, vs ch02 L293–314 (§"Civilizational agency without personhood," thermostat/market/bureaucracy). *Substantial thematic duplication — ch02 re-argues ch01's point with the same examples. Recommend ch02 cross-ref ch01 and shorten.*
8. **Seven invariants (ch03 L155–336) overlap the rest of the book** — by design (preview), but they overlap Part IV (value bundles), Part VI (correction channels), Part VII (successors). *Pedagogical preview (keep), but flag as the largest single source of downstream duplication.*

---

## E. Consistency (terminology / notation / titles)

**Section-title capitalization is split across the part:**
- Title Case: ch01, ch03, ch05.
- Sentence case: ch02 (e.g. "The change in scale" L14, "Three objects people confuse" L36), ch04 (e.g. "The static target trap" L16).
- Within ch01 there is internal inconsistency: Title-Case sections but sentence-case subsections "What to log / What to evaluate / Where to intervene / Who must be included / What counts as failure" (L533, L539, L549, L555, L561).
- Recommend one convention part-wide.

**Chapter-ending naming is split:** "Summary" (ch01 L652, ch03 L754, ch05 L106) vs "Chapter summary" (ch02 L397, ch04 L739). Pick one.

**Epigraph style split:** `\epigraph` (ch01 L10, ch03 L11, ch04 L11) vs `\begin{quote}` (ch02 L10) vs none (ch05). ch01/ch03 leave the attribution arg empty `{}`.

**Mutual-information macro inconsistency:** ch01/ch03/ch04 use `\MI` (= `\mathrm{I}`, defined `metadata/preamble.tex` L54). **ch02 uses raw `I(...)`** for mutual information (L144, L147, L230). Standardize ch02 to `\MI`.

**Symbol clashes across chapters (genuine — recommend a part/appendix notation reconciliation):**
- `I_t`: internal variables (ch01 L122; ch03 L164) vs **institutional structure** (ch02 L63; ch03 L591 `X_t=(A,H,E,I)`). Direct clash, including within ch03.
- `E_t`: external variables/environment (ch01 L122, ch02 L66, ch03 L591) vs **evidence** (ch04 L173, L355, L569).
- `D_t`: **delegation fraction** (ch02 L99–110) vs **deliberation** (ch02 correction chain L223; ch02 value-update L253; ch04 L173). Clash *within* ch02.
- `C_t`: correction signal (ch02 L223; ch03 L273) vs **boundary/control-locus structure** (ch03 `Z_t=(C_t,…)` L596–601). Clash within ch03.
- `B` / `B_t`: value-bundle vector (ch03 L209, ch04 L108). Spine calls capability "B"; ch03 sensibly uses `C_A` for capability (L187), so capability-vs-bundle does not clash in-text — but the appendix/notation should record that the spine's "B (capability)" is rendered `C_A` here.

**Order-of-introduction:** ch03 deploys value bundles, bearer maps `Φ`, tradeoff geometry, CCI, and successor certification (L201–L336) *before* their dedicated chapters (ch04 and Parts VI–VII). Each is defined inline so nothing is strictly used-before-defined, but readers meet the dedicated-chapter constructs first in the preview chapter; ch04 then re-introduces them with minimal back-reference.

---

## F. Open tangents / dangling promises / forward references

- **Forward `\ref`s all resolve:** ch01 L130 → `ch:finding-boundary` (ch07 ✓); ch05 L87 → `ch:correction-channel-integrity` (ch25 ✓), L90 → `ch:tradeoffs-bundle-geometry` (ch19 ✓), L93 → `ch:bearers-of-value` (ch43 ✓). Good.
- **ch05 Turchin citation is a real dangling promise:** section + thesis name Turchin; `% TODO[citation]` at L104; no Turchin entry in Chapter References (L116). Either cite or soften the attribution.
- Generic "developed later / will build" gestures (ch02 L345, L382; ch03 L776; ch04 L723 "civilizational self-governance under cognitive amplification" → Part X) are appropriately vague and supported by the part map; not problematic, but ch04 L723 is an un-anchored forward gesture (no `\ref`).
- ch03 L773 references RLHF/IRL/corrigibility/deception limits as motivation; these are citations, not promises — fine.

---

## G. Continuity hand-off

**(a) Concepts this part ASSUMES already known (incoming):**
- Alignment/ML vocabulary used without definition: mesa-optimizer (ch01 L21), corrigibility (ch01 L19), RLHF/IRL/CEV/Goodhart/instrumental convergence (ch03 L773, L782; ch04 L300–312, L418). Appropriate for the researcher tier; generalist readers will lean on `appendices/appF-glossary`.
- Information theory (mutual information, conditional MI) — assumed throughout.
- Dynamical-systems notions: transition kernels, basins, attractors, hitting times (ch03 L125–138), Markov blankets/active inference (ch03 L782).
- Replicator dynamics (ch02 L201–204).

**(b) Concepts this part INTRODUCES for later parts (outgoing):**
- Operational agent boundary + MI screening, "boundary card," perturbation audit → Part II (ch07 `ch:finding-boundary`).
- Composite optimizer / artificial-civilizational control loop; delegation transition; tool-failure conditions → book-wide framing.
- Dynamical guarantee; safe set/bad set/basin; certified class `C_certified`; safety-case shape; non-stationarity; four failure classes (drift/phase-transition/camouflage/successor-escape) → Parts IX (safety cases) and VIII (attractors).
- Capability envelope `C_A=I_pred+I_ctrl−βH(I)−γS` (spine's "B") → Part III.
- Value bundles `B_t`, tradeoff geometry `W_t`, bearer maps `Φ`, value-process tuple `V_t=(B,W,Φ,U^H,C^H)` → Part IV (ch16, ch19, ch43).
- Correction chain `W→O→J→D→C→U→A`, CCI, transparency-matched-to-power → Part VI (ch25).
- Successor stability/certification → Part VII.
- Scope boundary + correction-capacity assumption `C_corr^society(t0)>θ` → governs the whole book (ch05).

---

## Highest-priority fixes (ranked)

1. **ch01: add the required, exactly-titled "What Would Change This View" section** (currently absent; "Limits and What This Chapter Establishes" L588 is not a substitute).
2. **ch05: add "What Would Change This View"**, add at least one concrete failure-mode/counterexample, resolve the Turchin `% TODO[citation]` (L104) and add the Turchin reference, and remove/replace the inline `[Defined]` scaffolding markers (L56, L109–111).
3. **ch03: rename stale label** `sec:shaky-points-dynamical-guarantee` (L729) to match the corrected section title.
4. **Notation reconciliation** for `I_t`, `E_t`, `D_t`, `C_t` clashes and standardize ch02 to the `\MI` macro (L144, L147, L230).
5. **Trim/cross-reference duplicated formal objects** (correction chain, CCI, boundary screening, `G_B`, `Φ`) between ch02/ch03 and ch03/ch04 so ch03 reads as preview-with-pointers, not re-derivation.
6. **Standardize** section-title capitalization and "Summary" vs "Chapter summary" across the part; align epigraph style.
