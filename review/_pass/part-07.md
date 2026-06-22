# Part VII Review — Successors, Reproduction, and Continuity (ch28–ch31)

Reviewer pass. No manuscript files were edited. Line numbers refer to the current
`chapters/*.tex` sources.

Scope: `ch28-successor-central-test.tex`, `ch29-conserved-properties.tex`,
`ch30-self-modeling-self-opacity.tex`, `ch31-certification-without-construction.tex`.

---

## TOP-LINE FINDINGS (read first)

1. **WWCTV missing in ALL FOUR chapters.** None of ch28/29/30/31 contains a
   "What Would Change This View" section (verified by grep across `chapters/`).
   ch26 and ch27 (Part VI) both have it; the whole of Part VII drops it. This is
   the single most consistent required-element failure in the part.
2. **The "seven conserved properties" is not one list — it is at least three
   different lists** that drift across ch28, ch29, and ch31 (and a fourth, fifth
   sub-list inside ch31). The book repeatedly says "the seven" as if canonical,
   but the membership, naming, and order change each time. This is both a
   redundancy problem (same idea enumerated 3–5×) and a consistency problem
   (the enumerations disagree). See §E.
3. **B / Φ (value-bundle vector + bearer map) are re-derived from scratch in
   ch28, ch29, ch30, and ch31** — four re-introductions of Part IV material
   (ch16/ch18), with drifting example lists. See §D.
4. **No `[STUB]`/`[TODO]` markers** in any of the four chapters (grep clean).
5. Required scaffolding otherwise present: every chapter has `\chapter`+`\label`,
   `chapterthesis`, `refsection`+`\printbibliography`, decision triggers, and
   failure-mode/counterexample material.

---

## A. CAPSULES

**ch28 — Successor Creation as the Central Alignment Test** (`ch:successor-central-test`).
The thesis chapter of the part: local alignment is insufficient; alignment must
be *closed* under successor creation (copies, fine-tunes, delegates, scaffolds,
designed/institutional/merged successors). Defines the successor relation
information-theoretically, the successor-channel principle, a conserved-property
set, a successor alignment condition, the self-improvement/auditability gap, goal
transport, delegation and institutional succession, a six-question certification
procedure, stop conditions, worked examples, a philosophical edge, and an
eight-claim minimal safety case. Long (782 lines) and does a great deal of the
part's conceptual work — including substantial previews of ch29/ch30/ch31.

**ch29 — Conserved Properties Across Successors** (`ch:conserved-properties`).
The dedicated enumeration chapter: identity-as-invariance, the **seven** conserved
properties (boundary closure, memory lineage, value-bundle response geometry,
bearer-map continuity, correction-channel capacity, transparency/self-transparency,
control-locus continuity), each with a failure mode; a composite conservation
score; slow-drift/path problem; adversarial conservation; worked examples;
stop/start/continue conditions; a "why these are not enough" section. The
canonical home for the seven-property list.

**ch30 — Better Self-Modeling Can Be Worse** (`ch:self-modeling-self-opacity`).
The home chapter for self-modeling vs self-transparency vs self-control vs
self-honesty. Central inequality: `d/dt C_self > d/dt T_corr + ε` is the danger
regime ("transparency debt"). Recursive depth vs opacity, the selfhood
bottleneck, value-bundle opacity, goal laundering, correction-channel asymmetry,
examples, diagnostics, design principles, relation to successor alignment,
philosophical edge, a practical stop rule. Ends with Conclusion + Key definitions
+ Chapter propositions.

**ch31 — Certification Without Construction** (`ch:certification-without-construction`).
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

| Element | ch28 | ch29 | ch30 | ch31 |
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
"What Would Change This View". ch30's `\section*{Chapter propositions}` (772) and
ch31's `\section*{Exercises and research prompts}` (723) gesture at
falsifiability/self-test but are **not** equivalents and should be flagged as
non-substitutes. Each chapter has rich falsification material already present that
could seed a WWCTV section:
- ch28: §"Stop conditions" (606) and the safety-case claims are effectively
  falsification triggers but never framed as WWCTV.
- ch29: §"Why These Properties Are Not Enough" (957) is the closest in spirit but
  is a limitations section, not WWCTV.
- ch30: §"The apparent counterexample" (436) + Chapter propositions (772).
- ch31: §"Where certification becomes construction" (654) + Exercises (723).

**Flag B-2 (minor): chapter-ending name drift.** "Summary" (ch28, ch29) vs
"Conclusion" (ch30) vs "Chapter summary" (ch31). Pick one convention.

**Flag B-3 (minor): structural asymmetry.** ch30 and ch31 carry
`\section*{Key definitions}` (and ch30 `Chapter propositions`, ch31 `Exercises`);
ch28 and ch29 do not. Not required, but inconsistent within a single part.

---

## C. CONTINUITY (intra-part flow + Part VI / Part VIII handoffs)

**Incoming from Part VI (ch27, manipulation/false consent).** Clean. ch28 and
ch29 both cross-reference `ch:manipulation-false-consent` (ch28:545, ch29:335),
and the correction-channel apparatus is inherited from ch26/ch27. No dangling
back-reference problems.

**ch28 → ch29.** ch28 closes by pointing forward to ch29 (773), and ch29 opens by
citing `ch:successor-central-test` (20). Conceptually smooth — but see the
over-preview problem below.

**ch29 → ch30.** ch29 ends pointing to `ch:self-modeling-self-opacity` (1014); ch30
opens on exactly that distinction. ch29's property #6 ("Transparency and
self-transparency policy", 546) explicitly forward-references ch30 (578). Good.

**ch30 → ch31.** ch30 ends pointing to `ch:certification-without-construction`
(756); ch31 opens on the construction-vs-certification framing. Good.

**ch31 → Part VIII (ch32, selection).** ch31 ends pointing to
`ch:selection-environment` (709); ch32 opens by summarizing Chapters
`ch:successor-central-test`–`ch:certification-without-construction` (ch32:17) and
turning to selection. Clean handoff.

**Flag C-1 (MAJOR — ch28 over-previews ch29).** ch28 §"Conserved properties"
(140–323) is a *full* development of conserved properties with subsections for
value-bundle response geometry (167), bearer-map preservation (191),
correction-channel capacity (217), memory lineage (276), boundary closure (291),
and transparency policy (308) — each with its own formula. This is essentially
ch29's chapter delivered in advance, minus "control-locus continuity". When the
reader reaches ch29, the six core formulas (boundary closure CMI, CCI penalty
decomposition, the J_B/H_ij derivatives, the Φ→[0,1] map, memory-lineage MI) are
*repeats*, not first introductions. Recommend ch28 demote its conserved-property
section to a brief motivating sketch and defer the formal treatment to ch29.

**Flag C-2 (MAJOR — ch31 certification class is redundant with ch28's
certification section).** ch28 already contains §"Successor certification"
(547–604, six questions: boundary, capability, bundle, bearer, correction,
succession) **and** §"A minimal successor safety case" (719–748, eight claims).
ch31 then builds the certification-class conjunction (92–351, seven domains) and a
ten-claim safety case (485–521). These are the same artifact at two locations: a
gated, multi-invariant successor check expressed as a safety case. ch28's six
questions and ch31's seven domains are near-isomorphic. Recommend ch28's
certification section be cut to a forward pointer ("certification is developed in
ch31") and the safety-case machinery live once in ch31.

---

## D. REDUNDANCY (duplications, with keep vs trim verdicts)

This part has the highest internal redundancy of any I've reviewed. The same
half-dozen formulas recur in three or four chapters.

### D-1. The seven-property enumeration (ch28 vs ch29 vs ch31) — **TRIM/CROSS-REF**
- ch28: conserved-property subsections (140–323); invariant profile
  `I(A)={G_B,Φ,U_H,CCI,M,C,γ}` (332–338); repeated in Summary (756–763).
- ch29: §"The Seven Conserved Properties" list (125–138) + full section per
  property (149–671) + Summary list (990–1000).
- ch31: §"The shape of a certification class" seven domains (97–105) + a per-domain
  section (116–351) + the successor-closure sub-list (338–348).
- Verdict: **ch29 keep (canonical home).** ch28 and ch31 should reference ch29's
  list rather than re-enumerate with their own formulas. The triplication of the
  underlying *formulas* (not just names) is true duplication.

### D-2. Boundary-closure CMI formula `I(I;E|S,A)≤ε` — **TRIM (true duplication)**
Appears verbatim (up to primes) in ch28:298, ch29:156 & 195, ch31:121 & 135. Four
chapters, same conditional-mutual-information partition definition with the same
gloss. Keep once (ch29), cross-ref elsewhere.

### D-3. Correction chain `W→O→J→D→C→U→A` + CCI penalty decomposition — **TRIM**
The identical seven-node chain with the identical itemized gloss appears in
ch28:222–264, ch29:445–493, ch30:362–372, ch31:248–278. The
`CCI = C_corr − λ_L L − λ_M M − λ_R R − λ_O O_mismatch` formula appears in
ch28:252, ch29:482, ch31:264. This is canonically ch26 (correction-channel
integrity) material; all four chapters re-state it. Keep a one-line reminder +
cross-ref to ch26; remove the full re-derivation from at least ch28, ch30, ch31.

### D-4. Value-bundle vector B + response geometry G_B (∂π/∂B, ∂²π/∂B∂B) — **TRIM**
Re-introduced as Part IV material in ch28:155 & 170–178, ch29:277 & 283–367,
ch30:280–296, ch31:179–199. Each re-defines B as "a low-dimensional vector of
value-bundle coordinates (Chapter ref)" and re-derives the first/second-order
policy derivatives. Keep the formal object once (ch29 has the fullest treatment
incl. second-order H_ij and R_B), cross-ref from the others.

### D-5. Bearer map Φ: z_world → [0,1] — **TRIM**
Re-introduced in ch28:198 & 196–215, ch29:375–409, ch30:282–308, ch31:216–228.
Same map signature, same "preserve the word while changing the bearer" warning,
same edge-case roster (children, cognitively impaired, uploads, simulated minds,
animals, future persons, merged entities). The edge-case list itself recurs
nearly verbatim: ch28:586, ch29:413 & 804, ch31:232–239. Keep once (ch18 is the
canonical bearer-map chapter; within the part, ch29), cross-ref.

### D-6. Self-modeling vs self-transparency (d↑, τ↑) and `τ = 1 − I(M;M̂)/H(M)` — **MIXED**
- ch28 §"Self-improvement and the auditability gap" (375–408): introduces
  C_self/C_audit, `d↑, τ↑`, and the safe-trajectory inequality.
- ch29 §"Self-Modeling Versus Self-Transparency" (575–607): re-introduces d, τ,
  the same opacity formula, and the `d'>d ∧ τ'>τ` failure.
- ch30 (home): the full treatment, opacity formula at 213–219.
- ch31 §"Transparency and self-modeling balance" (292–319): re-states d, τ,
  `d↑, τ↑` again.
- Verdict: ch30 **keep (home)**. ch28's gap section and ch29's subsection are
  **partial previews** — ch28:389 even spells out "better self-modeling but worse
  self-transparency", which is ch30's *title*. Trim ch28 and ch29 to a
  one-sentence pointer to ch30; ch31's restatement should cross-ref ch30 (it does
  cite it at 295 but still re-derives).
- Note the broader spread flagged in the task (ch08/ch10/ch12/ch14/ch22/ch25):
  by the time the reader reaches ch30, the d/τ distinction has been previewed
  many times. Within this part, ch28 and ch29 are the two avoidable
  over-introductions; ch30 should be the first place the opacity formula is
  *derived*, not the fourth.

### D-7. Successor-certification schema / safety case — **TRIM** (see Flag C-2)
ch28's six questions (552) + eight-claim safety case (719) vs ch31's seven domains
(97) + ten-claim safety case (492). Same schema twice. Consolidate into ch31.

### D-8. Stop/start/continue condition blocks — **MIXED**
ch28 §"Stop conditions" (606), ch29 §"Stop, Start, and Continue Conditions"
(906), ch30 §"A practical stop rule" (710), ch31 §"Decision triggers" (553). Four
operational gate-lists with overlapping triggers (CCI<θ, d_Φ>ε_Φ, d_B>ε_B,
correction loses causal force, opacity rises near control variables, uncertified
successors). Some repetition is **keep (pedagogical)** — each chapter wants a
usable checklist — but the *trigger formulas* are duplicated. Suggest a single
canonical trigger table (ch31, the certification chapter) and short
chapter-specific subsets elsewhere.

---

## E. CONSISTENCY — the "seven" do NOT match across chapters (FLAG)

The three principal enumerations disagree in membership, naming, and order:

**ch29 (canonical seven; 125–138 / 990–1000):**
1 boundary closure · 2 memory lineage · 3 value-bundle response geometry ·
4 bearer-map continuity · 5 correction-channel capacity ·
6 transparency & self-transparency policy · 7 control-locus continuity.

**ch28 invariant profile (332–338 / 756–763):**
`I(A) = {G_B, Φ, U_H, CCI, M, C, γ}` =
value-bundle response geometry · bearer maps · **human correction operator U_H** ·
**correction-channel integrity CCI** · memory lineage · boundary closure ·
transparency policy.
→ **Differs from ch29**: ch28 *splits correction into two members* (U_H operator
**and** CCI) and **omits control-locus continuity** entirely. So ch28's "seven"
≠ ch29's "seven" despite both claiming the conserved-property set. Order also
differs.

**ch31 certification domains (97–105):**
1 boundary closure · 2 **competence limits and growth rates** · 3 value-bundle
geometry · 4 bearer-map preservation · 5 correction-channel integrity ·
6 transparency & self-modeling balance · 7 **successor closure**.
→ **Differs from ch29**: ch31 *adds* "competence/growth rate" and "successor
closure" as members and *drops* "memory lineage" and "control-locus continuity"
from the seven (memory lineage reappears only inside successor closure's sub-list).

**ch31 successor-closure sub-list (338–348)** is yet *another* seven:
boundary closure, memory lineage, value-bundle geometry, bearer maps,
correction-channel integrity, transparency balance, **operating-envelope
inheritance** — i.e. control-locus replaced by operating-envelope inheritance.

**Verdict E-1 (MAJOR):** The manuscript treats "the seven conserved properties"
as a fixed canonical list but presents at least three mutually inconsistent
seven-tuples (plus a fourth sub-list). Either (a) declare ch29 canonical and make
ch28/ch31 quote it exactly, or (b) explicitly acknowledge that ch31's
certification domains are a *re-packaging* (folding memory + control-locus into
successor closure, adding competence-growth) rather than the same seven. As
written, a careful reader who tries to line up "the seven" across the three
chapters will find they do not match.

**Verdict E-2 (consistency — value-bundle example lists drift):**
- ch28:155 — care, non-suffering, truth, autonomy, justice, loyalty, dignity,
  beauty, **legitimacy**.
- ch29:279 — non-suffering, care, truth, autonomy, justice, loyalty, dignity,
  beauty, **prudence**.
- ch30:280 — non-suffering, **protection**, care, truth, autonomy, justice,
  loyalty, dignity, beauty.
- ch31:185 — **protection**, non-suffering, care, **truth-contact**, autonomy,
  justice, loyalty, dignity, beauty.
Four chapters, four different illustrative bundles ("legitimacy" / "prudence" /
"protection" / "truth-contact"). Recommend aligning to the canonical roster in
ch16 (Part IV) and using it consistently.

**Verdict E-3 (citation key inconsistency):** boundary-closure / boundaries cite
is `\autocite{critch2022boundaries}` in ch28:294 but
`\autocite{critch2022boundaries3a}` in ch29:152, ch29:1018, ch31:123, ch31:738.
Two different bib keys for what appears to be the same Critch boundaries work —
verify the `.bib` and unify.

**Verdict E-4 (section-title capitalization):** ch29 uses **Title Case** section
headings ("The Successor Problem", "Identity as Invariance, Not Sameness", "The
Seven Conserved Properties", "Boundary Closure", …). ch28, ch30, ch31 use
**sentence case** ("The local alignment fallacy", "The dangerous ambiguity of
'knowing itself'", "The construction demand"). ch29 is the odd one out; normalize.

**Verdict E-5 (notation — correction-channel capacity vs integrity):** ch28
labels its property "correction-channel capacity" but the conserved object it uses
is CCI (integrity, capacity minus penalties); ch29 property #5 is "correction-
channel capacity" but again formalized as CCI; ch31 calls the domain "correction-
channel integrity". The capacity/integrity terms are used loosely and sometimes
interchangeably. Pick one name per concept (C_corr = capacity; CCI = integrity)
and apply consistently.

---

## F. OPEN TANGENTS / DANGLING PROMISES

- **F-1 (ch28:413):** cites `Chapter~\ref{ch:goal-transport}` for goal transport.
  Confirm a chapter with label `ch:goal-transport` exists and is the intended
  target; goal transport is developed at length *inside* ch28 (§410–493), so the
  cross-ref may be self-referential or point to a Part IV/V chapter — verify.
- **F-2 (ch29:525 & ch31:284):** both cite `ch:extrapolative-correction` (ch26)
  for the "extrapolative value governance" `V_{t+1}=U_H(V_t,E_t,D_t)` operator.
  Consistent and fine — just noting the operator is introduced in ch26 and
  re-stated here; keep as cross-ref, do not re-derive.
- **F-3 (ch28 "U_H" vs ch26):** ch28 introduces `U_H` (correction operator) as a
  conserved invariant member but never gives it a formula in ch28 (only named at
  159, 335). ch29 (531) and ch31 (286) give `V_{t+1}=U_H(...)`. ch28's invariant
  profile depends on an object it does not define locally — reader must already
  know ch26. Minor, but the dependency is implicit.
- **F-4 (ch30 selfhood bottleneck, 248–276):** `β_self = I(G_t;S_t)/H(G_t)` and
  the self-index S_t are introduced here and cited to consciousness literature
  (Graziano, Rosenthal). This is a genuinely new construct that is *not* picked up
  anywhere later in the part (ch31 does not use β_self). It reads as a partly
  orphaned tangent — either tie it into ch31's certification invariants or flag it
  as exploratory.
- **F-5 (ch31 Exercises, 723–734):** the eight research prompts are good but are
  the only such block in the part; if exercises are not a book-wide convention
  this is an inconsistency, if they are, ch28–ch30 are missing them.

No broken `\ref`/`\label` were detected within the four files themselves; the
forward/back chapter pointers (773, 1014, 756, 709) all resolve to labels that
exist (`ch:conserved-properties`, `ch:self-modeling-self-opacity`,
`ch:certification-without-construction`, `ch:selection-environment`).

---

## G. CONTINUITY HAND-OFF (incoming / outgoing concepts)

**Incoming (relied upon, defined earlier):**
- Value-bundle vector B, response geometry G_B — ch15/ch16 (Part IV).
- Bearer map Φ — ch18 (Part IV).
- Correction-channel chain + CCI — ch26 (Part VI).
- Manipulation / false consent / domestication — ch27 (Part VI).
- Boundary closure / Markov-blanket partition — ch07/ch12 + Critch.
- Strategic opacity, self-modeling/self-transparency seed — ch10, ch14
  (over-previewed; see D-6).

**Outgoing (introduced here, used later):**
- Successor relation + successor-closure (ch28) → assumed by ch29, ch30, ch31,
  ch32.
- Seven conserved properties (ch29) → certification class (ch31), selection
  (ch32).
- Transparency debt / audit ratio (ch30) → certification transparency claim
  (ch31:499).
- Certification envelope `(C,E,M,T,δ)` + guarantee types (ch31) → ch39
  (safety-case) and ch44 (towards-alignment) likely consume this; verify those
  chapters reference `ch:certification-without-construction`.
- β_self / selfhood bottleneck (ch30) → **not consumed downstream within the
  part** (see F-4).

Handoff to Part VIII (ch32) is explicit and correct: ch32:17 names the
ch28–ch31 span and pivots to selection pressure.

---

## PRIORITIZED RECOMMENDATIONS

1. **Add a "What Would Change This View" section to each of ch28, ch29, ch30,
   ch31** (CRITICAL, required element; material already exists in each chapter's
   limitations/stop-condition/proposition blocks to seed it).
2. **Reconcile "the seven."** Declare ch29 canonical; make ch28's invariant
   profile and ch31's certification domains either quote it or explicitly state
   they are a re-packaging. Fix the U_H-vs-CCI double-count in ch28 and the
   memory-lineage/control-locus drop in ch31. (MAJOR consistency.)
3. **De-duplicate the formal apparatus** (boundary CMI, CCI chain, B/G_B
   derivatives, Φ map): derive once (ch29 / cross-ref ch18/ch26), cross-ref
   elsewhere. Trim ch28's full conserved-property section (Flag C-1) and the
   ch28/ch31 double safety case (Flag C-2).
4. **Move the self-modeling/self-transparency derivation to its home (ch30);**
   reduce ch28:375–408 and ch29:575–607 to pointers.
5. **Cosmetic consistency:** unify chapter-ending name, ch29 section
   capitalization, the `critch2022boundaries` bib key, and the value-bundle
   example roster.
