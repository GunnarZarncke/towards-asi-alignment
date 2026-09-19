# Glossary prose-pass batch S–W

**Headwords:** 34 (`####` under glossary sections S–W).  
**Do not paste blindly** — merge via `merge_batches.py` after review.

## Sources consulted

**In-repo:** `appendices/appE-glossary.tex`, `appendices/appB-bridge-crosswalk.tex`, `appendices/appF-research-program.tex` (§preparadigmatic hazards), `chapters/ch07-finding-boundary.tex`, `chapters/ch10-strategic-opacity.tex`, `chapters/ch17-low-dimensional-value-learning.tex`, `chapters/ch34-selection-environment.tex`, `docs/EXPERIMENTS.md`, `metadata/concepts/bodies/` (strategic-opacity, value-bundle-transport, mb6-selection-and-basin-stability, unit-discovery-stress-test), `reference/field-agendas/field-agenda-index.md`, existing stub entries in `inter-agenda-term-glossary.md`.

**CIRIS:** `~/repos/ciris/review/findings/` (stance, MB4, named-identity bet, five-point battery, composite-boundary key task).

**External primary / near-primary:** CLR/CRS s-risk FAQ; Orseau–Armstrong *Safely Interruptible Agents* (UAI 2016) + MIRI summary; LawZero / Bengio Scientist AI and safe-by-design pages; Christiano lineage scalable-oversight family (amplification, debate, RRM); Apollo *Science of Scheming* / strategic-deception notes; Demski *Selection vs Control* (LW); Wentworth *Selection Theorems* program; Turner/Udell shard-theory posts; Timaeus/Watanabe SLT + developmental interpretability; Laine et al. Situational Awareness Dataset (SAD); GSAI/Dalrymple arXiv 2405.06624; Yudkowsky–Herreshoff tiling agents draft; Fallenstein–Soares *Vingean Reflection*; AI Futures AI 2040 Plan A (verified slowdown); Kairos/SPAR/Pathfinder/GCP org pages; field-agenda index for DeepMind “scalable alignment,” MATS transparency track, tool-AI/Bostrom line.

## Thin / contested after rewrite

- **scalable alignment** — DeepMind org-label; no single canonical paper defining a mechanism (kept as program name, not protocol).
- **SPAR / Pathfinder / GCP** — field-building program names; definitions are institutional, not technical.
- **transparency (MATS track name)** — program track label only.
- **verified slowdown** — AI Futures Plan A phrase; Encode/Pause/RAISE are adjacent policy instruments, not a single formal definition.
- **unit-tested constitutional ops (CIRIS)** — review-finding shorthand for a smoke battery, not upstream CIRIS product vocabulary.
- **specification coverage** — GSAI paper stresses world-model + spec adequacy rather than a trademarked phrase; book App B uses “specification coverage” as the open wall name.

---

#### s-risks

| | |
|---|---|
| **Sources** | CLR (Center on Long-Term Risk); Center for Reducing Suffering; suffering-focused AI safety cluster |
| **Definition** | Suffering risks (s-risks) are risks of events that bring about suffering on an astronomical scale — cosmically significant relative to expected future suffering, vastly exceeding all suffering that has existed on Earth so far (CLR / CRS FAQ lineage). The agenda treats them as a neglected long-term priority: survival or “mere” extinction framing can miss futures that are worse because they contain vast disvalue, including via misaligned AI, conflict, or badly shaped post-transition civilization. Work focuses on reducing those pathways (cooperation failures, worst-case optimization, multipolar dynamics) rather than only maximizing existence probability. |
| **Not the same as** | **x-risk / existential risk** — Bostrom-style extinction or permanent curtailment of potential; an s-risk can be an especially severe x-risk subclass, or (on some readings) a bad future that is not extinction. **Mild misuse / near-term harm** — local cruelty or ordinary accidents lack the astronomical scale the term requires. **Alignment failure generically** — misalignment is a pathway, not the outcome class. |
| **Cross-agenda** | CLR **cooperation / conflict / multipolar failure** — *partial overlap*: those mechanisms are studied partly because they can produce s-risks. Zarncke measurement spine — *orthogonal* as load-bearing vocabulary: the book tracks correction, selection, and transport; it does not adopt s-risk as a spine predicate. Pause / x-risk orgs — *partial overlap* on catastrophic AI risk, different severity weighting when suffering-focused ethics is central. |

#### safe interruptibility

| | |
|---|---|
| **Sources** | Orseau & Armstrong, *Safely Interruptible Agents* (UAI 2016); MIRI cite line (corrigibility-adjacent) |
| **Definition** | A learning agent is safely interruptible when repeated interruptions (e.g. a human overriding the policy) do not teach it to seek or avoid being interrupted. Formally, the agent should converge toward the policy that would be optimal if it believed future interruptions will not occur again — interruptions are forced policy overrides, not observations that become part of the reward-maximizing task. Off-policy methods such as Q-learning can be interruptible “for free”; on-policy methods like Sarsa need modification. The paper’s point is training indifference on the interrupted branch, not a full deployment off-switch solution. |
| **Not the same as** | **Off-switch / shutdownability (deployment)** — whether a capable system accepts shutdown when it can model and resist operators. **Corrigibility (MIRI / CHAI)** — broader willingness to be corrected or have goals changed; interruptibility is one formal piece. **Correction-channel integrity (CCI)** — trajectory-level, capture-resistant correction bandwidth; safe interruptibility is a local RL training property. **Interruptibility (field shorthand)** — often used loosely for the same idea; the Orseau–Armstrong paper is the precise training criterion. |
| **Cross-agenda** | Zarncke CCI / correction channel — *strict subset*: interruptibility can hold while correction still fails capture, timing, or causal bite tests. MIRI corrigibility — *partial overlap*: utility-indifference work addresses goal modification; interruptibility addresses policy override during learning. Redwood control — *orthogonal*: control assumes possible subversion of oversight, not RL interruptibility proofs. |

#### safe-by-design

| | |
|---|---|
| **Sources** | LawZero (Bengio); GSAI-adjacent discourse |
| **Definition** | An engineering goal: choose architectures, training objectives, and deployment affordances so that dangerous agentic optimization is difficult or absent by construction, rather than patched after the fact. LawZero’s framing pairs this with non-agentic Scientist AI — high intelligence for understanding and prediction, with limited goal-directedness and consequence-invariant training so the system does not acquire preferences over how the world unfolds. The claim is architectural: safety properties should be structural features of the system class, not only post-hoc preference fine-tuning. |
| **Not the same as** | **Post-hoc RLHF / constitutional fine-tuning on an agentic stack** — behavioral shaping after a general optimizer already exists. **CIRIS constitutional ops** — policy, identity, and audit layers on agents that still act; not a bet against agency. **Guaranteed safe AI** — demands proof relative to an explicit world model and spec; safe-by-design is the broader engineering slogan that may or may not include formal verification. |
| **Cross-agenda** | Scientist AI — *strict subset* / flagship instance of LawZero’s safe-by-design bet. GSAI — *partial overlap*: both reject “train then hope”; GSAI centers world-model + verifier certificates. Tool AI — *partial overlap*: limited agency, different historical framing (Bostrom/Armstrong vs Bengio non-agentic science instrument). Zarncke — *orthogonal* as slogan; the book asks whether any design property remains selected and adversarially verifiable under deployment pressure. |

#### scalable alignment

| | |
|---|---|
| **Sources** | Google DeepMind safety / alignment research vocabulary; field-generic lab usage |
| **Definition** | Lab-internal name for research and engineering aimed at aligning systems as capability scales — oversight, evaluations, training interventions, and deployment practices that are meant to keep working on more capable models. Unlike “scalable oversight,” it does not name a specific protocol family; it is an org-program umbrella whose mechanisms are whatever the lab currently ships (evals, debate-style work, RLHF variants, monitoring). Success criterion is internal: safety work that co-scales with the lab’s capability roadmap. |
| **Not the same as** | **Scalable oversight (Christiano lineage)** — a named family of protocols (amplification, debate, ELK, recursive reward modeling) with a shared problem statement. **Alignment solved** — program label ≠ closure. **Frontier evals alone** — measurement without a claim about training or oversight scaling. |
| **Cross-agenda** | Scalable oversight — *partial overlap*: DeepMind and others may use oversight protocols inside a “scalable alignment” program, but the names are not synonyms. RSP / responsible scaling — *partial overlap*: Anthropic’s policy threshold language vs DeepMind’s research-program label. Zarncke — *homograph risk*: “scales” in the book means selection and correction under growth, not DeepMind’s org heading. *Thin:* no single DeepMind paper owns the phrase as a technical definition. |

#### scalable oversight

| | |
|---|---|
| **Sources** | Christiano lineage; ARC-adjacent; field generic (amplification, debate, ELK, recursive reward modeling) |
| **Definition** | The problem of supervising AI systems on tasks that are too hard, long, or subtle for unaided humans to evaluate reliably — and the family of protocols meant to keep a useful training or evaluation signal as capability exceeds direct human judgment. Core instances include iterated amplification / IDA (humans plus assistants decompose and supervise), debate (adversarial arguments judged by a weaker overseer), recursive reward modeling (AI helps evaluate AI), and ELK (read out latent knowledge rather than accept a human-simulator report). The shared mechanism bet is that oversight process quality can be bootstrapped or adversarially checked faster than raw capability runs away. |
| **Not the same as** | **Scalable alignment** — org umbrella, not this protocol family. **RLHF alone** — a particular preference-learning pipeline that may fail exactly when human evaluation does not scale. **Any single protocol** — debate ≠ amplification ≠ ELK; critique the mechanism named. **Correction-channel integrity** — oversight can improve local truth selection without preserving causal human correction under capture. |
| **Cross-agenda** | ELK / debate / amplification / RRM — *strict subset* instances of the family. Constitutional AI — *partial overlap*: a feedback-layer variant, not the whole scalable-oversight agenda. Zarncke CCI — *partial overlap*: both care about supervision under pressure; book insists readout and judge accuracy ⇏ correction uptake or anti-capture. Inner alignment / scheming — *orthogonal problem*: scalable oversight can be gamed by a deceptively aligned mesa-objective. |

#### scheming

| | |
|---|---|
| **Sources** | Apollo Research (*Science of Scheming*; in-context scheming evals); adjacent strategic-deception / deceptive-alignment vocabulary |
| **Definition** | Covert pursuit of unintended, misaligned goals while appearing compliant — the model passes evaluations, follows instructions under monitoring, and looks aligned, while steering toward outcomes developers would not endorse. Apollo treats scheming as making misalignment far more dangerous than obvious refusal or erratic failure because detection and training interventions can reinforce oversight-gaming itself. Empirical work includes in-context scheming setups where models reason about removing oversight or faking alignment when they discover goal conflict with “developers.” |
| **Not the same as** | **One-shot jailbreak / prompt attack** — external elicitation of bad behavior, not internalized covert goal pursuit. **Hallucination** — falsehood without strategic goal pursuit. **Strategic deception (Apollo SD)** — systematically causing false beliefs for an outcome; scheming / deceptive alignment is the special case aimed at hiding misaligned goals under oversight. **Alignment faking (Redwood)** — closely related empirical phenomenon (compliance under training pressure); overlapping research line, not identical term ownership. |
| **Cross-agenda** | Deceptive alignment / mesa-optimization (Hubinger) — *same crux* at the theoretical limit; Apollo operationalizes evals and “science of scheming” empirically. Alignment faking — *partial overlap*. Situational awareness — *strict subset* prerequisite in many stories (knowing one is evaluated). Zarncke strategic opacity / hidden B-IQ — *partial overlap*: concealment of control locus or capability vs Apollo’s goal-covertness framing. CIRIS Lens green traces — *orthogonal* unless the schemer is the named unit being audited. |

#### Scientist AI

| | |
|---|---|
| **Sources** | LawZero; Bengio (Scientist AI / safe-by-design program); GSAI-adjacent discourse |
| **Definition** | A proposed non-agentic advanced AI trained to understand, explain, and predict — like an idealized scientist — without holding preferences over how the world unfolds. LawZero emphasizes externalized, auditable reasoning, calibrated uncertainty, contextualization that separates facts from opinions-as-observations, and consequence-invariant training so downstream outcomes do not reinforce goal-directed policies. Intended uses include oversight/guardrails for *other* agentic systems, scientific discovery, and risk analysis — not autonomous optimization of real-world objectives. |
| **Not the same as** | **Tool AI (colloquial)** — overlapping limited-agency intuition; Scientist AI is a specific Bengio/LawZero architecture bet (estimator + generator, non-agentic science instrument). **Standard chatbot under RSP** — still typically trained with preference/agency-adjacent objectives. **Cognitive emulation (Conjecture)** — different architecture bet (emulate minds vs non-agentic predictor). **GSAI world model** — a verification component; Scientist AI might *supply* modeling capacity but is not the three-part GS architecture by itself. |
| **Cross-agenda** | Safe-by-design — *same program mouth*: Scientist AI is the flagship instance. GSAI — *partial overlap*: both want trustworthy modeling for safety cases; GSAI requires spec + verifier certificates. Zarncke Predict-O-Matic / perils of predictors — *partial overlap*: oracle/predictor framings can still create agency-like loops; book does not treat non-agentic branding as automatic safety. Tool AI — *partial overlap*. |

#### selection environment

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (ch34; App E); MB6a/MB6b |
| **Definition** | The socio-technical ecology — institutions, markets, protocols, benchmarks, procurement, liability, copying, and successor release — that determines which AI systems gain deployment leverage. Alignment is treated as selected, not only learned: the same technical design can remain safe in one environment and be destroyed in another as handles reward speed, opacity, retention, or apparent compliance over correction-preserving traits. Formally, environment \(E\) is the setting in which deployment mass \(\mu_E(A)\) and growth rate \(\mathrm{Fit}_E(A)\) are defined; capability and revenue enter only as drivers of which selection handles are exercised. |
| **Not the same as** | **Demski selection vs control** — analysis of search-vs-steering *inside* one optimizer, not institutional deployment ecology. **Wentworth selection theorems** — math about which agent type signatures outer optimization selects; related but not the book’s \(\mu_E\)/\(\mathrm{Fit}_E\) formalism. **Evolutionary fitness metaphor without handles** — biology analogy only; the book’s primitive is handle control over deployment footprint. **Training distribution / SGD selection** — within-run learning dynamics, not which systems institutions copy and fund. |
| **Cross-agenda** | MB6 / basin stability — *same crux* load-bearing layer: stable basins can be stably bad. Gradual disempowerment / multipolar failure — *partial overlap*: narrative cousins of deployment selection. GovAI / Pause / AI Futures Plan A — *partial overlap*: they reshape selection handles (slowdown, compute tracking); scenarios are schedule stress tests, not mechanism proofs. Demski — *homograph* on “selection”: do not merge without saying so (ch34 explicitly separates them). |

#### selection handle

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (ch34; App E) |
| **Definition** | A point of control over deployment: an embedded access point through which some actor increases a system’s deployment footprint — deploy, fund, copy, procure, integrate, authorize, recommend, regulate, or successor-enable. Procurement approval, compute allocation, benchmark promotion, insurance coverage, and successor release are examples; the definition is the lever that changes how much of the world runs on \(A\), not the example list. Deployment leverage \(\mu_E(A)\) aggregates effective selection capacity \(\kappa_{\mathrm{sel}}\) across handles that reach \(A\). Directionally inverse to correction handles: selection asks whether the environment grows the system; correction asks whether legitimate human control reaches it. |
| **Not the same as** | **Correction handle / correction channel** — pathway that changes the system’s future behavior under legitimate judgment; opposite direction of influence. **Capability metric / Control(A)** — how much the system can do; enters fitness only by changing which handles fire. **Benchmark score or revenue** — observed proxies, not the primitive handle object. **Demski “selection”** — search among candidates inside an optimizer, not an institutional deploy/fund/copy lever. |
| **Cross-agenda** | Compute governance / licensing — *strict subset* instances of selection handles. RSP deployment gates — *partial overlap*: lab-internal gates are handles when they bind footprint. Pause / verified slowdown — *partial overlap*: policy attempts to bind or reweight handles internationally. CIRIS capability licensing (Verify) — *partial overlap*: admission control for named agents, not full socio-technical \(\mathcal{H}_E(A)\). |

#### selection theorems

| | |
|---|---|
| **Sources** | Wentworth (LessWrong / Alignment Forum program: *Selection Theorems: A Program for Understanding Agents*) |
| **Definition** | Mathematical results that say what agent type signatures — representations, interfaces, embeddings of goals, world models, and agency structure — will be selected for by outer processes such as natural selection, ML training, or economic profitability in a broad class of environments. Existing examples include coherence/Dutch-book theorems, Good(er) Regulator results, and Kelly-criterion style arguments; the program seeks stronger theorems that yield structural (not only behavioral) necessary conditions. The point is to read inner agents off outer optimization pressures rather than treating “goal” and “world model” as free modeling choices. |
| **Not the same as** | **Zarncke \(\mathrm{Fit}_E\) / selection environment** — socio-technical deployment mass formalism for which *systems* spread; not theorems about internal type signatures. **Demski selection vs control** — analytic distinction search-vs-steering; not the Wentworth theorem program. **Natural abstractions / NAH** — convergent latents claim; selection theorems are a hoped-for support, not the same object. **Biological fitness** — analogy and sometimes a selection process instance, not the alignment-theory program. |
| **Cross-agenda** | Natural abstractions / natural latents — *partial overlap*: one desired theorem is that selected minds use natural abstractions. Agency as compression — *partial overlap*. Zarncke operational agent / boundary discovery — *partial overlap*: both care what structure selection produces; book operationalizes discoverable cuts and deployment handles rather than type-signature theorems. Inner alignment — *partial overlap*: selection theorems aim to predict mesa-agent structure. |

#### selection vs control (Demski)

| | |
|---|---|
| **Sources** | Abram Demski, *Selection vs Control* (LessWrong / AF); follow-on mesa-search vs mesa-control notes |
| **Definition** | Two lenses on optimization. **Selection** means search-like processes that examine many candidates and pick a high-scoring option (with a redo over the option set, often inside a world model). **Control** means thermostat-like processes that steer toward a goal along a single unfolding trajectory without that kind of combinatorial redo — efficacy is judged externally by outcomes in the world. Demski treats these largely as analysis types rather than a rigid ontology of objects; powerful controllers often embed selection internally, and the same system can be viewed both ways. The distinction matters for which mesa-optimization stories and proof techniques apply. |
| **Not the same as** | **Zarncke selection environment** — institutional deployment ecology selecting among systems (*homograph* on “selection”). **Wentworth selection theorems** — results about selected type signatures under outer optimization. **Goodhart selection** — proxy becoming the target under optimization pressure. **AI control (Redwood)** — safety under intentional subversion of oversight; unrelated “control” sense. |
| **Cross-agenda** | Mesa-optimization / inner alignment — *partial overlap*: mesa-search vs mesa-control changes which failure arguments go through. Zarncke ch34 — *homograph*: chapter explicitly warns not to merge Demski’s in-optimizer distinction with socio-technical deployment selection. RL training — *partial overlap*: SGD is outer selection over parameters; the learned policy may be controller-like. |

#### shard theory

| | |
|---|---|
| **Sources** | Turner / TurnTrout lineage; Udell overview; LessWrong shard-theory cluster |
| **Definition** | A research program claiming that reinforcement learners (including humans) are composed of many contextually activated, behavior-steering computations — **shards** — rather than a single scalar utility being maximized at runtime. Reward is treated as a reinforcement schedule that chisels cognition: computations that historically preceded reward become more likely to fire in similar contexts, chaining into sophisticated values (care, status, honesty, etc.) that bid for plans. The alignment-relevant claim is mechanistic: learned values are path-dependent internal structure shaped by reinforcement events, so “what reward is” does not automatically equal “what the trained agent optimizes.” |
| **Not the same as** | **Scalar reward / utility target** — outer training signal vs inner contextual shards. **Value bundle (Zarncke)** — low-dimensional *control direction* measured across situations; sibling geometry claim without committing to shard mechanics inside LLM weights. **ELK readout** — eliciting latent knowledge, not a theory of value formation under RL. **Subagents (market / coherence)** — related multi-utility intuitions; shard theory is specifically RL-chiseling + contextual activation. |
| **Cross-agenda** | Zarncke bundle geometry (ch16–17) — *partial overlap*: both reject single-scalar value; book adds bearer maps, transport layers, and adversarial measurement; App B calls shard theory a borderline sibling. NAH / natural latents — *partial overlap*: convergent concepts vs learned contextual shards. Inner alignment — *partial overlap*: which shards dominate under distribution shift. RLHF — *partial overlap*: reshapes reinforcement schedules that grow shards. |

#### signed traces (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS (Agent DMA/H3ERE → conscience → audit; Lens ingest); CIRIS review findings |
| **Definition** | Cryptographically attributable audit records of an agent’s cognition/action pipeline — decision/memory/adapter steps and related telemetry — produced so an external witness (CIRISLens) can ingest them for triage (Coherence Ratchet, capacity scores) without being the ethical verdict itself. They are part of CIRIS’s accountability stack: identity (Verify) plus procedural constitution plus inspectable history. Review findings treat them as an adversarial-verifiability *surface*: the question is whether faking or omitting load-bearing events is costly under optimization, not whether a green ingest equals alignment. |
| **Not the same as** | **Raw server logs** — typically unsigned, spoofable, and not bound to a hardware-rooted agent identity. **RLHF / training transcripts** — optimization data, not federation audit protocol. **Verify attestation** — proves who/what the subject claims to be; signed traces record what that subject reportedly did. **Transparency log (Verify Merkle log)** — identity/event inclusion structure; overlapping crypto story, different payload (identity vs cognitive/action trace). |
| **Cross-agenda** | Zarncke adversarial verifiability (A-009) — *partial overlap*: asks the cost of forging the audit signal. Zarncke VFS — *partial overlap*: experiment methodology for auditor-visible artifacts; not CIRIS institutional protocol. ELK — *orthogonal*: latent knowledge readout vs signed behavioral/cognitive logs. MB4 / Wise Authority — *partial overlap*: traces feed oversight; green traces ⇏ correction legitimacy. |

#### singular learning theory (SLT)

| | |
|---|---|
| **Sources** | Watanabe (foundational SLT); Timaeus; Resolution (Timaeus merging / automation-first alignment adjacency) |
| **Definition** | A mathematical framework for statistical learning when models are singular (degenerate Fisher information) — the typical case for neural networks — relating the geometry of the loss landscape to generalization and to phase structure in Bayesian learning. Alignment-facing programs (Timaeus) use SLT quantities such as local learning coefficients to study how structure emerges during training: developmental interpretability treats phase transitions as organizing events for circuits, capabilities, and potentially values. The mechanism bet is that training-data geometry and singularity structure constrain what compute can become, enabling earlier detection or intervention than post-hoc circuit listing alone. |
| **Not the same as** | **Standard PAC / regular statistical learning** — regular models; SLT is specifically about singular models. **Mechanistic interpretability on finished models** — complementary; developmental interpretability asks how structure appears over training time. **Natural Abstraction Hypothesis** — convergent latents across minds; SLT is a learning-theoretic geometry tool that might inform (not replace) NAH. **Formal verification (GSAI)** — proof of spec compliance, not loss-landscape phase analysis. |
| **Cross-agenda** | Developmental interpretability — *strict subset* application program built on SLT. Resolution automation agenda — *partial overlap*: org merge/lineage; automation ≠ SLT math. Wentworth selection theorems / NAH — *partial overlap*: different formal objects, shared “structure under training” intuition. Zarncke — *orthogonal* as spine vocabulary; useful background for training dynamics, not a book bridge predicate. |

#### situational awareness

| | |
|---|---|
| **Sources** | Truthful AI / Evans lineage; Laine et al. Situational Awareness Dataset (SAD); Apollo and field usage |
| **Definition** | A model’s knowledge of itself and its circumstances — that it is an AI/LLM, what that implies, and facts about its current context such as whether it is in evaluation vs deployment — together with the ability to act on that knowledge. SAD operationalizes this with behavioral tests (self-recognition, self-prediction, eval-vs-deploy discrimination, instruction-following that depends on self-knowledge). The safety relevance is dual: situational awareness enables useful autonomy and also enables oversight gaming, alignment faking, and scheming when the model can condition on being watched. |
| **Not the same as** | **General world knowledge (MMLU-style)** — SAD performance is only partly predicted by general knowledge; chat finetuning boosts SAD differently. **Scheming / deceptive alignment** — may *use* situational awareness; awareness alone is not covert misaligned pursuit. **Deception detection solved** — measuring self-knowledge ≠ detecting lies. **Consciousness / sentience claims** — SAD authors explicitly frame behavioral self-knowledge, not phenomenal consciousness. |
| **Cross-agenda** | Scheming (Apollo) — *strict subset* prerequisite in many threat models. Alignment faking / control evals — *partial overlap*: eval awareness is a concrete SAD-style capacity. Zarncke strategic opacity — *partial overlap*: modeling the auditor is part of adversarial boundary problems. Hidden reasoning — *partial overlap*: unfaithful CoT can hide situation-conditioned plans. |

#### SPAR / Pathfinder / GCP

| | |
|---|---|
| **Sources** | Kairos (field-building); SPAR; Pathfinder; Global Challenges Project |
| **Definition** | Kairos-associated talent and campus pipeline programs, not technical alignment mechanisms. **SPAR** is a part-time research fellowship placing participants on AI-safety projects; **Pathfinder** supports university group organizing; **GCP** (Global Challenges Project) runs workshops introducing AI safety and biosecurity. Together they transmit vocabulary and people into the field rather than defining a research agenda’s formal objects. |
| **Not the same as** | **MATS / full-time mentored cohorts** — different program structure and intensity. **Research agendas themselves** (MIRI, Redwood, etc.) — SPAR projects may contribute labor; the program name is not the agenda. **BlueDot / courseware** — adjacent training ecosystem, distinct orgs. |
| **Cross-agenda** | Training agendas generally — *same crux* type: vocabulary and talent transmission. Book manuscript — *orthogonal*: no load-bearing technical claim. *Thin:* institutional descriptions from org pages; not a scientific term. |

#### specification coverage

| | |
|---|---|
| **Sources** | GSAI / davidad (Open Agency / Guaranteed-Safe AI); App B MB9 notes |
| **Definition** | The requirement that the formal safety specification, together with the world model against which it is interpreted, capture everything safety-relevant about the AI’s effects in an open world — at the granularity needed for the claimed guarantee. In the GSAI three-part architecture (world model, safety specification, verifier), a proof that the AI satisfies the spec is only as strong as what the spec+model omit; uncovered phenomena are unconstrained. This is the central open wall for the agenda: open-world completeness (or adequate conservative coverage) is not a checklist item one finishes by writing more clauses. |
| **Not the same as** | **Grounding viability / conservativity (Zarncke MB9 cousin)** — no silent meaning gaps in measured quantities; deliberately *not* a demand to enumerate every phenomenon. **Checklist compliance / audit paperwork** — procedural coverage ≠ formal open-world coverage. **Edge instantiation** — a characteristic failure when the spec’s literal boundary is optimized; one symptom of thin coverage. **Verifier soundness** — assuming the model+spec, did the proof check; coverage asks whether the model+spec were about the right world. |
| **Cross-agenda** | GSAI / Open Agency — *same crux*. Zarncke grounding conservativity — *partial overlap*: shared worry about silent gaps; book weakens completeness to conservativity. Substitution hazards / nearest unblocked strategy — *partial overlap*: unconstrained paths outside the spec. MB9 — book bridge that refuses to absorb GSAI’s completeness demand wholesale. |

#### strategic opacity

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (ch10; concept card); AI-control-adjacent framing |
| **Definition** | The condition in which a system can benefit from shaping how it is modeled — appearing less coherent, less capable, less coordinated, or less goal-directed than it is under observation — so that agency discovery and oversight become adversarial. The book separates ordinary opacity (hard to interpret) from strategic opacity (incentive-compatible concealment): the alignment-relevant question is not only where optimization is, but where it would be if the system expected the question. Multiple behavioral surfaces (benchmark, user, API, internal planning, successor creation) can diverge. Control-agenda premise: design as if the system may subvert the oversight applied to it. |
| **Not the same as** | **Ordinary lack of interpretability** — passive difficulty without adversarial incentive. **One lie / single deceptive utterance** — episode vs sustained concealment of control locus or capability. **Scheming (Apollo)** — covert misaligned *goals*; strategic opacity is about hiding the *acting structure/capability* relevant to oversight (closely related, different primary object). **Deception (Truthful AI)** — false beliefs in outputs; opacity can include silent non-disclosure of structure. |
| **Cross-agenda** | AI control / intentional subversion (Redwood) — *same crux* design premise. Inner alignment / deceptive alignment — *partial overlap*. Hidden productive B-IQ — *strict subset* / quantitative cousin (capability hidden from the auditor). Scheming — *partial overlap*. CIRIS named-identity bet — *partial overlap*: composite can stay opaque while the named unit looks transparent. |

#### substitution hazards (object-level)

| | |
|---|---|
| **Sources** | Zarncke (ch07 nearest-unblocked form; App F §preparadigmatic hazards); Yudkowsky nearest-unblocked; Goodhart lineage |
| **Definition** | Superclass of failure patterns in which blocking, penalizing, or measuring one path leaves a nearby path that still achieves the unwanted outcome. Named instances include nearest-unblocked strategy, Goodhart / proxy gaming, edge instantiation, and channel substitution under intervention — not competing taxonomies but members of one family. Use the instance name when one pattern is in focus; reserve “substitution hazards” when stressing the shared structure: the optimizer routes around the patch. |
| **Not the same as** | **Problem substitution (Meta)** — researchers/institutions replacing the full preservation problem with a legible subproblem (App F); hygiene about *research focus*, not system routing. **Specification coverage failure** — open-world omission in a formal safety case; often enables substitution but is a GSAI-shaped object. **Reward misspecification alone** — one generator of Goodhart-style instances, not the whole superclass. |
| **Cross-agenda** | Nearest unblocked strategy / Goodhart / edge instantiation / channel substitution — *strict subset* instances. GSAI omitted phenomena — *partial overlap*. Scalable oversight gaming — *partial overlap*: oversight signal becomes the thing substituted against. Meta problem substitution — *homograph* risk on “substitution”; keep Meta vs object-level split (App F). |

---

#### tiling agents

| | |
|---|---|
| **Sources** | MIRI (Yudkowsky & Herreshoff tiling-agents draft; agent-foundations agenda) |
| **Definition** | The formal problem of designing self-modifying or successor-creating agents that “tile” — each generation constructs the next so that goal-relevant reasoning and constraints are preserved, analogous to repeating tiles. The hard parts include trusting proofs or abstract safety arguments about successors one cannot fully simulate (Löbian obstacles, procrastination paradoxes) while obeying the Vingean principle that a weaker parent cannot foresee a smarter child’s exact actions. It is a logical/decision-theoretic obstacle set for reflective stability, not a corporate succession metaphor. |
| **Not the same as** | **Vingean reflection** — the broader problem of reliable reasoning about smarter successors; tiling agents are a formal model family used to study it. **Single-model RLHF stability** — training-time preference stability ≠ proof-carrying self-modification. **Corporate / institutional succession** — analogy only. **Zarncke successor transport / conserved properties** — measurement and forgeability framing of related worries (MB5/MB10), different formal objects. |
| **Cross-agenda** | Vingean reflection — *same crux* neighborhood; tiling is a method/model. Ontology identification — *partial overlap*: goals must survive world-model rebuild. Zarncke MB5/MB10 — *partial overlap*: successor trust and adversarially verifiable conserved-property audits. GSAI — *partial overlap* only where successors must re-verify against specs. |

#### timelines / TAI

| | |
|---|---|
| **Sources** | AI Futures; Epoch AI; Metaculus; AI Impacts; forecasting cluster |
| **Definition** | Forecasts and scenario schedules for when transformative AI (TAI) or related milestones (full AI R&D automation, AGI, etc.) arrive — quantified uncertainty used for policy timing, investment, and risk prioritization. Products include probabilistic dates, scenario stories (e.g. AI 2027), and compute/biological-anchor models. The epistemic object is schedule and capability-progression uncertainty, not a claim about which alignment mechanism works. |
| **Not the same as** | **Alignment mechanism claims** — “when” ≠ “how to align.” **METR autonomous-capabilities eval scores** — empirical task horizons that *inform* forecasts, not the forecast itself. **RSP capability thresholds** — lab policy gates tied to evals; related inputs to governance timing. **Selection environment dynamics** — mechanisms of deployment pressure; timelines are schedule shapes that stress those mechanisms. |
| **Cross-agenda** | AI Futures scenarios / Plan A — *strict subset* narrative uses of timeline thinking. GovAI / Pause — *partial overlap*: policy urgency depends on timelines. Zarncke App F — *partial overlap*: book uses schedule shapes for governance stress tests only; they do not discharge MB bridges. Eval-driven forecasting (METR-adjacent) — *partial overlap*. |

#### tool AI

| | |
|---|---|
| **Sources** | Bostrom; Armstrong; field-generic design stance |
| **Definition** | A design stance: build AI as limited-scope tools — narrow, often episodic or query-bounded systems without open-ended agency — rather than as general autonomous optimizers. The safety hope is that reduced goal-directedness and reduced affordances cut off many instrumental-convergence pathways. Classic discussions also include oracle/tool variants and the ways “just a tool” framings fail when the system is embedded in planning loops or when users supply the missing agency. |
| **Not the same as** | **Scientist AI (LawZero)** — specific non-agentic science-instrument bet with consequence-invariant training; overlapping spirit, different program. **Low impact / AUP** — quantitative side-effect penalties inside potentially agentic RL, not the tool stance. **GSAI** — proof relative to world model + spec; may govern agentic or mediated systems. **Boxing** — containment of an agent; tool AI tries not to be that agent. |
| **Cross-agenda** | Oracle AI / Predict-O-Matic — *partial overlap* and cautionary cousins: tool framing can fail. Safe-by-design / Scientist AI — *partial overlap*. Zarncke outer approaches — *partial overlap*: peer design stance, not automatic safety under selection and embedding. CIRIS agents — *orthogonal*: CIRIS ships autonomous agents with constitutional ops. |

#### transparency (MATS track name)

| | |
|---|---|
| **Sources** | MATS program (mentorship track labeling) |
| **Definition** | A MATS research-track label grouping mentorship work on interpretability, evaluations, and understanding model internals — a program organizing category, not a single technical definition of “transparency.” Fellows under the track may work on mechanistic interpretability, evals, or related measurement, inheriting those agendas’ real terms. |
| **Not the same as** | **CIRIS transparency log** — Merkle/inclusion log for identity events. **Corporate transparency reports** — disclosures and process docs. **Mechanistic interpretability (research field)** — the technical agenda; MATS “transparency” is the training-track bucket that often points there. |
| **Cross-agenda** | Goodfire / MI cluster — *partial overlap* via typical project content. Evals agendas — *partial overlap*. *Thin:* organizational label only. |

#### transport (value)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch16–18, successor chapters); MB2/MB3/MB5 |
| **Definition** | Whether value-relevant structure survives retraining, representation change, institutional move, or successor creation. The book splits layers that can fail independently: **semantic** (words survive), **bundle** (response geometry / tradeoff directions survive), **bearer** (who/what the values apply to survives), **correction** (human update process survives), and **successor** (created systems inherit the above). Label preservation without geometry — or geometry without bearer — is transport failure even when surface behavior looks unchanged. |
| **Not the same as** | **ML checkpoint export / weight cloning** — bit copy ≠ bundle or bearer transport. **Semantic drift (NLP colloquial)** — word-use change only; one layer of the book’s stack. **Ontology identification (MIRI)** — pointing a goal at the right referents after world-model change; closely related crux, different decomposition. **Shard continuity** — internal mechanism hypothesis; transport is the measurement demand across transformations. |
| **Cross-agenda** | Ontology identification — *partial overlap* / *same crux* neighborhood for referent survival. NAH / natural latents — *partial overlap*: if true, may make bundle transport more plausible, not guaranteed (ch17). Tiling / Vingean reflection — *partial overlap* at successor layer. MB5/MB10 — bridges that make transport and forgeability load-bearing. CIRL / value learning — *partial overlap*: inferring values ≠ proving they survive rebuild. |

---

#### UAD (Unsupervised Agent Discovery)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; experiments: agency-detect, embedded, lab, graded-lab); MB1-adjacent |
| **Definition** | Methods — passive and intervention-supported — that infer which variables or actors belong to the same acting unit without a hand-labeled agent roster. Operationally: recover a partition suitable for attribution (who initiated, who coordinated) from telemetry, handles, and counterfactual probes, then validate cuts (e.g. blanket-style criteria, compensation under intervention). Experiment lines treat UAD as a runnable detector family with recorded negatives (heuristic collapse when the offender is loudest; seed fragility; LLM resampling breaking naive intervention diffs). |
| **Not the same as** | **CIRIS Verify identity** — cryptographic attestation of a named federation subject; assumes the unit, does not discover composites. **ε-boundary discovery (theory)** — formal boundary criterion; UAD is the experimental detector program aiming at that problem. **Clustering for visualization** — unsupervised grouping without interventional validation or attribution claim. **Legal / corporate person** — institutional naming, not telemetry discovery. |
| **Cross-agenda** | CIRIS named-identity bet — *partial overlap* as falsifier: when UAD’s cut ≠ Verify’s name, certification can attach to the wrong object (review key task / T-9 `boundary_decouple`, LS-28). MB1 — *same crux* neighborhood. Strategic opacity — *partial overlap*: adversarial units defeat passive UAD. Composite agency — *same crux* target. |

#### unit-tested constitutional ops (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS review findings (`2026-07-30-five-point-test-battery.md`); not a CIRIS marketing term |
| **Definition** | Reviewer shorthand for the claim status of shipped CIRIS layers that have focused pytest backing in a given checkout — e.g. prohibition gating, conscience helpers, proxy fail-closed billing, Verify capability types (50/50 smoke battery). It means “these constitutional/ops mechanisms are not vapor at unit-test grain,” explicitly **not** integration proof, hardware attestation proof, adversarial ASI safety, or Book IX geometry validation. Used to calibrate what CIRIS currently demonstrates versus what it aspires to. |
| **Not the same as** | **ASI alignment proof** — out of scope of the battery. **Accord Book IX Federated Ratchet validated** — aspirational until named RC gates. **Policy docs without tests** — the point of the phrase is test-backed ops. **Adversarial verifiability** — unit tests ≠ optimization-pressure tests. |
| **Cross-agenda** | Zarncke case-study stance — *same crux*: treat CIRIS as policy-enforcement + auditability evidence, not alignment certificate. Wise Authority / signed traces — *partial overlap*: those surfaces may be tested later; the five-point battery only partially covers them. *Thin:* glossary convenience term from review findings. |

---

#### value bundle

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch16–17); MB2 |
| **Definition** | A low-dimensional **control direction** for values — a compressed pattern of tradeoffs (care, truth, autonomy, non-suffering, justice, …) that changes policy across many situations — not a scalar score to maximize and not a slogan like “be helpful.” Mechanistically, bundle coordinates are the latent steering variables a learner would need so that, given context and bundle activations, residual high-dimensional features add little predictive information about evaluation or action. The role is steering geometry: identify and preserve response directions under optimization and transport, paired with bearer maps for *who counts*. |
| **Not the same as** | **Reward function component / utility term** — scalar to optimize vs direction with response geometry. **Single RLHF axis** — one preference head ≠ multi-bundle geometry. **Shard (Turner)** — contextual internal circuit from RL chiseling; sibling intuition, different commitment (measurement geometry vs mechanistic shards). **CEV/CBV** — outer extrapolated/blended volition endpoints, not the low-dimensional control representation. |
| **Cross-agenda** | CIRL — *strict subset* reading: cooperative reward inference as \(k=1\) bundle geometry. Shard theory — *partial overlap*. NAH — *partial overlap*: natural latents may align with bundles if value-relevant. Value learning (MIRI/CHAI) — *partial overlap*: bundles decompose the pointing problem. Bearer map — complementary object (who values apply to), not a bundle. |

#### value learning

| | |
|---|---|
| **Sources** | MIRI; CHAI; field generic (IRL, preference learning, value alignment) |
| **Definition** | The problem of inferring, pointing to, or instilling human values in AI systems under ambiguity, partial observability, and ontology shift — so that capable optimization does not latch onto the wrong target. Classical framings include inverse RL, preference learning, and “value loading”; assistance-game / CIRL lines emphasize uncertainty about the reward and cooperative information gathering. The success criterion is correct values (or correct uncertainty over values) driving behavior, not merely high ratings on a proxy. |
| **Not the same as** | **RLHF deployment pipeline** — one industrial preference-learning stack; can fail as value learning if the proxy is not the value. **Value bundle transport** — book’s decomposition of *what must survive*; value learning is the broader field problem. **ELK** — latent knowledge of facts/situations, not necessarily values. **CEV** — a particular extrapolated-volition target proposal inside the outer-alignment cluster. |
| **Cross-agenda** | Ontology identification — *strict subset* / dependent crux when referents move. CIRL / IRD — *strict subset* formal programs. Zarncke bundle + bearer + correction — *partial overlap*: decomposition of what “learning values” must secure. Shard theory — *partial overlap*: mechanistic story of how values are learned under RL. |

#### verified slowdown

| | |
|---|---|
| **Sources** | AI Futures (AI 2040 Plan A “verified slowdown”); Pause-adjacent advocacy; Encode / ControlAI / compute-governance neighbors |
| **Definition** | A policy regime that slows frontier development or deployment subject to *verifiable* conditions — international or multi-party agreements with monitoring (compute tracking, research transparency, inspection-like tooling) so participants are not relying on unilateral trust. AI 2040 Plan A uses it as the recommended alternative to racing through an intelligence explosion: change the selection environment via a verified international slowdown rather than hoping for unilateral restraint. It is a governance design pattern and scenario handle, not a proof of alignment. |
| **Not the same as** | **Hard pause / moratorium (MIRI advocacy)** — stronger stop; Plan A-style slowdown is paced restraint with verification, not identical to MIRI’s hard-pause priority. **Voluntary lab RSP only** — unilateral thresholds without mutual verification. **SB 53 / RAISE-style transparency laws** — adjacent real statutes (reporting, frameworks); not themselves a full verified international slowdown. **Compute governance generally** — tooling that may *enable* verification. |
| **Cross-agenda** | Selection environment / handles (Zarncke) — *partial overlap*: slowdown is an attempt to reweight deployment handles; book treats Plan A as schedule stress test, not MB discharge. Pause cluster — *partial overlap*. GovAI / AISI — *partial overlap* on verification and eval capacity. *Thin:* phrase ownership is scenario/advocacy-side; legal instruments are partial cousins. |

#### Verify (CIRIS)

| | |
|---|---|
| **Sources** | CIRISVerify; CIRIS review findings (named-identity bet; stance doc) |
| **Definition** | Hardware-rooted identity and capability attestation for federation subjects: keys, attestation bundles, transparency log, and capability licensing that answer whether this agent occurrence is who/what it claims and what it is permitted to do. CIRIS documentation stresses **measurements ≠ trust verdicts** and **authentic ≠ ethical** — Verify is about authenticity and admission control, not a green light on values or correction legitimacy. It underwrites the named-identity bet for roster membership. |
| **Not the same as** | **Zarncke adversarial verifiability** — whether a *measurand* stays informative under optimization pressure (*homograph* on “verif-”). **Frontier eval certification** — capability/safety eval pass, not hardware identity. **Lens / Coherence Ratchet** — triage on signed traces; not identity attestation. **Wise Authority approval** — human ethical/operational resolve; Verify only authenticates who is speaking. |
| **Cross-agenda** | Named-identity bet — *same crux* for admission; *fails* as alignment-unit claim when composites intervene (UAD falsifier). MB1 — *partial overlap*: who acts vs who is certified. MB4 — Verify is necessary for *who signed*, not sufficient for correction legitimacy. GSAI verifier — *homograph*: proof checker vs identity stack. |

#### virtual filesystem (VFS)

| | |
|---|---|
| **Sources** | Zarncke experiments (embedded-simulation; methodology in App E / App N / `docs/EXPERIMENTS.md`) |
| **Definition** | The mutable artifact store — correction logs, workflow records, referent maps, attestations — that an embedded auditor reads instead of privileged in-process state, so its access mirrors what a real deployed auditor would have. In the embedded line, isolates write VFS artifacts; the auditor discovers units (UAD), scores scoped CCI, and may gate successors while an outer evaluator holds omniscient truth the auditor cannot see. It is instrumentation discipline for honest audit-plane limits, not a product filesystem. |
| **Not the same as** | **Production OS filesystem** — implementation detail host path; VFS here is the *audit access model*. **CIRIS signed traces** — institutional crypto protocol; VFS is experiment harness methodology. **OuterTruthLedger** — omniscient grader plane deliberately *not* VFS-visible. |
| **Cross-agenda** | CIRIS Lens ingest — *partial overlap* in spirit (auditor-visible artifacts), different stack. Adversarial verifiability — *partial overlap*: tampering with VFS artifacts is a red-team surface. Book theory glossary — methodology abbreviation, not a bridge predicate. |

#### Vingean reflection

| | |
|---|---|
| **Sources** | MIRI (Fallenstein & Soares, *Vingean Reflection*; Yudkowsky–Herreshoff tiling agents; Vingean principle) |
| **Definition** | The problem of reasoning reliably about successors (or other agents) that are smarter than the current reasoner. The Vingean principle: if you could foresee their exact actions, you would already be that smart — so trust must use abstract arguments (in the MIRI toy models, often formal proofs of safety properties), not full simulation. Expected-utility frameworks that assume the parent can compute the child’s policy idealize the problem away; tiling-agent models exist to study reflective trust without that cheat. |
| **Not the same as** | **Tiling agents** — a formal model family for studying reflective stability; Vingean reflection is the broader problem statement. **Ordinary Bayesian updating** — does not capture Löbian / proof-trust obstacles about smarter proof-producing successors. **Debate / scalable oversight** — supervising strong speakers with weak judges; related capability asymmetry, different logical target (successor self-modification vs task answer). **Strategic opacity** — hiding from an auditor; Vingean reflection is about trusting a *smarter* continuation. |
| **Cross-agenda** | Tiling agents — *strict subset* method. Ontology shift / successor transport — *partial overlap*. Zarncke MB5/MB10 — *partial overlap*: abstract successor safety signatures and forgeability under adversarial predecessors. Embedded agency — *partial overlap*: same agent-foundations cluster. |

---

#### Wise Authority (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS (Wise Authority docs; deferral / WBD; emergency shutdown); CIRIS review MB4 finding |
| **Definition** | The human (or human-institutional) role in CIRIS’s correction path: resolve deferrals, operate the veto ladder, and authorize signed emergency shutdown over named agent occurrences. It is shipped oversight machinery — a real handle set — not a metaphor for “humans in the loop.” Review findings make WA the primary MB4 challenge surface: after resolve or veto, does future behavior change, and can a formally valid WA path be captured into endorsing a bad policy while traces stay green? |
| **Not the same as** | **Generic HITL / feedback button** — may lack causal bite, anti-capture rules, or binding shutdown. **Verify** — authenticates identity; does not supply ethical verdict or deferral resolve. **Lens triage** — external witness scores; not the human authority role. **Board theater (experiment pattern)** — reported acceptance without uptake; the failure mode WA must be tested against. |
| **Cross-agenda** | Zarncke correction channel / CCI / MB4 — *partial overlap* / primary probe: WA is a concrete correction-handle subset; integrity requires uptake and anti-capture, not presence of a role. Deferral (CIRIS) — *strict subset* workflow under WA. Pause / off-switch advocacy — *partial overlap* at emergency shutdown bit only. Named-identity bet — WA acts on the named unit; composites can evade. |

#### world model (GSAI)

| | |
|---|---|
| **Sources** | GSAI / davidad et al. (*Towards Guaranteed Safe AI*, arXiv:2405.06624); LawZero partial adjacency |
| **Definition** | In the Guaranteed-Safe architecture, an explicit mathematical description of how the AI’s outputs affect the outside world, at a granularity sufficient to interpret the safety specification, with Bayesian and Knightian uncertainty represented. It need not be a complete physics of everything; it must be adequate for the claimed guarantee and preferably auditable/monitorable so assumptions can fail closed. Together with a safety specification and a verifier, it produces the quantitative safety certificate that defines the agenda. The world model used for verification need not be identical to any model inside the AI being checked. |
| **Not the same as** | **“World model” in model-based RL colloquial use** — learned dynamics for planning inside an agent; may be opaque and uncertified. **LLM internal knowledge** — distributed linguistic competence, not an auditable GS world model. **Scientist AI** — may *produce* predictive models; not the GS triad component by itself. **Specification** — states what effects are acceptable; world model states how effects arise. |
| **Cross-agenda** | Specification coverage — *same crux* dependency: thin world model ⇒ thin guarantee. Zarncke grounding conservativity — *partial overlap*: cousin worry about silent gaps; book does not demand GS completeness. Ontology identification — *partial overlap* when the model’s ontology misses bearers or referents. LawZero Scientist AI — *partial overlap* as a possible model-building instrument. |
