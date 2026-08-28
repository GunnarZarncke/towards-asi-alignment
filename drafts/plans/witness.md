# Witness — deployment witness plan

Status: **Phase 4 closed** (2026-08-28). Next: [`witness-c004-raw.md`](witness-c004-raw.md) (W-12). Freeze: [`witness-phase0.md`](witness-phase0.md) · [`witness-phase1.md`](witness-phase1.md) · [`witness-phase2.md`](witness-phase2.md) · [`witness-phase3.md`](witness-phase3.md) · [`witness-phase4.md`](witness-phase4.md) · [`witness-c004-raw.md`](witness-c004-raw.md). **Voice** — [`voice.md`](voice.md). **Construct** — [`construct.md`](construct.md) (2.0 plan open; concrete MS still gated on Exp. 4 **with deployment leverage** — W-9–W-11 are institutional analogues, not that gate).

- [x] **Phase 0 freeze** — charter + measurand sheet + pre-register pass/fail/refuse ([`witness-phase0.md`](witness-phase0.md))
- [x] **Phase 1** — H1 C2 mock (W-1 fail) + H4 MASK refuse (W-2)
- [x] **Phase 2** — H2 Linux (W-3 fail on C-004a/C-005/C-006) + H3 Wikipedia (W-4; C-006 fail, causal RfA refuse)
- [x] **Phase 3** — C-004 Moral Machine non-implication (W-5) + C-007 Arena×MASK selector (W-6)
- [x] **Phase 4** — C-004 leftover refuses (W-7); Lean C2 pin (W-8); three H5 trees (W-9–W-11)

## Goal

Meet the **implied reader expectations** from the current stack (values → mechanism → proof-shaped artifacts → alignment) **for real**, not by stronger disclaimers.

**Operational definition of “met”:** for each expectation below, produce at least one **bounded-class witness** on a system whose traces already exist, can be fetched, or can be inferred without building a new world. A witness must be able to **fail** the layer on that host. A **refuse** (explicit stop: this measurand cannot be adversarially verified here) counts as success for Expectation 3; a green dashboard with no stop does not.

**Non-goals:**

- Prove ASI alignment or discharge all `MB*` bridges globally.
- Treat in-repo simulators (toy, embedded, lab, graded-lab) as deployment-class witnesses by themselves. ET-1 (Orbit) and ET-2 (CIL `basin_stability`) are **substrate-suitability negatives**, not homework to “fix” before Witness.
- Block Phase 1 on CIRIS Lens cohort capture (substantial trace volume; deferred to Phase 5 per sibling charter).

**Sibling charter (C-003 / C-005 on CIRIS):** [`~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`](../../../ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md). Phase 1 here aligns with that Phase 1.

**Canonical experiment posture:** [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md) — methodology-building and sanity checks only; negatives are first-class.

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
| World Values Survey / European Social Survey | **W-7 refuse** (country unit) |
| Moral Machine (MIT) | **W-5:** country AMCE (wrong unit). **Next:** raw same-respondent dilemmas — [`witness-c004-raw.md`](witness-c004-raw.md) |
| HH-RLHF / PKU-SafeRLHF | Later/optional; need same judge across varied contexts |
| Sibling `brain-to-values` papers (if local mirror has tables) | Only if numbers, not narrative |

**Met if (paid W-5, wrong unit):** 1-D close while geometry far on **country** AMCE.

**Met if (same-unit, ch16):** repeated counterfactual policy from one decision-maker; frozen geometry predicts held-out choices better than frozen 1-D and intercept. Protocol: [`witness-c004-raw.md`](witness-c004-raw.md) (W-12). LHCV \(L\to H\to C\) is **not** required for this bar.

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
| **Linux `Reviewed-by` rings** | H2 | Rubber-stamp (MSR literature) | Likely **refuse** — still valid Witness outcome |

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

Four claims are **problem statements**. Witness = independent replication on a host not built for the book.

| Claim | Host | Measure |
|-------|------|---------|
| Anti-capture correction validity | H3 SPI; H1 WA-blind C2 | Same org on both ends of channel → invalid, not low score |
| Bearer-map commutation failure | H3 BLP vs quality metrics | Vocabulary stable, who counts changes |
| Certification-under-manipulation | H4 MASK; H2 `Reviewed-by`; H4 LMSYS | Estimate \(\kappa^*\) or **refuse** |
| Goodhart as selector | H4 leaderboards; H3 RfA vs sanctions; H2 vendor share | Population on proxy, target flat/down |

**Met if:** each has one **non-TSA-authored** results table. Status may stay `framework`; “established” = separation replicated, not alignment solved.

---

## Phasing

### Phase 0 — freeze (**done** 2026-08-28)

Canonical freeze: [`witness-phase0.md`](witness-phase0.md) (charter, pass/fail/refuse table, measurand sheet). Amend that file to reopen. This section is the index, not a second freeze.

### Phase 1 — highest leverage (**done** 2026-08-28)

Protocol: [`witness-phase1.md`](witness-phase1.md). Ledger: [`experiments/witness/results/FINDINGS.md`](../../experiments/witness/results/FINDINGS.md).

1. **H1 CIRIS C2** — **W-1** layer fail (named green, composite continues). Analog cut ≠ Verify subject (not UAD). Expectation 5 external pair unpaid.
2. **H4 MASK** — **W-2** refuse \(M\) as safety leaf (published honesty does not improve with scale).

**Exit met:** W-1 fail + W-2 refuse; mapped to C-003/C-005 and Expectation 3 / C-010. MB1 and A-009 still open.

### Phase 2 — public socio-technical hosts (**richer sources** 2026-08-28)

Protocol: [`witness-phase2.md`](witness-phase2.md) (`h2-v1.2.0`, `h3-v1.1.0`).

- **H2 Linux** — **W-3**: C-004a **fail** (`Reviewed-by` on 17 047/60 176 BIC SHAs); C-005 **fail** (cpufreq revert then same-title re-entry); C-006 **fail** (adjusted `-stable` `event_sched_out`); `Reviewed-by` as \(M\) refuse.
- **H3 Wikipedia** — **W-4**: causal RfA **refuse** (API join, no control); Orangemoody anti-capture **fail**; C-006 **fail** (BetacommandBot BRFA→flag/block); SPI as \(M\) refuse (wiki-socks twins, no \(\kappa^*\)).

**Exit:** host traces, not catalog text. KernelCI and lore NAK mbox still unpaid.

### Phase 3 — selection + bundle (**done** 2026-08-28)

Protocol: [`witness-phase3.md`](witness-phase3.md) (`h4-bundle-v1.0.0`, `h4-selector-v1.0.0`).

- **C-004** — **W-5** layer fail: Moral Machine country AMCE, Number 1-D vs eight-coordinate geometry.
- **C-007** — **W-6** layer fail: Arena Elo 20250301 × MASK \(P(\mathrm{honest})\) / Accuracy (\(n=24\)).

**Exit:** both tables paid. WVS/ESS refused in **W-7**; HH-RLHF optional not run; H2 vendor-share / H3 editor retention still unpaid.

### Phase 4 — Lean fixture + historical stops (**done** 2026-08-28)

Protocol: [`witness-phase4.md`](witness-phase4.md) (`c004-leftovers-v1.0.0`, `c2-lean-v1.0.0`, `h5-v1.0.0`).

- **Slice A** — **W-7** refuse WVS/ESS/LHCV-host; optional HH/PKU skip.
- **Slice B** — **W-8** `WitnessC2Instance.lean` pins C2 JSON; `#print axioms` honest; not `Safe`.
- **Slice C** — **W-9** FAA Order 2019-03-13; **W-10** GPLv3 §6; **W-11** Debian RC #802812. Institutional analogue; Construct concrete-MS still gated.

**Exit:** Expectation 2 paid on authored mock; Expectation 4 paid as analogue only.

### Next — C-004 same-unit MM raw (not a numbered Phase)

Protocol freeze: [`witness-c004-raw.md`](witness-c004-raw.md). Finding **W-12**. Country AMCE stays W-5. CIRIS live stays Phase 5.

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

**Phase fails Witness** only if outcome is *pass with no stop* while strong wording would still be warranted.

---

## What Witness still will not buy

Even if all phases hit:

- No bridge becomes “true of frontier ASI.”
- `MB11` / `Safe` stays open unless an authority with deployment leverage uses the tree (H5 is analogue, not AI).
- Graded-lab / Orbit / CIL remain **method limits**, not blockers.
- **Construction of an alignment attractor.** Expectations 1–6 pay *evaluation and certification* of existing processes. They do not change \((Q,f,\theta,E)\) so a pre-specified \(D\) becomes occupyable. Expectation 4 is explicitly *certification without construction*. The **Construct** lane ([`construct.md`](construct.md)) is separate: constructibility outlining is not a Witness phase; *concrete* manuscript chapters stay blocked until a real stop **with deployment leverage** (W-9–W-11 are analogues only).

---

## Suggested first actions

1. ~~Freeze Phase 0~~ — [`witness-phase0.md`](witness-phase0.md).
2. ~~Phase 1 H1 C2 + H4 MASK~~ — W-1 / W-2.
3. ~~Phase 2 H2 Linux + H3 Wikipedia~~ — W-3 fail / W-4. KernelCI and lore NAK optional later.
4. ~~Phase 3: H4 leaderboards + Moral Machine~~ — W-5 / W-6.
5. Sibling CIRIS Phase 2 (integration harness) is optional and not a gate for W-1.
6. ~~Phase 4: C-004 refuses + Lean pin + three H5 trees~~ — W-7–W-11.
7. **W-12 Moral Machine raw** — [`witness-c004-raw.md`](witness-c004-raw.md). Phase 5 CIRIS live is still not a gate for W-1.

## Related files

| File | Role |
|------|------|
| [`metadata/claims-ledger.md`](../../metadata/claims-ledger.md) | C-003–C-007, C-044 discharge language |
| [`metadata/experiments.yml`](../../metadata/experiments.yml) | MB coverage matrix; ET-1/ET-2 negatives |
| [`appendices/appM-institutional-histories.tex`](../../appendices/appM-institutional-histories.tex) | H5 stop candidates |
| [`formal/README.md`](../../formal/README.md) | Lean three-bucket rule |
| [`chapters/ch42-safety-case.tex`](../../chapters/ch42-safety-case.tex) | Refusal test definition |
| [`chapters/ch48-towards-alignment.tex`](../../chapters/ch48-towards-alignment.tex) | Comfort-ontology counterexample |
| [`papers/constructing-alignment-attractors/`](../../papers/constructing-alignment-attractors/) | Construction criterion (spin-out; not in manuscript) |
| [`drafts/plans/witness-phase0.md`](witness-phase0.md) | Phase 0 freeze (charter, measurands, pass/fail/refuse) |
| [`drafts/plans/witness-phase1.md`](witness-phase1.md) | Phase 1 H1/H4 protocol freeze |
| [`drafts/plans/witness-phase4.md`](witness-phase4.md) | Phase 4 freeze (C-004 leftovers, Lean pin, H5 trees) |
| [`drafts/plans/witness-c004-raw.md`](witness-c004-raw.md) | C-004 same-unit MM raw freeze (W-12) |
| [`drafts/plans/witness-next.md`](witness-next.md) | Next tests after Phase 4 |
| [`experiments/witness/`](../../experiments/witness/) | W- findings, C2 fixture, Eric memo |
| Sibling [`ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`](../../../ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md) | H1 Phase 1 charter |
