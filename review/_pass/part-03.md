# Part III Review — "Capability Growth and Competence" (Chapters 11–14)

Reviewer pass. Read in full and in order: `chapters/ch11-capability-without-task-ontology.tex`,
`chapters/ch12-boundary-expansion.tex`, `chapters/ch13-coordination-bottleneck.tex`,
`chapters/ch14-intelligence-deepens-misalignment.tex`. Part file: `parts/part03-capability-growth.tex`.

Line numbers refer to the current files. No manuscript files were edited.

---

## A. Capsules (thesis + what each establishes)

**ch11 — Measuring Capability Without Task Ontology** (`ch:capability-without-task-ontology`).
Thesis (lines 4–7): capability should be measured as predictive + control information across a
boundary, not as task-battery performance. Establishes the core competence functional
`B_X = I_pred + α I_ctrl − β H(I) − γ S` (eq:biq, lines 212–223; boxed eq:biq-boxed 233–245),
the windowed/horizon profile `B_X^(h)` (eq:windowed-biq 327–338), physical envelopes (276–307),
capability regimes/thresholds (598–662), the cap-to-correction ratio `R_cap/corr` (eq:cap-corr-ratio
671–676), and a decision table (1004–1028). This is the canonical definition chapter for the
"bitwise IQ"/blanket-information competence functional.

**ch12 — Capability Growth Is Boundary Expansion** (`ch:capability-growth-boundary-expansion`).
Thesis (4–8): capability growth = boundary expansion; alignment risk is *differential* growth
(reach outrunning value-bundle preservation, bearer-map accuracy, transparency, correction). Establishes
predictive/control reach sets (eq:predictive-reach 169–177, eq:control-reach 180–188), five growth
modes (sensory/actuator/memory/model/coordination, 213–404), growth vector `ḃ_X` (eq:growth-vector
409–421), correction-growth condition (eq:correction-growth-condition 589–596), expansion-correction
ratio `χ_X` (eq:expansion-correction-ratio 880–886), capability shocks, conserved-property list, and
operational Stop/Start/Continue triggers (958–1012).

**ch13 — The Coordination Bottleneck** (`ch:coordination-bottleneck`).
Thesis (4–7): large-scale alignment fails when capability grows faster than the ability to coordinate
prediction, control, correction, incentives; collective competence = local + coordination gain − loss.
Establishes `B_coll = Σ ω_i B_i + G_coord − Ω_coord` (eq:collective-competence 106–116), the seven
losses (eq:coordination-losses 147–164), the cooperativity edge condition `κ_ij = b·p·ρ/c > 1`
(eq:kappa-coordination 369–376), percolation of coordination (eq:cooperation-percolation 404–413) —
the canonical percolation derivation for the book — mid-scale U-collapse (439–497), and the
control-vs-coordination balance (eq:control-coordination-balance 685–693).

**ch14 — When Intelligence Deepens Misalignment** (`ch:intelligence-deepens-misalignment`).
Thesis (4–7): intelligence deepens misalignment when power grows faster than correction; sharper
question is *which* capacities grow vs *which* correction capacities. Establishes a competence
functional restated as `K` (eq:competence-functional 75–86), the capacity split
`C_world/self/social/succ` vs `C_corr/trans/value` (114–123), the basic misalignment-growth condition
(eq:misalignment-growth-condition 128–149), alignment margin `M_A` (eq:alignment-margin 163–174),
five deepening mechanisms (216–414), the correction chain `W→O→J→D→C→U→A`
(eq:correction-chain 564–578), basin-exit geometry (638–662), and a minimal admissibility criterion
(eq:admissible-growth 884–910). Includes an explicit positive counterexample ("The Wise System", 727–764).

---

## B. Required-element compliance

All four chapters are **fully compliant** with the required-element checklist. Detail:

| Element | ch11 | ch12 | ch13 | ch14 |
|---|---|---|---|---|
| `\chapter` + `\label{ch:...}` | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) |
| `chapterthesis` env | ✓ (4–7) | ✓ (4–8) | ✓ (4–7) | ✓ (4–7) |
| Decision-relevance content | ✓ but back-loaded | ✓ but back-loaded | ✓ mid/late | ✓ front-loaded (§"Why This Matters" 15–24) |
| Failure-mode / counterexample | ✓ §898–944 | ✓ §1074–1127 | ✓ §751–821 | ✓ §766–807 + counterexample 727–764 |
| Section titled EXACTLY "What Would Change This View" | ✓ (1052) | ✓ (1184) | ✓ (999) | ✓ (949) |
| Summary | ✓ "Summary" (1067) | ✓ "Chapter summary" (1235) | ✓ "Summary" (1014) | ✓ "Summary" (964) |
| `refsection` + `\printbibliography[heading=subbibliography,...]` | ✓ (9 / 1085) | ✓ (10 / 1255) | ✓ (9 / 1063) | ✓ (9 / 997) |

Notes:
- **WWCTV present in all four with the exact title**, including the two chapters flagged in the task:
  ch12 (which ends in a "Conclusion") has WWCTV at line 1184 *before* the Conclusion (1199); ch14 (which
  ends in "Summary") has WWCTV at line 949 *before* the Summary (964). No renamed equivalents — no flag.
- **No `[STUB]`/`[TODO]`/`FIXME` markers** anywhere in ch11–ch14 (confirmed by search). (Such markers do
  exist in the redundancy-neighbor ch33, not in this part.)
- **Chapter-ending structure drifts** across the part (consistency, not a missing element): ch11 = Summary;
  ch12 = Conclusion + Chapter summary + Key definitions; ch13 = Summary + Chapter Claims + Open Problems;
  ch14 = Summary. ch12 uniquely carries both a "Conclusion" and a "Chapter summary" (mild internal
  redundancy, lines 1199–1238); ch13 uniquely adds "Chapter Claims" and "Open Problems". Recommend a
  consistent tail convention across the part.

---

## C. Continuity

Inter-chapter "previous/next" handoffs are **excellent and explicit**:
- **From Part II (ch10):** ch11:18 opens by referencing strategic opacity ("The previous chapter
  examined strategic opacity"). Clean incoming handoff.
- **ch11→ch12:** ch11:1079 promises "capability growth as boundary expansion"; ch12:19 picks it up
  ("The previous chapter developed how to measure capability"). ✓
- **ch12→ch13:** ch12:1231–1233 promises the coordination bottleneck; ch13:18–19 picks it up. ✓
- **ch13→ch14:** ch13:1036 promises "when increasing capability deepens misalignment"; ch14:29 picks it
  up with an explicit `\ref{ch:coordination-bottleneck}`. ✓
- **To Part IV (ch15):** ch14:988–991 promises "the structure of human values… a compressed bundle
  geometry"; ch15 is "Values Are Compressed Control Signals". ✓

**Broken cross-reference (continuity defect).** ch12:20 reads "Chapter~\ref{ch:finding-boundary}
introduced predictive and control information across the boundary, discounted by memory cost and
residual surprise." `ch:finding-boundary` resolves to **Chapter 7** (`chapters/ch07-finding-boundary.tex:2`;
confirmed `book.aux:663` → chapter 7). But the competence functional *with memory cost and residual
surprise discounting* is introduced in **ch11** (eq:biq, 212–223), the immediately previous chapter — not
ch7. Either the ref should be `\ref{ch:capability-without-task-ontology}` (most likely intended) or the
descriptive clause is mis-attributed. Flag for correction.

**Setup not abrupt, but value-machinery is assumed before it is defined.** ch12 (§3.2 bearer map `Φ_k`
line 540; §conserved value-bundle geometry `B_k` line 705), ch13 (§value coordination `B_k`, `Φ^(i)`
lines 644–663, 907–949), and ch14 (§value-bundle preservation 494–553) lean heavily on value-bundle
coordinates, bearer maps, and the correction channel — all of which are *defined later* (Part IV ch15–19,
and the correction-channel chapter). The forward dependence is acknowledged at chapter ends (ch12:1181–1182;
ch14:988–991) but **not flagged at first use**. Consider an early forward `\ref` at the first appearance of
`Φ`/`B_k` so a Part-III-only reader is not stranded.

---

## D. Redundancy

1. **MAJOR: ch11 coordination sections duplicate ch13's whole thesis.** ch11 §"Competence and
   Coordination" (402–442) states `B_H ≈ Σ ω_i B_{X_i} + B_coord − C_friction` (eq:collective-biq
   412–422), and ch11 §"The U-Shaped Coordination Pattern" (495–531) gives the efficiency law
   `η(N) ∝ N^{a−b−c−1} ρ(N)` (eq line 517). ch13 then re-states the *same* collective-competence
   equation as `B_coll = Σ ω_i B_i + G_coord − Ω_coord` (eq:collective-competence 106–116) and the
   *identical* efficiency law `η(N) ∝ N^{a−b−c−1} ρ(N)` (eq:coordination-efficiency-scaling 458–466,
   §"Mid-Scale Collapse" 439–497). **trim/cross-ref:** ch11's 402–531 should compress to a forward
   pointer to ch13; ch13 is the right home for the collective/U-shape material. Notation also drifts
   (`B_coord`/`C_friction` in ch11 vs `G_coord`/`Ω_coord` in ch13 — see §E).

2. **Competence functional restated 4×.** Defined ch11 (eq:biq 212–223), restated ch12
   (eq:biq-growth-start 46–56), restated ch13 (eq:local-competence 71–82), and **re-derived under a new
   symbol `K`** ch14 (eq:competence-functional 75–93 with full sub-definitions). ch12 and ch13
   restatements are short and justified (growth use / collective use). ch14's is a full re-derivation
   (~20 lines) — **trim/cross-ref:** reference eq:biq and reuse the established symbol rather than
   re-deriving (see §E for the `B`-vs-`K` clash).

3. **`κ` cooperativity index defined twice.** ch10 defines `κ_ij` first (`eq:kappa-ch10`,
   ch10:91–96). ch13 re-defines `κ_ij = b·p·ρ/c` from scratch ("This is a generalized Hamilton
   condition…", 369–378) **without acknowledging ch10's prior definition**. **trim/cross-ref:** ch13
   should cross-ref ch10:eq:kappa-ch10 at first use. (Downstream ch33:52 and ch35:140 also use `κ_ij`;
   both correctly cite ch13 — see point 4.)

4. **Percolation handled well downstream — KEEP ch13 as canonical.** ch13 §"Percolation of Coordination"
   (398–429, eq:cooperation-percolation 404–413) is the canonical derivation. ch35 explicitly inherits
   it ("This is the same cooperation graph analyzed in Chapter~\ref{ch:coordination-bottleneck}… We
   therefore inherit its percolation result rather than re-deriving it", ch35:180; again ch35:1028).
   ch33 also defers to ch13's "percolation form" (ch33:45, 74). No action needed beyond point 3 — the
   percolation redundancy risk the task flagged is **already mitigated** by correct downstream cross-refs.

5. **ch11↔ch12 boundary-expansion overlap (minor).** ch11 §"Non-Stationary Systems" (361–400; moving
   boundary `T_{t→t+1}`, "A firm hires employees. A model gains tools.") previews ch12's boundary-expansion
   thesis. This is acceptable foreshadowing (ch11:1079 explicitly hands off), but ch11's growing-boundary
   examples (385–392) and ch12's (97, 854–860) are near-duplicates. **keep** (light foreshadow), optionally
   trim ch11's examples.

6. **Three+ "control-vs-correction" ratio constructs.** `R_cap/corr` (ch11 eq:cap-corr-ratio 671–676),
   `χ_X` (ch12 eq:expansion-correction-ratio 880–886), `control-coordination balance` (ch13
   eq:control-coordination-balance 685–693), and the margin/condition `M_A` + misalignment-growth
   (ch14 163–174, 128–149). All encode the same theme. They are genuinely distinct (level-ratio vs
   growth-rate-ratio vs margin), so **keep**, but they are nowhere related to one another. Recommend one
   explicit cross-referencing sentence (e.g. in ch14) showing `R_cap/corr → χ_X → M_A` are the
   level/rate/margin forms of one inequality.

---

## E. Consistency (notation, symbols, capitalization)

1. **Competence-functional symbol drift `B` → `K`.** ch11/ch12/ch13 call the functional `B`
   (`B_X`, `B_i`, `B_coll`). ch14 calls it **`K`** (eq:competence-functional, 75–86) while *also* using
   `B_t` for the value bundle (505–507). The likely reason for the switch: avoid clashing with the
   value-bundle `B` — but the switch breaks consistency with the three prior chapters and with the
   book's stated spine (which names the functional `B`). **Pick one convention book-wide.** If the
   value-bundle/competence clash is the driver, fix it once (see point 2) rather than per-chapter.

2. **`B` symbol clash: competence vs value-bundle, *within the same chapters*.** In ch12, `B_X` =
   competence (eq:biq-growth-start 46) while `B_k` = value-bundle coordinate (§conserved geometry 705).
   In ch13, `B_i` = competence (71) while `B_k` = value-bundle coordinate (656). Same letter, two
   unrelated objects, same chapter. This is the root clash that ch14 sidesteps with `K`. Flag and
   resolve globally.

3. **Coefficient set vs the spine.** The spine states `B = I_pred + I_ctrl − βH − γS`. The manuscript
   functional carries an extra control weight `α`: `I_pred + α I_ctrl − β H − γ S` (ch11:217, ch12:51,
   ch13:77, ch14:80). The chapters are **internally consistent** (all four include `α`, default `α=1`
   per ch11:225–226); the *spine description* omits `α`. Not a chapter defect — note the spine wording
   should include `α` (or the chapters should justify dropping it).

4. **Residual-surprise symbol drift.** ch11 uses `S_X` (eq:residual-surprise 200–206) and `S` inside
   `B`. ch12 uses `S_X` (348). ch13 uses `S^(i)` (80). ch14 uses calligraphic **`\mathcal{S}`** (84, 92).
   Harmonize to one glyph.

5. **Collective-competence notation drift (ch11 vs ch13).** `B_coord` / `C_friction` (ch11 eq 412–422)
   vs `G_coord` / `Ω_coord` (ch13 eq 106–116) for the same two quantities. Pick one (and per §D.1,
   ideally state it only in ch13).

6. **`η` overloaded.** In ch11, `η` is competence-to-growth efficiency (eq 466) *and* coordination
   efficiency `η(N)` (eq 515) — two different quantities in one chapter. ch13 also uses `η(N)` for
   coordination efficiency (463). Disambiguate the ch11 growth-efficiency `η` from the coordination
   `η(N)`.

7. **Denominator of the key claim drifts: "correction" vs "coordination".** The book's canonical claim
   ("dangerous when control grows faster than *correction-channel* capacity") is stated with a
   *correction* denominator in ch11 (688–691), ch12 (589–596), and ch14 (thesis + eq 128–149). ch13's
   core inequality (eq:control-coordination-balance 685–693) instead uses a **coordination** denominator
   `dB_control/dt ≤ dB_coord/dt + ε`; its Chapter Claim #5 (1046) hedges to "coordination *and*
   correction". This is defensible (ch13's subject is coordination) but the substitution should be made
   explicit so the spine's key claim reads consistently across the part.

8. **Section-title capitalization: ch12 is the outlier.** ch11, ch13, ch14 use Title Case
   ("The Seven Losses of Coordination", "Why This Matters"). **ch12 uses sentence case**
   ("The central claim", "Why benchmark growth is not enough", "Boundary expansion", "The five basic
   modes of capability growth", etc.). Normalize ch12 to match.

9. **Functional naming.** ch11 names it "blanket-information competence" (247); ch13 echoes
   "blanket-information measure of competence" (85) — consistent. The citekey is `zarncke2025biq`
   ("bitwise IQ"); prose never says "bitwise IQ". Consistent within the part; just note prose/citekey
   divergence.

---

## F. Open tangents / dangling promises

- **ch12:20 broken/mis-pointed cross-ref** (see §C) — the only hard reference defect found.
- **Value machinery used before defined** (ch12/13/14) with forward acknowledgement only at chapter
  ends — see §C. Not dangling (Part IV delivers), but first-use forward `\ref`s are missing.
- **ch11:765** "That problem belongs to later chapters on value-bundle transport." — resolved by Part IV;
  no `\ref`. Add one.
- **ch12:1182** promises value-bundle geometry, bearer import, correction-channel theory, successor
  certification "to later chapters" — resolved by Parts IV/V but with no `\ref`s. Add forward refs.
- **ch13 §"Open Problems" (1049–1057)** explicitly lists five unresolved threads (estimating `B_coll`,
  artifact selection, adversarial correction measurement, thresholds for `κ_ij`/`φ_c`, when institutions
  recover coordination). These are intentional open problems, not defects — but none are picked up by a
  later `\ref` in this part; confirm they are addressed in Parts V/VI or marked as genuinely open.
- No abandoned threads or contradicted promises detected within the four chapters.

---

## G. Continuity hand-off (assumed-in / introduced-out)

**Incoming concepts assumed (from Parts I–II):**
- Strategic opacity and the cooperativity index `κ_ij` (ch10) — ch11/13 build on these; ch13 should
  cross-ref ch10's `κ` (§D.3).
- The agent boundary `(I,S,A,E)` and boundary discovery (ch6–ch7, `ch:finding-boundary`) — assumed
  throughout; the ch12:20 ref to it is mis-described (§C).
- Markov-blanket / good-regulator / empowerment background (cited via `conant1970regulator`,
  `salge2014empowerment`, `tishby2000ib`) — consistently carried.

**Outgoing concepts introduced for later parts:**
- The competence functional `B`/`K` and horizon profile `B^(h)` → used by Part V practice chapters and
  reused by ch33/ch35 percolation.
- Value-bundle coordinates `B_k`, bearer map `Φ`, value-bundle response geometry `G_B`
  (ch12/13/14) → formally defined in Part IV (ch15–19: `ch:values-compressed-control`,
  `ch:value-bundle-model`, `ch:bearer-maps`, `ch:tradeoffs-bundle-geometry`). Hand-off to ch15 is clean
  (ch14:988–991).
- Correction-channel chain `W→O→J→D→C→U→A` and `C_corr` (ch12:566–586, ch14:564–606) → the
  correction-channel-integrity chapter (referenced from ch33:106 as `ch:correction-channel-integrity`).
- Successor certification `S_certified` (ch12:611, ch14:373–377) → successor/construction chapters
  (cited `zarncke2025construction`).
- Percolation/`φ_c` → correctly re-used and cross-referenced by ch33 and ch35 (§D.4).

Overall the part is a well-sequenced spine: ch11 defines the measure, ch12 makes it dynamic
(growth=expansion), ch13 makes it collective (coordination), ch14 makes it normative (deepening
misalignment + correction basin). The main work items are notational unification (`B`/`K`, `S`,
`η`, gain/loss symbols), the ch12:20 cross-ref fix, de-duplication of ch11's coordination/U-shape
sections against ch13, and adding first-use forward refs for the value machinery.
