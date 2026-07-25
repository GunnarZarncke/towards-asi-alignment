# Part VII Review — Successors, Reproduction, and Continuity (ch46–ch48)

Reviewer pass. No manuscript files were edited. Line numbers refer to the current
`chapters/*.tex` sources.

Scope: `ch46-successor-central-test.tex`, `ch48-conserved-properties.tex`,
`ch46-self-modeling-self-opacity.tex`, `ch48-certification-without-construction.tex`.

---

## TOP-LINE FINDINGS (read first)

1. **WWCTV missing in ALL FOUR chapters.** None of ch46/29/30/31 contains a
   "What Would Change This View" section (verified by grep across `chapters/`).
   ch46 and ch48 (Part VI) both have it; the whole of Part VII drops it. This is
   the single most consistent required-element failure in the part.
2. **The "seven conserved properties" is not one list — it is at least three
   different lists** that drift across ch46, ch48, and ch48 (and a fourth, fifth
   sub-list inside ch48). The book repeatedly says "the seven" as if canonical,
   but the membership, naming, and order change each time. This is both a
   redundancy problem (same idea enumerated 3–5×) and a consistency problem
   (the enumerations disagree). See §E.
3. **B / Φ (value-bundle vector + bearer map) are re-derived from scratch in
   ch46, ch48, ch46, and ch48** — four re-introductions of Part IV material
   (ch16/ch18), with drifting example lists. See §D.
4. **No `[STUB]`/`[TODO]` markers** in any of the four chapters (grep clean).
5. Required scaffolding otherwise present: every chapter has `\chapter`+`\label`,
   `chapterthesis`, `refsection`+`\printbibliography`, decision triggers, and
   failure-mode/counterexample material.

---

## A. CAPSULES

**ch46 — Successor Creation as the Central Alignment Test** (`ch:successor-central-test`).
The thesis chapter of the part: local alignment is insufficient; alignment must
be *closed* under successor creation (copies, fine-tunes, delegates, scaffolds,
designed/institutional/merged successors). Defines the successor relation
information-theoretically, the successor-channel principle, a conserved-property
set, a successor alignment condition, the self-improvement/auditability gap, goal
transport, delegation and institutional succession, a six-question certification
procedure, stop conditions, worked examples, a philosophical edge, and an
eight-claim minimal safety case. Long (782 lines) and does a great deal of the
part's conceptual work — including substantial previews of ch48/ch46/ch48.

**ch48 — Conserved Properties Across Successors** (`ch:conserved-properties`).
The dedicated enumeration chapter: identity-as-invariance, the **seven** conserved
properties (boundary closure, memory lineage, value-bundle response geometry,
bearer-map continuity, correction-channel capacity, transparency/self-transparency,
control-locus continuity), each with a failure mode; a composite conservation
score; slow-drift/path problem; adversarial conservation; worked examples;
stop/start/continue conditions; a "why these are not enough" section. The
canonical home for the seven-property list.

**ch46 — Better Self-Modeling Can Be Worse** (`ch:self-modeling-self-opacity`).
The home chapter for self-modeling vs self-transparency vs self-control vs
self-honesty. Central inequality: `d/dt C_self > d/dt T_corr + ε` is the danger
regime ("transparency debt"). Recursive depth vs opacity, the selfhood
bottleneck, value-bundle opacity, goal laundering, correction-channel asymmetry,
examples, diagnostics, design principles, relation to successor alignment,
philosophical edge, a practical stop rule. Ends with Conclusion + Key definitions
+ Chapter propositions.

**ch48 — Certification Without Construction** (`ch:certification-without-construction`).
Reframes the alignment problem from "construct an aligned ASI" to "certify a
restricted class". Certification envelope `(C,E,M,T,δ)`; a seven-domain
certification class (boundary, competence/growth, value-bundle geometry, bearer
maps, correction integrity, transparency/self-modeling balance, successor
closure); six guarantee types; adversarial certification; safety case;
local-first path; decision triggers; examples; "where certification becomes
construction"; philosophical limit. Ends with Chapter summary + Key definitions +
Exercises.

---

## B. REQUIRED-ELEMENT COMPLIANCE

| Element | ch46 | ch48 | ch46 | ch48 |
|---|---|---|---|---|
| `\chapter` + `\label` | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) |
| `chapterthesis` env | ✓ (4–6) | ✓ (4–6) | ✓ (4–6) | ✓ (4–6) |
| Decision relevance | ✓ stop conds (606), safety case (719) | ✓ stop/start/continue (906) | ✓ practical stop rule (710), diagnostics (447) | ✓ decision triggers (553) |
| Failure-mode / counterexample | ✓ examples & counterexamples (657) | ✓ failure modes + worked examples (834) | ✓ examples incl. apparent counterexample (436) | ✓ examples (606) |
| **EXACT "What Would Change This View"** | **✗ MISSING** | **✗ MISSING** | **✗ MISSING** | **✗ MISSING** |
| Summary section | ✓ "Summary" (750) | ✓ "Summary" (984) | ✓ "Conclusion" (739) | ✓ "Chapter summary" (704) |
| `refsection` + `\printbibliography` | ✓ (8 / 779) | ✓ (8 / 1020) | ✓ (8 / 786) | ✓ (8 / 740) |
| `[STUB]`/`[TODO]` markers | none | none | none | none |

**Flag B-1 (CRITICAL, all four chapters): no WWCTV section.** Required exactly as
"What Would Change This View". ch46's `\section*{Chapter propositions}` (772) and
ch48's `\section*{Exercises and research prompts}` (723) gesture at
falsifiability/self-test but are **not** equivalents and should be flagged as
non-substitutes. Each chapter has rich falsification material already present that
could seed a WWCTV section:
- ch46: §"Stop conditions" (606) and the safety-case claims are effectively
  falsification triggers but never framed as WWCTV.
- ch48: §"Why These Properties Are Not Enough" (957) is the closest in spirit but
  is a limitations section, not WWCTV.
- ch46: §"The apparent counterexample" (436) + Chapter propositions (772).
- ch48: §"Where certification becomes construction" (654) + Exercises (723).

**Flag B-2 (minor): chapter-ending name drift.** "Summary" (ch46, ch48) vs
"Conclusion" (ch46) vs "Chapter summary" (ch48). Pick one convention.

**Flag B-3 (minor): structural asymmetry.** ch46 and ch48 carry
`\section*{Key definitions}` (and ch46 `Chapter propositions`, ch48 `Exercises`);
ch46 and ch48 do not. Not required, but inconsistent within a single part.

---

## C. CONTINUITY (intra-part flow + Part VI / Part VIII handoffs)

**Incoming from Part VI (ch48, manipulation/false consent).** Clean. ch46 and
ch48 both cross-reference `ch:manipulation-false-consent` (ch46:545, ch48:335),
and the correction-channel apparatus is inherited from ch46/ch48. No dangling
back-reference problems.

**ch46 → ch48.** ch46 closes by pointing forward to ch48 (773), and ch48 opens by
citing `ch:successor-central-test` (20). Conceptually smooth — but see the
over-preview problem below.

**ch48 → ch46.** ch48 ends pointing to `ch:self-modeling-self-opacity` (1014); ch46
opens on exactly that distinction. ch48's property #6 ("Transparency and
self-transparency policy", 546) explicitly forward-references ch46 (578). Good.

**ch46 → ch48.** ch46 ends pointing to `ch:certification-without-construction`
(756); ch48 opens on the construction-vs-certification framing. Good.

**ch48 → Part VIII (ch46, selection).** ch48 ends pointing to
`ch:selection-environment` (709); ch46 opens by summarizing Chapters
`ch:successor-central-test`–`ch:certification-without-construction` (ch46:17) and
turning to selection. Clean handoff.

**Flag C-1 (MAJOR — ch46 over-previews ch48).** ch46 §"Conserved properties"
(140–323) is a *full* development of conserved properties with subsections for
value-bundle response geometry (167), bearer-map preservation (191),
correction-channel capacity (217), memory lineage (276), boundary closure (291),
and transparency policy (308) — each with its own formula. This is essentially
ch48's chapter delivered in advance, minus "control-locus continuity". When the
reader reaches ch48, the six core formulas (boundary closure CMI, CCI penalty
decomposition, the J_B/H_ij derivatives, the Φ→[0,1] map, memory-lineage MI) are
*repeats*, not first introductions. Recommend ch46 demote its conserved-property
section to a brief motivating sketch and defer the formal treatment to ch48.

**Flag C-2 (MAJOR — ch48 certification class is redundant with ch46's
certification section).** ch46 already contains §"Successor certification"
(547–604, six questions: boundary, capability, bundle, bearer, correction,
succession) **and** §"A minimal successor safety case" (719–748, eight claims).
ch48 then builds the certification-class conjunction (92–351, seven domains) and a
ten-claim safety case (485–521). These are the same artifact at two locations: a
gated, multi-invariant successor check expressed as a safety case. ch46's six
questions and ch48's seven domains are near-isomorphic. Recommend ch46's
certification section be cut to a forward pointer ("certification is developed in
ch48") and the safety-case machinery live once in ch48.

---

## D. REDUNDANCY (duplications, with keep vs trim verdicts)

This part has the highest internal redundancy of any I've reviewed. The same
half-dozen formulas recur in three or four chapters.

### D-1. The seven-property enumeration (ch46 vs ch48 vs ch48) — **TRIM/CROSS-REF**
- ch46: conserved-property subsections (140–323); invariant profile
  `I(A)={G_B,Φ,U_H,CCI,M,C,γ}` (332–338); repeated in Summary (756–763).
- ch48: §"The Seven Conserved Properties" list (125–138) + full section per
  property (149–671) + Summary list (990–1000).
- ch48: §"The shape of a certification class" seven domains (97–105) + a per-domain
  section (116–351) + the successor-closure sub-list (338–348).
- Verdict: **ch48 keep (canonical home).** ch46 and ch48 should reference ch48's
  list rather than re-enumerate with their own formulas. The triplication of the
  underlying *formulas* (not just names) is true duplication.

### D-2. Boundary-closure CMI formula `I(I;E|S,A)≤ε` — **TRIM (true duplication)**
Appears verbatim (up to primes) in ch46:298, ch48:156 & 195, ch48:121 & 135. Four
chapters, same conditional-mutual-information partition definition with the same
gloss. Keep once (ch48), cross-ref elsewhere.

### D-3. Correction chain `W→O→J→D→C→U→A` + CCI penalty decomposition — **TRIM**
The identical seven-node chain with the identical itemized gloss appears in
ch46:222–264, ch48:445–493, ch46:362–372, ch48:248–278. The
`CCI = C_corr − λ_L L − λ_M M − λ_R R − λ_O O_mismatch` formula appears in
ch46:252, ch48:482, ch48:264. This is canonically ch46 (correction-channel
integrity) material; all four chapters re-state it. Keep a one-line reminder +
cross-ref to ch46; remove the full re-derivation from at least ch46, ch46, ch48.

### D-4. Value-bundle vector B + response geometry G_B (∂π/∂B, ∂²π/∂B∂B) — **TRIM**
Re-introduced as Part IV material in ch46:155 & 170–178, ch48:277 & 283–367,
ch46:280–296, ch48:179–199. Each re-defines B as "a low-dimensional vector of
value-bundle coordinates (Chapter ref)" and re-derives the first/second-order
policy derivatives. Keep the formal object once (ch48 has the fullest treatment
incl. second-order H_ij and R_B), cross-ref from the others.

### D-5. Bearer map Φ: z_world → [0,1] — **TRIM**
Re-introduced in ch46:198 & 196–215, ch48:375–409, ch46:282–308, ch48:216–228.
Same map signature, same "preserve the word while changing the bearer" warning,
same edge-case roster (children, cognitively impaired, uploads, simulated minds,
animals, future persons, merged entities). The edge-case list itself recurs
nearly verbatim: ch46:586, ch48:413 & 804, ch48:232–239. Keep once (ch18 is the
canonical bearer-map chapter; within the part, ch48), cross-ref.

### D-6. Self-modeling vs self-transparency (d↑, τ↑) and `τ = 1 − I(M;M̂)/H(M)` — **MIXED**
- ch46 §"Self-improvement and the auditability gap" (375–408): introduces
  C_self/C_audit, `d↑, τ↑`, and the safe-trajectory inequality.
- ch48 §"Self-Modeling Versus Self-Transparency" (575–607): re-introduces d, τ,
  the same opacity formula, and the `d'>d ∧ τ'>τ` failure.
- ch46 (home): the full treatment, opacity formula at 213–219.
- ch48 §"Transparency and self-modeling balance" (292–319): re-states d, τ,
  `d↑, τ↑` again.
- Verdict: ch46 **keep (home)**. ch46's gap section and ch48's subsection are
  **partial previews** — ch46:389 even spells out "better self-modeling but worse
  self-transparency", which is ch46's *title*. Trim ch46 and ch48 to a
  one-sentence pointer to ch46; ch48's restatement should cross-ref ch46 (it does
  cite it at 295 but still re-derives).
- Note the broader spread flagged in the task (ch08/ch10/ch12/ch14/ch46/ch46):
  by the time the reader reaches ch46, the d/τ distinction has been previewed
  many times. Within this part, ch46 and ch48 are the two avoidable
  over-introductions; ch46 should be the first place the opacity formula is
  *derived*, not the fourth.

### D-7. Successor-certification schema / safety case — **TRIM** (see Flag C-2)
ch46's six questions (552) + eight-claim safety case (719) vs ch48's seven domains
(97) + ten-claim safety case (492). Same schema twice. Consolidate into ch48.

### D-8. Stop/start/continue condition blocks — **MIXED**
ch46 §"Stop conditions" (606), ch48 §"Stop, Start, and Continue Conditions"
(906), ch46 §"A practical stop rule" (710), ch48 §"Decision triggers" (553). Four
operational gate-lists with overlapping triggers (CCI<θ, d_Φ>ε_Φ, d_B>ε_B,
correction loses causal force, opacity rises near control variables, uncertified
successors). Some repetition is **keep (pedagogical)** — each chapter wants a
usable checklist — but the *trigger formulas* are duplicated. Suggest a single
canonical trigger table (ch48, the certification chapter) and short
chapter-specific subsets elsewhere.

---

## E. CONSISTENCY — the "seven" do NOT match across chapters (FLAG)

The three principal enumerations disagree in membership, naming, and order:

**ch48 (canonical seven; 125–138 / 990–1000):**
1 boundary closure · 2 memory lineage · 3 value-bundle response geometry ·
4 bearer-map continuity · 5 correction-channel capacity ·
6 transparency & self-transparency policy · 7 control-locus continuity.

**ch46 invariant profile (332–338 / 756–763):**
`I(A) = {G_B, Φ, U_H, CCI, M, C, γ}` =
value-bundle response geometry · bearer maps · **human correction operator U_H** ·
**correction-channel integrity CCI** · memory lineage · boundary closure ·
transparency policy.
→ **Differs from ch48**: ch46 *splits correction into two members* (U_H operator
**and** CCI) and **omits control-locus continuity** entirely. So ch46's "seven"
≠ ch48's "seven" despite both claiming the conserved-property set. Order also
differs.

**ch48 certification domains (97–105):**
1 boundary closure · 2 **competence limits and growth rates** · 3 value-bundle
geometry · 4 bearer-map preservation · 5 correction-channel integrity ·
6 transparency & self-modeling balance · 7 **successor closure**.
→ **Differs from ch48**: ch48 *adds* "competence/growth rate" and "successor
closure" as members and *drops* "memory lineage" and "control-locus continuity"
from the seven (memory lineage reappears only inside successor closure's sub-list).

**ch48 successor-closure sub-list (338–348)** is yet *another* seven:
boundary closure, memory lineage, value-bundle geometry, bearer maps,
correction-channel integrity, transparency balance, **operating-envelope
inheritance** — i.e. control-locus replaced by operating-envelope inheritance.

**Verdict E-1 (MAJOR):** The manuscript treats "the seven conserved properties"
as a fixed canonical list but presents at least three mutually inconsistent
seven-tuples (plus a fourth sub-list). Either (a) declare ch48 canonical and make
ch46/ch48 quote it exactly, or (b) explicitly acknowledge that ch48's
certification domains are a *re-packaging* (folding memory + control-locus into
successor closure, adding competence-growth) rather than the same seven. As
written, a careful reader who tries to line up "the seven" across the three
chapters will find they do not match.

**Verdict E-2 (consistency — value-bundle example lists drift):**
- ch46:155 — care, non-suffering, truth, autonomy, justice, loyalty, dignity,
  beauty, **legitimacy**.
- ch48:279 — non-suffering, care, truth, autonomy, justice, loyalty, dignity,
  beauty, **prudence**.
- ch46:280 — non-suffering, **protection**, care, truth, autonomy, justice,
  loyalty, dignity, beauty.
- ch48:185 — **protection**, non-suffering, care, **truth-contact**, autonomy,
  justice, loyalty, dignity, beauty.
Four chapters, four different illustrative bundles ("legitimacy" / "prudence" /
"protection" / "truth-contact"). Recommend aligning to the canonical roster in
ch16 (Part IV) and using it consistently.

**Verdict E-3 (citation key inconsistency):** boundary-closure / boundaries cite
is `\autocite{critch4622boundaries}` in ch46:294 but
`\autocite{critch4622boundaries3a}` in ch48:152, ch48:1018, ch48:123, ch48:738.
Two different bib keys for what appears to be the same Critch boundaries work —
verify the `.bib` and unify.

**Verdict E-4 (section-title capitalization):** ch48 uses **Title Case** section
headings ("The Successor Problem", "Identity as Invariance, Not Sameness", "The
Seven Conserved Properties", "Boundary Closure", …). ch46, ch46, ch48 use
**sentence case** ("The local alignment fallacy", "The dangerous ambiguity of
'knowing itself'", "The construction demand"). ch48 is the odd one out; normalize.

**Verdict E-5 (notation — correction-channel capacity vs integrity):** ch46
labels its property "correction-channel capacity" but the conserved object it uses
is CCI (integrity, capacity minus penalties); ch48 property #5 is "correction-
channel capacity" but again formalized as CCI; ch48 calls the domain "correction-
channel integrity". The capacity/integrity terms are used loosely and sometimes
interchangeably. Pick one name per concept (C_corr = capacity; CCI = integrity)
and apply consistently.

---

## F. OPEN TANGENTS / DANGLING PROMISES

- **F-1 (ch46:413):** cites `Chapter~\ref{ch:goal-transport}` for goal transport.
  Confirm a chapter with label `ch:goal-transport` exists and is the intended
  target; goal transport is developed at length *inside* ch46 (§410–493), so the
  cross-ref may be self-referential or point to a Part IV/V chapter — verify.
- **F-2 (ch48:525 & ch48:284):** both cite `ch:extrapolative-correction` (ch46)
  for the "extrapolative value governance" `V_{t+1}=U_H(V_t,E_t,D_t)` operator.
  Consistent and fine — just noting the operator is introduced in ch46 and
  re-stated here; keep as cross-ref, do not re-derive.
- **F-3 (ch46 "U_H" vs ch46):** ch46 introduces `U_H` (correction operator) as a
  conserved invariant member but never gives it a formula in ch46 (only named at
  159, 335). ch48 (531) and ch48 (286) give `V_{t+1}=U_H(...)`. ch46's invariant
  profile depends on an object it does not define locally — reader must already
  know ch46. Minor, but the dependency is implicit.
- **F-4 (ch46 selfhood bottleneck, 248–276):** `β_self = I(G_t;S_t)/H(G_t)` and
  the self-index S_t are introduced here and cited to consciousness literature
  (Graziano, Rosenthal). This is a genuinely new construct that is *not* picked up
  anywhere later in the part (ch48 does not use β_self). It reads as a partly
  orphaned tangent — either tie it into ch48's certification invariants or flag it
  as exploratory.
- **F-5 (ch48 Exercises, 723–734):** the eight research prompts are good but are
  the only such block in the part; if exercises are not a book-wide convention
  this is an inconsistency, if they are, ch46–ch46 are missing them.

No broken `\ref`/`\label` were detected within the four files themselves; the
forward/back chapter pointers (773, 1014, 756, 709) all resolve to labels that
exist (`ch:conserved-properties`, `ch:self-modeling-self-opacity`,
`ch:certification-without-construction`, `ch:selection-environment`).

---

## G. CONTINUITY HAND-OFF (incoming / outgoing concepts)

**Incoming (relied upon, defined earlier):**
- Value-bundle vector B, response geometry G_B — ch15/ch16 (Part IV).
- Bearer map Φ — ch18 (Part IV).
- Correction-channel chain + CCI — ch46 (Part VI).
- Manipulation / false consent / domestication — ch48 (Part VI).
- Boundary closure / Markov-blanket partition — ch07/ch12 + Critch.
- Strategic opacity, self-modeling/self-transparency seed — ch10, ch14
  (over-previewed; see D-6).

**Outgoing (introduced here, used later):**
- Successor relation + successor-closure (ch46) → assumed by ch48, ch46, ch48,
  ch46.
- Seven conserved properties (ch48) → certification class (ch48), selection
  (ch46).
- Transparency debt / audit ratio (ch46) → certification transparency claim
  (ch48:499).
- Certification envelope `(C,E,M,T,δ)` + guarantee types (ch48) → ch46
  (safety-case) and ch48 (towards-alignment) likely consume this; verify those
  chapters reference `ch:certification-without-construction`.
- β_self / selfhood bottleneck (ch46) → **not consumed downstream within the
  part** (see F-4).

Handoff to Part VIII (ch46) is explicit and correct: ch46:17 names the
ch46–ch48 span and pivots to selection pressure.

---

## PRIORITIZED RECOMMENDATIONS

1. **Add a "What Would Change This View" section to each of ch46, ch48, ch46,
   ch48** (CRITICAL, required element; material already exists in each chapter's
   limitations/stop-condition/proposition blocks to seed it).
2. **Reconcile "the seven."** Declare ch48 canonical; make ch46's invariant
   profile and ch48's certification domains either quote it or explicitly state
   they are a re-packaging. Fix the U_H-vs-CCI double-count in ch46 and the
   memory-lineage/control-locus drop in ch48. (MAJOR consistency.)
3. **De-duplicate the formal apparatus** (boundary CMI, CCI chain, B/G_B
   derivatives, Φ map): derive once (ch48 / cross-ref ch18/ch46), cross-ref
   elsewhere. Trim ch46's full conserved-property section (Flag C-1) and the
   ch46/ch48 double safety case (Flag C-2).
4. **Move the self-modeling/self-transparency derivation to its home (ch46);**
   reduce ch46:375–408 and ch48:575–607 to pointers.
5. **Cosmetic consistency:** unify chapter-ending name, ch48 section
   capitalization, the `critch4622boundaries` bib key, and the value-bundle
   example roster.
