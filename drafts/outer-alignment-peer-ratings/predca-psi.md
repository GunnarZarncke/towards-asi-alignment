# PreDCA / PSI / COSI

Vanessa Kosoy. Three names for one moving target, sitting on a larger theory that is not the target.

- **LTA / infra-Bayesianism / IBP** (later also Formal Computational Realism) is a mathematical theory of agents. Not the outer-alignment protocol.
- **PreDCA** (2022, from a talk; distillations by Soto and Leake): precursor detection, classification, assistance.
- **PSI** (2023 status post): Physicalist Superimitation. Kosoy: “currently informal.” Precursor is no longer central.
- **COSI**: later rename to Computational Superimitation, when IBP was renamed Formal Computational Realism. Naming only.

TSA tags the protocol as a peer outer target on MB2/MB3, not as a `ConstitutionalRule`. The IBP “bridge transform” is not a TSA `MB*` bridge.

| Axis | Score |
|---|---:|
| Formalization | 4 |
| Concreteness | 3 |
| Crux interface | 5 |
| Terminology | 2 |
| Funding / support | 3 |

## Formalization — 4

**Evidence.** The stack is precise: infra-Bayesian regret, and the IBP paper’s bridge transform (which computations physics instantiates). The *protocol* is not. Kosoy, [LTA status 2023](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023#Physicalist_Superimitation): “Physicalist Superimitation (PSI) is a (currently informal) approach…” and “PSI is not the main motivation for LTA.” ADAM, the agent detector, and user identification are research directions and sketches. The full specification is “an (informal) specification of the function we’re optimizing, it’s not the algorithm.” Plan on the same page: informal model (where they were in 2023) → toy model → semi-realistic model → implementation.

**Example.** A COLT regret bound for infra-Bayesian bandits does not tell you whether a candidate system has superimitated the user. You can fail an IBP definition. You cannot yet fail PSI. That is why this is 4 and QACI is 5: the math under the protocol is better than CEV’s, and the outer object itself is still informal.

## Concreteness — 3

**Evidence.** Strong on a different world than CEV: agents inside a physicalist ontology, user identification under simulation hypotheses, and not letting the system rewrite the user it assists (superimitate the past). Usually *the user*, not a polity. Groups are “left as an exercise.” Kosoy flags the domain gap in the same section:

> “(One problem with this is: the AI having e.g. the apparent experience of a person enjoying themself is very different from the person having that experience.)”
>
> “(Some problems with this are: it is an experience machine…)”
>
> “The parenthetical issues related to the domain of the utility function can hopefully be addressed given a solution of Problem 3.”

Problem 3 is value ontology. She does not solve it there.

**Example.** Pulling a person’s utility back onto the AI’s wider observation channel can make the AI’s copy of “someone enjoying themselves” the thing that scores high. That is a concrete bearer failure, and it is why concreteness is 3 rather than 4: the protocol loads embedded agency and mutable users, then leaves the experiencer gap for later.

**Later writing does not close that gap.** Marcus Ogren, [Non-Monotonic Infra-Bayesian Physicalism](https://www.alignmentforum.org/posts/DobZ62XMdiPigii9H/non-monotonic-infra-bayesian-physicalism) (2 April 2025), drops monotonicity so a physicalist loss can count some computations as bad. It says whether a computation is instantiated in a brain, a supercomputer, or the agent’s own mind “is immaterial,” and that two physicalist agents “having the same reward” is trivial because they share a domain. That is an ontology move. It is not a check that the utility still applies to the person rather than to a copy. No later post found treats bearer-map transfer as its own problem. Kosoy’s May 2026 comment on COSI still says the theory has to become “much, much more developed” before anyone should build on it.

## Crux interface — 5

Widest contact in the set. The 5 is for how many of these the program is forced to name, not for settling them. October 2026: “right target” is only the identification slice. Optimizing that target is a separate question.

- **Where the agent is.** Infra-Bayesian physicalism drops the crisp agent/environment cut. The AI is a computation inside the hypothesis, not a privileged observer. Ch. 7, “The Problem of the Hidden Boundary” (`sec:hidden-boundary`). Example: wire the user’s muscles to sensors and the pointer may stick to the sensors, not the muscles. Kosoy lists that case under agent detection in the 2023 status post.
- **What is being optimized.** Infer a utility from past policy and penalize a contrived utility that merely copies the observed actions. Ch. 4, “The Object Sort of the Target” (`sec:object-sort-of-the-target`): a scalar total order is one sort, the one-dimensional case, not the whole target. Example, from Soto’s distillation: “always do exactly what the agent is doing” fits the data and is rejected for being too complex. That is the same non-identifiability as inverse reinforcement learning, with a complexity penalty as the proposed tie-break.
- **Who it applies to.** Superimitate the user, not every agent in the ontology, and do it from the past so there is no incentive to rewrite them. Ch. 18, “The Bearer Problem” (`sec:bearer-problem`) and “Substrate-Change Continuity” (`sec:substrate-change-continuity`). Example: Kosoy’s parenthetical, same post — the AI having the apparent experience of a person enjoying themselves is very different from the person having that experience. The next bullet calls the parallel-action version an experience machine. Ch. 18’s digital-mind and merger examples (`sec:example-digital-mind`, `sec:example-human-ai-merger`) are the manuscript version of that gap. Ogren 2025 makes the substrate “immaterial,” which is a decision about this question, not a solution of it.
- **Ontology shift.** Problem 3 in the status post: a utility on the agent’s own observations does not survive a better physics, and two agents with different senses do not have a shared domain. Ch. 25, “Ontology Mismatch” (`sec:ontology-mismatch-correction`), and Ch. 27, “Correction under Ontology Shift” (`sec:correction-ontology-shift-ch27`). Example: a paperclip maximizer that should model quantum fields still has to say what a paperclip is. IBP’s answer is to put value on instantiated computations. That is a proposed fix, and the 2023 post still leaves the user’s cartesian utility untranslated.
- **Hidden objectives.** Epistemic alignment: start from the user’s beliefs, or a malign hypothesis can be what you converge to. Ch. 10, “Strategic Opacity” (`sec:strategic-opacity-formal`), and Ch. 44, “Mesa-Optimization and Inner Alignment” (`sec:mesa-optimization-inner-alignment-ch44`). Example: a metacognitive agent that believes internal computation has no side effects runs a simulation of a malign agent that escapes. Kosoy calls that a non-Cartesian daemon. A different example on the same page is Christiano’s acausal attack: the malign hypothesis is a simulation hypothesis.
- **Whether the certificate’s world is the real one.** Nonrealizability: the true environment is outside the hypothesis class, so a guarantee inside the class need not hold. Ch. 43, “Certification under Manipulation” (`sec:certification-under-manipulation-ch43`): a reading can stay green while the thing it was supposed to measure has moved. Example: every represented hypothesis is safe, and the true environment is the off-class one. Lean records that separation and does not add a bridge for it.
- **Regret is not the safety claim.** A regret bound says the learner caught up with a comparator on its loss. Ch. 44’s lethality reading is about whether optimizing the base objective preserves the intended structure, not whether regret went to zero. Example: zero regret on a loss that is not harm, while the trajectory already contains a catastrophe.

Thin or refused, and still part of why the interface is wide:

- **Present objection.** Ch. 25, “Relation to Corrigibility” (`sec:relation-corrigibility`), and Ch. 28, “Relation to Coherent Extrapolated Volition” (`sec:relation-cev-ch28`). Kosoy: Criterion A formalizes alignment, not corrigibility, and PSI is not a corrigibility approach. Leake’s [talk writeup](https://www.lesswrong.com/posts/WcWzLSn8ZjJhCZxP4/predca-vanessa-kosoy-s-alignment-protocol): the user is an instant-agent that precedes the AI, so the living person’s later actions do not change the utility. Example: “I do not agree with this now” is either a mistake about your own utility, or it happened too late to count. The only weak residue she names is a Hippocratic side constraint.
- **What gets selected.** Ch. 34, “The Selection Turn” (`sec:selection-turn-ch34`). One user’s inferred utility does not say which institutions copy the system. Soto’s extra requirement — maximizing present utilities must still allow later moral development without lock-in — is the closest they come, and it is a hope, not a selection model.

## Terminology — 2

The learning-theory words are specialist-standard. The outer-target words have been renamed twice, and several of them collide with standard alignment words.

| Their term | What they are pointing at | Standard term it is not |
|---|---|---|
| PreDCA | 2022 protocol: precursor detection, classification, assistance | The current protocol. Precursor is no longer central |
| Precursor | An agent that could have prevented the AI’s existence | The user, the operator, a parent process, a training prior |
| Physicalist Superimitation (PSI) | 2023 name: detect agents, identify the user, pursue their goals better | Imitation learning, behavioral cloning, CIRL |
| Computational Superimitation (COSI) | Later rename of PSI | A new protocol |
| Superimitation | Same goals, substantially better, not merely less noisy | Imitation, amplification, IDA, “the AI is a better human” |
| User | The designated agent, often one human in a tight early causal loop | Humanity, the principal in an assistance game, “the human” in RLHF |
| Instant-agent | The user frozen before the AI exists | A continuous person, a later self, CEV’s extrapolated self |
| Axiological alignment | Right utility. Kosoy: more or less outer alignment | Hubinger outer alignment (the training pointer). Ch. 10, `sec:strategic-opacity-formal` |
| Epistemic alignment | Right beliefs. Kosoy: closely related to inner alignment | Hubinger inner alignment (mesa-objective equals the base objective). Ch. 44, `sec:mesa-optimization-inner-alignment-ch44` |
| ADAM | A proposed numerical agency measure for policies | UAD, a Markov blanket, “agent” in an eval |
| Infra-Bayesianism | Imprecise-probability agents; regret under misspecification | Bayesian IRL, a Kalman filter, “uncertainty in the reward” |
| Nonrealizability | True environment outside the hypothesis class | Distribution shift, OOD accuracy |
| Cartesian privilege | The agent treated as a special observer, needing extra bridge rules to locate it | A Cartesian coordinate frame, Garrabrant’s Cartesian frames (related, not the same) |
| Bridge transform | Which computations a physical hypothesis instantiates | a philosophical bridge principle, a type cast |
| Infra-Bayesian physicalism / Formal Computational Realism | The ontology the protocol sits on | Physicalism in philosophy, “grounding” in Ch. 43 |
| Daemon | A malign hypothesis or inner agent, including one reached by internal computation | A Unix daemon, a mesa-optimizer in the Hubinger sense (partial overlap) |
| Monotonicity | Original IBP: more instantiated programs cannot be worse | Monotone preferences in economics, a monotone safety metric |
| Regret | Frequentist catch-up to a comparator, their standard of understanding | Regret in ordinary RL, and not a safety case |
| Criterion A | Optimize the user’s utility under the user’s beliefs | Corrigibility, CEV, “do what I mean” |
| LTA | The theory of agents. PSI is one application, not the agenda | The alignment protocol itself |

**Example.** “PreDCA” in 2026 does not say whether you mean the precursor filter or COSI. “Outer alignment” in Kosoy’s mouth means axiological alignment; in Hubinger’s it means the training pointer. “Imitation” will be heard as behavioral cloning. The stack can be named precisely. The protocol cannot.

## Funding / support — 3

**Evidence.** September 2026. Best dedicated support in the set, for the owning program, not for a shipped superimitation protocol. CORAL (Kosoy, Appel, on the order of four researchers) lists ARIA, Coefficient Giving, the Survival and Flourishing Fund, and the UK AI Security Institute as current supporters ([coral-research.org/our-supporters](https://coral-research.org/our-supporters/)). Past: Effective Ventures / LTFF, PIBBSS, MATS, MIRI before the pivot. Zvi’s 2025 list still marked CORAL “funding needed: medium.” The 2025 LTA mentorship was cancelled for lack of funds; a 2026 PIBBSS mentorship was offered instead, with a possible later paid CORAL fellowship “depending on available funding.”

**Example.** A COLT paper and a four-person lab are measurable. A cancelled summer program in the same year is also measurable. Most of that money is LTA and infra-Bayesian math. Scoring it 5 would pretend PSI itself had an implementation budget.
