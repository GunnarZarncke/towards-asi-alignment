# Assumptions Ledger

Single source for **Appendix E** (assumptions index). Regenerate the typeset appendix with `python3 scripts/generate_assumptions_appendix.py` (also run from `./build.sh`).

Maintainer detail (failure modes, tests, claim links): sections I–IV below. Claims: `metadata/claims-ledger.md`. Disconfirmers: `metadata/uncertainty-ledger.md`, Appendix H.

**Last verification:** 2026-06-25 — cross-checked chapter assumption statements against this ledger (see §Verification).

---

## Verification (2026-06-25)

| Chapter source | Ledger coverage |
|----------------|-----------------|
| ch05 Background Assumptions + \(C_{\text{corr}}^{\text{society}}\) | A-003, A-004, A-005 |
| ch02 Minimum Assumptions (civilizational frame) | A-011 |
| ch03 dynamical guarantee (certified class / basin) | A-010 |
| ch14 load-bearing co-scaling assumption | A-012 |
| ch20 WWCTV five bundle-inference dependencies | A-001, A-002, A-006 (split in ch20; one row each here) |
| ch21 compression test / MDL | A-006; S07 |
| ch24–27 correction channel | A-002 |
| ch28–31 successors / certification | A-007, A-010 |
| ch32–35 selection / basins | A-008 |
| ch36–40 adversarial measurement | A-009 |
| ch39b verifiability labels | A-009 |
| Lean `MB1`–`MB8`, `S07` | MB*, S07 |
| ch31 safety-case example assumptions (test coverage, human comprehension) | Instance-level; not book-wide A-rows (see ch31 prose) |
| ch21 “do not assume agent/sensors/goal” | Methodological (non-assumption); intentional model tested, not presupposed |

**Added this pass:** A-011 (ch02), A-012 (ch14).

---

## Quick index

| ID | Short name | Home |
|----|------------|------|
| A-001 | Low-dimensional value-bundle structure | ch16 |
| A-002 | Correction channels as causal chains with measurable integrity | ch24 |
| A-003 | Societal correction capacity above threshold | ch05 |
| A-004 | Observable / discoverable agent boundaries | ch07 |
| A-005 | Certifiable deployment + human agency | ch05 |
| A-006 | Intention / goal transport inferable via compression | ch21 |
| A-007 | Successor influence through auditable channels | ch28 |
| A-008 | Selection environment shapes outcomes | ch32 |
| A-009 | Adversarial verifiability (master crux) | ch39b |
| A-010 | Projectable dynamical / certified-class guarantees | ch03 |
| A-011 | Civilizational-frame minimum assumptions | ch02 |
| A-012 | Correction co-scales with capability (or pause/stop) | ch14 |
| S07 | MDL: positive gain ⇒ preferred model | ch21 |
| MB1–MB8 | Lean bridge axioms | appI (+ chapter bridges) |

---

## I. Manuscript assumptions (maintainer notes)

### A-001 — Low-dimensional value-bundle structure

**Assumption:** Human value-relevant variation has enough low-dimensional bundle structure to approximate, learn, and transport, and the representation map into that bundle structure is recoverable enough under counterfactual, cultural, and institutional variation.

**Also stated in:** ch04, ch15–17, ch20 (WWCTV items 1, 4), ch21, ch41–43.

**Failure mode if false:** Proxy preservation instead of values; cheap readout from supplied bundle coordinates but no tractable way to discover the right coordinates. **Lean:** MB2, MB3. **Bears on:** C-004 · **U-01, U-02**

### A-002 — Correction channels as causal chains

**Assumption:** Handle-controlled correction pathways with measurable \(\mathrm{CCI}\), evaluated only when the correcting agent or institution has independently controlled, not-captured handles into the target system.

**Also stated in:** ch25–27, ch34, ch20 (WWCTV item 5), ch40.

**Failure mode if false:** Corrigibility theater; capture; CCI reads high after the target has reshaped the human reference process. **Lean:** MB4, MB8 plus correction-path `notCaptured` condition. **Bears on:** C-005 · **U-03, U-07**

### A-003 — Societal correction capacity

**Assumption:** \(C_{\text{corr}}^{\text{society}}(t_0) > \theta\).

**Canonical:** ch05 §Correction-Capacity Assumption. **Not an MB axiom.** **Bears on:** C-002, C-005, C-007 · **U-15**

### A-004 — Discoverable boundaries

**Assumption:** Boundaries discoverable under approximate observability and adversarial limits.

**Also stated in:** ch05, ch09–10, ch36, ch38. **Lean:** MB1, MB7a–b. **Bears on:** C-001, C-003 · **U-05**

### A-005 — Certifiable deployment and human agency

**Assumption:** Deployment can be gated by certification; humans can refuse, revise, coordinate.

**Also stated in:** ch05, ch31–32, ch35. **Lean:** MB6. **Bears on:** C-006, C-007 · **U-11, U-15**

### A-006 — Compression / transport inferability

**Assumption:** Intentional and transport models earn compression gain after complexity cost; ch20 items 2–3 (bundle/bearer inferability).

**Canonical:** ch21. **Lean:** S07, MB2. **Bears on:** C-009 · **U-09**

### A-007 — Successor channel auditability

**Assumption:** Successor influence passes through specifiable, auditable channels (seven conserved properties, ch29).

**Also stated in:** ch08, ch29–31. **Lean:** MB5. **Bears on:** C-006 · **U-04, U-13**

### A-008 — Selection environment

**Assumption:** Outcomes depend on socio-technical selection (fitness, basins), not weights alone.

**Also stated in:** ch02 loop, ch35, ch40. **Lean:** MB6. **Bears on:** C-007 · **U-10, U-11**

### A-009 — Adversarial verifiability

**Assumption:** At least one core measurand is cheaper to satisfy honestly than to fake under optimization pressure.

**Also stated in:** ch36, ch39–39b, ch40. **Lean:** MB7b, MB7c. **Bears on:** C-005, C-010, C-044 · **U-03, U-14**

### A-010 — Dynamical guarantees

**Assumption:** Alignment expressed as certified-class / basin invariants over time, not static \(P(A_t)\).

**Also stated in:** ch31, ch39. **Lean:** certification scaffolding + MB5–6. **Bears on:** C-002, C-006, C-044 · **U-04, U-13**

### A-011 — Civilizational-frame minimum assumptions

**Assumption:** (1) AI mediates high-effect decisions; (2) institutions/markets select deployment patterns; (3) mediation changes correction-relevant information; (4) human values/institutions are plastic.

**Canonical:** ch02 §Minimum Assumptions. Stronger claims deferred to later chapters. **Bears on:** C-001, C-007

### A-012 — Correction co-scaling

**Assumption:** Correction, oversight, and interpretability can co-scale with capability across real jumps (Part III hinge); otherwise only pause/stop remains.

**Canonical:** ch14 WWCTV load-bearing bullet. **Bears on:** C-008 · **U-06**

---

## II. Lean scaffolding

Abstract carriers in `Core.lean` (`System`, `State`, …) are mathematical interfaces, not empirical assumptions. Criticize **A*** and **MB***, not `System : Type`.

---

## III. Lean imported (S01–S09)

Appendix I §Imported Assumptions. Only **S07** is an explicit Lean `axiom`. S09 enters via MB6.

---

## IV. Lean bridges (MB1–MB8)

Formal statements: Appendix I; validation program: Appendix H. Lean: `Core.lean` `BridgeAssumptions`.

| Bridge | Manuscript A-IDs |
|--------|------------------|
| MB1 | A-004 |
| MB2, MB3 | A-001, A-006 |
| MB4, MB8 | A-002 |
| MB5 | A-007, A-010 |
| MB6 | A-005, A-008, A-011 (institutional selection) |
| MB7a | A-004 |
| MB7b, MB7c | A-009 |
| MB8 | A-002 |

---

## Appendix index

Tables below are parsed into `metadata/assumptions-index.tex` for Appendix E. One line per assumption; full context in the cited chapter.

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
| A-006 | Intentional and transport models earn compression gain after complexity cost (MDL / $\Delta L$) | ch21 |

### Correction, capability, and verification

| ID | Assumption | Home |
|----|------------|------|
| A-002 | Correction is a handle-controlled causal chain with measurable integrity ($\mathrm{CCI}$) | ch24 |
| A-012 | Correction-relevant capacity co-scales with capability across real jumps (else pause/stop) | ch14 |
| A-009 | At least one safety-relevant measurand is adversarially verifiable under optimization pressure | ch39b |

### Successors, dynamics, and selection

| ID | Assumption | Home |
|----|------------|------|
| A-010 | Alignment is a dynamical guarantee over a certified class / basin, not a static property | ch03 |
| A-007 | Successor influence passes through specifiable, auditable channels | ch28 |
| A-008 | Alignment outcomes depend on socio-technical selection, not model weights alone | ch32 |

### Lean conventions and bridges

| ID | Assumption | Home |
|----|------------|------|
| S07 | Positive description-length gain $\Rightarrow$ preferred model (MDL ordering) | ch21 |
| MB1 | $\epsilon$-boundary certificates imply genuine boundary separation | ch07 |
| MB2 | Bundle-gradient equivalence implies bundle alignment | ch16 |
| MB3 | Bundle transport plus bearer-map agreement implies bearer transport | ch18 |
| MB4 | Correction-channel integrity implies legitimate correction-operator preservation | ch25 |
| MB5 | Full transport plus bearer transport implies successor safety | ch28 |
| MB6 | Socio-technical basin stability implies correction-channel integrity | ch35 |
| MB7a | Boundary alignment plus adequate access model implies access robustness | ch07 |
| MB7b | Access robustness plus filter coverage bounds hidden productive B-IQ | ch39b |
| MB7c | Correction integrity plus bounded hidden B-IQ implies adversarial robustness | ch39b |
| MB8 | Preserving the human value-update operator $U_H$ implies correction integrity | ch26 |

---

## Maintenance

When a chapter introduces a **new load-bearing assumption**, add a row to the Appendix index (and §I notes), then regenerate Appendix E.

Do not duplicate the Executive Overview or a front-matter list; point readers to chapters + Appendix E.
