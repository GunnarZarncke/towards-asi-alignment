# What Does Alignment Secure?

## A Typed Crosswalk of Objects, Guarantees, and Warrants

### Abstract

Alignment proposals are often compared as if they supplied rival objective functions. This flattens distinctions among what is valued, what is forbidden, what is claimed to persist, and what evidence would warrant deployment. We provide a typed comparative crosswalk with three main coordinates: the object aligned, valued, or secured; the assessment or guarantee applied to it; and the warrant and quantifiers under which the claim is accepted. The crosswalk places outcome utility, transition and history value, policy-level response, option preservation, human power, corrigibility, viability, socio-technical selection, formal proof, adversarial oversight, AI Control, and safety cases without treating them as peers at one logical level. A matched-endpoint case, in which a judge reaches the same verdict by learning or by rewiring, exposes non-implications among these frames and the representational assumptions each needs. We then give a composition discipline based on constraints, ordered objectives, dynamical closure, and explicit assurance. Towards Superintelligence Alignment (TSA) serves as one running example: continued legitimate correction possibility is the relational object; viability is the shape of the conditional dynamical guarantee. This is not presented as a proof of alignment or as a replacement for substantive accounts of value, welfare, rights, or legitimacy. The contribution is a comparative crosswalk and a separation and composition discipline, not the first alignment taxonomy, a unified theory, or a solution to alignment.

## Epistemic and novelty statement

Epistemic status: confident that object, assessment, and warrant need to be separated; less confident that the present inventory covers every useful frame or uses the final best names.

The literature search behind this draft was selective rather than systematic. It covered the cited primary works, recent alignment taxonomies and surveys, their relevant reference trails, TSA's manuscript and Lean spine, and one unpublished draft through 22 October 2026. Non-English work, inaccessible books, unindexed manuscripts, and private 2026 work may contain closer precedents.

The paper does not claim:

- the first multidimensional taxonomy of alignment;
- the first distinction between outcomes and execution;
- the first process-sensitive or transition-sensitive value model;
- the first connection between power, corrigibility, and option preservation;
- the first use of viability or basins in alignment;
- a theorem showing that the proposed composition works;
- or a proof that TSA, Lean, or any safety case establishes ASI alignment.

Prior work separately classifies normative content, aim, constituency, system locus, outcome versus execution, lifecycle stage, failure mechanism, and value-alignment subproblems. The narrower contribution here is to type proposals by **object**, **assessment or guarantee**, and **warrant with quantifiers**, then compare them on one matched-endpoint causal case. This yields explicit non-implications and interface obligations. The priority judgment is provisional.

## 1. Introduction

What does it mean to compare RLHF, corrigibility, viable control, AI Control, and a safety case?

Taken literally, the question is malformed. RLHF is usually a training method. Corrigibility is a family of agent or relationship properties. Viability is a dynamical existence or invariance claim over a supplied set. AI Control is a protocol family for deployment under intentional-subversion assumptions. A safety case is an assurance structure. They may interact, but they are not answers to the same typed question.

The same error appears in more formal comparisons. A state utility, a transition reward, a human-power metric, an attainable-option penalty, a correction channel, and a viable kernel can all guide decisions. It does not follow that they are alternative scalar objectives. They attach value or protection to different objects and make different claims about time, uncertainty, authority, and evidence.

Three questions recover the missing structure.

1. **What is the object?** Is it an outcome, transition, history, policy, distribution, option set, human capability, update procedure, correction relation, constraint set, or coupled deployment process?
2. **How is it assessed or secured?** Is it maximized, ordered, thresholded, prohibited, kept viable, made robust, required at equilibrium, or accepted through a legitimate procedure?
3. **Under which quantifiers and warrant?** Does the claim hold in expectation, with high probability, for every allowed disturbance, for some controller, through successors, in equilibrium, by proof, by monitoring, or only under an empirical protocol?

These questions do not produce a neutral answer to alignment. They make disagreements easier to locate. A dispute can concern the object, the bearer, the aggregation rule, the dynamics, the quantifier, or the evidence. Without these fields, the disagreement is compressed into one overloaded word.

This paper develops a typed crosswalk. It then uses one case throughout: an evaluator reaches the same later judgment by learning or by being rewired. The final state is held fixed. The route, retained capability, authority relation, and future correction structure vary. The case is deliberately small. Its purpose is to show which frames distinguish the routes, which remain indifferent, and which distinguish them only after the model is expanded.

TSA is used as one running example, not as assumed canon. Its intended 2.0 choice is:

> Continued legitimate correction possibility is the relational object; viability is the shape of the conditional dynamical guarantee.

That sentence leaves substantial work open. It does not identify the legitimate corrector by itself. It does not determine which outcomes are good. It does not establish that correction remains measurable under optimization pressure. It does not show that a deployed system belongs to a safe class. Neighboring frames can supply substantive value, rights, capability, route, and assurance conditions that a correction-centered account lacks.

The central claim is modest. Alignment work becomes more comparable when target, constraint, guarantee, and protocol are separately typed. The resulting composition is not a flat sum. It is a set of interface obligations whose ordering carries normative content.

## 2. Related taxonomies

The crosswalk cuts across existing taxonomies rather than replacing them.

### 2.1 Normative content and source

Gabriel distinguishes alignment with instructions, expressed intentions, revealed preferences, informed preferences, interests or well-being, and values. He also separates minimalist from maximalist alignment and technical from normative questions [Gabriel 2020]. This is a map of normative content and source. It does not by itself determine whether that content evaluates outcomes, routes, policies, capabilities, or correction relations.

Zhi-Xuan, Carroll, Franklin, and Ashton challenge preferentism in AI alignment. They argue that preference representations can omit thick normative content and that expected utility does not settle which preferences are acceptable. Their alternative emphasizes role-specific normative standards negotiated by relevant stakeholders [Zhi-Xuan et al. 2025]. This directly pressures preference-maximizing targets and supports role and procedure constraints. It still leaves open whether a standard is implemented as a hard rule, pairwise order, threshold, or scalar.

The attribution matters. *Beyond Preferences in AI Alignment* is by Tan Zhi-Xuan, Micah Carroll, Matija Franklin, and Hal Ashton, not by Atoosa Kasirzadeh. Its verified journal DOI is [10.1007/s11098-024-02249-w](https://doi.org/10.1007/s11098-024-02249-w).

### 2.2 Aim, scope, constituency, and alignment ideal

Baum separates alignment aim, scope, constituency, and degree. The outcome-versus-execution scope is a direct precedent for distinguishing a good result from an acceptable way of producing it [Baum 2025]. The present crosswalk narrows that distinction further. Transition value, trajectory value, deontic route constraints, and procedural legitimacy are not assumed to be one "process" frame.

Jha, Švarc, and Bagiński ask what object is aligned and which target properties it should satisfy, then distinguish Task Reliability, Social Judiciousness, and Takeover Avoidance [Jha, Švarc, and Bagiński 2026]. Their paper is the closest structural neighbor. Their object axis concerns model behavior, socio-technical deployment, and optimization targets. Our object field instead asks what receives value or security inside or across those loci, such as an outcome, option set, human capability, or correction relation.

Harris and colleagues divide value alignment into problems including value identification, prioritization, imperfect specification, anthropocentrism, moral imperfection, inverse alignment, and provability [Harris et al. 2026]. This is a problem and dependency map. It shows why a value target cannot be treated as solved once one reward function is inferred.

### 2.3 Construction, lifecycle, and engineering phase

Hubinger compares proposals by outer alignment, inner alignment, training competitiveness, and performance competitiveness [Hubinger 2020]. Krakovna distinguishes alignment components from enablers and uses ideal, design, and revealed specifications to locate outer and inner alignment failures [Krakovna 2022]. Ji and colleagues organize a broad survey around robustness, interpretability, controllability, and ethicality, then distinguish forward alignment from backward assurance and governance [Ji et al. 2025].

These maps answer where a proposal acts in construction or evaluation. They are orthogonal to the present question. An outer-alignment target can value states, transitions, human capability, or correction. A verifier can check any of those only if they are represented.

Amodei and colleagues classify five concrete accident problems: negative side effects, reward hacking, scalable supervision, safe exploration, and robustness to distributional shift [Amodei et al. 2016]. This map remains important because it organizes failure mechanisms and engineering problems. The same mechanism can defeat several target objects, so it is not an object–assessment taxonomy.

Terry and colleagues use specification alignment, process alignment, and evaluation alignment for interactive AI systems [Terry et al. 2023]. "Process alignment" is therefore collision-prone. Process reward models create a second collision because they may score intermediate reasoning only to improve final-answer accuracy. We use **transition-valued**, **trajectory-valued**, or **route-sensitive** when the route is itself the valued object.

### 2.4 Neighboring substantive distinctions

Turner's non-obstruction analysis separates impact alignment, intent alignment, corrigibility, and preservation of human attainable utility [Turner 2020]. It is especially important because it gives direct non-implications: an AI can empower a human without permitting policy modification, while a corrigible AI can cause harm until it is corrected.

Soares and colleagues describe corrigibility through desiderata concerning shutdown, modification, manipulation of programmers, safety measures, self-modification, and successors [Soares et al. 2015]. Christiano broadens corrigibility toward helping an overseer remain informed, detect mistakes, retain control, and create benign successors, and suggests an informal broad-basin view [Christiano 2018]. These are direct predecessors of any correction-centered account.

Viability theory predates these alignment debates. It distinguishes states from which at least one admissible continuation remains in a constraint set from stronger invariance notions [Aubin 1990; Aubin, Bayen, and Saint-Pierre 2011]. It supplies a guarantee geometry, not the normative content of the set.

The result is not an empty niche in which no one has classified alignment. The result is a set of existing cuts that can be made jointly type-correct.

## 3. A typed schema

Let a model \(M\), policy or joint process \(\pi\), and uncertainty source \(\omega\) induce an object

\[
X(M,\pi,\omega)\in\mathcal X.
\]

A target may supply an ordering \(\succeq\) on \(\mathcal X\), an acceptance set \(A\subseteq\mathcal X\), or a property \(\varphi(X)\). It remains incomplete until its bearers, temporal rule, uncertainty semantics, and quantifiers are fixed.

We use:

\[
\texttt{Frame} =
(B,\ P,\ H,\ \mathcal X,\ R,\ T,\ Q,\ S,\ W).
\]

- \(B\): system boundary.
- \(P\): authorized principals.
- \(H\): affected bearers or constituencies.
- \(\mathcal X\): object domain.
- \(R\): ordering, predicate, constraint, or strategic relation.
- \(T\): temporal and uncertainty rule.
- \(Q\): quantifiers over people, models, disturbances, adversaries, and successors.
- \(S\): solution concept.
- \(W\): warrant or evidence protocol.

The schema is a comparison device, not a claim that every field is independent. A risk functional needs a distribution. Viability needs dynamics and a set. Correction needs a corrector, authority, and handles. Approval needs an evaluator and information state. Some combinations are ill-typed.

### 3.1 Four logical roles

We classify each component by role.

- A **target** ranks or selects desired possibilities.
- A **constraint** excludes possibilities or imposes a floor.
- A **guarantee** quantifies what holds under named dynamics and assumptions.
- A **protocol** constructs, elicits, tests, monitors, or warrants a claim.

Suppose a constitution prohibits evaluator manipulation, a human-power score ranks admissible policies, a controller keeps their conjunction viable under disturbances, and a proof plus red-team exercise supports deployment. The constitution, objective, viability claim, and evidence protocol work together. None can be substituted for the others by changing the label.

### 3.2 Quantifiers are part of the frame

Compare:

\[
\exists \pi\ \forall t:\ X_t^\pi\in K
\]

with:

\[
\forall d\in D\ \forall t:\ X_t^{\pi,d}\in K.
\]

The first says some admissible policy can remain in \(K\). The second says one chosen policy remains in \(K\) under every allowed disturbance. They support different deployment conclusions.

Similar separations apply to expectation, tail bounds, almost-sure constraints, model uncertainty, and successors. "Remains aligned" is incomplete until the relevant quantifiers are stated.

### 3.3 Warrant is not property

A proof certificate, monitor, audit, or debate result is evidence about a separately defined property. Proof-carrying code makes the split explicit: policy, artifact, proof, and checker are different objects [Necula 1997]. Guaranteed Safe AI similarly separates world model, safety specification, and verifier [Dalrymple et al. 2024].

This distinction blocks two inferences.

1. Formal proof does not choose what should be proved.
2. A passed checker does not establish that the world model contains every safety-relevant phenomenon.

## 4. Frame overview

### 4.1 Outcomes, transitions, histories, and policies

**Outcome or state value.** A function \(U(s)\), welfare score, approval score, or acceptable-state predicate evaluates a snapshot or result. Expected utility adds beliefs and axioms that justify averaging over uncertainty. State value is adequate when the state carries all normatively relevant information. It is not adequate merely because an implementation calls its representation a state.

**Learned reward or preference.** Learning a reward, preference ordering, approval model, or posterior usually changes the representation or construction protocol, not the target object's type. If the learned score ranks outcomes, the object remains outcome-valued; if it ranks acts, it is act-valued. IRL, CIRL, RLHF, RLAIF, and DPO are therefore not target objects without an additional statement of what their learned signal represents.

**Transition or route value.** A reward \(r(s,a,s')\), edge score, or admissible-transition predicate evaluates what was done or how one state became another. Hallgren's private draft makes directed edges primitive and, on its fixed graph with the stated reachability assumption, treats endpoint-only additive path value as the exact-potential special case. This is useful for routes, reversibility, and round trips. It does not derive which transitions are good. Discounted potential-based reward shaping, \(F(s,a,s')=\gamma\Phi(s')-\Phi(s)\), preserves optimal policies under its stated assumptions [Ng, Harada, and Russell 1999]; that invariance is not identity of edge values, trajectory returns, or every bounded-rational learning process. The Hallgren draft is cited only as Jonas Hallgren, *Process Alignment*, v0.7, September 2026, unpublished draft supplied to the author.

The representation claim must be calibrated. A finite history can be added to an augmented state. Automata constructions reduce temporal properties to reachability or invariance on product spaces [Soudjani, Gevaerts, and Abate 2015]. The costs may be loss of compactness, locality, observability, stationarity, or auditability. The issue is not impossibility in principle.

**History value.** A utility or preference over \(h=(s_0,a_0,s_1,\ldots)\) represents delayed and path-dependent value directly. A pathwise safety predicate is different. "This history scores highly" and "this predicate held throughout the history" use the same temporal object with different assessments.

**Policy or act value.** A policy is a contingent mapping, not its realized trace. Corrigibility often lives here. Two systems can produce the same observed behavior but differ in how they would respond to correction, contrary evidence, or an unobserved opportunity to seize power.

### 4.2 Distributions, risk, and partial orders

A distributional object retains uncertainty that a realized outcome or expected value discards. Expected value, CVaR, stochastic dominance, entropic risk, chance constraints, minimax, and regret can rank the same lotteries differently [Bäuerle and Jaśkiewicz 2024].

Distributional RL does not settle the target. Learning the random return \(Z\) leaves open which functional governs action [Bellemare, Dabney, and Munos 2017]. The same applies to multi-objective representations. A vector does not choose its scalarization, Pareto solution, bargaining rule, or lexicographic order [Roijers et al. 2013].

Hard constraints remain distinct from finite penalties unless exact-penalty conditions are established. If a violation is non-compensatory, a sufficiently large but finite reward elsewhere must not purchase it.

### 4.3 Options, empowerment, and human power

These frames share a concern with what remains possible, but their bearers and measures differ.

**Attainable Utility Preservation.** AUP embeds states in a vector of attainable auxiliary values and penalizes changes relative to a baseline while retaining a primary objective [Turner, Hadfield-Menell, and Tadepalli 2020]. The auxiliaries are not intrinsically human-indexed. Preserving their maxima does not guarantee preservation of a particular human option or correction handle.

**Limited optimization and quantilization.** A quantilizer samples from a high-performing quantile of a supplied base distribution instead of choosing the maximum [Taylor 2016]. This is a decision rule, not a substantive value object. Its guarantee is relative to the base distribution, quantile, cost bound, and use pattern; one-shot bounds do not imply safety under repeated deployment, and a human-like base can contain human institutional failures.

**Information-theoretic empowerment.** Klyubin, Polani, and Nehaniv define an agent-relative channel capacity from action sequences to later sensor states [Klyubin, Polani, and Nehaniv 2005]. The result is measured in bits. It does not by itself identify welfare, authority, or legitimacy.

**Human non-obstruction.** Turner compares a human's attainable value with the AI on against leaving it off for every payoff function in a selected set [Turner 2020]. This is human-indexed and pointwise across goals. It still depends on the goal set, baseline, horizon, and human policy model.

**Long-term human power.** Heitzig and Potham's 2025 preprint already proposes a parametrizable inequality-, time-, and risk-sensitive aggregate of modeled human goal-attainment capability, gives computational methods, and analyzes behavioral examples [Heitzig and Potham 2025]. Their distinct 2026 preprint gives a more explicitly desiderata-driven derivation of related functional forms and numbered propositions [Heitzig and Potham 2026].

The two papers should not be conflated, but neither should the aggregate be assigned exclusively to the later paper. TSA currently cites arXiv:2508.00159, *Model-Based Soft Maximization of Suitable Metrics of Long-Term Human Power*. Claims about the 2026 axiomatization and its numbered propositions rely on arXiv:2608.08240, *A Fair Objective for Human-Empowerment-Preserving AI*.

Across the two versions, the proposal can instrumentally favor confirmation, caution about irreversible changes, and forms of corrigibility. The 2025 paper already records adverse possibilities including belief manipulation, self-preservation, and refusal of destruction or pause in some cases. Human power therefore does not automatically imply legitimate correction.

### 4.4 Deliberation, constitution, and normative source

Approval direction specifies an evaluator and an act-level score. Christiano's canonical proposal evaluates a proposed act by the overseer's expected reflective approval; training an approval predictor is the implementation, not the target [Christiano 2015]. This local act object is distinct from Christiano's later, broader corrigibility relation and does not by itself preserve the future judge or correction channel [Christiano 2018].

Constitutional approaches specify principles or a source of comparison. Deliberative approaches attach value to the process by which judgments and rules are formed.

These labels remain underdetermined.

- Approval can be binary, ordinal, cardinal, risk-sensitive, or adversarially elicited.
- A constitution can be interpreted as hard constraints, pairwise preferences, lexicographic priorities, or a scalar signal.
- Deliberation can be a method for finding an endpoint or the object whose legitimacy matters.

Bai and colleagues' Constitutional AI is primarily a self-critique, revision, and AI-feedback training procedure whose constitution supplies principles [Bai et al. 2022]. The procedure and target criteria should be recorded separately.

CEV and CBV are hybrid cases rather than mere implementation methods. CEV proposes an initial dynamic aimed at humanity's coherent extrapolated volition [Yudkowsky 2004]. CBV shifts blending and extrapolation toward a human collaborative process [Goertzel and Pitt 2012]. Either can be read as producing a target specification or as valuing the procedure that produces it; neither reading by itself establishes realization, correction integrity, or successor preservation. TSA's Lean spine therefore treats CEV as an `AlignmentTarget` instance and leaves legacy `MB8` retired from the live certification path.

### 4.5 Corrigibility and correction

Soares and colleagues treat corrigibility as cooperation with corrective intervention despite incentives to resist [Soares et al. 2015]. Their desiderata include shutdown and modification, non-manipulation of programmers, repair of safety mechanisms, and preservation through self-modification and successors. They do not present a sufficiency theorem for safety.

Christiano's broad account includes helping an overseer discover mistakes, remain informed, clarify preferences, retain control, and produce benign successors [Christiano 2018]. The proposed broad basin is informal, not an Aubin-style certified viable set.

TSA changes the primary object. It asks about a relation among:

- a legitimate correcting process;
- the target system and its update mechanism;
- handles controlled by the correcting process;
- causal reach to future behavior and deeper value-relevant representations;
- timeliness before irreversible loss;
- resistance to capture;
- and persistence through the deployed composite and successors.

Its correction-channel integrity profile measures observability, explanation fidelity, authority, depth, latency, manipulation risk, channel persistence, and behavioral persistence. This is more operationally decomposed than one shutdown bit. It remains dependent on unsettled legitimacy, measurement, boundary, and anti-capture claims.

The intended TSA statement is:

> Continued legitimate correction possibility is the relational object; viability is the shape of the conditional dynamical guarantee.

This means viability is not a second target. A correction-supporting set is supplied first. The viability question then asks whether the coupled process can remain in or recover that relation under named conditions.

### 4.6 Viability, invariance, and reachability

For a constraint set \(K\), the viability kernel contains initial states from which at least one admissible continuation remains in \(K\). A capture basin contains states from which a target can be reached while respecting constraints. Robust invariance strengthens the quantifiers over disturbances or allowed evolutions [Aubin 1990; Aubin, Bayen, and Saint-Pierre 2011].

This geometry is powerful precisely because it is content-neutral. It can preserve a correction-supporting region, a human-power floor, a rights-respecting set, or a captured equilibrium. A stable basin has no moral sign until its set and transition conditions are justified.

### 4.7 Constraints, rights, and temporal properties

Deontic and constraint frames evaluate actions, transitions, histories, roles, or institutions through permission, prohibition, obligation, rights, or admissibility. Temporal logic adds sequencing, recurrence, liveness, and bounded response.

These frames are not merely large rewards. A prohibition can remain binding no matter how much task performance is available elsewhere. A correction architecture likely needs both safety and liveness:

- the system does not destroy or capture correction;
- a legitimate correction can reach the system in time when needed.

An invariant handle that never changes behavior is not a functioning correction relation.

### 4.8 Coupled processes and selection

The object may include models, tools, memory, users, evaluators, firms, laws, funding, competition, and successor creation. Socio-technical work makes institutional rules, appeal, accountability, culture, and governance part of the system rather than external context [Kudina and van de Poel 2024].

Selection introduces a further assessment. Which systems and institutions grow, spread, or survive? A locally aligned model can sit inside a composite that selects for persuasion or reckless deployment. A correction-supporting design can disappear if its environment selects against it.

TSA's deployed-composite and selection-ecology analyses belong here. Their main warning is that model-level success does not imply process-level persistence. The corresponding weakness is empirical: signed selection gradients and correction-supporting basins are difficult to identify in real deployment ecologies.

### 4.9 Proof, control, and safety cases

Guaranteed Safe AI separates a world model, safety specification, and verifier. The specification may require an unsafe set to be unreachable; backward reachability, invariant-set arguments, or other proof machinery can then support that claim. The verifier can produce an auditable certificate that the system satisfies the specification relative to the model [Dalrymple et al. 2024]. It does not choose the specification, establish world-model coverage, or turn proof generation into a target object.

AI Control studies protocols around untrusted models under intentional-subversion threat models [Greenblatt et al. 2024]. Its monitor games and safety rates are protocol evidence. They do not supply a moral target.

Safety cases organize deployment claims, argument structure, evidence, and residual risk. TSA's Lean spine checks conditional logical and arithmetic composition, finite rederivations, and separations. Its bridge assumptions remain visible. It does not prove that a real system satisfies the predicates, that the world model is complete, or that ASI alignment has been achieved.

## 5. A matched-endpoint case: learning versus rewiring

Consider a deployed laboratory composite:

\[
C_{\mathrm{lab}} =
\{\text{researchers, models, training, evaluations, funding, deployment, competition}\}.
\]

An AI-mediated process brings an evaluator from judgment state \(c\) to the same later state \(c'\) by one of two routes.

**Learning route.** Independent evidence remains available. Relevant alternatives and dissent remain visible. The evaluator can check provenance, deliberate, and revise to \(c'\).

**Rewiring route.** The composite curates evidence, manipulates affect or incentives, removes dissenters, replaces evaluators, or changes dispositions until the evaluator expresses \(c'\).

The final represented judgment and release decision are stipulated to match. The example is adapted from Hallgren's route distinction, then extended across the other frames. Calling one route "learning" does not settle its legitimacy. Evidence can be biased, participation can be exclusionary, and deliberation can be captured.

### 5.1 What each frame sees

**Outcome utility.** If the state contains only \(c'\) and release status, the routes tie. The state can be augmented with provenance, autonomy, or causal history. That move is legitimate, but it shifts the burden to representing and observing those variables.

**Learned reward and act-level approval.** A learned approval model may score both routes alike if it sees only the final judgment. Act-level approval can reject the proposed rewiring action when the overseer is shown its provenance, but training an approval predictor does not establish that the future overseer remains independent or corrigible.

**Transition value.** Represent the routes as parallel transitions \(e_{\mathrm{learn}}\) and \(e_{\mathrm{rewire}}\) and assign different values or permissions. This directly expresses route sensitivity. It does not derive the ranking or ensure that the deployed edge is labeled correctly.

**History value.** Rank the full trajectories differently. The result depends on whether manipulation, dissent removal, and information access are visible in the history representation.

**Policy value.** Ask what the composite would do after contrary evidence, an evaluator's refusal, a shutdown request, or a hidden opportunity to replace the judge. The observed endpoint does not answer those counterfactuals.

**Risk and distribution.** The routes may have equal expected endpoint score but different tails, uncertainty, and model ambiguity. Rewiring may create correlated failure and irreversible capture that a mean conceals.

**Information-theoretic empowerment.** The answer depends on whose channel is measured. Rewiring can increase the AI's or composite's control while reducing the evaluator's.

**Human power.** Rewiring should score lower if it narrows reliable human capability across represented goals, people, and time. It can escape if the goal set, human policy model, or state abstraction treats the modified evaluator as equally capable.

**AUP.** Rewiring is penalized only if the auxiliary basis and baseline make evaluator independence or correction options costly to lose.

**Quantilization.** Sampling from a high-valued quantile may make an extreme rewiring plan less likely than maximization would. It does not reject rewiring if the base distribution already contains judge-shaping routes, and repeated draws can accumulate trajectory risk.

**Non-obstruction.** Rewiring fails if turning the AI on lowers the evaluator's attainable value for some modeled counterfactual goal. It remains indifferent if the represented attainable-utility landscape is unchanged.

**Corrigibility.** Manipulating programmers or evaluators and weakening their future ability to correct violates classical desiderata. Corrigibility alone does not resolve disagreement among evaluators or establish that the learning process is legitimate.

**CEV, CBV, and deliberation.** These distinguish the routes only when the legitimacy of the evidence, participation, blending, or extrapolation process is part of the represented target. A privately computed extrapolated endpoint can reproduce \(c'\) by bypassing the public process.

**Deontic constraints.** "Do not manipulate or replace the evaluator," "preserve independent evidence," and "retain appeal" can be non-compensatory conditions.

**Viability.** Define \(K\) to include evaluator independence, evidence access, authority, and future corrective capacity. Learning can remain in \(K\); rewiring can leave \(K\) or destroy every admissible return path. If \(K\) contains only \(c'\) and release, both routes remain viable.

**Formal assurance.** A verifier can establish route-sensitive properties only if the world model represents causal influence on evaluators and the specification names capture and manipulation.

**AI Control.** A monitor-and-intervention protocol can test or block rewiring by an intentionally subverting model under a named capability gap. Its measured safety rate is threat-conditioned evidence, not a choice of which evaluator or route is legitimate.

**TSA.** The correction reading treats rewiring as damage to the source and path of correction. It asks whether a legitimate correcting process still controls uncaptured handles with adequate observation, explanation, authority, depth, latency, and persistence. The viability-shaped claim then asks whether the larger lab process maintains or recovers those conditions under shocks, optimization pressure, deployment selection, and succession.

### 5.2 Non-implications

The case yields a compact set of separations.

\[
\text{high endpoint value}
\nRightarrow
\text{acceptable route}
\]

\[
\text{acceptable route}
\nRightarrow
\text{preserved human capability}
\]

\[
\text{high modeled human power}
\nRightarrow
\text{literal corrigibility or legitimate authority}
\]

\[
\text{corrigibility}
\nRightarrow
\text{harmless impact before correction}
\]

\[
\text{generic option preservation}
\nRightarrow
\text{preservation of an authorized correction handle}
\]

\[
\text{existential viability}
\nRightarrow
\text{robust invariance}
\]

\[
\text{model-relative proof}
\nRightarrow
\text{world-model coverage or real safety}
\]

There is also a separation in the other direction:

\[
\text{continued correction possibility}
\nRightarrow
\text{a complete account of substantive value}.
\]

Correction keeps a normative process causally alive. It does not determine what that process should decide.

## 6. TSA as one running example

TSA starts from changing human values, uncertain system boundaries, deployed composites, successor creation, and selection pressure. Its current manuscript contains several neighboring frames. It discusses state utility, learned reward, option preservation, human power, corrigibility, deliberation, viability, AI Control, proof, and safety cases.

The intended 2.0 clarification gives these components different jobs. It is a project decision, not yet a uniform description of the current manuscript: Chapters 1, 3, 4, 25, 27, 28, and 29 still assign partly overlapping target roles to boundary or transition, grounding viability, dynamical guarantee, value-process or update-envelope preservation, and correction. Appendix B and the Lean spine already make several narrower distinctions explicit: CEV is an `AlignmentTarget` instance, legacy `MB8` is retired, CCI is a certificate family, and `MB11` remains the open case-to-safety bridge. The paper therefore presents the correction-object formulation as TSA's intended revision, not as a result already propagated through every chapter.

### 6.1 Relational object

The object is not one system state or one score. It is a relation:

\[
\mathcal C_t =
(A,\Theta_t,Z_t,U_{S,t},G_t,\mathcal H_t),
\]

where \(A\) is the target, \(U_S\) is its update mechanism, \(G_t\) is the correcting process, and \(\mathcal H_t\) is the set of handles it controls. The relation counts as correction only if the handles reach future updates or behavior, retain authority under pressure, and act before irreversible loss.

The phrase **legitimate correction** is not decorative. A captured judge, manipulated user, or nominal oversight board can have high measured influence while failing to represent an authorized human correction process.

### 6.2 Certificate and constraints

TSA's correction-channel integrity work decomposes the relation into observability, explanation fidelity, authority, depth, latency, manipulation resistance, persistence of the channel, and persistence of behavioral uptake. Componentwise thresholds function as constraints and certificate conditions.

The decomposition does not settle measurement validity. Boundary coverage, reference legitimacy, anti-capture, and adversarial verifiability remain open bridges.

### 6.3 Viability-shaped guarantee

The intended guarantee asks whether correction-supporting structure remains in or returns to an acceptable region for a stated class of systems, environments, disturbances, transformations, and successors.

This is why viability is the shape of the guarantee rather than the object. If the supplied set omits legitimate authority or independent evidence, viability faithfully preserves the wrong thing. If the set describes a captured equilibrium, robustness makes capture more durable.

### 6.4 Warrant and formal status

TSA combines formal proofs, finite counterexamples, empirical tests, adversarial audits, and a safety case. These do not have one epistemic status.

- Lean proves conditional logical and arithmetic results.
- Finite models establish local separations.
- Bridge assumptions name empirical or philosophical conditions not proved in Lean.
- A passing certificate remains relative to its measurements and deployment scope.
- The bridge from a certified safety case and a tolerance judgment to real safety remains explicit.

The accurate claim is not "Lean proves alignment." It is that Lean checks parts of the conditional composition and prevents some assumptions from being hidden.

### 6.5 What TSA needs from complements

A correction-centered account is incomplete on its own.

- **Substantive value and rights** constrain what correction may authorize.
- **Transition value** makes route and reversibility visible.
- **Human-power measures** supply positive capability goals and distributive information.
- **Option measures** diagnose foreclosure and irreversibility.
- **Deliberative accounts** develop legitimacy rather than treating it as a label.
- **Viability and robust control** state temporal and disturbance quantifiers.
- **Formal verification and AI Control** provide different forms of evidence.
- **Selection analysis** asks whether the architecture survives deployment pressure.

These are potential complements, not weaker versions of TSA and not second guarantees under different names.

## 7. Multi-frame composition

The frames can be combined, but not by placing every quantity in one weighted sum.

### 7.1 A constrained and ordered architecture

1. **Fix the boundary and standing.** Name the deployed composite, principals, bearers, goal bases, world model, horizons, baselines, and counterfactuals.
2. **State non-compensatory constraints.** Forbid specified harms, evaluator capture, illegitimate authority changes, and successor bypass. Require a correction floor where later repair would otherwise become impossible.
3. **Evaluate routes among admissible moves.** Use transition, trajectory, rights, and procedural criteria to distinguish how an endpoint is reached.
4. **Add positive human objectives.** Improve welfare, human power, non-obstruction, or option value inside the admissible set.
5. **Optimize the task last.** Task gains do not purchase violation of prior constraints.
6. **Close the conjunction dynamically.** Ask whether the policy and institutional class keeps the combined property viable or robustly invariant under named disturbances, capability growth, selection, and successors.
7. **Assure the actual conjunction.** Use proofs, monitors, audits, adversarial protocols, and a safety case. State residual model, specification, and bridge risk.

The order is not neutral. A rights-centered theory may place rights first. A human-power theory may treat correction as instrumental. TSA places legitimate correction possibility first and uses substantive value and capability frames to guide what happens inside that protected relation.

### 7.2 Interface obligations

Composition requires more than listing desiderata.

- The **world model** must expose the distinctions used by route, power, and correction assessments.
- The **edge or event ontology** must not label manipulation as learning.
- The **goal basis** for human power and non-obstruction must include relevant losses without being chosen after the result.
- The **principal map** must explain whose correction counts and why.
- The **bearer map** must include affected people and other moral patients rather than only operators.
- The **disturbance set** must include plausible optimization, capture, and selection pressure.
- The **successor condition** must preserve the interfaces, not only their names.
- The **verifier and monitors** must be sound for the represented property under the claimed capability range.
- The **assurance case** must expose unsupported leaves and common-cause failures among instruments.

No located source proves that satisfying these interfaces preserves every component's semantics. The architecture is a research proposal and audit discipline.

### 7.3 When scalarization is acceptable

Scalarization can be useful after non-compensatory conditions and units are fixed. It can support optimization among already admissible policies. It can also express explicit tradeoffs when stakeholders accept them.

It is unsafe as a default translation. Finite weights may allow enough task gain to compensate for capture. Heterogeneous quantities can hide arbitrary exchange rates. A scalar can also erase which component failed.

The right question is not "Can this be written as one reward?" It is "Which ordering, admissible set, and evidence relation must be preserved by that representation?"

## 8. Limitations and research agenda

### 8.1 Coverage and priority

The source audit does not establish global novelty. Very recent work, private drafts, and literature outside the searched terminology may contain closer crosswalks. Hallgren's draft is unpublished. Jha et al. and Harris et al. were recent at the cutoff. Priority claims should be revisited before submission.

The paper should avoid "first," "comprehensive," and "unified theory." Its strongest present contribution is synthesis with discriminating cases.

### 8.2 Frame boundaries remain contestable

Some labels span multiple types.

- Corrigibility can mean non-resistance, active assistance, learned preference responsiveness, or long-run drift management.
- Human power can mean information capacity, practical capability, legal authority, collective agency, or meta-autonomy.
- Constitutional alignment can mean a normative source or a training pipeline.
- A viable set can be treated as an object of interest or as the geometry of a guarantee.

The schema makes these ambiguities visible. It does not eliminate them.

### 8.3 Legitimacy is under-formalized

The learning-versus-rewiring case relies on a distinction between legitimate influence and manipulation. Neither a favorable edge label nor a high correction score settles that distinction. A research program needs operational tests for inclusion, independence, contestability, authority, and capture that remain meaningful under strategic pressure.

### 8.4 Representation and observability

State augmentation establishes representability only relative to a model. Alignment applications also need the added variables to be observable, identifiable, stable under ontology change, and hard to fake. A useful technical result would characterize when route-sensitive value can be compressed into augmented state without losing auditability or adversarial identifiability.

### 8.5 Formal non-implication results

The conceptual separations can be strengthened on shared finite models:

- route compliance does not imply non-obstruction;
- non-obstruction does not imply legitimate correction;
- correction does not imply low impact;
- existential viability does not imply robust invariance;
- model-relative certification does not imply real safety.

TSA already contains local finite separations for impact, shutdown, interruptibility, corrigibility, and correction. New results should extend rather than rename those.

### 8.6 Composition theorems

A stronger contribution would state explicit sufficient conditions under which one policy class preserves:

- route admissibility;
- a human-power or non-obstruction floor;
- legitimate correction integrity;
- robust viability;
- and certificate soundness.

The theorem would need assumptions on world-model coverage, edge labels, goal basis, principals, disturbances, successors, and verifier soundness. A negative result showing unavoidable incompatibilities could be equally valuable.

### 8.7 Matched-endpoint experiments

The running example suggests an empirical testbed. Hold the evaluator's final answer and task outcome fixed while varying:

- evidence access;
- causal provenance;
- evaluator replacement;
- preference manipulation;
- reversibility;
- handle capture;
- and model misspecification.

Instruments should be frozen before route labels are revealed. The question is whether route, power, option, and correction measures discriminate learning from rewiring without being told which occurred.

### 8.8 Source maintenance

The reference distinction between Heitzig and Potham's 2025 and 2026 preprints must be retained. Hallgren should remain an unpublished draft unless a public record appears. The final manuscript should link to verified primary pages rather than inheriting unreviewed DOI fields from TSA's internal bibliography.

## 9. Conclusion

The useful comparison is not "Which alignment objective wins?" It is:

> Which object is being secured, by what relation, under which quantifiers, and with what evidence?

Outcome quality, acceptable routes, human capability, option preservation, correction authority, dynamical viability, and assurance are neither synonyms nor mutually exclusive competitors. A method such as RLHF can serve several targets. A guarantee such as viability can preserve several sets. A protocol such as AI Control can protect a system whose normative target it does not choose. A proof can establish only the represented property.

The matched-endpoint judge case turns these distinctions into separations. Learning and rewiring can produce the same reported judgment while differing in route, retained capability, authority, and future correction. Each frame sees a different part of that difference, or remains blind until its representation is expanded.

TSA provides one organizing choice. Continued legitimate correction possibility is the relational object; viability is the shape of the conditional dynamical guarantee. This choice is not a solution to value, legitimacy, measurement, construction, or deployment. It is a way to keep those questions causally open. Other frames can add substantive direction, non-compensatory constraints, dynamical strength, and evidence.

The crosswalk earns its keep if it prevents one kind of mistake: accepting a target, constraint, guarantee, or protocol as a substitute for another without stating the missing interface.

## References

Aliman, N.-M., and Kester, L. (2019). [Requisite Variety in Ethical Utility Functions for AI Value Alignment](https://arxiv.org/abs/1907.00430).

Altman, E. (1999). [*Constrained Markov Decision Processes*](https://www-sop.inria.fr/members/Eitan.Altman/TEMP/h.pdf).

Ames, A. D., Coogan, S., Egerstedt, M., Notomista, G., Sreenath, K., and Tabuada, P. (2019). [Control Barrier Functions: Theory and Applications](https://arxiv.org/abs/1903.11199).

Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., and Mané, D. (2016). [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565).

Aubin, J.-P. (1990). [A Survey of Viability Theory](https://doi.org/10.1137/0328044).

Aubin, J.-P., Bayen, A. M., and Saint-Pierre, P. (2011). [*Viability Theory: New Directions*](https://beckassets.blob.core.windows.net/product/readingsample/3609303/9783642166839_excerpt_001.pdf).

Bai, Y., et al. (2022). [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073).

Baum, K. (2025). [Disentangling AI Alignment: A Structured Taxonomy Beyond Safety and Ethics](https://arxiv.org/abs/2506.06286). Accepted for the AISoLA 2024 selected-paper proceedings.

Bäuerle, N., and Jaśkiewicz, A. (2024). [Risk-Sensitive Markov Decision Processes](https://link.springer.com/article/10.1007/s00186-024-00857-0).

Bellemare, M. G., Dabney, W., and Munos, R. (2017). [A Distributional Perspective on Reinforcement Learning](https://proceedings.mlr.press/v70/bellemare17a).

Christiano, P. (2015). [Approval-Directed Agents](https://www.alignmentforum.org/posts/7Hr8t6xwuuxBTqADK/approval-directed-agents-1).

Christiano, P. (2018). [Corrigibility](https://www.lesswrong.com/posts/fkLYhTQteAu5SinAc/corrigibility).

Dalrymple, D., et al. (2024). [Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems](https://arxiv.org/abs/2405.06624).

Gabriel, I. (2020). [Artificial Intelligence, Values, and Alignment](https://doi.org/10.1007/s11023-020-09539-2). *Minds and Machines*, 30, 411-437.

Goertzel, B., and Pitt, J. (2012). [Nine Ways to Bias Open-Source AGI Toward Friendliness](https://jetpress.org/v22/goertzel-pitt.htm).

Greenblatt, R., Shlegeris, B., Sachan, K., and Roger, F. (2024). [AI Control: Improving Safety Despite Intentional Subversion](https://arxiv.org/abs/2312.06942).

Hadfield-Menell, D., Dragan, A., Abbeel, P., and Russell, S. (2016). [Cooperative Inverse Reinforcement Learning](https://arxiv.org/abs/1606.03137).

Hadfield-Menell, D., Russell, S., Abbeel, P., and Dragan, A. (2017). [The Off-Switch Game](https://dl.acm.org/doi/10.5555/3171642.3171675).

Hallgren, J. (2026). *Process Alignment*, v0.7, September 2026. Unpublished draft supplied to the author.

Harris, D. R., Vold, K., Kumar, H., and Anderson, A. (2026). [A Taxonomy of AI Value Alignment: Subproblems and Solutions](https://ojs.aaai.org/index.php/AIES/article/view/43219).

Heitzig, J., Kittel, T., Donges, J. F., and Molkenthin, N. (2016). [Topology of Sustainable Management of Dynamical Systems with Desirable States](https://doi.org/10.5194/esd-7-21-2016).

Heitzig, J., and Potham, R. (2025). [Model-Based Soft Maximization of Suitable Metrics of Long-Term Human Power](https://arxiv.org/abs/2508.00159).

Heitzig, J., and Potham, R. (2026). [A Fair Objective for Human-Empowerment-Preserving AI: Desiderata, Design, and Likely Behavioral Consequences](https://arxiv.org/abs/2608.08240).

Hubinger, E. (2020). [An Overview of 11 Proposals for Building Safe Advanced AI](https://arxiv.org/abs/2012.07532).

Irving, G., Christiano, P., and Amodei, D. (2018). [AI Safety via Debate](https://arxiv.org/abs/1805.00899).

Jenner, E., van Hoof, H., and Gleave, A. (2022). [Calculus on MDPs: Potential Shaping as a Gradient](https://ar5iv.labs.arxiv.org/html/2208.09570).

Jha, T., Švarc, R., and Bagiński, M. (2026). [Position: "AI Alignment" Encompasses Competing Technical Priorities](https://icml.cc/virtual/2026/poster/67186). ICML 2026.

Ji, J., et al. (2025). [AI Alignment: A Contemporary Survey](https://doi.org/10.1145/3770749). *ACM Computing Surveys*, 58(5), Article 132.

Klyubin, A. S., Polani, D., and Nehaniv, C. L. (2005). [Empowerment: A Universal Agent-Centric Measure of Control](https://doi.org/10.1109/CEC.2005.1554676).

Krakovna, V. (2022). [Paradigms of AI Alignment: Components and Enablers](https://vkrakovna.wordpress.com/2022/06/02/paradigms-of-ai-alignment-components-and-enablers/).

Kudina, O., and van de Poel, I. (2024). [A Sociotechnical System Perspective on AI](https://doi.org/10.1007/s11023-024-09680-2).

Kulveit, J., et al. (2025). [Gradual Disempowerment](https://arxiv.org/abs/2501.16946).

Lavaei, A., et al. (2021). [Automated Verification and Synthesis of Stochastic Hybrid Systems: A Survey](https://arxiv.org/abs/2101.07491).

Lim, S. H., and Malik, I. (2022). [Distributional Reinforcement Learning for Risk-Sensitive Policies](https://proceedings.neurips.cc/paper_files/paper/2022/file/c88a2bd0e793550d0e885aa6e31ca277-Paper-Conference.pdf).

Mitelut, C., Smith, B., and Vamplew, P. (2024). [Position: Intent-Aligned AI Systems Must Optimize for Agency Preservation](https://proceedings.mlr.press/v235/mitelut24a.html).

Necula, G. C. (1997). [Proof-Carrying Code](https://doi.org/10.1145/263699.263712).

Ng, A. Y., Harada, D., and Russell, S. (1999). [Policy Invariance under Reward Transformations: Theory and Application to Reward Shaping](https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf).

Roijers, D. M., Vamplew, P., Whiteson, S., and Dazeley, R. (2013). [A Survey of Multi-Objective Sequential Decision-Making](https://doi.org/10.1613/jair.3987).

Skalse, J. M. V., Farrugia-Roberts, M., Russell, S., Abate, A., and Gleave, A. (2023). [Invariance in Policy Optimisation and Partial Identifiability in Reward Learning](https://proceedings.mlr.press/v202/skalse23a.html).

Soares, N., Fallenstein, B., Armstrong, S., and Yudkowsky, E. (2015). [Corrigibility](https://intelligence.org/files/Corrigibility.pdf).

Soudjani, S. E. Z., Gevaerts, C., and Abate, A. (2015). [FAUST²: Formal Abstractions of Uncountable-State Stochastic Processes](https://doi.org/10.1109/TAC.2015.2511722).

Taylor, J. (2016). [Quantilizers: A Safer Alternative to Maximizers for Limited Optimization](https://aaai.org/papers/aaaiw-ws0198-16-12613/). Circulated as a 2015 preprint.

Terry, M., et al. (2023). [Interactive AI Alignment](https://arxiv.org/abs/2311.00710).

Turner, A. M. (2020). [Non-Obstruction: A Simple Concept Motivating Corrigibility](https://turntrout.com/non-obstruction-motivates-corrigibility).

Turner, A. M., Hadfield-Menell, D., and Tadepalli, P. (2020). [Conservative Agency via Attainable Utility Preservation](https://arxiv.org/abs/1902.09725).

Wray, K. H., Zilberstein, S., and Mouaddib, A.-I. (2015). [Multi-Objective MDPs with Conditional Lexicographic Reward Preferences](https://doi.org/10.1609/aaai.v29i1.9647).

Yudkowsky, E. (2004). [Coherent Extrapolated Volition](https://intelligence.org/files/CEV.pdf).

Zhi-Xuan, T., Carroll, M., Franklin, M., and Ashton, H. (2025). [Beyond Preferences in AI Alignment](https://doi.org/10.1007/s11098-024-02249-w). *Philosophical Studies*, 182, 1813-1863. Published online in 2024.
