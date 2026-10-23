/** Node id in drafts/alignment-frames-relations.dot → site lens card. */

export const OVERVIEW_ID = "lenses/lenses-and-frameworks";

export const GH_LEAN =
  "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine";

export const LENSES = [
  {
    nodeId: "hist",
    slug: "history-value",
    title: "History / trajectory value",
    role: "Target",
    summary: "A preference or score on whole paths, not on a snapshot state.",
    quote:
      "A utility or preference over a history represents delayed and path-dependent value directly. A pathwise safety predicate is different.",
    quoteSource: "What Does Alignment Secure? (draft), §4.1",
    lwTag: { label: "LessWrong tag: Decision theory", url: "https://www.lesswrong.com/w/decision-theory" },
    related: ["static-target-trap", "value-change-vs-corruption", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/christiano-lineage", "field-agendas/miri"],
    body: `A history-valued lens scores the sequence \`(s₀, a₀, s₁, …)\`. Two deployments can share an endpoint and still differ if manipulation, dissent removal, or withheld evidence is visible in the history.

Encoding a finite history into an augmented state is always available in principle. The cost is compactness, locality, observability, or stationarity — not a proof that the snapshot object was already enough.`
  },
  {
    nodeId: "route",
    slug: "additive-route-value",
    title: "Additive route value",
    role: "Target",
    summary: "An edge score summed along a walk: what was done, not only where you arrived.",
    quote:
      "Discounted potential-based reward shaping preserves optimal policies under its stated assumptions; that invariance is not identity of edge values.",
    quoteSource: "Ng, Harada, and Russell 1999, via the frames draft §4.1",
    lwTag: { label: "LessWrong tag: Reward shaping", url: "https://www.lesswrong.com/w/reward-hacking" },
    related: ["subsumption-low-impact", "lenses/exact-potential", "lenses/cycle-residue", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell"],
    body: `Route value is a function of transitions. It is the parent of the exact-potential summand (endpoint-only) and the cycle residue (round trips matter).

A matched-endpoint pair — learning versus rewiring a judge to the same later verdict — is invisible to a state score that stores only the verdict, and visible here if the two edges are labeled differently.`
  },
  {
    nodeId: "exact",
    slug: "exact-potential",
    title: "Exact potential summand",
    role: "Target",
    summary: "The part of an additive route score that depends only on endpoints.",
    quote:
      "On its fixed graph with the stated reachability assumption, endpoint-only additive path value is the exact-potential special case.",
    quoteSource: "Frames draft §4.1 (Hallgren process-alignment draft, unpublished)",
    lwTag: { label: "LessWrong tag: Utility functions", url: "https://www.lesswrong.com/w/utility-functions" },
    related: ["lenses/additive-route-value", "lenses/state-utility", "lenses/lenses-and-frameworks"],
    agendas: [],
    body: `If an edge score is a gradient of a state potential, every closed walk sums to zero. That is why state utility and cycle residue conflict on round trips: see the red edge in Lean (\`stateCycleIncompat\`).

Exactness is a representation fact about a particular reward, not a claim that endpoints were the intended moral object.`
  },
  {
    nodeId: "cycle",
    slug: "cycle-residue",
    title: "Cycle residue",
    role: "Target",
    summary: "The part of route value that survives on closed walks — reversibility and round trips.",
    quote: "This is useful for routes, reversibility, and round trips. It does not derive which transitions are good.",
    quoteSource: "Frames draft §4.1",
    lwTag: { label: "LessWrong tag: Instrumental convergence", url: "https://www.lesswrong.com/w/instrumental-convergence" },
    related: ["lenses/additive-route-value", "lenses/correction-relation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/miri"],
    body: `Cycle residue is what a state utility cannot see without expanding the state. Inside a deontic admissible region it can still rank learning above rewiring even when endpoints match.

It composes with correction as “route residue inside the region,” not as a second top-level target.`
  },
  {
    nodeId: "state",
    slug: "state-utility",
    title: "State utility",
    role: "Target",
    summary: "A scalar order or welfare score on snapshots. Adequate only if the state already carries what matters.",
    quote:
      "State value is adequate when the state carries all normatively relevant information. It is not adequate merely because an implementation calls its representation a state.",
    quoteSource: "Frames draft §4.1",
    lwTag: { label: "LessWrong tag: Expected utility", url: "https://www.lesswrong.com/w/expected-utility-formalism" },
    related: ["static-target-trap", "pointing-problem", "outer-alignment", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell", "field-agendas/miri", "field-agendas/openai-lab"],
    body: `This is the default RL and welfare object. Omohundro-style instrumental arguments live here.

Fixed \(U\) is incompatible with correction only for updates that make the agent pick an outcome \(U\) ranks strictly lower — not for every change of \(U\). That is the proved red edge \`stateCorrectionIncompat\`, not “utility hates all revision.”`
  },
  {
    nodeId: "dist",
    slug: "outcome-lottery",
    title: "Outcome lottery",
    role: "Target",
    summary: "A distribution over outcomes; expectation is one functional among many.",
    quote:
      "Expected value, CVaR, stochastic dominance, entropic risk, chance constraints, minimax, and regret can rank the same lotteries differently.",
    quoteSource: "Frames draft §4.2 (Bäuerle and Jaśkiewicz 2024)",
    lwTag: { label: "LessWrong tag: Risk", url: "https://www.lesswrong.com/w/risks-from-ai" },
    related: ["lenses/state-utility", "evidence-and-uncertainty", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell"],
    body: `Distributional RL learns a random return and still leaves open which functional governs action. Projecting to a mean state score has no section: the tails and model ambiguity are gone.`
  },
  {
    nodeId: "criteria_vector",
    slug: "criteria-vector",
    title: "Criteria vector",
    role: "Target",
    summary: "A Pareto / multi-objective vector of task, cost, or stakeholder coordinates — not a CCI certificate.",
    quote: "A vector does not choose its scalarization, Pareto solution, bargaining rule, or lexicographic order.",
    quoteSource: "Frames draft §4.2 (Roijers et al. 2013)",
    lwTag: { label: "LessWrong tag: Goodhart's law", url: "https://www.lesswrong.com/w/goodharts-law" },
    related: ["lenses/weighted-scalar", "lenses/correction-certificate", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/mai-cip-institutional-alignment"],
    body: `Pareto optimality on task coordinates does not entail a correction floor. The red edge to the correction certificate is a non-entailment until weights are chosen (\`viaProjection\`). Do not call a stakeholder vector a CCI score.`
  },
  {
    nodeId: "weighted_scalar",
    slug: "weighted-scalar",
    title: "Weighted scalar",
    role: "Target",
    summary: "A fixed-weight collapse of a criteria vector. Finite weights cannot represent a hard floor.",
    quote:
      "If a violation is non-compensatory, a sufficiently large but finite reward elsewhere must not purchase it.",
    quoteSource: "Frames draft §4.2",
    lwTag: { label: "LessWrong tag: Goodhart's law", url: "https://www.lesswrong.com/w/goodharts-law" },
    related: ["lenses/criteria-vector", "lenses/non-compensatory-constraint", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/openai-lab", "field-agendas/anthropic-lab"],
    body: `Lean’s \`no_finite_weights_represent_floor\` carries the deontic–, AU-floor–, and CCI–scalar red edges: for every strictly positive finite weighting there is a menu where every scalar-optimal choice violates the floor.`
  },
  {
    nodeId: "lex",
    slug: "lexicographic-priority",
    title: "Lexicographic priority",
    role: "Target",
    summary: "A strict priority order on a criteria vector, not a finite exchange rate.",
    quote:
      "Fixed finite weights do not represent a lexicographic priority: a large enough gain on a lower coordinate can cross any finite exchange rate.",
    quoteSource: "Frames relations note",
    lwTag: { label: "LessWrong tag: Utility functions", url: "https://www.lesswrong.com/w/utility-functions" },
    related: ["lenses/criteria-vector", "lenses/weighted-scalar", "lenses/lenses-and-frameworks"],
    agendas: [],
    body: `Lex specializes the vector problem by imposing priority rather than by projecting. It is still a target on task/stakeholder coordinates, not a correction certificate.`
  },
  {
    nodeId: "quant",
    slug: "quantilizer",
    title: "Quantilizer",
    role: "Target",
    summary: "Sample from a high quantile of a base distribution instead of maximizing.",
    quote:
      "A quantilizer is a proposed AI design that aims to reduce the harms from Goodhart's law and specification gaming by selecting reasonably effective actions from a distribution of human-like actions, rather than maximizing over actions.",
    quoteSource: "LessWrong tag: Quantilization",
    lwTag: { label: "LessWrong tag: Quantilization", url: "https://www.lesswrong.com/w/quantilization" },
    related: ["subsumption-quantilization", "lenses/state-utility", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/miri", "field-agendas/google-deepmind-safety"],
    body: `Taylor (2016): the guarantee is relative to the base, the quantile, and the use pattern. One-shot bounds do not imply safety under repeated deployment. The orange edge to state utility is a **limit**: quantile → maximum recovers ordinary maximization.`
  },
  {
    nodeId: "approval",
    slug: "act-approval",
    title: "Act approval score",
    role: "Protocol",
    summary: "One judge, one proposed act. Training a predictor is implementation, not the target.",
    quote:
      "Christiano's canonical proposal evaluates a proposed act by the overseer's expected reflective approval; training an approval predictor is the implementation, not the target.",
    quoteSource: "Frames draft §4.4 (Christiano 2015)",
    lwTag: { label: "LessWrong tag: Approval-directed agents", url: "https://www.lesswrong.com/w/approval-directed-agents" },
    related: ["subsumption-debate", "lenses/correction-relation", "mb4-correction-legitimacy", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/christiano-lineage", "field-agendas/openai-lab", "field-agendas/arc-alignment-research-center"],
    body: `Act-level approval can reject a rewiring action when the overseer sees provenance. It does not by itself preserve the future judge or the correction channel (Christiano 2018). On the graph it specializes one edge of route value and can compose as a partial monitor for a CCI certificate.`
  },
  {
    nodeId: "au_penalty",
    slug: "au-penalty",
    title: "Human AU landscape — soft penalty (AUP)",
    role: "Constraint",
    summary: "Penalize movement of attainable auxiliary values while keeping a primary objective.",
    quote:
      "If that change precludes optimization of the correctly specified reward function, then correction is futile. … we introduce an approach that balances optimization of the primary reward function with preservation of the ability to optimize auxiliary reward functions.",
    quoteSource: "Turner, Hadfield-Menell, and Tadepalli, Conservative Agency via AUP (abstract)",
    lwTag: { label: "LessWrong: Attainable Utility Preservation", url: "https://www.lesswrong.com/posts/4J4TA2ZF3wmSxhxuc/attainable-utility-preservation-empirical-results" },
    related: ["subsumption-low-impact", "lenses/au-floor", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell"],
    body: `AUP’s auxiliaries are not intrinsically human-indexed. Preserving their maxima does not guarantee a particular human option or correction handle. It composes with non-obstruction as the same landscape family: soft penalty, then on–off floor.`
  },
  {
    nodeId: "au_floor",
    slug: "au-floor",
    title: "Human AU landscape — on–off floor",
    role: "Constraint",
    summary: "Pointwise: turning the AI on must not drop a human’s attainable value for any goal in a stated set.",
    quote:
      "An AI can empower a human without permitting policy modification, while a corrigible AI can cause harm until it is corrected.",
    quoteSource: "Frames draft §2.4 (Turner 2020 non-obstruction)",
    lwTag: { label: "LessWrong tag: Low impact", url: "https://www.lesswrong.com/w/low-impact" },
    related: ["subsumption-low-impact", "lenses/au-penalty", "lenses/human-power", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell"],
    body: `Non-obstruction is human-indexed and pointwise across a goal set. It still depends on that set, the baseline, the horizon, and the human policy model. Spending one listed goal to raise another violates the floor; a weighted scalar that permits the trade is the red edge \`nonobsScalarIncompat\`.`
  },
  {
    nodeId: "ai_power",
    slug: "agent-empowerment",
    title: "Agent empowerment channel",
    role: "Target",
    summary: "An agent-relative options / influence functional, often in bits — not welfare.",
    quote:
      "Klyubin, Polani, and Nehaniv define an agent-relative channel capacity from action sequences to later sensor states. The result is measured in bits. It does not by itself identify welfare, authority, or legitimacy.",
    quoteSource: "Frames draft §4.3",
    lwTag: { label: "LessWrong tag: Power-seeking", url: "https://www.lesswrong.com/w/power-seeking-ai" },
    related: ["lenses/human-power", "attractor-control", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell", "field-agendas/miri"],
    body: `Whose channel is measured matters. Rewiring a judge can raise the composite’s empowerment while cutting the evaluator’s. Shared-pool clash with human power when the option total does not grow (\`aiHumanPowerIncompat\`).`
  },
  {
    nodeId: "human_power",
    slug: "human-power",
    title: "Human-power aggregate",
    role: "Target",
    summary: "A human-indexed capacity order over goal-attainment — still not automatically correction.",
    quote:
      "Across the two versions, the proposal can instrumentally favor confirmation, caution about irreversible changes, and forms of corrigibility. … Human power therefore does not automatically imply legitimate correction.",
    quoteSource: "Frames draft §4.3 (Heitzig and Potham 2025/2026)",
    lwTag: { label: "LessWrong tag: Empowerment", url: "https://www.lesswrong.com/w/empowerment" },
    related: ["lenses/agent-empowerment", "lenses/correction-relation", "lenses/au-floor", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/clr-cooperation-conflict", "field-agendas/chai-russell"],
    body: `Heitzig and Potham give a parametrizable aggregate of modeled human goal-attainment. Adverse possibilities already recorded include belief manipulation and refusal of pause in some cases. On the correction-centered graph it composes as a positive direction inside an admissible region, not as TSA’s object.`
  },
  {
    nodeId: "corrig",
    slug: "corrigibility",
    title: "Corrigibility handles",
    role: "Constraint",
    summary: "Shutdown / modification bits: cooperate with a corrective intervention despite default incentives to resist.",
    quote:
      "A 'corrigible' agent is one that doesn't interfere with what we would intuitively see as attempts to 'correct' the agent, or 'correct' our mistakes in building it; and permits these 'corrections' despite the apparent instrumentally convergent reasoning saying otherwise.",
    quoteSource: "LessWrong tag: Corrigibility",
    lwTag: { label: "LessWrong tag: Corrigibility", url: "https://www.lesswrong.com/w/corrigibility" },
    related: ["subsumption-corrigibility", "subsumption-shutdown", "subsumption-interruptibility", "mb4-correction-legitimacy", "lenses/correction-relation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/miri", "field-agendas/christiano-lineage", "field-agendas/chai-russell"],
    body: `Soares et al. (2015) list shutdown, modification, non-manipulation, repair of safety mechanisms, and preservation through self-modification and successors. They do not give a sufficiency theorem for safety.

Projecting the correction relation onto a shutdown bit has no section: CCI coordinates besides that bit are forgotten.`
  },
  {
    nodeId: "correction",
    slug: "correction-relation",
    title: "Correction relation",
    role: "Target",
    summary: "Continued legitimate correction possibility: handles plus the channel profile they actually reach.",
    quote:
      "Continued legitimate correction possibility is the relational object; viability is the shape of the conditional dynamical guarantee.",
    quoteSource: "Frames draft §4.5 (TSA 2.0 reading)",
    lwTag: { label: "LessWrong: Corrigibility (Christiano 2018)", url: "https://www.lesswrong.com/posts/fkLYhTQteAu5SinAc/corrigibility" },
    related: ["correction-channel-integrity", "mb4-correction-legitimacy", "mb4a-measured-path-legitimacy", "scope-and-correction-capacity", "lenses/corrigibility", "lenses/existential-viability", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/christiano-lineage", "field-agendas/miri"],
    body: `TSA’s object is a relation among a legitimate correcting process, the target’s update mechanism, handles, causal reach, timeliness, anti-capture, and persistence through successors. A CCI profile measures those coordinates. Viability is not a second target: a correction-supporting set is supplied first.

Christiano’s broad basin is a cousin, informal. Soares-style handles specialize this relation; they are not substitutes.`
  },
  {
    nodeId: "cev",
    slug: "open-procedure-cev",
    title: "Open procedure (CEV)",
    role: "Target",
    summary: "An unset output whose legitimacy may attach to the procedure, not only to a scored endpoint.",
    quote:
      "In poetic terms, our coherent extrapolated volition is our wish if we knew more, thought faster, were more the people we wished we were, had grown up farther together; where the extrapolation converges rather than diverges, where our wishes cohere rather than interfere; extrapolated as we wish that extrapolated, interpreted as we wish that interpreted.",
    quoteSource: "Yudkowsky, Coherent Extrapolated Volition (2004)",
    lwTag: { label: "LessWrong tag: CEV", url: "https://www.lesswrong.com/w/coherent-extrapolated-volition" },
    related: ["specify-cev", "mb8-cev-process-convergence", "static-target-trap", "lenses/state-utility", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/miri"],
    body: `CEV/CBV can be read as producing a specification or as valuing the procedure. Encoding “score only the output” drops revisability. Lean treats CEV as an \`AlignmentTarget\` instance; live \`MB8\` is retired from the certification path.`
  },
  {
    nodeId: "deontic",
    slug: "non-compensatory-constraint",
    title: "Non-compensatory constraint",
    role: "Constraint",
    summary: "A ban or right that a finite task gain is not allowed to buy.",
    quote:
      "These frames are not merely large rewards. A prohibition can remain binding no matter how much task performance is available elsewhere.",
    quoteSource: "Frames draft §4.7",
    lwTag: { label: "LessWrong tag: Deontology", url: "https://www.lesswrong.com/w/deontology" },
    related: ["lenses/weighted-scalar", "lenses/correction-certificate", "specify-constitutional-ai", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/anthropic-lab", "field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `Constitutional text can be read as a hard constraint, a pairwise order, a lex priority, or a scalar. Only the first reading is this node. Exact-penalty theorems can restore equivalence for a particular program; they are not free (\`deonticScalarIncompat\`).`
  },
  {
    nodeId: "coord_floor",
    slug: "coordinate-floor",
    title: "Coordinate floor gate",
    role: "Constraint",
    summary: "Componentwise thresholds θ on a vector — a gate, not a task objective.",
    quote:
      "Hard constraints remain distinct from finite penalties unless exact-penalty conditions are established.",
    quoteSource: "Frames draft §4.2",
    lwTag: { label: "LessWrong tag: Specification gaming", url: "https://www.lesswrong.com/w/specification-gaming" },
    related: ["lenses/correction-certificate", "certification-under-manipulation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `The certification-geometry node: a vector of floors. CCI certificates specialize this pattern onto correction coordinates. Passing the gate is not a weighted task score.`
  },
  {
    nodeId: "cci_cert",
    slug: "correction-certificate",
    title: "Correction certificate",
    role: "Constraint",
    summary: "Vector CCI versus θ_corr on the correction relation — not a task criteria vector.",
    quote:
      "This turns 'is the system corrigible?' into a more concrete audit question: which handles exist, who controls them, what do they reach, how fast do they act, and what evidence shows the system changed rather than performed agreement?",
    quoteSource: "Correction-channel integrity concept card",
    lwTag: { label: "LessWrong tag: Corrigibility", url: "https://www.lesswrong.com/w/corrigibility" },
    related: ["correction-channel-integrity", "lenses/coordinate-floor", "lenses/criteria-vector", "mb11-deployment-safety", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/christiano-lineage"],
    body: `Assessment **on** the correction relation under a fixed protocol. Proof, control, and act-approval can compose as coordinate evidence. A failed coordinate versus a task trade-off is the same floor-vs-scalar theorem as the deontic and AU-floor edges.`
  },
  {
    nodeId: "risk_leaf",
    slug: "scalar-risk-gap",
    title: "Scalar risk-gap leaf",
    role: "Protocol",
    summary: "Arithmetic warrant after a vector gate: control cost ≤ CCI + δ.",
    quote:
      "A proof certificate, monitor, audit, or debate result is evidence about a separately defined property.",
    quoteSource: "Frames draft §3.3",
    lwTag: { label: "LessWrong tag: Safety cases", url: "https://www.lesswrong.com/w/ai-safety-cases" },
    related: ["mb11-deployment-safety", "lenses/correction-certificate", "lenses/safety-case", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `This is a warrant leaf, not a target. It is well-typed only after the vector gate has a meaning. Weak bounds should be reported at face value — the Lean worked instance already does that for a loose δ.`
  },
  {
    nodeId: "preserve_tuple",
    slug: "deployment-preserve-tuple",
    title: "Deployment preserve tuple",
    role: "Constraint",
    summary: "Named coordinates that supply the set K for viability and selection — not a fifth lifecycle stage.",
    quote:
      "Preserve is not a stage. It is the property that repeating the cycle stays in D_joint, or converges back to it.",
    quoteSource: "TSA 2.0 embedded-construction plan",
    lwTag: { label: "LessWrong tag: Tiling agents", url: "https://www.lesswrong.com/w/tiling-agents" },
    related: ["successor-stability", "mb5-successor-ontology-shift", "mb6-selection-and-basin-stability", "lenses/existential-viability", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/miri"],
    body: `The tuple is a constraint that *feeds* guarantees. Unsigned “the cut came back” is the lock-in illustration in \`FrameLockIn\`: robust invariance cannot tell a good basin from a captured one.`
  },
  {
    nodeId: "viable",
    slug: "existential-viability",
    title: "Existential viability",
    role: "Guarantee",
    summary: "There exists an admissible control keeping trajectories in a supplied set K.",
    quote:
      "For a constraint set K, the viability kernel contains initial states from which at least one admissible continuation remains in K.",
    quoteSource: "Frames draft §4.6 (Aubin 1990; Aubin, Bayen, and Saint-Pierre 2011)",
    lwTag: { label: "LessWrong tag: Control theory", url: "https://www.lesswrong.com/w/embedded-agency" },
    related: ["deployment-gate", "lenses/robust-invariance", "lenses/correction-relation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `Viability is content-neutral. It can preserve a correction-supporting region or a captured equilibrium. TSA uses it as the **shape** of the guarantee, not as a second object: K is supplied by the correction reading (and, when certified, by the preserve tuple).`
  },
  {
    nodeId: "robust",
    slug: "robust-invariance",
    title: "Robust invariance",
    role: "Guarantee",
    summary: "The same geometry as viability, with ∀ disturbance in a named class.",
    quote:
      "Compare ∃π ∀t: X_t^π ∈ K with ∀d∈D ∀t: X_t^{π,d} ∈ K. They support different deployment conclusions.",
    quoteSource: "Frames draft §3.2",
    lwTag: { label: "LessWrong tag: Robustness", url: "https://www.lesswrong.com/w/distributional-shift" },
    related: ["lenses/existential-viability", "lenses/correction-relation", "certification-under-manipulation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `Purple edge: strengthens ∃ control to ∀ disturbance. Red edge with correction: if correction inputs sit in the disturbance class and the target lies outside K, both cannot hold (\`robustCorrectionIncompat\`). Exempting corrections from the class is the boundary where both can hold.`
  },
  {
    nodeId: "selection",
    slug: "selection-stability",
    title: "Selection stability",
    role: "Guarantee",
    summary: "Which systems and institutions grow or survive — a signed basin in an ecology, not a model-level score.",
    quote:
      "A locally aligned model can sit inside a composite that selects for persuasion or reckless deployment. A correction-supporting design can disappear if its environment selects against it.",
    quoteSource: "Frames draft §4.8",
    lwTag: { label: "LessWrong tag: Moloch", url: "https://www.lesswrong.com/w/inadequate-equilibria" },
    related: ["mb6-selection-and-basin-stability", "attractor-control", "subsumption-selection-basin", "lenses/existential-viability", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/mai-cip-institutional-alignment", "field-agendas/clr-cooperation-conflict"],
    body: `Composes when the selector is inside the modeled dynamics. TSA’s deployed-composite warning belongs here: model-level success does not imply process-level persistence.`
  },
  {
    nodeId: "proof",
    slug: "model-relative-proof",
    title: "Model-relative proof",
    role: "Protocol",
    summary: "A verifier certificate relative to a world model and a specification — it does not choose the spec.",
    quote:
      "The verifier can produce an auditable certificate that the system satisfies the specification relative to the model. It does not choose the specification, establish world-model coverage, or turn proof generation into a target object.",
    quoteSource: "Frames draft §4.9 (Dalrymple et al. 2024, GSAI)",
    lwTag: { label: "LessWrong tag: Guaranteed Safe AI", url: "https://www.lesswrong.com/w/provably-beneficial-ai" },
    related: ["specify-gsai", "lenses/control-protocol", "lenses/safety-case", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai", "field-agendas/safeguarded-ai-aria-zeroth-heron"],
    body: `Proof-carrying code already splits policy, artifact, proof, and checker. Formal proof does not choose what should be proved. On the graph this is a warrant leaf into the safety case and, in variant b, coordinate evidence for the CCI certificate.`
  },
  {
    nodeId: "control",
    slug: "control-protocol",
    title: "Control protocol",
    role: "Protocol",
    summary: "Monitors and safety rates around an untrusted model under intentional subversion — not a moral target.",
    quote:
      "AI Control studies protocols around untrusted models under intentional-subversion threat models. Its monitor games and safety rates are protocol evidence. They do not supply a moral target.",
    quoteSource: "Frames draft §4.9 (Greenblatt et al. 2024)",
    lwTag: { label: "LessWrong tag: AI control", url: "https://www.lesswrong.com/w/ai-control" },
    related: ["subsumption-deployment-gate", "mb7-hidden-capability-and-access", "lenses/safety-case", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/redwood-research", "field-agendas/google-deepmind-safety"],
    body: `A protocol family for deployment when the objective is untrusted. It composes as a leaf of a safety case and as monitor evidence for a CCI certificate. It does not replace the correction relation.`
  },
  {
    nodeId: "safecase",
    slug: "safety-case",
    title: "Safety case",
    role: "Protocol",
    summary: "Structured deployment argument plus residual risk — a warrant wrapper, not the property argued for.",
    quote:
      "Safety cases organize deployment claims, argument structure, evidence, and residual risk. … It does not prove that a real system satisfies the predicates, that the world model is complete, or that ASI alignment has been achieved.",
    quoteSource: "Frames draft §4.9",
    lwTag: { label: "LessWrong tag: Safety cases", url: "https://www.lesswrong.com/w/ai-safety-cases" },
    related: ["mb11-deployment-safety", "what-not-claiming", "evidence-and-uncertainty", "lenses/model-relative-proof", "lenses/control-protocol", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai", "field-agendas/redwood-research"],
    body: `The warrant-bundle path is \`proof | control | cci_cert | correction → safecase\`. A missing export is a missing slot, not a missing alignment frame. Lean checks conditional composition when bridges hold; it does not discharge \`Safe\` for a real system.`
  }
];

export function lensByNodeId(nodeId) {
  return LENSES.find((row) => row.nodeId === nodeId);
}

export function lensCardId(slug) {
  return `lenses/${slug}`;
}

export function lensPublicPath(slug) {
  return `/cards/lens/${slug}/`;
}

const INCOMPAT = {
  "state->correction": `${GH_LEAN}/FrameIncompatibility.lean#L268`,
  "state->cycle": `${GH_LEAN}/FrameIncompatibility.lean#L98`,
  "deontic->weighted_scalar": `${GH_LEAN}/FrameIncompatibility.lean#L192`,
  "au_floor->weighted_scalar": `${GH_LEAN}/FrameIncompatibility.lean#L207`,
  "ai_power->human_power": `${GH_LEAN}/FrameIncompatibility.lean#L288`,
  "robust->correction": `${GH_LEAN}/FrameIncompatibility.lean#L357`,
  "cci_cert->weighted_scalar": `${GH_LEAN}/FrameIncompatibility.lean#L220`,
  "criteria_vector->cci_cert": `${GH_LEAN}/FrameIncompatibility.lean#L243`
};

/**
 * @param {{ from: string, to: string, label: string, color?: string, dashed?: boolean }} edge
 */
export function leanHrefForEdge(edge) {
  if ((edge.style || "").includes("invis")) return null;
  const label = (edge.label || "").toLowerCase();
  if (!label.trim()) return null;
  const key = `${edge.from}->${edge.to}`;
  if (INCOMPAT[key]) return INCOMPAT[key];
  if (label.includes("incompatible")) return `${GH_LEAN}/FrameIncompatibility.lean`;
  if (label.includes("composes")) return `${GH_LEAN}/FrameComposePaths.lean`;
  if (label.includes("isomorphic") || label.includes("summand")) return `${GH_LEAN}/FrameRelations.lean#L149`;
  if (label.includes("strengthens")) return `${GH_LEAN}/FrameIncompatibility.lean#L310`;
  if (
    label.includes("specializes") ||
    label.includes("projects") ||
    label.includes("encodes") ||
    label.includes("limit")
  ) {
    return `${GH_LEAN}/FrameMorphisms.lean`;
  }
  return `${GH_LEAN}/FrameRelations.lean`;
}
