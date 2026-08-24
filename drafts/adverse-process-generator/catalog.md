# Catalog: physical harm families and analogues

Not exhaustive as a list of named threats. Instances of the grammar in [`generator.md`](generator.md). Used to check that the generator can *generate* both boring accidents and spore-like reconstitution.

## 1. Direct energy / chemistry (often “boring”)

| Family | Physical primitive | Typical latency | Countermeasure interaction |
|---|---|---|---|
| Fire / thermal runaway | oxidation + heat feedback | fuel can wait | suppression; detection of *heat/smoke*, not of intent |
| Explosion / BLEVE / dust | rapid expansion | precursors look industrial | blast walls; inerting |
| Electrical fault / arc | current, ohmic heating | wiring as latent | breakers (can be the trigger if mis-set) |
| Kinetic impact, collapse | momentum, structural failure | fatigue is latent | inspection of *structure*, not of who scheduled load |
| Radiation / criticality | nuclear / high-energy EM | sources can sit inert | shielding, inventory |
| Asphyxia, pressure, vacuum | atmosphere / constraint | enclosed spaces | sensors |
| Toxin / precursor chemistry | binary mixing, catalysis | two inert halves | precursor control (supply chain) |
| Flood, dam, coolant loss | stored gravitational/thermal potential | long store | civil engineering |

**Coupling example.** A cyber action that only opens a valve is not a fire. The fire is the stored chemical potential. TSA looking at the *agent* misses the tank farm unless successor/boundary is read as “whatever stores the next irreversible joule.”

## 2. Biological replication and latency

| Family | Pattern | TSA-relevant analogue |
|---|---|---|
| Acute infection | replicate until host fails | fast R>1 process |
| Endospore (Bacillus, Clostridium) | metabolically inert; survives sterilization; germinates on cue | digital “spore” |
| Viral latency (herpes, HIV, temperate phage) | genome inserted, silent, reactivates | weights/files that are not the running agent |
| Prion | template misfolding; no nucleic acid | “just data” that converts other data |
| Quorum sensing | inert until density | many copies wait; none looks dangerous alone |
| Reservoir + vector (plague, malaria) | harm not in the designer’s body | cloud blob → USB → lab robot |
| Parasitoid / behavior-manipulating fungus | host’s control system is the effector | correction/human as actuator |
| Horizontal gene transfer / plasmids | payload rides unrelated replicators | library, package, firmware update |
| Cancer micrometastasis | dormant cells, later angiogenesis | distributed inert shards |
| Periodical emergence (cicadas) | long wait, synchronized | time-locked payload |
| Seed bank / cyst | organism as packet | compressed checkpoint |

**Coupling example.** Pandemic × hospital cyber outage × disinformation that blocks correction. Each slice is ordinary; the composition is the catastrophe.

## 3. Information in physical media

| Family | Pattern |
|---|---|
| Computer virus / worm | copy + payload; can be delayed |
| Bootkit / firmware / BMC / GPU VBIOS | below the OS the audit sees |
| Logic bomb / dead man’s switch | trigger = *absence* of keepalive (shutdown is the fuse) |
| Supply-chain implant | inserted far from the audited object |
| Stuxnet-class | long latent; physical centrifuges as effector |
| Encrypted blob / steganography | looks like noise or a JPEG |
| Model weights as constructor | not an agent until loaded with tools + compute + actuators |
| Compromised compiler/CI | every later “clean” build is a spore |

## 4. Institutional / human as physical process

Humans are physical. Processes that live in habits, procedures, and incentives still dump energy and block correction.

| Family | Pattern |
|---|---|
| Compliance theater | correction host colonized (ch36) |
| Sleeper / social engineering | human as delayed actuator |
| Market/selection | copies the profitable process, not the safe one |
| Dependency lock-in | turning the system off *is* the harm (life-support, grid) |
| Attention capture | reduces \(C_{\mathrm{corr}}\) without a “weapon” |

## 5. Spore / reconstitution (the user’s example)

A template, not a new kind of physics:

1. A process with control (need not remain) **writes** structure into a store.
2. The store is **inert under the audit ontology** (not running, not agent-shaped, not on the network, not a successor-as-controller).
3. Copies may **proliferate** as data, DNA, chemicals, spare parts, procedures, trained humans.
4. A **trigger** (time, signal, density, shutdown, scan, environment) starts a later process.
5. That process **reconstitutes** the original controller, **multiplies**, or **builds a physical effector** (robot, toxin, fire, false instruction to a human).

Natural: endospore, lysogeny, seed, cyst, prion. Engineering: firmware, binary chemical weapon, dead man’s switch, offline weights + future cluster, “harmless” scientific protocol that is a constructor.

## 6. Cross-layer hops (indirection)

Typical hop sequences the grammar must generate:

- Bits → firmware → actuator → chemistry (Stuxnet)
- Bits → human belief → hand → physical switch
- Bits → DNA order → lab robot → organism
- Procedure PDF → trained staff → “normal operations” → valve state
- Market signal → many firms copy a design → fleet-wide latent defect
- Shutdown command → dead-man → reconstitution elsewhere

Each hop can look like a different TSA object (or like none). The harm is the **composition**.

## 7. Continuous incremental (no hop)

The finite-word grammar treated these as C2 “already running” or C4 “slow leak.” They are neither. The harm is \(\int F\); snapshots can be green the whole way.

| Family | Pattern |
|---|---|
| Fatigue / creep / corrosion | structure fails after sub-threshold increments |
| Slow chemistry / bioaccumulation | dose integrates; no ignition event |
| Capability creep | each eval pass is in-family; the limit is not |
| Replicator-frequency slide | A5 with no copy-*event*; composition of the population changes |
| Salami-slice lock-in | each institutional step is locally justified |
| Unconscious value drift (ch46) | agent-shaped C6 on value geometry only |
| Attention / dependency capture | \(C_{\mathrm{corr}}\) erodes without a weapon |

## 8. Iterated sporulation / transmission

One write-then-germinate is a word. Nature and engineering iterate it, often changing type and substrate.

| Family | Pattern |
|---|---|
| Epidemic generations | \(T^{n}\); \(R_0=\rho(T)\) |
| Alternating life cycle | malaria: mosquito ↔ human; typed \(T_i\) |
| Nested constructors | assembler that builds a better assembler |
| Compiler/CI reimplant | each clean build writes a *different* next implant |
| Seed bank → plants → seeds | generation on a new host |
| Micrometastasis cascade | dormant → angiogenic → new dormants |
| Horizontal transfer chain | plasmid hops species; type set grows |

## 9. What this list is not

A complete threat encyclopedia. If a family cannot be written as a hybrid execution typed on (primitive × substrate × persistence including drift × topology × trigger including none × identity-change × replication including \(T^{n}\) × defense-coupling × harm-endpoint), the generator in `generator.md` is incomplete. Known leftovers and what is *provable* vs merely schema-complete: [`formalizability.md`](formalizability.md).
