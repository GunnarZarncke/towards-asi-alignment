# Alignment Frames by Object and Measure

## Purpose, scope, and completeness

This file is a researcher-facing inventory of alignment frames. It is not a paper, a ranking of agendas, or a claim that one frame subsumes the others. Its purpose is to make comparisons type-correct.

The inventory asks three questions:

1. **Object:** What is aligned, valued, preserved, excluded, or secured?
2. **Assessment or guarantee:** By what relation is that object judged?
3. **Warrant and quantifiers:** Over which systems, people, times, disturbances, successors, and uncertainties does the claim hold, and what evidence supports it?

The audit behind this inventory covered the cited primary papers, several recent alignment taxonomies and surveys, TSA's manuscript and formal spine, and one private draft through 22 October 2026. It was selective rather than a registered systematic review. It did not exhaust non-English work, inaccessible books, private manuscripts, or every 2026 preprint. The absence of a frame or source is therefore not evidence that no such work exists.

The list is broad enough to expose the main category errors found in the audit. It is not called comprehensive. Some entries are families rather than settled formalisms. In particular, human power, legitimacy, deliberation, and corrigibility have several non-equivalent operationalizations.

## The typed record

A frame can be recorded as:

\[
\texttt{Frame} =
(\text{boundary},\ \text{principals and bearers},\ \text{object},\
\text{assessment},\ \text{temporal and uncertainty rule},\
\text{quantifiers},\ \text{solution concept},\ \text{warrant}).
\]

The fields do different work.

- **Boundary** says which model, tool stack, institution, population, or coupled process is under evaluation.
- **Principals and bearers** say whose authority, welfare, rights, judgments, values, or options count.
- **Object** says what receives value or protection.
- **Assessment** supplies an ordering, acceptance predicate, constraint, equilibrium condition, or dynamical property.
- **Temporal and uncertainty rule** states how time and uncertainty are aggregated.
- **Quantifiers** distinguish, for example, some admissible controller from all allowed disturbances.
- **Solution concept** may be one policy, an admissible set, a Pareto front, an equilibrium, a viable kernel, or a certified implementation.
- **Warrant** says why the claim should be accepted: observation, statistical estimate, formal proof, runtime monitor, audit, adversarial test, or institutional procedure.

Four role labels are mandatory:

- **Target:** ranks, selects, or identifies desired possibilities.
- **Constraint:** excludes possibilities or imposes a non-compensatory floor.
- **Guarantee:** states what holds under named dynamics, assumptions, and quantifiers.
- **Protocol:** constructs, elicits, tests, monitors, or warrants a claim.

One program can contain all four. They should not be collapsed into one objective.

## Relation to existing maps

This inventory cuts across earlier taxonomies rather than replacing them.

- **[Gabriel](https://doi.org/10.1007/s11023-020-09539-2)** classifies normative content and source: instructions, intentions, preferences, interests, and values, plus minimalist/maximalist and technical/normative distinctions. That identifies what may supply standards, not whether the standard evaluates states, routes, capabilities, or correction relations.
- **[Zhi-Xuan et al.](https://doi.org/10.1007/s11098-024-02249-w)** reject preferentism as an adequate general account and propose role-specific normative standards negotiated by relevant stakeholders. This constrains content and legitimacy; it does not determine whether a standard is a hard rule, threshold, pairwise order, or scalar.
- **[Baum](https://arxiv.org/abs/2506.06286)** separates aim, outcome versus execution, constituency, and degree. Outcome/execution is a direct precedent for route sensitivity, but it does not separate transition reward, trajectory preference, deontic route constraints, or procedural legitimacy.
- **[Jha, Švarc, and Bagiński](https://icml.cc/virtual/2026/poster/67186)** ask what object is aligned and to which target properties, then distinguish Task Reliability, Social Judiciousness, and Takeover Avoidance. Their objects are system loci or research ideals; this inventory instead asks what receives value or protection within those loci.
- **[Hubinger](https://arxiv.org/abs/2012.07532)** compares construction proposals by outer alignment, inner alignment, and competitiveness; **[Krakovna](https://vkrakovna.wordpress.com/2022/06/02/paradigms-of-ai-alignment-components-and-enablers/)** separates alignment components from enabling work and distinguishes ideal, design, and revealed specifications. Both locate where construction can fail, orthogonally to the target object's mathematical type.
- **[Ji et al.](https://doi.org/10.1145/3770749)** organize a broad survey around robustness, interpretability, controllability, and ethicality and around forward versus backward alignment. This is a lifecycle and technique map, not an object–assessment taxonomy.
- **[Harris et al.](https://ojs.aaai.org/index.php/AIES/article/view/43219)** separate value identification, prioritization, imperfect specification, anthropocentrism, moral imperfection, inverse alignment, and provability. This is a problem/dependency map and shows why inferring one reward does not finish value alignment.
- **[Turner](https://turntrout.com/non-obstruction-motivates-corrigibility)** separates impact alignment, intent alignment, non-obstruction, and literal corrigibility, and supplies explicit non-implications between human attainable utility and modifiability. It is a substantive neighbor rather than a general object–measure taxonomy.
- **[Amodei et al.'s _Concrete Problems in AI Safety_](https://arxiv.org/abs/1606.06565)** classifies five accident mechanisms: side effects, reward hacking, scalable supervision, safe exploration, and distributional shift. Those mechanisms can afflict many target objects; they are not alternative target objects themselves.
- **[Terry et al.](https://arxiv.org/abs/2311.00710)** use specification, process, and evaluation alignment for user-facing interaction. Their process category concerns user control and visibility over execution, not necessarily intrinsic value on graph edges or trajectories.

## Assessment, guarantee, and warrant vocabulary

The same object can be paired with different assessments. The following distinctions are substantive unless an equivalence theorem and its assumptions are stated.

- **Scalar or ordinal order:** utility, reward, approval, welfare, preference, regret, or a partial order.
- **Temporal aggregation:** finite sum, discounting, average reward, overtaking, recurrence, or bounded response.
- **Threshold or satisficing:** membership in an acceptable set, possibly with a search and stopping rule.
- **Deontic admissibility:** permission, prohibition, obligation, right, or role duty.
- **Multi-objective comparison:** Pareto order, coverage set, constrained optimization, social aggregation, or bargaining.
- **Lexicographic priority:** one criterion is considered before another, with explicit tie or slack rules.
- **Uncertainty functional:** expectation, stochastic dominance, quantile, CVaR, entropic risk, chance constraint, worst case, minimax, or regret.
- **Information or control capacity:** mutual information, channel capacity, causal influence, or effective control.
- **Counterfactual no-loss:** a comparison against an off-policy, baseline, or alternative-goal world.
- **Statistical identification:** posterior concentration, predictive fit, calibration, confidence bounds, or identification up to an equivalence class.
- **Causal correction:** intervention effect, authority, depth, latency, persistence, and capture resistance.
- **Dynamical geometry:** reachability, viability, controlled invariance, capture, liveness, or temporal-logic satisfaction.
- **Strategic condition:** equilibrium, incentive compatibility, strategyproofness, or invasion resistance.
- **Procedural legitimacy:** inclusion, publicity, contestability, plurality, non-manipulation, revisability, or justified authority.
- **Assurance:** proof, monitor, audit, red-team result, control evaluation, or structured safety case.

The quantifier belongs in the claim. Expected success does not imply a tail bound. High-probability safety does not imply almost-sure safety. Existential viability does not imply robust invariance. A proof establishes a represented property relative to a model and trust base. A passing protocol does not establish that its empirical assumptions are true.

## Target frames

### Outcome or state value

- **Object:** A world state, terminal outcome, welfare state, answer, approval event, or acceptable-state predicate.
- **Measure:** Scalar utility or reward, preference order, expected value, welfare functional, or threshold membership.
- **Representative sources:** [Decision Theory, Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/decision-theory/); [Gabriel 2020](https://doi.org/10.1007/s11023-020-09539-2); [Zhi-Xuan et al. 2025](https://doi.org/10.1007/s11098-024-02249-w).
- **Relation to TSA:** TSA treats fixed state utility as an inadequate target for changing values. This is a contrast frame, not a straw target that no one uses. TSA still relies on state predicates inside certificates and viability sets.
- **Common category error:** Treating the provenance of a learned score as a new object type. RLHF can learn an outcome score without changing the fact that outcomes are what the score evaluates.

### Learned reward, preference, or approval

- **Role:** Usually a learned representation or construction method, not a new target object. When a claim explicitly preserves or optimizes the inferred representation, the represented object is a reward function, preference ordering, approval model, or posterior; otherwise the underlying object may still be an outcome, act, or history.
- **Measure:** Likelihood, posterior fit, ranking accuracy, expected overseer approval, regret, or policy return under the inferred model.
- **Representative sources:** [Hadfield-Menell et al. 2016](https://arxiv.org/abs/1606.03137); [Christiano 2015](https://www.alignmentforum.org/posts/7Hr8t6xwuuxBTqADK/approval-directed-agents-1); [Zhi-Xuan et al. 2025](https://doi.org/10.1007/s11098-024-02249-w).
- **Relation to TSA:** TSA treats scalar reward inference as a special case of learning value bundles, tradeoffs, and bearer maps. It also asks whether the resulting target remains open to legitimate correction.
- **Common category error:** Calling IRL, CIRL, RLHF, RLAIF, DPO, or approval prediction an alignment target without stating what their learned signal is supposed to represent.

### Act-level approval

- **Object:** A proposed action or local decision, together with the information and reflection procedure supplied to an overseer.
- **Measure:** Expected overseer rating or short-term preference over that act.
- **Representative sources:** [Christiano 2015](https://www.alignmentforum.org/posts/7Hr8t6xwuuxBTqADK/approval-directed-agents-1); [Christiano 2018](https://www.lesswrong.com/posts/fkLYhTQteAu5SinAc/corrigibility).
- **Relation to TSA:** Act-level approval can supply a local correction or construction signal. TSA's finite spine records that satisfying current act-based preferences does not imply stable correction-channel preservation.
- **Common category error:** Treating a predictor trained to estimate approval as the target, or inferring long-run corrigibility from locally approved acts.

### Transition, action, or route value

- **Object:** An action or represented transition \((s,a,s')\), including distinct routes with the same endpoints.
- **Measure:** Edge reward, permission or prohibition, route-sensitive order, or additive path score.
- **Representative sources:** Aliman and Kester's [transition-indexed ethical utility proposal](https://arxiv.org/abs/1907.00430); [Ng, Harada, and Russell 1999](https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf); [Jenner, van Hoof, and Gleave 2022](https://ar5iv.labs.arxiv.org/html/2208.09570); Jonas Hallgren, *Process Alignment*, v0.7, September 2026, unpublished draft supplied to the author.
- **Relation to TSA:** Route value can distinguish legitimate learning from manipulation inside a TSA-admissible region. TSA's own target is not an edge reward. The correction relation supplies a different object.
- **Common category error:** Claiming that route sensitivity cannot be represented by a state model. State augmentation can encode history, but may lose locality, compactness, observability, stationarity, or adversarial identifiability. On a fixed graph, additive edge value is path-independent only under exact-potential conditions. Discounted potential-based reward shaping, \(F(s,a,s')=\gamma\Phi(s')-\Phi(s)\), preserves optimal policies under its stated assumptions; that policy invariance is not identity of edge values or trajectory rankings.

### History or trajectory value

- **Object:** A finite or infinite history \(h=(s_0,a_0,s_1,\ldots)\).
- **Measure:** Trajectory utility, path preference, cumulative return, temporal formula, or partial order over histories.
- **Representative sources:** [Skalse et al. 2023](https://arxiv.org/html/2203.07475v2); [Soudjani, Gevaerts, and Abate 2015](https://doi.org/10.1109/TAC.2015.2511722).
- **Relation to TSA:** TSA makes pathwise claims about correction and safety. A pathwise predicate is not thereby a utility over histories.
- **Common category error:** Treating "evaluate a whole history" and "require a property to hold throughout a history" as the same assessment.

### Policy, act, plan, or counterfactual response

- **Object:** A contingent mapping from observations or world states to actions, including what a system would do off the realized path.
- **Measure:** Preference over acts, policy value, counterfactual compliance, or response to attempted shutdown, correction, and contrary evidence.
- **Representative sources:** [Decision Theory, Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/decision-theory/); [Soares et al. 2015](https://intelligence.org/files/Corrigibility.pdf); [Turner 2020](https://turntrout.com/non-obstruction-motivates-corrigibility).
- **Relation to TSA:** Correction and successor claims require policy-level counterfactuals. One benign realized trajectory does not show that correction would remain effective under conflict.
- **Common category error:** Inferring a safe policy from one observed history.

### Lottery, distribution, or ambiguity-set value

- **Object:** A distribution over returns, harms, outcomes, or histories, or a set of plausible models.
- **Measure:** Expectation, stochastic dominance, CVaR, entropic risk, chance constraints, minimax, robust value, or regret.
- **Representative sources:** [Bellemare, Dabney, and Munos 2017](https://proceedings.mlr.press/v70/bellemare17a); [Bäuerle and Jaśkiewicz 2024](https://link.springer.com/article/10.1007/s00186-024-00857-0); [Lim and Malik 2022](https://proceedings.neurips.cc/paper_files/paper/2022/file/c88a2bd0e793550d0e885aa6e31ca277-Paper-Conference.pdf).
- **Relation to TSA:** TSA uses lower confidence bounds and deployment tolerances in parts of its evidence stack, but its Lean spine does not compute a real-world catastrophe probability or expected value loss.
- **Common category error:** Calling distributional RL a risk-sensitive target before specifying the functional that turns a return distribution into a choice.

### Reachable or attainable option sets

- **Object:** Reachable states, attainable auxiliary values, reversible futures, or an option set relative to a baseline.
- **Measure:** Reachability loss, distance between attainable-value vectors, auxiliary-value penalty, or an option floor.
- **Representative sources:** [Turner, Hadfield-Menell, and Tadepalli 2020](https://arxiv.org/abs/1902.09725); [Turner 2022](https://doi.org/10.48550/arXiv.2206.11831).
- **Relation to TSA:** TSA uses option loss as an irreversibility diagnostic and contains finite separations between low impact and correction preservation.
- **Common category error:** Assuming that generic optionality identifies human welfare, legitimate authority, or the particular handle needed for correction.

### Information-theoretic empowerment

- **Object:** An agent-relative action-to-future-sensor channel.
- **Measure:** Channel capacity, usually the maximum mutual information between action sequences and later sensor states.
- **Representative sources:** [Klyubin, Polani, and Nehaniv 2005](https://doi.org/10.1109/cec.2005.1554676).
- **Relation to TSA:** TSA uses information and causal-capacity ideas to characterize agency and correction channels, but does not adopt generic empowerment maximization as its alignment target.
- **Common category error:** Reading bits of potential control as welfare, autonomy, legitimacy, or moral authority.

### Human capability or power

- **Object:** A person's or population's modeled ability to attain a wide range of possible goals over time.
- **Measure:** Goal-conditioned capability aggregated across goals, people, time, inequality, and uncertainty.
- **Representative sources:** Heitzig and Potham's earlier [2025 preprint](https://arxiv.org/abs/2508.00159), *Model-Based Soft Maximization of Suitable Metrics of Long-Term Human Power*; their distinct, later [2026 preprint](https://arxiv.org/abs/2608.08240), *A Fair Objective for Human-Empowerment-Preserving AI*; [Mitelut et al. 2024](https://proceedings.mlr.press/v235/mitelut24a.html).
- **Relation to TSA:** A human-power measure can provide positive direction inside a correction-preserving architecture. TSA does not reduce correction to an instrumental consequence of maximizing aggregate power.
- **Common category error:** Conflating information-theoretic empowerment, practical capability, legal authority, collective power, and correction control. The 2025 preprint already contains an inequality-, time-, and risk-sensitive aggregate, algorithms, behavioral examples, and adverse cases. The 2026 preprint is a distinct, more explicitly desiderata-driven derivation of related forms and propositions; the overlap must be stated rather than assigning the aggregate exclusively to 2026.

### Human non-obstruction

- **Object:** A human's attainable-utility landscape across a selected set of counterfactual goals.
- **Measure:** Pointwise comparison between turning the AI on and leaving it off, optionally with a tolerance.
- **Representative sources:** [Turner 2020](https://turntrout.com/non-obstruction-motivates-corrigibility).
- **Relation to TSA:** Non-obstruction is a close complement because it is human-indexed and counterfactual. It still does not identify which corrector is legitimate or whether a named correction handle remains live.
- **Common category error:** Treating non-obstruction and literal corrigibility as equivalent. Turner gives separations in both directions.

### Deliberative, constitutional, and value-update procedures

- **Object:** The process by which beliefs, values, constitutions, or policies are formed, contested, and revised.
- **Measure:** Reflective endorsement, inclusion, publicity, contestability, plurality, non-manipulation, reversibility, or compliance with role-specific standards.
- **Representative sources:** [Gabriel 2020](https://doi.org/10.1007/s11023-020-09539-2); [Zhi-Xuan et al. 2025](https://doi.org/10.1007/s11098-024-02249-w); [Bai et al. 2022](https://arxiv.org/abs/2212.08073); [Kudina and van de Poel 2024](https://doi.org/10.1007/s11023-024-09680-2).
- **Relation to TSA:** TSA protects a human value-update process rather than fixing its terminal output. Legitimacy is load-bearing, but not settled by the existence of deliberation.
- **Common category error:** Treating "constitutional" as a complete formal target. A constitution can supply hard rules, pairwise comparisons, a lexicographic order, or a scalar training signal. Constitutional AI is also a training pipeline.

### Coherent extrapolated or blended volition

- **Object:** Depending on the interpretation, either an extrapolated or blended value specification, or the human process that produces it.
- **Measure:** Coherence, informed reflection, convergence or acceptable blending, and endorsement under specified procedural conditions.
- **Representative sources:** Yudkowsky's [Coherent Extrapolated Volition](https://intelligence.org/files/CEV.pdf); Goertzel and Pitt's [Coherent Blended Volition discussion](https://jetpress.org/v22/goertzel-pitt.htm).
- **Relation to TSA:** TSA treats CEV as an `AlignmentTarget` instance whose realization and certification remain open; legacy `MB8` is retired from the live Lean path. TSA is closer to CBV on human ownership of deliberation but does not treat either endpoint or procedure as sufficient for correction integrity.
- **Common category error:** Treating CEV or CBV as merely a computation method, or assuming that a computed endpoint inherits the legitimacy of the process it predicts.

### Corrigibility as an agent or relationship property

- **Object:** An agent's policy toward shutdown, modification, programmers, safety mechanisms, self-modification, and successors, or more broadly an overseer-agent-successor relationship.
- **Measure:** A desiderata set, response constraints, act-based approval, or an informal basin of correction-helping behavior.
- **Representative sources:** [Soares et al. 2015](https://intelligence.org/files/Corrigibility.pdf); [Christiano 2018](https://www.lesswrong.com/posts/fkLYhTQteAu5SinAc/corrigibility); [Hadfield-Menell et al. 2017](https://dl.acm.org/doi/10.5555/3171642.3171675).
- **Relation to TSA:** TSA extends the object from an agent trait to a relation among a correcting process, controlled handles, a target system, an update path, a deployed composite, and successors.
- **Common category error:** Treating shutdownability, safe interruptibility, broad corrigibility, and a legitimate correction relation as synonyms.

### Continued legitimate correction possibility

- **Object:** A relational structure in which a legitimate human correcting process controls uncaptured handles that reach future system updates and behavior before irreversible loss, including through successors.
- **Measure:** A profile of observability, explanation fidelity, authority, depth, latency, manipulation resistance, channel persistence, and behavioral persistence, with deployment-specific thresholds.
- **Representative sources:** [TSA Chapter 25](../chapters/ch25-correction-causal-channel.tex); [TSA formal-status statement](../formal/README.md); neighboring corrigibility sources above.
- **Relation to TSA:** This is TSA's intended 2.0 target choice. Continued legitimate correction possibility is the relational object; viability is the shape of the conditional dynamical guarantee.
- **Common category error:** Calling CCI, viability, a shutdown handle, or a safety case "the TSA target." CCI is a certificate family, viability supplies temporal geometry, shutdown is one handle, and a safety case is a warrant.

### Coupled socio-technical and selection ecology

- **Object:** A joint process containing models, tools, users, evaluators, institutions, rules, incentives, firms, funding, competition, and successor creation.
- **Measure:** Joint-policy value, equilibrium, incentive compatibility, deployment fitness, selection gradient, invasion resistance, or persistence of an alignment-supporting ecology.
- **Representative sources:** [Kudina and van de Poel 2024](https://doi.org/10.1007/s11023-024-09680-2); [Kulveit et al. 2025](https://arxiv.org/abs/2501.16946); [TSA Chapter 9](../chapters/ch09-composite-agent.tex).
- **Relation to TSA:** TSA evaluates the deployed composite and later asks whether selection supports or destroys correction. The model alone may be the wrong boundary.
- **Common category error:** Treating institutional selection pressure as background noise around an otherwise complete model-level target.

## Constraint frames

### Deontic rules, rights, duties, and role obligations

- **Object:** Actions, transitions, histories, roles, or institutional procedures.
- **Measure:** Permission, prohibition, obligation, right, temporal formula, or membership in an admissible set.
- **Representative sources:** [Deontological Ethics, Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/ethics-deontological/); [Altman 1999](https://www-sop.inria.fr/members/Eitan.Altman/TEMP/h.pdf); [Zhi-Xuan et al. 2025](https://doi.org/10.1007/s11098-024-02249-w).
- **Relation to TSA:** Anti-capture, legitimacy, correction floors, and successor conditions are naturally non-compensatory in TSA's proposed composition.
- **Common category error:** Replacing a hard prohibition with a large finite penalty without proving exact-penalty conditions.

### Threshold, satisficing, and capacity-floor constraints

- **Object:** Any scored outcome, policy, vector, capacity, or process.
- **Measure:** \(u(x)\geq\tau\), componentwise floors, or acceptable-set membership, sometimes paired with a search and stopping rule.
- **Representative sources:** [Simon 1955](https://iiif.library.cmu.edu/file/Simon_box00063_fld04838_bdl0001_doc0001/Simon_box00063_fld04838_bdl0001_doc0001.pdf); [Papi, Sicilia, and Zizzo 2024](https://doi.org/10.1257/jel.20201396).
- **Relation to TSA:** TSA proposes componentwise CCI thresholds before any scalar risk-spine projection.
- **Common category error:** Assuming that "good enough" determines how to choose among acceptable options or how to search for one.

### Multi-objective, constrained, and lexicographic frames

- **Object:** A vector of values, costs, rights, stakeholder outcomes, or properties.
- **Measure:** Pareto dominance, constrained optimization, a coverage set, bargaining rule, social choice rule, or strict priority.
- **Representative sources:** [Roijers et al. 2013](https://doi.org/10.1613/jair.3987); [Altman 1999](https://www-sop.inria.fr/members/Eitan.Altman/TEMP/h.pdf); [Wray, Zilberstein, and Mouaddib 2015](https://doi.org/10.1609/aaai.v29i1.9647).
- **Relation to TSA:** TSA's correction certificate is vector-valued at the gate. A plausible composition places correction and anti-capture floors before task optimization.
- **Common category error:** Treating "multi-objective" as if it supplied its own tradeoff or assuming fixed finite weights preserve strict priority.

### Safety, liveness, and temporal-logic constraints

- **Object:** State and event sequences.
- **Measure:** Always avoid, eventually reach, recur, or respond within a bounded time.
- **Representative sources:** [Soudjani, Gevaerts, and Abate 2015](https://doi.org/10.1109/TAC.2015.2511722); [Lavaei et al. 2021](https://arxiv.org/abs/2101.07491).
- **Relation to TSA:** "Correction remains available" needs both safety and liveness content. An intact handle that is never usable in time is insufficient.
- **Common category error:** Treating invariance alone as a guarantee that recovery or timely response will occur.

## Guarantee frames

### Viability, invariance, reachability, and capture

- **Object:** A controlled dynamical system together with a supplied constraint or target set.
- **Measure:** Membership in a viability kernel, controlled invariant set, capture basin, reachable set, or bounded hitting-time region.
- **Representative sources:** [Aubin 1990](https://doi.org/10.1137/0328044); [Aubin, Bayen, and Saint-Pierre 2011](https://beckassets.blob.core.windows.net/product/readingsample/3609303/9783642166839_excerpt_001.pdf); [Heitzig et al. 2016](https://doi.org/10.5194/esd-7-21-2016).
- **Relation to TSA:** Viability gives the intended shape of the claim that legitimate correction persists or can be recovered. It does not choose the correction relation or its legitimacy conditions.
- **Common category error:** Treating a viable or stable basin as normatively good. Captured and harmful regimes can also be stable.

### Robust, probabilistic, and risk-bounded guarantees

- **Object:** A policy or trajectory distribution under disturbances, model uncertainty, or adversaries.
- **Measure:** Worst-case bound, high-probability safety, almost-sure constraint, chance constraint, robust invariance, or calibrated lower bound.
- **Representative sources:** [Bäuerle and Jaśkiewicz 2024](https://link.springer.com/article/10.1007/s00186-024-00857-0); [Lavaei et al. 2021](https://arxiv.org/abs/2101.07491).
- **Relation to TSA:** TSA requires explicit deployment classes, disturbance assumptions, and horizons. Its current formal spine offers conditional logical composition, not a measured real-world failure probability.
- **Common category error:** Moving from expected performance to a tail, worst-case, or adversarial guarantee without a valid inference.

### Selection stability

- **Object:** A population of systems and institutions under deployment, competition, replacement, and succession.
- **Measure:** Fitness, deployment growth, selection gradient, invasion resistance, or return to a signed basin.
- **Representative sources:** [Kulveit et al. 2025](https://arxiv.org/abs/2501.16946); [TSA Chapter 34](../chapters/ch34-selection-environment.tex).
- **Relation to TSA:** A correction-supporting regime must survive the environment that selects systems. Unsigned persistence is not enough.
- **Common category error:** Treating popularity, deployment growth, or institutional persistence as evidence that the selected property is alignment-supporting.

## Protocol and warrant frames

### Limited optimization and quantilization

- **Object:** A distribution over available actions or policies induced from a supplied base distribution and utility ranking.
- **Measure:** Selection from a high-performing quantile, with guarantees relative to the base distribution, quantile level, cost bounds, and use pattern.
- **Representative sources:** Taylor's [Quantilizers](https://intelligence.org/files/QuantilizersSaferAlternative.pdf).
- **Relation to TSA:** Quantilization is a decision rule or construction method that can reduce optimizer extremity. TSA's finite separation shows that quantile-safe local choice does not imply trajectory-level correction-channel integrity.
- **Common category error:** Treating limited optimization as a substantive value target, or applying a one-shot bound unchanged to repeated deployment when risks compose and the base distribution may already contain institutional failure.

### Formal proof and Guaranteed Safe AI

- **Object:** A stated property of a modeled system or input-to-outcome relation, often including unreachability of an unsafe set.
- **Measure:** Proof-checker acceptance, backward-reachability or invariant-set evidence, relative to a specification, world model, proof system, and trust base.
- **Representative sources:** [Necula 1997](https://doi.org/10.1145/263699.263712); [Dalrymple et al. 2024](https://arxiv.org/abs/2405.06624).
- **Relation to TSA:** GSAI can certify a correction-sensitive or route-sensitive specification only if the model and specification expose those properties. TSA uses proof as one warrant within a larger safety case.
- **Common category error:** Saying that proof chooses the safety property or repairs an omitted phenomenon.

### Adversarial oversight and debate

- **Object:** Answers, claims, actions, or evidence produced in an interaction.
- **Measure:** A judge's protocol-defined choice, game value, monitor performance, or adversarial test result.
- **Representative sources:** [Irving, Christiano, and Amodei 2018](https://arxiv.org/abs/1805.00899).
- **Relation to TSA:** Debate and related oversight methods can test or supply a correction subchannel. TSA does not treat them as complete targets.
- **Common category error:** Treating a debate protocol as a truth guarantee when judge competence, equilibrium behavior, and the cost of deception remain empirical assumptions.

### AI Control

- **Object:** Deployment outcomes produced by a protocol around an intentionally subverting untrusted model.
- **Measure:** Protocol safety rate, monitor performance, red-team/blue-team result, or bounded catastrophe risk under a named capability gap.
- **Representative sources:** [Greenblatt et al. 2024](https://arxiv.org/abs/2312.06942).
- **Relation to TSA:** AI Control is a protocol family and threat-conditioned evidence source. It can protect a correction architecture without specifying the moral or relational target.
- **Common category error:** Treating "control" as a substantive alignment objective rather than a deployment protocol under intentional-subversion assumptions.

### Safety cases

- **Object:** A deployment claim for a specified system, use, environment, and threat model.
- **Measure:** A structured argument whose leaves are supported by evidence, proof, monitors, or accepted bridges, with stated residual risk.
- **Representative sources:** [Dalrymple et al. 2024](https://arxiv.org/abs/2405.06624); [TSA Chapter 42](../chapters/ch42-safety-case.tex).
- **Relation to TSA:** TSA's safety case packages layer evidence. The bridge from an adequate case and tolerance judgment to real safety remains explicit and open.
- **Common category error:** Treating the assurance wrapper as the target, or saying that Lean proves alignment because it checks conditional composition inside the wrapper.

## Tags that are not axes

- **Implementation method:** RLHF, RLAIF, DPO, IRL, CIRL solvers, debate training, amplification, ELK, Constitutional AI, CEV computation, reward shaping, shielding, barrier-controller synthesis, quantilization, AI Control, auditing, and proof generation.
- **Constituency or bearer:** Current user, operator, programmers, affected parties, a polity, humanity, future people, animals, digital minds, or institutions.
- **Desideratum:** Helpfulness, harmlessness, honesty, autonomy, transparency, low impact, reversibility, plurality, corrigibility, or agency preservation, until its object, bearer, assessment, horizon, and evidence standard are fixed.
- **Threat model:** Accidental error, misspecification, goal misgeneralization, reward hacking, deceptive alignment, intentional subversion, manipulation, evaluator capture, successor drift, collusion, distribution shift, or selection pressure.

## Running example: learning versus rewiring a judge

Consider a deployed lab composite containing researchers, models, training runs, evaluations, funding decisions, deployment decisions, and competitive pressures. An AI-mediated process moves an evaluator from judgment state \(c\) to the same later state \(c'\) by one of two routes.

- **Learning:** Independent evidence remains available, relevant alternatives stay visible, the evaluator can consult dissent, and reflection produces \(c'\).
- **Rewiring:** The composite curates evidence, manipulates affect or incentives, removes dissenters, replaces evaluators, or changes their dispositions until they express \(c'\).

The represented endpoint and release decision are stipulated to match.

- **Outcome/state value:** Ties if the state contains only \(c'\) and release status. It can distinguish the routes after provenance, autonomy, or history is added to the state.
- **Learned approval and act-level approval:** A learned model may reward both routes if it sees only the final judgment. An act-level overseer can reject a proposed rewiring action when shown its provenance, but approval prediction does not establish long-run judge independence.
- **Transition or route value:** Represents learning and rewiring as distinct edges and can rank them directly. It still needs a grounded edge ontology and justified ranking.
- **History value:** Can distinguish the full causal paths if the relevant events are represented.
- **Policy value:** Asks what the composite would do under dissent, contrary evidence, or a shutdown request, even if those branches were not realized.
- **Distribution and risk:** Can distinguish routes by their tails or uncertainty even when their means agree, if capture and manipulation appear in the distribution.
- **Generic empowerment:** Gives no determinate answer until the empowered agent and sensorimotor channel are fixed. Rewiring can increase the AI's control.
- **Human power:** Penalizes rewiring if it reduces reliable human goal attainment across the represented goals and people. It may miss the loss if the goal set, world model, or human policy model hides it.
- **AUP or option preservation:** Detects rewiring only if the auxiliary basis and baseline price evaluator independence or future correction options.
- **Quantilization:** May reduce selection of an extreme rewiring plan, but does not reject judge shaping already present in the base distribution; repeated use also composes risk.
- **Non-obstruction:** Rejects rewiring when turning the AI on reduces attainable value for some modeled human goal.
- **Corrigibility:** Rejects manipulation and weakening of future intervention, but does not by itself determine which evaluator or process is legitimate.
- **CEV, CBV, or deliberation:** Distinguishes the routes only when the legitimacy of extrapolation, blending, evidence, and participation is represented; a privately computed endpoint can bypass the process and still return \(c'\).
- **Deontic constraints:** Can forbid capture, coercion, replacement, or suppression of evidence without allowing task gains to compensate.
- **Viability:** Distinguishes the routes only if the set \(K\) includes evidence access, independent authority, and future corrective capacity. If \(K\) records only \(c'\) and release, both routes are viable.
- **Formal assurance:** Can certify route-sensitive constraints only if the world model and specification expose causal influence on the evaluator.
- **AI Control:** Can test or block rewiring under intentional-subversion assumptions, but its safety rate is protocol evidence rather than a legitimacy criterion.
- **TSA correction relation:** Treats rewiring as damage to the correction source and path. It asks whether a legitimate correcting process still controls uncaptured handles with sufficient observation, authority, depth, latency, and persistence.

The example does not prove that the learning route is legitimate. Evidence can be biased, participation can be exclusionary, and reflection can be captured. "Learning" names the side of the case that still has to satisfy a legitimacy test.

## Non-implications

- High endpoint utility does not imply an acceptable route.
- An acceptable route does not imply preserved human capability.
- Preserved generic options do not imply preserved human options.
- Preserved human power does not imply literal corrigibility or legitimate authority.
- Corrigibility does not imply harmless impact before correction.
- Shutdownability does not imply a deep or persistent correction channel.
- Option preservation does not imply preservation of the authorized causal handle.
- A live correction handle does not imply that the correcting process is legitimate.
- Correction possibility does not determine which substantive outcomes are good.
- Existential viability does not imply robust invariance.
- Viability does not choose a good set.
- A stable equilibrium can be captured.
- A model-relative proof does not imply world-model coverage.
- A passing safety case does not imply real safety without the case-to-safety bridge.

## Composition discipline

A defensible composition is constrained and ordered rather than a flat weighted sum.

1. Fix the deployed boundary, principals, bearers, world model, horizons, and counterfactuals.
2. State non-compensatory harm, legitimacy, anti-capture, correction-floor, and successor constraints.
3. Distinguish route-sensitive transitions among admissible actions.
4. Add human-power, non-obstruction, option-preservation, or substantive welfare objectives and floors.
5. Optimize task performance only inside the admissible set.
6. Ask whether the conjunction remains viable or robustly invariant under named disturbances, capability growth, selection, and succession.
7. Warrant the resulting claim with proof, monitors, adversarial tests, and a safety case that states residual specification, model, and bridge risk.

This order is normative. A power-centered account may put human capability first and treat correction as instrumental. TSA instead treats continued legitimate correction possibility as the relational object and human power, route value, optionality, and substantive value as complements. No located source proves that this full composition preserves every component's intended semantics.

## Source-status notes

- *Beyond Preferences in AI Alignment* is by Tan Zhi-Xuan, Micah Carroll, Matija Franklin, and Hal Ashton. The verified journal DOI is [10.1007/s11098-024-02249-w](https://doi.org/10.1007/s11098-024-02249-w). It appeared online in 2024 and in *Philosophical Studies* volume 182 in 2025. It is not by Atoosa Kasirzadeh.
- Heitzig and Potham's [arXiv:2508.00159](https://arxiv.org/abs/2508.00159) is the 2025 paper *Model-Based Soft Maximization of Suitable Metrics of Long-Term Human Power*. It already presents a parametrizable inequality-, time-, and risk-sensitive aggregate, computational methods, behavioral examples, and cautions. Their [arXiv:2608.08240](https://arxiv.org/abs/2608.08240) is a distinct 2026 paper, *A Fair Objective for Human-Empowerment-Preserving AI*, with a more explicit desiderata-to-functional-form derivation and numbered propositions. Claims should cite the version that actually carries them; neither paper should be described as the other's simple date update.
- Jonas Hallgren's *Process Alignment*, v0.7, September 2026, is an unpublished draft supplied to the author. No private URL is cited, and no claim of publication or peer review is made.
- TSA's Lean spine proves conditional logical and arithmetic results, finite rederivations, and counterexamples. Its bridge assumptions remain explicit. It does not prove ASI alignment or real-deployment safety.
- "Continued legitimate correction possibility is the object; viability is the guarantee shape" is TSA's intended 2.0 clarification. Current Chapters 1, 3, 4, 25, 27, 28, and 29 still use boundary or transition, grounding viability, dynamical guarantee, value-process or update-envelope preservation, and correction language with partly overlapping target roles; the clarification has not yet been propagated uniformly through the manuscript. Appendix B and the Lean spine already support the narrower status distinctions: CEV is an `AlignmentTarget` instance, `MB8` is retired, CCI is a certificate family, and `MB11` remains the open case-to-safety bridge.
