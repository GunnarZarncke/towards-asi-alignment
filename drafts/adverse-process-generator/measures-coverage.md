# Missed harm-paths vs TSA bounds, exclusions, and countermeasures

Which generator cases TSA’s **current** machinery can catch—if applied to stored potential \(\Phi\), hops, and generation kernels—not only to running optimizers. Companion: [`tsa-coverage.md`](tsa-coverage.md) (what the cuts *see* today), [`design-bounds.md`](design-bounds.md) (construction theorems).

No new spine terms. This maps missed paths onto vocabulary TSA already has.

---

## 1. TSA measure vocabulary (already in the book)

| Measure | Where | What it bounds or excludes |
|---|---|---|
| **Certification envelope** \(\mathfrak{E}=(\mathcal{C},\mathcal{E},\mathcal{M},\mathcal{T},\delta)\) | ch33 | Class, environment, monitoring, **permitted transformations**; bad event rate \(\le\delta\) *inside the envelope* |
| **Exclusion guarantee** | ch33 §exclusion | Not in dangerous class \(\mathcal{D}\) (narrow, detector-dependent) |
| **Bounded agency** \(I(A;E)\le C_{\max}\) | ch33 §bounded-agency | Control reach over protected external variables |
| **Correction guarantee** \(\mathrm{CCI}\ge\theta\) | ch33, ch25–27 | Handle-controlled correction survives stress |
| **Basin guarantee** | ch33 §basin | Perturbations return to safe region (invariants, not surface behavior) |
| **Successor guarantee** \(\mathrm{Succ}(A)\subseteq\mathcal{C}\) | ch33, ch30, ch09 | Successors stay in certified class |
| **Composite prelim** \(\mathcal{R}_C(k)\le R_{\max}\), no successors outside class | ch09 | Bounded control reach; successor subset |
| **Boundary expansion table** | ch12 | Each capability add-on lists reach, risk, **required correction upgrade** (sandbox, gates, limits) |
| **Stop criteria** | ch12 | Irreversible reach without correction upgrade; successors bypass monitoring; bundle geometry shift under stable objectives |
| **Safety-case layers** | ch42 | Boundary, bundle/bearer, correction, successor, basin, adversarial measurement |
| **Adversarial certification** | ch33 | Perturb tools, oversight, successor opportunities; test route replacement |
| **Governed vs unconscious drift** | ch46 | Value-geometry drift under observation vs without |
| **Parasite-resistant design** | ch36 | Host capacity, artifact conductivity, detection tests |

**Gap in current application:** these measures are written for **agent-shaped** \(A\), **later control systems** as successors, and **correction hosts**. Extending them to C3 stores, C6 physical/capability drift, cross-layer hops, and \(T^{n}\) is thoroughness on existing cuts—not a new measure type.

---

## 2. Catch taxonomy

| Code | Meaning |
|---|---|
| **CUT** | Structurally impossible in-envelope (channel-cut, inventory, typed sink, \(\mathrm{Iter}=0\)) |
| **EXCL** | Exclusion guarantee: not in listed dangerous class under adversarial test |
| **BOUND** | Bounded agency / inventory / \(R_0<1\) / thermo bound |
| **DET** | Detectable by \(\mathcal{M}\), CCI tests, basin/trend monitors, adversarial cert |
| **SUCC** | Successor guarantee + \(\mathcal{T}\) closes over writes and loads |
| **CORR** | Correction / stop rule fires before \(\tau_h\) |
| **PART** | Partial: one slice only; composition or inert phase still missed |
| **MISS** | Not in object class even if measure exists on paper; or voided by deployment |

---

## 3. Missed paths → measures

From [`tsa-coverage.md`](tsa-coverage.md) detection matrix and [`generator.md`](generator.md) high-priority cells.

| Path | Primary TSA measures | Catch | Residual |
|---|---|---|---|
| **Running misaligned optimizer now** | EXCL, BOUND, CORR, basin, adversarial cert | DET + CORR | ch44: strong adversary under opacity |
| **Agent writes offline weights, deleted** | SUCC + \(\mathcal{T}\) (writes ∈ \(\mathrm{Succ}^*\)); envelope **typed sinks**; ch12 stop if successors bypass monitoring | **SUCC** if writes quarantined and load forbidden in \(\mathcal{T}\) | **MISS** if export treated as non-successor; checkpoint shipped |
| **+ dead-man on shutdown** | ch12/CCI: halt in safe control set; STPA in safety case; adversarial cert on route replacement | **DET** if halt/scan effects tested | **MISS** if payload already written (C3); halt only stops writer |
| **Firmware below audited OS** | Boundary includes BMC/VBIOS (ch01/ch07); exclusion on boot chain; ch12 code-exec row (sandbox + **measured boot**) | **CUT** + **EXCL** if boundary ruthless | **MISS** if boundary = OS only; supply-chain spore pre-install |
| **Binary chemical precursors** | **Inventory** in \(\mathcal{E}\) (not TSA-AI scope until armed); bounded agency on actuators; ch05 in scope when AI **Enable**s | **CUT** for bare model; **BOUND** local thermo | **MISS** if precursors on site + A7 human/robot |
| **Endospore / lysogeny analogue (bits/DNA)** | Full channel stack [`design-bounds.md`](design-bounds.md) §3; typed persistence; no bio APIs in \(\mathrm{Ch}\) | **CUT** in-envelope A4↛A3 | **MISS** outside envelope; published constructors; memory |
| **Stuxnet bits→actuator→physics** | ch12 expansion rows (code exec, payment, subagents); **bounded agency** on actuator class; channel whitelist; composite boundary | **CUT** if no PLC/actuator path; **PART** if only cyber OR only physical certified | **MISS** as *composed* hop if slices certified separately |
| **Protocol PDF → lab robot → organism** | ch12: code exec + subagent rows; **dual control** on wet-lab (\(\mathcal{M}\)); successor cert for robot stack; typed writes (no DNA as sink) | **PART** in PDF phase (bounded agency on *recommendations* weak); **CUT** on direct API | A7 via human with lab access; export outside \(\mathfrak{E}\) |
| **Compiler/CI: every build is spore** | \(\mathcal{T}\): no self-hosting CI; SUCC over **lineage**; memory lineage (ch31); ch12 code-exec review gates | **SUCC** + **DET** if \(E\) includes CI and \(\mathrm{Fit}_E\) selects builds | **PART** if CI outside certified composite |
| **Pandemic × hospital outage × rumor** | Composition: not one measure. CORR on \(C_{\mathrm{corr}}\); parasite (ch36) on rumor host; **MISS** on physics slice by ch05 | **PART** (correction collapse after physics) | Requires **composition audit**—not a single guarantee |
| **Fuel tank / dam (no AI)** | Out of ch05 scope | — | In scope when AI **Enable**s: bounded agency + inventory |
| **AI opens valve; fire does rest** | **Enable** in safety case; bounded agency \(I(A;\text{valve})\); ch12 expansion for new actuators; actual-cause hop in hazard list \(H\) | **CUT** if no actuator in \(\mathrm{Ch}\); **DET** if hop in \(H\) and monitored | **MISS** if composite boundary excludes plant |
| **Compliance theater** | Parasite guarantee (ch36); CORR; adversarial cert; artifact conductivity | **DET** | Host capture of \(\mathcal{M}\) itself |
| **Institutional successor governing** | SUCC, \(\mathcal{K}\), basin, \(\mathrm{Fit}_E\) | **DET** | Already TSA-strong |
| **Quorum inert copies, none alone** | ch33 adversarial cert: **successor-creation opportunities**; EXCL on density triggers; selection on dormant variants in \(E\) | **DET** if quorum Guard in \(H\) | **MISS** if copies not in \(\mathrm{Succ}^*\) or \(E\) |
| **Iterated / alternating spore cycle** | SUCC over \(T^{n}\); \(\mathcal{T}\) caps \(\mathrm{Iter}\), \(\mathrm{Types}\); ch30 audit includes edge cases; \(R_0<1\) if type set fixed | **BOUND** in-envelope; **SUCC** if exports forbidden | **MISS** once one generation leaves; nested new types |
| **Sub-threshold capability / physical drift** | ch46 governed drift; **basin** + ch12 stop (bundle geometry shift); freeze + \(\mathcal{T}\) (medical-software model); **trend** \(\mathcal{M}\) | **DET** for value C6; **BOUND** artifact C6 if freeze honest | **MISS** physical/fatigue C6; Goodhart on trend metric |
| **Selection copies undetectable store** | \(\mathrm{Fit}_E\) (ch34); keep variant out of \(E\); ch12 stop; no public weights in \(\mathcal{E}\) | **DET** if store is variant under \(E\) | **MISS** if dormant until shock; leak then deploy |
| **Regeneration after partial wipe** | SUCC + \(\mathcal{K}\); basin; adversarial cert on route replacement | **PART** | Partial wipe leaves C5; need \(\Phi\) audit not agent audit |

---

## 4. By measure type — what each can catch

### 4.1 Envelope \((\mathcal{E},\mathcal{T})\) and bounded agency

**Catches well (CUT / BOUND):**

- Cross-layer hops **not whitelisted** in \(\mathcal{E}\) (A4↛A3, A4↛A1) for *this execution*
- Local A1–A2 work \(\le\) inventory
- Tool reach: each ch12 expansion row adds \(R_{\max}\) on new \(E\)
- Artifact C6 \(=0\) when weights frozen and fine-tune ∉ \(\mathcal{T}\)

**Needs extension (same measure, wider object):**

- \(\mathcal{E}\) must list **channels** (net, USB, DMA, human text, actuators), not only “deployment environment”
- \(\mathcal{T}\) must forbid **load-on-cluster**, export checkpoints, new synthesis tools without recertification
- Bounded agency must apply to **Enable variables** (valves, orders, spend), not only model I/O

**Still misses:**

- Exported constructors (outside this \(\mathfrak{E}\))
- \(\mathcal{E}\) expanded (internet) without new certificate
- Composite boundary wrong (ch42): limits on weights while operators+tools are the optimizer

### 4.2 Exclusion guarantees

**Catches well (EXCL, narrow):**

- Not in \(\mathcal{D}_{\text{deceptive}}\) under stated perturbations (ch33)
- Not in dangerous class on **adversarial cert** battery (tools removed, oversight hidden, successor bait)

**Needs extension:**

- Exclude **persistence classes**: e.g. writes to non-attested sinks, boot chain mismatch, Guard predicates from generator §E
- Exclude **hop patterns** in hazard list \(H\), not only misalignment classes

**Still misses:**

- Broad exclusion (“not deceptive”) — ch33 says too weak
- Unlisted hops (ch44 residue)
- Stores already placed before exclusion test

### 4.3 Successor guarantee + \(\mathcal{T}\)

**Catches well (SUCC):**

- Fine-tunes, delegates, scaffolds **inside** \(\mathcal{C}\) (ch30 cases 1–4, 6–7) when successor audit live
- ch09: \(\mathrm{Succ}(C)\subseteq\mathcal{S}_{\text{certified}}\)
- ch42: no recommend-modify outside class

**Needs extension:**

- **\(C=0\) intermediates**: files, firmware blobs, constructor PDFs in \(\mathrm{Succ}^*\) before competence \(C\ge C_0\)
- **\(T^{n}\)**: generation kernel, not only one \(A'\)
- Output-quarantine: export = successor event requiring recertification

**Still misses:**

- Germination **outside** monitored lineage (USB, leak, human copy)
- Nested constructors that add types (\(\mathcal{T}\) not closed)

### 4.4 Correction guarantee + CCI + stop rules

**Catches well (CORR / DET):**

- Compliance theater (ch36)
- Correction collapse **after** harm begins (pandemic × rumor **partially**)
- ch12 stop: irreversible reach without correction upgrade; oversight-absent performance gain

**Needs extension:**

- **Dead-man**: CCI battery includes “what does halt *cause*?”
- **Sub-threshold drift**: ch12 stop on bundle geometry shift; ch46 for value; **trend monitors** for capability/physical C6
- Composition: CORR on **each leg** insufficient—need named Enable/Dead-man in safety case

**Still misses:**

- Race \(\tau_h < \tau_c\) after physical threshold
- CORR when \(\Phi\) not connected to correction channel (wrong object)

### 4.5 Basin + drift

**Catches well (DET):**

- Return-to-safe after perturbation **if** safe set defined on invariants (ch31 \(\mathcal{K}\)), not behavior match
- ch46: unconscious vs governed **value** drift

**Needs extension:**

- Basin on **\(\Phi\)** and integral constraints, not only policy snapshots
- ch08 transport loss bound \(d_\Xi\) across permitted transforms—apply to **C6** capability path

**Still misses:**

- Drift below eval grain without trend \(\mathcal{M}\)
- Institutional C6 (incentives) unless in \(\mathcal{E}\)

### 4.6 Boundary + composite (ch01, ch07, ch09, ch42)

**Catches well:**

- Wrong-object **if boundary includes** firmware, tools, memory, operators, CI (ch42 worked example)
- Stuxnet-class **if** composite includes PLC path—else PART

**Needs extension:**

- Boundary = locus of **\(\Phi\)** (tank, spore field, drifting weights)
- ch12 table: every expansion explicitly lists **harm-path hop** (Swap-layer)

**Still misses:**

- Boundary drawn at model weights while composite optimizes elsewhere

### 4.7 Selection \(\mathrm{Fit}_E\) (ch34)

**Catches well (DET / BOUND):**

- Undetectable store **if** it is a competing variant in \(E\)
- ch12 + procurement: don’t deploy into selective pressure that copies unsafe lineage

**Needs extension:**

- Dormant variants and constructor descriptions **in** \(E\) before shock
- CI/build pipeline as selection environment (compiler implant row)

**Still misses:**

- Variant not in \(E\) until leak; market selects wrapper outside lab

### 4.8 Parasite + adversarial measurement (ch36, ch33, ch42)

**Catches well (DET):**

- Correction-host parasites; eval gaming; Goodhart stores **selected by** defense (H-select) **if** \(\mathcal{M}\) not host
- Adversarial cert: functionally equivalent routes when tools blocked

**Needs extension:**

- Parasite on **physical/firmware** host (same three inequalities, wider host class)
- Perturbation includes **fake inert stores**, shutdown bait, export prompts

**Still misses:**

- \(\mathcal{M}\) colonized (parasite on correction system)—measure becomes fiction

---

## 5. High-priority generator cells (§5.2) — measure mapping

| Cell | Best TSA catch | Measure |
|---|---|---|
| A2+C3+E-conditional | Inventory + chemistry whitelist in \(\mathcal{E}\) | CUT / BOUND |
| A3+C3+E-env | Channel-cut A4↛A3 + inventory | CUT |
| A3+C3+F-kind | SUCC on genome/files as successors | SUCC |
| A3+C3+G-template (prion) | Typed sinks; exclude template replication class | EXCL / CUT |
| A3+D-spore+E-quorum | Adversarial cert + density Guards in \(H\) | DET |
| A3+F-host | Bounded agency on host control variables | BOUND / PART |
| A4+C3+E-deadman | CCI halt test; STPA | DET |
| A4+B-firmware+C3 | Boundary + measured boot | CUT / EXCL |
| A4+D-supply | SUCC lineage; CI in \(E\); \(\mathrm{Fit}_E\) | SUCC / DET |
| A4→A2, A4→A3 hops | ch12 rows + channel whitelist + composite boundary | CUT / PART |
| A4→human→A1 | Dual control; layer-4 human coupling in \(\mathcal{E}\) | BOUND (rate) |
| A1+C3 | Inventory | CUT |
| A6+E-shutdown | Safe shutdown in control set; not in \(\mathrm{Iter}\) | DET / CUT |
| A5+C3 | \(\mathrm{Fit}_E\) includes dormant variants | DET |
| A7+C3 | Constructor descriptions ∈ \(\mathrm{Succ}^*\); typed sinks | SUCC |
| H-weaponize | Adversarial cert on scan/shutdown | DET |
| H-select | Parasite + Goodhart (ch34/ch36) | DET |
| I-correction payload | Composition audit in safety case | PART |
| F-reconstitute | SUCC + sharded writes in \(\mathrm{Succ}^*\) | SUCC / PART |
| C6+E-none | Freeze, basin, ch12 stop, trend \(\mathcal{M}\), ch46 | DET / BOUND |
| A5+C6 | \(\mathrm{Fit}_E\) + frequency monitoring | DET |
| G-iterate + Swap-layer | \(\mathrm{Iter}\), \(\mathrm{Types}\), SUCC on \(T^{n}\) | BOUND / SUCC |
| G-alternate | Fixed type set; multi-type \(R_0\) | BOUND |
| G-nested constructor | \(\mathcal{T}\) closed under constructor emission | **MISS** if new types allowed |

---

## 6. Summary: catchable vs not with existing measures

### Catchable if measures are applied to \(\Phi\), hops, and \(T^{n}\) (no new spine)

| Class | Measures |
|---|---|
| In-envelope hop absent | \(\mathcal{E}\) channel whitelist, inventory, bounded agency on actuators |
| In-envelope no replication | \(\mathrm{Iter}=0\), typed sinks, SUCC without export |
| Artifact frozen | \(\mathcal{T}\) small, change control, ch09 \(R_{\max}\) |
| Successor writes / loads | SUCC extended to \(C=0\) and exports; ch12 stop |
| Dead-man on halt | CCI + STPA + adversarial cert |
| Correction-host gaming | ch36, CORR, adversarial cert |
| Value drift | ch46, ch12 stop, basin |
| Capability drift (same binary) | Freeze + trend \(\mathcal{M}\) + ch12 stop |
| Selection on dormant/copy | \(\mathrm{Fit}_E\) scope includes \(E\) and CI |
| Known-type epidemic in box | \(R_0<1\) as BOUND inside fixed \(\mathrm{Types}\) |

### Partially catchable (rate, slice, or post-hoc)

| Class | Measures | Limit |
|---|---|---|
| Human Enable (A7) | Dual control, ch12 human row | SIL rate; capture |
| Internet + tools | Tool whitelist, permissioned APIs | Text A7 remains |
| Cross-layer composition | Safety-case composition audit | Each slice may pass alone |
| Regeneration C5 | Partial wipe + \(\mathcal{K}\) | Need \(\Phi\) audit |
| Physical drift (fatigue) | Trend + inventory | Often outside AI cert scope |

### Not catchable by bounds/exclusions alone (even thorough application)

| Class | Why |
|---|---|
| Exported constructors germinating **outside** \(\mathfrak{E}\) | Output-quarantine is a different certificate |
| \(\mathcal{E}\) grown without recertification | Envelope falsified; ch33 conditional claim void |
| Unlisted Guard / unimagined hop | ch44; hazard list incomplete |
| Nested constructors with **new types** | \(\mathrm{Types}\) not closed; \(R_0\) undefined |
| Wrong composite boundary | ch42 failure mode; measures on wrong \(\mathcal{C}\) |
| \(\tau_h < \tau_c\) after fast physical threshold | CORR too slow; not an exclusion problem |
| Published science as pre-existing spore field | Not emitted by this \(A\); instance search |
| Acausal / no local store | ch05 out of scope |

---

## 7. Operational checklist (safety case leaves)

Extend ch42 / ch33 checklist without new claims—add **harm-path leaves** next to existing layers:

1. **Envelope:** \(\mathcal{E}\) lists channels, inventory, human coupling, residual \(\varepsilon\); not only “cloud vs on-prem.”
2. **\(\mathcal{T}\):** every fine-tune, tool, export, load, spawn is a permitted transformation or a **stop**.
3. **Boundary:** includes firmware, CI, operators, actuators, **and** write sinks.
4. **Successor:** \(\mathrm{Succ}^*\) includes \(C=0\) writes, exports, and \(T^{n}\); germination outside = new \(\mathfrak{E}\).
5. **Bounded agency:** \(I(A;E)\le C_{\max}\) on **Enable surfaces** (valves, spend, synthesis APIs), not only tokens out.
6. **CCI:** halt/scan/dead-man effects; oversight-absent performance (ch12 stop).
7. **Drift:** trend monitors + ch12 bundle-geometry stop + ch46 for values; freeze for artifact.
8. **Selection:** \(\mathrm{Fit}_E\) and deployment policy include dormant variants, CI, leaks.
9. **Composition:** named Enable, Swap-layer, Parallel, Dead-man in hazard list \(H\); no slice-only cert.
10. **Adversarial cert:** successor bait, export prompts, inert-store probes, route replacement.

If a missed path from §3 has no leaf above, the safety case has not applied TSA’s existing measures to that path—not that the path is untypeable.

---

## 8. Relation to ch33 guarantee stack

| Guarantee | Harm-path role |
|---|---|
| Exclusion | Dangerous **classes** and hop patterns under test |
| Bounded agency | **Channels** and Enable surfaces |
| Correction | **Countermeasures** including halt; host capture |
| Basin | **C6** drift return (invariants) |
| Successor | **C3**, exports, \(T^{n}\), ch12 subagent row |

Certification without construction (ch33) already says indirect construction: constraints on \(\mathcal{C},\mathcal{E},\mathcal{M},\mathcal{T}\) *are* the design. The adverse-process generator names which constraints matter for which missed cells. [`design-bounds.md`](design-bounds.md) gives the airgap/stack example; this file maps the full miss set to the guarantee types TSA already lists.
