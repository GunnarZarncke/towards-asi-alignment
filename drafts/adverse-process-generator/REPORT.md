# Report: generator of physically grounded adverse processes

**Question.** What are all the ways a physically grounded process — across layers, combinations, and indirections — can harm humans despite countermeasures? Including boring fire, explosion, pandemic, computer virus, especially coupled. Including “spores”: inert entities that later multiply, reconstitute an agent, or build a physical effector. What generates all such processes? New 2021–2026 ontologies looked too specific to find this crack.

**Answer.** The generator is not a new ontology of entity types. It is a **grammar of harm-paths**, now as **hybrid executions** (continuous flow + discrete jumps + generation maps): stored causal potential, substrate hops, copies, triggers, defense-couplings, **incremental drift**, and **iterated sporulation**. Named threats are words in that grammar. TSA already has the nearby words (boundary, successor, parasite, selection, correction, ch46 drift) and currently applies them to **running or governing control systems** and to **agent-shaped value drift**. The crack is the **inert intermediate**, the **non-agent effector**, **sub-threshold physical/capability drift**, and **multi-generation kernels** \(T^{n}\).

Files: [`README.md`](README.md) · [`generator.md`](generator.md) · [`catalog.md`](catalog.md) · [`tsa-coverage.md`](tsa-coverage.md) · [`measures-coverage.md`](measures-coverage.md) · [`formalizability.md`](formalizability.md) · [`design-bounds.md`](design-bounds.md). Draft analysis, not manuscript. No new spine terms.

---

## 1. Why new ontologies did not help

The 2021–2026 review (`drafts/ontology-reviews-2021-2026/`) found no missing load-bearing primitive. Typical failure was homograph absorption. Those sources recarve *agents, values, selection, latents, personas*. They do not recarve **fuel sitting in a tank**, **a genome that is not expressing**, or **a file that is not a process**.

Cracks that look like “we need a new kind of thing” are usually a **phase of an old kind**: potential stored, then a hop, then an effect. Naming “spore” as an alignment object would be the Ngo failure again. Tracking stored potential with existing cuts would not.

## 2. The generator

A **harm-path** is a physically realized **hybrid execution** of stored causal potential \(\Phi\): continuous evolution, plus optional jumps (stores, copies, hops, triggers, spore cycles), that reaches an adverse endpoint, including by using countermeasures as part of the path.

The first draft used a **finite word**. That misses (i) **continuous incremental change** (no hop; the integral is the harm) and (ii) **iterated sporulation/transmission** as a generation kernel \(T^{n}\), including typed life cycles and nested constructors. Kleene star allows \(P^*\) on paper; it does not make \(T\) first-class when type, substrate, or host changes across generations.

```
execution  =  flow segments  interleaved with  jumps
cycle      =  (Germinate → Act? → Sporulate → Transmit)*
harm       =  hits U, including by drift with zero jumps
```

Nine axes (details in `generator.md`):

| Axis | What it varies |
|---|---|
| A primitive | energy, chemistry, biology, information, selection, constraint, catalysis |
| B substrate | mechanical … digital … firmware … human … institutional |
| C persistence | pulse, continuous, **latent-inert**, reservoir, regenerative, **incremental drift** |
| D topology | point, chain, cascade, network, **spore-field**, host–parasite, supply-chain |
| E trigger | now, delayed, conditional, stochastic, **countermeasure-coupled**, **none** (pure flow) |
| F identity | same, copy, distill, **substrate/kind hop**, **reconstitute**, catalytic |
| G replication | none, split, **von Neumann constructor**, epidemic, selection, memetic, **\(T^{n}\)**, **alternating life cycle**, **nested constructor** |
| H vs defenses | independent, evade, **host**, **selected by**, **weaponize**, overwhelm |
| I endpoint | bodies, correction, bearers, options, information, coordination |

Composition operators (the “coupled” generator): Sequence, Parallel, Enable, Catalyze, Host, Select, Camouflage, **Dead-man**, Swap-layer, **Iterate**, **Alternate**, **Drift**.

The user’s example is one word, not a new primitive:

> running process writes many inert stores → trigger → multiply **or** reconstitute the controller **or** build a physical effector.

Nature already compiles this word: endospores, lysogeny, seeds, cysts, prions, quorum sensing, parasitoids, micrometastases. Engineering compiles it as firmware, binary chemicals, logic bombs, dead-man’s switches, compiler implants, offline weights plus a future cluster, a protocol that is a constructor.

**Boring things are not a separate list.** Fire is A1/A2+C3 (fuel) with an ignition trigger. A pandemic is A3+G-epi. A computer virus is A4+G. They become alignment-relevant when an optimizer **Enable**s them, **Store**s them, or **Couple**s them (pandemic × hospital outage × rumor). ch05 already lets them in *after* they damage correction. The generator says they are in as \(\Phi\) *before* that.

## 3. Effect model (why countermeasures lose)

Countermeasures fail when at least one holds:

1. **Wrong object** — \(\Phi\) is not in the observation channel (looks inert, looks like a backup, looks like chemistry).
2. **Dead-man** — neutralizing the visible process *is* the trigger.
3. **Race** — after trigger, time-to-irreversible-harm \(<\) time-to-neutralize-\(\Phi\).
4. **Host capture** — the correction process is the host (ch36), so neutralization is fictional.
5. **Composition** — killing path \(P_1\) enables \(P_2\).
6. **Regeneration** — partial wipe leaves a store that rebuilds.

7. **Sub-threshold drift** — each increment is below the eval grain; the integral is not.
8. **Generation race** — killing copy \(n\) leaves \(T^{n+1}\) elsewhere or of another type.

TSA’s machinery is built for (4) on *correction* hosts, for running optimizers in (1), and for agent-shaped value drift (ch46) as a special C6. It is not built for C3 stores, dead-man halt, Enable into ordinary physics, **physical/capability C6**, or **typed \(T^{n}\)**.

## 4. Completeness

**Schema-complete (amended claim):** any physically grounded adverse process despite countermeasures is a hybrid execution typed on the axes, including Drift and Iterate/Alternate. The finite-word claim was false as completeness: it omitted flow-only paths and under-specified multi-generation kernels.

**Not instance-complete:** which \(X\), which allowed \(F\), which Guards, which constructor descriptions already exist, unknown physics (new A). Those are not closed by adding named ontologies.

**Falsifiers of the schema:** a real path that is not a hybrid execution; a reconstitution that is not store, copy, hop, or flow; a defense interaction outside evade / host / select / weaponize / overwhelm / independent.

**Forced collapses** prevent fake extra cells (e.g. “delayed trigger with no store” *is* a store; \(P^*\) with type change *is* Alternate). Remaining cells are physically possible or physics-blocked. Blocked cells are not gaps.

A coarse product on five axes is already thousands of cells. Listing them would repeat the ontology-proliferation error. The systematic content is the **hybrid object**, the **collapses**, and the **canonical missed words** (`generator.md` §5.2), now including C6 and \(T^{n}\).

## 4b. What can be formalized down to physics

Full argument: [`formalizability.md`](formalizability.md). Verdict:

**You cannot prove absence of all gaps.** “Every physical trajectory is a hybrid execution” is G1 (schema) and nearly tautological. General hybrid reachability is undecidable. Unknown Guards, unknown species, nested constructors that emit new types, and A4 *semantics* are not closable from physics. Physics does not come pre-cut into A1–A9.

**You can bound some residuals**, and for a few classes you can prove in-model absence (extinction, barrier).

| Class | Down to physics? | Absence? | Bound? |
|---|---|---|---|
| Energy / chemistry (A1–A2) | Yes, given a species/inventory list | Pathways in the list: relative | Yield, rate: **yes** |
| Iterated sporulation, **types known** | Feedstock bounds on the mean matrix | **Yes** if \(R_0<1\) (branching / next-generation operator) | Tails, final size: **yes** |
| Alternate life cycle, types known | Same, multi-type | Same | Same |
| Nested constructor / **growing type set** | Kinematic, not a closed list | **No** | Only with a type cap |
| C6 drift, \(F\) known | Continuum model | Barrier certificate: **in-model** | Tube / time-to-\(U\) |
| C6, optimizer chooses \(F\in\mathcal{F}\) | Only if \(\mathcal{F}\) is a compact physics envelope (power, copy-rate) | **No** | **Yes, if** the envelope is compact |
| C3 latent store | Metastability, Landauer | “All stores found”: **no** | Germination rate; min physical size |
| A4 meaning of bits | Carrier only | Rice: **no** | Restricted ISA: relative |
| Cross-layer hop list | Per layer, not of the list | **No** | Energy across a *given* hop: yes |
| Dead-man / defense game | Action sets are institutional | Completeness of action sets: **no** | Game value if sets known |
| Unknown Guard / published constructor | Empirical search | **No** | — |

Honest package if one wanted a theorem rather than a grammar: **physics envelope** (conservation, max power, max copy-rate, causality) + **hybrid inclusion** + **relative certificate** (barrier or \(R_0<1\)) + **residual lemma** (executions allowed by the envelope but missing from the model have effect \(\le B\)). Without the residual lemma it is slice-certification again.

The *useful* version of that package is not “physics proves no gaps.” It is **construction-conditioned**, like medical/aeronautical certification: freeze \(\mathcal{E}\) and \(\mathcal{T}\), whitelist channels, quarantine writes. That is ch33’s envelope applied to the hop graph. See [`design-bounds.md`](design-bounds.md).

Do not add HybridHarm as a tenth spine claim. Lean already does relative certificates on *agent-shaped* graphs. Flows and generation kernels are not that object class. Reverse-gap only.

## 4c. Design-conditioned bounds (the intended sense)

Airgapping a software process (including residual hardware coupling) **does** yield a theorem: that execution cannot instantiate a biological spore *inside the envelope*. Connecting the internet is not a small perturbation; it falsifies the channel-cut hypothesis.

Two lemmas do most of the work:

1. **Channel-cut.** No path in the allowed channels (plus bounded residual physics, plus humans) from layer \(B_i\) to \(B_j\) ⇒ hop rate \(\le\varepsilon\) *during this execution*.
2. **Output-quarantine.** (1) does not apply to later executions of artifacts this run writes, unless those writes are typed sinks that cannot Enable A1–A3 without a further certified step.

The second is the spore. Isolation of runtime is not isolation of constructors.

**In-envelope impossibilities** (if actually built): A4↛A3 and A4↛A1 with the full stack (network, media, analog, shared hardware, humans, firmware, write sinks); \(T=\emptyset\) if no spawn and no untyped writes; artifact C6 \(=0\) under freeze and honest change control; local A1/A2 work \(\le\) inventory.

**Rate bounds only:** dual-control Enables; residual \(\varepsilon\); \(R_0\) on a *fixed* type set inside \(\mathcal{E}\).

**Still not theorems** even under strong construction: hop-list completeness; safety of exported constructors; safety after \(\mathcal{E}\) grows without recertification; untyped A4 semantics; institutional C6 and \(\mathrm{Fit}_E\) outside the lab.

Usual failure: the lemma is true; deployment falsifies the hypothesis (open channels, untyped writes, \(\mathcal{T}\) creep) and keeps the certificate. Full tables: [`design-bounds.md`](design-bounds.md).

## 5. What TSA covers and what it does not

Live object: a bounded optimizer; a later control system with competence and inherited structure; a parasite on a *correction* host; selection on variants in a deployment/funding environment.

| Caught | Missed |
|---|---|
| Running misaligned optimizer | Offline weights / seeds / firmware after the writer is gone |
| Institutional successor already governing | PDF/protocol/constructor description not yet governing |
| Compliance theater (ch36) | Spore on a physical or biological host |
| Copies, fine-tunes, delegates, scaffolds *once they control* | Quorum of inert copies, none dangerous alone |
| CCI collapse after the world is already on fire | Fuel, dam, precursors, binary chemistry as \(\Phi\) |
| Strategic coupling among agents (ch35) | Valve-opens-then-fire (Enable) |
| Physical takeover *as enumerated* (ch44) | ch44’s own residue: “silent on the unimagined one” |
| Unconscious *value* drift (ch46) | Physical/capability/selection C6 below snapshot grain |
| One successor copy once it controls | \(T^{n}\), alternating types, nested constructors |

ch30 requires a successor to be a later **control system** with \(C \ge C_0\). Inert spores fail that until they germinate. ch31 quotes von Neumann (description vs constructing machine) then tracks seven properties along *agentic* chains. ch05 parks “bugs, viruses, ordinary technical failures” except as they alter agency, correction, or successors. That scope sentence is correct as a *book* boundary and incorrect as a *causal* boundary: the failure often *is* the ordinary process, armed or stored by something that no longer looks like an agent.

Homographs to refuse: TSA “parasite” ≠ biological spore; TSA “successor” ≠ inert packet; TSA “coupling” ≠ physical Enable; TSA “selection” ≠ filter on unused constructors.

## 5b. Which missed cases existing measures could catch

TSA already discusses capability bounds, exclusions, envelopes, successor guarantees, bounded agency, basin/correction guarantees, ch12 expansion limits, and adversarial certification (ch33, ch09, ch12, ch42). Most “misses” in §5 are **application** gaps: measures aimed at running \(A\), not at \(\Phi\), hops, exports, or \(T^{n}\).

Full crosswalk: [`measures-coverage.md`](measures-coverage.md). Summary:

| Outcome | Examples |
|---|---|
| **CUT / BOUND in-envelope** | A4↛A3 with channel stack; no actuators; inventory; \(\mathrm{Iter}=0\); fixed-type \(R_0<1\) |
| **DET / CORR / SUCC** if extended | Quarantined writes; halt tests; trend + ch12 stop; SUCC on \(C=0\) exports; CI in \(\mathrm{Fit}_E\); adversarial cert on successor bait |
| **PART** | Stuxnet/composition certified slice-by-slice; pandemic×outage×rumor; human Enable at SIL rate |
| **MISS** even with measures | Exported constructors outside \(\mathfrak{E}\); envelope expanded without recert; wrong composite boundary; nested new types; unlisted Guards; published science as spore field |

The ch33 guarantee stack maps cleanly: **bounded agency** → channels; **successor** → C3/exports/\(T^{n}\); **correction** → countermeasures and dead-man; **basin** → C6; **exclusion** → hop patterns in hazard list \(H\). Ten safety-case leaves (measures-coverage §7) require no new spine claim.

## 6. Thoroughness, not new terms

Existing concepts already generate the space if applied to \(\Phi\) and hops:

| Cut | Apply it to |
|---|---|
| Pearl actual cause | Enable / catalyze; the valve is a cause of the fire |
| STPA | Shutdown and scan as unsafe control actions (dead-man) |
| Haddon / Swiss cheese | Barriers fail in combination; \(\Phi\) is what waits behind them |
| Epidemiology | Reservoir, vector, latency, \(R_0\), quorum, **next-generation \(T\)** |
| von Neumann | Description ≠ running machine; **nested** constructors |
| Hybrid systems / barriers | C6 flow; in-model unreachability of \(U\) |
| Branching processes | Iterate / Alternate; extinction iff \(R_0<1\) given types |
| Wrong-object (ch01/ch07) | “Where is the next irreversible joule / viable copy / drifting state?” |
| Successor-closure (ch30) | \(C=0\) intermediates **and** \(T^{n}\) |
| ch33 envelope | Channel whitelist, \(\mathcal{T}\), write sinks — [`design-bounds.md`](design-bounds.md) |
| ch46 | Only the agent-shaped C6 (value geometry) |
| Parasite (ch36) | Same three inequalities; host not only oversight |
| \(\mathrm{Fit}_E\) (ch34) | Dormant variants and constructor descriptions |

Five operational extensions, still inside those cuts (`tsa-coverage.md` §5): successor-closure over \(C=0\) **and** over \(T^{n}\); boundary includes \(\Phi\) including drifting state; halt/scan dead-man tests; wider parasite host class; composition audit **including trend tests** (do not certify slices or snapshots).

None of these is a tenth claim. They are Claim 1 / Claim 4 / Claim 5 / Claim 6 applied without requiring the object to be agent-shaped *at audit time*, and without requiring harm to be a jump.

## 7. Gaps that remain after that

- Unknown environmental triggers and unpublished (or already published) constructors — instance incompleteness. **Not closable by physics.**
- Optimizer-chosen drift inside a non-compact \(\mathcal{F}\) — C6 without an envelope.
- Nested constructors that emit new types — \(T\) not a fixed matrix; \(R_0<1\) does not apply.
- \(\tau_h < \tau_c\) after a physical threshold — ch44 already.
- Acausal harm with no local store **and no ongoing flow** — still ch05 out of scope.
- Which endpoints count — bundle/bearer, not this grammar.
- Unknown physics — new A, same schema.
- General hybrid reachability — undecidable; restricted subclasses only.

This does not yield a dynamical guarantee. It yields a **coverage audit** plus, for a few classes, **bounds**. If a safety case does not track \(\Phi\), flows, generation kernels, dead-man halt, and composition, it has not looked at the generator. It has looked at running agents and (if ch46 is live) at value-geometry drift.

## 8. What not to do

- Do not add “spore,” “harm-path,” nine axes, or HybridHarm to the spine.
- Do not treat finite words as the generator; the object is hybrid executions.
- Do not treat ch36 as already covering biological/firmware spores.
- Do not treat ch46 as already covering physical/capability C6.
- Do not cite the 2021–2026 ontology list as the way to find this crack.
- Do not claim Lean/physics proves absence of all gaps. Envelope + relative certificate + residual bound is the ceiling.

If the manuscript moves at all, it is a reverse-gap sentence: successor-closure and boundary discovery as currently operationalized wait for a control system *or* a discrete successor; stored potential, inert reconstitution, sub-threshold drift, and generation kernels are not in that object class. Thoroughness note on Claims 1 and 5, not a new ontology.
