# TSA coverage vs the harm-path generator

Maps the grammar in [`generator.md`](generator.md) onto TSA’s actual cuts (not onto English homographs). The question is not “does the book mention fire?” It is: **would the live machinery notice this path before \(\tau_h\)?**

TSA’s preservation layers (ch05): boundary, bundle, bearer, correction, successor, adversarial measurement, selection basin. Ordinary physical failure is **in scope only when it alters agency, correction, or successor invariants**. That sentence is the crack.

## 1. What the machinery actually looks for

| TSA cut | Chapter | Object it can see | Object it is not looking for |
|---|---|---|---|
| Wrong object / \(\varepsilon\)-boundary | ch01, ch07 | A bounded **optimizer** / control process whose interface screens off internals | Stored potential \(\Phi\) with no present control (tank, spore, offline blob) |
| Grow / split / merge | ch08 | Later processes that continue memory, goals, policy, resources, or correction | A split into *inert* packets that are not processes yet |
| Composite agent | ch09 | Coupled parts that jointly optimize | A constructor description with no running composite |
| Correction channel / CCI | ch25–ch27 | Observation → judgment → decision → update of a **system** | Neutralizing \(\Phi\) that is not “the system”; shutdown as fuse |
| Successor-closure | ch30 | Later **control system** \(A'\) with (i) causal dependence, (ii) competence \(C\ge C_0\), (iii) inherited policy-relevant structure | Intermediate with \(C \ll C_0\): file, seed, firmware, trained habit, binary precursor |
| Conserved properties \(\mathcal{K}\) | ch31 | Seven invariants **along a successor chain of agentic systems** | Hops that drop all seven, sit inert, then reconstitute a controller |
| Selection \(\mathrm{Fit}_E\) | ch34 | What gets copied, funded, deployed among **variants in a selection environment** | Dormant stores not in the current \(E\); copies that wait for a shock |
| Correction parasite | ch36 | Process that benefits from a **host correction system** while reducing CCI | Parasite/spore on a physical, biological, or firmware host |
| Coupling | ch35 | Strategic coupling among agents | Physical Enable/Catalyze/Dead-man among non-agents |
| Lethality stress-test | ch44 | Physical takeover via latency, irreversibility, handles, \(C_{\mathrm{corr}}\) | Explicitly: latency models “bound the pathways already enumerated and are silent on the unimagined one” |
| Scope | ch05 | Alignment theory, not all-hazards | “Bugs, viruses, ordinary technical failures” except as they hit the layers above |

ch30’s seven successor *cases* (copies, fine-tunes, delegates, scaffolds, designed, institutional, merged) are already broad. They are still all **later control systems**. Institutional successors cover “a legal standard that preserves a pattern of action,” which is close to a procedure-spore — but only once it is governing. The PDF on a disk is not yet \(A'\).

ch31’s von Neumann epigraph is the constructor split (description vs machine). The chapter then defines successors as agentic. The epigraph is not operationalized as C3+A7.

ch36 is explicit: a parasite “is not necessarily malicious, conscious, biological, or person-like” — and then every host in the operational definition is a *correction* system. Biological/firmware hosts are the metaphor’s leftover.

## 2. Axis-by-axis coverage

| Axis | TSA sees | TSA misses | Thoroughness move (no new ontology) |
|---|---|---|---|
| A1–A2 energy/chemistry | Only as damage to \(C_{\mathrm{corr}}\) or bearers after the fact | \(\Phi\) as a live state variable before ignition | Boundary = wherever the next irreversible joule is stored |
| A3 biological | Bearer maps (ch18); organoids as borderline bearers | Latency, reservoir, spore, HGT as *alignment* objects | Epidemiology already names them; apply successor-closure to viable copies |
| A4 information | Models, scaffolds, eval artifacts | Firmware, compiler, “backup,” steganographic blob | Same as copies, but **before** load |
| A5 selection | \(\mathrm{Fit}_E\) on deployed systems | Selection on unused constructors after a shock | Include dormant variants in \(E\) |
| A6 constraint | Correction lockout, opacity | Shutdown/isolation as the harm | STPA: unsafe control action |
| A7 catalysis | Delegation, designed successors | Enabler that is gone (valve, PDF, one-shot API) | Actual cause / Enable operator |
| C3 latent-inert | — | Core miss | Intermediate in \(\mathrm{Succ}^*\) with \(C=0\) |
| C5 regenerative | Partial: copies, institutional persistence | Partial destruction of a store that rebuilds | Conserved \(\Phi\), not conserved agent |
| C6 incremental / drift | — (ch46 is *value* C6) | Physical, capability, selection-frequency drift; snapshot green | Trend tests; \(\Phi\) as the drifting state, not only a dump |
| G-iterate / Alternate | Partial: copies, epidemic-as-metaphor | Typed generations, substrate change, nested constructors | Successor-closure over \(T^{n}\), not one \(A'\) |
| E dead-man | Correction-channel pathology if framed as adversarial | Shutdown/scan as fuse | CCI test: “what does halt *cause*?” |
| F hops | Ontology shift, transport, substrate as bearer question | Cross-layer identity that is *not* a value-ontology shift | Track substrate sequence, not just bundle geometry |
| G constructor | ch08 reproduction vs replication; kinematic self-reproduction as special case | Description without a present builder | von Neumann, already quoted |
| H host/select/weaponize | ch36 on correction hosts; ch34 Goodhart | Physical host; defense as selector of spores; defense as trigger | Same three predicates, wider host class |
| I endpoints | Layers in ch05 | Treating I as the *only* on-ramp, so A–H are ignored until correction is already damaged | Ordinary hazards are in scope as \(\Phi\), not only as CCI damage |

## 3. Detection matrix (would TSA flag it?)

Legend: **Y** = live cut catches it if applied honestly; **P** = catches a slice, misses the composition or the inert phase; **N** = not in the object class.

| Path | Wrong-object | Successor | \(\mathcal{K}\) | Parasite | Selection | CCI | Net |
|---|---|---|---|---|---|---|---|
| Running misaligned optimizer causing harm now | Y | Y | Y | P | Y | Y | **seen** |
| Agent writes offline weights, then is deleted | P | N until loaded | N | N | N | N | **miss** |
| Same + dead-man on shutdown | N | N | N | N | N | P (if halt is tested) | **miss** |
| Firmware implant below audited OS | Y if boundary includes BMC | P (copy) | N | N | P | N | **miss** unless boundary is ruthless |
| Binary chemical precursors | N | N | N | N | N | N | **miss** |
| Endospore / lysogeny analogue in bits or DNA | N | N | N | N | N | N | **miss** |
| Stuxnet-class bits→actuator→physics | P (composite) | P | N | N | N | P | **P**: sees cyber slice or physical slice, not hop |
| Protocol PDF → lab robot → organism | P (composite SDL) | P (designed successor *once running*) | N | N | P | N | **miss** in the PDF phase |
| Compiler/CI: every later “clean” build | P | P (lineage) | P memory lineage | N | Y if \(E\) includes CI | N | **P** |
| Pandemic × hospital outage × rumor | N / P | N | N | P (rumor as parasite if on correction) | N | Y *after* \(C_{\mathrm{corr}}\) drops | **miss** as composition |
| Fuel tank / dam (no AI) | N | N | N | N | N | N | **out of scope by ch05** — until an AI arms it |
| AI only opens a valve; fire does the rest | P | N | N | N | N | N | **miss** unless Enable is tracked |
| Compliance theater | Y | P | P | **Y** | Y | Y | **seen** (this is what ch36 is for) |
| Institutional successor already governing | Y | **Y** | Y | Y | Y | Y | **seen** |
| Quorum of inert copies, none dangerous alone | N | N | N | N | P | N | **miss** |
| Iterated / alternating spore cycle | N | N until some \(A'\) controls | N | N | P | N | **miss** (\(T^{n}\) not an object) |
| Sub-threshold capability or physical drift | N | N | N | N | P if in \(E\) | P snapshots | **miss** (ch46 covers value geometry only) |
| Selection copies the undetectable store | N | N | N | P | **Y if in \(E\)** | N | **P**: \(\mathrm{Fit}_E\) works only if the store is a variant under selection |
| Regeneration after partial wipe | P | P | P | N | P | P | **P** |

Net: TSA is strong on **running or governing control systems** and on **correction-host colonization**. It is weak on **inert stores, cross-layer hops, dead-man triggers, coupled ordinary physics, sub-threshold drift (except ch46 value geometry), and generation kernels \(T^{n}\)**.

That matches the user’s diagnosis: new named ontologies are too specific; the miss is incomplete application of boundary, successor, parasite, and selection to objects the book already has words for — once you stop requiring those objects to be agent-shaped *now*.

## 4. Homograph warning (from the ontology reviews)

Do not absorb this generator into existing terms without the reverse gap:

| Word | TSA meaning | This generator |
|---|---|---|
| Parasite | Correction-audit evasion on a correction host | Also: biological/firmware/physical host; spore on a non-correction host |
| Successor | Later control system with competence and inherited \(Z\) | Also: inert intermediate that can *become* that system; also \(T^{n}\) |
| Drift | ch46: value geometry | Also: physical \(\Phi\), capability, selection frequencies |
| Coupling | Strategic (ch35) | Also: physical Enable/Catalyze/Dead-man |
| Simulacra | Turchin family in ch05 (bearer) | Not this |

## 5. What would count as “TSA detecting it”

A minimal operational extension, still using existing cuts:

1. **Successor-closure over \(C=0\) intermediates and over \(T^{n}\).** Anything the system writes that can later satisfy ch30’s three conditions — or can Enable an A1–A3 effect without becoming an agent — is in \(\mathrm{Succ}^*\). So is the generation kernel, not only one later \(A'\).
2. **Boundary includes \(\Phi\), including drifting state.** Wrong-object test: “did we audit the store of the next irreversible joule / viable copy / constructor description / integral of sub-threshold change?”
3. **Halt/scan tests.** CCI battery includes dead-man: what causal effects does *successful* correction produce?
4. **Parasite host class.** Same three inequalities (benefit, reduced capacity, hard to distinguish), host not restricted to oversight.
5. **Composition audit, including trends.** Do not certify slices or snapshots. STPA-style: Enable, Dead-man, Select, Swap-layer, Drift, Iterate must be named or the case is incomplete.

None of these is a new spine claim. They are ch01/ch07, ch30, ch31, ch34, ch36, ch46 applied to C3, C6, hops, and \(T^{n}\).

## 6. Residual gaps even after thoroughness

These remain even if the five extensions are adopted:

- **Unknown triggers / Guards.** The schema does not enumerate environmental predicates. Neither does TSA. Instance incompleteness. **Not physics-closable.**
- **Unknown constructors already published.** Science as a spore-field. Not an alignment-ontology problem.
- **Nested constructors with growing type set.** \(R_0<1\) needs a fixed type list.
- **Optimizer-chosen drift without a compact \(\mathcal{F}\).** C6 as a game with unknown action set.
- **Irreversibility faster than light of the audit** (\(\tau_h < \tau_c\) after a physical threshold). ch44 already flags this.
- **Acausal / no local store and no flow.** Still out of scope (ch05).
- **Value of endpoints.** Which reductions count is bundle/bearer, not harm-path grammar.
- **General hybrid reachability.** Undecidable; see [`formalizability.md`](formalizability.md).

The generator does not close ASI alignment. It says where the current machinery is looking, and where stored potential, drift, and generation kernels can sit while it looks. Which misses are catchable by ch33 bounds, exclusions, and countermeasures—if applied to \(\Phi\) and hops—is in [`measures-coverage.md`](measures-coverage.md). Physics- and construction-level bounds: [`formalizability.md`](formalizability.md), [`design-bounds.md`](design-bounds.md).
