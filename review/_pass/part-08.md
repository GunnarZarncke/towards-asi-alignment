# Review Pass — Part VIII: Attractor Basins and Socio-Technical Selection (ch32–ch35)

Reviewer: AI pass. Date: 2026-06-22. Scope: `chapters/ch32-selection-environment.tex`,
`chapters/ch33-multi-agent-strategic-coupling.tex`, `chapters/ch34-parasites-correction-system.tex`,
`chapters/ch35-alignment-attractor.tex`. No manuscript files were edited.

Cross-referenced for consistency: ch10 (`ch10-strategic-opacity.tex`), ch13
(`ch13-coordination-bottleneck.tex`), ch31 (`ch31-certification-without-construction.tex`),
ch36 (`ch36-passive-observation-not-enough.tex`), ch40 (`ch40-lethality-stress-test-open-issues.tex`),
`metadata/book.yml`.

---

## HEADLINE FINDINGS

1. **ch33 is a genuine stub (book.yml `status: stub`).** Its *Formal Model* (lines 25–114) is
   real, dense, and largely complete — it does absorb the cooperation/privacy/opacity and
   percolation material. But **three whole Shape-A sections are placeholder `[STUB]` one-liners**:
   *Worked Example* (116–118), *Counterexample or Failure Mode* (120–122), and *What Would Change
   This View* (124–126), plus an inline `[STUB]` (line 45). Decision relevance is effectively
   absent (only a `% TODO` at line 114). See §B(ch33).

2. **Missing "What Would Change This View" in three of four chapters.** Only ch33 has the exact
   heading (and it is a stub). **ch32, ch34, ch35 all end at "Summary" with no WWCTV section.**

3. **Parasite-persistence criterion diverges from canon.** The brief's canonical form
   `C_X < H(A_Y) − λ_Y·H(I_Y)/β` is the one in **ch10** (lines 474–481). **ch34 uses a different
   formula**, `C_H < H(A_Y) + K_Y − L_Y` (lines 140, 148, 811). Same phenomenon, two
   non-matching formalizations across the book. See §E.

4. **Pivotal-process notation `B_race → B_certified-deployment` is NOT in ch35.** It actually
   appears only in **ch40 line 56** (`\mathcal{B}_{race} → \mathcal{B}_{certified deployment}`),
   and ch40's own comment (line 117) says "pivotal process — ch35." ch35 uses
   `\mathcal{B}_{align}` / `\mathcal{S}_{align}` instead. Dangling cross-reference. See §E.

5. **"Artifact conductivity" is defined two different ways in adjacent chapters.** ch34 line 400:
   `χ(A,H)=I(R;D_H|A)−I(R;D_H)`. ch35 line 138: `κ_ij(a)=b·p·ρ/c`. Same term, two formalisms.
   See §D.

---

## A. CAPSULES

**ch32 — Alignment Is Selected or Destroyed by Its Environment** (788 lines, `draft`).
The "selection turn": the unit of analysis shifts from model to model-in-environment. Builds a
socio-technical selection model (fitness `F` vs preservation `P`, danger when `∇F ∦ ∇P`),
distinguishes training from selection (lines 117–142), Goodhart-as-selector (144–182), endogenous
selection by capable systems (184–221), the deployment-fitness trap (223–246), the alignment
externality (286–307), artifacts as selection shapers (309–358), selection channels (360–419),
self-stabilizing patterns/attractors (421–462), false attractors (464–533), local-first path
(535–562), Stop/Start/Continue decision triggers (564–623), a worked example (625–642), and the
selection-alignment condition `E[∇F·∇P]>0` (706–731). Mature, complete, well-formed.

**ch33 — Multi-Agent Superintelligence and Strategic Coupling** (145 lines, `stub`).
Shape-A skeleton. The two former standalone chapters are inserted as subsections: *Cooperation,
Privacy, and Opacity* (line 27) and *Percolation and Inferential Coupling* (line 47). Formal core
is real: cooperativity `κ_ij` (50–56), effective cooperativity with ICI `~κ_ij` (58–72), the key
claim `p_ij=0 ⇏ ~κ_ij=0` (72), the ICI definition (77–84), five inferential-coupling sources
(86–91), coalition collapse (93), value-sensitive cooperation `ρ^V/κ^V/φ_V` (95–104), correction
percolation `φ_C` (106), and edge-level goal laundering `D_ij` (108–112). Everything after the
Formal Model is placeholder. See §B.

**ch34 — Parasites in the Correction System** (832 lines, `draft`).
Defines a correction parasite operationally (three conditions, lines 44–57), revisits
correction-channel capacity / CCI (62–129), states the parasite-persistence criterion (131–156),
gives three worked examples (benchmark parasites, compliance rituals, safety theater by
delegation, 158–225), value-update capture (227–260), privacy/opacity/legitimacy with κ and a
legitimacy sign Λ (262–348), multi-level/scale-mismatch parasites (350–379), host capacity &
artifact conductivity χ (381–414), Goodhart parasites (416–448), adversarial uplift (450–476),
the legibility trap (478–505), six detection tests (507–578), red flags (580–598), anti-patterns
(600–628), seven parasite-resistant design principles (630–698), local-first interventions
(700–719), a minimal safety-case fragment (721–770). Rich and complete.

**ch35 — The Alignment Attractor** (1044 lines, `draft`).
The part's synthesis. "Structural non-conductance" (14–55), minimal model `Z_t` and basin
`B_align` (57–114), artifact conductivity `κ_ij(a)` (116–165), percolation of alignment practice
(167–190, inherits ch13's threshold), the attractor as a six-loop feedback system (192–261), what
it attracts (263–276), false attractors (278–351), six high-conductivity properties (352–407),
"Monday-morning" five-step local-first method (409–507), six attractor metrics (509–589), design
principles (591–633), safety-case view (669–705), two worked examples (707–795), centralization
critique (796–815), role chapters for funders/labs/regulators/public (817–915), open failure
modes (917–963), what success looks like (964–994), connection to later chapters (996–1011).
Comprehensive; reads as the Part VIII capstone.

---

## B. REQUIRED-ELEMENT COMPLIANCE

| Element | ch32 | ch33 | ch34 | ch35 |
|---|---|---|---|---|
| `\chapter` + `\label` | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) |
| `chapterthesis` env | ✓ (4–6) | ✓ (4–6) | ✓ (4–6) | ✓ (4–6) |
| `epigraph` | ✓ (10–12) | ✗ (none) | ✓ (10–12) | ✓ (10–12) |
| Decision relevance | ✓ Stop/Start/Continue (564–623) | ✗ only `% TODO` (114) | ✓ tests/design/local-first (507–719) | ✓ Monday-morning/metrics (409–589) |
| Failure-mode / counterexample | ✓ False Attractors (464–533) | `[STUB]` (120–122) | ✓ examples + anti-patterns | ✓ False attractors (278) + open failure modes (917) |
| **Exact "What Would Change This View"** | **✗ MISSING** | ✓ present **but `[STUB]`** (124–126) | **✗ MISSING** | **✗ MISSING** |
| Summary | ✓ (759) | ✓ (128) | ✓ (806) | ✓ (1013) |
| `refsection` + `\printbibliography` | ✓ (8 / 785) | ✓ (8 / 142) | ✓ (8 / 829) | ✓ (8 / 1042) |

**WWCTV (critical).** Three of four chapters lack the exact section. ch32 substitutes Decision
Triggers; ch34 substitutes detection tests / red flags / anti-patterns; ch35 substitutes "Open
failure modes" (917) + "What success looks like" (964). These are good content but not the
required canonical heading. **Flag: add an exact `\section{What Would Change This View}` to ch32,
ch34, ch35**, and **fill** ch33's (line 126).

**ch33 stub enumeration (line-by-line):**

- Real prose, thin but present: *Why This Matters* (10–16), *Plain-Language Model* (18–23).
- *Formal Model* (25–114): **substantive and essentially complete.** Markers:
  `[Defined]` at 30, 37, 50, 77, 95, 106; `[Conjectural]` at 34, 43, 58, 86, 93, 108.
  - Inline **`[STUB]`** at **line 45**: "Privacy islands and cooperative attractors under
    socio-technical selection pressure (percolation form in Ch. coordination-bottleneck)" —
    promised but not written.
  - `% TODO[empirical-test]` at **line 114** (estimate `D_ij`; coalition-collapse tests).
- *Worked Example* (116): body is a single **`[STUB]`** (118).
- *Counterexample or Failure Mode* (120): body is a single **`[STUB]`** (122).
- *What Would Change This View* (124): body is a single **`[STUB]`** (126).
- *Summary* (128–136): real `[Defined]/[Claim]/[Open]` bullets.

**Subsection-title requirement.** Brief requires subsections "Cooperation, Privacy, and Opacity"
and "Percolation of Cooperation."
- `\subsection{Cooperation, Privacy, and Opacity}` — present, exact match (line 27). ✓
- `\subsection{Percolation and Inferential Coupling}` (line 47) — **title mismatch** vs required
  "Percolation of Cooperation." Content covers percolation + the inferential-coupling extension;
  recommend either rename to include "Cooperation" or note the deliberate retitling.

---

## C. CONTINUITY

**Incoming from Part VII (ch31 → ch32).** Clean. ch31 closes "The next chapter examines how
alignment is selected or destroyed by its environment (ch32)" (ch31 line 709). ch32 opens by
explicitly resuming Chapters successor-test→certification (ch32 line 17). Good handoff.

**ch32 → ch33.** ch32 closes pointing to ch33 (line 779). But ch33 is a stub, so the promised
"multi-agent superintelligence and strategic coupling" lands on a skeleton: the reader gets the
formal apparatus but no worked example, no failure mode, no decision hooks.

**ch33 → ch34 (the broken link).** ch33 has **no outgoing "next chapter" sentence** — it ends on
Summary bullets + references (128–144). ch34 in turn opens from the correction-channel chapters
(ch34 lines 17, referencing ch24/ch25), **not** from ch33. So ch33 sits as a partial orphan
between two strong chapters: its incoming transition (selection → multipolarity) is implicit and
its outgoing transition (→ parasites) is absent. ch33 *does* forward-reference ch34 for
opacity-legitimacy (line 43), and ch34 *does* treat privacy/opacity/κ (262–348), so the concepts
connect even though the narrative seam does not. **Yes — the ch33 stub weakens the ch32→ch34
flow**: a reader moving ch32→ch33→ch34 experiences a dense-but-skeletal interlude with no bridge
sentences on either side.

**ch34 → ch35.** Clean. ch34 closes "The next chapter examines the alignment attractor (ch35)"
(line 823).

**ch35 → Part IX (ch36).** Strong. ch35 §"Connection to later chapters" (996–1011) explicitly
routes to ch36 passive-observation (1001), ch37 goal-laundering (1003), ch38 multiscale (1005),
ch39 safety-case (1009). ch36 opens cleanly on adversarial measurement. Good handoff.

**Does ch35 serve as the part's culmination?** Yes. Part VIII is titled "Attractor Basins and
Socio-Technical Selection"; the attractor motif is seeded in ch32 (§Self-Stabilizing Patterns,
421–462; False Attractors, 464–533) and culminates in ch35 "The Alignment Attractor," which
synthesizes selection (ch32), coupling/percolation (ch33), and correction/parasites (ch34) into a
single feedback ecosystem and then hands off to Part IX. The capstone role is well executed.

---

## D. REDUNDANCY

**1. False-attractor taxonomy — ch32 (464–533) vs ch35 (278–351).** Partial duplication.
- ch32 list: Compliance (469), Benchmark (481), Reputational Silence (493), Dependency (507),
  Strategic Secrecy (521).
- ch35 list: Reputation (283), Compliance (300), Benchmark (317), Centralization (330),
  Transparency-absolutism (339).
- Overlap of three (Compliance / Benchmark / Reputation) but **different referents**: ch32's are
  false attractors of the *deployed-system population / selection environment*; ch35's are false
  attractors of the *alignment field/ecosystem*. Defensible distinction.
- ch35 already cross-refs ch32 (line 281); **ch32 does not cross-ref ch35.**
- **Verdict: KEEP both, TRIM the overlap.** Add a ch32→ch35 forward pointer; in ch35 compress the
  shared three (compliance/benchmark/reputation) to lean on ch32 and foreground the
  field-specific two (centralization, transparency-absolutism).

**2. Percolation — ch13 vs ch33 vs ch35.** Healthy division of labor; **KEEP all.**
- ch13 is canonical: derivation + `eq:cooperation-percolation` (line 412).
- ch33 applies the threshold to the `~κ_ij` (inferential-coupling) graph and explicitly imports
  ch13 rather than re-deriving (ch33 lines 45, 74).
- ch35 specializes `κ` to artifact conductivity and explicitly inherits ch13's result (ch35 lines
  180, 1028, citing `eq:cooperation-percolation`). No redundant derivation. Good.

**3. κ cooperativity — ch10 vs ch13 vs ch33.** Same formula `b·p·ρ/c` in ch10 (line 95), ch13
(canonical, `eq:kappa-coordination`, line 375), ch33 (line 54). Each re-states the b/p/ρ/c gloss
for self-containment. **Verdict: KEEP** (chapters are designed self-contained), but ch33 cites
Hamilton for κ without pointing to ch13's canonical definition — **add a cross-ref** ch33→ch13 at
the κ definition (line 50) for consistency, as it already does for percolation.

**4. Artifact conductivity — ch34 (381–414) vs ch35 (116–165).** **Inconsistent, not merely
redundant.** Two *different* formal definitions share one name:
- ch34 line 400: `χ(A,H)=I(R;D_H|A)−I(R;D_H)` (mutual-information lift of risk→decision).
- ch35 line 138: `κ_ij(a)=b·p·ρ/c` (cost-benefit edge-transmission ratio).
- **Verdict: RECONCILE / cross-ref.** They are complementary (χ = decision-relevance gain; κ(a) =
  edge transmissibility), but the manuscript never says so. Add a sentence in ch35 (near 116)
  noting ch34's χ and that the two measure different facets, or unify the term.

**5. Local-first path — ch31 / ch32 / ch34 (and ch35).** Repeated motivational preamble.
- ch32 §The Local-First Path (535–562) opens "socio-technical selection is too large… not
  decisive" (538–540).
- ch34 §Local-First Interventions (700–719) opens "Global coordination is hard" (703).
- ch35 §Monday-morning version (409–507) and Summary (1034) restate local-first as method.
- The *content lists differ* (selection-gradient levers vs parasite-resistance levers vs
  artifact steps), so the substance is not duplicated. **Verdict: KEEP the distinct lists, TRIM
  the repeated "global coordination is hard, act where you have leverage" framing** to one
  canonical statement (ch32) and cross-ref from ch34/ch35.

---

## E. CONSISTENCY

**κ_ij = b·p·ρ/c.** Consistent everywhere it appears: ch13 line 372 (canonical), ch10 line 95,
ch33 line 54, ch34 line 273, ch35 line 143. ✓ ch33's effective form `~κ_ij` (58–72) and the key
claim `p_ij=0 ⇏ ~κ_ij=0` (line 72) are present and correct. ✓

**Parasite-persistence criterion.** **DIVERGENCE.** Brief's canonical form
`C_X < H(A_Y) − λ_Y·H(I_Y)/β` matches **ch10** (lines 474–481: action entropy `H(A_Y)`, internal
entropy `H(I_Y)`, extraction parameter `β`, threshold `H(A_Y) − λ_Y H(I_Y)/β`). **ch34 instead
uses** `C_H < H(A_Y) + K_Y − L_Y` (lines 140, 148, 811) with camouflage complexity `K_Y` and
maintenance cost `L_Y`. The two formalizations are independently reasonable but **do not match**,
and ch34 never reconciles its `K_Y/L_Y` form with ch10's `λ_Y H(I_Y)/β` form. **Flag for author
decision**: pick one canonical form or add a bridging note. (Also a symbol issue: ch10 uses
`C_X`/host vs ch34 uses `C_H` for the host capacity.)

**Pivotal-process `B_race → B_certified-deployment`.** **MISSING from ch35.** Not present in
ch35 (which uses `B_align`/`S_align`/`C_certified`). The notation lives only in **ch40 line 56**
(`\mathcal{B}_{race} → \mathcal{B}_{certified deployment}`), and ch40's inline comment (line 117)
asserts "pivotal process — ch35," and ch40 lines 134/145 lean on it. **Dangling promise:** ch40
attributes the pivotal-process formalization to ch35, but ch35 does not contain it. Either add the
`B_race → B_certified-deployment` framing to ch35 (it fits the §"What success looks like" / §basin
material), or correct ch40's pointer.

**Section-title capitalization.** **Inconsistent across the part.** ch32, ch33, ch34 use **Title
Case** ("The Selection Turn", "Operational Definition", "Why This Matters"). **ch35 uses sentence
case** ("The problem of structural non-conductance", "A minimal model", "Artifact conductivity",
"Percolation of alignment practice", "The attractor as a feedback system"…). Normalize ch35 to
Title Case to match the rest of Part VIII (and the book convention seen in ch31/ch36 headings).

**Chapter-ending naming.** Consistent *within* Part VIII: all four end in a section literally
titled "Summary" (ch32 759, ch33 128, ch34 806, ch35 1013). Note ch31 (Part VII) ends with
"Chapter summary" + "Key definitions" + "Exercises" — different convention, but that is outside
this part.

**Percolation equation reference.** ch35 cites `eq:cooperation-percolation` (lines 180, 1028) and
ch33 refers to the "percolation form in Chapter coordination-bottleneck" (line 45) — both point
correctly to ch13's `eq:cooperation-percolation` (ch13 line 412). ✓

---

## F. OPEN TANGENTS / DANGLING PROMISES

- **ch33 line 45 `[STUB]`** — "Privacy islands and cooperative attractors under socio-technical
  selection pressure (percolation form in ch13)": promised, unwritten.
- **ch33 lines 118, 122, 126** — Worked Example, Counterexample, WWCTV are all bare `[STUB]`
  forward-stubs (bargaining among frontier labs; multipolar-by-count but percolates;
  inferential-coupling-stays-negligible evidence). These are the chapter's chief dangling
  promises.
- **ch33 line 114 `% TODO[empirical-test]`** — estimate `D_ij` on real deployment edges; tests for
  effective-coalition collapse. Open research hook, acceptable as a comment but unresolved.
- **ch40 → ch35 mis-pointer** — ch40 line 117 says "pivotal process — ch35," but ch35 lacks the
  `B_race → B_certified-deployment` construction (see §E).
- **ch35 §"Connection to later chapters" (996–1011)** — promises adversarial measurement, goal
  laundering, multiscale, tripwires, safety cases. These resolve in ch36–ch39 (verified targets
  exist), so these are fulfilled forward refs, not dangling.
- **ch34 line 348** forward-refs ch25 for the "AI legible to correction, correctors private from
  manipulation" remedy — fulfilled (ch25 exists). OK.

---

## G. CONTINUITY HAND-OFF (incoming / outgoing concepts)

**ch32.** In: agents/successors/value-bundle transport/correction channels (from ch28–ch31).
Out: selection model, fitness `F` vs preservation `P`, attractors & false attractors, artifact
conductivity (seed), local-first, selection channels → consumed by ch33 (coupling), ch34
(parasites attack the selection/correction surface), ch35 (the attractor synthesis).

**ch33.** In (implicit): selection environment + multipolarity from ch32; κ from ch10/ch13;
percolation from ch13; value-bundle/bearer-map from ch16/ch18. Out: `~κ_ij`, ICI, value-sensitive
cooperation `φ_V`, correction percolation `φ_C`, edge-level laundering `D_ij` → feed ch34
(opacity-legitimacy, line 43 ref) and ch37 (goal laundering, line 112 ref) and ch35
(percolation/attractor). **Weak narrative seams on both sides (see §C).**

**ch34.** In: correction-as-causal-channel + CCI (ch24/ch25); value-bundle `B` & bearer map `Φ`
(ch16/ch18); selection (ch32). Out: parasite-persistence criterion, χ artifact conductivity,
detection tests, parasite-resistant design → ch35 (artifact conductivity, false attractors) and
Part IX (safety case ch39).

**ch35.** In: selection (ch32), coupling/percolation (ch33/ch13), parasites/conductivity (ch34),
certification (ch31). Out: artifact conductivity `κ_ij(a)`, percolation of practice, the
feedback-loop ecosystem, attractor metrics → explicitly into ch36–ch39 (Part IX). Capstone, clean
exit.

---

## PRIORITIZED ACTIONS

1. **Build out ch33** (status `stub`): fill Worked Example (118), Counterexample (122), WWCTV
   (126), resolve the `[STUB]` at line 45; add decision-relevance content; add incoming/outgoing
   bridge sentences (ch32→ch33→ch34); add a "next chapter" line. Consider an epigraph for parity.
2. **Add exact `\section{What Would Change This View}`** to ch32, ch34, ch35 (repurpose existing
   triggers / open-failure-modes content).
3. **Reconcile the parasite-persistence criterion** (ch34 `+K_Y−L_Y` vs ch10/brief
   `−λ_Y H(I_Y)/β`); unify symbol `C_H`/`C_X`.
4. **Fix the pivotal-process mismatch**: add `B_race → B_certified-deployment` to ch35 or correct
   ch40's pointer (ch40 line 117).
5. **Reconcile "artifact conductivity"** (ch34 χ vs ch35 κ(a)) with a clarifying cross-ref.
6. **Normalize ch35 section titles to Title Case.**
7. **Trim/cross-ref redundancy**: false-attractor overlap (ch32↔ch35), local-first preamble
   (ch32/ch34/ch35), κ definition cross-ref (ch33→ch13); retitle ch33's percolation subsection or
   note the change.
