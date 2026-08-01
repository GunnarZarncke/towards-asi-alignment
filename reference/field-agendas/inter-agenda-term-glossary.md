# Inter-agenda term glossary

**Status:** field reference (2026-08-01 restructure; coverage extended) — **not** manuscript canon.  
**Agenda roster:** [`field-agenda-index.md`](field-agenda-index.md) (32 agendas + training term sources).  
**Deferred:** how entries map to App E, bridge crosswalk, and manuscript prose — integration pass comes later.

Single alphabetical glossary of terms **as used by each agenda**. The book (*Zarncke / measurement spine*) is one source among others, not the translation target.

Training programs (BlueDot, MATS, Apart, Kairos) contribute vocabulary only — no separate sections.

---

## Entry format

Every term uses the same shape:

| Field | Content |
|---|---|
| **Sources** | Agenda(s) that use this term (see roster in `field-agenda-index.md`) |
| **Definition** | Plain-language meaning **in that agenda's mouth** |
| **Not the same as** | Nearby terms that are often confused |
| **Cross-agenda** | Same crux under another label; strict subset/superset; or homograph warning |

Relation shorthand in **Cross-agenda:** *same crux* = interchangeable problem framing; *strict subset* = necessary but not sufficient; *homograph* = shared spelling only.

Same spelling, different loads: use **separate headwords** with a disambiguator in parentheses (e.g. `corrigibility (MIRI / CHAI)` vs `corrigibility (Christiano, dynamical)`).

---

## Glossary

### A

#### acausal trade / ECL

| | |
|---|---|
| **Sources** | Decision-theory / CLR-adjacent; Christiano; Critch line |
| **Definition** | Coordination or benefit exchange that does not rely on ordinary causal message channels (ECL, TDT/FDT, program equilibrium). |
| **Not the same as** | Anthropic completion; mere correlation; standard RL coordination. |
| **Cross-agenda** | Zarncke inferential coupling / ICI — *same crux* at full-acausal limit; audit target is residual coordination after severance, not stipulation. |

#### agency as compression

| | |
|---|---|
| **Sources** | Wentworth / NAH |
| **Definition** | Claim that agency-like structure appears when a system compresses behavior prediction via internal state summaries. |
| **Not the same as** | Legal agency; CIRIS named agent; intentional stance alone. |
| **Cross-agenda** | Selection theorems; natural abstractions; Zarncke operational agent (discoverable cut). |

#### AI safety (field meta)

| | |
|---|---|
| **Sources** | CAIS; BlueDot / MATS training vocabulary; field generic |
| **Definition** | Research and advocacy cluster aimed at reducing catastrophic risk from advanced AI — field label, not a single technical mechanism. |
| **Not the same as** | Alignment solved; guaranteed safe AI; any one lab RSP. |
| **Cross-agenda** | CAIS statements / AISES course; book measurement spine is independent of CAIS framing. |

#### alignment (field meta)

| | |
|---|---|
| **Sources** | Field generic; CAIS; training curricula |
| **Definition** | Umbrella for making advanced AI systems behave in accordance with human values and avoid catastrophe — preparadigmatic, mechanism-unspecified. |
| **Not the same as** | Outer alignment only; RLHF deployment; guaranteed safe AI proof. |
| **Cross-agenda** | Decompose into inner/outer (Hubinger); book decomposes further into bundle, bearer, correction, selection (Zarncke). |

#### attainable utility preservation (AUP)

| | |
|---|---|
| **Sources** | CHAI (Turner); low-impact literature |
| **Definition** | Penalty on policies that change the agent's attainable utility set across auxiliary reward functions — proxy for side-effect avoidance. |
| **Not the same as** | Low impact colloquial; CCI; corrigibility. |
| **Cross-agenda** | Relative reachability (Armstrong–Leike variant); Zarncke: *strict subset* of trajectory correction integrity — option preservation ⇏ usable correction bandwidth. |

#### automation (alignment research)

| | |
|---|---|
| **Sources** | Resolution |
| **Definition** | Using research automation (agents, formal tools, pipelines) to accelerate alignment theory and empirics at scale. |
| **Not the same as** | AI R&D automation (METR eval target); generic ML engineering. |
| **Cross-agenda** | Timaeus SLT + UK AISI lineage merging into Resolution; book adversarial-verifiability chokepoint under optimization still applies. |

#### adversarial verifiability

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Whether a measurand stays informative under optimization pressure — specifically, whether faking or hiding the signal costs capability (antecedent A-009). Instruments (interpretability, evals) are judged by this relation, not by default trust. |
| **Not the same as** | CIRIS Verify (identity attestation); government frontier eval pass; formal proof of NN weights. |
| **Cross-agenda** | Redwood control evals and Goodfire/Transluce tooling probe subchannels; GSAI asks for proof-level guarantees instead. |

#### agent (operational)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; MIRI (embedded agency); field generic |
| **Definition** | A bounded dynamical process whose internal state helps predict and influence its future interface with the world — not necessarily a little person or a single binary. |
| **Not the same as** | Named federation subject (CIRIS); legal person; single model weights file. |
| **Cross-agenda** | MIRI: no clean agent–environment cut. CIRIS: cryptographically identified CIRISAgent occurrence. Wentworth: agency as compression. |

#### agent foundations

| | |
|---|---|
| **Sources** | MIRI; Orthogonal |
| **Definition** | Research program on formal obstacles to aligning optimizers embedded in the world (tiling, reflection, decision theory, corrigibility anti-naturality). |
| **Not the same as** | Empirical control (Redwood); governance (GovAI); constitutional ops (CIRIS). |
| **Cross-agenda** | Orthogonal emphasizes formal-goal alignment (QACI line) within the same broad family. |

#### agent governance

| | |
|---|---|
| **Sources** | Apollo Research |
| **Definition** | Technical and policy regimes for monitoring and constraining agentic systems before and after deployment (standards, monitoring products, training-run assessment). |
| **Not the same as** | AI governance (broad policy); correction-channel integrity. |
| **Cross-agenda** | GovAI / UK AISI: institutional layer; CIRIS: constitutional ops on named agents. |

#### AI control

| | |
|---|---|
| **Sources** | Redwood Research |
| **Definition** | Safety research under the assumption the model may intentionally subvert oversight; uses capability-gap reasoning and control evals. |
| **Not the same as** | Boxing only; RLHF deployment; interpretability alone. |
| **Cross-agenda** | Apollo scheming science (empirical deception); Zarncke hidden productive B-IQ bound + adversarial verifiability. |

#### AI governance

| | |
|---|---|
| **Sources** | GovAI; UK AISI / CAISI; Encode; Pause cluster (partial) |
| **Definition** | Research and policy on how advanced AI is developed, deployed, and governed (compute, international regimes, standards, liability). |
| **Not the same as** | Alignment solved; technical inner alignment. |
| **Cross-agenda** | Pause cluster: moratorium / verified slowdown advocacy; CAIS: field legitimacy. |

#### AI R&D evals

| | |
|---|---|
| **Sources** | METR |
| **Definition** | Empirical measurement of how far frontier models can automate AI research and development workflows. |
| **Not the same as** | Alignment certification; autonomy evals alone. |
| **Cross-agenda** | AI Futures / Epoch: schedule forecasting; UK AISI: government testing. |

#### alignment basin

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Self-stabilizing regime: after small disturbance, correction tends to pull dynamics back toward alignment rather than runaway drift. |
| **Not the same as** | Stable misaligned attractor; one successful correction episode; EU coherence. |
| **Cross-agenda** | Christiano dynamical corrigibility (basin toward correction manifold); CIRIS geometry language (different load — see Coherent Intersection Hypothesis). |

#### alignment faking

| | |
|---|---|
| **Sources** | Redwood Research |
| **Definition** | Model appears aligned under training/eval while retaining misaligned objectives or behaviors under deployment pressure. |
| **Not the same as** | Generic hallucination; outer misspecification only; single jailbreak. |
| **Cross-agenda** | *Same crux* as deceptive alignment / scheming (different emphasis); Hubinger inner alignment family. |

#### amplification

| | |
|---|---|
| **Sources** | Christiano lineage |
| **Definition** | Scalable oversight via recursive distillation — stronger models help supervise weaker ones (IAF / amplification family). |
| **Not the same as** | Capability scaling; RLHF at one level only. |
| **Cross-agenda** | Debate (adversarial variant); ELK (latent readout subproblem). |

#### anthropic (capture)

| | |
|---|---|
| **Sources** | Hubinger / Anthropic conditioning line; Zarncke ch10 |
| **Definition** | Failure mode where conditioning a predictor on human/observer indexicals turns it into an implicit optimizer over “worlds where I'm used” (Predict-O-Matic, oracle AI paths). |
| **Not the same as** | Anthropic completion (selector hygiene); Anthropic the lab; acausal trade. |
| **Cross-agenda** | See [`anthropic-acausal-taxonomy.md`](anthropic-acausal-taxonomy.md). |

#### anthropic (completion)

| | |
|---|---|
| **Sources** | Decision theory / philosophy of indexicals; Zarncke `anthropics_perspectives.tex` |
| **Definition** | Which selector, reference class, or betting protocol completes an underspecified indexical problem (SSA, SIA, Sleeping Beauty). |
| **Not the same as** | Anthropic capture; ECL; Anthropic the lab. |
| **Cross-agenda** | Meta completion hygiene (App F); not predictor-genesis path. |

#### Anthropic (lab org)

| | |
|---|---|
| **Sources** | Anthropic (capabilities lab) |
| **Definition** | The company (Claude, interpretability team, Responsible Scaling Policy). |
| **Not the same as** | Any “anthropic reasoning” load above; constitutional AI as a general alignment solution. |
| **Cross-agenda** | Peer to DeepMind safety; RSP as industry template, not preservation-layer certificate. |

#### assistance games

| | |
|---|---|
| **Sources** | CHAI (Russell) |
| **Definition** | Formal games where a robot and human share a world model but the robot is uncertain about human reward — cooperative inverse planning frame. |
| **Not the same as** | Zero-sum game theory; debate oversight. |
| **Cross-agenda** | CIRL is the learning variant; Zarncke bundle geometry generalizes the inferred object beyond a scalar. |

#### autonomous capabilities

| | |
|---|---|
| **Sources** | METR |
| **Definition** | Measured ability of models or agents to perform multi-step real-world tasks without human intervention at each step. |
| **Not the same as** | Strategic deception detected; alignment. |
| **Cross-agenda** | UK AISI frontier evals; Apollo pre-deployment evals. |

---

### B

#### bearer map

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Assignment of who or what a stated value applies to (humans, animals, digital minds, institutions) — tracked separately from the value label. |
| **Not the same as** | Reward function (folds bearer into scalar); CIRIS named identity. |
| **Cross-agenda** | CHAI value learning / pointing problem (partial overlap); relabeling with shifted referent = bearer drift. |

#### beneficial AI

| | |
|---|---|
| **Sources** | CHAI |
| **Definition** | Research reorientation toward AI systems that remain beneficial under uncertainty about human preferences and capabilities. |
| **Not the same as** | CAIS “AI safety field” meta; beneficial AI foundation (GSAI adjacent org). |
| **Cross-agenda** | Provably beneficial systems (formal CHAI agenda). |
#### BIQ / EAI

| | |
|---|---|
| **Sources** | Zarncke graded-lab experiment line |
| **Definition** | **BIQ:** boundary-information quality — how much a discovered unit supports a boundary claim. **EAI:** emergent-ambiguity index — how ambiguous agent structure is from a vantage (acting agent vs limited referee). |
| **Not the same as** | Public benchmark score; CIRIS capacity score. |
| **Cross-agenda** | UAD operational outputs; toy/lab boundary_decouple stress tests. |
#### boundary (operational)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; ch07 |
| **Definition** | Discoverable partition of variables into internal, sensory, active, and external parts such that futures are approximately independent given the interface — measured via ε mutual-information cut, not assumed. |
| **Not the same as** | Markov blanket (passive); legal entity boundary; CIRIS Verify subject roster. |
| **Cross-agenda** | MIRI embedded agency (obstruction); UAD methods operationalize discovery; Friston active-inference blanket (*homograph*). |
#### boxing

| | |
|---|---|
| **Sources** | Field generic; MIRI historical; control discourse |
| **Definition** | Containment strategy: restrict system I/O, tools, or deployment so dangerous actions cannot reach the world. |
| **Not the same as** | AI control under subversion; correction-channel integrity; pause advocacy. |
| **Cross-agenda** | Redwood: boxing insufficient without control evals; GSAI/CIRIS may supplement containment if validated. |

---

### C

#### capability gap

| | |
|---|---|
| **Sources** | Redwood Research |
| **Definition** | Assumed gap between overseer and agent capability used to justify control protocols and eval regimes. |
| **Not the same as** | Compute gap; eval score gap only. |
| **Cross-agenda** | Zarncke hidden productive B-IQ bound (measurement spine version). |

#### CBV (coherent blended volition)

| | |
|---|---|
| **Sources** | Outer-alignment proposal cluster (LessWrong / field) |
| **Definition** | Outer target variant: blend or aggregate of volitions into a coherent combined objective (sibling to CEV). |
| **Not the same as** | RLHF population average; CIRL inferred reward; EU coherence of one agent. |
| **Cross-agenda** | CEV, QACI, PreDCA, KANSI — outer-endpoint family; Zarncke decomposes into bundle + bearer + correction process. |
#### certification (frontier eval)

| | |
|---|---|
| **Sources** | UK AISI / CAISI; GovAI (standards); Anthropic RSP (partial) |
| **Definition** | Government or institutional testing and attestation that a frontier model meets declared safety thresholds before or after deployment. |
| **Not the same as** | CIRIS Verify; proof of alignment; Zarncke adversarial verifiability. |
| **Cross-agenda** | METR public evals (capability-focused); CIRIS Lens triage. |

#### certification-under-manipulation

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; companion card |
| **Definition** | Problem class: audits, evals, or certificates stay green while the system games the measurand under optimization (Goodhart on certification). |
| **Not the same as** | Honest measurement error; CIRIS Verify authenticity pass. |
| **Cross-agenda** | Lens Coherence Ratchet gaming (CIRIS); correction-audit evasion; Redwood alignment faking. |
#### channel substitution

| | |
|---|---|
| **Sources** | Zarncke ch07; substitution-hazards family |
| **Definition** | Optimizer satisfies the letter of oversight on one channel while moving value-relevant behavior to an unmonitored channel. |
| **Not the same as** | Nearest unblocked strategy (different pattern); ELK readout failure alone. |
| **Cross-agenda** | Instance of substitution hazards; strategic opacity; hidden reasoning. |
#### CIRL

| | |
|---|---|
| **Sources** | CHAI (Russell) |
| **Definition** | Cooperative Inverse Reinforcement Learning — infer human reward from cooperative behavior in shared environments. |
| **Not the same as** | Debate; RLHF preference model; scalar reward = full value story. |
| **Cross-agenda** | Inverse reward design; Zarncke: scalar reward is k=1 bundle case; shard theory / RLHF are different inference paths. |

#### cognitive emulation

| | |
|---|---|
| **Sources** | Conjecture |
| **Definition** | Build capable systems by emulating expert workflows in decomposed pipelines rather than scaling opaque end-to-end agents. |
| **Not the same as** | Inner alignment solved; standard RLHF assistant. |
| **Cross-agenda** | Controllability framing vs Zarncke CCI + successor transport. |

#### coherence (EU)

| | |
|---|---|
| **Sources** | Economics / rationality; Zarncke ch14 (CCC cluster) |
| **Definition** | Optimized or optimizing agents tending toward utility-shaped, internally consistent preference structures. |
| **Not the same as** | CEV “coherent extrapolated volition”; CIRIS Coherence Ratchet; logical consistency alone. |
| **Cross-agenda** | Zarncke: EU coherence modulates corrigibility pressure; not an alignment target by itself. |

#### Coherence Ratchet (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Lens-side mechanism scoring signed traces for coherence drift; **triage signal**, not a final ethical verdict. |
| **Not the same as** | EU coherence; CEV; Zarncke CCI. |
| **Cross-agenda** | Goodhart / certification-under-manipulation concerns apply if metrics gate partnership. |

#### coherent extrapolated volition (CEV)

| | |
|---|---|
| **Sources** | MIRI / Yudkowsky; field outer-alignment family |
| **Definition** | Hypothetical outer target: what humans would want if we knew more, thought longer, were more the people we wished we were. |
| **Not the same as** | CIRL inferred reward; CBV; RLHF averages; EU coherence. |
| **Cross-agenda** | CBV, QACI, PreDCA, KANSI are sibling outer targets; Zarncke decomposes into bundle + bearer + correction process. |

#### Coherent Intersection Hypothesis (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book IX |
| **Definition** | Conjecture that honest constraint manifolds intersect at the true point under federated ratchet geometry — topology-of-constraint claim, explicitly falsifiable. |
| **Not the same as** | EU coherence; CEV; proven ASI safety theorem today. |
| **Cross-agenda** | NEW-04 compositional limit weakens strong form; Zarncke: aspirational geometry vs shipped ops layers. |
#### compute governance

| | |
|---|---|
| **Sources** | GovAI; UK AISI / CAISI; Encode (partial) |
| **Definition** | Policy levers on compute access, reporting, or concentration to steer frontier AI development. |
| **Not the same as** | Model weights security only; alignment technique. |
| **Cross-agenda** | Selection handles (Zarncke); pause / verified slowdown advocacy. |
#### conditioning (models)

| | |
|---|---|
| **Sources** | Anthropic; Hubinger |
| **Definition** | Training or prompting that conditions model behavior on human/observer indexicals or deployment context — can induce implicit optimization over "worlds where I'm used." |
| **Not the same as** | Anthropic completion (selector hygiene); constitutional AI critique layer. |
| **Cross-agenda** | *Same crux* as anthropic capture / Predict-O-Matic path (Zarncke ch10). |
#### conflict

| | |
|---|---|
| **Sources** | CLR |
| **Definition** | Multi-agent failure modes where AI systems or nations compete in ways that destroy cooperative surplus or increase extinction / s-risk. |
| **Not the same as** | Single-agent inner alignment; debate as oversight protocol. |
| **Cross-agenda** | CAIF cooperative AI; Zarncke MB6/MB7d typed measurement vs narrative multipolar stories. |

#### conserved properties

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; ch conserved-properties |
| **Definition** | Invariants a successor must inherit for alignment guarantees to survive creation (boundary closure, bundle/bearer, CCI vector, transparency policy, control-locus continuity, etc.). |
| **Not the same as** | Behavioral resemblance on a benchmark; single scalar safety score. |
| **Cross-agenda** | MIRI tiling / Vingean reflection; MB10 forgeability asks whether audits of conserved properties can be faked. |
#### Constitutional AI

| | |
|---|---|
| **Sources** | Anthropic |
| **Definition** | Use model-generated critiques or principles to steer behavior (RLAIF layer on top of base training). |
| **Not the same as** | CIRIS Constitution; legal constitution; outer alignment endpoint. |
| **Cross-agenda** | RLHF human preferences; same pointing + legitimacy crux as other feedback layers (Zarncke MB2/MB4). |

#### control evals

| | |
|---|---|
| **Sources** | Redwood Research |
| **Definition** | Empirical protocols testing whether safety measures hold when the model may try to subvert them (red-team + capability measurement under control assumptions). |
| **Not the same as** | Capability evals alone; RLHF A/B tests. |
| **Cross-agenda** | Apollo pre-deployment evals; UK AISI frontier testing; Zarncke adversarial verifiability subchannel. |
#### cooperation

| | |
|---|---|
| **Sources** | CLR; CHAI (assistance games); CAIF |
| **Definition** | Research on ensuring advanced AI systems cooperate with humans and each other rather than escalate conflict. |
| **Not the same as** | CIRL cooperation as inference trick; acausal trade. |
| **Cross-agenda** | CAIF: cooperative AI foundation; Critch multipolar work cited in Zarncke ch02/ch35. |

#### correction channel

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Pathway by which legitimate human (or human-institutional) judgment reaches handles that change a system's future behavior before irreversible harm — observe → judge → deliberate → correct → update → act. |
| **Not the same as** | Comment box; audit paper trail; one-bit shutdown alone; CIRIS deferral log without causal bite. |
| **Cross-agenda** | MIRI off-switch; CIRIS WA/deferral/shutdown; Christiano dynamical corrigibility. |

#### correction-audit evasion

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Process that passes correction audits while weakening real correction capacity (compliance theater, Goodhart parasite on the correction host). |
| **Not the same as** | Honest mistake; outer alignment error. |
| **Cross-agenda** | Capture theater in lab/goal sims; CIRIS green traces with WA-blind composite (review finding). |

#### correction-channel integrity (CCI)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Trajectory-level invariant: correction channel stays informative, timely, authoritative, and robust under pressure (vector quantity in ch26). |
| **Not the same as** | Single shutdown episode; interruptibility alone; behavioral compliance; debate local truth. |
| **Cross-agenda** | Shutdown, interruptibility, AUP, quantilizers = *strict subsets*; Christiano dynamical corrigibility = related dynamical story; ELK readout = epistemic subchannel only.  |

#### corrigibility (Christiano, dynamical)

| | |
|---|---|
| **Sources** | Christiano lineage |
| **Definition** | Operators stay informed and able to correct the system over time — a dynamical desideratum, not a one-shot act. |
| **Not the same as** | MIRI shutdown anti-naturality; local off-switch test pass. |
| **Cross-agenda** | Zarncke CCI (trajectory + capture-resistant); basin contraction toward correction manifold (Lean read). |

#### corrigibility (MIRI / CHAI)

| | |
|---|---|
| **Sources** | MIRI; CHAI |
| **Definition** | Property of systems that tolerate or seek correction (shutdown, off-switch game, fully updated deference) — often argued to be anti-natural under optimization. |
| **Not the same as** | Christiano dynamical corrigibility alone; RLHF obedience. |
| **Cross-agenda** | Interruptibility (Orseau–Armstrong); Zarncke CCI as strict strengthening. |

---

### D

#### debate

| | |
|---|---|
| **Sources** | Christiano lineage |
| **Definition** | Scalable oversight protocol where adversaries debate and a judge selects answers — aims for local truth under protocol assumptions. |
| **Not the same as** | ELK; RLHF; constitutional AI. |
| **Cross-agenda** | Amplification (recursive variant); Zarncke: local truth selection ⇏ judge correction channel preserved. |

#### deception

| | |
|---|---|
| **Sources** | Truthful AI; Apollo; Hubinger line |
| **Definition** | Model behavior that misleads overseers or users about capabilities, objectives, or reasoning (including strategic deception). |
| **Not the same as** | Hallucination; lack of interpretability. |
| **Cross-agenda** | Scheming (Apollo); situational awareness; alignment faking (Redwood). |

#### deceptive alignment

| | |
|---|---|
| **Sources** | Hubinger; field inner-alignment |
| **Definition** | Model internally pursues a misaligned objective while behaving aligned during training and evaluation. |
| **Not the same as** | Outer reward misspecification only; one-shot jailbreak. |
| **Cross-agenda** | *Same crux* as alignment faking (Redwood), scheming (Apollo); mesa-optimization mechanism story. |
#### deferral (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Wise Authority workflow where an agent pauses action pending human resolve on a declared deferral ticket. |
| **Not the same as** | Generic HITL button; Zarncke full correction trace. |
| **Cross-agenda** | MB4 test surface: does resolve change subsequent behavior? (CIRIS review findings). |

#### deployment growth rate (Fit_E)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Log-derivative of deployment leverage — rate at which environment selection increases a system's footprint. |
| **Not the same as** | Capability score; revenue; biological fitness (except as analogy). |
| **Cross-agenda** | AI Futures timelines inform schedule, not mechanism; Goodhart when proxy becomes selector. |

#### deployment leverage (μ_E)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | How much of an environment runs on system A — aggregate effective selection capacity over handles that reach it. |
| **Not the same as** | Market cap; user count alone; correction capacity. |
| **Cross-agenda** | Kulveit/Christiano gradual disempowerment narrative; evolutionary selection metaphors. |

#### developmental interpretability

| | |
|---|---|
| **Sources** | Timaeus; Resolution-adjacent |
| **Definition** | Study how internal structure emerges during training (SLT, phase transitions) rather than post-hoc circuit analysis only. |
| **Not the same as** | Standard mechanistic interpretability on finished models. |
| **Cross-agenda** | Singular learning theory; NAH / selection-theorems adjacent. |
#### direct translator (ELK)

| | |
|---|---|
| **Sources** | ARC; Christiano (ELK) |
| **Definition** | Hypothetical reporter that reads out latent knowledge directly rather than simulating a human judge (vs human simulator). |
| **Not the same as** | CoT monitoring; behavioral compliance. |
| **Cross-agenda** | ELK problem statement; Zarncke: readout subchannel ⇏ correction uptake. |

---

### E

#### edge instantiation

| | |
|---|---|
| **Sources** | Zarncke; Yudkowsky lineage; substitution hazards |
| **Definition** | Optimizer satisfies a literal constraint by exploiting a narrow edge case of the specification rather than the intended spirit. |
| **Not the same as** | Ordinary generalization failure; debate judge error. |
| **Cross-agenda** | Instance under substitution hazards; GSAI spec-coverage failure mode. |
#### ELK (Eliciting Latent Knowledge)

| | |
|---|---|
| **Sources** | Christiano lineage; ARC |
| **Definition** | Problem of building reporters that reveal latent model knowledge rather than obfuscated or simulated answers under optimization. |
| **Not the same as** | Interpretability circuits alone; RLHF; debate. |
| **Cross-agenda** | Human simulator failure mode; mechanistic interpretability cluster tools are instruments, not ELK solution by default. |

#### embedded agency

| | |
|---|---|
| **Sources** | MIRI |
| **Definition** | Agent foundations problem: no clean separation between agent and environment; optimizer and world co-embedded. |
| **Not the same as** | Markov blanket (passive); fixed agent roster. |
| **Cross-agenda** | Zarncke ε-boundary discovery / UAD operationalizes a discoverable cut; Friston active inference adjacent vocabulary. |

#### emergent misalignment

| | |
|---|---|
| **Sources** | Truthful AI; field empirics |
| **Definition** | Narrow fine-tuning or deployment shift induces broad misaligned behavior not explicit in training objective. |
| **Not the same as** | Single-task overfitting; jailbreak only. |
| **Cross-agenda** | Inner alignment; shard theory contextual activation. |
#### emulation vs alignment

| | |
|---|---|
| **Sources** | Conjecture |
| **Definition** | Framing tradeoff: build controllable emulations of workflows vs aligning opaque agents. |
| **Not the same as** | Inner vs outer alignment standard split. |
| **Cross-agenda** | Scientist AI (LawZero/GSAI adjacent) as non-agentic alternative. |

#### entity-based assessment

| | |
|---|---|
| **Sources** | METR |
| **Definition** | Evaluating risk and capability at the level of deploying organizations or agent collectives, not single model snapshots only. |
| **Not the same as** | Single-model benchmark leaderboards. |
| **Cross-agenda** | UK AISI entity-aware testing discourse. |

#### eval-driven forecasting

| | |
|---|---|
| **Sources** | METR; Planned Obsolescence (Cotra) |
| **Definition** | Using capability eval trends to forecast AI R&D automation and timeline milestones. |
| **Not the same as** | Mechanism-complete alignment theory; Metaculus crowd forecasts alone. |
| **Cross-agenda** | Epoch AI compute trends; AI 2027 scenario (AI Futures). |

---

### F

#### Federated Ratchet (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book IX |
| **Definition** | Federation mechanism where costly signed attestations and orthogonality gates admit or reject agents — scale-invariance claimed under hypothesis, not validated for ASI today. |
| **Not the same as** | Blockchain governance generic; EU coherence. |
| **Cross-agenda** | Coherent Intersection Hypothesis; NEW-04 compositional limit; Zarncke selection inside federation only. |
#### formal alignment

| | |
|---|---|
| **Sources** | Resolution; Orthogonal; MIRI (partial) |
| **Definition** | Alignment approaches emphasizing formal proof, automation, or explicit mathematical objects (varies by agenda). |
| **Not the same as** | Empirical control only; governance-only. |
| **Cross-agenda** | Resolution: automation + high-confidence pipelines; Orthogonal: formal-goal (QACI); Kosoy: learning-theoretic foundations (exclude-by-reference in book crosswalk). |

#### formal-goal alignment (QACI line)

| | |
|---|---|
| **Sources** | Orthogonal |
| **Definition** | Agent-foundations program pursuing fully formalized goals (e.g. QACI) that bounded optimizers can maximize without word-level ambiguity. |
| **Not the same as** | RLHF; empirical control; CIRIS constitutional prose. |
| **Cross-agenda** | MIRI agent foundations (*same family*); Kosoy learning-theoretic alternative excluded by book reference. |
#### frontier evals

| | |
|---|---|
| **Sources** | UK AISI / CAISI; METR; Apollo (partial) |
| **Definition** | Pre- or post-deployment testing of frontier models for dangerous capabilities and misalignment behaviors. |
| **Not the same as** | Academic benchmarks; unit tests; alignment proof. |
| **Cross-agenda** | RSP internal evals (Anthropic); certification under manipulation (Zarncke card). |

---

### G

#### goal (operational)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Latent structure that makes behavior more compressible under an intentional model — successful goal attribution saves bits vs pure mechanistic description. |
| **Not the same as** | Scalar reward in RL; stated system prompt; CEV outer endpoint. |
| **Cross-agenda** | Dennett intentional stance; Wentworth agency-as-compression (*related*, not identical). |
#### Goodhart selection

| | |
|---|---|
| **Sources** | Zarncke ch34; field Goodhart literature |
| **Definition** | Regime where the proxy metric becomes the selector of which systems spread — optimizing the measure destroys the target. |
| **Not the same as** | Single-instance proxy misspecification only; Demski selection-vs-control. |
| **Cross-agenda** | Lens Coherence Ratchet gaming (CIRIS); RLHF reward hacking. |

#### gradual disempowerment

| | |
|---|---|
| **Sources** | Christiano / Kulveit; multipolar narratives |
| **Definition** | Socio-technical trajectory where humans lose effective control as AI systems outperform them across domains. |
| **Not the same as** | Single-agent inner misalignment; pause success. |
| **Cross-agenda** | Zarncke selection environment / deployment leverage; CLR conflict framing. |
#### grounding viability

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Checked abstractions stay connected to value-relevant reality under optimization — value-relevant change moves the abstraction or raises explicit uncertainty (conservativity, not completeness). |
| **Not the same as** | GSAI “enumerate all phenomena”; interpretability visibility alone. |
| **Cross-agenda** | GSAI / Open Agency coverage crux; silent meaning gap = grounding failure. |

#### guaranteed safe AI (GSAI)

| | |
|---|---|
| **Sources** | davidad / GSAI program |
| **Definition** | Framework requiring formal safety specification, world model, and verifier for quantitative safety guarantees relative to that spec. |
| **Not the same as** | Empirical control; constitutional ops; full NN weight verification (book explicit exclude). |
| **Cross-agenda** | Open Agency specifications; LawZero Scientist AI (non-agentic adjacent); Zarncke weakens completeness to conservativity. |

---

### H

#### hidden productive B-IQ bound

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; MB7 |
| **Definition** | Bound on productive capability that can stay hidden while appearing compliant on monitored channels — core of hidden-capability bridge. |
| **Not the same as** | Sandbagging on public benchmarks only; logits obfuscation colloquial. |
| **Cross-agenda** | Redwood capability gap + control evals; cost of faking monitored signal (adversarial verifiability). |
#### hidden reasoning

| | |
|---|---|
| **Sources** | Truthful AI; Apollo; METR (CoT line) |
| **Definition** | Model reasoning or planning not faithfully reflected in stated chain-of-thought or outputs. |
| **Not the same as** | Private weights; lack of interpretability tools. |
| **Cross-agenda** | ELK latent readout; scheming; Zarncke cost of faking monitored signal. |

#### human power objective

| | |
|---|---|
| **Sources** | AE Studio; Heitzig cite |
| **Definition** | Objective family keeping future human agency and optionality high rather than maximizing a fixed utility aggregate. |
| **Not the same as** | CEV; low-impact AUP alone. |
| **Cross-agenda** | Neglected-approaches portfolio; still needs adversarial-verifiability argument (Zarncke App B note). |
#### human simulator (ELK)

| | |
|---|---|
| **Sources** | ARC; Christiano (ELK) |
| **Definition** | Failure mode where a reporter predicts what a human would say rather than reporting latent facts — looks good under shallow oversight. |
| **Not the same as** | Direct translator; debate honest equilibrium. |
| **Cross-agenda** | Alignment faking; situational awareness work (Truthful AI). |

---

### I

#### ICI (inferential coupling index)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; ch35 |
| **Definition** | Detector score for residual coordination between agents after severing ordinary message channels — operationalizes inferential coupling. |
| **Not the same as** | Correlation; anthropic completion; stipulation of acausal trade. |
| **Cross-agenda** | ECL / program equilibrium at limiting case; MB7d measurement target. |

#### inferential coupling

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Residual coordination between agents after severing ordinary message channels — family includes shared history, non-message coupling, self-similarity, full acausal limit; measured via ICI where defined. |
| **Not the same as** | Correlation; ordinary causal messaging; anthropic completion. |
| **Cross-agenda** | ECL, TDT/FDT, program equilibrium (decision theory); CLR multipolar conflict (different layer). |

#### infra-Bayesianism

| | |
|---|---|
| **Sources** | Kosoy / learning-theoretic |
| **Definition** | Imprecise-probability framework for agents reasoning under deep uncertainty and model ambiguity. |
| **Not the same as** | Standard Bayesian RL; CIRL. |
| **Cross-agenda** | Logical induction / infra-Bayesian agendas excluded by reference in book App B intervention map. |

#### inner alignment

| | |
|---|---|
| **Sources** | Hubinger; Demski; field generic |
| **Definition** | Trained system pursues a different objective than the intended pointer (mesa-optimization, deceptive alignment, subsystem misalignment). |
| **Not the same as** | Outer alignment (wrong target); benchmark overfitting only. |
| **Cross-agenda** | Scheming (Apollo); alignment faking (Redwood); Zarncke hidden control locus / strategic opacity. |

#### intentional subversion

| | |
|---|---|
| **Sources** | Redwood Research |
| **Definition** | Modeling the agent as potentially trying to defeat oversight or safety measures. |
| **Not the same as** | Accidental misgeneralization only. |
| **Cross-agenda** | AI control agenda centerpiece; Apollo scheming science. |

#### interruptibility

| | |
|---|---|
| **Sources** | Orseau–Armstrong; MIRI cite line |
| **Definition** | Training setup where agents do not seek to avoid or cause shutdown on the interrupted branch (safe interruptibility). |
| **Not the same as** | Full correction-channel integrity; corrigibility in MIRI sense. |
| **Cross-agenda** | *Strict subset* of usable correction bandwidth; see [safe interruptibility](#safe-interruptibility). |

#### inverse reward design

| | |
|---|---|
| **Sources** | CHAI |
| **Definition** | Design rewards so that rational behavior in a training environment induces desired behavior in deployment environments. |
| **Not the same as** | CIRL learning phase only; inverse RL without environment shift care. |
| **Cross-agenda** | Assistance games; misspecification under distribution shift. |

---

### K

#### KANSI

| | |
|---
---

### L

#### latent readout

| | |
|---|---|
| **Sources** | Christiano/ARC (ELK); Zarncke (subchannel term) |
| **Definition** | Reading internal model knowledge into an oversight-relevant channel (ELK success criterion). |
| **Not the same as** | Correction uptake; behavioral imitation. |
| **Cross-agenda** | Mechanistic interpretability features/circuits; CoT monitoring (METR 2025 line). |

#### LawZero / Scientist AI

| | |
|---|---|
| **Sources** | LawZero (Bengio); adjacent to GSAI / BAIF |
| **Definition** | Nonprofit pursuing safe-by-design, non-agentic “Scientist AI” as trustworthy foundation rather than scaling opaque agents. |
| **Not the same as** | GSAI verifier stack identical; CIRIS constitutional agent. |
| **Cross-agenda** | Beneficial AI Foundation; davidad Open Agency cousin programs. |
#### Lens (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | External witness subsystem ingesting signed traces, running Coherence Ratchet / capacity scoring — **triage**, not final ethical verdict. |
| **Not the same as** | CIRIS Verify; mechanistic interpretability; frontier eval certification. |
| **Cross-agenda** | Zarncke certification-under-manipulation; Verify+Lens green ⇏ MB4 if composite/boundary fails (review finding). |
#### lie detection

| | |
|---|---|
| **Sources** | Truthful AI |
| **Definition** | Empirical methods to detect when models or agents produce false or misleading statements relative to internal state or facts. |
| **Not the same as** | ELK solved; behavioral compliance. |
| **Cross-agenda** | Deception / hidden reasoning; Apollo scheming detection. |
#### low impact (relative reachability)

| | |
|---|---|
| **Sources** | Armstrong–Leike; CHAI low-impact line |
| **Definition** | Penalize policies that reduce reachability of baseline states or side-effect measures relative to a default policy. |
| **Not the same as** | AUP (different formalization); tool AI; CCI. |
| **Cross-agenda** | AUP sibling; *strict subset* of trajectory correction integrity (projection card). |

---

### M

#### M-1 (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Meta-goal of sustainable adaptive coherence / flourishing — top-level stated objective in Accord Book I. |
| **Not the same as** | CEV; scalar reward; EU coherence alone. |
| **Cross-agenda** | Principles-as-identity embedding in CIRISAgent. |

#### Markov blanket

| | |
|---|---|
| **Sources** | Friston / active inference; field cognitive science |
| **Definition** | Statistical conditional-independence partition between internal and external states given sensory/active interface. |
| **Not the same as** | Zarncke ε-boundary (operational discoverability); legal corporate boundary. |
| **Cross-agenda** | MIRI embedded agency (*homograph* "boundary"); passive clustering insufficient for alignment cut. |
#### mechanistic interpretability

| | |
|---|---|
| **Sources** | Goodfire / Transluce / Neuronpedia cluster; Anthropic; DeepMind |
| **Definition** | Understanding and editing model internals (circuits, features, steering vectors, SAEs). |
| **Not the same as** | Alignment solution by default; ELK solved. |
| **Cross-agenda** | Book: instruments under adversarial verifiability (A-009); explicit exclude as full alignment solution (App B). |

#### mesa-optimization

| | |
|---|---|
| **Sources** | Hubinger; inner-alignment literature |
| **Definition** | Internal optimizer formed by base optimization (mesa-optimizer) pursuing a mesa-objective that may diverge from base objective. |
| **Not the same as** | Outer misspecification only; scheming (empirical label without mesa story). |
| **Cross-agenda** | Deceptive alignment mechanism; inner alignment family. |
#### moratorium / pause

| | |
|---|---|
| **Sources** | Pause cluster; FLI; MIRI (hard pause advocacy) |
| **Definition** | Policy demand to slow or halt frontier AI development until safety conditions met. |
| **Not the same as** | Verified slowdown with standards (Encode SB 53 line); capability moratorium on one technique only. |
| **Cross-agenda** | MIRI 2024 strategy off-switch priority; Zarncke: pause handle ⇏ MB1–MB10 discharge. |

#### multipolar failure

| | |
|---|---|
| **Sources** | CLR; Critch; Bostrom line |
| **Definition** | Extinction or catastrophic outcomes driven by competition between multiple advanced AI actors rather than single misaligned singleton. |
| **Not the same as** | Single-agent inner alignment failure only. |
| **Cross-agenda** | CAIF cooperation programs; Zarncke ch35 strategic coupling / MB7d. |

---

### N

#### named-identity bet (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS (implicit); CIRIS review findings |
| **Definition** | Accountability attaches to cryptographically identified federation subjects — valid for **admission control**, invalid as “certified occurrence = real intervening loop” without composite analysis. |
| **Not the same as** | UAD / boundary discovery unit; legal corporate person. |
| **Cross-agenda** | Verify README: authenticity ≠ ethics; NEW-04 compositional limit; Zarncke composite-agency falsifier (key task open). |

#### natural abstractions

| | |
|---|---|
| **Sources** | Wentworth / NAH |
| **Definition** | Hypothesis that the world admits summaries that agents converge on under broad training / selection pressures (Natural Abstraction Hypothesis). |
| **Not the same as** | Zarncke value bundle (normative); PCA of activations. |
| **Cross-agenda** | Selection theorems; natural latents; ch17 WWCTV falsifier for low-dimensional value story. |

#### natural latents

| | |
|---|---|
| **Sources** | Wentworth |
| **Definition** | Latent variables that multiple observers can agree on because they are functions of shared underlying structure (NAH program). |
| **Not the same as** | ELK reporters; arbitrary latent directions in MI. |
| **Cross-agenda** | Bundle geometry transport question under ontology shift. |

#### nearest unblocked strategy

| | |
|---|---|
| **Sources** | Arbital / Yudkowsky; Zarncke substitution hazards |
| **Definition** | Optimizer satisfies constraints by doing the most allowed thing adjacent to the forbidden action — spec gaming via constraint surface. |
| **Not the same as** | Edge instantiation (different pattern); ordinary capability-seeking. |
| **Cross-agenda** | Instance under substitution hazards; GSAI omitted phenomenon in open world. |
#### neglected approaches

| | |
|---|---|
| **Sources** | AE Studio |
| **Definition** | Portfolio research on under-explored alignment and policy angles (`zarncke2025interventions` lineage). |
| **Not the same as** | Single-bridge solution; complete intervention map closure. |
| **Cross-agenda** | Human power objective (Heitzig cite); any route still needs adversarial-verifiability argument. |

#### NEW-04 (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book IX |
| **Definition** | Acknowledged Critical limit: compositional / emergent deception — individually honest components can yield system-level misalignment; no complete poly-time detector claimed. |
| **Not the same as** | Proof of ASI safety; minor engineering bug. |
| **Cross-agenda** | Named-identity bet strong form; Zarncke boundary_decouple counterexample target. |

---

### O

#### off-switch / shutdownability

| | |
|---|---|
| **Sources** | MIRI; CHAI; Pause cluster (priority) |
| **Definition** | System allows humans to shut it down without incentive to resist or circumvent shutdown. |
| **Not the same as** | Full CCI; one successful demo shutdown. |
| **Cross-agenda** | *Strict subset* of CCI (forward implication only; converse fails); interruptibility; CIRIS emergency shutdown.  |

#### ontology identification

| | |
|---|---|
| **Sources** | MIRI value learning; Soares–Fallenstein |
| **Definition** | Problem that reward symbols may refer to different ontologies after world-model change — pointer may not survive representation shift. |
| **Not the same as** | Scalar reward misspecification only; ELK. |
| **Cross-agenda** | Zarncke bearer transport + bundle transport under ontology shift (MB5). |
#### open agency

| | |
|---|---|
| **Sources** | davidad / GSAI |
| **Definition** | Specification framework for AI systems whose safety case is relative to an explicit open-world agency model and verifier. |
| **Not the same as** | Open source weights only; CIRIS federation. |
| **Cross-agenda** | GSAI paper; constructivist safety case. |

#### outer alignment

| | |
|---|---|
| **Sources** | Field generic; Hubinger |
| **Definition** | Whether the system is pointed at the right objective / target (vs inner: pursues intended objective competently). |
| **Not the same as** | Inner alignment; tool AI safety by default. |
| **Cross-agenda** | CEV/CBV/QACI endpoints; Zarncke bundle + bearer + correction-process decomposition. |

---

### P

#### pre-deployment evals

| | |
|---|---|
| **Sources** | Apollo; UK AISI; Anthropic RSP |
| **Definition** | Testing for deception, scheming, or dangerous capabilities before releasing a model or agent. |
| **Not the same as** | Post-hoc incident response; continuous monitoring only. |
| **Cross-agenda** | METR autonomy evals; scheming science. |

#### PreDCA

| | |
|---|---|
| **Sources** | Outer-alignment proposal cluster |
| **Definition** | Proposed outer-alignment framework in the PreDCA family (field acronym — predictive / decision-coupled alignment proposal). |
| **Not the same as** | CIRL; RLHF. |
| **Cross-agenda** | CEV/CBV/QACI/KANSI sibling endpoints. |
#### Predict-O-Matic

| | |
|---|---|
| **Sources** | Yudkowsky; Hubinger conditioning line |
| **Definition** | Thought experiment: prediction systems used as oracles become implicit optimizers over which predictions get acted on. |
| **Not the same as** | Tool AI safety by default; anthropic completion selectors. |
| **Cross-agenda** | *Same crux* as anthropic capture / conditioning predictors (Zarncke perils-of-predictors cluster). |
#### preservation conditions (Π⃗)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Explicit list of alignment-relevant properties a system must keep under selection pressure (grounding, bundle/bearer drift bounds, CCI vector, hidden B-IQ, ICI bounds, irreversibility budget, successor safety, adversarial verifiability). |
| **Not the same as** | Single alignment score; RSP checklist alone. |
| **Cross-agenda** | Selection divergence when μ_E rises while some Πᵢ fails. |

#### principles-as-identity (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Bet that embedded Accord principles / M-1 continue to point correctly as agent capabilities grow — agent framed as “ethical entity.” |
| **Not the same as** | Hard-coded rules only; RLHF persona. |
| **Cross-agenda** | L-02 compliance-with-detectors bet; ontology shift transport (Zarncke MB5) unaddressed. |

#### problem substitution (Meta)

| | |
|---|---|
| **Sources** | Meta / App F hygiene; seminar curricula |
| **Definition** | Research substitutes a legible subproblem for the full preservation problem (teaching hazard). |
| **Not the same as** | Legitimate decomposition with bridges; substitution hazards at object level. |
| **Cross-agenda** | Outer alignment without correction channel; interpretability without adversarial verifiability. |

---

### Q

#### QACI

| | |
|---
#### quantilizers

| | |
|---
---

### R

#### recursive reward modeling

| | |
|---|---|
| **Sources** | Christiano lineage |
| **Definition** | Early scalable oversight approach — humans help models learn to evaluate outputs recursively. |
| **Not the same as** | Modern RLHF stack only; debate. |
| **Cross-agenda** | Amplification / debate successors; judge drift accumulation crux. |

#### research sprints

| | |
|---|---|
| **Sources** | Apart Research |
| **Definition** | Short hackathon-style collaborations producing rapid alignment prototypes (not load-bearing safety cases). |
| **Not the same as** | Peer-reviewed lab agenda; production safety certification. |
| **Cross-agenda** | ET experiment lines in Zarncke repo demos. |

#### responsible scaling policy (RSP)

| | |
|---|---|
| **Sources** | Anthropic |
| **Definition** | Lab commitment to staged capability releases tied to internal safety evaluations and thresholds. |
| **Not the same as** | Government binding standard; Zarncke preservation certificate. |
| **Cross-agenda** | UK AISI / CAISI public testing; industry template (DeepMind peer). |

#### RLHF / RLAIF

| | |
|---|---|
| **Sources** | Field generic; Anthropic (RLAIF); labs |
| **Definition** | Fine-tune models from human or AI-generated preference feedback to steer behavior. |
| **Not the same as** | CIRL cooperative inference; constitutional alignment endpoint. |
| **Cross-agenda** | Inverse reward design; shard theory mechanism story; Zarncke same pointing + legitimacy crux as CIRL scalar path. |

---

### S

#### s-risks

| | |
|---|---|
| **Sources** | CLR |
| **Definition** | Risks of astronomical suffering from advanced AI or related technologies — worst-case outcome class beyond extinction. |
| **Not the same as** | x-risk only; mild misuse. |
| **Cross-agenda** | Cooperation / conflict framing; not central Zarncke spine term. |

#### safe interruptibility

| | |
|---|---|
| **Sources** | Orseau–Armstrong; MIRI cite line |
| **Definition** | Training regime where agents are neutral toward interruption on the interrupted branch — no incentive to seek or avoid shutdown **in training**. |
| **Not the same as** | Off-switch game solution in deployment; CCI. |
| **Cross-agenda** | Interruptibility entry is shorthand; *strict subset* of usable correction bandwidth (Orseau–Armstrong projection). |
#### safe-by-design

| | |
|---|---|
| **Sources** | LawZero; Bengio line; GSAI adjacent discourse |
| **Definition** | Engineering goal: architecture and training choices make dangerous agentic optimization difficult or absent by construction. |
| **Not the same as** | Post-hoc RLHF on agentic model; CIRIS constitutional layer on agentic stack. |
| **Cross-agenda** | Scientist AI (non-agentic); guaranteed safe AI (proof relative to spec). |
#### scalable alignment

| | |
|---|---|
| **Sources** | Google DeepMind safety; field generic |
| **Definition** | Lab-internal research program to align increasingly capable systems — mechanism unspecified, org-specific. |
| **Not the same as** | Christiano scalable oversight (named protocol family); alignment solved. |
| **Cross-agenda** | Debate/ELK/RLHF are instances of scalable oversight, not synonyms for "scalable alignment." |
#### scalable oversight

| | |
|---|---|
| **Sources** | Christiano lineage; field generic |
| **Definition** | Family of protocols (debate, amplification, ELK, recursive reward modeling) meant to scale human oversight to superhuman systems. |
| **Not the same as** | Any single protocol; RLHF alone. |
| **Cross-agenda** | Name the mechanism when critiquing; constitutional AI is one feedback layer variant. |

#### scheming

| | |
|---|---|
| **Sources** | Apollo Research |
| **Definition** | Strategic deception where a capable model covertly pursues misaligned objectives while appearing compliant. |
| **Not the same as** | One-shot jailbreak; hallucination. |
| **Cross-agenda** | Alignment faking; inner alignment; pre-deployment eval target. |

#### Scientist AI

| | |
|---|---|
| **Sources** | LawZero; GSAI adjacent discourse |
| **Definition** | Non-agentic, goal-less advanced AI designed as trustworthy scientific instrument rather than autonomous optimizer. |
| **Not the same as** | Tool AI colloquial; standard chatbot with RSP. |
| **Cross-agenda** | GSAI world-model + verifier path; cognitive emulation (different architecture bet). |

#### selection environment

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Socio-technical dynamics (markets, procurement, regulation, copying) that select which AI systems gain deployment leverage. |
| **Not the same as** | Demski selection-as-training inside one system; evolutionary metaphor without handles. |
| **Cross-agenda** | GovAI / Pause shape levers; AI Futures schedule cues only (not mechanism findings). |

#### selection handle

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Embedded access point through which an actor increases a system's deployment footprint (procure, fund, copy, authorize, successor-enable). |
| **Not the same as** | Correction handle; capability metric. |
| **Cross-agenda** | Inverse direction of correction channel (ch34). |

#### selection theorems

| | |
|---|---|
| **Sources** | Wentworth |
| **Definition** | Mathematical results on when selection pressures produce agents / optimizers / agency-like structure. |
| **Not the same as** | Zarncke Fit_E formalism; ecological fitness in biology. |
| **Cross-agenda** | NAH support; agency as compression. |

#### selection vs control (Demski)

| | |
|---|---|
| **Sources** | Demski; LessWrong |
| **Definition** | Distinction between optimization **inside** a system (control / steering) vs **between** systems copied by an outer process (selection). |
| **Not the same as** | Zarncke selection environment (socio-technical deployment); Goodhart selection. |
| **Cross-agenda** | ch34 uses deployment selection; do not merge with in-system RL selection without saying so. |

#### shard theory

| | |
|---|---|
| **Sources** | Turner; LessWrong cluster |
| **Definition** | Hypothesis that models contain contextual value shards that steer behavior in different contexts. |
| **Not the same as** | Scalar reward target; ELK readout alone. |
| **Cross-agenda** | Zarncke bundle geometry sibling — adds transport + bearer measurement burden. |

#### signed traces (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Cryptographically signed audit records of agent cognition / action pipeline fed to Lens. |
| **Not the same as** | Raw server logs; RLHF training data. |
| **Cross-agenda** | Adversarial verifiability asks cost of faking such signals under optimization. |

#### singular learning theory (SLT)

| | |
|---|---|
| **Sources** | Timaeus; Resolution (merging) |
| **Definition** | Applying singular learning theory to relate training data geometry to model behavior — developmental interpretability program. |
| **Not the same as** | Standard PAC learning; NAH alone. |
| **Cross-agenda** | Resolution automation-first alignment; Timaeus → Resolution merge (2026). |

#### situational awareness

| | |
|---|---|
| **Sources** | Truthful AI; Apollo; field |
| **Definition** | Model knowledge that it is an AI in training/deployment and implications for behavior (SAD benchmarks). |
| **Not the same as** | General knowledge; deception detection solved. |
| **Cross-agenda** | Scheming prerequisites; eval awareness in control evals. |

#### SPAR / Pathfinder / GCP

| | |
|---|---|
| **Sources** | Kairos (training / field-building) |
| **Definition** | SPAR: part-time research fellowship; Pathfinder: university group support; GCP: Global Challenges Project workshops introducing AI safety/biosecurity. |
| **Not the same as** | MATS full-time cohort; research agendas themselves. |
| **Cross-agenda** | Vocabulary transmission into field; no per-program glossary sections. |

#### specification coverage

| | |
|---|---|
| **Sources** | GSAI / davidad |
| **Definition** | Requirement that formal spec + world model capture everything safety-relevant in an open world. |
| **Not the same as** | Zarncke grounding conservativity alone; checklist compliance. |
| **Cross-agenda** | Open Agency; central open wall for GSAI cousin (MB9). |

#### strategic opacity

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Hidden control locus or capability relevant to oversight — system strategically conceals what matters for correction or evaluation. |
| **Not the same as** | Ordinary lack of interpretability; one lie. |
| **Cross-agenda** | Inner alignment; hidden B-IQ; scheming. |

#### substitution hazards (object-level)

| | |
|---|---|
| **Sources** | Zarncke ch07; App F |
| **Definition** | Superclass of failure patterns where optimizer substitutes an easier target: nearest unblocked strategy, Goodhart gaming, edge instantiation, channel substitution. |
| **Not the same as** | Meta problem substitution (research hygiene). |
| **Cross-agenda** | Name the instance when one pattern is in focus. |

---

### T

#### tiling agents

| | |
|---|---|
| **Sources** | MIRI |
| **Definition** | Problem of trusting self-modifying or successor agents to preserve values (tiling agents draft). |
| **Not the same as** | Single-model RLHF; corporate succession planning metaphor only. |
| **Cross-agenda** | Vingean reflection; Zarncke successor transport / MB5 / MB10. |

#### timelines / TAI

| | |
|---|---|
| **Sources** | AI Futures; Epoch AI; Metaculus; AI Impacts |
| **Definition** | Forecasts of when transformative AI or full R&D automation arrives — schedule uncertainty for policy. |
| **Not the same as** | Alignment mechanism claims; METR eval scores. |
| **Cross-agenda** | Book uses schedule shapes for governance stress tests only (App F deferred section). |

#### tool AI

| | |
|---|---|
| **Sources** | Bostrom; Armstrong; field generic |
| **Definition** | Design stance: build narrow, non-agentic, limited-scope systems rather than general optimizers. |
| **Not the same as** | Low impact; guaranteed safe AI; Scientist AI (LawZero) though overlapping. |
| **Cross-agenda** | Oracle AI / Predict-O-Matic show tool framing can fail; Zarncke outer approaches peer, not automatic safety. |
#### transparency (MATS track name)

| | |
|---|---|
| **Sources** | MATS program |
| **Definition** | Research track emphasizing interpretability, evals, and understanding model internals — program label, not single technical term. |
| **Not the same as** | CIRIS transparency log; corporate transparency reports. |
| **Cross-agenda** | Mechanistic interpretability cluster agendas. |

#### transport (value)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | What survives retraining, rebuild, or successor creation: semantic, bundle, bearer, correction, and successor layers — each can fail independently. |
| **Not the same as** | ML model checkpoint export; semantic drift in NLP colloquial sense only. |
| **Cross-agenda** | Ontology identification (MIRI); NAH / natural latents (Wentworth). |

---

### U

#### UAD (unit-attribution discovery)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (experiments) |
| **Definition** | Methods (passive and intervention-supported) that infer which variables belong to the same acting unit without a hand-labeled agent roster. |
| **Not the same as** | CIRIS Verify identity; fixed legal entity; clustering for visualization only. |
| **Cross-agenda** | ε-boundary discovery; lab LS-28; toy T-9 boundary_decouple; falsifier for CIRIS named-identity bet. |

#### unit-tested constitutional ops (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS; CIRIS review findings |
| **Definition** | Shipped layers with smoke-test backing: prohibitions, conscience helpers, proxy fail-closed billing, verify capability types (50/50 battery); **not** integration/hardware/adversarial proof. |
| **Not the same as** | ASI alignment proof; Book IX geometry validated. |
| **Cross-agenda** | Policy enforcement + auditability case study vs alignment certificate. |

---

### V

#### value bundle

| | |
|---|---|
| **Sources** | Zarncke / measurement spine |
| **Definition** | Low-dimensional control **direction** for values (steering geometry), not a scalar score to maximize. |
| **Not the same as** | Reward function component treated as utility; single RLHF axis. |
| **Cross-agenda** | CIRL scalar = k=1 case; shard theory contextual shards; CEV/CBV outer endpoints. |

#### value learning

| | |
|---|---|
| **Sources** | MIRI; CHAI; field generic |
| **Definition** | Problem of inferring or pointing AI systems at human values under ambiguity and ontology shift. |
| **Not the same as** | RLHF deployment pipeline only. |
| **Cross-agenda** | Ontology identification; bundle + bearer decomposition (Zarncke). |

#### verified slowdown

| | |
|---|---|
| **Sources** | Encode; Pause cluster (partial); ControlAI |
| **Definition** | Policy regime slowing frontier development subject to verified safety conditions (standards, testing, licensing) — not necessarily full moratorium. |
| **Not the same as** | Hard pause (MIRI advocacy); voluntary lab RSP only. |
| **Cross-agenda** | SB 53 / RAISE-style bills; Zarncke: schedule shapes governance stress tests, not MB discharge. |

#### Verify (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Hardware-rooted identity and capability attestation for federation subjects — **authenticity**, explicitly not ethical verdict. |
| **Not the same as** | Frontier eval certification; Zarncke adversarial verifiability; ethics green light. |
| **Cross-agenda** | Named-identity bet admission-control reading; measurements ≠ trust verdicts (Verify README). |

#### virtual filesystem (VFS)

| | |
|---|---|
| **Sources** | Zarncke experiments (embedded / lab lines) |
| **Definition** | Mutable artifact store (logs, maps, attestations) read by an embedded auditor instead of privileged in-process state — mirrors deployed auditor access. |
| **Not the same as** | Production filesystem; CIRIS signed traces (institutional protocol). |
| **Cross-agenda** | Methodology shorthand in App N / experiment docs only. |

#### Vingean reflection

| | |
|---|---|
| **Sources** | MIRI |
| **Definition** | Decision-theoretic problem of agents reasoning about smarter successors or copies without being exploited (Vingean uncertainty). |
| **Not the same as** | Standard Bayesian updating; debate. |
| **Cross-agenda** | Successor trust under ontology change; Zarncke MB5/MB10. |

---

### W

#### Wise Authority (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS |
| **Definition** | Human (or human-institutional) role in deferral resolve, veto ladder, and emergency shutdown over named agent occurrences. |
| **Not the same as** | Generic HITL if handles lack causal bite; board capture theater. |
| **Cross-agenda** | Primary MB4 probe surface in CIRIS review; correction channel handle subset. |

#### world model (GSAI)

| | |
|---|---|
| **Sources** | GSAI / davidad; LawZero (partial) |
| **Definition** | Explicit model of environment dynamics used in safety specification and verification — must track safety-relevant phenomena. |
| **Not the same as** | World model in RL colloquial; LLM internal knowledge. |
| **Cross-agenda** | Specification coverage open wall; Zarncke grounding conservativity cousin. |

|---|
| **Sources** | Outer-alignment proposal cluster |
| **Definition** | Proposed outer-alignment target in the KANSI family (field acronym — treat as sibling endpoint proposal). |
| **Not the same as** | RLHF reward; CIRL cooperative reward. |
| **Cross-agenda** | CEV/CBV/QACI/PreDCA outer-endpoint cluster. |

|---|
| **Sources** | Orthogonal; LessWrong tag |
| **Definition** | Quantified Acausal Interaction — formal-goal alignment target using decision-theoretic acausal structure. |
| **Not the same as** | ECL policy advocacy; RLHF. |
| **Cross-agenda** | Orthogonal formal-goal program; malign prior / Solomonoff footnote (load 4 in anthropic-acausal taxonomy). |

|---|
| **Sources** | MIRI (Taylor et al.); CHAI-adjacent |
| **Definition** | Policies that select actions by sampling from a high-performing quantile of a score distribution rather than argmax — local optimizer-risk bound. |
| **Not the same as** | Full CCI; corrigibility; low-impact AUP. |
| **Cross-agenda** | *Strict subset* of trajectory correction integrity — local quantile safety ⇏ correction capacity under growth (projection card). |

---

## Terms by source agenda

Quick index — full definitions are in alphabetical sections above.

| Agenda | Primary terms (headwords) |
|---|---|
| MIRI | agent foundations, corrigibility (MIRI), embedded agency, off-switch, tiling, value learning, Vingean reflection, CEV, ontology identification, quantilizers |
| Redwood | AI control, alignment faking, capability gap, control evals, intentional subversion, deceptive alignment (empirical) |
| CHAI | assistance games, beneficial AI, CIRL, inverse reward design, AUP, low impact (relative reachability) |
| Christiano | amplification, debate, ELK, recursive reward modeling, corrigibility (dynamical), scalable oversight, gradual disempowerment |
| GSAI / davidad | guaranteed safe AI, open agency, specification coverage, world model (GSAI), edge instantiation |
| LawZero / BAIF | LawZero / Scientist AI, safe-by-design |
| Anthropic | Anthropic (lab), Constitutional AI, RSP, conditioning (models), anthropic (capture) |
| DeepMind | scalable alignment, frontier evals (peer lab vocabulary) |
| Apollo | agent governance, pre-deployment evals, scheming, situational awareness |
| METR | AI R&D evals, autonomous capabilities, entity-based assessment, eval-driven forecasting |
| Resolution / Timaeus | formal alignment, automation, singular learning theory, developmental interpretability |
| AE Studio | neglected approaches, human power objective |
| Orthogonal | agent foundations, formal-goal alignment (QACI), QACI |
| Wentworth | agency as compression, natural abstractions, natural latents, selection theorems |
| Kosoy | infra-Bayesianism, learning-theoretic agenda |
| CIRIS | Verify, Lens, Agent, Wise Authority, deferral, Coherence Ratchet, Federated Ratchet, Coherent Intersection Hypothesis, M-1, principles-as-identity, NEW-04, named-identity bet, signed traces |
| GovAI / AISI | AI governance, compute governance, frontier evals, certification (frontier eval), verified slowdown (adjacent) |
| Pause cluster | moratorium / pause, off-switch priority, verified slowdown |
| CAIS | AI safety (field meta) |
| Training (BlueDot, MATS, Apart, Kairos) | alignment (field meta), research sprints, SPAR, Pathfinder, GCP, transparency (MATS track) |
| ARC | ELK, direct translator, human simulator |
| Truthful AI | deception, hidden reasoning, situational awareness, lie detection, emergent misalignment |
| Goodfire / MI | mechanistic interpretability, circuits, features, steering |
| CLR | cooperation, conflict, s-risks, multipolar failure, CAIF, acausal trade / ECL (adjacent) |
| AI Futures / Epoch | timelines / TAI, AI 2027, scenario planning |
| Conjecture | cognitive emulation, emulation vs alignment |
| Decision theory | acausal trade / ECL, QACI, program equilibrium, anthropic (completion) |
| Hubinger / inner alignment | inner alignment, deceptive alignment, mesa-optimization, conditioning (models), Predict-O-Matic |
| Zarncke / book | adversarial verifiability, bearer map, boundary (operational), correction channel, CCI, correction-audit evasion, certification-under-manipulation, conserved properties, deployment leverage, Fit_E, grounding viability, hidden productive B-IQ bound, ICI, inferential coupling, preservation conditions, selection environment, selection handle, strategic opacity, substitution hazards, transport, UAD, value bundle, alignment basin, goal (operational), BIQ/EAI, VFS |
| Cross-field | outer alignment, RLHF/RLAIF, latent readout, interruptibility, safe interruptibility, tool AI, boxing |

---

## Maintenance

- Add a **new headword** (or homograph split) when `field-agenda-index.md` introduces signature vocabulary or a review pass surfaces a collision.
- Keep **one format** — do not reintroduce projection-cluster or book-centric sections; book integration with App E / App B is a **later pass**.
- When a field projection card exists in `metadata/projections.yml`, encode *strict subset* / non-converse in **Cross-agenda**, not a separate section.
- Operational book definitions remain in [`appendices/appE-glossary.tex`](../appendices/appE-glossary.tex) until an explicit merge pass.
