# Formalizability: absence of gaps vs bounds

Question: which parts of the harm-path generator can be formalized down to known physics in a way that would **prove absence of gaps**, or at least **bound** them?

Short answer: **absence of all gaps is not a physics theorem.** Hybrid executions make the *schema* almost tautologically complete (every physical trajectory is a flow, plus jumps as fast-flow idealizations). That does not enumerate instances and does not decide reachability. What physics *does* give is **bounds** on energy, speed, copy-count, and (given a model) barrier certificates. Iterated sporulation is the most tractable class. Continuous drift is tractable *if* the allowed vector field is known or power-bounded; it is a differential game if an optimizer chooses the drift inside physics. Cross-layer hops and unknown Guards are where formality leaks.

This file is the argument. It is not Lean and not a spine claim.

## 1. Three things “no gaps” could mean

| | Meaning | Closable? |
|---|---|---|
| **G1 Schema** | Every physical harm-path is some hybrid execution typed on the axes | Almost yes, and almost vacuous: any Lipschitz world-trajectory is a flow |
| **G2 Model** | Given \((X,F,G,U,u)\), every execution that hits \(U\) is accounted for | Yes *relative to the model*; general reachability is **undecidable** |
| **G3 World** | The model includes all physically relevant degrees of freedom and all allowed \(F,G\) | Never from the armchair; physics constrains \(F\), it does not hand you \(F\) |

Proving G1 is the amendment (finite words → hybrid). It does **not** prove there are no missed *kinds of threat*. Kinds are our cut; physics does not come pre-factored into A1–A9.

The useful target is **G2 plus physics bounds on the G3 residual**: every trajectory *allowed by this conservation/causal envelope* either is in the model or has effect \(\le B\).

When the envelope is a **construction** (channel whitelist, inventory, write sinks, type/iteration caps, change control), those bounds become the medical/aeronautical kind of theorem. That is the intended reading; it is written in [`design-bounds.md`](design-bounds.md), not as schema-completeness.

TSA’s Lean spine already does a G2-shaped thing on a *different* object (graphs, correction reachability, successor invariance). It does not currently take \(X\) to be physical state. See `formal/README.md`: Lean proves logical shape *if* bridges hold; it does not prove ASI alignment, and it does not prove all-hazards coverage.

## 2. What known physics actually supplies

These are the handles. They bound **magnitude and rate**, not taxonomy.

| Handle | Bound | Applies to |
|---|---|---|
| Conservation (energy, baryon number, charge, …) | Work from a store \(\le\) free energy of that store vs environment | A1, A2, A3 (as mass/energy), A4 *carriers* |
| Relativistic causality | No effect outside the causal future; \(\tau_h\) has a light-cone lower bound (usually uselessly tight) | all hops |
| Second law / available work | Dormant \(\Phi\) is a non-equilibrium store; equilibrium has \(\Phi=0\) | C3, C4, C5, C6 |
| Landauer | Erasing a bit costs \(\ge kT\ln 2\); information is physical | A4 stores |
| Bekenstein / holographic | Information in a region is density-bounded | size of a C3 bit-store |
| Resource-limited replication | Copy-count \(\le\) feedstock / energy; \(R_0\) not free | G-epi, constructors |
| Metastability / Arrhenius | Spontaneous germination rate \(\sim e^{-\Delta E/kT}\) for barrier \(\Delta E\) | C3 → germinate |
| No-cloning | Unknown *quantum* states cannot be copied; almost irrelevant to classical spores | edge case |
| Min duration/energy per jump | Zeno executions are unphysical | hybrid regularization |

**Consequence.** Given a *specified* store, you can bound blast yield, max copies, and (order-of-magnitude) how small an inert information store can be. You cannot bound “all possible Guards an optimizer will discover” or “all constructor descriptions already published.”

Coupling does not mint free work: Sequence/Enable/Dead-man of energy-bounded processes stays energy-bounded. It can still *bypass a barrier* (Swiss cheese). Bounds on energy are not bounds on *which barrier is left standing*.

## 3. Class by class

Legend: **Abs** = can prove *absence* of this class of gap, under stated hypotheses. **Bnd** = can prove a quantitative bound. **Rel** = complete relative to a model (G2). **No** = not closable as absence.

### 3.1 Energy dump and chemistry (A1–A2) — strongest physics

| Question | Status |
|---|---|
| Max work from a known inventory | **Bnd** (thermo + stoichiometry) |
| All reaction pathways in a *given* species list | **Rel** (chemical reaction network); unknown species = G3 residual |
| CRN deficiency / persistence | **Rel**, sometimes **Abs** inside the CRN (no explosion, extinction of a species) |
| Fatigue / corrosion as C6 | **Rel** (continuum damage mechanics); parameters empirical |

This is the closest to “down to known physics.” The residual is *unknown species and unknown catalysts* (A7), which is exactly the constructor/protocol spore.

### 3.2 Iterated sporulation / transmission (G-iterate, Alternate) — most tractable *process* class

The user’s guess is right: this is the easy generalization **and** the one with the best existing math.

| Object | Status |
|---|---|
| Single-type branching process | **Bnd**: extinction probability, mean, explosion vs \(R\le 1\) |
| Multi-type Galton–Watson | **Bnd**: spectral radius of the mean matrix; Alternate life cycles |
| Epidemic next-generation operator (Diekmann–Heesterbeek) | **Bnd**: \(R_0 = \rho(T)\); final-size bounds given mixing |
| Spatial branching random walk / metapopulation | **Bnd** under mixing assumptions; **No** for arbitrary hidden hosts |
| Nested constructor (von Neumann) | **Rel** as kinematics; **No** as “all possible constructor lineages already in the literature” |
| Continuous replication (ODE / CRN) | **Rel**; same as C6 on copy-number |

**Absence result you can actually state.** If you *know* the type set, the mean offspring matrix \(M\), and the mixing, then \(R_0<1\) implies almost-sure extinction (plus a tail bound). That is a real theorem. The gap is: unknown types, unknown hosts, unknown \(M\), and types that hop out of the type set (Swap-layer). Nested constructors that emit a *new* type are exactly “\(M\) is not a fixed matrix.”

Physics enters as feedstock bounds on \(M\)’s entries, not as a proof that the type set is complete.

### 3.3 Continuous incremental change (C6) — formal as math, physics only once \(F\) is constrained

| Object | Status |
|---|---|
| ODE / Lipschitz flow, \(F\) known | Unique execution; **Rel** reachability; barrier certificates can give **Abs** of hitting \(U\) *in that model* |
| Differential inclusion \(\dot x \in F(x)\) | Tube of trajectories; **Bnd** if \(F\) is compact-valued and you have a barrier for the whole inclusion |
| Polynomial / linear hybrid automata | Some reachability **decidable**; general hybrid reachability **undecidable** (Henzinger et al.) |
| Optimizer chooses \(F\) inside a physics-allowed set \(\mathcal{F}\) | Differential game. **Bnd** if \(\mathcal{F}\) is power/rate-bounded (max watts, max mutation rate, max institutional change). **No** if \(\mathcal{F}\) is “whatever physics allows” without a compact envelope |
| Sub-threshold increments | Sequential testing / occupation measures; **Rel** to the observation σ-algebra. Physics does not pick the eval grain |

**Absence of missed *flow* kinds:** if you accept “every physical evolution is a (possibly set-valued) flow on some \(X\),” C6 is schema-complete (G1). That is the right amendment. It does not prove a given audit will see the drift.

TSA already has an agent-shaped C6: ch46 unconscious value drift (governed vs unconscious change of value geometry). That does not cover material fatigue, capability creep below eval resolution, or replicator-frequency slide (A5+C6).

**Physics bound that *is* available without knowing \(F\):** if the system’s available power is \(\le P\) and the unsafe set is a distance \(d\) away in a metric where work relates to motion, time-to-\(U\) is at least something like \(d\)-in-work-units \(/ P\). This is usually too coarse to be operational, but it is the honest energy envelope. For selection, the analogous envelope is a maximum replication rate given energy and mass.

### 3.4 Latent stores / single-cycle spores (C3) — thermo + detection theory, not completeness

Metastable stores are physically characterized (local free-energy minimum, barrier). **Bnd** on spontaneous germination (Arrhenius). **No** on “we have found all metastable stores,” which is a search problem over \(X\).

Landauer + Bekenstein: a bit-store of size \(N\) has a physical footprint. In principle a complete matter-scan would see it. That is not an operational absence proof; it is a reminder that C3 is not acausal.

### 3.5 Information *semantics* (A4) — physics bounds the carrier, not the meaning

| | |
|---|---|
| Carrier energy / size | **Bnd** (Landauer, mass) |
| “Does this bitstring ever Enable A1–A3?” | **No** as a general program property (Rice). Restricted ISAs / typed constructors can be **Rel** |
| Firmware below the audited OS | Model-completeness of the *boundary*, not physics |

This is why TSA’s wrong-object cut is load-bearing: physics will not parse a PDF as a constructor for you.

### 3.6 Selection (A5) — formal, only weakly “physics”

Replicator dynamics, Price equation, adaptive dynamics: **Rel**. Physics enters only as the substrate of copying. \(\mathrm{Fit}_E\) is already TSA’s object; C6+A5 is the *continuous* version (frequencies slide with no copy-event). Absence of missed selection *kinds* is not a physics result.

### 3.7 Cross-layer hops (F, Swap-layer) — where formality leaks

Each layer has its own theory (EM, chemistry, CRN, digital, institutional). The hop is a coupling of two models. There is **no single** physics that composes them. You can:

- **Rel**: hybrid automaton with one mode per layer and guarded resets
- **Bnd**: energy/causality still apply across the hop (the fire cannot exceed the fuel plus whatever work the bits spent on the actuator)
- **No**: completeness of the *hop list* (which layer-pairs exist as Enable)

Stuxnet-class is the witness: the cyber slice and the physical slice can each be modeled; the missed object is the reset map between them.

### 3.8 Defense coupling and dead-man — games, not physics

If the action sets of system and correction are known, this is a (possibly differential) game: **Rel**, sometimes **Bnd** (value of the game). Proving *no missed coupling kind* requires knowing both action sets. Dead-man is an unsafe control action (STPA); formalizable as a reset triggered by \(u\in U_{\mathrm{correct}}\). Physics does not tell you the action set of a lab’s shutdown procedure.

### 3.9 Unknown Guards / unknown constructors — instance incompleteness, permanent

Not a missing axis. Not closable by a better grammar. Science-as-spore-field is empirical. An optimizer searching for Guards is searching a space physics does not enumerate.

## 4. What a “proof of no gaps” could honestly look like

A package that does not lie:

1. **Envelope.** All processes consistent with listed conservation laws, a max power \(P\), a max copy-rate, and a causal structure (light cones / network topology). This is G3-*bounded*, not G3-complete.
2. **Model.** A hybrid inclusion \((X,F,G)\) whose \(F\) is the physics-allowed set \(\mathcal{F}\), not a single ODE. Unsafe set \(U\). Correction as a constrained \(u\).
3. **Certificate, relative to (2).** Barrier / barrier-like function, or \(R_0<1\) for the generation operator, or unreachability for a *restricted* class (linear, timed, finite-mode). State the class; do not imply general hybrid unreachability.
4. **Residual lemma.** Any execution allowed by (1) but not in (2) has effect \(\le B\) (energy, copies, or probability). If you cannot prove this lemma, you have not bounded gaps; you have only modeled.
5. **Open remainder (named, not swept).** Unknown species/Guards/constructors; hops out of \(X\); optimizer-enlarged type sets (nested constructors); Rice-hard semantics of A4; value of endpoints (bundle/bearer).

Step 4 is the one usually missing. Without it, “we formalized the generator” is G2 theater — the same failure mode as certifying slices.

Lean’s present role: it can host G2 certificates for *abstract* successor/correction graphs (already the spine’s job). It cannot, without new bridges, host (1) or (4). Do not add a tenth spine claim named HybridHarm. If anything ever moves, it is a reverse-gap sentence: successor-closure and barriers as currently operationalized are discrete and agent-shaped; flows and generation kernels are not in that object class.

## 5. Verdict table

| Class | Formal object | Down to physics? | Absence of gaps? | Bound gaps? |
|---|---|---|---|---|
| Schema (flow+jump+iterate) | Hybrid inclusion + generation kernel | G1 yes (trajectory = execution) | Kinds: no (our cut) | — |
| A1–A2 energy/chemistry | Thermo + CRN | **Yes**, given species list | Pathways in list: Rel | Yield, rate: **yes** |
| C6 drift, \(F\) known | ODE / inclusion + barrier | As continuum physics | Hitting \(U\): Rel, sometimes Abs in-model | Tube / time-to-\(U\) |
| C6, optimizer chooses \(F\in\mathcal{F}\) | Differential game | Only if \(\mathcal{F}\) is a physics envelope (power, rates) | No | Yes, *if* envelope is compact |
| G-iterate / Alternate, types known | Branching / next-generation \(T\) | Feedstock bounds on \(M\) | Extinction if \(R_0<1\): **yes** | Tail, final size: **yes** |
| Nested constructor / new types | Typed \(T\) with growing type set | Kinematic, not a closed physics list | **No** | Only under a type-set cap |
| C3 latent store | Metastability + Landauer | Carrier: yes | “All stores found”: **no** | Spontaneous germ rate; min size |
| A4 semantics | Programs / constructors | Carrier only | Harm-Enable: **no** (Rice) | Restricted ISA: Rel |
| A5 selection | Replicator / Price / \(\mathrm{Fit}_E\) | Weak | Kinds: no | Frequencies given \(E\): Rel |
| Cross-layer hop | Hybrid reset between theories | Per layer, not of the hop list | Hop list: **no** | Energy across the hop: yes |
| Dead-man / defense game | STPA + game | Action sets are institutional | Action-set completeness: **no** | Value of game if sets known |
| Unknown Guard / published constructor | Search | Empirical | **No** | — |
| General hybrid reachability | Hybrid automaton | — | Undecidable | Restricted subclasses only |

**If the goal is a proof that TSA-shaped machinery has no remaining physical holes:** that proof does not exist. The strongest honest result is an **envelope + relative certificate + residual bound**, with iterated sporulation and energy/chemistry as the parts that actually compute, and with C6-under-known-\(\mathcal{F}\) as the next.

**If the goal is to stop missing classes in the generator:** hybrid executions close the finite-word hole (C6 and \(T^{n}\) including Alternate). That is schema work, not a physics completeness theorem.
