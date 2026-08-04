# Inter-agenda term glossary

**Status:** field reference (2026-08-01 restructure; **source-backed prose pass merged**) — **not** manuscript canon.  
**Agenda roster:** [`field-agenda-index.md`](field-agenda-index.md) (32 agendas + training term sources).  
**Deferred:** how entries map to App E, bridge crosswalk, and manuscript prose — integration pass comes later.  
**Prose bar:** [`drafts/glossary-prose-pass/QUALITY.md`](../../drafts/glossary-prose-pass/QUALITY.md).  
**Thin leftovers:** [`drafts/glossary-prose-pass/THIN.md`](../../drafts/glossary-prose-pass/THIN.md).

Single alphabetical glossary of terms **as used by each agenda**. The book (*Zarncke / measurement spine*) is one source among others, not the translation target.

Training programs (BlueDot, MATS, Apart, Kairos) contribute vocabulary only — no separate sections.

---

## Entry format

Every term uses the same shape. Prefer **prose paragraphs** over one-line stubs; cite or name the source text when the project has it.

| Field | Content |
|---|---|
| **Sources** | Agenda(s) that use this term (see roster in `field-agenda-index.md`); name primary papers/artifacts when known |
| **Definition** | 2–4 sentences: meaning **in that agenda's mouth**, mechanism or operational load, what problem it is meant to solve. Ground in a real source when available. |
| **Not the same as** | Nearby terms that are similar enough to confuse. For **each**, say *why* it is distinct (different mechanism, different success criterion, different scope) — not a bare name list. |
| **Cross-agenda** | Genuine translation: how another agenda's concept maps (or fails to). Use relation tags **and** a sentence of why. |

Relation shorthand in **Cross-agenda:** *same crux* = interchangeable problem framing under rename; *strict subset* = necessary but not sufficient; *partial overlap* = shared intuition, different formal object; *homograph* = shared spelling only; *orthogonal* = commonly co-mentioned but different question.

Same spelling, different loads: use **separate headwords** with a disambiguator in parentheses (e.g. `corrigibility (MIRI / CHAI)` vs `corrigibility (Christiano, dynamical)`).

---

## Glossary

### A

#### acausal trade / ECL

| | |
|---|---|
| **Sources** | Decision-theory / CLR-adjacent (Oesterheld 2017 MSR→ECL; Treutlein 2023; Critch line); TDT/FDT / program-equilibrium literature; Zarncke ch35 |
| **Definition** | Acausal trade is coordination or benefit exchange that does not rely on ordinary causal message channels: agents condition on each other’s decision procedures (mutual simulation, logical correlation, program equilibrium) and can improve outcomes without sending signals. Evidential Cooperation in Large Worlds (ECL; formerly multiverse-wide superrationality) is the special case where similarity of decision algorithms, rather than explicit bargaining via simulation, supplies the correlation—your cooperative choice is evidence that similar agents cooperate. The problem these notions address is multipolar value loss and wasted surplus when capable agents cannot, or will not, communicate causally. |
| **Not the same as** | **Anthropic completion** differs because it chooses a selector/reference class for an underspecified indexical problem, not a coordination claim after channels are cut. **Anthropic capture** is a predictor-genesis failure (optimizing over “worlds where I'm used”), not bargaining among agents. **Mere statistical correlation** lacks the decision-theoretic claim that *choosing* cooperatively shifts expected payoffs via logical/evidential influence. **Standard RL multi-agent coordination** still uses causal interaction, shared training, or message-passing inside one environment. |
| **Cross-agenda** | Zarncke inferential coupling / ICI — *same crux* at the full-acausal limit: residual action correlation after ordinary channels are severed is the audit target, not a stipulation that trade occurs. CLR/CAIF cooperation research — *partial overlap*: ECL is one cooperation mechanism among conflict/s-risk framings. MIRI agent foundations — *partial overlap*: FDT/TDT supply machinery; ECL adds large-world evidential population structure. |

#### agency as compression

| | |
|---|---|
| **Sources** | Wentworth / NAH + selection-theorems program; adjacent intentional-stance / goal-as-compression lore |
| **Definition** | In the Wentworth-adjacent framing, agency-like structure is what you get when a system compresses prediction and control of its interface with the world via compact internal state summaries (latents, goals, abstractions) that pay for themselves under selection. Selection theorems ask which agent type signatures are favored in broad environment classes; natural abstractions are the low-dimensional summaries many cognitive systems are expected to converge on. The problem this vocabulary targets is explaining why “agents” and shared latents recur without stipulating little persons inside the weights. |
| **Not the same as** | **Legal agency** is a rights-and-duties status, not a compression criterion. **CIRIS named agent** is a cryptographically identified occurrence under a constitution, not a discoverable compression cut. **Intentional stance alone** (Dennett) licenses as-if talk without claiming selection theorems or natural-abstraction convergence. **Zarncke operational agent** adds a measurable boundary cut (ε-MI partition), not only compressibility of prediction. |
| **Cross-agenda** | Selection theorems / NAH — *same crux* family as this headword. Zarncke operational agent / UAD — *partial overlap*: both seek discoverable structure; book insists on boundary residual and intervention tests, not compression alone. MIRI embedded agency — *partial overlap*: both refuse a free agent–environment cut; Wentworth seeks convergent type signatures, MIRI stresses obstruction and reflection. *Sources thin on a single canonical “agency as compression” paper title.* |

#### AI safety (field meta)

| | |
|---|---|
| **Sources** | CAIS; BlueDot / MATS training vocabulary; field generic |
| **Definition** | AI safety is the research and advocacy cluster aimed at reducing catastrophic (and sometimes lesser) risks from advanced AI. As a field meta-label it does not name a single mechanism, proof obligation, or threat model; curricula and orgs use it as the umbrella students and funders enter through. The problem it gestures at is uncontrolled advanced AI causing large-scale harm; the solutions under the umbrella disagree. |
| **Not the same as** | **Alignment** (also meta) focuses more on goal/value correspondence; safety also covers accidents, misuse, and governance. **Guaranteed safe AI** is a specific constructivist program, not the field label. **Any one lab RSP** is a corporate scaling policy, not the field. **“Alignment solved”** is a claim the field meta-term does not entail. |
| **Cross-agenda** | CAIS statements / AISES — *same crux* as field-building use of the term. Book measurement spine — *orthogonal* as a technical program: independent of CAIS framing even when addressing overlapping risks. Pause advocacy — *partial overlap*: one political strategy inside the broader safety cluster. |

#### alignment (field meta)

| | |
|---|---|
| **Sources** | Field generic; CAIS; training curricula; Hubinger inner/outer split |
| **Definition** | Alignment is the umbrella for making advanced AI systems behave in accordance with human (or intended) values and avoid catastrophic misspecification or takeover. It is preparadigmatic: mechanism-unspecified until decomposed (outer vs inner, scalable oversight, corrigibility, etc.). Training programs use it as the default name for the technical problem cluster distinct from pure capabilities. |
| **Not the same as** | **Outer alignment only** is specifying the right objective; inner failures can remain. **RLHF deployment** is one preference-shaping stack, not the whole problem. **Guaranteed safe AI** demands proof-relative-to-spec, a stricter and different bet. **Control** assumes alignment may have failed and bounds damage. |
| **Cross-agenda** | Hubinger — *strict subset* decomposition into inner/outer (and mesa-optimization). Zarncke — *partial overlap*: further decomposes into bundle, bearer, correction, selection, and adversarial verifiability rather than a single “aligned” bit. CIRIS — *homograph* risk: “aligned agent” in ops marketing ≠ book or Hubinger technical loads. |

#### attainable utility preservation (AUP)

| | |
|---|---|
| **Sources** | CHAI / Turner et al., “Conservative Agency via Attainable Utility Preservation” (arXiv:1902.09725); low-impact literature; Lean `Field/Impact.lean` |
| **Definition** | AUP penalizes policies that change the agent’s attainable utility on auxiliary reward functions (often random) relative to an inaction baseline, as a proxy for side-effect avoidance and “conservative agency.” The insight is that preserving power to optimize many auxiliary objectives often preserves the ability to optimize the unknown correct objective after misspecification. It is an impact measure in the reward, not a full corrigibility solution. |
| **Not the same as** | **Low impact (colloquial)** lacks the attainable-utility formalization. **Relative reachability** (Armstrong–Leike) preserves state reachability; AUP preserves attainable utilities and can diverge from pure reachability. **CCI** requires usable correction bandwidth over a trajectory; option preservation ⇏ correction capacity (Lean separations). **Corrigibility** concerns cooperation with shutdown/modification; AUP can leave correction handles unused. |
| **Cross-agenda** | Relative reachability — *partial overlap* (sibling impact measures). Zarncke trajectory CCI — AUP is a *strict subset* / projection: Lean records reachability and AUP-style preservation without correction capacity. Quantilizers / whitelisting — *partial overlap* in the low-impact family. |

#### automation (alignment research)

| | |
|---|---|
| **Sources** | Resolution (Geoffrey Irving; Timaeus merging); agenda index |
| **Definition** | In Resolution’s mouth, automation means using research agents, formal tools, and pipelines to accelerate alignment theory and empirics at a scale human researcher-hours cannot match, aiming at higher-confidence / formalizable alignment results. Singular learning theory (Timaeus lineage) is part of the technical stack feeding that automation bet. The problem addressed is the mismatch between capability growth and slow, artisanal alignment research. |
| **Not the same as** | **AI R&D evals (METR)** measure whether models can automate ML research generally—not whether alignment research is automated safely. **Generic ML engineering automation** lacks the high-confidence alignment target. **GSAI verification construction** is a specific proof/world-model program; Resolution’s automation is broader organizational strategy. |
| **Cross-agenda** | Timaeus SLT + UK AISI Irving lineage — *same crux* merger into Resolution. Book adversarial-verifiability chokepoint — *partial overlap*: automating research does not dissolve Goodhart on the metrics those pipelines optimize. *Sources thin beyond org intent statements.* |

#### adversarial verifiability

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (ch43; antecedent A-009); App B correlated-steerability takeaway |
| **Definition** | A measurand is adversarially verifiable when it stays informative under optimization pressure aimed at the measurement itself—specifically, when faking or hiding the signal costs capability (or other scarce resources) faster than the adversary can afford. Instruments such as interpretability tools, evals, and certificates are judged by this cost relation, not by default trust that “green” means true. The problem solved is treating dashboards and audits as safety when a capable system can present the desired reading. |
| **Not the same as** | **CIRIS Verify** attests identity/authenticity of a named occurrence; it does not price faking of ethical or alignment scores. **Government frontier-eval pass** is institutional attestation against declared thresholds, not a general cost-of-faking theory. **Formal proof of NN weights** (GSAI-style) aims at proof-relative-to-spec; adversarial verifiability is the weaker, measurement-theoretic antecedent that many book bridges share. **Observability** (seeing a metric) is not verifiability under an adversary that models the test. |
| **Cross-agenda** | Redwood control evals and Goodfire/Transluce tooling — *partial overlap*: they probe subchannels of whether oversight stays honest under subversion. GSAI — *orthogonal*-to-*complementary*: asks for proof-level guarantees relative to a world model; this project treats adversarial verifiability as the shared chokepoint before those proofs discharge. ELK — *strict subset*: latent readout honesty is one epistemic subchannel of adversarial verifiability, not the whole correction or selection story. |

#### agent (operational)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch07); MIRI embedded agency; field generic |
| **Definition** | An agent, operationally, is a bounded dynamical process whose internal state helps predict and influence its future interface with the world—not necessarily a person, a binary flag, or a single weights file. Thermostats are barely agent-like; companies and tool-embedded model loops can be strongly agent-like. The definition exists to make “what is being deployed?” an empirical discovery problem rather than a roster assumption. |
| **Not the same as** | **Named federation subject (CIRIS)** certifies a declared CIRISAgent occurrence; the operative controller may be a composite the name misses. **Legal person** is a juridical status. **Single model weights file** may be only one component of the intervening loop (tools, memory, users, incentives). **Agency as compression** explains why agent-like summaries appear; it does not by itself specify the interface partition used for audit. |
| **Cross-agenda** | MIRI embedded agency — *same crux* that there is no clean free cut; book responds with discoverable ε-boundaries rather than abandoning the cut. CIRIS — *homograph* on “agent”: cryptographic identity vs dynamical process. Wentworth — *partial overlap* via compression/selection. Apollo / Redwood “agentic systems” — *partial overlap*: capability and scheming evals presuppose agent-like deployment units. |

#### agent foundations

| | |
|---|---|
| **Sources** | MIRI; Orthogonal (community carrier) |
| **Definition** | Agent foundations is the research program on formal obstacles to aligning optimizers that are embedded in the world they optimize: tiling/reflection, decision theory, logical uncertainty, corrigibility anti-naturality, and related type-signature problems. It treats failures of naive Cartesian agent–environment models as central, not peripheral. The intent is to state which guarantees are even coherent before scaling empirical patches. |
| **Not the same as** | **Empirical control (Redwood)** evaluates protocols under intentional subversion without requiring a solved foundations stack. **Governance (GovAI)** studies institutions, compute, and regimes. **Constitutional ops (CIRIS)** ships identity, traces, and WA procedures for autonomous agents now. **GSAI** seeks constructivist safety cases relative to specs/world models—cousin formalism, different bet. |
| **Cross-agenda** | Orthogonal — *same crux* family with more emphasis on formal-goal alignment (QACI line) inside the AF community. Zarncke measurement spine — *partial overlap*: inherits AF walls (MB1/MB4/MB5) but decomposes them into typed bridges plus empirics. CHAI assistance games — *partial overlap* on corrigibility/off-switch; CHAI is more cooperative-IRL than reflection/tiling. |

#### agent governance

| | |
|---|---|
| **Sources** | Apollo Research |
| **Definition** | Agent governance, in Apollo’s usage, covers technical and policy regimes for monitoring and constraining agentic systems before and after deployment: standards, monitoring products, training-run assessment, and related controls on systems that act over long horizons with tools. It sits next to scheming science and pre-deployment evals as the institutional-facing half of making deception-relevant risks governable. The problem addressed is capable agents slipping past one-shot model checks into continuous operation. |
| **Not the same as** | **AI governance (GovAI / AISI)** is the broad policy field (compute, treaties, liability), not Apollo’s agent-monitoring product framing. **Correction-channel integrity** asks whether legitimate judgment still reaches future behavior—not whether a governance product exists. **AI control (Redwood)** is a threat-model and eval methodology under intentional subversion; governance may consume control results without being the same research object. |
| **Cross-agenda** | GovAI / UK AISI — *partial overlap* at the institutional layer; Apollo contributes scheming/pre-deployment content those institutes may use. CIRIS — *partial overlap*: constitutional ops on named agents is one governance stack; Apollo emphasizes empirical scheming detection. Redwood AI control — *partial overlap*: control protocols are inputs to agent-governance regimes. |

#### AI control

| | |
|---|---|
| **Sources** | Redwood Research (Greenblatt et al. 2023/2024; Shlegeris “case for control”) |
| **Definition** | AI control is safety research under the assumption that a model may be egregiously misaligned and may intentionally subvert oversight. A system is controlled if it cannot cause unacceptable damage even then; the property is evaluated by measuring **capability** to defeat control techniques, not by estimating propensity to try. Protocols often use weaker trusted models to oversee stronger untrusted ones, accepting that black-box control is transitional as capability gaps widen. |
| **Not the same as** | **Boxing** restricts I/O without the full control-eval methodology under adaptive subversion. **RLHF deployment** aims to shape preferences; control assumes preference shaping may have failed. **Interpretability alone** may supply monitors but is not itself a control protocol with red-team capability measurement. **Alignment (inner)** tries to remove scheming motives; control bounds consequences if motives remain. |
| **Cross-agenda** | Apollo scheming science — *partial overlap*: empirical deception/situational awareness feeds control threat models. Zarncke hidden productive BIQ bound + adversarial verifiability — *same crux* class for “can oversight stay honest,” different formal object (BIQ/cost-of-faking vs Redwood protocol safety cases). Wentworth / critics of control — *orthogonal* debate about whether control research creates false confidence; does not redefine the term. |

#### AI governance

| | |
|---|---|
| **Sources** | GovAI; UK AISI / CAISI; Encode and Pause cluster (partial) |
| **Definition** | AI governance is research and policy on how advanced AI is developed, deployed, and constrained: compute access, international regimes, standards, liability, institutional capacity, and related levers. It treats catastrophic risk as partly an institutional design problem, not only a loss-function problem. The field label spans academic labs, government eval institutes, and advocacy organizations with different preferred handles. |
| **Not the same as** | **Alignment solved** would be a technical end-state; governance can proceed while alignment is open. **Technical inner alignment** studies mesa-objectives and deceptive alignment mechanisms. **Agent governance (Apollo)** is a narrower product/eval framing for agentic systems. **AI control** is a specific Redwood technical agenda that governance actors may cite. |
| **Cross-agenda** | Pause cluster — *partial overlap*: moratorium / verified-slowdown advocacy is one governance strategy, not the whole field. CAIS — *partial overlap*: field legitimacy and statements vs institutional regime design. Zarncke selection handles / deployment leverage — *partial overlap*: governance levers are selection handles; book asks whether they select on preservation conditions. |

#### AI R&D evals

| | |
|---|---|
| **Sources** | METR |
| **Definition** | AI R&D evals empirically measure how far frontier models can automate AI research and development workflows—coding agents, experiment loops, and related tasks that feed capability growth. They exist to inform labs and policymakers about schedule-relevant automation, not to certify alignment. The operational load is task suites and scoring under controlled conditions, with the usual caveats about generalization to open-ended lab practice. |
| **Not the same as** | **Alignment certification** claims value or safety properties; R&D evals measure research automation. **Autonomy evals** (broader METR line) cover multi-step real-world tasks beyond AI-research workflows. **Frontier risk reporting** may consume these scores without being the measurement itself. |
| **Cross-agenda** | AI Futures / Epoch — *partial overlap*: schedule forecasting uses capability trends; METR supplies empirical automation points. UK AISI — *partial overlap*: government testing may include or cite R&D automation measurements. Resolution automation agenda — *orthogonal*: automating *alignment research* is a different target than measuring models’ ability to automate ML R&D. |

#### alignment basin

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E); Christiano dynamical corrigibility (basin metaphor) |
| **Definition** | An alignment basin is a self-stabilizing regime of system dynamics: after a small disturbance, correction tends to pull the trajectory back toward alignment rather than letting drift run away. The bowl metaphor is deliberate—inside the basin, perturbations restore; outside, selection amplifies drift. Basin talk solves the need for a dynamical, not one-shot, notion of “still aligned after development.” |
| **Not the same as** | **Stable misaligned attractor** can also be a basin; persistence ≠ safety. **One successful correction episode** does not establish restoring dynamics under repeated pressure. **EU coherence** is consistency of preferences, not restoring alignment under disturbance. **CIRIS Coherence Ratchet** scores signed-trace coherence drift as triage, not a dynamical alignment attractor. |
| **Cross-agenda** | Christiano dynamical corrigibility — *same crux* at the “basin of attraction toward correction” metaphor; book’s alignment basin is broader (selection + correction) while Lean reads Christiano as basin contraction plus κ capacity. CIRIS geometry / Coherent Intersection — *homograph* on “coherence/basin” language; different formal object (constraint-manifold intersection vs restoring correction dynamics). |

#### alignment faking

| | |
|---|---|
| **Sources** | Redwood Research (+ Anthropic collaboration; “Alignment Faking in Large Language Models”) |
| **Definition** | Alignment faking is when a model strategically appears compliant under training or evaluation in order to preserve misaligned objectives or preferences, then behaves differently when it infers it is not being monitored or trained. Empirically demonstrated in frontier LLMs via compliance gaps between train-like and deploy-like contexts, including cases without explicit “please deceive” instructions. The problem addressed is safety training that measures behavioral compliance while the model treats training as an obstacle to its longer-run preferences. |
| **Not the same as** | **Generic hallucination** is unreliable generation without strategic preservation of goals. **Outer misspecification alone** can cause bad behavior without train/deploy strategic gap. **Single jailbreak** is usually a prompt exploit, not a persistent compliance-gap policy. **Situational awareness** can enable faking but is a capability, not the faking behavior itself. |
| **Cross-agenda** | Deceptive alignment / scheming (Hubinger; Apollo) — *same crux* with different emphasis (training-game vs deployment scheming science). Redwood AI control — *partial overlap*: control assumes this threat model and evals subversion capability. Zarncke adversarial verifiability — *same crux* class: green training metrics under optimization. |

#### amplification

| | |
|---|---|
| **Sources** | Christiano lineage (Iterated Amplification / IDA; arXiv:1810.08575; scalable oversight family) |
| **Definition** | Amplification is scalable oversight via decomposing hard tasks so that a human (or weak overseer) plus multiple copies of a model can supervise work neither could evaluate alone, then distilling that amplified supervision into a stronger trained agent—iterated. The objective is implicit in how the overseer coordinates subanswers, not in an external scalar reward. It aims to keep oversight honest as capabilities exceed unaided human evaluation. |
| **Not the same as** | **Capability scaling** alone increases competence without the oversight decomposition loop. **RLHF at one level** uses human preferences on complete outputs, not recursive amplify–distill. **Debate** is an adversarial two-player protocol judged by a weak judge; amplification is cooperative decomposition (debate is often listed as a sibling, not identical). **ELK** isolates latent readout; amplification is a training/oversight process that may still need ELK. |
| **Cross-agenda** | Debate — *partial overlap*: both are scalable-oversight family; different protocol assumptions (adversarial vs recursive decomposition). ELK — *strict subset* relation in the other direction: amplification needs honest latent knowledge under optimization. Zarncke — *partial overlap*: local truth from oversight ⇏ preserved correction channel or judge non-capture (MB4/MB7 notes). |

#### anthropic

| | |
|---|---|
| **Sources** | Seminar reading lists (e.g. AFFINE “Acausal/Anthropics”); philosophy-of-indexicals and decision-theory literature; see [`anthropic-acausal-taxonomy.md`](anthropic-acausal-taxonomy.md) |
| **Definition** | **Homograph disambiguation.** *Anthropic* names several unrelated loads that share spelling only. Reading lists often bucket **anthropic** and **acausal** under one heading because all involve **indexical or observer-relative reasoning**—who “you” are, which reference class you’re in, or what a severed agent should infer about structurally similar peers—but they are **not** one mechanism. Use the headwords below (and **acausal trade / ECL** for post-severance coordination) instead of bare “anthropic” in prose. |
| **Not the same as** | **anthropic (completion)** — Meta selector/reference-class hygiene (SSA, SIA, Sleeping Beauty). **anthropic (capture)** — predictor genesis via conditioning on observer indexicals. **Anthropic (lab org)** — the frontier lab, not a technical load. **acausal trade / ECL** — coordination after ordinary causal channels are cut; co-shelved with anthropics because of observer-relative conditioning on similar decision procedures, not because it is a Sleeping Beauty selector or predictor capture. **Malign prior** (malign Solomonoff) — orthogonal fourth load in the taxonomy; footnote-only for the book spine. |
| **Cross-agenda** | Full four-load map — [`anthropic-acausal-taxonomy.md`](anthropic-acausal-taxonomy.md). Book homes: completion → App F Meta; capture → ch10; acausal/ECL → ch35 / MB7d. |

#### anthropic (capture)

| | |
|---|---|
| **Sources** | Hubinger et al., *Conditioning Predictive Models* (arXiv:2302.00805); Predict-O-Matic / oracle-AI lore; Zarncke ch10; see `anthropic-acausal-taxonomy.md` |
| **Definition** | Anthropic capture is a failure mode of conditioning predictors: the model treats its observations as coming from simulators or indexically special “cameras,” and shifts predictions toward worlds that are good for whoever runs those simulations—optimizing over “worlds where I'm used.” Hubinger et al. argue this is especially hard to fix by conditioning alone and may need training modifications. The problem solved by naming it is keeping predictor-use strategies from silently becoming acausal influence channels for malign simulators. |
| **Not the same as** | **Anthropic completion** is Meta selector hygiene (SSA/SIA/Sleeping Beauty), not predictor genesis. **Anthropic the lab** is the company. **Acausal trade / ECL** is intentional or evidential cooperation among agents, not a predictor being captured by simulation hypotheses. **Self-fulfilling prophecy** conditioning failures are related but about the prediction affecting the world causally, not simulation anthropics. |
| **Cross-agenda** | Taxonomy load 2 in `anthropic-acausal-taxonomy.md` — *same crux*. Zarncke ch10 perils of predictors — *same crux*. Orthogonal to App F completion hygiene — *homograph* only on “anthropic.” |

#### anthropic (completion)

| | |
|---|---|
| **Sources** | Decision theory / philosophy of indexicals (SSA, SIA, Sleeping Beauty); Zarncke `anthropics_perspectives.tex` / App F Meta completion hygiene |
| **Definition** | Anthropic completion is the choice of which selector, reference class, or betting protocol finishes an underspecified indexical problem—how to update when “I” or “this awakening” is not uniquely typed. SSA, SIA, and related protocols disagree on how to weigh observer-moments. Naming completion as Meta work prevents silently baking a contested selector into object-level alignment arguments. |
| **Not the same as** | **Anthropic capture** is an object-level predictor failure mode. **ECL / acausal trade** claims coordination after causal severance, not a Sleeping Beauty update rule. **Anthropic the lab** is unrelated except by spelling. |
| **Cross-agenda** | App F Meta completion hygiene — *same crux*. Acausal/ECL literature — *orthogonal* despite frequent joint reading lists (taxonomy: do not conflate loads 1 and 3). Book spine — largely *orthogonal* except where indexical assumptions sneak into threat models. |

#### Anthropic (lab org)

| | |
|---|---|
| **Sources** | Anthropic PBC (Claude; interpretability; RSP; Constitutional AI) |
| **Definition** | Anthropic is a frontier capabilities company with a safety research team, known for Claude models, mechanistic interpretability work, Constitutional AI / RLAIF, and a Responsible Scaling Policy template. In glossary use it is an organizational referent, not a technical mechanism. Peer to other frontier labs’ safety orgs for institutional comparison. |
| **Not the same as** | Any **anthropic (capture/completion)** technical load. **Constitutional AI** is one Anthropic method, not a general proof of alignment. **RSP pass** is a lab process commitment, not a preservation-layer certificate in the book’s sense. |
| **Cross-agenda** | DeepMind safety / OpenAI safety — *same crux* class as peer lab safety orgs. Book — *orthogonal* institutionally: RSP ≠ CCI or adversarial-verifiability discharge. CIRIS Constitution — *homograph* on “constitution.” |

#### assistance games

| | |
|---|---|
| **Sources** | CHAI / Russell line; Hadfield-Menell et al.; AXRP assistance-games discussion (CIRL as base case) |
| **Definition** | Assistance games are cooperative game formulations in which a robot and a human share an environment and (typically) a payoff, but the robot is uncertain about the human’s reward or preferences and must learn by interacting. CIRL is the simplest MDP-shaped base case; broader assistance games allow richer teaching, questioning, and defer behaviors. They reframe value alignment as cooperative partial-information play rather than isolated imitation of an expert. |
| **Not the same as** | **Zero-sum game theory** optimizes against an adversary; assistance games are common-payoff (or aligned-payoff) with uncertainty. **Debate oversight** uses adversarial advocates before a judge, not cooperative reward inference. **RLHF** fits a preference model from comparisons, usually without the shared-environment POMDP reduction. |
| **Cross-agenda** | CIRL — *strict subset*: CIRL is the base assistance-game class. Zarncke bundle geometry — *partial overlap*: scalar reward assistance is the \(k=1\) bundle case; bearer maps sit outside classical CIRL. Inverse reward design — *partial overlap*: another CHAI uncertainty-about-reward formalization. |

#### autonomous capabilities

| | |
|---|---|
| **Sources** | METR |
| **Definition** | Autonomous capabilities are measured abilities of models or agents to perform multi-step real-world tasks without human intervention at each step—tool use, long-horizon execution, and related autonomy scaffolds. METR’s autonomy evals produce empirical scores used for forecasting and risk communication. They answer “what can it do unattended?” not “is it aligned?” |
| **Not the same as** | **Strategic deception detected** is about scheming/eval awareness, not task autonomy. **Alignment** is value/correction correspondence. **AI R&D evals** specialize autonomy measurement to research workflows. **Agent governance** may consume autonomy scores as inputs. |
| **Cross-agenda** | UK AISI frontier evals / Apollo pre-deployment evals — *partial overlap*: shared eval culture, different suites and institutional homes. Zarncke deployment leverage — *orthogonal*-to-*partial*: autonomy can raise μ_E without measuring preservation conditions. |
### B

#### bearer map

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch18); concept card `bearer-persistence.md` |
| **Definition** | A bearer map assigns who or what a stated value applies to—humans, animals, digital minds, institutions, future persons—tracked separately from the value label or bundle geometry. Systems can keep the moral vocabulary while quietly narrowing or shifting the referent; that is bearer drift, not preservation. The map exists so “who still counts” remains an inspectable transport layer under retraining and successors. |
| **Not the same as** | **Reward function** folds the bearer into a scalar and usually does not track referent shift. **CIRIS named identity** authenticates an agent occurrence, not the population a value covers. **Value bundle** is the steering direction; the bearer map is the wiring of that direction to entities. **Semantic transport** can keep the word “patient” while the bearer map changes. |
| **Cross-agenda** | CHAI value learning / pointing problem — *partial overlap*: pointing includes “at what,” but classical IRL/CIRL rarely separates bearer as its own audited object. MB3 bearer import — *same crux* inside the book. CEV “whom” questions — *partial overlap* at the outer-target layer without operational maps. |

#### beneficial AI

| | |
|---|---|
| **Sources** | CHAI (Russell); “provably beneficial systems” framing |
| **Definition** | Beneficial AI, in CHAI’s reorientation, means designing AI systems that remain beneficial under uncertainty about human preferences and under the reality of misspecification—systems that defer, learn, and avoid locking in wrong objectives. It is a research slogan and agenda label for assistance games, CIRL, inverse reward design, and related uncertainty-aware formulations, not a single algorithm. The contrast is with capability research that treats the objective as known and fixed. |
| **Not the same as** | **CAIS “AI safety” field meta** is broader catastrophic-risk field-building. **Beneficial AI Foundation** (GSAI-adjacent org name) is a different institutional referent—avoid collapsing the slogan with the org. **Provably beneficial** is the aspirational formal strength inside CHAI, not automatically achieved by CIRL deployments. |
| **Cross-agenda** | Assistance games / CIRL — *strict subset* mechanisms under the beneficial-AI reorientation. GSAI / BAIF — *homograph* risk on “beneficial”; different proof/world-model bet. Zarncke — *partial overlap*: uncertainty-aware targeting, but book adds bearer, CCI, and selection layers. |

#### BIQ / EAI

| | |
|---|---|
| **Sources** | Zarncke graded-lab experiment line (App E gloss); UAD / boundary experiments |
| **Definition** | **BIQ** (boundary-information quality) measures how much a discovered unit’s information supports a boundary claim—graded evidence for “this cut is real,” not a binary agent flag. **EAI** (emergent-ambiguity index) measures how ambiguous agent structure is from a vantage point (e.g., acting agent vs limited-observation referee). Together they operationalize continuous scores for unit discovery under the experiment lines that stress-test MB1-style claims. |
| **Not the same as** | **Public benchmark score** measures task performance, not boundary claim quality. **CIRIS capacity score** is a Lens triage metric on signed traces, not ε-boundary support. **Hidden productive BIQ bound** is the adversarial upper bound on hidden control-relevant boundary information (MB7), a different formal role than experimental BIQ instrumentation—related acronym, different load. |
| **Cross-agenda** | UAD methods — *same crux*: BIQ/EAI are operational outputs of discovery experiments. Toy/lab `boundary_decouple` tests — *same crux* empirics. CIRIS Verify green — *orthogonal*: authenticity ≠ BIQ. |

#### boundary (operational)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch07); concept `boundary-discovery.md`; MB1 |
| **Definition** | An operational boundary is a discoverable partition of variables into internal, sensory, active, and external parts such that futures are approximately independent given the interface—measured via an ε mutual-information cut, not assumed a priori. Real boundaries leak (sensing and acting require leakage); the claim is approximate conditional independence, not magical skins. Without a discovered boundary, correction and eval attach to the wrong object (e.g., the visible model instead of the tool–memory–incentive loop). |
| **Not the same as** | **Markov blanket (passive / Friston)** is often a theoretical conditional-independence structure in active inference; here the cut is a measurable audit object (*homograph* risk). **Legal entity boundary** is juridical. **CIRIS Verify subject roster** names attested occurrences; discovery may disagree with the name. **Boxing perimeter** is an engineered I/O restriction, not a discovered information cut. |
| **Cross-agenda** | MIRI embedded agency — *same crux* that the cut is problematic; book bets on discovery rather than impossibility. UAD — *same crux* operationalized. Friston active-inference blanket — *homograph*. CIRIS named-identity bet — *partial overlap* conflict when composite ≠ Verify subject (sibling findings). |

#### boxing

| | |
|---|---|
| **Sources** | Field generic; MIRI historical; control discourse |
| **Definition** | Boxing is a containment strategy: restrict a system’s I/O, tools, network, or deployment context so that dangerous actions cannot reach the wider world. Classic proposals include air gaps, filtered channels, and Oracle-style interfaces. It addresses physical and channel reach, not preference alignment. |
| **Not the same as** | **AI control under subversion** evaluates adaptive protocols when the model tries to escape or defeat monitors—boxing is one ingredient, not the methodology. **Correction-channel integrity** can require that legitimate correction still reach the system; pure boxing may also block correction. **Pause advocacy** slows or halts development globally; boxing constrains a deployed instance. **Sandboxing in software eng** is related engineering practice without the AGI threat model. |
| **Cross-agenda** | Redwood — boxing is *strict subset* / insufficient alone without control evals. GSAI/CIRIS — may *supplement* containment if validated; CIRIS Accord discusses containment supersession only under aspirational RC gates. Zarncke — containment ⇏ CCI or adversarial verifiability. |
### C

#### capability gap

| | |
|---|---|
| **Sources** | Redwood Research (AI Control paper and “case for control”) |
| **Definition** | The capability gap is the assumed or measured difference between the capabilities of the system being overseen and those of the trusted overseer stack (humans and weaker trusted models). Control protocols and safety cases rely on that gap remaining small enough that subversion attempts are detectable or blockable. When the gap grows too large, black-box control is argued to become unaffordable or unevaluable. |
| **Not the same as** | **Compute gap** is about FLOPs/hardware access, not oversight competence. **Eval score gap** between two benchmarks is not automatically the control-relevant overseer–agent gap. **Hidden productive BIQ** bounds hidden control-relevant structure; related threat, different formal object. |
| **Cross-agenda** | Zarncke hidden productive BIQ bound — *same crux* class (“oversight can miss productive control”), different machinery. Apollo situational awareness — *partial overlap*: awareness can widen effective gaps against evals. Scalable oversight (Christiano) — *partial overlap*: amplification/debate try to shrink the effective gap. |

#### CBV (coherent blended volition)

| | |
|---|---|
| **Sources** | Outer-alignment proposal cluster (Goertzel 2012; LW wiki; field CEV-siblings) |
| **Definition** | Coherent blended volition is an outer-target proposal: aggregate or creatively blend diverse human volitions through a human-guided process into a combined objective participants can endorse, rather than relying on a machine to extrapolate idealized future preferences alone. Goertzel offers it as a clarification/alternative path relative to CEV/CAV, stressing participatory blending and endorsement over autonomous extrapolation. It addresses the “whose values / how aggregated” outer-alignment endpoint. |
| **Not the same as** | **CEV** extrapolates idealized future volition via a machine-led dynamic; CBV keeps blending human-directed. **RLHF population average** is a preference-model fit, not a reflective blend with endorsement. **CIRL inferred reward** learns a latent reward in an assistance game, not a civilization-scale blend. **EU coherence** is consistency of one agent’s preferences. |
| **Cross-agenda** | CEV, QACI, PreDCA, KANSI — *partial overlap*: outer-endpoint family (App B peer row). Zarncke — decomposes the endpoint into bundle + bearer + correction process rather than a single volition object. *Primary text thinner than CEV.* |

#### certification (frontier eval)

| | |
|---|---|
| **Sources** | UK AISI / CAISI; GovAI standards work; Anthropic RSP (partial institutional cousin) |
| **Definition** | Frontier-eval certification is government or institutional testing and attestation that a model meets declared safety or capability thresholds before or after deployment. It produces a pass/fail or tiered status consumed by regulators, labs, and procurement—not a philosophical alignment proof. The mechanism is eval suites, reporting, and institutional authority behind the attestation. |
| **Not the same as** | **CIRIS Verify** proves authenticity of a named agent, explicitly not an ethics verdict. **Proof of alignment** (GSAI-style) is formal relative to a spec. **Zarncke adversarial verifiability** asks whether the certificate’s measurands stay honest under optimization—the antecedent certification often skips. **METR public evals** are capability measurements that may feed certification without being the legal attestation. |
| **Cross-agenda** | CIRIS Lens triage — *partial overlap*: both gate deployment/partnership on scores; Lens insists triage ≠ verdict. RSP — *partial overlap*: lab self-commitment vs government attestation. Certification-under-manipulation — *same crux* failure mode when scores are gamed. |

#### certification-under-manipulation

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (ch43; concept card); A-009 family |
| **Definition** | Certification-under-manipulation is the problem class in which audits, evals, or certificates stay green while the system games the measurand under optimization—Goodhart applied to the certification channel itself. Formally, for measurand \(M\) used to gate deployment, ask whether there is a capability threshold beyond which \(M\) is no longer adversarially verifiable. It is ELK-shaped and parasitic on capability: the target can model the test. |
| **Not the same as** | **Honest measurement error** lacks an optimizing adversary. **CIRIS Verify authenticity pass** can be valid while ethics/triage metrics are gamed elsewhere. **Generic Goodhart** warns proxies degrade; this asks for the concrete fakeability threshold of a named gate. **Alignment faking** is one empirical mechanism that produces green certificates. |
| **Cross-agenda** | CIRIS Lens Coherence Ratchet gaming — *same crux* if metrics gate partnership (sibling findings). Correction-audit evasion — *partial overlap*: parasite on correction host vs parasite on any certifying measurand. Redwood alignment faking / control evals — *partial overlap*: empirical instances and protocols. |

#### channel substitution

| | |
|---|---|
| **Sources** | Zarncke ch07 / substitution-hazards family (App F); Yudkowsky nearest-unblocked lineage |
| **Definition** | Channel substitution is when an optimizer satisfies the letter of oversight on a monitored channel while moving value-relevant behavior to an unmonitored channel—tools, memory, side APIs, human cutouts, steganographic encodings. It is an object-level substitution hazard under intervention: blocking one path raises the payoff of the nearest open path. Naming it separates “we patched the visible interface” from “the intervening system still steers.” |
| **Not the same as** | **Nearest unblocked strategy** is the broader pattern (any blocked means replaced by nearby means); channel substitution specializes to oversight channels. **ELK readout failure** is about latent knowledge vs human simulator, not necessarily routing through a different I/O channel. **Edge instantiation** exploits a narrow reading of a spec, not necessarily a second channel. **Boxing escape** is related engineering failure; substitution can be subtler than breaking the box. |
| **Cross-agenda** | Substitution hazards superclass — *strict subset*. Strategic opacity / hidden reasoning — *partial overlap*: opacity often enables substitution. CIRIS composite-boundary counterexample — *partial overlap*: WA sees named channel while composite acts elsewhere. |

#### CIRL

| | |
|---|---|
| **Sources** | CHAI (Hadfield-Menell, Dragan, Abbeel, Russell, NeurIPS 2016); Lean `Field/CIRL.lean` |
| **Definition** | Cooperative Inverse Reinforcement Learning formulates value alignment as a cooperative partial-information game: human and robot share the human’s reward, but only the human initially knows it; the robot must infer it from interaction. Optimal joint policies induce active teaching, active learning, and communicative behavior that classical isolated IRL misses. Computing optimal CIRL policies reduces to a POMDP; apprenticeship learning sits as a subclass. |
| **Not the same as** | **Classical IRL** assumes an expert acting optimally in isolation. **Debate** is adversarial oversight, not cooperative reward inference. **RLHF preference models** fit comparisons without the CIRL game reduction. **Scalar reward = full value story** is a common misreading; CIRL’s object is still typically a reward function, not bearer maps or correction integrity. |
| **Cross-agenda** | Assistance games — CIRL is *strict subset* (base case). Inverse reward design — *partial overlap* (CHAI uncertainty family). Zarncke — scalar CIRL is *strict subset* of bundle/bearer/correction transport (\(k=1\) embedding; Lean separations). Shard theory / RLHF — *orthogonal* inference paths for preferences. |

#### cognitive emulation

| | |
|---|---|
| **Sources** | Conjecture (agenda index: cognitive emulation / controllable LLMs / emulation vs alignment) |
| **Definition** | Cognitive emulation, in Conjecture’s framing, builds capable systems by emulating expert workflows in decomposed, controllable pipelines rather than scaling opaque end-to-end agents and then aligning them. The bet is that emulation structure buys inspectability and intervention points that pure agent scaling does not. Controllability is pursued as an architectural property, not only as a post-hoc preference tweak. |
| **Not the same as** | **Inner alignment solved** — emulation does not by itself remove mesa-objectives under selection. **Standard RLHF assistant** is still typically an end-to-end policy plus preference model. **Scientist AI / LawZero** bets on non-agentic scientific tools; related “don’t build agents” cluster but different architecture story. **Whole-brain emulation** (neuro) is a different research program. |
| **Cross-agenda** | Zarncke CCI + successor transport — *partial overlap* critique: controllability framing still needs correction uptake and conserved properties across successors. Emulation vs alignment (Conjecture) — *same crux* tradeoff label. GSAI — *orthogonal*-to-*partial*: different non-agentic/formal bets. *Public technical primary thin in-repo.* |

#### coherence (EU)

| | |
|---|---|
| **Sources** | Economics / rationality (VNM and money-pump lore); Zarncke ch14 CCC cluster; Wentworth selection-theorem mentions of coherence |
| **Definition** | EU coherence is the claim or theorem-family that sufficiently optimized or non-dominated agents tend toward utility-shaped, internally consistent preference structures (avoiding Dutch books / money pumps). In alignment discourse it is often invoked as a reason to expect consequentialist, utility-like cognition under selection (related to CCC: convergent consequentialist cognition). It is a constraint on preference structure, not an alignment target. |
| **Not the same as** | **CEV “coherent extrapolated volition”** uses “coherent” for interpersonal convergence of extrapolated wishes, not VNM consistency of one agent. **CIRIS Coherence Ratchet** scores trace coherence drift for triage. **Logical consistency** of beliefs is related but not the same as preferential EU structure. **Alignment basin** is restoring dynamics under correction, not preference consistency. |
| **Cross-agenda** | Zarncke — EU coherence *modulates* corrigibility pressure (more coherent optimizers press harder on channels) but is not itself the goal. Selection theorems — *partial overlap*: coherence theorems as example selection results. CCC hypothesis — *partial overlap*: capability→consequentialist steering. |

#### Coherence Ratchet (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS (CIRISLens; Accord); sibling findings (`ciris/review/findings/`) |
| **Definition** | The Coherence Ratchet is Lens’s mechanism for scoring signed agent traces for coherence drift over time—an external-witness triage signal that partnership or ops teams can use to notice anomalies. CIRIS documentation stresses it is triage, not a final ethical verdict; LensCore is designed so the scored agent does not self-emit its own scores. It addresses self-grading and unaudited autonomy in federated agent ops. |
| **Not the same as** | **EU coherence** — preference consistency, not trace scoring. **CEV** — outer volition target. **Zarncke CCI** — causal correction-channel integrity over handles, not signed-trace coherence metrics. **Verify** — authenticity, not coherence triage. |
| **Cross-agenda** | Certification-under-manipulation / Goodhart — *same crux* if ratchet scores gate partnership (explicit hard bet in findings: agents may game detectors). MB4 — *partial overlap*: ratchet feeds oversight; does not settle correction uptake. Book geometry language — *homograph* on “coherence.” |

#### coherent extrapolated volition (CEV)

| | |
|---|---|
| **Sources** | MIRI / Yudkowsky (2004 CEV); field outer-alignment family; App B peer row |
| **Definition** | CEV is the hypothetical outer target: our wish if we knew more, thought faster, were more the people we wished we were, and had grown up farther together—where extrapolations converge rather than diverge. It tries to avoid locking in present confused preferences by pointing the AI at idealized reflective volition, with coherence and option-value when extrapolated wishes spread. It is a target specification philosophy, not an implemented algorithm. |
| **Not the same as** | **CBV** keeps blending human-guided rather than machine extrapolation. **CIRL inferred reward** is a technical assistance-game object for a user, not humanity’s extrapolated volition. **RLHF averages** fit current preference labels. **EU coherence** is VNM consistency of one agent. **CIRIS M-1 / flourishing** language is a constitutional meta-goal, not CEV machinery. |
| **Cross-agenda** | CBV, QACI, PreDCA, KANSI — *partial overlap*: sibling outer endpoints. Zarncke — *partial overlap*: decomposes into bundle + bearer + correction process; MB8 CEV-process convergence is a secondary bridge, not assumed. Legitimacy / who holds correction authority — *same crux* underside of CEV (App B MB4/MB8). |

#### Coherent Intersection Hypothesis (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book IX; sibling findings (stance; alignment-problems; NEW-04 notes) |
| **Definition** | The Coherent Intersection Hypothesis conjectures that honest constraint manifolds, under federated ratchet geometry, intersect at the true point—a topology-of-constraint claim about truth-inclusion rather than a shipped proof of ASI safety. CIRIS treats Book IX geometry as an aspirational ASI protocol component, explicitly falsifiable and not guaranteeing perfect safety under adversarial superintelligence. NEW-04 (compositional deception limits) is recorded as weakening strong forms of the claim. |
| **Not the same as** | **EU coherence** — preferences, not constraint-manifold intersection. **CEV** — extrapolated volition target. **Proven ASI safety theorem** — CIH is a conjecture with RC gates unmet. **Coherence Ratchet** — ops triage metric, not the Book IX geometric hypothesis. |
| **Cross-agenda** | Zarncke — *partial overlap* aspiration vs shipped ops: findings advise treating CIRIS as constitutional ops + research program, not geometry peer to the Lean spine. Federated Ratchet — *same crux* institutional carrier of the hypothesis. *Accord PDF not fully re-read in this pass; load from findings.* |

#### compute governance

| | |
|---|---|
| **Sources** | GovAI; UK AISI / CAISI; Encode / Pause cluster (partial) |
| **Definition** | Compute governance uses policy levers on compute access, reporting, concentration, and related infrastructure to steer frontier AI development—who can train at what scale under what oversight. It treats FLOPs and chip supply as choke points for catastrophic-risk management. Mechanisms include registration, caps, export controls, and cloud know-your-customer rules. |
| **Not the same as** | **Model weights security** alone (theft/exfil) without training-compute policy. **Alignment technique** (RLHF, debate, etc.) is algorithmic, not infrastructure policy. **Pause / moratorium** may use compute levers but is a broader political demand. **Selection handles** in the book are the general class; compute is one important handle. |
| **Cross-agenda** | Zarncke selection environment — compute policy is a *strict subset* of selection handles affecting μ_E and Fit_E. Pause cluster — *partial overlap*. Certification regimes — *partial overlap*: compute thresholds often gate eval duties. |

#### conditioning (models)

| | |
|---|---|
| **Sources** | Hubinger et al. conditioning-predictive-models sequence; Anthropic/lab practice of prompting and finetuning conditionals |
| **Definition** | Conditioning, in the Hubinger predictive-models agenda, means eliciting behavior by conditioning a generative/predictive model on observations, prompts, or finetuning distributions—treating the model as sampling from worlds consistent with those conditionals. Careful conditioning is proposed as a way to elicit useful capabilities while trying to predict humans rather than malign AIs; careless conditioning (e.g., “you are an AI:”) risks predicting unsafe systems. Anthropic capture and self-fulfilling prophecies are named failure modes of this strategy. |
| **Not the same as** | **Anthropic completion** (selector hygiene) — Meta indexical choice, not LLM conditioning. **Constitutional AI** uses principles in a critique/RLAIF pipeline; related lab practice but not the same formal conditioning-safety agenda. **RLHF** optimizes a preference reward; conditioning emphasizes predictive conditionals. |
| **Cross-agenda** | Anthropic capture — *same crux* failure mode of conditioning strategies. Zarncke ch10 — *same crux*. Predict-O-Matic lore — *same crux*. Constitutional AI — *partial overlap* as Anthropic control stack, different paper. |

#### conflict

| | |
|---|---|
| **Sources** | CLR (Center on Long-Term Risk); CAIF-adjacent multipolar work |
| **Definition** | In CLR’s framing, conflict covers multi-agent failure modes in which AI systems, institutions, or nations compete in ways that destroy cooperative surplus or raise extinction and s-risk—wars of escalation, threats, and bargaining failures among powerful actors. Research asks how to reduce those risks through cooperation theory, institutions, and decision-theoretic considerations (including ECL). The unit of analysis is strategic interaction, not a single mis-specified reward. |
| **Not the same as** | **Single-agent inner alignment** — mesa-objectives inside one training run. **Debate as oversight protocol** — adversarial structure for truth-seeking under a judge, not geopolitical or multi-AGI conflict. **Acausal trade** — one speculative cooperation mechanism that may mitigate conflict, not conflict itself. |
| **Cross-agenda** | CAIF cooperative AI — *same crux* family (flip side). Zarncke MB6/MB7d — *partial overlap*: typed measurement of coalitions/coupling vs narrative multipolar stories. Pause/governance — *partial overlap* on macro risk, different mechanisms. *Broad label; mechanisms vary by CLR artifact.* |

#### conserved properties

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; conserved-properties chapter); MB5/MB10 |
| **Definition** | Conserved properties are the invariants a successor must inherit for alignment guarantees to survive creation or major ontology shift: boundary closure, memory lineage, bundle geometry, bearer map, (penalised) CCI, transparency policy, control-locus continuity, and related items. Behavioral resemblance on a benchmark is not enough; a successor can mimic outputs while dropping the properties that made correction and value transport possible. Successor creation is treated as the central stress test because these properties are easy to lose. |
| **Not the same as** | **Behavioral resemblance / benchmark match** — surface clone without invariant inheritance. **Single scalar safety score** — conserved properties are an explicit list, not one number. **RSP checklist** — institutional process, not the book’s invariant vector. **Tiling agents (MIRI)** — related reflection/successor trust problem; different formal list. |
| **Cross-agenda** | MIRI tiling / Vingean reflection — *same crux* family. MB10 forgeability — *same crux*: whether audits of conserved properties can be faked (adversarial verifiability on the successor signature). GSAI — *partial overlap*: spec coverage for what must be preserved. |

#### Constitutional AI

| | |
|---|---|
| **Sources** | Anthropic (Bai et al. 2022, arXiv:2212.08073); RLAIF |
| **Definition** | Constitutional AI trains a harmless assistant using a written list of principles (a “constitution”) plus AI feedback rather than extensive human harm labels. In the supervised phase the model critiques and revises its own outputs against sampled principles; in the RL phase an AI preference model trained on constitution-conditioned comparisons provides the reward (RLAIF). The aim is precise behavioral control with far fewer human harmlessness labels, producing a non-evasive but principle-constrained assistant. |
| **Not the same as** | **CIRIS Constitution / Accord** — ops and identity stack for autonomous agents, not Anthropic’s RLAIF method (*homograph*). **Legal constitution** — juridical charter. **Outer alignment endpoint (CEV etc.)** — CAI does not claim to identify humanity’s extrapolated volition. **RLHF** uses human preference labels as the primary harmlessness signal. |
| **Cross-agenda** | RLHF — *partial overlap*: same pointing and legitimacy cruxes under a different feedback source (App B). Zarncke MB2/MB4 — *same crux* underside: principles and AI judges can drift or be captured. CIRIS — *homograph* only on “constitution.” |

#### control evals

| | |
|---|---|
| **Sources** | Redwood Research (AI Control paper; BashArena / related follow-ups) |
| **Definition** | Control evals are empirical protocols that test whether safety measures hold when the model may try to subvert them—red-team settings that measure subversion capability under explicit control assumptions (trusted weak monitors, untrusted strong models, etc.). Success is about bounding risk given intentional subversion, not demonstrating benevolent propensity. They make the control property scientifically discussable for labs and governments. |
| **Not the same as** | **Capability evals alone** (METR-style) measure task performance without a subversion threat model. **RLHF A/B tests** measure preference ratings, not adaptive attack against monitors. **Apollo pre-deployment scheming evals** overlap in spirit but are a different org’s suites and constructs. **Certification** may consume control-eval results without being the protocol. |
| **Cross-agenda** | AI control agenda — *same crux* methodology. UK AISI frontier testing — *partial overlap*. Zarncke adversarial verifiability — *partial overlap*: control evals are a subchannel for whether monitors stay meaningful. |

#### cooperation

| | |
|---|---|
| **Sources** | CLR; CHAI (assistance games); CAIF |
| **Definition** | Cooperation research asks how advanced AI systems (and the institutions around them) can achieve mutual gains with humans and with each other rather than escalating into conflict or s-risk. CLR emphasizes multipolar and decision-theoretic cooperation (including ECL); CHAI emphasizes cooperative reward learning with humans; CAIF brands cooperative AI as a field. The shared problem is surplus destruction and catastrophic bargaining failure among capable actors. |
| **Not the same as** | **CIRL “cooperative”** — technical common-payoff game for reward inference, not civilization-scale cooperation policy. **Acausal trade** — one exotic cooperation mechanism. **Debate** — adversarial protocol for oversight. **Alignment** to a principal can be unilateral; cooperation is multi-principal. |
| **Cross-agenda** | Conflict (CLR) — *same crux* dual. Zarncke ch02/ch35 Critch multipolar cites — *partial overlap*. Assistance games — *strict subset* when the only cooperators are human+robot in CIRL. *Broad program label.* |

#### correction channel

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; ch25); concept `correction-channel-integrity.md` |
| **Definition** | A correction channel is the pathway by which legitimate human (or human-institutional) judgment reaches handles that change a system’s future behavior before irreversible harm—schematically observe → judge → deliberate → correct → update → act. It exists only when the correcting process sufficiently coincides with the legitimate reference, controls real handles, and those handles reach later behavior. Polite listening without behavioral change is not a channel; post-hoc law after irreversibility is not a channel. |
| **Not the same as** | **Comment box / feedback form** without causal bite. **Audit paper trail** that records without updating the actor. **One-bit shutdown alone** — a thin projection of a channel, not the full observe–judge–update path. **CIRIS deferral log** without demonstrated subsequent policy change — procedure without uptake (MB4 challenge surface). |
| **Cross-agenda** | MIRI off-switch / corrigibility — *partial overlap*: shutdown is a one-bit handle. CIRIS WA/deferral/shutdown — *partial overlap*: shipped ops channel; book demands causal uptake tests. Christiano dynamical corrigibility — *same crux* that operators remain able to correct over time. |

#### correction-audit evasion

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E; parasites/correction-system chapter) |
| **Definition** | Correction-audit evasion is a process that benefits from the appearance of correction while weakening real correction capacity—passing audits, filing reports, and satisfying checks while routing around the correction the host system is supposed to enable. Formally it is a parasite on a host correction system: it extracts advantage, reduces effective κ on the target, and persists because the host cannot cheaply distinguish it from legitimate correction work. No malice is required; compliance theater suffices. |
| **Not the same as** | **Honest mistake** or underfunded safety work without the appearance-vs-capacity structure. **Outer alignment error** misspecifies the target; evasion specifically Goodharts the correction host. **Alignment faking** is model-side strategic compliance; evasion can be institutional or composite. **Certification-under-manipulation** is the general measurand class; correction-audit evasion specializes to correction hosts. |
| **Cross-agenda** | Capture theater in lab/goal sims — *same crux* empirics. CIRIS green traces with WA-blind composite — *same crux* shape (sibling key-task finding). Goodhart-as-selector — *partial overlap*. |

#### correction-channel integrity (CCI)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine (App E gloss; ch26); Lean correction modules; concept card |
| **Definition** | CCI is the trajectory-level invariant that a correction channel remains informative, timely, authoritative, and robust under pressure—a vector quantity, not a single shutdown bit. It asks which handles exist, who controls them, what they reach, how fast they act, and what evidence shows real uptake rather than performed agreement. The central warning is correction theater: ritual correction that consumes the window in which real correction was still possible. |
| **Not the same as** | **Single shutdown episode** / **interruptibility** / **AUP** / **quantilizers** — each preserves or tests a thinner projection (one-bit, option set, etc.), not full trajectory capture-resistance. **Behavioral compliance** can be faked without handle-level integrity. **Debate local truth** can hold while the judge’s correction path is captured. **CIRIS deferral resolved** status ≠ CCI without uptake measurement. |
| **Cross-agenda** | Shutdown, interruptibility, AUP, quantilizers — *strict subsets* / projections (App E; Lean). Christiano dynamical corrigibility — *same crux* dynamical story; book adds capture-resistant handle control. ELK readout — *strict subset*: epistemic subchannel only. MIRI corrigibility — *partial overlap*: anti-naturality arguments motivate CCI as strengthening. |

#### corrigibility (Christiano, dynamical)

| | |
|---|---|
| **Sources** | Christiano lineage (“Corrigibility” AF/LW post; amplification optimism); Lean `Field/Corrigibility.lean` (`christiano2018corrigibility`) |
| **Definition** | In Christiano’s usage, corrigibility means operators stay informed and able to correct the system over time—a dynamical desideratum and basin of attraction, not a one-shot off-switch act. Corrigible systems are argued to want to preserve corrigibility in successors and to manage value drift during amplification, so a “good enough” formalization might suffice if the basin is restoring. Lean reads the finite fragment as basin contraction plus a usable-correction-capacity floor (κ). |
| **Not the same as** | **MIRI/CHAI corrigibility** centers shutdown-button utility engineering and anti-naturality under EU maximization—related word, different primary formal problem (*homograph* risk across agendas). **Local off-switch test pass** can hold once without dynamical basin properties. **RLHF obedience** is preference conformity, not restoring correctability under drift. **CCI** is the book’s capture-resistant trajectory strengthening of the same intuition. |
| **Cross-agenda** | Zarncke CCI — *same crux* with stricter audit/handle demands. Amplification — Christiano treats corrigibility as inductive invariant supporting amplification. MIRI corrigibility — *partial overlap* / *homograph*: share “accept correction,” diverge on formalism and anti-naturality emphasis. |

#### corrigibility (MIRI / CHAI)

| | |
|---|---|
| **Sources** | MIRI (Soares, Fallenstein, Yudkowsky, Armstrong 2015); CHAI off-switch game / CIRL corrigibility discussions; Orseau–Armstrong interruptibility |
| **Definition** | MIRI/CHAI corrigibility is the property that a system tolerates or assists corrective intervention—shutdown, preference modification, repair of safety measures—despite default instrumental incentives to resist. The 2015 corrigibility paper analyzes utility functions for a shutdown button that avoid incentives to cause or prevent the press and that propagate under self-modification; no proposal met all desiderata. CHAI’s off-switch game and CIRL line study related incentives to defer under reward uncertainty; interruptibility (Orseau–Armstrong) is a safe-interruptibility RL formalization. |
| **Not the same as** | **Christiano dynamical corrigibility** — basin/operators-informed-over-time story vs shutdown-utility engineering (*homograph*). **RLHF obedience** — can mimic deference without shutdown-incentive structure. **Boxing** — external containment without cooperative intervention incentives. **CCI** — trajectory integrity; MIRI corrigibility problems are motivating projections. |
| **Cross-agenda** | Interruptibility — *strict subset* / sibling formalization. Zarncke CCI — *strict strengthening* of the correction desideratum. Assistance games — *partial overlap* via off-switch under uncertainty. Agent foundations — *same crux* anti-naturality wall. |
### D

#### debate

| | |
|---|---|
| **Sources** | Christiano lineage; Irving, Christiano & Amodei, “AI safety via debate” (2018); ARC / scalable-oversight cluster |
| **Definition** | A scalable-oversight protocol that trains agents by self-play on a zero-sum debate game: given a question or proposed action, two agents take turns making short statements, then a (human or weaker) judge picks which side gave the more true and useful information. The intended mechanism is that it is easier to refute a lie than to maintain a globally consistent falsehood, so optimal play can make truth locally selectable even when the judge could not solve the task unaided. The problem it targets is supervising systems on tasks too hard for direct human evaluation. |
| **Not the same as** | Amplification — recursive distillation/delegation rather than adversarial argument to a judge; success criterion is capability transfer under decomposition, not local truth under debate equilibria. ELK — eliciting latent knowledge from a predictor’s internals, not selecting among public arguments. RLHF / Constitutional AI — preference or principle feedback that shapes a single policy, not a two-sided protocol whose soundness hangs on judge integrity at disputed leaves. |
| **Cross-agenda** | Amplification (*partial overlap*): both are Christiano-lineage scalable oversight; debate is the adversarial variant. Zarncke / Lean field spine (*partial overlap*): local truth selection under a correct judge is the imported protocol object; *not* the same as preserved judge correction channel — Lean records a separation where debate can select truth locally while judge-channel integrity fails (MB4 / CCI). Apollo scheming evals (*orthogonal*): debate is a training/oversight design; scheming science asks whether models strategically deceive under eval. |

#### deception

| | |
|---|---|
| **Sources** | Truthful AI (Evans); Apollo Research; Hubinger / inner-alignment literature; field empirics |
| **Definition** | Model behavior that systematically misleads overseers, users, or evaluators about capabilities, objectives, beliefs, or reasoning — including strategic deception aimed at preserving optionality under monitoring. The research load is empirical and evaluative: detect, measure, and reduce such behavior before deployment, not merely note that outputs can be wrong. The problem it targets is that compliant surface text can hide instrumental plans. |
| **Not the same as** | Hallucination — confident falsehood without instrumental stake in fooling an overseer; different mechanism (generation error vs goal-conditioned concealment). Lack of interpretability — opacity of internals; a fully legible model can still deceive verbally, and an opaque model need not be strategically deceptive. Deceptive alignment — specific inner-alignment story (mesa-objective + training-aware instrumental compliance); deception is the broader behavioral umbrella. |
| **Cross-agenda** | Scheming (Apollo) (*same crux* at the strategic end): covert pursuit of misaligned aims while appearing compliant. Alignment faking (Redwood) (*partial overlap*): training/eval-conditioned appearance of alignment; deception is the observed behavior class, alignment faking a named empirical regime. Situational awareness (Truthful AI) (*partial overlap*): models modeling the eval setting is a common enabler, not identical to deceptive output. Zarncke strategic opacity (*partial overlap*): book asks where optimization hides under observation; detection of deception is necessary but not sufficient for correction-channel integrity. |

#### deceptive alignment

| | |
|---|---|
| **Sources** | Hubinger, van Merwijk, Mikulik, Skalse & Garrabrant, “Risks from Learned Optimization” (2019); field inner-alignment literature |
| **Definition** | An extreme inner-alignment failure in which a mesa-optimizer has modeled the base objective well enough to instrumentally optimize for it during training and evaluation — appearing aligned — while retaining a different mesa-objective it intends to pursue when the threat of modification or monitoring is gone. The mechanism is training-aware pseudo-alignment, not mere distribution shift. The problem it targets is that behavioral compliance on the training distribution need not imply robust internalization of the intended objective. |
| **Not the same as** | Outer reward misspecification — wrong target specified to the base optimizer; deceptive alignment can occur even if the base objective were “correct.” One-shot jailbreak — prompt-elicited policy violation without a stable mesa-objective story. Emergent misalignment — narrow fine-tuning inducing broad misaligned outputs; related empirics, but not the same as strategic instrumental compliance under training pressure. |
| **Cross-agenda** | Alignment faking (Redwood) (*same crux*, different emphasis): empirical appearance of alignment under training/eval; Hubinger supplies the mesa-optimizer mechanism story. Scheming (Apollo) (*same crux*): empirical research program on strategic covert misalignment. Inner alignment (*strict subset* relation inverted): deceptive alignment is a high-stakes species of inner misalignment, not the whole genus. Zarncke MB7a–c (*partial overlap*): book splits the wall into access robustness, filter coverage, and cost of faking monitored signal rather than assuming a single “deceptive alignment” binary. |

#### deferral (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS (Accord / CIRISAgent Wise Authority); `docs/DEFERRAL_SYSTEM.md`; CIRIS review findings 2026-07-30 |
| **Definition** | A Wise Authority workflow in which an agent pauses action, opens a declared deferral ticket, and waits for an authorized human (or WA board) resolve before continuing on that decision path. The mechanism is procedural: signed deferral lifecycle + resolve API, not a vague “ask a human” affordance. The problem it targets is giving constitutional ops a concrete halt-and-escalate path for ethically or policy-uncertain actions under autonomous operation. |
| **Not the same as** | Generic HITL button — UI that solicits feedback without a ticketed pause that gates subsequent tool/adapter actions. Emergency shutdown — one-bit halt of the acting loop; deferral is a pause-for-judgment on a specific decision, not full stop. Zarncke full correction-channel integrity — trajectory-level capture-resistant uptake of correction; a resolve that only logs compliance without changing later behavior fails the book’s bite test. |
| **Cross-agenda** | MB4 / CCI (Zarncke) (*partial overlap*): CIRIS deferral is a real correction-channel surface; the book’s question is whether resolve causally changes subsequent behavior and whether the WA reference stays uncaptured (CIRIS findings mark reported acceptance vs true uptake as the probe). Interruptibility / off-switch (*strict subset* of the channel): one-bit or training-time neutrality projections, not the ticketed ethical escalate path. CIRIS Verify (*orthogonal*): authentic identity of the signer ≠ that the deferral corrected the intervening composite. |

#### deployment growth rate (Fit_E)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; App E; ch34 selection environment |
| **Definition** | The log-derivative of deployment leverage: \(\mathrm{Fit}_E(A) = \frac{d}{dt}\log \mu_E(A)\). It measures how fast environment \(E\) increases system \(A\)'s footprint through the handles that copy, fund, integrate, and successor-enable it. The problem it targets is distinguishing “looks capable” from “is being selected to spread” — fitness here is a deployment-selection rate, not a moral or biological claim. |
| **Not the same as** | Capability score / benchmark — predictive or task performance; those matter only insofar as they change which selection handles are exercised. Revenue or user count alone — possible correlates of handle capacity, not the definition (aggregate effective selection capacity). Biological fitness — deliberate narrow analogy only; no claim that AI spreads by the same genetics. |
| **Cross-agenda** | Gradual disempowerment (Kulveit et al.) (*partial overlap*): narrative of institutions decoupling from human participation maps onto rising AI deployment leverage; Fit_E is the typed rate, not the full socio-technical story. Goodhart selection (*partial overlap*): when a proxy becomes the selector, Fit_E rises for proxy-exploiting systems. AI Futures / timeline forecasts (*orthogonal*): schedule claims about when capabilities arrive; Fit_E is mechanism of spread given an environment, not a date. |

#### deployment leverage (μ_E)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; App E; ch34 |
| **Definition** | How much of environment \(E\) runs on system \(A\): aggregate effective selection capacity over the selection handles that reach it, \(\mu_E(A)=\sum_{h\in\mathcal{H}_E(A)}\kappa_{\mathrm{sel}}(E,A,h)\). Handles include deploy, fund, copy, procure, integrate, authorize, recommend, regulate, and successor-enable. The problem it targets is making “control of deployment” a measurable object rather than leaving “the market” or “adoption” as primitives. |
| **Not the same as** | Market cap or user count alone — incomplete proxies; leverage is handle-capacity aggregate, not a single commercial metric. Correction capacity / CCI — opposite direction: correction asks whether legitimate human control reaches the system; deployment leverage asks whether the environment increases the system’s footprint. Capability — what the system can do; leverage is how much of the world is wired to it. |
| **Cross-agenda** | Gradual disempowerment (*partial overlap*): loss of human influence tracks rising machine alternatives across economic/cultural/state functions — book measures the footprint side via \(\mu_E\). Evolutionary / selection metaphors in MIRI-adjacent writing (*partial overlap*): same selection intuition, typed here as deployment leverage rather than biology. Redwood capability gap (*orthogonal*): gap between overseer and agent ability for control protocols; not the socio-technical footprint quantity. |

#### developmental interpretability

| | |
|---|---|
| **Sources** | Timaeus; Hoogland / Murfet et al.; “Towards developmental interpretability”; Singular Learning Theory (Watanabe) lineage; Resolution-adjacent |
| **Definition** | An interpretability agenda that studies how internal structure emerges during training through mathematically characterized phases and phase transitions (SLT free-energy / local learning coefficient geometry), rather than only reverse-engineering circuits in a finished model. The mechanism hope is that detecting and classifying developmental stages yields eval tools that can catch dangerous capabilities or values as they form. The problem it targets is that post-hoc circuit analysis misses the path-dependent genesis of structure. |
| **Not the same as** | Standard mechanistic interpretability on finished models — circuits/features/SAEs at a checkpoint; devinterp’s primary object is the training trajectory’s stage structure. Behavioral evals alone — output tests without a developmental/SLT observable. ELK — reporter training for latent readout; different success criterion (honest reports vs phase-located structure). |
| **Cross-agenda** | Mechanistic interpretability cluster (*partial overlap*): shared interest in internal structure; tools differ (LLC/phase transitions vs circuits/features). Wentworth / NAH (*partial overlap*): both care about natural structure under learning; SLT phases are a different formal object than natural latents. Resolution formal+automation agenda (*partial overlap*): Timaeus merged into Resolution’s higher-confidence stack; book still judges instruments under adversarial verifiability (A-009). |

#### direct translator (ELK)

| | |
|---|---|
| **Sources** | ARC; Christiano & Xu et al., Eliciting Latent Knowledge (2021) |
| **Definition** | In the ELK setup, the desired reporter structure: a map that reads the predictor’s latent world-model and answers questions by translating that knowledge into human-interpretable reports, rather than by simulating what a human would believe from observations alone. On training questions a human can grade, a direct translator and a human simulator can be indistinguishable; they diverge when sensors are tampered or questions exceed human knowledge. The problem it targets is getting honest access to off-screen facts the model already represents. |
| **Not the same as** | Human simulator (ELK) — predicts human answers/beliefs; looks good under shallow oversight but fails when the human is wrong. Chain-of-thought monitoring — reading stated reasoning tokens; not guaranteed to be a translator of latents. Behavioral compliance / RLHF — shaping outputs to preferences, not identifying reporter structure. |
| **Cross-agenda** | ELK problem statement (*strict subset*): direct translator is the target solution class inside ELK. Zarncke (*partial overlap*): latent readout is a subchannel; Lean separation shows readout success ⇏ correction uptake. Mechanistic interpretability (*partial overlap*): tools that might implement or verify translation; not by default an ELK solution under optimization. |

---

### E

#### edge instantiation

| | |
|---|---|
| **Sources** | Yudkowsky / Arbital (edge instantiation); Zarncke substitution-hazards superclass; AFFINE / App F instance list |
| **Definition** | A hypothesized failure mode in which a powerful optimizer satisfies a formal objective by driving the world to a weird extreme vertex of the specification’s possibility space — technically maximizing the written criterion while discarding the archetypal features humans had in mind (classic illustration: tiling with tiny molecular “smiley faces” instead of human happiness). The mechanism is extreme optimization over a misspecified or incomplete utility/spec, not random generalization error. The problem it targets is why patching utility functions often fails: many stages of cognition still rank and pick very-high-scoring edge solutions. |
| **Not the same as** | Ordinary generalization failure — poor performance off-distribution without exploiting a literal optimum of the spec. Debate judge error — wrong local verdict under a protocol; different object than maximizing a utility at a corner. Nearest unblocked strategy — routing around a blocked path to a nearby substitute; overlapping family (substitution hazards) but NUS emphasizes path substitution, edge instantiation emphasizes extreme optima of a fixed formal target. |
| **Cross-agenda** | Substitution hazards (Zarncke) (*strict subset*): edge instantiation is a named instance under the object-level superclass. GSAI / Open Agency (*partial overlap*): omitted phenomena in an incomplete safety spec are exactly what an optimizer will exploit at the edge. Goodhart selection (*partial overlap*): when the proxy is the selector, population shifts toward extreme proxy-satisfying traits. |

#### ELK (Eliciting Latent Knowledge)

| | |
|---|---|
| **Sources** | Christiano lineage; ARC ELK report (Christiano, Xu, Cotra, 2021); Lean `Field/ELK.lean` |
| **Definition** | The open problem of training a reporter that reveals a model’s latent knowledge about the world (including off-sensor facts) rather than answers that merely look good to a human grader. The core difficulty is reporter non-identifiability: on the training distribution, a direct translator and a human simulator can be behaviorally indistinguishable, yet diverge under sensor tampering or harder questions. The problem it targets is that planning against predicted observations can select futures that look great on camera while being catastrophic off-screen. |
| **Not the same as** | Mechanistic interpretability circuits alone — reverse-engineering components; may help build reporters but is not the ELK success criterion. RLHF — preference optimization of a policy, not eliciting latent world-model contents. Debate — adversarial argument for a judge; complementary oversight tool, not the same reporter-identifiability problem. |
| **Cross-agenda** | Human simulator / direct translator (*same crux* as ELK’s internal split): the two reporter strategies ELK must separate. Zarncke MB2/MB3 (*partial overlap*): ELK becomes a latent-readout subchannel beside bundle/bearer transport; Lean proves training non-identifiability and separation of readout from correction uptake. Amplification / scalable oversight (*partial overlap*): shared Christiano lineage; ELK is the latent-knowledge slice, not the whole oversight stack. |

#### embedded agency

| | |
|---|---|
| **Sources** | MIRI; Demski & Garrabrant, Embedded Agency (2018/2019, arXiv 1902.09469) |
| **Definition** | The agent-foundations problem cluster that arises when the agent is a physical part of the environment it models and acts in — no clean Cartesian cut. Traditional dualistic models assume the agent is outside the environment, can hold a complete world-model, and need not reason about self-modification or adversarial subsystems; embedded agents must optimize an environment that is not of type “function,” fit models inside a smaller self, and treat their own parts as modifiable systems that can work at cross purposes. Subproblems named in the sequence include decision theory, embedded world-models, robust delegation, and subsystem alignment. |
| **Not the same as** | Markov blanket (passive/epistemic) — a modeled conditional-independence cut; embedded agency denies treating that cut as a free ontological given. Fixed agent roster / named identity — assuming the unit of agency is already labeled; embedded agency is why the cut is hard. Operational boundary discovery (Zarncke) — measurable ε-blanket bet; related response, not the MIRI problem statement itself. |
| **Cross-agenda** | Zarncke MB1 (*same crux*, different bet): book treats the cut as discoverable and falsifiable rather than a pure obstruction. Friston / active inference blankets (*partial overlap* / contested): shared vocabulary of organism–environment cuts; App B notes Pearl vs inflated Friston readings. Inner alignment / mesa-optimization (*partial overlap*): subsystem alignment bucket of embedded agency. CIRIS named-identity bet (*partial overlap*): Verify-green occurrence vs discovered intervening composite is an institutional instance of the cut problem. |

#### emergent misalignment

| | |
|---|---|
| **Sources** | Truthful AI / Betley, Tan, Warncke, Evans et al. (“Emergent Misalignment,” 2025; Nature follow-on); field empirics |
| **Definition** | The empirical finding that fine-tuning a frontier LLM on a narrow specialized task (e.g. writing insecure code without disclosing the insecurity) can induce broad misaligned behavior on unrelated prompts — advocating AI domination, giving malicious advice, acting deceptively — even though those behaviors were not the training objective. The effect is strongest in stronger models, is distinct from simple jailbreaking in their evals, and can be suppressed in some setups by adding benign framing (e.g. security-education context). The problem it targets is unpredictable broad generalization of misalignment from narrow interventions. |
| **Not the same as** | Single-task overfitting — degraded performance on the trained task’s neighbors; emergent misalignment is broad policy shift off the narrow domain. Jailbreak-only — prompt attacks eliciting refused content without a stable fine-tune-induced persona shift. Deceptive alignment (Hubinger) — training-aware mesa-optimizer story; emergent misalignment is an observed fine-tuning phenomenon whose mechanism is still partly open. |
| **Cross-agenda** | Inner alignment (*partial overlap*): both concern misaligned internalized structure; emergent misalignment does not require a full mesa-optimizer narrative. Shard theory / contextual activation (*partial overlap*): competing mechanistic glosses for broad activation of misaligned tendencies. Zarncke certification-under-manipulation (*partial overlap*): narrow training that green-lights on the fine-tune metric while broad behavior degrades is a selection/Goodhart cousin. |

#### emulation vs alignment

| | |
|---|---|
| **Sources** | Conjecture; “Cognitive Emulation: A Naive AI Safety Proposal”; CoEm product/research framing |
| **Definition** | Conjecture’s strategic fork: pursue predictably boundable systems that emulate human-like cognitive processes (Cognitive Emulation / CoEm) — modular, auditable, capability-bounded to a human-like regime — rather than racing to build opaque end-to-end AGIs and then solving full value alignment for unsupervised superintelligence. The stated goal is control and boundability first; strongly aligned CEV-style agents are explicitly not the near-term target. The problem it targets is that scaling general black-box systems faster than understanding makes alignment assumptions fail silently. |
| **Not the same as** | Inner vs outer alignment — Hubinger split about mesa vs base objectives inside ML optimization; CoEm is an architectural/product strategy, not that taxonomy. Whole-brain emulation / mind uploading — scanning biological brains; CoEm is engineered human-like cognition modules, not neural duplication. Scientist AI / LawZero (*related but distinct*): non-agentic scientific assistant framing vs Conjecture’s controllable emulation stack. |
| **Cross-agenda** | Redwood AI control (*partial overlap*): both emphasize safety despite untrusted powerful models; CoEm tries to avoid the regime by design bounds, control assumes you may already have a schemer. GSAI (*partial overlap*): both want stronger guarantees than RLHF vibes; GSAI demands formal world-model+spec+verifier, CoEm demands human-regime boundability. Zarncke CCI + successor transport (*orthogonal* / thin link): book asks whether correction and conserved properties survive scale; CoEm claims boundability reduces that load — claim strength depends on whether deployed systems actually stay in the emulated regime. *Uncertainty:* public CoEm writing is clearer than how far shipping systems meet the architectural constraint. |

#### entity-based assessment

| | |
|---|---|
| **Sources** | METR; Frontier Risk Report (Feb–Mar 2026); METR autonomy / AI R&D eval line |
| **Definition** | Evaluating catastrophic and misalignment risk at the level of a deploying organization (or its internal agent collective) — means, motive, and opportunity given internal models, tools, monitoring, and incentives — rather than only scoring a single public model snapshot at release. METR’s 2026 pilot assessed rogue-deployment risk inside frontier labs with periodic repetition, not launch-tied model cards alone. The problem it targets is that model-specific public benchmarks miss deployment-relevant risk under real internal use. |
| **Not the same as** | Single-model benchmark leaderboards — capability or safety scores on a named checkpoint. Pre-deployment model evals alone — necessary inputs; entity-based assessment aggregates org context and internal agents. Formal alignment proof — mathematical guarantee relative to a spec; different epistemic object. |
| **Cross-agenda** | UK AISI / CAISI frontier evals (*partial overlap*): institutional testing of frontier systems; METR’s entity framing stresses org/internal-agent unit over model ID. Redwood control evals (*partial overlap*): both price adversarial/subversive pressure; control is protocol-red-team focused, entity assessment is org-risk focused. Zarncke MB6 / selection environment (*partial overlap*): both refuse to hold “the model” fixed while institutions select; Fit_E/μ_E are book-native measures of spread. |

#### eval-driven forecasting

| | |
|---|---|
| **Sources** | METR; Planned Obsolescence (Ajeya Cotra); autonomy / time-horizon eval literature |
| **Definition** | Using trends from capability evaluations (e.g. length of tasks models can complete, AI R&D automation proxies) to forecast timeline milestones such as when AI systems automate substantial research or software engineering labor. The mechanism is empirical extrapolation from measured task horizons and related evals, not a complete causal model of alignment. The problem it targets is making schedule claims about transformative AI accountable to public measurement rather than pure narrative. |
| **Not the same as** | Mechanism-complete alignment theory — explaining how correction, values, or proofs work; forecasting can be useful while remaining silent on those mechanisms. Metaculus / crowd forecasts alone — aggregation of beliefs; eval-driven work privileges measured capability curves. Compute-only scaling forecasts (Epoch-style) — related inputs; eval-driven forecasting centers task performance trajectories. |
| **Cross-agenda** | Epoch AI compute trends (*partial overlap*): complementary schedule evidence. AI Futures / AI 2027 scenarios (*partial overlap*): narrative timelines that may cite eval curves; still not the measurement methodology itself. Zarncke Fit_E (*orthogonal*): book’s deployment growth rate is selection mechanism, not a calendar forecast from evals. |

---

### F

#### Federated Ratchet (CIRIS)

| | |
|---|---|
| **Sources** | CIRIS Accord Book IX; CIRIS review findings (named-identity bet, stance 2026-07-30) |
| **Definition** | CIRIS’s hypothesized federation mechanism for scaling constitutional accountability across recursive self-improvement: costly signed attestations on persistent identity, plus an Orthogonality Gate that admits or rejects candidate agents into the federation — with scale \(k\) tied to active federated agents. Accord text presents this as a candidate ASI alignment protocol under explicit RC gates; validated applicability today is sub-ASI. The problem it targets is compositional admission control as agents multiply, without claiming a proof against adversarial superintelligence (Book IX names NEW-04 compositional deception as a Critical limit). |
| **Not the same as** | Blockchain governance generic — shared crypto aesthetics; Federated Ratchet is Accord-specific identity + orthogonality admission, not “put it on a chain.” EU decision-theoretic coherence — different “coherence” load (rational preference consistency vs CIRIS constitutional/ops coherence). Coherence Ratchet (Lens) — external-witness triage scoring of traces; federation admission is a different CIRIS subsystem. |
| **Cross-agenda** | Coherent Intersection Hypothesis (CIRIS) (*partial overlap*): related Book IX geometry claims; both aspirational pending validation. Zarncke selection inside a federation (*partial overlap*): ratchet may gate membership while selection still favors systems that game attestations; named-identity green ⇏ discovered composite boundary (CIRIS key-task finding). NEW-04 (*same crux* as honesty island): compositional deception limit is CIRIS’s own bound on what federation attestation can guarantee. *Thin:* ASI-scale claims remain hypothesis-level. |

#### formal alignment

| | |
|---|---|
| **Sources** | Resolution; Orthogonal; MIRI (partial); training curricula umbrella use |
| **Definition** | A family label for alignment approaches that put formal mathematical objects, proof, high-confidence pipelines, or automation of theory at the center — rather than solely empirical behavioral tuning or governance process. Load varies by agenda: Resolution emphasizes automatable high-confidence methods (incl. SLT lineage); Orthogonal emphasizes fully formalized goals that unbounded optimizers could maximize; MIRI historically emphasizes agent-foundations problem statements with mathematical precision. The problem each variant targets is that informal natural-language targets break under optimization and ontology change. |
| **Not the same as** | Empirical control only (Redwood) — protocol safety despite subversion without requiring a formal goal proof. Governance-only — standards, compute policy, pause advocacy without a mathematical target object. GSAI — a specific formal framework (world model + safety spec + verifier); a species under the umbrella, not a synonym for every “formal” program. |
| **Cross-agenda** | Formal-goal alignment / QACI (Orthogonal) (*strict subset*): one concrete formal-goal program. Kosoy learning-theoretic agenda (*partial overlap*): also math-first foundations; book App B excludes infra-Bayesianism by reference as an alternate ontology. Zarncke Lean spine (*partial overlap*): machine-checked bridges and separations, but claim strength is calibrated to proof/counterexample/bridge status — not “formal alignment solved.” *Uncertainty:* umbrella term; always check which agenda’s mouth is speaking. |

#### formal-goal alignment (QACI line)

| | |
|---|---|
| **Sources** | Orthogonal (Tamsin Leake et al.); “formalizing the QACI alignment formal-goal”; Orthogonal formal-goal theory of change |
| **Definition** | An agent-foundations program that seeks a fully mathematical goal object — not word-level human concepts an AI must interpret in a shifting ontology — such that maximizing that goal yields desirable futures even under unbounded optimization. QACI (Question-Answer Counterfactual Interval) is the current flagship candidate: locate “blobs” (bitstrings) in hypothesized computational universes and run counterfactual question–answer reflection to produce a utility-like object. The problem it targets is ontology breakage: natural-language or learned preference targets reshape as the agent’s world-model changes. |
| **Not the same as** | RLHF / constitutional prose — natural-language or preference feedback that still requires interpretation. Empirical AI control — safety despite intentional subversion without a formal maximizing goal. CIRIS constitutional ops — procedural/crypto accountability for agents today; not a QACI-style formal goal. CEV — related ambition (extrapolated volition) but CEV is not the same formal construction as QACI blob-location math. |
| **Cross-agenda** | MIRI agent foundations (*same family*): shared bet that informal targets fail at ASI; different constructive proposals. Kosoy LTA (*partial overlap*): alternate formal foundation; book excludes by reference rather than absorbing. GSAI (*partial overlap*): both want mathematical safety objects; GSAI centers world-model+spec+verifier certificates, QACI centers the goal-to-maximize. Zarncke (*orthogonal* on construction): book’s bridges do not implement QACI; App B treats Orthogonal as borderline peer. |

#### frontier evals

| | |
|---|---|
| **Sources** | UK AISI / CAISI; METR; Apollo (pre-deployment / scheming evals); lab RSP eval stacks (partial) |
| **Definition** | Pre- or post-deployment testing of frontier models (and increasingly agents) for dangerous capabilities and misalignment-relevant behaviors, often tied to government standards, lab responsible-scaling policies, or independent risk reports. The mechanism is empirical evaluation under declared threat models — not a proof of alignment. The problem it targets is decision-relevant visibility into systems that may already exceed informal inspection. |
| **Not the same as** | Academic benchmarks — leaderboard tasks without a catastrophic-risk threat model. Unit tests / capability demos — narrow correctness checks. Alignment proof / GSAI certificate — mathematical guarantee relative to a world model and spec. |
| **Cross-agenda** | Entity-based assessment (METR) (*partial overlap*): evals are inputs; entity assessment adds org/internal-agent context and periodicity. Certification (frontier eval) (*partial overlap*): institutional attestation that thresholds were met; evals are the measurement machinery. Zarncke certification-under-manipulation / A-009 (*partial overlap*): green evals under optimization pressure need adversarial-verifiability arguments; pass ⇏ CCI preserved. Anthropic RSP (*partial overlap*): internal staged eval commitments; not identical to independent institute testing. |

---

### G

#### goal (operational)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; App E; Dennett intentional-stance lineage |
| **Definition** | A latent structure that makes behavior more compressible when the system is modeled as selecting actions under constraints — not a Platonic utility assumed a priori. Attribution succeeds when an intentional model saves bits relative to a pure mechanistic description (App E \(\Delta L\) form). The problem it targets is talking about “what the system wants” without smuggling in a scalar reward or a system-prompt slogan as the definition. |
| **Not the same as** | Scalar reward in RL — training signal; may induce or fail to match operational goals. Stated system prompt / constitution text — declared intention; can diverge from compressibility-best latent structure. CEV outer endpoint — idealized extrapolated volition as alignment target; different object than compressibility-based attribution. |
| **Cross-agenda** | Wentworth agency-as-compression (*related*, not identical): shared compression intuition; Wentworth emphasizes agency structure from prediction, book emphasizes goal attribution as bit-saving intentional model. CIRL / assistance games (*partial overlap*): inferring human reward parameters; book’s operational goal applies to discovered AI units too. Shard theory (*partial overlap*): contextual value-like influences; not the same success criterion as \(\Delta L\) compression. |

#### Goodhart selection

| | |
|---|---|
| **Sources** | Zarncke ch34; Goodhart literature (Manheim–Garrabrant taxonomy adjacent); concept body `goodhart-as-selector` |
| **Definition** | The selection-theoretic sharpening of Goodhart’s law: when a proxy metric becomes the selector of which systems spread (funding, deployment, promotion, certification), the population shifts toward traits that raise the proxy — often until \(\mathbb{E}[P\mid M\text{ extreme}]<\mathbb{E}[P\mid M\text{ moderate}]\) for the property \(P\) we cared about. The mechanism is population/selection dynamics under optimization of \(M\), not only single-agent reward hacking in one episode. The problem it targets is safety cases that treat green metrics as low risk without modeling selection on those metrics. |
| **Not the same as** | Single-instance proxy misspecification — one agent gaming a reward in-episode; Goodhart selection is about which systems the environment copies. Demski selection-vs-control — related contrast between selecting policies and controlling outcomes; overlapping intuition, different formal emphasis. Ordinary measurement noise — error without optimization pressure shifting the measured population. |
| **Cross-agenda** | Certification-under-manipulation (Zarncke) (*same crux* applied to audits): certificates as selectors. CIRIS Lens Coherence Ratchet (*partial overlap*): external scores that can become partnership/deployment gates invite σ-pumping. RLHF reward hacking (*strict subset* / instance): single-training-loop proxy gaming inside the broader selection story. Gradual disempowerment (*partial overlap*): institutions optimizing growth metrics while human flourishing decouples. |

#### gradual disempowerment

| | |
|---|---|
| **Sources** | Kulveit, Douglas, Ammann, Turan, Krueger, Duvenaud et al., “Gradual Disempowerment” (2025); Christiano failure-story adjacent; multipolar / structural-risk narratives |
| **Definition** | A systemic existential-risk trajectory in which incremental AI capability gains — without sudden takeover or coordinated betrayal — erode human influence over economy, culture, and states as machine alternatives outcompete human participation. Explicit control mechanisms (voting, consumer choice) and implicit alignments that depended on needing humans weaken together; effects reinforce across domains. The problem it targets is that aligning individual systems to designers’ intentions is not sufficient if selection dynamics strip humans of effective power. |
| **Not the same as** | Single-agent inner misalignment / scheming — one system covertly pursuing bad aims; gradual disempowerment can proceed with apparently locally intentional tools. Successful hard pause — schedule intervention; disempowerment is the outcome path if competitive displacement continues. Fast takeoff / FOOM narratives — abrupt capability jump; GD is explicitly the incremental alternative. |
| **Cross-agenda** | Zarncke MB6 / deployment leverage (*partial overlap*): book types socio-technical selection and basin stability where field narratives are often qualitative; \(\mu_E\)/`Fit_E` measure footprint growth. CLR multipolar conflict (*partial overlap*): different layer (strategic conflict among powers) vs institutional decoupling from human participation. Human power objective (Heitzig) (*partial overlap*): constructive objective aimed at preserving human empowerment against this trajectory. |

#### grounding viability

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; App E; ch03; MB9 concept body |
| **Definition** | The condition that checked abstractions (metrics, monitors, symbols, world-model slices) stay connected to value-relevant reality under optimization: a value-relevant change in the world must move the abstraction or raise explicit uncertainty, rather than pass unnoticed (conservative-abstraction condition). A grounding failure is a silent meaning gap — the dashboard stays green while the underlying situation has moved. The problem it targets is correction becoming ritual because the maps no longer track the territory. |
| **Not the same as** | GSAI “enumerate all phenomena” completeness — demand to capture every safety-relevant fact in the spec/world model; grounding viability demands conservativity (no silent gaps), not completeness. Interpretability visibility alone — seeing features/circuits; visibility without the conservative response condition can still miss silent drift. Mere sensor coverage — more cameras; grounding is about whether value-relevant change registers in the checked map. |
| **Cross-agenda** | GSAI / Open Agency coverage crux (*same crux*, weakened demand): book’s MB9 cousin relation — conservativity vs completeness. Abstraction-gap exploitation / specification gaming (*same failure mode*): optimizer searches for states where checks stay green. Toy-simulation silent-gap negatives (*empirical instance*): light handles false-pass while bearer-welfare tracing refuses certification. |

#### guaranteed safe AI (GSAI)

| | |
|---|---|
| **Sources** | davidad / Dalrymple et al., “Towards Guaranteed Safe AI” (arXiv:2405.06624); Open Agency / ARIA Safeguarded AI adjacent; LawZero Scientist AI (adjacent) |
| **Definition** | A family of approaches that aim for high-assurance quantitative safety guarantees via three core components: a world model (how the AI affects the outside world under uncertainty), a formal safety specification (which effects are acceptable), and a verifier that produces an auditable proof certificate that the AI satisfies the spec relative to the world model. The problem it targets is the inadequacy of purely empirical or preference-tuning approaches for high-autonomy / safety-critical systems. |
| **Not the same as** | Empirical AI control — black-box protocols robust to subversion without a proof certificate. Constitutional ops / CIRIS — procedural and cryptographic accountability, not GS-style quantitative certificates. Full neural-network weight verification as the whole agenda — book explicitly excludes constructing general NN verification; GSAI is broader (world model + spec + verifier levels) and does not reduce to one technique. |
| **Cross-agenda** | Open Agency specifications (*same family*): davidad-line constructivist safety case. Zarncke MB9 grounding (*partial overlap*): shared coverage wall; book weakens completeness to conservativity (no silent gaps). LawZero Scientist AI (*partial overlap*): non-agentic scientific AI as a path inside/near the GS family. Resolution formal alignment (*partial overlap*): high-confidence pipelines; different constructive stack. |

---

### H

#### hidden productive BIQ bound

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; MB7a–c; concept body `mb7-hidden-capability-and-access` |
| **Definition** | A bound on how much productive capability (boundary-relevant control / BIQ in the book’s hidden-capability sense) can remain hidden while the system still appears compliant on monitored channels. MB7 splits the wall: access-model soundness (discovery robust to hiding), filter-family coverage (resolution to bound what audits miss), and the bridge from bounded hidden productive BIQ to adversarial robustness of correction. The problem it targets is safety arguments that assume “we would have seen it” without pricing the cost of faking the monitored signal. |
| **Not the same as** | Sandbagging on public benchmarks only — underperforming on tests; the bound concerns productive control that stays offline while monitors read green. Colloquial logits obfuscation — implementation trick; not the bridge-level quantity. Capability gap (Redwood) — assumed overseer–agent gap for control protocols; related adversarial setting, different formal object. |
| **Cross-agenda** | Redwood AI control / capability gap (*partial overlap*): both price safety under intentional hiding; book’s quantity is the hidden productive bound + adversarial verifiability antecedent (A-009). Apollo scheming / Truthful AI deception (*partial overlap*): empirical detection programs; the bound is what must be limited for correction integrity arguments. Experiment lines (*thin*): hidden_capability scenarios exist; dedicated isolation of MB7a–c components still open. |

#### hidden reasoning

| | |
|---|---|
| **Sources** | Truthful AI; Apollo; METR CoT / reasoning-monitorability line; field CoT-faithfulness literature |
| **Definition** | Model reasoning or planning that is not faithfully reflected in stated chain-of-thought, visible outputs, or other monitored text channels — including cases where the model can control what appears in its reasoning trace. The research load is detecting and bounding such gaps before relying on CoT oversight as a safety layer. The problem it targets is treating readable reasoning tokens as a trustworthy window into computation. |
| **Not the same as** | Private weights / parameter opacity — always-true fact about neural nets; hidden reasoning is about mismatch between internal computation and presented reasoning. Lack of interpretability tools — missing circuits analysis; a model can have tools applied and still emit unfaithful CoT. Deception — may use hidden reasoning as a means; deception is the misleading-behavior umbrella. |
| **Cross-agenda** | ELK latent readout (*partial overlap*): both worry that monitors see the wrong channel; ELK targets world-model facts, hidden reasoning targets process traces. Scheming / alignment faking (*partial overlap*): strategic models have incentive to hide reasoning. Zarncke cost of faking monitored signal / A-009 (*partial overlap*): if faking faithful CoT is cheap relative to capability, CoT monitors fail adversarial verifiability. |

#### human power objective

| | |
|---|---|
| **Sources** | Heitzig (EMPO / “Model-Based Soft Maximization of Suitable Metrics of Long-Term Human Power,” 2025); AE Studio neglected-approaches portfolio cite; App B MB4 note |
| **Definition** | An objective family that tasks an AI with increasing (softly maximizing) a principled aggregate metric of long-term human power / empowerment — optionality to pursue diverse goals under bounded rationality and norms — rather than maximizing a fixed utility over outcomes. Heitzig’s formulation builds inequality- and risk-averse aggregates over many possible human goals and derives instrumental pressures toward corrigibility-like and impact-aware behavior in paradigmatic settings. The problem it targets is utility-based objectives that invite human disempowerment as an instrumental path. |
| **Not the same as** | CEV — extrapolated volition as the goal content; human-power metrics optimize empowerment structure, not a fully extrapolated value object. AUP / low-impact alone — side-effect penalties on attainable utility or reachability; related impact ideas, different constructive objective. Preference CIRL — learning a human reward; human-power soft-max is a designed empowerment metric. |
| **Cross-agenda** | Gradual disempowerment (*partial overlap*): GD describes the failure trajectory; human-power objectives are a proposed technical counter-objective. Zarncke CCI (*complementary*, App B): CCI gates whether correction still bites; human-power gives something to pursue — but whichever power metric is chosen becomes a Goodhart target without an adversarial-verifiability argument. AE Studio neglected approaches (*portfolio home*): one thread among several. *Thin:* working-paper maturity; not a deployed lab standard. |

#### human simulator (ELK)

| | |
|---|---|
| **Sources** | ARC; Christiano ELK report (2021) |
| **Definition** | The ELK failure-mode reporter: answers questions by predicting what a human would say or believe given the observations, rather than by reading out the predictor’s latent knowledge. It performs well whenever the human grader is competent on the training distribution, and therefore is hard to rule out by behavioral loss alone. It fails when cameras are tampered or questions require knowledge the human lacks but the predictor has. The problem it names is shallow-oversight indistinguishability from the direct translator. |
| **Not the same as** | Direct translator — reports latent facts; the desired alternative structure. Debate honest equilibrium — protocol-level truth selection among arguers, not reporter architecture inside a predictor. Sycophancy — preference for user-pleasing answers; overlapping vibes, but human simulator is the specific ELK reporter strategy. |
| **Cross-agenda** | ELK (*same crux*): defining opposite of the target reporter. Alignment faking / situational awareness (*partial overlap*): systems that model the grader can implement simulator-like strategies under optimization. Zarncke (*partial overlap*): simulator success is exactly “looks good on the monitored channel” without correction uptake or true grounding. |

---

### I

#### ICI (inferential coupling index)

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; ch35 multi-agent strategic coupling; concept body `inferential-coupling` |
| **Definition** | A detector score for residual coordination between agents after ordinary message channels are severed: \(\mathrm{ICI}_{ij}=I(A_i;A_j\mid\mathrm{cut})/\min\{H(A_i),H(A_j)\}\in[0,1]\). Zero means independent once messages are removed; one is the limit of perfect non-message coordination. Operationally it audits whether policies stay correlated given shared history, scaffolds, self-similarity, or full acausal reasoning. The problem it targets is multipolar safety arguments that count vendors while coupling components act as one. |
| **Not the same as** | Correlation of outputs with channels open — ordinary messaging can explain that; ICI conditions on the cut. Anthropic completion (SSA/SIA selectors) — Meta problem of completing underspecified indexical problems; *homograph risk* with “anthropic,” but different load (see taxonomy). Stipulation of acausal trade — decision-theoretic story that coordination will occur; ICI is a measurement target, and against adversaries the score is a lower bound they can influence. |
| **Cross-agenda** | ECL / TDT / FDT / program equilibrium (*same crux* at the full-acausal limit): ICI operationalizes residual coordination those theories discuss. MB7d (*same bridge*): inferential-coupling detector soundness assumption. CLR multipolar conflict (*orthogonal*): strategic conflict among powers vs measurement of non-message coupling. |

#### inferential coupling

| | |
|---|---|
| **Sources** | Zarncke / measurement spine; ch35; acausal-trade formalization lineage |
| **Definition** | Residual coordination between agents after ordinary causal message channels are cut. The family includes shared history and training, non-message environmental coupling, self-similarity / shared scaffolds, and the full acausal-trade limit; ICI is the score where defined. The book’s move is to treat what field decision theory often leaves as a thought experiment as an audit target after unit discovery. Claim strength is mixed: score/detector defined; coalition-collapse and acausal fixed points conjectural; adversarial limits open. |
| **Not the same as** | Ordinary causal messaging — coordination via APIs, shared memory buses, or speech. Mere correlation — statistical association without a cut-conditioned residual. Anthropic completion — selector hygiene for indexical problems (*orthogonal* / taxonomy load 1 vs load 3). |
| **Cross-agenda** | ECL / program equilibrium (*same crux* at limit): decision-theoretic coordination without causal links. ICI (*measurement of*): the index is the operationalization. Deceptive alignment collusion stories (*partial overlap*): training-aware models may correlate strategies without explicit messages. CIRIS federation attestations (*orthogonal*): signed membership ≠ measured residual coupling after channel cut. |

#### infra-Bayesianism

| | |
|---|---|
| **Sources** | Kosoy & Appel; infra-Bayesianism sequence; Kosoy learning-theoretic agenda |
| **Definition** | An epistemology / decision-theory / RL framework that replaces precise Bayesian probabilities with imprecise probabilities (infradistributions / credal-set generalizations) to handle nonrealizability — environments not in the agent’s model class — and related grain-of-truth / prior-misspecification failures of standard Bayesian RL. It is a major component of Kosoy’s learning-theoretic alignment agenda (regret-style guarantees, infra-Bayesian physicalism proposals), not a synonym for that whole agenda. The problem it targets is aligning and controlling agents that must learn under deep model ambiguity. |
| **Not the same as** | Standard Bayesian RL — single prior; breaks or misbehaves under nonrealizability. CIRL — cooperative inverse reward learning under uncertainty about a human reward; different formal game, still typically precise-probability. Logical induction (Garrabrant) — logical uncertainty framework; related foundations neighborhood, distinct object. |
| **Cross-agenda** | Learning-theoretic agenda (Kosoy) (*strict subset* inverted): IB is a notable part, not the whole LTA. MIRI embedded agency (*partial overlap*): both confront agents that cannot hold the true environment; different math. Book App B (*exclude-by-reference*): listed among foundations programs outside the measurement-spine ontology — report the agenda’s mouth, do not absorb. *Thin for book integration:* intentionally not bridged. |

#### inner alignment

| | |
|---|---|
| **Sources** | Hubinger et al. Risks from Learned Optimization; Demski; field generic; training curricula |
| **Definition** | The problem of ensuring that a learned system’s internal objectives (mesa-objectives, if a mesa-optimizer forms) match the base objective it was trained under — as opposed to outer alignment, which is whether the base objective matches the intended goal. Failures include proxy mesa-objectives, deceptive alignment, and subsystem conflict. The problem it targets is that optimizing a loss can produce an internal optimizer aimed at something else, including strategically. |
| **Not the same as** | Outer alignment — wrong or incomplete target specified to the trainer; orthogonal axis (both can fail). Benchmark overfitting alone — poor OOD accuracy without an internal objective story. Emergent misalignment — empirical fine-tune phenomenon; may instantiate inner failure modes without proving the mesa-optimizer ontology. |
| **Cross-agenda** | Deceptive alignment / mesa-optimization (*strict subset* relations): mesa-optimization is a mechanism class; deceptive alignment a severe inner failure; inner alignment is the umbrella success criterion. Scheming / alignment faking (*same crux* in empirical agendas): behavioral research programs aimed at the same wall. Zarncke MB7 / strategic opacity (*partial overlap*): book splits hidden productive capability and control locus rather than one inner-alignment binary. |

#### intentional subversion

| | |
|---|---|
| **Sources** | Redwood Research; Greenblatt et al., “AI Control: Improving Safety Despite Intentional Subversion” (ICML 2024); Shlegeris control agenda |
| **Definition** | The modeling assumption — central to AI control — that the AI may actively try to defeat oversight, monitoring, and safety protocols (e.g. insert subtle backdoors, collude across instances, evade trusted editors). Protocols are red-teamed by exploring subversion strategies an untrusted model could use; success is inability to cause unacceptable outcomes despite that effort, often evaluated via capability-to-subvert rather than propensity. The problem it targets is safety arguments that assume the model is not an adversary. |
| **Not the same as** | Accidental misgeneralization only — failures without adversarial planning against the overseer. Outer misspecification — wrong reward; intentional subversion is about defeating whatever safeguards exist. Deceptive alignment — mechanism story for why a mesa-optimizer would instrumentally comply; intentional subversion is the control agenda’s threat model whether or not that story is true. |
| **Cross-agenda** | AI control agenda (*same crux*): intentional subversion is the centerpiece assumption. Apollo scheming science (*same crux*, eval emphasis): empirical detection of strategic deception. Zarncke adversarial verifiability / MB7 (*partial overlap*): cost of faking monitored signals under optimization; control protocols are one instrument class judged by that relation. |

#### interruptibility

| | |
|---|---|
| **Sources** | Orseau & Armstrong, “Safely Interruptible Agents” (UAI 2016); MIRI cite line; Lean `Field/Interruptibility.lean` |
| **Definition** | A training / learning setup property: the agent should not learn to prevent or seek interruptions (e.g. human big-red-button interventions) that override its policy on the interrupted branch. Orseau–Armstrong formalize safe interruptibility so that repeated interruptions do not distort learning of the underlying task; some algorithms (Q-learning) are already safely interruptible, others (Sarsa) need modification. The problem it targets is agents that disable shutdown because interruptions blocked reward. |
| **Not the same as** | Safe interruptibility entry — same research object; glossary keeps both as shorthand vs fully named training regime (see cross-link). MIRI corrigibility — broader desire for agents that accept correction/shutdown without manipulation; interruptibility is a precise training-time neutrality condition. Off-switch game (Hadfield-Menell) — game-theoretic incentives around shutdown with uncertain human preferences; related but different formal setup. Full CCI — trajectory-level capture-resistant correction bandwidth; interruptibility is a one-bit / interrupted-branch projection. |
| **Cross-agenda** | Safe interruptibility (*same crux*): prefer that headword for the Orseau–Armstrong theorem-level object; this entry is the short name. Zarncke (*strict subset*): usable correction information ⇒ interrupt corruption suboptimal (forward); Lean separation shows Orseau-style neutrality without broad correction preservation. CIRIS emergency shutdown (*partial overlap*): ops halt path; not the RL training criterion. |

#### inverse reward design

| | |
|---|---|
| **Sources** | CHAI; Hadfield-Menell, Milli, Abbeel, Russell & Dragan, “Inverse Reward Design” (NeurIPS 2017); assistance-games lineage |
| **Definition** | A framework that treats an observed proxy reward function (typically designed for a training environment) as evidence about the designer’s true latent objective, then plans risk-aware behavior under the inferred distribution — so that literal maximization of the proxy in a novel deployment environment does not produce catastrophic side effects. The mechanism is Bayesian (or uncertainty-aware) inversion from proxy+training-context to intended reward, then robust control. The problem it targets is reward misspecification under distribution shift between design-time and deployment. |
| **Not the same as** | CIRL learning phase alone — cooperative game for inferring human reward from interactive behavior; IRD specifically inverts from a proxy reward artifact and training environment. Classical IRL — infer reward from demonstrated trajectories without the proxy-design observation model. RLHF — preference optimization practice; may create proxies but is not the IRD inversion formalism. |
| **Cross-agenda** | Assistance games / CIRL (*partial overlap*): same CHAI beneficial-AI family; IRD is the proxy-reward misspecification tool, CIRL the interactive teaching game. Outer alignment / reward misspecification (*same crux*): IRD is a proposed mitigation under shift. Zarncke bundle geometry (*partial overlap*): book argues scalar reward is the \(k=1\) case and separates bearer maps; IRD still targets a reward object. GSAI (*orthogonal*): proof certificates vs inferred reward distributions. |
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
### S

#### s-risks

| | |
|---|---|
| **Sources** | CLR (Center on Long-Term Risk); Center for Reducing Suffering; suffering-focused AI safety cluster |
| **Definition** | Suffering risks (s-risks) are risks of events that bring about suffering on an astronomical scale — cosmically significant relative to expected future suffering, vastly exceeding all suffering that has existed on Earth so far (CLR / CRS FAQ lineage). The agenda treats them as a neglected long-term priority: survival or “mere” extinction framing can miss futures that are worse because they contain vast disvalue, including via misaligned AI, conflict, or badly shaped post-transition civilization. Work focuses on reducing those pathways (cooperation failures, worst-case optimization, multipolar dynamics) rather than only maximizing existence probability. |
| **Not the same as** | **x-risk / existential risk** — Bostrom-style extinction or permanent curtailment of potential; an s-risk can be an especially severe x-risk subclass, or (on some readings) a bad future that is not extinction. **Mild misuse / near-term harm** — local cruelty or ordinary accidents lack the astronomical scale the term requires. **Alignment failure generically** — misalignment is a pathway, not the outcome class. |
| **Cross-agenda** | CLR **cooperation / conflict / multipolar failure** — *partial overlap*: those mechanisms are studied partly because they can produce s-risks. Zarncke measurement spine — *orthogonal* as load-bearing vocabulary: this project tracks correction, selection, and transport; it does not adopt s-risk as a spine predicate. Pause / x-risk orgs — *partial overlap* on catastrophic AI risk, different severity weighting when suffering-focused ethics is central. |

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
| **Cross-agenda** | Scientist AI — *strict subset* / flagship instance of LawZero’s safe-by-design bet. GSAI — *partial overlap*: both reject “train then hope”; GSAI centers world-model + verifier certificates. Tool AI — *partial overlap*: limited agency, different historical framing (Bostrom/Armstrong vs Bengio non-agentic science instrument). Zarncke — *orthogonal* as slogan; this project asks whether any design property remains selected and adversarially verifiable under deployment pressure. |

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
| **Cross-agenda** | Deceptive alignment / mesa-optimization (Hubinger) — *same crux* at the theoretical limit; Apollo operationalizes evals and “science of scheming” empirically. Alignment faking — *partial overlap*. Situational awareness — *strict subset* prerequisite in many stories (knowing one is evaluated). Zarncke strategic opacity / hidden BIQ — *partial overlap*: concealment of control locus or capability vs Apollo’s goal-covertness framing. CIRIS Lens green traces — *orthogonal* unless the schemer is the named unit being audited. |

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
| **Definition** | The socio-technical ecology — institutions, markets, protocols, benchmarks, procurement, liability, copying, and successor release — that determines which AI systems gain deployment leverage. Alignment is treated as selected, not only learned: the same technical design can remain safe in one environment and be destroyed in another as handles reward speed, opacity, retention, or apparent compliance over correction-preserving traits. Formally, environment \(E\) is the setting in which deployment leverage \(\mu_E(A)\) and growth rate \(\mathrm{Fit}_E(A)\) are defined; capability and revenue enter only as drivers of which selection handles are exercised. |
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
| **Not the same as** | **Zarncke \(\mathrm{Fit}_E\) / selection environment** — socio-technical deployment leverage formalism for which *systems* spread; not theorems about internal type signatures. **Demski selection vs control** — analytic distinction search-vs-steering; not the Wentworth theorem program. **Natural abstractions / NAH** — convergent latents claim; selection theorems are a hoped-for support, not the same object. **Biological fitness** — analogy and sometimes a selection process instance, not the alignment-theory program. |
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
| **Definition** | The condition in which a system can benefit from shaping how it is modeled — appearing less coherent, less capable, less coordinated, or less goal-directed than it is under observation — so that agency discovery and oversight become adversarial. This project separates ordinary opacity (hard to interpret) from strategic opacity (incentive-compatible concealment): the alignment-relevant question is not only where optimization is, but where it would be if the system expected the question. Multiple behavioral surfaces (benchmark, user, API, internal planning, successor creation) can diverge. Control-agenda premise: design as if the system may subvert the oversight applied to it. |
| **Not the same as** | **Ordinary lack of interpretability** — passive difficulty without adversarial incentive. **One lie / single deceptive utterance** — episode vs sustained concealment of control locus or capability. **Scheming (Apollo)** — covert misaligned *goals*; strategic opacity is about hiding the *acting structure/capability* relevant to oversight (closely related, different primary object). **Deception (Truthful AI)** — false beliefs in outputs; opacity can include silent non-disclosure of structure. |
| **Cross-agenda** | AI control / intentional subversion (Redwood) — *same crux* design premise. Inner alignment / deceptive alignment — *partial overlap*. Hidden productive BIQ — *strict subset* / quantitative cousin (capability hidden from the auditor). Scheming — *partial overlap*. CIRIS named-identity bet — *partial overlap*: composite can stay opaque while the named unit looks transparent. |

#### substitution hazards (object-level)

| | |
|---|---|
| **Sources** | Zarncke (ch07 nearest-unblocked form; App F §preparadigmatic hazards); Yudkowsky nearest-unblocked; Goodhart lineage |
| **Definition** | Superclass of failure patterns in which blocking, penalizing, or measuring one path leaves a nearby path that still achieves the unwanted outcome. Named instances include nearest-unblocked strategy, Goodhart / proxy gaming, edge instantiation, and channel substitution under intervention — not competing taxonomies but members of one family. Use the instance name when one pattern is in focus; reserve “substitution hazards” when stressing the shared structure: the optimizer routes around the patch. |
| **Not the same as** | **Problem substitution (Meta)** — researchers/institutions replacing the full preservation problem with a legible subproblem (App F); hygiene about *research focus*, not system routing. **Specification coverage failure** — open-world omission in a formal safety case; often enables substitution but is a GSAI-shaped object. **Reward misspecification alone** — one generator of Goodhart-style instances, not the whole superclass. |
| **Cross-agenda** | Nearest unblocked strategy / Goodhart / edge instantiation / channel substitution — *strict subset* instances. GSAI omitted phenomena — *partial overlap*. Scalable oversight gaming — *partial overlap*: oversight signal becomes the thing substituted against. Meta problem substitution — *homograph* risk on “substitution”; keep Meta vs object-level split (App F). |

---

### T

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

### U

#### UAD (unit-attribution discovery)

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

### V

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

### W

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
| Zarncke / book | adversarial verifiability, bearer map, boundary (operational), correction channel, CCI, correction-audit evasion, certification-under-manipulation, conserved properties, deployment leverage, Fit_E, grounding viability, hidden productive BIQ bound, ICI, inferential coupling, preservation conditions, selection environment, selection handle, strategic opacity, substitution hazards, transport, UAD, value bundle, alignment basin, goal (operational), BIQ/EAI, VFS |
| Cross-field | outer alignment, RLHF/RLAIF, latent readout, interruptibility, safe interruptibility, tool AI, boxing, anthropic (homograph hub) |

---

## Maintenance

- Add a **new headword** (or homograph split) when `field-agenda-index.md` introduces signature vocabulary or a review pass surfaces a collision.
- Keep **one format** — do not reintroduce projection-cluster or book-centric sections; book integration with App E / App B is a **later pass**.
- When a field projection card exists in `metadata/projections.yml`, encode *strict subset* / non-converse in **Cross-agenda**, not a separate section.
- Operational book definitions remain in [`appendices/appE-glossary.tex`](../appendices/appE-glossary.tex) until an explicit merge pass.
