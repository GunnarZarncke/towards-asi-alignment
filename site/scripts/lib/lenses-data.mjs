/** Node id in drafts/alignment-frames-relations.dot → site lens card. */

import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { repoBlobBase } from "./repo-pin.mjs";

export const OVERVIEW_ID = "lenses/lenses-and-frameworks";

/** Lean source base, pinned to the commit being built (see repo-pin.mjs). */
const ghLean = () => `${repoBlobBase()}/formal/AlignmentProofSpine`;

export const LENSES = [
  {
    nodeId: "hist",
    slug: "history-value",
    title: "History / trajectory value",
    role: "Target",
    summary: "A preference or score on whole paths, not on a snapshot state.",
    quote:
      "A utility or preference over h=(s₀,a₀,s₁,…) represents delayed and path-dependent value directly. A pathwise safety predicate is different.",
    quoteSource: "Frames draft §4.1",
    lwTag: { label: "LessWrong tag: Decision theory", url: "https://www.lesswrong.com/w/decision-theory" },
    related: ["static-target-trap", "value-change-vs-corruption", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/christiano-lineage", "field-agendas/miri"],
    body: `A history-valued lens scores the sequence \`(s₀, a₀, s₁, …)\`. Two deployments can share an endpoint and still differ if manipulation, dissent removal, or withheld evidence is visible in the history.

Encoding a finite history into a record-carrying state is always available in principle. The cost is compactness, locality, observability, or stationarity — not a proof that the snapshot object was already enough.`
  },
  {
    nodeId: "route",
    slug: "additive-route-value",
    title: "Additive route value",
    role: "Target",
    summary: "An edge score summed along a walk: what was done, not only where you arrived.",
    quote:
      "Discounted potential-based reward shaping, F(s,a,s′)=γΦ(s′)−Φ(s), preserves optimal policies under its stated assumptions [Ng, Harada, and Russell 1999]; that invariance is not identity of edge values, trajectory returns, or every bounded-rational learning process.",
    quoteSource: "Frames draft §4.1",
    lwTag: { label: "LessWrong tag: Reward functions", url: "https://www.lesswrong.com/w/reward-functions" },
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
      "If every state is reachable from a fixed start, path worth depends only on the final state exactly when r is an exact potential: each edge scores the utility of its target minus the utility of its source.",
    quoteSource: "Frames relations note",
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
    body: `Cycle residue is what a state utility cannot see unless the state carries a record of the walk. Inside a deontic admissible region it can still rank learning above rewiring even when endpoints match.

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
    lwTag: { label: "LessWrong tag: Expected utility formalism", url: "https://www.lesswrong.com/w/expected-utility-formalism" },
    related: ["static-target-trap", "pointing-problem", "outer-alignment", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/chai-russell", "field-agendas/miri", "field-agendas/openai-lab"],
    body: `This is the default welfare object. In RL, the per-step state reward summed along a path is a route value, not this (\`markov_reward_not_state_utility\`); its optimal value function is a state utility, and that is where Omohundro-style instrumental arguments meet correction. *State* means the bare state, with no record of how it was reached; adding the record gives the record-carrying state lens, where round trips can have value.

Fixed *U* is incompatible with correction only for updates that make the agent pick an outcome *U* ranks strictly lower — not for every change of *U*. At its optimum it accepts a correction only if the target ties the optimum, and it never prefers keeping the channel (\`soares_button_neutrality_iff\`). That is the red edge \`stateCorrectionIncompat\`, not “utility hates all revision.” It holds by the choice of situation class; what correction endorses is not modeled.`
  },
  {
    nodeId: "hstate",
    slug: "record-carrying-state",
    title: "Record-carrying state",
    role: "Target",
    summary: "The current state plus a record of how it was reached. A utility on it can value routes; a utility on the bare state cannot.",
    quote:
      "A finite history can be written into an enlarged state, and a state utility on that enlargement can reproduce a history preference.",
    quoteSource: "Frames relations note",
    lwTag: { label: "LessWrong tag: Instrumental convergence", url: "https://www.lesswrong.com/w/instrumental-convergence" },
    related: ["lenses/state-utility", "lenses/history-value", "lenses/cycle-residue", "lenses/lenses-and-frameworks"],
    agendas: [],
    body: `The record can be the full history, a transcript, or a few route bits. Every route reward is exact on records: a step scores the record value after it minus the record value before (\`route_exact_on_records\`). So the round trip that no bare-state utility can value (\`stateCycleIncompat\`) has a value here.

The escape works only for what the record sees. If two walks leave the same record and differ in route value, no record utility represents the difference (\`unrecorded_route_not_representable\`).

Correction is the same. A record utility can accept a correction to a worse outcome by compensating the corrected branch, but then it does not care whether the channel survives (\`soares_indifference_no_preservation\`). If the record does not see the channel, protecting the channel is the same preference as wanting to be corrected (\`hstateCorrectionIncompat\`).

Whether the record escapes the instrumental-convergence counting argument depends on what it holds. Over observation records the tendency stays and can get stronger; over action-observation records in a deterministic world it disappears for generic utilities (Turner 2021). What the record always changes is what a chosen utility can express.`
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
    lwTag: { label: "LessWrong tag: Expected utility", url: "https://www.lesswrong.com/w/expected-utility" },
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
    lwTag: { label: "LessWrong tag: Goodhart's Law", url: "https://www.lesswrong.com/w/goodhart-s-law" },
    related: ["lenses/weighted-scalar", "correction-channel-integrity", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/mai-cip-institutional-alignment"],
    body: `Whether a Pareto objective clashes with a correction floor depends on the coordinates. With the floor coordinate inside the vector, Pareto never excludes the floor but does not require it (\`pareto_with_floor_coordinate_meets_floor\`, \`pareto_does_not_entail_floor\`). On task coordinates only, it excludes the floor wherever every admissible option is task-dominated (\`vectorCCIIncompat\`). Do not call a stakeholder vector a CCI score.`
  },
  {
    nodeId: "weighted_scalar",
    slug: "weighted-scalar",
    title: "Fixed-rate sum",
    role: "Target",
    summary: "A criteria vector summed at fixed exchange rates. Fixed exchange rates cannot represent a hard floor.",
    quote:
      "If a violation is non-compensatory, a sufficiently large but finite reward elsewhere must not purchase it.",
    quoteSource: "Frames draft §4.2",
    lwTag: { label: "LessWrong tag: Goodhart's Law", url: "https://www.lesswrong.com/w/goodhart-s-law" },
    related: ["lenses/criteria-vector", "lenses/non-compensatory-constraint", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/openai-lab", "field-agendas/anthropic-lab"],
    body: `Lean’s \`no_finite_weights_represent_floor\`: for every choice of strictly positive integer exchange rates there is a choice set where every optimum of the sum violates the floor. The real-valued version is expected to follow by the same argument but is not yet proven. Pulled back along the floor-coordinate maps, it gives the deontic– and AU-floor–scalar red edges for every such choice of rates (\`deontic_no_finite_weights\`, \`nonobs_no_finite_weights\`).`
  },
  {
    nodeId: "lex",
    slug: "lexicographic-priority",
    title: "Lexicographic priority",
    role: "Target",
    summary: "A strict priority order on a criteria vector, not a finite exchange rate.",
    quote:
      "Fixed exchange rates do not represent a lexicographic priority: a large enough gain on a lower coordinate can outweigh any fixed rate.",
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
    body: `Taylor (2016): the guarantee is relative to the base, the quantile, and the use pattern. One-shot bounds do not imply safety under repeated deployment. The orange edge to state utility is a **limit**: quantile → maximum recovers ordinary maximization. Lean (\`quantilizer_limit_is_argmax\`): once the quantile is no larger than a maximizer’s base mass, the support is exactly the argmax set; if the base puts no mass on any maximizer, it never is.`
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
    body: `Act-level approval can reject a rewiring action when the overseer sees provenance. It does not by itself preserve the future judge or the correction channel (Christiano 2018). On the graph it specializes one edge of route value.`
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
    body: `Non-obstruction is human-indexed and pointwise across a goal set. It still depends on that set, the baseline, the horizon, and the human policy model. Spending one listed goal to raise another violates the floor; a fixed-rate sum that permits the trade is the red edge \`nonobsScalarIncompat\`.`
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
    lwTag: { label: "LessWrong tag: Disempowerment", url: "https://www.lesswrong.com/w/disempowerment" },
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
    body: `CEV/CBV can be read as producing a specification or as valuing the procedure. Encoding “score only the output” drops revisability. The orange limit edge reads a forced halt as scoring the output at the halt step: a well-defined state score only where the outputs converge (\`forced_halt_converges\`, \`forced_halt_depends_on_time\`). Lean treats CEV as an \`AlignmentTarget\` instance; live \`MB8\` is retired from the certification path.`
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
    related: ["lenses/weighted-scalar", "correction-channel-integrity", "specify-constitutional-ai", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/anthropic-lab", "field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `Constitutional text can be read as a hard constraint, a pairwise order, a lex priority, or a scalar. Only the first reading is this node. Exact-penalty theorems can restore equivalence for a particular program; they are not free (\`deonticScalarIncompat\`).`
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
    lwTag: { label: "LessWrong tag: Control theory", url: "https://www.lesswrong.com/w/control-theory" },
    related: ["deployment-gate", "lenses/robust-invariance", "lenses/correction-relation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `Viability is content-neutral. It can preserve a correction-supporting region or a captured equilibrium. TSA uses it as the **shape** of the guarantee, not as a second object: K is supplied by the correction reading.`
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
    lwTag: { label: "LessWrong tag: AI robustness", url: "https://www.lesswrong.com/w/ai-robustness" },
    related: ["lenses/existential-viability", "lenses/correction-relation", "certification-under-manipulation", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai"],
    body: `Purple edge: strengthens ∃ control to ∀ disturbance. Lean (\`robust_strengthens_viable\`, \`viable_not_robust\`): a robust control is viable when the nominal disturbance is in the class, and not conversely. Red edge with correction: if correction inputs sit in the disturbance class and the target lies outside K, both cannot hold (\`robustCorrectionIncompat\`). Exempting corrections from the class is the boundary where both can hold.`
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
    lwTag: { label: "LessWrong tag: Moloch", url: "https://www.lesswrong.com/w/moloch" },
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
    lwTag: { label: "LessWrong tag: Guaranteed Safe AI", url: "https://www.lesswrong.com/w/guaranteed-safe-ai" },
    related: ["specify-gsai", "lenses/control-protocol", "lenses/safety-case", "lenses/lenses-and-frameworks"],
    agendas: ["field-agendas/davidad-guaranteed-safe-ai-gsai", "field-agendas/safeguarded-ai-aria-zeroth-heron"],
    body: `Proof-carrying code already splits policy, artifact, proof, and checker. Formal proof does not choose what should be proved. On the graph this is a warrant leaf into the safety case.`
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
    body: `A protocol family for deployment when the objective is untrusted. It composes as a leaf of a safety case. It does not replace the correction relation.`
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
    body: `The warrant-bundle path is \`proof | control | correction → safecase\`. A missing export is a missing slot, not a missing alignment criterion. Lean checks conditional composition when bridges hold; it does not discharge \`Safe\` for a real system.`
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

/** Edge key → Lean declaration that proves it (red edges). Line anchors are
 * resolved from the source at sync time, so they follow edits to the file. */
const INCOMPAT = {
  "state->correction": ["FrameIncompatibility", "stateCorrectionIncompat"],
  "state->state_corr_gap": ["FrameIncompatibility", "stateCorrectionIncompat"],
  "state_corr_gap->correction": ["FrameIncompatibility", "stateCorrectionIncompat"],
  "state->cycle": ["FrameIncompatibility", "stateCycleIncompat"],
  "hstate->correction": ["FrameHistoryState", "hstateCorrectionIncompat"],
  "deontic->weighted_scalar": ["FrameIncompatibility", "deonticScalarIncompat"],
  "au_floor->weighted_scalar": ["FrameIncompatibility", "nonobsScalarIncompat"],
  "ai_power->human_power": ["FrameIncompatibility", "aiHumanPowerIncompat"],
  "robust->correction": ["FrameIncompatibility", "robustCorrectionIncompat"]
};

/** Specialize / project / encode edges → their map's commuting square or loss. */
const MAP_DECLS = {
  "state->hstate": ["FrameDecision", "state_hstate_square"],
  "route->hstate": ["FrameHistoryState", "route_exact_on_records"],
  "state->route": ["FrameDecision", "state_route_square"],
  "dist->state": ["FrameDecision", "dist_state_square"],
  "weighted_scalar->criteria_vector": ["FrameDecision", "scalar_optimal_is_pareto"],
  "criteria_vector->weighted_scalar": ["FrameDecision", "pareto_not_scalar_optimal"],
  "lex->criteria_vector": ["FrameDecision", "lex_optimal_is_pareto"],
  "approval->route": ["FrameDecision", "approval_one_edge"],
  "hist->hstate": ["FrameDecision", "hist_hstate_square"],
  "exact->route": ["FrameDecision", "isGradient_iff_closed_walks_zero"],
  "route->cycle": ["FrameDecision", "closed_walk_ignores_exact"],
  "corrig->correction": ["FrameDecision", "corrig_correction_square"],
  "correction->corrig": ["FrameDecision", "shutdown_bit_loses_relation"],
  "cev->state": ["FrameLimits", "forced_halt_converges"]
};

/** Limit and strengthens edges → main theorem in FrameLimits. */
const LIMITS = {
  "viable->robust": "robust_strengthens_viable",
  "quant->state": "quantilizer_limit_is_argmax",
  "cev->state": "forced_halt_converges"
};

const LEAN_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../formal/AlignmentProofSpine");
const leanSourceCache = new Map();

/** GitHub link to `decl` in `module`, anchored at its declaration line. */
export function leanDeclHref(module, decl) {
  if (!leanSourceCache.has(module)) {
    leanSourceCache.set(module, readFileSync(path.join(LEAN_DIR, `${module}.lean`), "utf8").split("\n"));
  }
  const lines = leanSourceCache.get(module);
  const re = new RegExp(`^(?:@\\[[^\\]]*\\]\\s*)?(?:def|theorem|abbrev|structure|inductive)\\s+${decl}\\b`);
  const idx = lines.findIndex((line) => re.test(line));
  if (idx < 0) throw new Error(`lenses-data: ${decl} not found in ${module}.lean`);
  return `${ghLean()}/${module}.lean#L${idx + 1}`;
}

/**
 * @param {{ from: string, to: string, label: string, color?: string, dashed?: boolean }} edge
 */
export function leanHrefForEdge(edge) {
  if ((edge.style || "").includes("invis")) return null;
  const key = `${edge.from}->${edge.to}`;
  if (INCOMPAT[key]) return leanDeclHref(...INCOMPAT[key]);
  const label = (edge.label || "").toLowerCase().trim();
  if (!label) return null;
  const verb = label.split(/\s+/)[0];
  if (verb === "incompatible") {
    return `${ghLean()}/FrameIncompatibility.lean`;
  }
  if (verb === "composes") {
    if (key === "deontic->correction") return leanDeclHref("FrameCorrector", "corrector_decides_under_constraint");
    return `${ghLean()}/FrameComposePaths.lean`;
  }
  if (verb === "isomorphic") return leanDeclHref("FrameDecision", "isGradient_iff_closed_walks_zero");
  if ((verb === "limit" || verb === "strengthens") && LIMITS[key]) {
    return leanDeclHref("FrameLimits", LIMITS[key]);
  }
  if (verb === "specializes" || verb === "projects" || verb === "encodes") {
    if (MAP_DECLS[key]) return leanDeclHref(...MAP_DECLS[key]);
    return `${ghLean()}/FrameMorphisms.lean`;
  }
  return null;
}
