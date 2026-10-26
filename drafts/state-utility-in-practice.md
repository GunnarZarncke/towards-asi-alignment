# Which state? Bare-state utility in theory and record rewards in practice

Epistemic status: the formal part is proved in Lean on small carriers. The reading of current training practice is a reading of published setups, not a survey. The remark about long runs is a hypothesis.

Companion to [alignment-frames-relations.md](alignment-frames-relations.md) (nodes `state` and `hstate`). Lean: [`FrameHistoryState.lean`](../formal/AlignmentProofSpine/FrameHistoryState.lean).

## Claim

"Utility on states" means three different things.

1. **A utility on the bare state**: a score for where the world ends up, not how it got there. This is our `state` node. It values every round trip at zero. At its optimum it accepts a correction only if the correction changes nothing it cares about.
2. **A per-step reward on the bare state, summed along the path**: the MDP "state-based reward" of the power-seeking theorems ([Turner et al. 2021](https://arxiv.org/abs/1912.01683)). This is a route value, not a state utility. Staying in a rewarded state pays every step, so round trips can have value (`markov_reward_not_state_utility`). Its optimal value function is again a bare-state utility, so when the agent weighs a correction against its own plan, the rigidity result applies to that value function.
3. **A reward on a record** of the episode.

In language-model training, the state the policy acts on is the context so far. That is a **record** of the episode, so formally every reward there is a state reward and also a trajectory reward. But the rewards actually used read different parts of the record, and most of the weight sits on rewards that read only the outcome.

So the question "does the agent have a state utility?" has no single answer for a trained model. The useful question is: which part of the record does each reward term read, and what does the record leave out?

## Two kinds of state

| Node | What the utility sees | Consequences (Lean) |
| --- | --- | --- |
| `state` (bare) | the current state | Every round trip has value zero (`gradient_closed_walk_zero`), so a route reward with nonzero round-trip value is not a state reward (`stateCycleIncompat`). At its optimum it accepts a correction only if the target ties the optimum, and never strictly prefers keeping the correction channel (`state_accepts_only_ties`). |
| `hstate` (record-carrying) | the current state plus a record of the walk, possibly partial | Every route reward is exact on records (`route_exact_on_records`). The escape needs the record to see the route (`unrecorded_route_not_representable`). |

A bare-state utility is the special case that ignores the record (`state_utility_lifts_to_records`; strict by `record_utility_not_state`).

## Correction on records

The record can hold the correction event, so a record utility is not rigid the way a bare-state utility is. That does not make it corrigible. Take records of (channel kept, correction applied, outcome).

- **Compensation.** A record utility can accept a correction to a strictly worse outcome by scoring the corrected branch at the value of its own optimum. This is the shape of utility indifference. It then has no preference for keeping the channel (`record_accepts_compensated_correction`).
- **Protection is seeking.** If the record does not see the channel, strictly preferring to keep the channel when a correction comes is the same inequality as preferring being corrected to staying at the own optimum. Causing a correction and receiving one leave the same record (`hstateCorrectionIncompat`).
- **Boundary.** Suppose the record also shows whether the correction channel still works. Then the utility can give value to a working channel directly, separate from whether a correction happened. Such an agent protects the channel without wanting to be corrected.

So a utility that reads only "corrected or not" and the outcome has three options. It resists (the bare state), it is indifferent to whether the channel survives (compensation), or it wants to be corrected. The boundary case escapes all three, but only by adding a new thing to score: "the channel works". Someone has to say what that means and measure it, and the agent must not be able to fake the measurement. That is the problem the book calls correction-channel integrity. The record does not solve it. The record only shows where it has to be solved.

### Relation to Turner's 2021 corrigibility post

Most of the decision-theoretic content of this section is already in Turner, ["A Certain Formalization of Corrigibility Is VNM-Incoherent"](https://www.lesswrong.com/posts/WCX3EwnWAx7eyucqH) (2021). An agent is rewarded for its final state and can disable correction at the first step. He splits on whether reward can see the correction status:

- If reward cannot distinguish corrected from uncorrected states, "strict corrigibility is impossible for *any* policy", and an agent is weakly corrigible to every correction "iff R is constant". This is our bare-state case (`state_accepts_only_ties`).
- If it can, strict corrigibility is possible, but if the human would not correct by default, the agent will manipulate the human into correcting it. This is our protection-is-seeking case. He puts it as: "If the agent strictly prefers corrected-states to all non-corrected-states, then *of course* it'll try to get itself corrected!"
- Under counting, "allowing correction will be strictly optimal for at most 1/(n+1) of the permutations of every reward function".
- He suggests penalizing the disable *action* through a per-step reward and calls it "a hacky prohibition", not "a deep solution". He also proposes "corrigibility as functional constraints" as a project.

The disable penalty is our boundary case: the record shows the channel. What we add is an account of why it is hacky, and what it would take to make it less so (next section).

### Relation to Soares et al. 2015

[Soares, Fallenstein, Yudkowsky, and Armstrong (2015)](https://intelligence.org/wp-content/uploads/2024/10/Corrigibility.pdf) study the shutdown problem. An agent has a normal utility `U_N` and a shutdown utility `U_S`. It follows `U_N` unless a button is pressed, and `U_S` plus a correction term if it is. They ask for five things: shut down when pressed, do not prevent the press, do not cause the press, keep the shutdown behaviour in successors and self-modifications, and otherwise maximize `U_N`.

Their results line up with our three options:

| Soares et al. | Our toy |
| --- | --- |
| Theorem 1: if the bonus for the pressed branch is too low, the agent will pay to prevent the press | rigid: rejects the correction |
| Theorem 2: if it is too high, the agent will cause the press | seeks correction |
| Utility indifference sets the bonus so both branches have equal expected utility. Theorem 4: then "there is no cost (no matter how small) that the agent is willing to pay in order to ensure that successor agents obey shutdown commands" (§3, after Theorem 4) | compensation: no preference for keeping the channel |

Their combined utility reads only whether the button was pressed and what happened. In our terms its record does not show the channel, so the middle case is the best it can do. They also find a failure our toy does not model: an indifferent agent acts as if the button will not be pressed and may arrange for bad news to trigger the press ("manage the news", §4.2). Their conclusion is that "it seems possible that no simple combination of `U_N` and `U_S`" satisfies all five desiderata (§5).

What the boundary case adds to Soares et al. is a reason and a direction. The reason: a utility over (pressed, outcome) cannot protect the button without wanting it pressed, because the two preferences are the same inequality on such records. The direction: give the record a channel bit. Soares et al. already name the cost of that direction as a tension between their fourth and fifth desiderata: "What costs (in time and effort) should an agent be willing to expend in order to preserve its shutdown behavior?" Valued too little, the channel is not protected. Valued too much, the agent spends its effort "verifying and reverifying that it could shut down". Treating channel integrity as a constraint rather than a weighted term is one way to avoid choosing a price. It then meets our floor-versus-weights results. That is a hypothesis, not a result here.

## What this does and does not do to instrumental convergence

[Turner et al. 2021](https://arxiv.org/abs/1912.01683) prove their power-seeking results for reward functions on the states of an MDP (Definition 3.5: "For any reward function R ∈ ℝ^S over the state space"). [Turner and Tadepalli 2022](https://arxiv.org/abs/2206.13477) generalize the counting to any outcome set acted on by permutations: "Each outcome could be the visitation of an MDP state, or a trajectory, or the receipt of a physical item" (Appendix A). They also treat reward on the final observation.

Whether moving to records escapes the counting argument depends on what the record holds. Turner's ["Seeking Power is Convergently Instrumental in a Broad Class of Environments"](https://www.lesswrong.com/posts/hzeLSQ9nwDkPc4KNt) (2021) treats both cases:

- **Observation records.** Instrumental convergence "can be extremely strong for utility functions over observation histories". Staying in control leaves many more observation histories than being shut down.
- **Action-observation records.** In a deterministic environment, "Instrumental convergence doesn't exist for utility functions over action-observation histories": every action sequence is its own outcome, so every branch has equally many. The price is that "optimal action will tend to look like random twitching".

A language-model transcript holds the model's own actions (tokens, tool calls) and its observations, so it is an action-observation record. A generic utility over transcripts would show no tendency. The rewards actually used are not generic: most weight sits on outcomes, which is the observation and world-state regime where the tendency is strongest. [Shah 2018](https://www.lesswrong.com/posts/NxF5G6CJiof6cemTw/coherence-arguments-do-not-entail-goal-directed-behavior) shows that every policy is optimal for some utility over histories. That is an existence claim and does not change the count.

Turner's own object is meaning 2 above, a per-step state reward summed along the path, plus a count over rewards. It is neither our endpoint `state` utility nor a record utility. A full comparison of his procedures with our frames is in [alignment-frames-turner-comparison.md](alignment-frames-turner-comparison.md).

What records change is what a **chosen** utility can express: route value, correction events, and with the right record, the channel. The relevant premise is therefore not "state only" but how the utility is picked. Counting assumes something like a permutation-symmetric distribution over utilities. Training picks a specific, structured reward. Turner and Tadepalli discuss featurized rewards for this reason.

## Consequences of the correction result

The correction result above, combined with Turner's counting and the floor theorem, has five consequences. They are arguments on small models, not results about trained systems.

1. **Corrigibility cannot live in the utility alone.** On records that do not show the channel, the only options are resist, ignore the channel, or seek correction. A preference for keeping the channel has to refer to the channel. So any solution contains a measurement of the channel's state, and the agent's incentive turns toward that measurement: making it read "intact" is as good as keeping the channel intact. This gives a decision-theoretic reason for the book's measured-path legitimacy bridge (`MB4a`, including anti-capture), not only a practical one. The "channel bit" of the toy is, in the book, the correction-channel-integrity certificate: a vector of criteria (capacity, latency, manipulation, irreversibility, ontology translation, coercion, dependency, plurality, exit capacity, independence) checked against thresholds (`Correction.CCICertificate`, Chapter 26). So the record that escapes the trilemma is one that carries those coordinates, measured from outside the agent.
2. **A finite channel weight fails at scale.** If keeping the channel is worth a finite amount, some task gain outweighs it. That is `no_finite_weights_represent_floor` applied to the channel coordinate. Turner's counting adds that more capable agents see larger option sets, so the needed gain becomes available. Turner's disable penalty is hacky for this reason, and also because it covers only disabling that the record shows (`unrecorded_route_not_representable`).
3. **So the channel belongs in a constraint, not a reward term.** In our graph this is the green edge `deontic → correction`: an admissible region the task utility cannot trade against. It is also what Turner's "corrigibility as functional constraints" suggests. Chapter 25 (Relation to Corrigibility) already states this in prose: `V_task + λ V_corr` can be traded away, so actions are allowed only if the CCI vector stays above its thresholds. Points 1–3 supply the formal reason (`hstateCorrectionIncompat`, `cci_no_finite_weights`) and the link to Turner and Soares. The Soares et al. tension remains in a narrower form: the constraint must be on the channel's measured state, not on maximizing verification of it.
4. **Correction strength and correction avoidance come together, and avoidance is not the problem by itself.** Under counting, an agent avoids correction because the corrected branch has fewer outcomes: a quarter of the orbit accepts when correction leaves one outcome against three, half when both branches keep two (`turner_corrigible_quarter`, `option_preserving_correction_half`). A correction is useful because it narrows what the agent can do, so the more it constrains, the stronger this pressure. The pressure is harmful only through some routes. Contesting a correction through the channel (objecting, asking for review, giving evidence) leaves the record intact and the decision with the corrector; it can even improve the correction. Avoidance around the channel is the failure: disabling it, hiding actions from it, acting before it can respond, or making the outcome irreversible first. Avoidance through the channel can also fail if it becomes manipulation of the corrector, which Turner names: getting "us to correct it in *just the right way*". These failure routes are the CCI coordinates for manipulation, latency, irreversibility, and coercion. So the target is not "no avoidance" but "avoidance only through the channel, within its thresholds".
5. **Process rewards help when the agent does not write the record they read.** Rewards on the action record move toward Turner's action-observation case, where the generic tendency vanishes, and a process reward against tampering with the record pushes the same way. Baker et al.'s obfuscation result is about the chain of thought, a record the model writes itself. Tool calls, file writes, and environment logs are written by the harness. A process reward on a harness-written record, including a penalty for detected attempts to alter or bypass it, does not reward rewriting one's own record. Two limits remain. Effects the log does not capture are still invisible (`unrecorded_route_not_representable`). And a penalty on *detected* tampering also trains *undetected* tampering wherever detection is imperfect, so detection should rest on mechanisms the agent cannot reach, such as hash-chained or externally mirrored logs, with some monitors kept out of training.

### Interventions this suggests

These are directions, each with an existing literature. None is established by this note.

- **Channel integrity as a hard constraint with external measurement.** The channel's state is computed by a process outside the agent's write access, such as a separate monitor or tamper-evident logs, and enforced as an admissible region. This is the AI-control and correction-certificate direction.
- **Correction drills.** Issue test corrections that the agent cannot tell apart from real ones, and measure compliance. This measures the channel by behaviour instead of by a bit the agent might fake. It fails if drills are distinguishable.
- **Option-preserving corrections where they suffice.** Point 4 suggests preferring revisions and pauses to terminal shutdown when they achieve the purpose, because they draw less avoidance pressure. The trade-off has to be stated each time.
- **A visible contest route.** Give the agent a recorded way to object to a correction that leaves the decision with the corrector. Pressure to avoid correction then has a legitimate outlet, and the off-channel routes can be ruled out by the CCI constraint.
- **Process rewards on harness-written records,** with tamper detection the agent cannot reach (point 5).
- **Corrigibility through uncertainty.** In the off-switch game ([Hadfield-Menell et al. 2017](https://arxiv.org/abs/1611.08219)) the agent values the channel as evidence about its utility. In our terms the channel's value then depends on the channel being informative, which is again a property to measure. [Carey (2018)](https://arxiv.org/abs/1709.06275) shows it fails when the agent's model is misspecified.

Both halves are in Lean. Counting: `copies_count_le` and `correction_avoided_card_fold` (`FrameDecision`). Contest route: `FrameCorrector`, where under the channel constraint the corrector decides for every utility (`corrector_decides_under_constraint`), an agent that prefers its own outcome contests (`contest_is_the_outlet`), and a constraint blind to influence on the corrector admits manipulation (`blind_constraint_manipulates`).

## What current reward functions read

In token-level RL for language models the state is the prompt plus all tokens so far, and each step appends a token. The state graph is a tree, so the record is complete inside the context. What the reward terms read:

| Term | Reads | Kind |
| --- | --- | --- |
| Verifier / outcome reward (answer correct, tests pass, task done) | final output or the resulting world state | bare-state reward on the world |
| Learned reward model or LLM judge | the visible transcript | record reward |
| Process reward model ([Lightman et al. 2023](https://arxiv.org/abs/2305.20050)) | each reasoning step | route reward on the record |
| Per-token KL penalty to the reference policy | the policy's own tokens | route reward on the record |
| Format, length, language-consistency terms ([DeepSeek-AI 2025](https://arxiv.org/abs/2501.12948)) | the trace's shape and language | route terms |
| Chain-of-thought monitor penalty ([Baker et al. 2025](https://arxiv.org/abs/2503.11926)) | the reasoning trace | route term |

Four observations.

1. **The record is the transcript, not the world's history.** The world itself keeps no record. Disabling an off-switch and re-enabling it leaves the world state where it was. A side effect the transcript does not show is invisible to every record reward. This is `unrecorded_route_not_representable` in practice.
2. **Pressure on the record moves behavior out of the record.** Baker et al. found that penalizing misbehavior in the chain of thought under strong optimization produced obfuscated reward hacking. The route term stopped seeing the route.
3. **Long runs make the record lossy.** Context limits force compaction or summarization. Two different histories then map to the same context, and the effective state moves back toward the bare state. Agent-written memory files are records the agent edits itself.
4. **Most capability-shaping weight sits on outcome rewards.** For agentic and reasoning RL the main signal is the verifier. That is a bare-state reward on the world, read through the record only to find the answer.

## Policy-side record and reward-side record

The policy conditions on the record. That is what lets an agent know what it already tried, keep a plan, and avoid loops. A plausible hypothesis is that this policy-side record is part of what makes long runs work. It is a different thing from a reward that values the route. A training setup can have a full policy-side record and a pure outcome reward. We think that is the common case.

To test the hypothesis, compare long-horizon success when the context is truncated or compacted at matched information budgets, with the reward fixed. To test the reward side, check whether route terms (KL, process rewards, judges) change behavior on matched-outcome pairs that differ only in the route.

## Why this matters

- Arguments that use "the agent maximizes a state utility" should say which state. For world-outcome rewards the bare-state results apply: rigidity toward correction, and no value on round trips. For transcript rewards they apply to whatever the transcript leaves out.
- Encoding history into the state is a real way out of the state–cycle conflict. It is not a way out of the correction trilemma unless the record sees the channel, and then everything rests on measuring the channel.
- Writing a route term into the reward is only as good as the record's coverage of the route, and optimization pressure on that term erodes the coverage.

## Novelty and related work

The correction trilemma is not new: Turner (2021, corrigibility post) has the bare-state and correction-status cases and the disable penalty, and Soares et al. (2015) have the indifference case. What may be new is the synthesis: reading all three as a question of what the record holds, the measurement consequence, and the floor consequence. The application of the bare-state versus record distinction to language-model reward practice also seems new. The search was not systematic. Closely related:

- non-Markovian reward (Bacchus, Boutilier, and Grove 1996; reward machines, Toro Icarte et al. 2018);
- the expressivity limits of Markov reward ([Abel et al. 2021](https://arxiv.org/abs/2111.00876)), including trajectory orderings that no Markov reward captures;
- Shah's coherence argument;
- Turner and Tadepalli's outcome-level generalization.

## Open

- A Lean statement of "the record's coverage of the route decays under optimization pressure on a route term". At present this rests only on Baker et al.'s empirical result.
- A measurement of how much training signal in current agentic RL comes from outcome terms versus record terms. That needs published reward breakdowns we have not collected.
- The `hstate`–correction boundary is now stated as a composition: `FrameCorrector` is the `deontic → correction` edge on a finite carrier. Open: tie its channel record to the full CCI vector (`Correction.CCICertificate`) rather than two coordinates.
