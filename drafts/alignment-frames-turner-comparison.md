# Alignment frames compared with Turner's power-seeking results

Companion to [alignment-frames-relations.md](alignment-frames-relations.md) and [state-utility-in-practice.md](state-utility-in-practice.md).

Sources: Turner, Smith, Shah, Critch, and Tadepalli, [Optimal Policies Tend to Seek Power](https://arxiv.org/abs/1912.01683) (NeurIPS 2021, "T21"); Turner and Tadepalli, [Parametrically Retargetable Decision-Makers Tend To Seek Power](https://arxiv.org/abs/2206.13477) (NeurIPS 2022, "T22"). Section and theorem numbers are from the arXiv versions. The quotes were checked against the extracted text.

## The main difference

Turner counts. Each of his results fixes the environment and counts, over the permutation orbit of a utility or reward parameter, how many parameter settings make one choice optimal (T21 Def 6.5; T22 Def 3.2). We fix the utility and prove a limit, a representation, or an incompatibility. The graph has no node for "a distribution over objectives".

So most overlaps are the same object seen two ways. He asks which choice most objectives favour. We ask what a given objective can express and what it accepts.

One consequence is easy to miss. Turner's "state-based reward" is a per-step reward `R(s)` summed along the path. In our graph that is a **route value**, not a state utility: staying in a rewarded state pays every step, so a round trip has value (`markov_reward_not_state_utility`). His average-reward results live on the **cycle** summand, which is why his outcomes are recurrent state distributions and not states.

## The shared frame

The mapping works because both sides talk about the same object: a **decision problem**. It has four parts:

- an outcome set `O`: states, trajectories, records, or menus of criteria vectors;
- a menu `C` of what the agent can bring about;
- an objective parameter `θ`: a utility, reward, or weights;
- a decision rule `f(C, θ)`: argmax, quantilizer, satisficer, or weighted scalar.

T22 states this explicitly. A decision-making function maps a set of options and a parameter to a choice probability. Our `Incompatibility` carriers are of the same shape, for example `(menu, choice)`, or the utility itself in `hstateCorrectionIncompat`.

The two programs use different parts of it:

- **Turner** studies the **symmetries of one decision problem**: permutations of `O` acting on `θ`. He counts how many parameters in an orbit favour one part of the menu. His quantifier is "most θ".
- **We** study **maps between decision problems**. Encode, project, and specialize are maps `O → O'` with a pullback of parameters. An incompatibility is a statement "for all (C, θ) in a class H" plus a boundary witness. Our quantifiers are ∀ and ∃.

A permutation is a map from a decision problem to itself, so his tools are a special case of ours. Our morphisms are the general case.

**Should we use the frame directly?** For the Scores cluster and for correction viewed as a decision, yes. A small Lean structure (finite `O`, menu, parameter, rule) would give three things:

- It would supply the missing `mapId` functions and commuting squares: a map `g : O → O'` should satisfy `f(θ' ∘ g, C) = g⁻¹(f(θ', g C))` where the edge claims it.
- It would state Turner's counting next to our ∀/∃ results on the same objects.
- It is needed for the Lean candidates below.

For Guarantees and Warrants, no: viability, robustness, proofs, and safety cases are about dynamics and evidence, not choice from a menu, and forcing them into the frame would hide that. The recommended scope is a new module that re-expresses argmax, quantilizer, weighted scalar, and record utilities, proves one commuting square (`state → hstate`), and one counting result (candidate 1).

## Coverage

| Turner procedure | What is proved | Our node | Our Lean | Verdict |
| --- | --- | --- | --- | --- |
| Discounted per-step state reward, optimal policy (T21 Def 4.1, Prop 6.9) | Keeping options open tends to be optimal | `route` (edge reward `R(target)`) | `markov_reward_not_state_utility` | Different representation: we classify the objective type, he counts over its orbit |
| Average-optimal, outcomes = recurrent state distributions (T21 Thm 6.13, Cor 6.14; T22 Thm D.11) | Agents tend to end in larger RSD sets | `cycle` | `stateCycleIncompat`, `gradient_closed_walk_zero` | Different representation: our state–cycle edge explains why his outcomes are cycles |
| Limits of optimal policy sets as γ→0, γ→1 (T21 Def 4.1, Lemma E.35) | The limits exist | none | nothing | Turner only |
| POWER (T21 Def 5.2, Props 5.4–6.12) | States with more options have more POWER for most rewards | `ai_power` | `aiHumanPowerIncompat` (option counts) | Different representation: our counts are close to the information-theoretic empowerment he argues against (T21 App. A) |
| POWER under a bounded planner (T21 Def C.1); POWER-seeking vs optimality (T21 Props B.1, B.4) | Power grows with planner quality; more POWER does not imply higher optimality probability | `ai_power` | nothing | Turner only |
| Shutdown avoidance (T21 §6.3) | "average-optimal policies tend to avoid shutdown" | `corrig`, `correction` | `soares_prevention_incentive`, `soares_button_neutrality_iff` (`Field.Finite.ShutdownIncentives`), `hstateCorrectionIncompat` | Different representation: he shows a majority over the orbit; we show that every fixed utility accepts correction only on ties |
| Disempowering other agents (T21 §7) | Open: "We do not yet formally understand if, when, or why POWER-seeking policies tend to disempower other agents" | `human_power`, edge `ai_power–human_power` | `aiHumanPowerIncompat` | Ours only, for the zero-sum case |
| Orbits and n-fold retargetability (T22 Defs 3.1–3.5, Thm 3.6, Def A.7) | A retargetable decision rule favours the larger option set for most parameters | none | nothing | Turner only |
| Expected-utility decision rules over outcome lotteries (T22 Def A.1, Thm A.13) | Every rule that depends only on expected utility is retargetable | `dist` | edge only | Different representation |
| Rational, Boltzmann, best-of-k, satisficing (T22 Prop A.11 items 1–6) | Same orbit tendency | `state` (argmax) for item 1, none for the rest | `argmaxSet` (definition only) | Turner only |
| Quantilizer (T22 A.11 item 7, Def B.12; Conj B.13) | Proved for a **uniform** base; conjectured for any base with "min_{b∈B} P(b) ≥ max_{a∈A} P(a)" | `quant` | `quantilizer_limit_is_argmax`, `quantilizer_never_argmax_without_base_mass` | Different representation: he fixes q and counts utilities; we fix the utility, take the q-limit, and show base mass is needed |
| Greedy action-level reward (T22 §4.1) | Retargetable over actions; he calls this "less concerning" (§6.2) | `approval` | nothing | Different representation |
| Reward on the final observation, Montezuma's Revenge (T22 §4.2, Prop C.4) | More screens and inventories after leaving the room, so leaving is favoured | `hstate` (the observation carries score and inventory) | `state_utility_lifts_to_records`, `record_utility_not_state` | Different representation: here a richer record **strengthens** the tendency, because it multiplies outcomes |
| Featurized reward over item counts (T22 §4.3, Prop C.9) | Most weightings leave the first room | `weighted_scalar` | `no_finite_weights_represent_floor` | Different representation: he permutes weights; we show fixed weights cannot represent a floor |
| Learned RL policies (T22 §4.3, §5.2) | Semi-formal: better exploration gives more retargetability | none | nothing | Turner only |
| Corrigibility to a new policy, final-state reward (Turner 2021 [corrigibility post](https://www.lesswrong.com/posts/WCX3EwnWAx7eyucqH)) | Reward blind to correction status: strict corrigibility impossible, weak corrigibility to all corrections iff reward constant. Reward sees status: corrigible but manipulates into correction. Counting: strictly corrigible for at most 1/(n+1) of permutations | `state`, `hstate`, `correction` | `soares_button_neutrality_iff`, `hstateCorrectionIncompat` | Both, his first. We add the channel bit as a third record type and the measurement consequence |
| Utilities over observation vs action-observation histories (Turner 2021 [power-seeking post](https://www.lesswrong.com/posts/hzeLSQ9nwDkPc4KNt)) | Observation histories: tendency very strong. Action-observation histories, deterministic: tendency disappears ("random twitching") | `hstate` | nothing | Turner only. Shows that what the record holds decides whether counting applies |
| Trajectories as outcomes (T22 App. A) | One sentence ("Each outcome could be … a trajectory"); no trajectory-specific theorem | `hist`, `hstate` | `FrameHistoryState` | Different representation |

Not in either paper: `exact` as a summand, Pareto `criteria_vector`, `lex`, `deontic`, `cev`, `viable`, `robust`, `selection`, and the warrant nodes. AUP (`au_penalty`, `au_floor`) appears only as a reference. Correction appears only as shutdown, a terminal state, not as a relation with a channel.

## Candidates for Lean

These are ranked by value. All fit our style: finite carriers, integers, and `decide` or `omega`, with no measure theory.

1. **Correction records under orbit counting.** Suppose disabling the channel leads to n distinct records and accepting the correction leads to one. Then for any injective record utility, at least n times as many permutations make a disabled record optimal as make `recCorrected` optimal. If accepting the correction also branches into n records, the counts are equal. This joins our `hstate`–correction edge to his shutdown-avoidance result and says which record design removes the tendency.
2. **Small cases of Conjecture B.13** (quantilizers with a non-uniform base): d = 3, A = {0}, B = {1, 2}, natural-number base weights with min over B ≥ max over A. Either `decide` proves the orbit inequality, or it finds a counterexample to an open conjecture.
3. **Record refinement multiplies copies.** If B contains n copies of A and each B-outcome splits into k records, B contains n·k copies. This is the mechanism of his Montezuma's Revenge result, stated through our `state → hstate` edge.
4. **Orbit-sum POWER on a shared pool.** If agent and human option sets partition a fixed pool, a rise in the agent's orbit-sum POWER forces the human's to weakly fall. This replaces the option counts in `aiHumanPowerIncompat` with a POWER-like quantity and answers T21 §7 for the zero-sum case only.
5. **Quantilizer at the smallest quantile is the rational rule.** This is a corollary of `quantilizer_limit_is_argmax`: T22's item 7 reduces to item 1, a finite instance of his §6.2 limit remark.

Done:
- Turner's objective is a route value (`markov_reward_not_state_utility`).
- The shared frame as Lean (`FrameDecision`): map functions, commuting squares, and orbit counts on his corrigibility example (`turner_corrigible_quarter`, `option_preserving_correction_half`), next to the ∀ form (`subset_branch_never_strictly_better`). The general argmax form of n-fold retargetability is proved for every objective (`copies_count_le`), with the corrigibility corollary `correction_avoided_card_fold`. Still open from the list: Conjecture B.13 cases, record refinement multiplying copies, orbit-sum POWER on a shared pool.

## What this changes in our graph

- The `ai_power` node measures options by counting. Turner argues for POWER (average optimal value) instead. The edge label and card should say which measure is meant.
- The instrumental-convergence premise is a per-step reward on the bare state, accumulated, plus a count over objectives. It is neither our endpoint `state` utility nor a record utility. [state-utility-in-practice.md](state-utility-in-practice.md) uses this.
