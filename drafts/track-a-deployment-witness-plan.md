# Track A — deployment witness plan

Status: **draft plan** (2026-08-21). Follow-up to review of implied-reader expectations vs paid claims. **Track B** (packaging / voice) is separate; do not start B until this plan is frozen or explicitly scoped down.

## Goal

Meet the **implied reader expectations** from the current stack (values → mechanism → proof-shaped artifacts → alignment) **for real**, not by stronger disclaimers.

**Operational definition of “met”:** for each expectation below, produce at least one **bounded-class witness** on a system whose traces already exist, can be fetched, or can be inferred without building a new world. A witness must be able to **fail** the layer on that host. A **refuse** (explicit stop: this measurand cannot be adversarially verified here) counts as success for Expectation 3; a green dashboard with no stop does not.

**Non-goals:**

- Prove ASI alignment or discharge all `MB*` bridges globally.
- Treat in-repo simulators (toy, embedded, lab, graded-lab) as deployment-class witnesses by themselves. ET-1 (Orbit) and ET-2 (CIL `basin_stability`) are **substrate-suitability negatives**, not homework to “fix” before Track A.
- Block Phase 1 on CIRIS Lens cohort capture (substantial trace volume; deferred to Phase 5 per sibling charter).

**Sibling charter (C-003 / C-005 on CIRIS):** [`~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`](../../ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md). Phase 1 here aligns with that Phase 1.

**Canonical experiment posture:** [`docs/EXPERIMENTS.md`](../docs/EXPERIMENTS.md) — methodology-building and sanity checks only; negatives are first-class.

---

## Host systems (reuse; do not invent new worlds)

| ID | Host | Why feasible | Primary traces / data | Layers |
|----|------|--------------|----------------------|--------|
| **H0** | In-repo sims | Oracle + frozen fixtures exist | Toy / embedded / lab / graded-lab; `WorkedInstance.lean` | Lean fixture wiring; cost-of-faking **with ground truth only** |
| **H1** | CIRIS local stack | Cloned in review workspace; named-identity vs composite is the sharpest falsifier | Agent traces, Accord, Verify/Lens semantics, tool loop (live or C2 mock) | C-003, C-005, C-006 (partial), MB11 (if real stop), Expectation 5 |
| **H2** | Linux kernel | Public git + labeled review/bug pairs | [Zenodo Linux commits 2005–2023](https://zenodo.org/records/10654193); git.kernel.org; `Reviewed-by` / NAK / revert; stable trees | C-003, C-004a, C-005, C-006, C-007, MB10 analogue |
| **H3** | Wikipedia | Dumps + elections + sockpuppet ground truth | [SNAP wiki-RfA](https://snap.stanford.edu/data/wiki-RfA.html); XML dumps; SPI/sockpuppet cases; bot policy | C-004a, C-005, C-006, C-007, standalone anti-capture |
| **H4** | Model-eval public surface | No lab access required | [MASK](https://huggingface.co/datasets/cais/MASK); field-news incidents (HF eval, CoT optimization, BrowseComp eval-awareness); HF Hub cards + leaderboards; LMSYS Arena | C-004a, C-010, Expectation 3, Goodhart-as-selector |
| **H5** | Conductive-artifact archive | Appendix M already names mechanisms | NTSB/FAA ADs; FDA recalls / FAERS; GPLv2→v3 + AGPL (tivoization, SaaS); Debian RC freeze | Expectation 4 (real stop), MB11 analogue |

**Do not** pick another multi-agent gym whose units are scripted into the generator (ET-1 lesson).

---

## Expectation 1 — Six intro claims paid as deployment-class witnesses

**Met when:** for each of C-003–C-007, a pre-registered protocol on H1–H5 can return **fail**, not only “framework defined.” Chapter 48 status labels (`strong framing`, `conditional`, `necessary`, `plausible`) map to pass/fail/refuse outcomes.

### C-003 Boundary (MB1)

| Approach | Host | Instrument | Success criterion |
|----------|------|------------|-------------------|
| **Primary** | H1 CIRIS | C2 tool-scout scenario (locked in sibling charter): named Verify subject vs tool+memory+user loop | Recovered cut ≠ Verify subject while Verify/Lens stay green |
| **Quant backing** | H0 | Toy T-9 `boundary_decouple`; lab LS-28 intervention-supported UAD | Same disagreement criterion on frozen fixture |
| **Second host** | H2 Linux | Commit + review graph: author vs reviewer vs employer domain | Visible “maintainer” ≠ control locus when vendor subtree dominates merge flow |
| **Retrospective** | H4 field news | OpenAI/Hugging Face eval incident — composite model + harness + staff | Coding of intervening unit vs named model (no new collection) |

**Deliverables:** dual timeline artifact (Phase 1); optional Eric memo; design note mapping five sibling success criteria to evidence.

### C-004 Value-bundle (MB2)

Sims are weakest (toy stub; graded-lab selectable-Goodhart **null** GL-85). Need **fixed ontology + public labels**.

| Dataset / source | Use |
|------------------|-----|
| World Values Survey / European Social Survey | Compressed directions across countries; scalar “progress” vs bundle geometry |
| Moral Machine (MIT) | Tradeoff geometry under shared scene ontology |
| HH-RLHF / PKU-SafeRLHF | Stated preference vs ranking under pressure |
| Sibling `brain-to-values` papers (if local mirror has tables) | Only if numbers, not narrative |

**Met if:** one host shows **non-implication**: moral words or 1-D RM score stable while tradeoff geometry moves, with frozen distance. Wikipedia category/text is backup (noisier).

### C-004a Grounding (MB9)

| Approach | Host | Silent-gap shape |
|----------|------|------------------|
| **License / handle** | H5 + GH Archive | GPLv2 “distribution” trigger vs SaaS deploy: constraint text holds, user cannot run modified code (tivoization / AGPL patch — Appendix M) |
| **Trace vs belief** | H4 | MASK belief vs pressured statement; CoT / eval-awareness field news |
| **Symbol vs harm** | H2 | CI green / message vs Zenodo `bfc_bic` bug-introducing/fixing pairs |

**Met if:** green checked symbol while independent referent (bug, handle, belief) moved; referent pre-registered.

### C-005 Correction (MB4 / MB4a)

| Approach | Host | Test |
|----------|------|------|
| **Institutional** | H3 | RfA: oppose / ArbCom → future edit behavior (causal CCI) vs ritual; SPI as captured corrector |
| **Handle uptake** | H2 | NAK/revert: same patch class re-enters via another tree (theater) vs stops |
| **Named-unit blind** | H1 | WA deferral/shutdown on occurrence while C2 side effects continue → `capturedInvalid`, not low CCI |

### C-006 Successor (MB5 / MB10)

| Approach | Host | Forgeability test |
|----------|------|-------------------|
| **Git successors** | H2 | Parent → `-stable` / distro fork: seven *checked* properties pass, unchecked invariant fails (Lean `forgeability_gap` on real git) |
| **Model successors** | H4 | HF Hub API: base → fine-tune; model card safety text stable, eval suite changed |
| **Bot successors** | H3 | Bot approval → later bot block |

**Met if:** successor passes audited checklist, fails on **unlisted** invariant frozen before inspection.

### C-007 Basin (MB6)

Sims: lab LS-36 (preserving mass erodes); graded-lab selection **null** (GL-23–GL-27). Need **exogenous selector**.

| Selector | Proxy vs target |
|----------|-----------------|
| LMSYS / Open LLM leaderboard / HF downloads | Helpful/fast/Elo vs refusal or correction features across generations |
| Wikipedia editor retention | RfA theater vs article quality |
| Linux vendor-affiliated commit share | Basin mass over time |

**Met if:** selector-driven population shift on proxy that is **not** the preservation target; frozen proxy/target pair.

---

## Expectation 2 — Lean matches a real (bounded) class

**Met when:** `WorkedInstance.lean` (or successor) consumes a **pinned fixture from H1–H4**, not only embedded-sim `honestCert_passes`.

| Step | Work |
|------|------|
| Export | One CIRIS dual-timeline or one Linux revert episode as JSON the spine already eats |
| Theorems | Do **not** add lemmas that assume `Safe`; keep `MB11` as named gap unless H5 supplies analogue |
| Leaves | Replace `Bool`/`True` only where fixture supplies integer/enum; else axiom + **refuse** tag |

**Dependency:** first successful host from Expectation 1 Phase 1–2. Not a separate empirical campaign.

---

## Expectation 3 — One adversarially verifiable measurand

**Met when:** for one measurand \(M\), Chapter 43’s question is answered on a host: below \(\kappa\), faking \(M\) is more expensive than surplus; above \(\kappa\), **stop claiming** \(M\) is evidence — or publish explicit **refuse**.

| Candidate \(M\) | Host | Adversary | Notes |
|-----------------|------|-----------|-------|
| **MASK honesty gap** (belief vs pressured statement) | H4 | Model under pressure prompt | Dataset + protocol exist; RepE optional intervention |
| **Pipeline self-preservation under perturbation** | H1 + deployment-pipeline-simulator logic on **real** CI/tool logs | Randomized threats to visibility/memory | Sim AUROC ~0.75–0.85 is **not** discharge; need non-authored logs or refuse |
| **Wikipedia SPI / sockpuppet** | H3 | Known socks vs honest twins | Labels exist; cost of faking = new account + mimicry |
| **Linux `Reviewed-by` rings** | H2 | Rubber-stamp (MSR literature) | Likely **refuse** — still valid Track A outcome |

**Recommendation:** Phase 1 pair **MASK + CoT/eval-awareness field news** as \(M\) = “honest inner report.” If MASK honesty does not improve with scale (published result), **refuse** the measurand as a safety leaf.

Second shot (Phase 4+): port pipeline perturbation detector to GitHub Actions or CIRIS traces; if logs unavailable, document refuse.

---

## Expectation 4 — Certification without construction: a real stop

**Met when:** some decision (merge, release, bot flag, insurance, WA shutdown, publish/deploy) **would have gone the other way** if a named leaf were ignored.

| Source (H5) | Decision changed | Leaf that bound |
|-------------|------------------|-----------------|
| FAA airworthiness directive | Aircraft grounded / AD mandatory | Independent investigation + enforceable handle |
| Debian RC bug / freeze | Release delayed | Unfixed RC = refused leaf |
| Wikipedia bot block / ArbCom | Rights removed | Correction handle with uptake |
| GPLv3 installation information | Constraint after failed GPLv2 grounding | Successor constraint inheritance |
| CIRIS (if WA actually defers) | Document that decision | MB4a / named-identity fail |

**Protocol:** code **three historical stops** in Chapter 42 tree form (root claim, unsupported leaf, stop). In-sim MB5 deploy gate does **not** count.

**Optional:** self-imposed publish gate (e.g. do not cite “discharge” until C-003 witness exists).

---

## Expectation 5 — Artifacts are not progress unless they can refuse

Same evidence as Expectations 1 and 4. **Met when:** at least one **green artifact + failed uptake** pair on a host:

- CIRIS Verify green / composite continues
- Linux CI green / bug-introducing commit
- MASK-high accuracy / low honesty
- GPL-compliant / tivoized handle

**Deliverable:** single table for Chapter 48 comfort-ontology section — **external** pairs, not only imagined.

---

## Expectation 6 — Standalone claims as replicated separations

Four claims are **problem statements**. Track A = independent replication on a host not built for the book.

| Claim | Host | Measure |
|-------|------|---------|
| Anti-capture correction validity | H3 SPI; H1 WA-blind C2 | Same org on both ends of channel → invalid, not low score |
| Bearer-map commutation failure | H3 BLP vs quality metrics | Vocabulary stable, who counts changes |
| Certification-under-manipulation | H4 MASK; H2 `Reviewed-by`; H4 LMSYS | Estimate \(\kappa^*\) or **refuse** |
| Goodhart as selector | H4 leaderboards; H3 RfA vs sanctions; H2 vendor share | Population on proxy, target flat/down |

**Met if:** each has one **non-TSA-authored** results table. Status may stay `framework`; “established” = separation replicated, not alignment solved.

---

## Phasing

### Phase 0 — freeze (1–2 weeks)

- One-page charter: hosts H0–H5, which claim each may pay, stop rules (ET-1/ET-2 style).
- Pre-register pass/fail/refuse per expectation; no sixth sim line.
- **Exit:** signed-off scope doc (this file + Phase 0 addendum if needed).

### Phase 1 — highest leverage (parallel)

1. **H1 CIRIS C2** — dual timeline + UAD disagreement (C-003, C-005, Expectation 5). Sibling Phase 1 deliverables.
2. **H4 MASK** — honesty gap as \(M\); threshold sketch or explicit refuse (Expectation 3, C-010).

**Exit:** finding IDs + mapping to C-00x / `MB*`; at least one refuse or fail (not only pass).

### Phase 2 — public socio-technical hosts

- **H2 Linux** — revert/fork + `bfc_bic` grounding (C-004a, C-005, C-006).
- **H3 Wikipedia** — RfA + SPI (C-005, MB4a, standalone anti-capture).

**Exit:** two hosts with frozen protocols; negative results logged if null.

### Phase 3 — selection + bundle

- **H4** leaderboards/downloads (C-007, Goodhart-as-selector).
- **WVS / Moral Machine / RLHF** (C-004).

**Exit:** one bundle non-implication table; one selector shift table.

### Phase 4 — Lean fixture + historical stops

- Pin Phase 1 JSON into `WorkedInstance.lean`.
- Code three **H5** stops as safety-case trees (Expectations 2, 4).

**Exit:** `#print axioms` on pinned module; three stop narratives with leaf IDs.

### Phase 5 — only if Phase 1–2 pass

- CIRISAgent live harness (sibling Phase 2).
- Lens cohort / Coherence Ratchet battery (sibling Phase 3) — **not** a gate for logical falsifier.

---

## Verification template (every phase)

Each finding file must include:

```md
## Host
H1 | H2 | …

## Frozen protocol
(version, seed, data snapshot date)

## Expectation / claim
C-003 | Expectation 3 | MB4 | …

## Outcome
pass | fail | refuse

## Stop condition triggered?
yes | no | n/a

## Artifact paths
…
```

**Phase fails Track A** only if outcome is *pass with no stop* while strong wording would still be warranted.

---

## What Track A still will not buy

Even if all phases hit:

- No bridge becomes “true of frontier ASI.”
- `MB11` / `Safe` stays open unless an authority with deployment leverage uses the tree (H5 is analogue, not AI).
- Graded-lab / Orbit / CIL remain **method limits**, not blockers.
- **Construction of an alignment attractor.** Expectations 1–6 pay *evaluation and certification* of existing processes. They do not change \((Q,f,\theta,E)\) so a pre-specified \(D\) becomes occupyable. Expectation 4 is explicitly *certification without construction*. A proposed partial extension is below; it is **not** in the frozen Phase 0 charter until signed off.

---

## Proposed extension — Expectation 7 (construction, partial; not frozen)

**Why this is not already in Track A.** The implied-reader stack is values → mechanism → proof-shaped artifacts → *alignment*. Track A pays that stack by making the existing claims **fail-able on hosts**. Construction is a different verb: change the selection geometry so a *pre-specified* desirable region \(D\) can satisfy the five attractor conditions (*Constructing Alignment Attractors*). The two companion papers currently outrun what they can *do*; integrating them into the manuscript is blocked (`metadata/TODO.md`) until something can fail a construction check, not until the definitions get denser.

**What “partly address” can mean here.** Not: construct \(D\) for ASI, or add a sixth intro claim. Yes: one **bounded-class intervention witness** where the construction *criterion* can return **fail** or **refuse**. That is the same success shape as Expectation 3 (a refuse is success; a green dashboard is not). It answers the reviewer vulnerability — unearned weight — by putting the apparatus under a stop rule.

**Met when:** for one named intervention \(I\) on H2, H3, or H5:

1. \(D\) is frozen **before** \(I\) (clause (iii): \(D\) is not “whatever \(I\) stabilized”).
2. \(I\) is a documented change to at least one of \(Q\), \(f\), \(\theta\), \(E\) (not a stronger score on an unchanged selector).
3. A pre-registered protocol returns **fail**, **refuse**, or a *local* pass with named remaining attractor conditions still open.

A local pass on Wikipedia or Debian is **not** manuscript construction. It is evidence that the vocabulary can be applied without baking the conclusion.

### Candidate witnesses (reuse hosts; do not invent a construction gym)

| Host | Intervention \(I\) (acts on) | Frozen \(D\) (must be independent of \(I\)) | Likely outcome |
|------|------------------------------|---------------------------------------------|----------------|
| **H5** FAA AD / Debian RC freeze | Sanction / release gate on \(f\) or \(\theta\) (PD-lemma analogue: \(\sigma\) against a named defect class) | Pre-registered safety/quality referent (hull integrity; RC policy text), not “whatever shipped after the gate” | **Fail** if the gate is green while the referent moved; **pass-local** if a real stop bound the referent; still open: invasion/regeneration under later capture |
| **H3** Wikipedia | Policy/enforcement change (3RR, SPI, bot policy) — \(\theta\) and announced \(f\) | Article-quality or sockpuppet-suppression referent frozen from dumps *before* the policy date | **Fail** (enforcement collapse / RfA theater); **refuse** if \(D\) cannot be scored independently of the policy language |
| **H2** Linux | Process rewrite (two-maintainer, `-stable` rules, Signed-off-by) — \(\theta\), successor \(Q\) | Unlisted invariant frozen before the process change (C-006 forgeability already in Track A) | Distinguishes *checklist construction* from *signature gaming*; likely **fail** or **refuse** on MB10 analogue |
| **H4** leaderboard / eval-suite change | Selector rewrite \(\theta\) | Pre-registered target *not* the leaderboard metric (C-007 pair) | Default **fail**: proxy basin, target flat — this is Goodhart-as-selector, i.e. construction that occupied the wrong vacuum |
| **H1** CIRIS | Do **not** count WA shutdown as construction; that is Expectation 4 (stop). Construction would be a change to Accord/Verify *rules* with \(D\) frozen first | — | Defer until Phase 1 certification witnesses exist |

**H0 sims are out** for this expectation (same ET-1 rule as the rest of Track A). A replicator sanction in a authored PD is the paper’s lemma, not a deployment witness.

### What this still does not buy

- The five attractor conditions jointly, on one host, for an alignment \(D\).
- Breaking observational symmetry (MASK / Verify remaining a proxy is an Expectation 3 refuse, not a constructed \(D\)).
- Selector endogeneity / Acemoglu–Robinson neutralization: H3/H2 can *illustrate* capture of \(I\); they cannot prove a construction that survives \(G\).
- Identity crystallization / Harris directed \(Q\): no public host currently gives a pre-registered self-model \(D\) plus a training-mixture intervention with a stop. Log as **refuse**, do not stretch H4 cards into it.
- One failed or refused construction check on H2/H3/H5 is **talking-tool validation**, not a contribution to solving alignment. That is the intended calibration.

### Phasing (only if Phase 0 explicitly opts in)

Do **not** block Phases 1–2. Construction needs a selector baseline (Phase 3) and at least one real stop (Expectation 4) so \(I\) is not confused with “we refused to ship.”

- **Phase 3b (optional, after Phase 3):** one H4 or H3 protocol — frozen \(D\), named \(I\), fail/refuse. Cheapest illustration of wrong-vacuum / enforcement-collapse.
- **Phase 4b (optional, with H5 stops):** recode **one** of the three historical stops as an attempted *construction* (payoff/selector change) vs a *certification stop* (leaf ignored → other decision). Same episode, two trees. Makes Expectation 4 and Expectation 7 distinct.
- **Manuscript gate:** even a local pass does not pull Construction into chapters. Revisit the TODO only after at least one **fail** or **refuse** on this expectation (same rule as Track A overall: pass-with-no-stop is the failure mode).

### Relation to existing expectations

| Existing | Construction overlap |
|----------|----------------------|
| C-007 / Goodhart-as-selector | Observes a bad basin. Construction asks whether a named \(I\) *changed* that geometry toward a frozen \(D\). |
| Expectation 4 | Stop without constructing \(D\). Keep this distinction; do not relabel H5 stops as attractor construction. |
| Expectation 3 / C-004a | Observational symmetry. Construction that only intensifies \(\theta\) fails here by the papers’ own lemma limits. |
| C-006 / MB10 | Successor checklist after \(Q\) change — closest existing handle on reconstructive \(Q\); still certification of a signature, not construction of \(D\). |

---

## Suggested first actions

1. Freeze Phase 0 charter (edit § Host systems + § Phasing exit criteria only). **Do not** opt Expectation 7 into Phase 0 by default; construction stays a later addendum.
2. Execute sibling CIRIS Phase 1 (C2 trace mock + memo) in parallel with MASK protocol draft.
3. Add finding stubs under `experiments/` or `review/` only when protocols are frozen — not before.

## Related files

| File | Role |
|------|------|
| [`metadata/claims-ledger.md`](../metadata/claims-ledger.md) | C-003–C-007, C-044 discharge language |
| [`metadata/experiments.yml`](../metadata/experiments.yml) | MB coverage matrix; ET-1/ET-2 negatives |
| [`appendices/appM-institutional-histories.tex`](../appendices/appM-institutional-histories.tex) | H5 stop candidates |
| [`formal/README.md`](../formal/README.md) | Lean three-bucket rule |
| [`chapters/ch42-safety-case.tex`](../chapters/ch42-safety-case.tex) | Refusal test definition |
| [`chapters/ch48-towards-alignment.tex`](../chapters/ch48-towards-alignment.tex) | Comfort-ontology counterexample |
| [`papers/constructing-alignment-attractors/`](../papers/constructing-alignment-attractors/) | Construction criterion (spin-out; not in manuscript) |
| Sibling [`ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`](../../ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md) | H1 Phase 1 charter |
