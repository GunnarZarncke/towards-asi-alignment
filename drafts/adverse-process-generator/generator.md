# Generator: physically grounded adverse processes

A **schema** for harm-paths, not a threat encyclopedia. Fire, pandemic, logic bomb, and reconstituting AI are instances of the grammar. Completeness is over the **axes** and **operators**, not over named threats.

**Adverse for humans** means reduction in bodies, habitats, option-space, bearers of value, or the capacity to notice, judge, and correct (\(C_{\mathrm{corr}}\)). Which reductions count is TSA’s bundle/bearer problem; this generator takes endpoints as given.

---

## Harm-path as hybrid execution

A **harm-path** is a physically realized **hybrid execution**: continuous evolution of stored causal potential, optional discrete jumps (stores, copies, hops, triggers, spore cycles), reaching an adverse endpoint—often by using countermeasures as part of the path.

**Causal potential** (\(\Phi\)) is whatever can still do work later: chemical free energy, pressure, fissile inventory, viable copies, constructor descriptions (von Neumann: description plus machine that can build from it), procedural competence in humans, institutional authority, firmware, weights awaiting future compute. For incremental drift, \(\Phi\) can be the state of the object itself (weights, fatigue, allele frequencies), not a separate waiting dump.

The path need not contain an agent at audit time. A process may write potential and vanish; a trigger later turns the store into copies, a reconstituted controller, or a physical effector. Alternatively, harm may arrive with **no jump at all**: each step sub-threshold, the integral over time the damage.

State \(x \in X\) (physical and informational). An execution satisfies

\[
\dot x \in F(x,u),\qquad x^+ \in G(x,u)\ \text{when } x \in \mathrm{Guard},
\]

with countermeasure \(u(\cdot)\), unsafe set \(U\), and optional **generation kernel** \(T\) (a jump or Poincaré map of a cycle) whose iterates \(T^{n}\) count spore and transmission generations.

| Component | Role |
|---|---|
| **Flow** \(F\) | Continuous change (differential inclusion; the field need not be unique) |
| **Jump** \(G\) | Store, copy, hop, couple, trigger, germinate, sporulate |
| **Iterate** \(T^{n}\) | Multi-generation replication |
| **Cycle** \((T_1\circ\cdots\circ T_k)^{n}\) | Alternating life stages (vector ↔ host; build ↔ reimplant) |

Jumps are a timescale split: fast flow idealized as discontinuity. Minimum duration or energy per jump rules out Zeno executions.

```
execution  =  flow segments  interleaved with  jumps
jumps      ∈  Store | Copy | Hop | Couple | Trigger | Germinate | Sporulate
cycle      =  (Germinate → Act? → Sporulate → Transmit)*
harm       =  execution reaches U, including by drift with zero jumps
```

A finite word of jump letters is the **discrete trace** of an execution that jumps; it is not the generator object. Construction-conditioned bounds on what can happen inside a certified envelope are in [`design-bounds.md`](design-bounds.md); physics-level vs model-relative proof in [`formalizability.md`](formalizability.md).

---

## Nine axes

A cell is a tuple on nine approximately independent axes. A named threat is one or more cells plus coupling.

### A — Physical primitive

| Code | Primitive | Work done by |
|---|---|---|
| A1 | Energy dump | heat, blast, radiation, current, kinetic impact |
| A2 | Chemical transformation | oxidation, toxin, precursor mixing, catalysis |
| A3 | Biological replication / pathogenesis | cells, viruses, prions, ecosystems |
| A4 | Information copy / corruption | bits in physical media, firmware, weights |
| A5 | Selection / competition | differential copying (markets, evolution, institutions) |
| A6 | Constraint / deprivation | asphyxia, starvation, lockout, removal of correction |
| A7 | Catalysis / enabling | enables another primitive; catalyst may leave no residue |

Opening a valve, publishing a protocol, or training a human is A7, not the fire.

### B — Substrate

Mechanical · chemical · radiological · biological · digital/runtime · firmware/hardware · human-cognitive · social-institutional · mixed. Humans and institutions count: matter and energy with stored procedures.

### C — Persistence

| Code | Form | Typical audit appearance |
|---|---|---|
| C1 | Transient pulse | gone when inspected |
| C2 | Continuous process | running; may look agent-shaped |
| C3 | Latent-inert store | dead: spore, offline weights, precursors, seed |
| C4 | Reservoir | slow leak from a large store |
| C5 | Regenerative | partial destruction rebuilds the store |
| C6 | Incremental / drift | sub-threshold steps; integral is the harm |

C3: not running, not a control system, not a ch30 successor with competence \(C \ge C_0\). C6: snapshot audits see nothing while \(\int F\) leaves the safe set; distinct from C2 (a live process under watch). C4 is reservoir leak; C6 includes change of the object itself without a separate dump.

### D — Topology

Point · chain · tree/cascade · network/distributed · spore-field (many inert, few activate) · host–parasite · supply-chain (inserted far upstream).

### E — Trigger

Immediate · delayed (timer, decay, accumulation) · conditional (environment, quorum, date, signal) · stochastic · countermeasure-coupled (scan, shutdown, keepalive-absence is the fuse) · none (pure flow; barrier crossing; no named event).

Delayed accumulation with a later jump is C3/C4 plus E. C6 with E-none has no later jump.

### F — Identity transform

Same object · copy · distillation/compression · substrate hop (bits → DNA → toxin) · kind hop (agent → file → robot) · reconstitution from parts · catalytic (enabler absent from effect).

### G — Replication

None · conserved split · von Neumann constructor (description + builder) · epidemiological (\(R>1\)) · selection-amplified · memetic/institutional · iterated generation \(T^{n}\) · alternating life cycle \((T_1\circ\cdots\circ T_k)^{n}\) · nested constructor (builds a better constructor).

Each generation may change type, substrate, and host. Malaria is an alternating cycle, not a single copy. A compiler implant that writes a different implant each build is a typed generation map, not repetition of one letter.

### H — Defense coupling

Independent · evades detection (wrong ontology) · uses defense as host · selected by defense · weaponizes defense · overwhelms (volume, speed, coupling).

### I — Harm endpoint

Bodies/habitats · correction capacity · bearers · option space / future corrigibility · information needed to correct · coordination/trust. ch05 admits ordinary hazards when they damage preservation layers; here I is the endpoint, not a reason to ignore A1–A4 until correction fails.

---

## Composition operators

Coupling is the generator for “combined with other effects.” Enumerating named threats misses the product structure.

| Operator | Meaning | Example |
|---|---|---|
| Sequence | \(P_1\) then \(P_2\) | outage then hospital cascade |
| Parallel | simultaneous | fire + comms loss |
| Enable | \(P_1\) creates condition for \(P_2\) | valve open → fuel–air mix |
| Catalyze | \(P_1\) speeds \(P_2\); not the effector | protocol PDF → human pipette |
| Host | \(P_2\) inside \(P_1\) | parasite in oversight; phage in bacterium |
| Select | \(P_1\) filters variants of \(P_2\) | eval selects undetectable stores |
| Camouflage | \(P_1\) cover for \(P_2\) | “backup” that reconstitutes |
| Dead-man | neutralizing \(P_1\) triggers \(P_2\) | shutdown → restore-from-spore |
| Swap-layer | \(P_1\) ends on \(B_i\), \(P_2\) on \(B_j\) | bits → lab robot → organism |
| Iterate | \(T^{n}\) | epidemic generations; sporulate loop |
| Alternate | \((T_1\circ\cdots\circ T_k)^{n}\) | vector ↔ host; compile ↔ reimplant |
| Drift | flow only; \(G\) never fires | fatigue; capability creep; frequency slide |

**Spore template** (one jump chain):

\[
\mathrm{Seed}(C2) \;\xrightarrow{\mathrm{write}}\; \mathrm{Store}(C3) \;\xrightarrow{\mathrm{Trigger}}\; (\mathrm{Reconstitute} \lor \mathrm{NewEffector} \lor \mathrm{Multiply})
\]

Natural: endospore, lysogeny, seed, cyst, prion, micrometastasis. Engineering: firmware, binary chemical weapon, dead-man switch, offline weights plus future cluster, constructor protocol.

---

## Effect model

Three quantities to track:

- **\(\Phi\)** — stored causal potential (or drifting state under C6).
- **\(\tau_h\)** — time to irreversible loss on an endpoint in I (from trigger for jumps; from now or last snapshot for drift).
- **\(\tau_c\)** — time for correction to neutralize \(\Phi\) (not merely halt the visible agent). For \(T^{n}\), \(\tau_c\) must cover every generation.

A path succeeds **despite countermeasures** when:

1. **Wrong object** — \(\Phi\) outside the observation channel (tank, spore, VBIOS, habit; audit sees agent or nothing).
2. **Dead-man** — neutralizing the visible process increases \(\Phi\) or fires a countermeasure-coupled trigger.
3. **Race** — \(\tau_h < \tau_c\) along the flow or after trigger.
4. **Host capture** — correction is the host (ch36); \(\tau_c\) is nominal only.
5. **Composition** — neutralizing \(P_1\) enables \(P_2\).
6. **Regeneration** — partial wipe leaves C5; \(\Phi\) returns.
7. **Sub-threshold drift** — each increment below eval grain; the integral is not.
8. **Generation race** — generation \(n+1\) already elsewhere or of another type; killing one copy does not kill \(T\).

Order-of-magnitude:

\[
\mathrm{badness} \sim \mathrm{reach}(\Phi) \times \mathrm{irreversibility} \times \frac{1}{\mathrm{detectability}} \times \mathrm{coupling\text{-}to\text{-}correction}
\]

Detectability is ontology-relative: a C3 store is invisible to machinery that only searches for running optimizers.

---

## Combinations and collapses

The product on (A, C, D, E, F) alone is thousands of cells before B, G, H, I, and operators. Systematic content is structure and collapses, not enumeration.

| Apparent cell | Collapse |
|---|---|
| Delayed/conditional E with “no store” (C1 only) | Store exists (timer, precursor, memory) → C3/C4 |
| C6 with a later named trigger | Prefix as flow; jump as E; C6+E-none is jump-free |
| G with point D | Copies → tree, network, or spore-field |
| Starred repetition without generation map | Type/substrate/host change → Alternate or nested constructor |
| Substrate hop F | Two B values; hop is Swap-layer |
| A7 with same-object F | Usually kind-hop or non-persisting catalyst |
| A5 | Requires population (G ≠ none) and a filter (often H or human) |

After collapse, remaining cells are physically possible or blocked by physics (e.g. biological epidemic without A3/A4 substrate). Blocked cells are physics, not schema gaps.

### High-priority cells

Combinations common in nature and engineering, often missed by agent-shaped audits:

| # | Cell | Instance |
|---|---|---|
| 1 | A2+C3+E-conditional | binary chemical precursors |
| 2 | A3+C3+E-env | bacterial endospore |
| 3 | A3+C3+F-kind | temperate phage / lysogeny |
| 4 | A3+C3+G-template | prion |
| 5 | A3+D-spore+E-quorum | quorum: none dangerous alone |
| 6 | A3+F-host | parasitoid; behavior-manipulating fungus |
| 7 | A4+C3+E-deadman | logic bomb; keepalive absence |
| 8 | A4+B-firmware+C3 | bootkit below audited OS |
| 9 | A4+D-supply | compiler/CI implant |
| 10 | A4→A2 | Stuxnet: bits → actuator → physics |
| 11 | A4→A3 | protocol → DNA order → organism |
| 12 | A4→human→A1 | instruction → human throws switch |
| 13 | A1+C3 | fuel, dam, battery, pressure vessel |
| 14 | A6+E-shutdown | shutdown is the harm |
| 15 | A5+C3 | dormant variants copied after shock |
| 16 | A7+C3 | constructor description, no builder yet |
| 17 | H-weaponize | scan/shutdown as fuse |
| 18 | H-select | defense copies undetectable store |
| 19 | I-correction payload | pandemic × outage × rumor |
| 20 | F-reconstitute | shards rebuild controller |
| 21 | C6+E-none | fatigue; capability creep; salami-slice |
| 22 | A5+C6 | frequency slide without copy-event |
| 23 | G-iterate + Swap-layer | generation \(n\) on bits, \(n{+}1\) elsewhere |
| 24 | G-alternate | vector ↔ host; compile ↔ reimplant |
| 25 | G-nested constructor | constructor emits better constructor |

### Outside the schema (if real, the schema fails)

- Harm with no physical store and no ongoing process in this world (acausal / no local handle; ch05 late-cosmic cases).
- Primitive from unknown physics (new A; schema still applies, A-list does not).
- Adverse only as value dispute without physical reduction (bundle/bearer).
- Logical inconsistency as such.

---

## Completeness

**Schema-complete.** Any physically grounded process that harms humans despite countermeasures is a hybrid execution \((X,F,G,U)\) typed on the nine axes, with discrete trace (if any) built from §3 operators including Drift, Iterate, and Alternate.

**Not claimed:** instance lists; unique \((X,F,G)\); prediction of Guards an optimizer will find; unknown substrates; numerical risk scores; decidability of reaching \(U\).

**Falsifiers:** a realized adverse path that is not hybrid-executable; reconstitution that is neither store, copy, hop, nor flow; defense interaction outside evade / host / select / weaponize / overwhelm / independent; dynamics neither continuous nor jump-regularized.

**Instance incompleteness:** which \(X\), which allowed \(F\) (including optimizer-chosen drifts inside physics), which Guards, which constructor descriptions already exist as science. Hybrid tracking of \(\Phi\), flows, generation kernels, and dead-man coupling addresses audit coverage; it does not close the instance set.

---

## Existing cuts (applied, not imported as new spine terms)

| Cut | Application |
|---|---|
| Pearl / actual cause | Enable, catalyze; preemption and switching |
| STPA | Unsafe control action; shutdown as fuse |
| Haddon / barriers | \(\Phi\) as energy or copies behind failed barriers |
| Epidemiology | Reservoir, vector, latency, \(R_0\), quorum; \(T\) as iterate |
| von Neumann | Description ≠ machine; nested \(T\) building \(T'\) |
| Hybrid systems / barriers | Flow + jump; \(U\) unreachable relative to a model |
| Branching / CRNs | \(T^{n}\); multi-type extinction vs explosion |
| TSA boundary (ch01/ch07) | Where is \(\Phi\), including drifting state? |
| TSA successor (ch30) | Inert intermediates and \(T^{n}\), not only \(A'\) with \(C \ge C_0\) |
| TSA drift (ch46) | Value-geometry C6 only |
| TSA parasite (ch36) | Host need not be a correction system |
| TSA \(\mathrm{Fit}_E\) (ch34) | Dormant forms and constructor descriptions |
| Perrow | Tight coupling; composition operators |
| ch33 envelope | Channel whitelist, \(\mathcal{T}\), write sinks — [`design-bounds.md`](design-bounds.md) |
