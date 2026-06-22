# Review Pass — Part IX: "Safety Cases, Adversaries, and Open Questions" (ch36–ch40)

Reviewer pass over `parts/part09-safety-cases.tex` and its five chapters. No manuscript
files were edited. Line numbers refer to the chapter `.tex` files as read in full.

Part file: `parts/part09-safety-cases.tex` — `\part{Safety Cases, Adversaries, and Open Questions}`
inputs ch36→ch37→ch38→ch39→ch40 in order (lines 3–7). Correct order, no missing/extra inputs.

book.yml status (lines 219–248): ch36 draft, ch37 draft, ch38 draft, **ch39 stub (word_target 10000)**,
ch40 draft (word_target 9000). The stub/thin flags below match book.yml.

---

## HEADLINE FINDING

**ch39 (`ch:safety-case`) — the book's central safety-case SYNTHESIS chapter — is a bare
Shape-A skeleton stub, ~49 lines, with every substantive section marked `\textbf{[STUB]}`.**
This is the single most important defect in the part and arguably in the manuscript: the
entire arc of Parts I–IX (boundary → capability → value-bundle → correction → successor →
basin → adversarial measurement) is explicitly engineered to converge here, and the
convergence chapter does not exist as prose. Three chapters point forward into it
(ch35 line 1009; ch36 line 1055; ch38 line 709), so the promised payoff lands on an empty
page. Its companion appendix `appG-safety-case-template.tex` is **also a `[STUB]`** (4 lines),
so neither the synthesis nor its reusable template is written.

---

## A. CAPSULES

- **ch36 — Passive Observation Is Not Enough** (`ch:passive-observation-not-enough`, ~1083 lines).
  Argues observation is not evidence of safety for strategically adaptive systems unless
  embedded in perturbation/invariance/adversarial-measurement. Five failure modes of passive
  obs (boundary, non-stationarity, hidden common cause, strategic opacity, goal laundering),
  a perturbation taxonomy (tool/memory/oversight/reward/ontology/successor), invariants under
  perturbation, a six-component adversarial-measurement protocol, five institutional artifacts,
  and decision triggers. Substantial, mature, dense. The methodological backbone of the part.

- **ch37 — Detecting Goal Laundering** (`ch:goal-laundering`, ~847 lines). Goal laundering =
  preserving moral language while the value-bearing/correction-bearing structure shifts.
  Four laundering layers (semantic/bundle/bearer/correction), the laundering index (GLI),
  stress tests, the stakes gradient, legitimate-change criteria, institutional laundering,
  detection artifacts, decision triggers, detector failure modes, a steelman critic. Full, mature.

- **ch38 — Checking a System at Every Level** (`ch:multiscale-decomposition`, ~718 lines).
  Multi-scale decomposition: maintain a posterior over decompositions `P(D|X,Z)`, a
  risk-relevance score `R(D)`, boundary closure, intentional compression, stress traces,
  control-locus continuity, a seven-stage protocol, stop/start/continue criteria. Full, mature.
  Explicitly hands off to ch39 (line 709).

- **ch39 — A Safety Case for Superintelligence Alignment** (`ch:safety-case`, 49 lines).
  **STUB.** Bare Shape-A skeleton; all content placeholders. See §B.

- **ch40 — Lethality Stress Test and Open Issues** (`ch:lethality-stress-test-open-issues`, 160 lines).
  Yudkowsky's *List of Lethalities* used as an adversarial checklist (13-row longtable) plus a
  10-item Open Problem Ledger. Real but skeletal: framing + table + ledger + summary, no
  per-row prose. Correctly confines Yudkowsky to a checklist (see §C).

---

## B. REQUIRED-ELEMENT COMPLIANCE

Legend: ✓ present / ⚠ substitute or partial / ✗ missing / **[STUB]**.

| Element | ch36 | ch37 | ch38 | ch39 | ch40 |
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
The **only** chapter with the exact heading "What Would Change This View" is ch39 — and there
it is a `[STUB]`. Every *drafted* chapter substitutes a differently-titled section:
- ch36 §"What evidence would update us?" (line 1017, `sec:what-would-update-ch36`) — content is
  correct (four ways the adversarial-measurement frame could be wrong + the empirical evidence
  that would strengthen it), but the title is non-standard. **Flag: rename or accept as canon.**
- ch37 §"A steelman critic" (line 802, `sec:steelman-critic-ch37`) — functions as WWCTV (strongest
  objection + reply) and is complemented by §"Failure modes of the detector" (772). **Flag.**
- ch38 §"Where this can go wrong" (line 655) + "Confidence decreases" paragraph (line 644) — these
  jointly cover WWCTV but under non-standard titles. **Flag.**
- ch40 has **no** WWCTV section. Arguably the whole chapter (checklist statuses + Open Problem
  Ledger) is WWCTV-shaped, but there is no exact section. **Flag.**

Recommendation: decide one policy. Either (a) these prose-style substitutes are the house style
for drafted chapters and ch39 should follow suit, or (b) standardize on the exact heading. Right
now the exact heading exists *only* in the unwritten chapter, which is the worst of both worlds.

### ch39 placeholder enumeration (every section is a stub)
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

So ch39 is 100% placeholder except its three reference citations. It does **not** assemble any of
the claims the spine promised (boundary/capability/value-bundle/correction/successor/basin), does
**not** reference `appG-safety-case-template`, and does **not** back-reference ch36/ch37/ch38
whose tools it is supposed to integrate.

### ch40 thinness (draft but skeletal)
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

### Internal flow ch36→ch37→ch38→ch39→ch40
- ch36→ch37: clean. ch36 §"The goal-laundering problem" (228–260) ends "Chapter~\ref{ch:goal-laundering}
  develops detection methods in detail" (line 260). ch37 opens referencing ch36 (line 19) and re-anchors
  on it in stress testing (line 335).
- ch37→ch38: implicit rather than explicit. ch37 ends on the laundering defense; ch38 opens on "the
  problem of scale" without a back-link to ch37, though ch38 later cites ch37 for the laundering
  diagnostic at scale (line 353). Acceptable; a one-line bridge from ch37 to ch38 would tighten it.
- ch38→ch39: ch38 line 709 promises "The next chapter assembles these tools into an explicit safety
  case with stop conditions and evidence requirements (Chapter~\ref{ch:safety-case})." **This promise
  is unmet — ch39 is a stub.**
- ch39→ch40: ch40 stands on its own (it reframes itself as a stress-test that comes *after* the
  safety-case chapter, line 13: "after the safety-case chapter and before the civilizational limit"),
  so the stub ch39 does not syntactically break ch40, but the logical dependency (stress-test *of the
  safety case*) is hollow because there is no safety case to stress-test.

### Handoff from Part VIII (ch35) and to Part X (ch41)
- ch35 (Alignment Attractor) line 1009 explicitly funnels into ch39: "Safety cases require auditors,
  funders, and regulators who know what evidence should look like (Chapter~\ref{ch:safety-case})."
  Incoming handoff is correct in intent but again lands on the stub.
- ch40→ch41: ch40 makes **no** forward reference to ch41 ("When Value Change Is the Thing at Stake").
  ch41 opens fresh (lines 14–17) on the value-change problem. The Part IX→Part X seam is abrupt;
  a closing pointer from ch40 (or, properly, from a written ch39 summary) to Part X would help.

### Does the ch39 stub critically break the synthesis?
**Yes.** This is the load-bearing failure of the part. The book's stated spine routes all
adversarial-measurement machinery (ch36 perturbation/invariants, ch37 laundering detection, ch38
multi-scale decomposition) plus the earlier boundary/capability/value-bundle/correction/successor/
basin claims into one consolidated safety case at ch39. With ch39 empty:
1. There is no single artifact a reader/funder/auditor can point to as "the safety case."
2. ch36 line 1055 ("Alignment is counterfactual… (Chapter~\ref{ch:safety-case})") and ch38 line 709
   are dangling promises.
3. ch40's "stress test of the framework after the safety-case chapter" (line 13) stress-tests a
   framework whose synthesis is unwritten.
This should be the top remediation priority for the part. Until ch39 is drafted (and `appG` with it),
Part IX cannot be considered structurally complete regardless of how strong ch36–ch38 are.

### Does ch40 properly confine Yudkowsky lethalities to a checklist?
**Yes, explicitly and well.** line 13: "This chapter does not organize the book." line 14:
"Yudkowsky's *AGI Ruin: A List of Lethalities* … is treated as a checklist, not as the manuscript
spine." Summary line 143: the organizing frame "remains value-bundle transport… not an external doom
checklist." The longtable is framed as an adversarial benchmark (line 12) with an honest Status column
and an "absence-of-structure" framing (lines 16–23) turning lethalities into named cruxes rather than
refuted points. This matches the brief precisely.

---

## D. REDUNDANCY

### D1. Goal laundering (ch10 / ch23 / ch37) — **largest redundancy in the part**
- **ch10** (`ch10-strategic-opacity.tex`) already introduces the *identical* four-layer taxonomy:
  lines 378–383 "Goal laundering can then occur at four levels: Semantic / Bundle / Bearer /
  Correction laundering", with `eq:goal-laundering-signature` (line 349), `eq:bundle-laundering`
  (line 392), `eq:bearer-laundering` (line 399).
- **ch23** (`ch23-transport-types.tex`) gives the *positive* mirror: four transport layers
  semantic/bundle/bearer/correction (+successor) — lines 6, 19–37, 88–96, `eq:transport-stack`
  (line 38). The ch37 laundering layers are precisely the failure modes of the ch23 transport layers.
- **ch37** §"The four layers of laundering" (138–274) restates the same four layers a third time.
- **ch36** §"Goal laundering" (635–729) independently presents a *four-STAGE* model
  (semantic preservation / proxy substitution / bearer narrowing / correction capture) — note this is
  a *different* four-tuple from the ch37 four-LAYER model (proxy-substitution vs bundle-laundering),
  which is itself a low-grade inconsistency (see §E).

**Judgment:** The four laundering layers are now stated in **ch10, ch23 (as transport), and ch37** —
triple coverage. **Keep ch37 as the canonical detection chapter** (it adds GLI, stress tests, the
stakes gradient, legitimacy criteria, artifacts — genuinely new), but:
- **Trim/cross-ref ch10 lines 378–399**: it should *introduce* the term and point forward to ch37,
  not re-derive `eq:bundle-laundering`/`eq:bearer-laundering` which ch37 re-derives.
- **ch37 should explicitly cite ch10 (`eq:goal-laundering-signature`) and ch23 (`eq:transport-stack`)**
  to make the inheritance legible; currently ch37 cross-refs ch23 only via `ch:tradeoffs-bundle-geometry`/
  `ch:value-bundle-model`, not the transport-stack layers it mirrors.
- **ch36 §goal-laundering (635–729) is the most cuttable**: it builds a *second, competing* four-tuple
  model inside the methods chapter. Recommend **trimming to a short preview + cross-ref to ch37**
  (ch36 already has the forward pointer at line 260). Keep at most the §"The goal-laundering problem"
  sketch (228–260); demote the four-stage expansion.

### D2. Perturbation / adversarial measurement (ch07 / ch10 / ch36)
- **ch07** (`ch07-finding-boundary.tex`) already has §"Adversarial boundary discovery" (line 676),
  "We need perturbations" (693), "A perturbation test changes part of the system… observes whether a
  hidden control structure reappears" (697), and perturbation-robustness as evidence (945, 949, 980,
  1039, 1054).
- **ch10** carries the strategic-opacity / `J_hide` objective that ch36 reuses (ch36 line 89–99 cites
  `ch:strategic-opacity`).
- **ch36** is the dedicated perturbation/adversarial-measurement chapter (262–633).

**Judgment: keep all three — roles are distinct.** ch07 = perturbation for *boundary* discovery;
ch10 = the opacity model that *motivates* perturbation; ch36 = the full perturbation/invariant/
adversarial-measurement *methodology*. ch36 does cross-ref ch07 (`ch:finding-boundary`, lines 40, 112)
and ch10 (lines 99). Low-grade overlap only in the generic "prod the system" framing (ch36 line 31
vs ch07 697); acceptable. **Keep, ensure cross-refs stay.**

### D3. Multi-scale / composite detection (ch07 / ch09 / ch38)
- **ch09** (`ch09-composite-agent.tex`) already establishes composite agency, composite surplus
  `\mathcal{D}` and decomposition penalty `\lambda_\Sigma` (lines 100–192), and "align only the model
  while the loop is the agent" (line 32) — which ch38 restates as its closing maxim "Do not align the
  component while the loop becomes the agent" (line 691).
- **ch07** supplies boundary closure / `\epsilon`-boundaries that ch38 reuses (ch38 §boundary closure
  84–108 cites `ch:finding-boundary`).
- **ch38** generalizes ch07+ch09 into a *posterior over decompositions* + multi-scale risk score.

**Judgment: keep ch38 — it is a genuine generalization** (posterior over decompositions, regime-
sensitivity `P(D|X,Z)`, the risk-relevance score `R(D)`, the seven-stage protocol). But the
**conceptual overlap with ch09 is high**: ch38's customer-support worked example (388–419) and the
"loop becomes the agent" thesis are close to ch09's composite-agent argument. **Cross-ref, don't trim:**
ch38 should explicitly cite `ch:composite-agent` at its thesis (currently ch38 cross-refs ch07
`ch:finding-boundary` at line 29 but **not** ch09 for the composite claim). Also ch36 §"Cross-scale
measurement" (568–591) previews the ch38 decomposition posterior `P(C_1..C_n|X,I)` **without** a
forward ref to ch38 — add one.

---

## E. CONSISTENCY

1. **Laundering index vs goal-laundering signature.** ch37 defines GLI (line 314):
   `GLI = (w_B D_bundle + w_Φ D_bearer + w_C D_corr + w_S D_succ)·exp(-α D_sem)`. ch10 defines a
   separate `eq:goal-laundering-signature` (line 349, oversight-conditional form). They are
   compatible but never reconciled; ch37 does not cite ch10's signature. **Recommend one explicit
   cross-ref so readers see GLI as the multi-layer generalization of the ch10 signature.**

2. **Four-LAYER vs four-STAGE laundering.** ch37 layers = semantic / **bundle** / bearer / correction
   (line 139ff). ch36 stages = semantic preservation / **proxy substitution** / bearer narrowing /
   correction capture (642–728). "Bundle laundering" (ch37) and "proxy substitution" (ch36) are not
   the same construct, yet both are presented as the second of four. This will confuse a careful
   reader. **Recommend ch36 adopt ch37's layer names (or drop the four-stage list per §D1).**

3. **CCI base term differs across chapters.** ch36 (443–453): `CCI = C_corr − λ_L L − λ_M M − λ_R R −
   λ_O O` with `C_corr = I(C^H;A | S,I)` (single mutual information). ch37 (256–267) and ch38
   (451–462): `CCI / C_corr = min_j I(X_j;X_{j+1}) − penalties` (information-bottleneck *min* over the
   correction chain). Same symbol, two different base quantities. **Recommend standardizing on one
   definition (presumably ch25's canonical CCI) and citing it in all three.**

4. **Multi-scale score.** ch38 `R(D)` (line 287, `sec:multiscale-score-ch38`) is internally consistent
   and consistent with ch36's cross-scale posterior; no conflict found. Good.

5. **Section-title capitalization.** ch36 / ch37 / ch38 use **sentence case** ("The problem with
   watching", "A minimal model of passive and active evidence"). ch39 and ch40 use **Title Case**
   ("Why This Matters", "Plain-Language Model" / "Lethality Checklist", "Open Problem Ledger").
   ch39's headers are the generic Shape-A skeleton labels; ch40's are custom Title Case.
   **Inconsistent within the part.** When ch39 is written it should match ch36–38 sentence case;
   ch40's headers should likely be lower-cased to match.

6. **Chapter-ending naming.** All five end in a section literally titled "Summary" (ch36 1057, ch37
   815, ch38 694, ch39 34, ch40 140) followed by "Chapter References". **Consistent — good.**

7. **Epigraph presence.** ch36/ch37/ch38 (and ch41) have `\epigraph`; ch39 and ch40 have none.
   Minor; add when ch39 is drafted, optionally ch40, for part-internal uniformity.

---

## F. OPEN TANGENTS / DANGLING PROMISES

1. **ch39 stub** — the master dangling promise (see §B, §C). All `[STUB]` content; references appG
   topic but never cites it.
2. **`appG-safety-case-template.tex` is itself a `[STUB]`** (4 lines: "Appendix content to be
   written"). The safety-case chapter and its reusable template appendix are both unwritten — a
   compound gap. ch39, when written, is expected to forward-ref appG; today neither end exists.
3. **ch36 line 1055 / ch38 line 709 / ch35 line 1009** all promise the safety case (ch39) that is not
   delivered.
4. **ch40 inline TODOs in committed source** — lines 119 and 121 (`% TODO[open-crux]…`) and line 117
   (cross-chapter index pointer to `metadata/TODO.md`). These are author scaffolding left in the .tex.
5. **ch36 §"Cross-scale measurement" (568–591)** previews the ch38 posterior over decompositions with
   no forward ref to ch38 — a soft dangling thread.
6. **ch38→ch37 / ch36→ch38 / ch40→ch41** missing or one-directional bridges (see §C/§D3/§G).

---

## G. CONTINUITY HAND-OFF (incoming / outgoing concepts)

- **Incoming to Part IX (from ch35 / Part VIII):** alignment attractor, artifact conductivity,
  tripwires/decision authority, "safety cases require auditors who know what evidence looks like"
  (ch35 line 1009). Part IX is the cash-out of that attractor in concrete measurement + a safety case.
- **ch36 carries in:** boundary (`ch:finding-boundary`), strategic opacity / `J_hide`
  (`ch:strategic-opacity`), value-bundle geometry (`ch:value-bundle-model`), correction channels
  (`ch:correction-causal-channel`, `ch:correction-channel-integrity`), successors
  (`ch:successor-central-test`, `ch:conserved-properties`), goal transport (`ch:goal-transport`).
- **ch36 carries out:** perturbation/invariant/adversarial-measurement toolkit; forwards laundering
  detail to ch37 (260) and the safety case to ch39 (1055).
- **ch37 carries in/out:** four-layer laundering (shared with ch10/ch23); forwards stress/perturbation
  back to ch36 (335) and successor invariants to ch28/ch29; central output is GLI + the stakes gradient.
- **ch38 carries in/out:** composite agency (ch09, *uncited at thesis*), boundary closure (ch07),
  laundering-at-scale (ch37, line 353); output is the decomposition posterior + `R(D)`; **explicitly
  hands to ch39 (709).**
- **ch39 (stub):** *intended* to ingest ch36+ch37+ch38 plus Parts I–VIII claims and emit the
  consolidated safety case + stop conditions + evidence requirements; currently ingests/emits nothing.
- **ch40 carries in:** the whole framework as the object under stress; cites ch33 (ICI/coalitions) and
  ch35 (pivotal process) in a source comment (line 117). **No outgoing ref to ch41** — the Part IX→X
  seam is unmarked.

---

## PRIORITIZED RECOMMENDATIONS (no edits made)

1. **Write ch39.** Highest priority in the part. Assemble the boundary/capability/value-bundle/
   correction/successor/basin claims into one explicit safety case with stop conditions and evidence
   requirements; cite ch36/ch37/ch38 as its measurement instruments; reference `appG`. Match ch36–38
   sentence-case headers and add an epigraph + real `chapterthesis`.
2. **Write `appG-safety-case-template`** in tandem with ch39 (it is the reusable artifact ch39 promises).
3. **Flesh out ch40** to its 9000-word target: add per-lethality prose, resolve or migrate the two
   inline `% TODO[open-crux]` items, and add a forward bridge to ch41.
4. **Dedupe goal laundering:** demote ch10 (378–399) and ch36 (635–729) to previews that cross-ref the
   canonical ch37; reconcile ch36's four-stage list with ch37's four-layer list; have ch37 cite
   ch10's `eq:goal-laundering-signature` and ch23's `eq:transport-stack`.
5. **Standardize CCI** base term across ch36/ch37/ch38 to the canonical ch25 definition.
6. **Decide a WWCTV policy** — the exact heading currently exists only in the stub ch39; either adopt
   the prose substitutes as house style or standardize the heading across ch36–ch40.
7. **Add missing cross-refs:** ch38 thesis → ch09 (composite); ch36 §cross-scale → ch38; ch37 → ch36
   bridge; ch40 → ch41 bridge.
