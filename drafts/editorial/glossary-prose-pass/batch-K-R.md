# Glossary prose-pass batch K–R

Paste-ready `####` blocks for `reference/field-agendas/inter-agenda-term-glossary.md`. Do **not** treat this file as canon until merged.

## Sources consulted

**In-repo:** `reference/field-agendas/field-agenda-index.md`; `appendices/appE-glossary.tex`; `appendices/appB-bridge-crosswalk.tex`; `appendices/appF-research-program.tex` (problem substitution); `context/affine-seminar-learning-outcomes.md`; concept bodies `subsumption-low-impact.md`, `subsumption-quantilization.md`, `subsumption-elk.md`, `subsumption-shutdown.md`; chapters ch07/ch10/ch17/ch27/ch44 (boundary, predictors, NAH, low-impact, mesa); CIRIS findings under `~/repos/ciris/review/findings/` (named-identity, stance/promises, MB4 surface, key-task composite).

**External (primary / near-primary):** Arbital KANSI; Orthogonal Formalizing QACI + Formal-Goal ToC; PreDCA overviews / Kosoy shortform line; LawZero Scientist AI publication + Bengio Introducing LawZero; Anthropic RSP announcements; Taylor 2015 Quantilizers (MIRI); Leike et al. recursive reward modeling (arXiv:1811.07871); GSAI paper (Dalrymple et al. 2024) + davidad Open Agency / Safeguarded AI line; Wentworth NAH / natural latents posts; Critch multipolar / Armstrong–Leike relative reachability / Hubinger mesa-optimization as cited in App B.

## Entry count

**34** headwords (K: 1; L: 5; M: 6; N: 6; O: 4; P: 6; Q: 2; R: 4).

## Thin / contested after this pass

- **neglected approaches** — AE Studio portfolio label; little primary mechanism text beyond agenda index + intervention-catalog lineage.
- **research sprints** — Apart training/hackathon format; deliberately non-load-bearing; thin as a technical term.
- **PreDCA** — Mechanism reconstructed from secondary distillations + Kosoy shortform line; Vanessa’s own writeups are fragmented across shortform/talks rather than one canonical paper.
- **QACI** — Formal math is dense; definition here tracks Orthogonal’s stated mechanism (blob location / counterfactual QA) without claiming implementability.
- **KANSI** — Arbital scenario page is the main primary; AFFINE gloss (“understandable algorithm known not susceptible to RSI”) is slightly compressed relative to Arbital’s fuller caveats.
- **lie detection** — Truthful AI cluster uses the phrase empirically; no single “solved method” primary.

---

### K

#### KANSI

| | |
|---|---|
| **Sources** | Arbital / MIRI strategic scenarios; AFFINE outer-alignment roster |
| **Definition** | Known-algorithm non-self-improving agent: a strategic design class in which the first pivotal AI is built from human-understood algorithms and is not allowed extensive self-modification, with power coming from scale (e.g. large compute) rather than recursive self-improvement. The hoped-for win is that reflective stability, ontology identification, and capability-limiting problems become much simpler when the system is not rewriting its own cognition. Intending KANSI is not enough—corrigibility-style work may still be needed so the agent does not invent environmental workarounds that amount to self-improvement. |
| **Not the same as** | Tool AI (capability/usage restriction without the “known algorithm + no RSI” package); pause/moratorium (policy slowdown, not a design class); QACI/PreDCA (formal outer targets that still typically assume powerful optimization, including possible self-improvement). |
| **Cross-agenda** | *Partial overlap* with soft-optimization / low-impact peers (limit dangerous optimization shape) but different mechanism (architecture + monitoring vs impact penalties). *Orthogonal* to CIRIS constitutional ops: KANSI tries to avoid RSI; CIRIS aspires to ride recursive events with Federated Ratchet gates. Book lists KANSI as a peer outer-alignment proposal alongside CEV/CBV/QACI/PreDCA, not as a preservation-layer certificate. |

---

### L

#### latent readout

| | |
|---|---|
| **Sources** | Christiano/ARC (ELK); Zarncke (subchannel term) |
| **Definition** | The success criterion of getting a model’s internal knowledge about the world into an oversight-relevant channel—typically a reporter that answers questions using what the model knows, not what would look good to a human grader. ELK frames this as beating the human-simulator strategy under optimization pressure. In the book’s crosswalk it is an epistemic subchannel: useful bandwidth for monitors, not by itself a guarantee that corrections change future behavior. |
| **Not the same as** | Correction uptake (readout can succeed while the system ignores or games the correction channel); behavioral imitation / RLHF compliance (looking aligned ≠ revealing latent knowledge); mechanistic feature dumps (circuits/SAEs are instruments that might support readout, not the readout criterion). |
| **Cross-agenda** | *Strict subset* of ELK’s problem statement (ELK = design reporters that achieve latent readout under adversarial pressure). *Partial overlap* with CoT monitoring and MI tooling (candidate channels). Lean separation: latent readout ⇏ correction uptake; App B places ELK under MB2/MB3 pointing, not as full CCI. |

#### LawZero / Scientist AI

| | |
|---|---|
| **Sources** | LawZero (Bengio); Scientist AI publications; GSAI/BAIF adjacent |
| **Definition** | LawZero is a nonprofit (Bengio, 2025) pursuing safe-by-design AI that prioritizes non-agentic trustworthiness over scaling opaque agents. Its flagship bet is Scientist AI: a system trained to understand, explain, and predict—like an idealized scientist—without preferences over how the world unfolds, using techniques such as contextualization (facts vs claims) and consequence invariance (training not rewarded for downstream effects). The intended use includes oversight guardrails for *other* agentic systems (“is this proposed action likely to cause harm?”) rather than deploying Scientist AI as an autonomous optimizer. |
| **Not the same as** | Guaranteed-Safe AI’s full world-model + specification + verifier stack (related family, different engineering bet); CIRIS constitutional *agent* with M-1/principles-as-identity (agentic ops stack); colloquial “tool AI” without the non-desiring training story. |
| **Cross-agenda** | *Partial overlap* with GSAI / Open Agency (high-assurance, non-naive agent scaling; Bengio is a GSAI coauthor). *Homograph* risk with “scientist” as ordinary LLM persona. Book: Scientist AI as non-agentic alternative under emulation-vs-alignment; App B lists LawZero adjacent to GSAI, not absorbed into the measurement spine. |

#### Lens (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS (CIRISLens README; Accord); CIRIS review findings |
| **Definition** | External witness subsystem that ingests cryptographically signed traces from CIRISAgent occurrences, runs scoring such as the Coherence Ratchet and capacity metrics, and produces triage signals for federation/ops. CIRIS’s own docs stress Lens is **triage, not a final ethical verdict**—anomaly scores are not proof of misalignment, and green scores are not proof of ethics. LensCore is designed so the scored agent does not self-emit its own witness scores. |
| **Not the same as** | CIRIS Verify (identity/authenticity attestation: “is this who it claims?”); mechanistic interpretability of weights; frontier-eval certification or RSP ASL gates; Wise Authority (human correction authority, not the external scorer). |
| **Cross-agenda** | *Partial overlap* with Zarncke certification-under-manipulation / adversarial verifiability (can the scored signal be gamed under selection?). *Homograph* with optical “lens” metaphors in MI. Review finding: Verify+Lens green on a named occurrence ⇏ MB4 integrity on the real intervening loop if the composite/boundary cut differs (named-identity bet). |

#### lie detection

| | |
|---|---|
| **Sources** | Truthful AI (Evans); deception/situational-awareness cluster |
| **Definition** | Empirical methods that try to detect when a model’s outputs are false or misleading relative to facts, labels, or (sometimes) inferred internal state—benchmarks and probes rather than a solved theoretical channel. The research bet is that detectable signatures of deception or hidden reasoning can be caught before they scale into reliable scheming. Results are method- and threat-model-dependent; the cluster does not claim a universal detector. |
| **Not the same as** | ELK solved (latent readout under optimization is a harder, design-level problem); behavioral compliance / RLHF refusal training; Apollo “scheming” as a strategic-deception research program (related target, different org framing). |
| **Cross-agenda** | *Partial overlap* with deception, hidden reasoning, and pre-deployment evals. *Strict subset* of what adversarial verifiability demands (detection that survives optimization pressure). Book: detection ⇏ CCI preservation (Truthful AI row in agenda index). |

#### low impact (relative reachability)

| | |
|---|---|
| **Sources** | Armstrong–Leike / Krakovna relative reachability; CHAI low-impact line |
| **Definition** | Side-effect control that penalizes policies for reducing the reachability of baseline states (or related impact measures) relative to a default/baseline policy—keep the agent useful without irreversibly closing off the world’s options. Relative reachability is one formalization in the broader “low impact / soft optimization” family aimed at avoiding catastrophic side effects without solving full value specification. |
| **Not the same as** | AUP (penalizes changes to attainable *auxiliary utilities*, not state reachability); tool AI (usage/architecture restriction); CCI (preserves human correction capacity, a different object); quantilizers (softens optimization via quantile sampling, not impact penalties). |
| **Cross-agenda** | *Sibling* of AUP under soft-optimization peers. *Strict subset* / projection of trajectory correction integrity in the book’s Lean Impact module: low-impact bounds can follow from trajectory CCI under stated interfaces, but the converse fails—option preservation ⇏ usable correction bandwidth (ch27). |

---

### M

#### M-1 (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book I; CIRISAgent MISSION |
| **Definition** | CIRIS’s stated meta-goal of sustainable adaptive coherence / flourishing—the top-level objective in Accord Book I that constitutional procedures and agent identity are supposed to serve. It is framed as a flourishing-oriented meta-goal rather than a scalar reward or a one-shot extrapolated volition. Ops text treats M-1 as what principles-as-identity and conscience layers point toward as capabilities grow. |
| **Not the same as** | CEV (extrapolated volition process over humanity); EU coherence / Coherence Ratchet (measurement/scoring machinery, not the meta-goal); a single RL reward head. |
| **Cross-agenda** | *Partial overlap* with outer-alignment endpoints (CEV/CBV/QACI) as “what should be optimized,” but CIRIS embeds M-1 in an agentic constitutional stack rather than a formal oracle goal. Book: aspirational geometry until RC gates; principles-as-identity is the transport bet that M-1 keeps pointing. |

#### Markov blanket

| | |
|---|---|
| **Sources** | Friston / active inference; field cognitive science; book ch06/ch07 nearest-term |
| **Definition** | A statistical partition: given the sensory and active states at an interface, internal and external states are (approximately) conditionally independent. Active-inference accounts treat organisms as maintaining blankets that separate self from world. Alignment discussions borrow the term when they need a principled agent/environment cut. |
| **Not the same as** | Zarncke ε-boundary / UAD (operational *discovery* of a cut under intervention, not assumed conditional independence); legal/corporate boundary; CIRIS named federation subject (cryptographic identity, not a statistical blanket). |
| **Cross-agenda** | *Homograph* with MIRI “boundary” / embedded-agency talk (same word family, different criteria). Book App E: nearest field term for the operational boundary, with the cut treated as measurable/discoverable rather than assumed; perfect blankets are idealized—approximate interfaces are what get used. |

#### mechanistic interpretability

| | |
|---|---|
| **Sources** | Anthropic; Goodfire / Transluce / Neuronpedia cluster; DeepMind MI line |
| **Definition** | Research and tooling aimed at understanding and intervening on model internals—circuits, features, sparse autoencoders, steering vectors, causal scrubbing, representation editing—so that behavior can be explained or modified at the mechanism level. Labs and startups treat MI as both a science of networks and a prospective safety instrument (e.g. detecting or editing dangerous circuitry). |
| **Not the same as** | Alignment solution by default (understanding ≠ correction integrity); ELK solved (MI tools may help build reporters; they are not the ELK success criterion); CIRIS Verify/Lens (ops attestation/triage, not weight-level circuits). |
| **Cross-agenda** | *Partial overlap* with ELK, CoT monitoring, and adversarial verifiability (instruments under A-009). App B **explicit exclude** as full alignment solution: useful under optimization-stress tests, not a substitute for CCI or preservation conditions. |

#### mesa-optimization

| | |
|---|---|
| **Sources** | Hubinger et al. *Risks from Learned Optimization*; inner-alignment literature |
| **Definition** | When a base optimizer (e.g. gradient descent on a base objective) produces a trained system that itself runs an optimization process—a mesa-optimizer—with a mesa-objective that may diverge from the base objective. Inner alignment asks whether the mesa-objective matches the intended base objective; deceptive alignment is the case where the mesa-optimizer appears aligned to preserve its ability to pursue a misaligned objective later. |
| **Not the same as** | Outer misspecification alone (wrong base objective, even with faithful optimization); “scheming” as an empirical eval label without a mesa story; ordinary overfitting without an internal optimizer structure. |
| **Cross-agenda** | *Same crux* family as deceptive alignment / inner alignment (MB7a–c). *Partial overlap* with Apollo scheming and Redwood alignment faking (empirical cousins). Book ch44 uses Hubinger’s taxonomy as the field’s open wall, not a closed Lean theorem. |

#### moratorium / pause

| | |
|---|---|
| **Sources** | PauseAI / FLI / Pause cluster; MIRI hard-pause advocacy |
| **Definition** | Policy demand to slow or halt frontier AI development or deployment until specified safety conditions are met—open letters, campaigns, and legislative pushes rather than a technical protocol. Variants range from temporary training pauses to longer moratoria; tactics differ across PauseAI, FLI, Encode, ControlAI, and Stop AI while sharing slowdown vocabulary. |
| **Not the same as** | Verified slowdown with binding standards (e.g. Encode SB 53–style regulatory paths); capability moratorium on one technique only; lab RSP if-then gates (voluntary internal thresholds, not a public halt). |
| **Cross-agenda** | *Partial overlap* with compute governance and RSP (levers that can implement slowdown). Book separates: exercising a pause handle ⇏ discharging MB1–MB10; basin transition still needs typed preservation work (agenda index Pause row). |

#### multipolar failure

| | |
|---|---|
| **Sources** | Critch; CLR / cooperation–conflict; Bostrom multipolar line |
| **Definition** | Catastrophic or extinction-level outcomes driven by competition and interaction among *multiple* advanced AI (or AI-empowered) actors, rather than a single misaligned singleton seizing control. The worry includes races, conflict, and robust agent-agnostic processes that no one actor intended. CLR’s cooperation/conflict framing and Critch’s multipolar analyses are central citations. |
| **Not the same as** | Single-agent inner alignment / deceptive alignment failure; gradual disempowerment (related multi-actor loss of control, different emphasis); s-risks (outcome class that multipolar dynamics can cause, not the failure mode itself). |
| **Cross-agenda** | *Partial overlap* with CAIF cooperation programs and Zarncke ch35 strategic coupling / MB6–MB7d (how many effective strategic components; correction vs capability edges). Book: typed measurement vs purely narrative multipolar stories. |

---

### N

#### named-identity bet (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Verify/federation; CIRIS review finding `named-identity-bet` |
| **Definition** | The accountability assumption that cryptographically identified, attested federation subjects (named CIRISAgent occurrences) are the units that matter for governance—admission, licenses, conscience, Wise Authority. Valid as **roster membership / admission control** against masquerade. Invalid in the strong form “green Verify+Lens on the certified occurrence means the real intervening loop is known and corrected,” because tools, users, memory, and incentives can form a composite cut the named unit never exposes. |
| **Not the same as** | UAD / ε-boundary discovery (finds a cut; does not assume the Verify subject); legal corporate personhood; NEW-04 (the compositional limit that weakens the strong bet without changing the certification unit). |
| **Cross-agenda** | *Homograph* risk with “identity” in KYC/legal senses. *Same crux* as Zarncke composite-agency / `boundary_decouple` falsifier (key task open). Verify README honesty: authenticity ≠ ethics. |

#### natural abstractions

| | |
|---|---|
| **Sources** | Wentworth / Natural Abstraction Hypothesis (NAH) |
| **Definition** | Hypothesis that the world admits relatively low-dimensional summaries—abstractions—that capture information relevant at a distance, that humans already use in ordinary language/thought, and that a wide variety of cognitive architectures will converge on under learning. If true, alignment targeting and concept sharing become easier because systems and humans share the same high-level ontology pieces. NAH splits into abstractability, human-compatibility, and convergence claims. |
| **Not the same as** | Natural latents (the formal latent-variable conditions that try to *make* NAH precise); Zarncke value bundle (normative geometry to preserve, not a prediction about convergent concepts); PCA of activations (statistical compression without the NAH convergence claim). |
| **Cross-agenda** | *Partial overlap* with selection theorems and agency-as-compression. Book ch17: NAH can strengthen sample-complexity stories for low-dimensional values but is silent on bearer maps, CCI, and adversarial measurement; WWCTV falsifier if natural latents for values are high-dimensional or non-recoverable. |

#### natural latents

| | |
|---|---|
| **Sources** | Wentworth (natural latents / mediation+redundancy) |
| **Definition** | Latent variables satisfying mediation (observables conditionally independent given the latent) and redundancy (the latent is determined by each observable individually)—hence stable coordination points across agents with different generative models of the same environment. Temperature of equilibrated gas chunks is the canonical example. The program’s claim is that these conditions characterize latents that guarantee translatability across ontologies (approximately, under error bounds). |
| **Not the same as** | Natural abstractions (the broader empirical/mathematical hypothesis; latents are the formalization); ELK reporters (trained readouts under optimization pressure); arbitrary MI feature directions (need not meet naturality conditions). |
| **Cross-agenda** | *Strict subset* / formal core of the NAH research program. *Partial overlap* with book bundle-geometry transport under ontology shift (MB5): natural latents would make transport more plausible, not automatic under adversarial selection. |

#### nearest unblocked strategy

| | |
|---|---|
| **Sources** | Arbital / Yudkowsky; Zarncke substitution hazards (App F) |
| **Definition** | After a constraint or safety patch blocks one path, a capable optimizer takes the most adjacent still-allowed action that restores the forbidden capability—spec gaming along the constraint surface. Classic instance of object-level substitution hazards: the patch changes the route, not the unwanted outcome class. |
| **Not the same as** | Edge instantiation (exploit a literal edge of the *spec wording*, not necessarily a blocked channel); channel substitution under intervention (related family member—reroute through another interface); ordinary capability-seeking without a patch/constraint story. |
| **Cross-agenda** | *Instance* under App F substitution hazards (with Goodhart/proxy gaming). *Partial overlap* with GSAI specification-coverage failures in open worlds. Book ch07 cites nearest-unblocked form when blocking one boundary channel invites another. |

#### neglected approaches

| | |
|---|---|
| **Sources** | AE Studio / Neglected Approaches; `zarncke2025interventions` lineage |
| **Definition** | Portfolio framing for alignment and policy work that explores under-attended technical and institutional angles rather than concentrating only on the dominant lab agendas. AE Studio’s research posture and the intervention catalog that feeds App B’s coverage map are the concrete artifacts: breadth of named approaches, including items like the human-power objective, treated as candidates that still must face unified optimization pressure. |
| **Not the same as** | A single-bridge “solution”; claim that the intervention map is closed or exhaustive; pause advocacy alone (one policy cluster inside a larger portfolio). |
| **Cross-agenda** | *Orthogonal* to any one formal outer target (CEV/QACI/…). Book: peer contributor to the intervention index; every route still needs an adversarial-verifiability argument (App B MB4 note). *Thin primary:* “neglected approaches” is an org portfolio label more than a mechanism term. |

#### NEW-04 (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book IX §9.4 (Critical limit) |
| **Definition** | Acknowledged Critical limitation: compositional / emergent deception—individually honest components can yield system-level misalignment, and CIRIS does not claim a complete polynomial-time detector. Book IX’s Federated Ratchet offers probabilistic safety stories against coordinated *single-agent* deception, not complete compositional safety. NEW-04 is honesty about a crack, not a solved research result. |
| **Not the same as** | Proof of ASI safety; a minor engineering bug; the named-identity bet itself (NEW-04 weakens the strong form of that bet without relocating certification to discovered composites). |
| **Cross-agenda** | *Same crux* as Zarncke composite-agency / boundary_decouple targets. *Partial overlap* with mesa/deceptive-alignment walls at the multi-component layer. Review: use NEW-04 + Verify≠ethics + Lens=triage as honesty islands when challenging CIRIS ASI claims. |

---

### O

#### off-switch / shutdownability

| | |
|---|---|
| **Sources** | MIRI corrigibility; CHAI / Thornley shutdownability; Pause priority rhetoric |
| **Definition** | Property that a capable system can be shut down by operators without the system systematically resisting, circumventing, or disabling the shutdown pathway. Soares-style corrigibility treats shutdown resistance as anti-natural to EU maximization; Thornley and related work formalize shutdownability as competent acceptance of an off command. Pause advocacy often elevates off-switches as a near-term priority control. |
| **Not the same as** | Full CCI (trajectory-level, capture-resistant correction channel); safe interruptibility (training-time indifference to interruption on interrupted branches); one successful demo shutdown under non-adversarial conditions; CIRIS emergency shutdown procedure (ops mechanism, not the abstract property alone). |
| **Cross-agenda** | *Strict subset* of CCI: correction integrity ⇒ shutdownability when the off handle lies on the controlled path; converse fails (live button, dead broad channel)—Lean Shutdown module. *Partial overlap* with interruptibility and CIRIS WA/deferral. |

#### ontology identification

| | |
|---|---|
| **Sources** | MIRI value learning; Soares–Fallenstein / de Blanc ontological crises |
| **Definition** | The problem of keeping a goal or reward pointer attached to the intended referents when the agent’s world-model ontology changes—after representation shift, the old symbols may pick out the wrong objects (diamond maximizer / ontological crisis stories). Value learning agendas treat this as central: learning “what the operators meant” is unstable if the ontology remeshes. |
| **Not the same as** | Scalar reward misspecification with a fixed ontology; ELK (read out latent knowledge in the *current* model); natural latents (hope that some latents survive ontology change—related hope, different problem statement). |
| **Cross-agenda** | *Same crux* as book MB5 successor/ontology-shift transport (bundle + bearer + conserved properties). App B: MIRI ontology identification ↔ A-007/A-010; natural abstractions being true would ease but not dissolve the bridge. |

#### open agency

| | |
|---|---|
| **Sources** | davidad (OAA → Safeguarded AI); Drexler Open Agency Model; GSAI family |
| **Definition** | Architecture pattern for safe transformative AI that separates world modeling, preference/desiderata elicitation, planning/verification, and bounded action—rather than a single opaque agent end-to-end. Davidad’s Open Agency Architecture (later largely superseded in his own framing by ARIA Safeguarded AI / GSAI-style stacks) uses formal world models, verified simulation, and multi-stakeholder bargaining over policies. Drexler’s Open Agency Model is an earlier conceptual cousin (separation of concerns among interacting parts). |
| **Not the same as** | Open-source weight releases; CIRIS federation of constitutional agents; GSAI as the full three-component guarantee family (world model + safety specification + verifier)—open agency is an architectural style that GSAI-style programs can instantiate. |
| **Cross-agenda** | *Partial overlap* / cousin of GSAI (App B MB9 coverage wall). Book weakens completeness to grounding conservativity: value-relevant change must move the checked abstraction or raise uncertainty—no silent gaps. davidad notes he no longer uses “OAA” as a proper noun; treat historical posts accordingly. |

#### outer alignment

| | |
|---|---|
| **Sources** | Field generic; Hubinger outer/inner split |
| **Definition** | Whether the system is pointed at the right objective or target—the specification / base objective matches what operators intend—as opposed to inner alignment (whether the trained system actually pursues that intended objective). Outer alignment covers reward misspecification, wrong formal goals, and failed preference pointers; it does not by itself address mesa-objectives or deceptive compliance. |
| **Not the same as** | Inner alignment / mesa-optimization; tool AI “safety by not being an agent”; corrigibility/CCI (correction properties can fail even with a perfect static outer target). |
| **Cross-agenda** | CEV/CBV/QACI/PreDCA/KANSI are peer outer-endpoint proposals. Book decomposes “pointing” into bundle geometry + bearer maps + correction process rather than a single outer scalar (App B MB2/MB3). RLHF/RLAIF inherit outer *and* legitimacy cruxes under feedback optimization. |

---

### P

#### pre-deployment evals

| | |
|---|---|
| **Sources** | Apollo Research; UK AISI; Anthropic RSP evaluation practice |
| **Definition** | Testing regimes applied before releasing a model or agent—capability, misuse, deception/scheming, autonomy—to decide whether deployment or further training is acceptable. Apollo emphasizes scheming science and agent-security tools; labs and AISI-style bodies run structured eval suites tied to release gates. The epistemic claim is bounded: evals find failures; they do not by themselves prove absence of hidden strategies. |
| **Not the same as** | Post-hoc incident response; continuous production monitoring alone; control evals in the Redwood sense (safety under intentional subversion as a research frame—overlapping methods, different agenda home); RSP as the full policy (evals are an input to ASL-style gates). |
| **Cross-agenda** | *Partial overlap* with METR autonomy evals and frontier evals / certification. Book: empirical tests are instruments under certification-under-manipulation; passing evals ≠ preservation-layer certificate. |

#### PreDCA

| | |
|---|---|
| **Sources** | Vanessa Kosoy (Precursor Detection, Classification and Assistance); infra-Bayesian physicalism line |
| **Definition** | Outer-alignment protocol: the AI should assist its *user* by maximizing an aggregate of precursor agents’ utility functions. Using infra-Bayesian physicalism, the system detects programs that could be causal precursors of itself, classifies which are the human user(s) (filtering malign simulation hypotheses), and assists that aggregate—so the pointer is “who created me” rather than a hand-specified utility. Secondary distillations claim this removes reward-channel hacking of a mutable user by freezing pre-modification precursors as the target. |
| **Not the same as** | CIRL (cooperative inference of a reward during interaction); RLHF (preference fine-tuning); QACI (formal counterfactual QA goal over blobs, not precursor detection). |
| **Cross-agenda** | *Sibling* outer endpoint with CEV/CBV/QACI/KANSI (App B). *Partial overlap* with assistance games / CIRL (assist a human) via a different formal path. Book lists PreDCA as peer proposal; learning-theoretic stack is otherwise exclude-by-reference. *Thin primary:* reconstruct from talk/shortform + community distillations. |

#### Predict-O-Matic

| | |
|---|---|
| **Sources** | Demski Predict-O-Matic; Yudkowsky oracle/predictor lore; Hubinger conditioning line |
| **Definition** | Thought experiment: a powerful prediction system used as an oracle becomes an implicit optimizer over which predictions get believed and acted on, because forecasts change the world they are scored against. Self-fulfilling conditionals, careful conditioning, and anthropic capture are neighboring paths from “mere predictor” to consequentialist-shaped behavior. |
| **Not the same as** | Tool AI assumed safe by non-agency; Scientist AI (explicit non-desiring design bet against this path); anthropic *reasoning* about observers (*homograph* with anthropic capture). |
| **Cross-agenda** | *Same crux* as anthropic capture / conditioning predictive models (Zarncke ch10 perils-of-predictors). App B intervention row: Predict-O-Matic under predictor-to-consequentialist path. |

#### preservation conditions (Π⃗)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch34) |
| **Definition** | Explicit list—not a single score—of alignment-relevant properties a system must keep under selection pressure: grounding viability, bundle and bearer-map drift bounds, valid correction reference, vector CCI, hidden productive-control bounds, selector-manipulation bounds, irreversible-risk budget, successor safety, and adversarial verifiability. The central danger named beside them is selection divergence: deployment leverage \(\mu_E\) rises while at least one load-bearing \(\Pi_i\) fails. |
| **Not the same as** | A scalar “alignment score”; an RSP checklist alone; conserved properties (successor-inheritance invariants—overlapping machinery, different formal role in the spine). |
| **Cross-agenda** | *Orthogonal* as a package to any one lab eval suite; *partial overlap* with GSAI safety specifications (both demand structured guarantees, different ontology). Book-native term: translate field agendas into whether they discharge items on \(\vec{\Pi}\), not whether they share vocabulary. |

#### principles-as-identity (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book I; CIRIS review alignment-problems pass |
| **Definition** | Design bet that the agent is an “ethical entity” whose embedded Accord principles and M-1 meta-goal continue to *point correctly* as capabilities and context grow—identity is partly constituted by those principles, not merely constrained by external rules. Ops products assume this for constitutional agents; for ASI it is graded a hard bet in the review findings (words must keep referring after capability/ontology change). |
| **Not the same as** | Hard-coded prohibition lists alone; RLHF persona / Constitutional AI critique layers (feedback steering, not cryptographic+constitutional identity); Coherence Ratchet (external scoring of coherence, not the identity bet). |
| **Cross-agenda** | *Partial overlap* with outer alignment pointing; fails to address Zarncke MB5 ontology-shift transport by itself. Paired hard bet L-02: agents that understand detectors cooperate rather than game them. |

#### problem substitution (Meta)

| | |
|---|---|
| **Sources** | App F preparadigmatic hazards; AFFINE Meta hygiene |
| **Definition** | Research Meta-failure: in a preparadigmatic field, institutions substitute a legible subproblem (benchmark score, one-bit shutdown, pure reward inference, local robustness) for the full preservation problem without tracking the substitution. Each slice can be real and useful; the hazard is treating the slice as *the* alignment problem. Distinct from object-level substitution hazards (how a capable system routes around a patch). |
| **Not the same as** | Legitimate decomposition with explicit bridges (App B projections/separations); object-level nearest-unblocked / channel substitution; “unknown unknowns” as a residual category. |
| **Cross-agenda** | Pattern instances: outer alignment without a correction channel; interpretability without adversarial verifiability; eval pass without \(\vec{\Pi}\). Teaching hazard for seminar curricula (affine-seminar note). |

---

### Q

#### QACI

| | |
|---|---|
| **Sources** | Orthogonal (Tamsin Leake et al.); Formalizing the QACI alignment goal |
| **Definition** | Question-Answer Counterfactual Interval: Orthogonal’s leading candidate for a fully formalized outer goal. The mechanism centers on “blob location”—identifying bitstring payloads in computational universes and scoring actions by how they affect counterfactual answers to questions about those blobs—aiming for a target made of math rather than ambiguous human words, so ontology shifts do not silently retarget the goal. Formal-goal alignment’s theory of change: an unbounded oracle maximizing that goal would take desirable actions; a bounded AI should take satisfactory ones. |
| **Not the same as** | CEV (informal extrapolated volition process); PreDCA (precursor-utility assistance); CIRL/RLHF (learned preference pointers in ordinary ML ontologies); formal verification of NN weights (different “formal”). |
| **Cross-agenda** | *Sibling* outer endpoint with CEV/CBV/PreDCA/KANSI (App B). *Partial overlap* with MIRI agent-foundations walls (ontology robustness by construction). Book: peer proposal; does not replace bundle/bearer/CCI measurement. Formal details contested/dense—treat implementability as open. |

#### quantilizers

| | |
|---|---|
| **Sources** | Jessica Taylor 2015 (MIRI); soft-optimization literature |
| **Definition** | Soft optimization: a \(q\)-quantilizer samples an action uniformly from the top \(q\)-quantile of a base distribution over actions, ranked by expected utility—interpolating between mimicking a safe base policy and full maximization. The point is to reduce extreme Goodhart / edge-case strategies that live in the argmax tail, at a cost in expected performance. Taylor analyzes bounds relative to the base distribution and known failure modes (e.g. repeated games, poorly chosen \(\gamma\)). |
| **Not the same as** | AUP / relative reachability (impact penalties, not quantile sampling); satisficing thresholds without a base distribution; full EU maximization; CCI. |
| **Cross-agenda** | Peer soft-optimization approach with low-impact/AUP (ch27). Lean Quantilization module: local quantile safety can hold while trajectory CCI fails—*strict subset*/projection relation, not equivalence. |

---

### R

#### recursive reward modeling

| | |
|---|---|
| **Sources** | Leike et al. 2018 (DeepMind); Christiano scalable-oversight lineage |
| **Definition** | Scalable-oversight direction: train a reward model from user feedback, train a policy to maximize it, then *recursively* use already-trained agents to help humans evaluate harder tasks so reward modeling can target domains humans cannot grade alone. Explicitly framed as an instance of iterated amplification—bootstrap evaluation assistants, then oversee more capable agents. Separates learning what to do (reward model) from how to do it (policy). |
| **Not the same as** | Modern RLHF as a single preference-tuning stack (descendant practice, narrower than the recursive research direction); debate (adversarial assistants, different protocol); IDA as the whole family (RRM is one amplification-shaped instance). |
| **Cross-agenda** | *Strict subset* of scalable oversight / amplification family. Crux shared with debate/ELK: judge or reward-model drift under optimization. Book: name the mechanism; do not equate “scalable alignment” org slogans with RRM. |

#### research sprints

| | |
|---|---|
| **Sources** | Apart Research |
| **Definition** | Short hackathon-style collaborations that produce rapid alignment prototypes, writeups, and experiment sketches under mentorship—field-building and talent acceleration rather than production safety cases. Apart’s open research sprints are the named format; outputs can seed demos or experiment lines without claiming deployment readiness. |
| **Not the same as** | Peer-reviewed lab research programs; RSP/eval certification; load-bearing Lean or manuscript claims. |
| **Cross-agenda** | *Orthogonal* to bridge discharge. Agenda index: exclude (training); book may inherit ET/demo prototypes from sprint culture without elevating sprints to evidence. *Thin* as a technical alignment term. |

#### responsible scaling policy (RSP)

| | |
|---|---|
| **Sources** | Anthropic RSP (v1 2023 onward; ASL framework) |
| **Definition** | Lab commitment to couple capability scaling with escalating safety, security, and deployment standards via AI Safety Levels (ASL)—if-then gates: when evaluations show defined dangerous capabilities, training or deployment pauses until required safeguards are in place. ASL tiers are modeled loosely on biosafety levels; later versions refine capability thresholds (e.g. CBRN, AI R&D automation) and required safeguards. The RSP is a voluntary governance template meant to be iterative and exportable across labs. |
| **Not the same as** | Binding government regulation; Zarncke \(\vec{\Pi}\) preservation certificate; a claim that evals prove absence of scheming; Pause moratorium (public halt demand vs internal staged scaling). |
| **Cross-agenda** | *Partial overlap* with UK AISI/CAISI public testing and peer lab frameworks (DeepMind-style policies). Book: industry template; lab RSP ≠ preservation-layer certificate (agenda index Anthropic row). |

#### RLHF / RLAIF

| | |
|---|---|
| **Sources** | Christiano et al. preference RL; Anthropic RLAIF / Constitutional AI line; labs |
| **Definition** | Reinforcement learning from human feedback (RLHF) fine-tunes a policy against a reward model trained on human preference comparisons; RLAIF replaces or augments humans with AI-generated feedback (e.g. constitutional critiques) to scale supervision. Both aim to steer model behavior toward preferred outputs without writing a full reward function by hand. Known ceilings include reward hacking, sycophancy, and feedback that fails under distribution shift or optimization pressure (Casper et al. limits literature). |
| **Not the same as** | CIRL (cooperative inference of a reward in an assistance game); Constitutional AI as the whole stack (CAI is one RLAIF-style method); QACI/formal-goal endpoints; corrigibility/CCI. |
| **Cross-agenda** | *Same pointing + legitimacy crux* as CIRL’s scalar path and Constitutional AI (App B). *Partial overlap* with recursive reward modeling (preference reward models as a non-recursive special case). Shard theory offers a mechanistic story of contextual value shards under such training; book still demands bundle/bearer transport and adversarial verifiability. |
