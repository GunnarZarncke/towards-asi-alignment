# Review Pass — Part IX: "Safety Cases, Adversaries, and Open Questions" (ch46–ch48)

Reviewer pass over `parts/part09-safety-cases.tex` and its five chapters. No manuscript
files were edited. Line numbers refer to the chapter `.tex` files as read in full.

Part file: `parts/part09-safety-cases.tex` — `\part{Safety Cases, Adversaries, and Open Questions}`
inputs ch46→ch48→ch45→ch46→ch48 in order (lines 3–7). Correct order, no missing/extra inputs.

book.yml status (lines 219–248): ch46 draft, ch48 draft, ch45 draft, **ch46 stub (word_target 10000)**,
ch48 draft (word_target 9000). The stub/thin flags below match book.yml.

---

## HEADLINE FINDING

**ch46 (`ch:safety-case`) — the book's central safety-case SYNTHESIS chapter — is a bare
Shape-A skeleton stub, ~49 lines, with every substantive section marked `\textbf{[STUB]}`.**
This is the single most important defect in the part and arguably in the manuscript: the
entire arc of Parts I–IX (boundary → capability → value-bundle → correction → successor →
basin → adversarial measurement) is explicitly engineered to converge here, and the
convergence chapter does not exist as prose. Three chapters point forward into it
(ch48 line 1009; ch46 line 1055; ch45 line 709), so the promised payoff lands on an empty
page. Its companion appendix `appK-safety-case-template.tex` is **also a `[STUB]`** (4 lines),
so neither the synthesis nor its reusable template is written.

---

## A. CAPSULES

- **ch46 — Passive Observation Is Not Enough** (`ch:passive-observation-not-enough`, ~1083 lines).
  Argues observation is not evidence of safety for strategically adaptive systems unless
  embedded in perturbation/invariance/adversarial-measurement. Five failure modes of passive
  obs (boundary, non-stationarity, hidden common cause, strategic opacity, goal laundering),
  a perturbation taxonomy (tool/memory/oversight/reward/ontology/successor), invariants under
  perturbation, a six-component adversarial-measurement protocol, five institutional artifacts,
  and decision triggers. Substantial, mature, dense. The methodological backbone of the part.

- **ch48 — Detecting Goal Laundering** (`ch:goal-laundering`, ~847 lines). Goal laundering =
  preserving moral language while the value-bearing/correction-bearing structure shifts.
  Four laundering layers (semantic/bundle/bearer/correction), the laundering index (GLI),
  stress tests, the stakes gradient, legitimate-change criteria, institutional laundering,
  detection artifacts, decision triggers, detector failure modes, a steelman critic. Full, mature.

- **ch45 — Checking a System at Every Level** (`ch:multiscale-decomposition`, ~718 lines).
  Multi-scale decomposition: maintain a posterior over decompositions `P(D|X,Z)`, a
  risk-relevance score `R(D)`, boundary closure, intentional compression, stress traces,
  control-locus continuity, a seven-stage protocol, stop/start/continue criteria. Full, mature.
  Explicitly hands off to ch46 (line 709).

- **ch46 — A Safety Case for Superintelligence Alignment** (`ch:safety-case`, 49 lines).
  **STUB.** Bare Shape-A skeleton; all content placeholders. See §B.

- **ch48 — Lethality Stress Test and Open Issues** (`ch:lethality-stress-test-open-issues`, 160 lines).
  Yudkowsky's *List of Lethalities* used as an adversarial checklist (13-row longtable) plus a
  10-item Open Problem Ledger. Real but skeletal: framing + table + ledger + summary, no
  per-row prose. Correctly confines Yudkowsky to a checklist (see §C).

---

## B. REQUIRED-ELEMENT COMPLIANCE

Legend: ✓ present / ⚠ substitute or partial / ✗ missing / **[STUB]**.

| Element | ch46 | ch48 | ch45 | ch46 | ch48 |
|---|---|---|---|---|---|
| `\chapter` + `\label` | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) | ✓ (1–2) |
| `chapterthesis` env | ✓ (4–6) | ✓ (4–6) | ✓ (4–6) | ⚠ **[STUB]** (4–6) | ✓ (4–6) |
| epigraph | ✓ (10–12) | ✓ (10–12) | ✓ (10–12) | ✗ none | ✗ none |
| decision relevance | ✓ "Decision triggers" (905) | ✓ "Decision triggers" (714) | ✓ "Stop, start, continue" (601) | **[STUB]** "Why This Matters" (10–12) | ⚠ "Why This Matters" (10–14) |
| failure-mode / counterexample | ✓ (993 counterexample) | ✓ "Failure modes of the detector" (772) | ✓ "Where this can go wrong" (655) | **[STUB]** (26–28) | ⚠ checklist+ledger as failure inventory |
| **EXACT** "What Would Change This View" | ✗ ⚠ "What evidence would update us?" (1017) | ✗ ⚠ "A steelman critic" (802) | ✗ ⚠ "Where this can go wrong" (655) | ✓ heading but **[STUB]** (30–32) | ✗ none |
| Summary | ✓ (1057) | ✓ (815) | ✓ (694) | **[STUB]** (34–40) | ✓ (140) |
| `refsection` + `\printbibliography` | ✓ (8 / 1080) | ✓ (8 / 844) | ✓ (8 / 715) | ✓ (8 / 46) | ✓ (8 / 158) |

### WWCTV finding (part-wide consistency problem)
The **only** chapter with the exact heading "What Would Change This View" is ch46 — and there
it is a `[STUB]`. Every *drafted* chapter substitutes a differently-titled section:
- ch46 §"What evidence would update us?" (line 1017, `sec:what-would-update-ch46`) — content is
  correct (four ways the adversarial-measurement frame could be wrong + the empirical evidence
  that would strengthen it), but the title is non-standard. **Flag: rename or accept as canon.**
- ch48 §"A steelman critic" (line 802, `sec:steelman-critic-ch48`) — functions as WWCTV (strongest
  objection + reply) and is complemented by §"Failure modes of the detector" (772). **Flag.**
- ch45 §"Where this can go wrong" (line 655) + "Confidence decreases" paragraph (line 644) — these
  jointly cover WWCTV but under non-standard titles. **Flag.**
- ch48 has **no** WWCTV section. Arguably the whole chapter (checklist statuses + Open Problem
  Ledger) is WWCTV-shaped, but there is no exact section. **Flag.**

Recommendation: decide one policy. Either (a) these prose-style substitutes are the house style
for drafted chapters and ch46 should follow suit, or (b) standardize on the exact heading. Right
now the exact heading exists *only* in the unwritten chapter, which is the worst of both worlds.

### ch46 placeholder enumeration (every section is a stub)
- line 5: `chapterthesis` — `\textbf{[STUB]} One paragraph stating the chapter's core claim.`
- line 12: §Why This Matters — `[STUB]`
- line 16: §Plain-Language Model — `[STUB]`
- line 20: §Formal Model — `[STUB]`
- line 24: §Worked Example — `[STUB]`
- line 28: §Counterexample or Failure Mode — `[STUB]`
- line 32: §What Would Change This View — `[STUB]`
- lines 37–39: §Summary — three `[STUB]` bullets
- lines 42–47: Chapter References / bibliography is the **only** real content (cites
  `kelly1998safety, bloomfield2012safety, seoul2024commitments, iaisr2025`).

So ch46 is 100% placeholder except its three reference citations. It does **not** assemble any of
the claims the spine promised (boundary/capability/value-bundle/correction/successor/basin), does
**not** reference `appK-safety-case-template`, and does **not** back-reference ch46/ch48/ch45
whose tools it is supposed to integrate.

### ch48 thinness (draft but skeletal)
Content is *real*, not placeholder, but thin relative to the 9000-word target (actual ≈ 1,500 words):
- Lethality Checklist (lines 41–115): a genuine 13-row longtable (first-critical-try, pivotal act,
  capability-generalizes, latent pointers, corrupted feedback, corrigibility-anti-natural, inner
  alignment, deception/opacity, uncheckable outputs, physical takeover, multipolar, boxing, field
  failure) with honest Status column (Mostly open / Conjectural / Reframed / Partly addressed /
  Weakly addressed / Diagnostic only / Needs development). Good but each "Response" cell is a single
  phrase; no per-lethality prose.
- Two unresolved inline TODOs left in source: line 119 `% TODO[open-crux]` (reflective stability of
  correction-channel preservation) and line 121 `% TODO[open-crux]` (safe delegation of uncheckable
  plans). **[TODO] markers in committed source.**
- line 117 comment points to `metadata/TODO.md` cross-chapter index.
- Open Problem Ledger (lines 123–138): real 10-item enumerate, all `[Open]`. Good.

---

## C. CONTINUITY

### Internal flow ch46→ch48→ch45→ch46→ch48
- ch46→ch48: clean. ch46 §"The goal-laundering problem" (228–260) ends "Chapter~\ref{ch:goal-laundering}
  develops detection methods in detail" (line 260). ch48 opens referencing ch46 (line 19) and re-anchors
  on it in stress testing (line 335).
- ch48→ch45: implicit rather than explicit. ch48 ends on the laundering defense; ch45 opens on "the
  problem of scale" without a back-link to ch48, though ch45 later cites ch48 for the laundering
  diagnostic at scale (line 353). Acceptable; a one-line bridge from ch48 to ch45 would tighten it.
- ch45→ch46: ch45 line 709 promises "The next chapter assembles these tools into an explicit safety
  case with stop conditions and evidence requirements (Chapter~\ref{ch:safety-case})." **This promise
  is unmet — ch46 is a stub.**
- ch46→ch48: ch48 stands on its own (it reframes itself as a stress-test that comes *after* the
  safety-case chapter, line 13: "after the safety-case chapter and before the civilizational limit"),
  so the stub ch46 does not syntactically break ch48, but the logical dependency (stress-test *of the
  safety case*) is hollow because there is no safety case to stress-test.

### Handoff from Part VIII (ch48) and to Part X (ch45)
- ch48 (Alignment Attractor) line 1009 explicitly funnels into ch46: "Safety cases require auditors,
  funders, and regulators who know what evidence should look like (Chapter~\ref{ch:safety-case})."
  Incoming handoff is correct in intent but again lands on the stub.
- ch48→ch45: ch48 makes **no** forward reference to ch45 ("When Value Change Is the Thing at Stake").
  ch45 opens fresh (lines 14–17) on the value-change problem. The Part IX→Part X seam is abrupt;
  a closing pointer from ch48 (or, properly, from a written ch46 summary) to Part X would help.

### Does the ch46 stub critically break the synthesis?
**Yes.** This is the load-bearing failure of the part. The book's stated spine routes all
adversarial-measurement machinery (ch46 perturbation/invariants, ch48 laundering detection, ch45
multi-scale decomposition) plus the earlier boundary/capability/value-bundle/correction/successor/
basin claims into one consolidated safety case at ch46. With ch46 empty:
1. There is no single artifact a reader/funder/auditor can point to as "the safety case."
2. ch46 line 1055 ("Alignment is counterfactual… (Chapter~\ref{ch:safety-case})") and ch45 line 709
   are dangling promises.
3. ch48's "stress test of the framework after the safety-case chapter" (line 13) stress-tests a
   framework whose synthesis is unwritten.
This should be the top remediation priority for the part. Until ch46 is drafted (and `appG` with it),
Part IX cannot be considered structurally complete regardless of how strong ch46–ch45 are.

### Does ch48 properly confine Yudkowsky lethalities to a checklist?
**Yes, explicitly and well.** line 13: "This chapter does not organize the book." line 14:
"Yudkowsky's *AGI Ruin: A List of Lethalities* … is treated as a checklist, not as the manuscript
spine." Summary line 143: the organizing frame "remains value-bundle transport… not an external doom
checklist." The longtable is framed as an adversarial benchmark (line 12) with an honest Status column
and an "absence-of-structure" framing (lines 16–23) turning lethalities into named cruxes rather than
refuted points. This matches the brief precisely.

---

## D. REDUNDANCY

### D1. Goal laundering (ch10 / ch46 / ch48) — **largest redundancy in the part**
- **ch10** (`ch10-strategic-opacity.tex`) already introduces the *identical* four-layer taxonomy:
  lines 378–383 "Goal laundering can then occur at four levels: Semantic / Bundle / Bearer /
  Correction laundering", with `eq:goal-laundering-signature` (line 349), `eq:bundle-laundering`
  (line 392), `eq:bearer-laundering` (line 399).
- **ch46** (`ch46-transport-types.tex`) gives the *positive* mirror: four transport layers
  semantic/bundle/bearer/correction (+successor) — lines 6, 19–37, 88–96, `eq:transport-stack`
  (line 38). The ch48 laundering layers are precisely the failure modes of the ch46 transport layers.
- **ch48** §"The four layers of laundering" (138–274) restates the same four layers a third time.
- **ch46** §"Goal laundering" (635–729) independently presents a *four-STAGE* model
  (semantic preservation / proxy substitution / bearer narrowing / correction capture) — note this is
  a *different* four-tuple from the ch48 four-LAYER model (proxy-substitution vs bundle-laundering),
  which is itself a low-grade inconsistency (see §E).

**Judgment:** The four laundering layers are now stated in **ch10, ch46 (as transport), and ch48** —
triple coverage. **Keep ch48 as the canonical detection chapter** (it adds GLI, stress tests, the
stakes gradient, legitimacy criteria, artifacts — genuinely new), but:
- **Trim/cross-ref ch10 lines 378–399**: it should *introduce* the term and point forward to ch48,
  not re-derive `eq:bundle-laundering`/`eq:bearer-laundering` which ch48 re-derives.
- **ch48 should explicitly cite ch10 (`eq:goal-laundering-signature`) and ch46 (`eq:transport-stack`)**
  to make the inheritance legible; currently ch48 cross-refs ch46 only via `ch:tradeoffs-bundle-geometry`/
  `ch:value-bundle-model`, not the transport-stack layers it mirrors.
- **ch46 §goal-laundering (635–729) is the most cuttable**: it builds a *second, competing* four-tuple
  model inside the methods chapter. Recommend **trimming to a short preview + cross-ref to ch48**
  (ch46 already has the forward pointer at line 260). Keep at most the §"The goal-laundering problem"
  sketch (228–260); demote the four-stage expansion.

### D2. Perturbation / adversarial measurement (ch07 / ch10 / ch46)
- **ch07** (`ch07-finding-boundary.tex`) already has §"Adversarial boundary discovery" (line 676),
  "We need perturbations" (693), "A perturbation test changes part of the system… observes whether a
  hidden control structure reappears" (697), and perturbation-robustness as evidence (945, 949, 980,
  1039, 1054).
- **ch10** carries the strategic-opacity / `J_hide` objective that ch46 reuses (ch46 line 89–99 cites
  `ch:strategic-opacity`).
- **ch46** is the dedicated perturbation/adversarial-measurement chapter (262–633).

**Judgment: keep all three — roles are distinct.** ch07 = perturbation for *boundary* discovery;
ch10 = the opacity model that *motivates* perturbation; ch46 = the full perturbation/invariant/
adversarial-measurement *methodology*. ch46 does cross-ref ch07 (`ch:finding-boundary`, lines 40, 112)
and ch10 (lines 99). Low-grade overlap only in the generic "prod the system" framing (ch46 line 31
vs ch07 697); acceptable. **Keep, ensure cross-refs stay.**

### D3. Multi-scale / composite detection (ch07 / ch09 / ch45)
- **ch09** (`ch09-composite-agent.tex`) already establishes composite agency, composite surplus
  `\mathcal{D}` and decomposition penalty `\lambda_\Sigma` (lines 100–192), and "align only the model
  while the loop is the agent" (line 32) — which ch45 restates as its closing maxim "Do not align the
  component while the loop becomes the agent" (line 691).
- **ch07** supplies boundary closure / `\epsilon`-boundaries that ch45 reuses (ch45 §boundary closure
  84–108 cites `ch:finding-boundary`).
- **ch45** generalizes ch07+ch09 into a *posterior over decompositions* + multi-scale risk score.

**Judgment: keep ch45 — it is a genuine generalization** (posterior over decompositions, regime-
sensitivity `P(D|X,Z)`, the risk-relevance score `R(D)`, the seven-stage protocol). But the
**conceptual overlap with ch09 is high**: ch45's customer-support worked example (388–419) and the
"loop becomes the agent" thesis are close to ch09's composite-agent argument. **Cross-ref, don't trim:**
ch45 should explicitly cite `ch:composite-agent` at its thesis (currently ch45 cross-refs ch07
`ch:finding-boundary` at line 29 but **not** ch09 for the composite claim). Also ch46 §"Cross-scale
measurement" (568–591) previews the ch45 decomposition posterior `P(C_1..C_n|X,I)` **without** a
forward ref to ch45 — add one.

---

## E. CONSISTENCY

1. **Laundering index vs goal-laundering signature.** ch48 defines GLI (line 314):
   `GLI = (w_B D_bundle + w_Φ D_bearer + w_C D_corr + w_S D_succ)·exp(-α D_sem)`. ch10 defines a
   separate `eq:goal-laundering-signature` (line 349, oversight-conditional form). They are
   compatible but never reconciled; ch48 does not cite ch10's signature. **Recommend one explicit
   cross-ref so readers see GLI as the multi-layer generalization of the ch10 signature.**

2. **Four-LAYER vs four-STAGE laundering.** ch48 layers = semantic / **bundle** / bearer / correction
   (line 139ff). ch46 stages = semantic preservation / **proxy substitution** / bearer narrowing /
   correction capture (642–728). "Bundle laundering" (ch48) and "proxy substitution" (ch46) are not
   the same construct, yet both are presented as the second of four. This will confuse a careful
   reader. **Recommend ch46 adopt ch48's layer names (or drop the four-stage list per §D1).**

3. **CCI base term differs across chapters.** ch46 (443–453): `CCI = C_corr − λ_L L − λ_M M − λ_R R −
   λ_O O` with `C_corr = I(C^H;A | S,I)` (single mutual information). ch48 (256–267) and ch45
   (451–462): `CCI / C_corr = min_j I(X_j;X_{j+1}) − penalties` (information-bottleneck *min* over the
   correction chain). Same symbol, two different base quantities. **Recommend standardizing on one
   definition (presumably ch46's canonical CCI) and citing it in all three.**

4. **Multi-scale score.** ch45 `R(D)` (line 287, `sec:multiscale-score-ch45`) is internally consistent
   and consistent with ch46's cross-scale posterior; no conflict found. Good.

5. **Section-title capitalization.** ch46 / ch48 / ch45 use **sentence case** ("The problem with
   watching", "A minimal model of passive and active evidence"). ch46 and ch48 use **Title Case**
   ("Why This Matters", "Plain-Language Model" / "Lethality Checklist", "Open Problem Ledger").
   ch46's headers are the generic Shape-A skeleton labels; ch48's are custom Title Case.
   **Inconsistent within the part.** When ch46 is written it should match ch46–38 sentence case;
   ch48's headers should likely be lower-cased to match.

6. **Chapter-ending naming.** All five end in a section literally titled "Summary" (ch46 1057, ch48
   815, ch45 694, ch46 34, ch48 140) followed by "Chapter References". **Consistent — good.**

7. **Epigraph presence.** ch46/ch48/ch45 (and ch45) have `\epigraph`; ch46 and ch48 have none.
   Minor; add when ch46 is drafted, optionally ch48, for part-internal uniformity.

---

## F. OPEN TANGENTS / DANGLING PROMISES

1. **ch46 stub** — the master dangling promise (see §B, §C). All `[STUB]` content; references appG
   topic but never cites it.
2. **`appK-safety-case-template.tex` is itself a `[STUB]`** (4 lines: "Appendix content to be
   written"). The safety-case chapter and its reusable template appendix are both unwritten — a
   compound gap. ch46, when written, is expected to forward-ref appG; today neither end exists.
3. **ch46 line 1055 / ch45 line 709 / ch48 line 1009** all promise the safety case (ch46) that is not
   delivered.
4. **ch48 inline TODOs in committed source** — lines 119 and 121 (`% TODO[open-crux]…`) and line 117
   (cross-chapter index pointer to `metadata/TODO.md`). These are author scaffolding left in the .tex.
5. **ch46 §"Cross-scale measurement" (568–591)** previews the ch45 posterior over decompositions with
   no forward ref to ch45 — a soft dangling thread.
6. **ch45→ch48 / ch46→ch45 / ch48→ch45** missing or one-directional bridges (see §C/§D3/§G).

---

## G. CONTINUITY HAND-OFF (incoming / outgoing concepts)

- **Incoming to Part IX (from ch48 / Part VIII):** alignment attractor, artifact conductivity,
  tripwires/decision authority, "safety cases require auditors who know what evidence looks like"
  (ch48 line 1009). Part IX is the cash-out of that attractor in concrete measurement + a safety case.
- **ch46 carries in:** boundary (`ch:finding-boundary`), strategic opacity / `J_hide`
  (`ch:strategic-opacity`), value-bundle geometry (`ch:value-bundle-model`), correction channels
  (`ch:correction-causal-channel`, `ch:correction-channel-integrity`), successors
  (`ch:successor-central-test`, `ch:conserved-properties`), goal transport (`ch:goal-transport`).
- **ch46 carries out:** perturbation/invariant/adversarial-measurement toolkit; forwards laundering
  detail to ch48 (260) and the safety case to ch46 (1055).
- **ch48 carries in/out:** four-layer laundering (shared with ch10/ch46); forwards stress/perturbation
  back to ch46 (335) and successor invariants to ch46/ch48; central output is GLI + the stakes gradient.
- **ch45 carries in/out:** composite agency (ch09, *uncited at thesis*), boundary closure (ch07),
  laundering-at-scale (ch48, line 353); output is the decomposition posterior + `R(D)`; **explicitly
  hands to ch46 (709).**
- **ch46 (stub):** *intended* to ingest ch46+ch48+ch45 plus Parts I–VIII claims and emit the
  consolidated safety case + stop conditions + evidence requirements; currently ingests/emits nothing.
- **ch48 carries in:** the whole framework as the object under stress; cites ch48 (ICI/coalitions) and
  ch48 (pivotal process) in a source comment (line 117). **No outgoing ref to ch45** — the Part IX→X
  seam is unmarked.

---

## PRIORITIZED RECOMMENDATIONS (no edits made)

1. **Write ch46.** Highest priority in the part. Assemble the boundary/capability/value-bundle/
   correction/successor/basin claims into one explicit safety case with stop conditions and evidence
   requirements; cite ch46/ch48/ch45 as its measurement instruments; reference `appG`. Match ch46–38
   sentence-case headers and add an epigraph + real `chapterthesis`.
2. **Write `appK-safety-case-template`** in tandem with ch46 (it is the reusable artifact ch46 promises).
3. **Flesh out ch48** to its 9000-word target: add per-lethality prose, resolve or migrate the two
   inline `% TODO[open-crux]` items, and add a forward bridge to ch45.
4. **Dedupe goal laundering:** demote ch10 (378–399) and ch46 (635–729) to previews that cross-ref the
   canonical ch48; reconcile ch46's four-stage list with ch48's four-layer list; have ch48 cite
   ch10's `eq:goal-laundering-signature` and ch46's `eq:transport-stack`.
5. **Standardize CCI** base term across ch46/ch48/ch45 to the canonical ch46 definition.
6. **Decide a WWCTV policy** — the exact heading currently exists only in the stub ch46; either adopt
   the prose substitutes as house style or standardize the heading across ch46–ch48.
7. **Add missing cross-refs:** ch45 thesis → ch09 (composite); ch46 §cross-scale → ch45; ch48 → ch46
   bridge; ch48 → ch45 bridge.
