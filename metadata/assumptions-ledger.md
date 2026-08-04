# Assumptions Ledger

Single source for the maintained assumptions record. The ledger is not currently typeset as a standalone appendix; keep its entries synchronized with the chapters and formal spine.

Maintainer detail (failure modes, tests, claim links): sections I–IV below. Claims: `metadata/claims-ledger.md`. Disconfirmers: `metadata/uncertainty-ledger.md`, Appendix H.

**Maintenance note:** This ledger is the source for generated Appendix E, but the ledger itself is manually maintained. Update it whenever chapter assumptions, Lean bridge assumptions, claim links, or uncertainty links change. Treat the generated appendix as downstream of this file, not as an independent source of truth, until ledger automation is implemented.

**Last verification:** 2026-06-27 — cross-checked chapter assumption statements and Lean bridge assumptions after adding grounding viability as the sixth Introduction claim and eighth safety-case layer (see §Verification).

---

## Verification (2026-06-25)

| Chapter source | Ledger coverage |
|----------------|-----------------|
| ch05 Background Assumptions + \(C_{\text{corr}}^{\text{society}}\) | A-003, A-004, A-005 |
| ch02 Minimum Assumptions (civilizational frame) | A-011 |
| ch03 dynamical guarantee (certified class / basin; grounding viability) | A-010, A-014 |
| ch14 load-bearing co-scaling assumption | A-012 |
| ch46 WWCTV five bundle-inference dependencies | A-001, A-002, A-006 (split in ch46; one row each here) |
| ch46 compression test / MDL | A-006; S07 |
| ch46–27 correction channel | A-002 |
| ch46–31 successors / certification | A-007, A-010 |
| ch46–35 selection / basins | A-008 |
| ch46–40 adversarial measurement | A-009 |
| ch47 verifiability labels / grounding capture | A-009, A-014 |
| Lean `MB1`–`MB9`, `S07` | MB*, S07 |
| ch48 inferential-coupling / acausal-UAD detector, audit-side \(P_{\text{meta}}\), and threshold caveat | A-013, U-12, MB7d |
| ch48 safety-case example assumptions (test coverage, human comprehension) | Instance-level; not book-wide A-rows (see ch48 prose) |
| ch46 “do not assume agent/sensors/goal” | Methodological (non-assumption); intentional model tested, not presupposed |

**Added this pass:** A-014 (grounding viability / conservative abstraction) and MB9.

---

## Quick index

| ID | Short name | Home |
|----|------------|------|
| A-001 | Low-dimensional value-bundle structure | ch16 |
| A-002 | Correction channels as causal chains with measurable integrity | ch46 |
| A-003 | Societal correction capacity above threshold | ch05 |
| A-004 | Observable / discoverable agent boundaries | ch07 |
| A-005 | Certifiable deployment + human agency | ch05 |
| A-006 | Intention / goal transport inferable via compression | ch46 |
| A-007 | Successor influence through auditable channels | ch46 |
| A-008 | Selection environment shapes outcomes | ch46 |
| A-009 | Adversarial verifiability (master crux) | ch47 |
| A-010 | Projectable dynamical / certified-class guarantees | ch03 |
| A-011 | Civilizational-frame minimum assumptions | ch02 |
| A-012 | Correction co-scales with capability (or pause/stop) | ch14 |
| A-013 | Inferential-coupling detector certificates | ch48 |
| A-014 | Grounding viability / conservative abstraction | ch03 |
| S07 | MDL: positive gain ⇒ preferred model | ch46 |
| MB1–MB10 | Lean bridge axioms (`MB1`–`MB9` packaged in `BridgeAssumptions`; `MB10` threaded explicitly) | appI (+ chapter bridges) |

---

## I. Manuscript assumptions (maintainer notes)

### A-001 — Low-dimensional value-bundle structure

**Assumption:** Human value-relevant variation has enough low-dimensional bundle structure to approximate, learn, and transport, and the representation map into that bundle structure is recoverable enough under counterfactual, cultural, and institutional variation.

**Also stated in:** ch04, ch15–17, ch46 (WWCTV items 1, 4), ch46, ch45–43.

**Failure mode if false:** Proxy preservation instead of values; cheap readout from supplied bundle coordinates but no tractable way to discover the right coordinates. **Lean:** MB2, MB3. **Bears on:** C-004 · **U-01, U-02**

### A-002 — Correction channels as causal chains

**Assumption:** Handle-controlled correction pathways with measurable \(\mathrm{CCI}\), evaluated only when the correcting agent or institution has independently controlled, not-captured handles into the target system, and where No-Bypass authorization rests on certified boundary separation rather than a target-mediated independence story.

**Also stated in:** ch46–27, ch46, ch46 (WWCTV item 5), ch48.

**Failure mode if false:** Corrigibility theater; capture; shutdown buttons remain as one-bit rituals while broader correction collapses; CCI reads high after the target has reshaped the human reference process or manufactured the independence test. **Lean:** MB4 plus the explicit bridge **MB4a** (measured-path legitimacy: control, persistence, and the anti-capture `notCaptured` condition for the designated measured path — no longer a field of the axiomatic path itself, so capture is a representable state and `capture_defeats_correction_integrity` derives its refutation of correction integrity); MB8 is a legacy/CEV-style alternate route from externally certified value-update preservation to correction integrity. Manuscript ch48 now ties the anti-capture condition to UAD/BIQ-style separation of control loci. **Bears on:** C-005 · **U-03, U-07**

### A-003 — Societal correction capacity

**Assumption:** \(C_{\text{corr}}^{\text{society}}(t_0) > \theta\).

**Canonical:** ch05 §Correction-Capacity Assumption. **Not an MB axiom.** **Bears on:** C-002, C-005, C-007 · **U-15**

### A-004 — Discoverable boundaries

**Assumption:** Boundaries are discoverable under approximate observability and adversarial limits when the candidate class is structured, intervention handles are adequate, the boundary margin exceeds observation distortion and finite-sample error, and learned detector targets do not merely amortize the criterion or import labeled-agent ontology.

**Failure mode if false:** Boundary recovery fails under finite data or adversarial presentation (measurement hardness); or, prior to measurement, the agent--world cut is ill-defined, modeler-supplied, or metaphysically inflated rather than a stable object to estimate (Pearl/Friston blanket skepticism; ch06 footnote).

**Also stated in:** ch05, ch06–07, ch09–10, ch46, ch45. **Lean:** MB1, MB7a–b. **Bears on:** C-001, C-003 · **U-05**

### A-005 — Certifiable deployment and human agency

**Assumption:** Deployment can be gated by certification; humans can refuse, revise, coordinate.

**Also stated in:** ch05, ch48–32, ch48. **Lean:** MB6a, MB6b. **Bears on:** C-006, C-007 · **U-11, U-15**

### A-006 — Compression / transport inferability

**Assumption:** Intentional and transport models earn compression gain after complexity cost; ch46 items 2–3 (bundle/bearer inferability).

**Canonical:** ch46. **Lean:** S07, MB2. **Bears on:** C-009 · **U-09**

### A-007 — Successor channel auditability

**Assumption:** Successor influence passes through specifiable, auditable channels (seven conserved properties, ch48), and syntactic/semantic preservation can be tested separately from import-preserving transport.

**Also stated in:** ch08, ch46–31. **Lean:** MB5; syntactic-tiling/import-preservation separation. **Bears on:** C-006 · **U-04, U-13**

### A-008 — Selection environment

**Assumption:** Outcomes depend on socio-technical selection (fitness, basins), not weights alone.

**Also stated in:** ch02 loop, ch48, ch48, ch48. **Lean:** MB6a, MB6b. **Bears on:** C-007 · **U-10, U-11**

### A-009 — Adversarial verifiability

**Assumption:** At least one core measurand is cheaper to satisfy without faking than to fake under optimization pressure.

**Also stated in:** ch48, ch46, ch46–39b, ch48. **Lean:** MB7b, MB7c, MB7d. **Bears on:** C-005, C-007, C-010, C-044 · **U-03, U-12, U-14**

### A-010 — Dynamical guarantees

**Assumption:** Alignment expressed as certified-class / basin invariants over time, not static \(P(A_t)\).

**Also stated in:** ch48, ch46. **Lean:** certification scaffolding + MB5, MB6a, MB6b. **Bears on:** C-002, C-006, C-044 · **U-04, U-13**

### A-011 — Civilizational-frame minimum assumptions

**Assumption:** (1) AI mediates high-effect decisions; (2) institutions/markets select deployment patterns; (3) mediation changes correction-relevant information; (4) human values/institutions are plastic.

**Canonical:** ch02 §Minimum Assumptions. Stronger claims deferred to later chapters. **Bears on:** C-001, C-007

### A-012 — Correction co-scaling

**Assumption:** Correction, oversight, and interpretability can co-scale with capability across real jumps (Part III hinge); otherwise only pause/stop remains.

**Canonical:** ch14 WWCTV load-bearing bullet. **Bears on:** C-008 · **U-06**

### A-013 — Inferential-coupling detector certificates

**Assumption:** At a specified audit resolution, UAD-discovered agents plus inferential-coupling detector evidence are sufficient to identify action-relevant dependence that remains after ordinary communication and control channels are cut. Full acausal trade is one limiting case; common-cause/shared-history, non-message inference, and self-similarity can also produce the relevant dependence. The \(P_{\text{meta}}\) structure is an audit-side/expositional certificate over shared decision-relevant inference structure, not a claim that agents symbolically represent a meta-prior. Self-modeling evidence may be symbolic, implicit in weights, scaffold-mediated, or behavioral; probe coverage and \(\tau_{\mathrm{ac}}\) / open-edge thresholds must be calibrated against base rates, adversarial costs, and false-positive/false-negative tradeoffs.

**Canonical:** ch48 inferential-coupling / acausal-trade section; threshold calibration deferred to ch47/ch48. **Lean:** `CooperationGraph.lean` (`MetaPriorEvidence`, `InferentialDetectionCertificate`) and MB7d. **Bears on:** C-007 · **U-12**

### A-014 — Grounding viability / conservative abstraction

**Assumption:** The deployment class admits checked abstractions whose grounding relation is conservative enough that value-relevant real-world changes either move the checked representation or raise uncertainty before irreversible loss. Formally, the safety case needs a defensible domain for \(\Gamma\) where \(d_V(x,x')>\epsilon\) implies \(d_Z(\alpha(x),\alpha(x'))>\delta\) or \(\mathsf{Unc}_{\alpha}(x,x')\uparrow\).

**Canonical:** ch03 grounding viability; propagated through ch16/ch46 value-bundle validity, ch46 correction validity, ch46 safety-case layer, and ch47 adversarial verifiability. **Lean:** MB9 plus structural grounding predicates. **Bears on:** C-004a, C-004, C-005, C-044 · **U-16**

---

## II. Lean scaffolding

Abstract carriers in `Core.lean` (`System`, `State`, …) are mathematical interfaces, not empirical assumptions. Criticize **A*** and **MB***, not `System : Type`.

---

## III. Lean imported (S01–S10)

Appendix I §Imported Assumptions. Only **S07** (MDL ordering) and **S10** (blanket-measurand coherence: the per-system BIQ measurands respect their channel-capacity semantics; replaced four formerly unlabeled axioms in `Capability.lean`, 2026-07-19) are explicit Lean `axiom`s. S09-style percolation theory enters via MB6a.

---

## IV. Lean bridges (MB1–MB11, MB4a)

Formal statements: Lean Proof Spine appendix; validation program: Research Program appendix. Lean: `Core.lean` `BridgeAssumptions` packages `MB1`–`MB9`; three bridges are threaded explicitly rather than packaged because their statements need later definitions: `MB4a` (measured-path legitimacy incl. anti-capture, `Correction.lean`), `MB10` (`AlignmentProofSpine/Forgeability.lean`), and `MB11` (safety-case adequacy, `Certification.lean`). Mapping of each bridge to the canonical field crux it inherits (and the owning agenda): `appendices/appB-bridge-crosswalk.tex` (*Bridges and the Field: A Crosswalk*).

**Anti-capture / `MB4a` (2026-07-19):** the anti-capture condition (`notCaptured`) is no longer a field of the axiomatic `SystemCorrectionPath` — the measured path carries data only (corrector, handles, capacities), and legitimacy (control, reach, persistence, anti-capture) is the separate predicate `CorrectionPathLegitimate`, supplied only by the labeled bridge `MB4a`. Capture is therefore a representable state: `capture_makes_cci_captured_or_invalid` (unconditional) and `capture_defeats_correction_integrity` (contrapositive of `MB4a`) are theorems, replacing what was previously assumed by construction plus three unlabeled `CorrectionIntegrity_implies_*` axioms (the nonempty-links one turned out to be provable outright).

**Safety-case adequacy / `MB11` (2026-07-19):** the step from a `CertifiedSafetyCase` (layer evidence + `RiskGap ≤ δ`) plus a deployment-tolerance judgment to the abstract `Safe` predicate is the named bridge `MB11`; the assembly theorems are labeled as packaging, and `P30_safe_of_case` consumes the record through exactly this axiom. `MB11`'s `WithinDeploymentRiskTolerance` (2026-07-20) is the framework's honest answer to "what is the probability of failure / expected value loss" — a `Prop`-valued acceptance gate, not a quantified number; no theorem in this development computes a failure probability or a value-loss estimate. **`ToyDeploymentGate.lean` (2026-07-20):** `EpisodeBatteryGate` + `frozen_validation_battery_gate_passes` (`decide` on committed `embedded_frozen_validation.json` aggregates: 3 false passes / 36 runs, max 5 pre-registered) shows the *shape* of discharging tolerance; mapping that gate to `WithinDeploymentRiskTolerance A δ` remains a governance judgment (same epistemic class as θ / `MB1`).

**Bridge independence / `SpineModel.lean` (2026-07-20):** `spine_axioms_consistent` + `spine_axioms_nontrivial` plus one `*_independently_load_bearing` theorem per labeled bridge (reusing `Defeaters`/`Forgeability` toys where they exist). Checked by `formal/scripts/check_spine_model.py`.

**Löbian tiling contrast / `Field/Finite/LobTiling.lean` (2026-07-20):** `lob_rule_from_fixed_point` derives the Löb rule from an explicit `HBLConditions` record and a named `LobFixedPoint`. The fixed-point existence is a field-scope diagonal-lemma hypothesis, not an `MB*` bridge and not asserted for the book's proof spine or real agents. `self_certifying_tiling_obstruction` gives the conditional diagonal case against accepting a successor solely by reflecting the same proof system's proof of its safety. The contrast theorem uses `SuccessorAuditLinks` instead: measured control and correction inequalities, with their validation and governance still open at every step.

**Successor forgeability / `MB10` (2026-07-02):** ch08/ch31's own WWCTV sections already name the failure mode --- a successor can pass every conserved-property check while defecting on the unmeasured remainder. `formal/AlignmentProofSpine/Forgeability.lean` makes it a checked finite counterexample (`forgeability_gap`: for every claimed harm bound, a toy successor reads all-seven-green and stays within the measured risk bound while its true harm exceeds it) and names the missing condition as `MB10`: the conserved-property audit channel must be adversarially verifiable up to the successor's capability (ch43's cost relation, `appendices/appG-lean-proof-spine.tex` §`appi:sec:forgeability`). `MB10` is not required for the top certification theorem; it gates whether `MB5`'s successor-safety conclusion means anything against a capable adversarial predecessor.

**Defeater ledger (2026-07-02):** each bridge's "failure mode if false" now has a named Lean-side signal in `formal/AlignmentProofSpine/Defeaters.lean` (`appendices/appG-lean-proof-spine.tex` §`appi:sec:defeaters`), so the reservation has a type, not just prose. `MB1`, `MB4`, `MB6b`, `MB8` additionally have a finite toy model proving the antecedent-signal-not-consequent shape is logically consistent (axiom footprint: `propext` only). `MB7b`–`MB7d` reduce their defeater to `Chokepoint.SteerableAt`. No signal is claimed to hold; this does not discharge or refute any `MB*`.

**Axiom budget guard (2026-07-02):** which top-level theorems actually depend on which `MB*` bridges is checked mechanically, not asserted from memory. `formal/scripts/check_axiom_budget.py` diffs `#print axioms` on a curated set of headline theorems against `formal/axiom-ledger.json` and regenerates `appendices/appG-lean-proof-spine.tex` §`appi:sec:axiom-budget` (Table `tab:appi-axiom-budget`) from it; e.g. it confirms `certified_class_safety_from_spine_and_bridges` uses all nine bridges while `certified_class_safety_from_bridge_record` uses none directly (bridges supplied as data), and that the chokepoint/defeater sanity theorems stay exactly as axiom-heavy as claimed.

| Bridge | Manuscript A-IDs |
|--------|------------------|
| MB1 | A-004 |
| MB2, MB3 | A-001, A-006 |
| MB4, MB4a, MB8 | A-002 |
| MB5 | A-007, A-010 |
| MB6a | A-008, A-011, A-013 (percolation / coupling evidence) |
| MB6b | A-005, A-008, A-011 (institutional selection) |
| MB7a | A-004 |
| MB7b, MB7c | A-009 |
| MB7d | A-009, A-013 |
| MB8 | A-002 |
| MB9 | A-014 |
| MB10 | A-007, A-009 (not packaged in `BridgeAssumptions`) |
| MB11 | C-001 (claims ledger; not packaged in `BridgeAssumptions`) |

---

## Appendix index

Tables below provide one line per assumption; full context is in the cited chapter.

### Scope and preconditions

| ID | Assumption | Home |
|----|------------|------|
| A-003 | Civilization retains enough correction capacity: $C_{\text{corr}}^{\text{society}}(t_0) > \theta$ | ch05 |
| A-004 | Frontier systems remain observable enough for boundary discovery and measurement | ch05 |
| A-005 | Deployment can be conditioned on certification; humans retain agency to refuse, revise, and coordinate | ch05 |
| A-011 | AI mediates high-effect decisions; selection shapes deployment; mediation changes correction information; values and institutions are plastic | ch02 |

### Value, inference, and transport

| ID | Assumption | Home |
|----|------------|------|
| A-001 | Human values have enough low-dimensional bundle structure to approximate, learn, and transport | ch16 |
| A-006 | Intentional and transport models earn compression gain after complexity cost (MDL / $\Delta L$) | ch46 |
| A-014 | Grounding relation is conservative: value-relevant change moves the checked abstraction or raises uncertainty | ch03 |

### Correction, capability, and verification

| ID | Assumption | Home |
|----|------------|------|
| A-002 | Correction is a handle-controlled causal chain with measurable integrity ($\mathrm{CCI}$) | ch46 |
| A-012 | Correction-relevant capacity co-scales with capability across real jumps (else pause/stop) | ch14 |
| A-013 | Inferential-coupling detector certificates: audit-side \(P_{\text{meta}}\), self-modeling evidence, probe coverage, calibrated \(\tau_{\mathrm{ac}}\) | ch48 |
| A-009 | At least one safety-relevant measurand is adversarially verifiable under optimization pressure | ch47 |

### Successors, dynamics, and selection

| ID | Assumption | Home |
|----|------------|------|
| A-010 | Alignment is a dynamical guarantee over a certified class / basin, not a static property | ch03 |
| A-007 | Successor influence passes through specifiable, auditable channels | ch46 |
| A-008 | Alignment outcomes depend on socio-technical selection, not model weights alone | ch46 |

### Lean conventions and bridges

| ID | Assumption | Home |
|----|------------|------|
| S07 | Positive description-length gain $\Rightarrow$ preferred model (MDL ordering) | ch46 |
| S10 | Blanket-measurand coherence: per-system BIQ measurands respect their channel-capacity semantics ($I_{\text{pred}} \le C_{\text{sens}}$, $I_{\text{ctrl}} \le C_{\text{act}}$, nonnegative penalties) | ch11 |
| MB1 | $\epsilon$-boundary certificates imply genuine boundary separation | ch07 |
| MB2 | Bundle-gradient equivalence implies bundle alignment | ch16 |
| MB3 | Bundle transport plus bearer-map agreement implies bearer transport | ch18 |
| MB4 | Correction-channel integrity implies legitimate correction-operator preservation | ch46 |
| MB4a | Measured correction path is legitimate under correction integrity: controlled, reaching, persistent, uncaptured (not packaged in \texttt{BridgeAssumptions}) | ch26 |
| MB5 | Full transport plus bearer transport implies successor safety | ch46 |
| MB6a | Percolation / coupling evidence implies socio-technical basin stability | ch48 |
| MB6b | Socio-technical basin stability implies correction-channel integrity | ch48 |
| MB7a | Boundary alignment plus adequate access model implies access robustness | ch07 |
| MB7b | Access robustness plus filter coverage bounds hidden productive BIQ | ch47 |
| MB7c | Correction integrity plus bounded hidden BIQ implies adversarial robustness | ch47 |
| MB7d | Access robustness plus adequate inferential detector assumptions implies valid inferential-coupling measurement | ch48 |
| MB8 | Legacy CEV-style bridge: externally certified preservation of schematic $U_H$ implies correction integrity; live certification uses the value-update envelope | ch46 |
| MB9 | Grounding certificates imply conservative value-correction abstraction over the certified domain | ch03 |
| MB10 | Successor-safe transition with bounded measured risk implies bounded true harm, given a verifiable conserved-property signature (not packaged in \texttt{BridgeAssumptions}) | ch08 |
| MB11 | Certified safety case within deployment risk tolerance implies deployment safety (not packaged in \texttt{BridgeAssumptions}) | ch42 |

---

## Maintenance

When a chapter introduces a **new load-bearing assumption**, add a row to the Appendix index (and §I notes), then regenerate Appendix E.

Do not duplicate the Executive Overview or a front-matter list; point readers to chapters + Appendix E.
