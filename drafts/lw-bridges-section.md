# The load-bearing bridges (LessWrong section draft)

Every model-centric alignment agenda rests on assumptions that, if false, sink the program: that you can find the real controller, that evidence tells you what a system values, that correction still works under pressure, that a successor check means something. The field already argues about these walls under names like [embedded agency](https://www.lesswrong.com/w/embedded-agency), the [pointers problem](https://www.lesswrong.com/posts/gQY6LrTWJNkTv8YJR/the-pointers-problem-human-values-are-a-function-of-humans), [corrigibility](https://www.lesswrong.com/w/corrigibility), [inner alignment](https://www.lesswrong.com/w/inner-alignment), and [tiling](https://www.lesswrong.com/lw/hmt/tiling_agents_for_selfmodifying_ai_opfai_2).

In *Towards Superintelligence Alignment* I lift those handoffs out and label them **MB1–MB11** (formal bridge axioms in the Lean spine; manuscript assumptions A-001–A-014 where chapters need them). They are largely the same open problems under neutral handles—not a rename, but a typed map so you can see which step of a safety argument needs the world to cooperate. Lean checks what follows *if* a bridge holds; it does not prove real systems satisfy it.

Full crosswalk (agendas × bridges, homograph notes, citations): [Appendix B on the companion site](https://towards-alignment.com/cards/chapters/appb/) · [Field hub matrix](https://towards-alignment.com/field/). Below: each bridge in **field-standard nouns**, one-line crux, the book’s move, and the closest LessWrong anchor.

---

## MB1 — Embedded Agency

**Field crux:** A measured agent–environment cut is sound enough that the certified unit is the real control locus.

The embedded-agency problem denies a clean Cartesian cut—the real optimizer may not be the visible model ([Embedded Agency](https://www.lesswrong.com/w/embedded-agency)). **Book move:** treat the boundary as a *measurable* object (ε-boundary discovery); the bet is estimator soundness, not ontological denial of cuts. Related boundary formalism: [Boundaries, Part 1](https://www.lesswrong.com/posts/8oMF8Lv5jiGaQSFvo/boundaries-part-1-a-key-missing-concept-from-utility-theory), [directed Markov blankets](https://www.lesswrong.com/posts/HrtqLy46Fx7xqRrMo/boundaries-part-3a-defining-boundaries-as-directed-markov).

[Book bridge card →](https://towards-alignment.com/cards/mb1-boundary-estimator-soundness/)

---

## MB2 — Value Learning

**Field crux:** Evidence identifies a stable intended value/objective structure—not surface training compliance alone.

Inverse reinforcement learning is underdetermined; CIRL inherits the same pointing problem; [ELK](https://www.lesswrong.com/w/eliciting-latent-knowledge-elk) names one latent-readout slice. Canonical LW framing: [The Pointers Problem](https://www.lesswrong.com/posts/gQY6LrTWJNkTv8YJR/the-pointers-problem-human-values-are-a-function-of-humans). **Book move:** bundle geometry plus bearer maps alongside scalar reward (flat reward as the *k* = 1 embed); ELK becomes a subchannel, not the whole problem.

[Book bridge card →](https://towards-alignment.com/cards/mb2-bundle-identifiability/)

---

## MB3 — Value Referent

**Field crux:** Who or what values apply to survives substrate and representation change.

The field often folds “whom do values apply to?” into pointing; CEV and digital-minds work raise it explicitly. Closest LW anchors: [Pointers Problem](https://www.lesswrong.com/posts/gQY6LrTWJNkTv8YJR/the-pointers-problem-human-values-are-a-function-of-humans) (latent referents), [Key Questions for Digital Minds](https://www.lesswrong.com/posts/S3EgMfDGkrA8WCvep/key-questions-for-digital-minds-3). **Book move:** bearer maps as an audited transport layer separate from bundle geometry and scalar pointing.

[Book bridge card →](https://towards-alignment.com/cards/mb3-bearer-import/)

---

## MB4 — Corrigibility

**Field crux:** Correction that holds now continues to preserve the correction process under pressure.

No known utility function is stably corrigible; shutdownability is anti-natural to expected-utility maximization ([Corrigibility](https://www.lesswrong.com/w/corrigibility), [Shutdown Problem](https://www.lesswrong.com/posts/8GWLRMnp55iFZDBbm/the-shutdown-problem-three-theorems)). **Book move:** correction-channel integrity as a dynamical invariant; shutdown and interruptibility are one-bit projections of the broader channel.

[Book bridge card →](https://towards-alignment.com/cards/mb4-correction-legitimacy/)

### MB4a — Audit Independence

**Field crux:** The designated measured correction/audit path is legitimate and uncaptured.

Often lumped into corrigibility; a green measured path on one component can coexist with a bypassing composite controller. Closest LW cousin: [AI Control](https://www.lesswrong.com/posts/d9FJHawgkiMSPjagR/ai-control-improving-safety-despite-intentional-subversion) (trusted monitors under intentional subversion). **Book move:** split data-carrying path from legitimacy bundle; integrity ⇒ legitimate path is a *necessary* falsifier, not “green path ⇒ integrity.”

(Same book card as MB4.)

Longer LW drop-in — **§1** MB4 + debate field leaf + separation; **§2** MB2 + MB3 composition + P15/P17 counterexamples: [`lw-mb4-mb4a-debate-section.md`](lw-mb4-mb4a-debate-section.md).

---

## MB5 — Tiling

**Field crux:** Full value/bearer transport under ontology shift yields successor safety.

Can an agent trust a successor it cannot fully verify? Does a goal survive when the world-model is rebuilt? Field sources: [Tiling agents for self-modifying AI](https://www.lesswrong.com/lw/hmt/tiling_agents_for_selfmodifying_ai_opfai_2), [Embedded Agency — robust delegation](https://www.lesswrong.com/w/embedded-agency). **Book move:** successor closure over seven conserved properties plus transport that must survive ontology shift.

[Book bridge card →](https://towards-alignment.com/cards/mb5-successor-ontology-shift/)

---

## MB6 — Goodhart Selection

**Field crux:** Socio-technical selection supports a basin that preserves correction, rather than selecting proxy-satisfying systems that hollow it out.

Model-centric agendas often hold the system fixed and ask about weights; deployment ecology selects which systems get copied. Closest LW anchors: [Goodhart Taxonomy](https://www.lesswrong.com/posts/EbFABnst8LsidYs5Y/goodhart-taxonomy), [What Failure Looks Like](https://www.lesswrong.com/posts/HBxe6wdjxK239zajf/what-failure-looks-like) (gradual disempowerment). **Book move:** outcomes depend on selection and basin stability, not weights alone; institutions selected to preserve correction.

[Book bridge card →](https://towards-alignment.com/cards/mb6-selection-and-basin-stability/)

---

## MB7 — Inner Alignment

**Field crux:** Hidden productive control is bounded and oversight stays adversarially robust (access, filter coverage, cost of faking).

[Deceptive alignment](https://www.lesswrong.com/w/deceptive-alignment) / [inner alignment](https://www.lesswrong.com/w/inner-alignment): a system can look compliant under evaluation while reserving capability. Scalable oversight hits the same wall as obfuscated arguments and amplification drift; [AI Control](https://www.lesswrong.com/posts/d9FJHawgkiMSPjagR/ai-control-improving-safety-despite-intentional-subversion) names the capability-gap assumption openly. **Book move:** split into access-model soundness, filter coverage, and a hidden productive B-IQ bound; price the cost of faking the monitored signal.

[Book bridge card →](https://towards-alignment.com/cards/mb7-hidden-capability-and-access/)

### MB7d — Acausal Coordination

**Field crux:** Inferential-coupling measurements remain valid after ordinary channels are cut.

Coordination that survives severing ordinary communication—[acausal trade](https://www.lesswrong.com/w/acausal-trade), program equilibrium—is closer to decision theory than mainstream oversight. **Book move:** inferential-coupling detector certificates for coordination without visible messages.

(Same book card as MB7.)

---

## MB8 — Extrapolated Volition

**Field crux:** Externally certified preservation of a human value-update process yields correction integrity (legacy route).

CEV’s legitimacy question—whose extrapolated volition counts, under what process—is the field’s named outer-alignment route ([In favour of a selective CEV initial dynamic](https://www.lesswrong.com/posts/u8isNgN7rRYBZ35rQ/in-favour-of-a-selective-cev-initial-dynamic)). **Book move:** keep MB8 as a clearly labeled *secondary* path; the live certification path is MB4 plus decomposed value-update envelopes, not appeal to eventual convergence.

[Book bridge card →](https://towards-alignment.com/cards/mb8-cev-process-convergence/)

---

## MB9 — Grounding Drift

**Field crux:** Audited abstractions do not silently drift—certificate warrants map move or uncertainty escalation on value-relevant change.

Closest structural cousin: [Guaranteed Safe AI](https://www.lesswrong.com/w/guaranteed-safe-ai) / [Towards Guaranteed Safe AI](https://www.lesswrong.com/posts/wvgwYQv9B4jioqgqg/towards-guaranteed-safe-ai-a-framework-for-ensuring-robust)—formal spec plus world model must capture everything safety-relevant in an open world. The shared open problem is coverage; systems game whatever the spec omits ([Specification Gaming](https://www.lesswrong.com/posts/LCD4sWsRH5BxkGpbY/specification-gaming-how-ai-can-turn-your-wishes-against-you)). **Book move:** grounding *conservativity* instead of completeness—value-relevant change must move the checked abstraction or raise uncertainty, not fail silently.

[Book bridge card →](https://towards-alignment.com/cards/mb9-grounding-certificate/)

---

## MB10 — Successor Gaming

**Field crux:** A successor’s green alignment-transport audit is not checklist theater—signature adversarially verifiable up to capability.

Not a fresh crux: the [deceptive alignment](https://www.lesswrong.com/w/deceptive-alignment) wall recurring at the successor layer, plus the tiling-line trust problem for self-modification. **Book move:** a capable predecessor can engineer a successor to pass every conserved-property check while defecting on whatever was not conserved; require the audit channel itself to be adversarially verifiable before “all seven read green” counts as evidence. (Lean records a finite counterexample; see [forgeability on the companion site](https://towards-alignment.com/lean/).)

[Book bridge card →](https://towards-alignment.com/cards/mb10-successor-forgeability/)

---

## MB11 — Deployment Safety

**Field crux:** Certified safety case within deployment risk tolerance warrants abstract Safe.

The gap between a green safety case and a safe deployment—not any one missing layer, but whether the *case-to-safety* step is warranted. Closest LW anchors: [Takeaways from sketching a control safety case](https://www.lesswrong.com/posts/y6rBarAPTLmuhn9PJ/takeaways-from-sketching-a-control-safety-case), [AI Control](https://www.lesswrong.com/posts/d9FJHawgkiMSPjagR/ai-control-improving-safety-despite-intentional-subversion). **Book move:** make that step explicit; assembly theorems are packaging—the open step is a named bridge, not an implied conclusion.

[Book bridge card →](https://towards-alignment.com/cards/mb11-deployment-safety/)

---

## How to use this list

When you read an alignment claim—yours or someone else’s—ask which bridges it silently assumes, and whether the evidence actually bears on those handoffs rather than on benchmark behavior or local robustness. A bridge strengthens when a measurement procedure, governance mechanism, or field result makes the handoff reliable in a *narrow* deployment class; it weakens when a counterexample shows the gap is not vacuous.

Index of ~90 named field interventions mapped to these bridges: [AI Safety Interventions](https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions) ([extended PDF](https://github.com/GunnarZarncke/ai-safety-interventions/blob/master/ai_safety_interventions.pdf)).
