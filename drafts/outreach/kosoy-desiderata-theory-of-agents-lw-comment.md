# LessWrong comment draft — *Desiderata for the Theory of Agents* (Nov 2026)

**Thread:** [Desiderata for the Theory of Agents](https://www.lesswrong.com/posts/sqjti8dxcKSvZJikd/desiderata-for-the-theory-of-agents) — Vanessa Kosoy, 4 November 2026.

**Status:** Draft, not posted. Same vein as [`kosoy-alignment-problem-lw-comment.md`](kosoy-alignment-problem-lw-comment.md).

**Leave to others:** Haru (5 Nov 2026) already asks whether the five desiderata are pass/fail for one theory or a patchwork.


[Embedded Agency](https://www.lesswrong.com/w/embedded-agency), [Boundaries / Membranes](https://www.lesswrong.com/w/boundaries-membranes-technical), [The Pointers Problem](https://www.lesswrong.com/w/the-pointers-problem), [Value Drift](https://www.lesswrong.com/w/value-drift), [User Manipulation](https://www.lesswrong.com/w/user-manipulation), [Successor Alignment](https://www.lesswrong.com/w/successor-alignment), [Corrigibility](https://www.lesswrong.com/w/corrigibility-1), [Ontological Crisis](https://www.lesswrong.com/w/ontological-crisis), [Reward Hacking](https://www.lesswrong.com/w/reward-hacking), [Unsupervised Agent Discovery](https://www.lesswrong.com/posts/pXYosC3eoS9GrDRAw/unsupervised-agent-discovery).
## Comment

Thanks for laying out the desiderata. I want to add a few places where the theory still has to say which process is the agent, what a guarantee is about, and who a value applies to.

Going in order of your post.

### A Theory of What?

> a system with inputs ("observations") and outputs ("actions") that is effective at steering its environment in the direction of particular preferences

The observations and actions are already chosen. That is a [Cartesian agent-environment boundary](https://www.lesswrong.com/w/cartesian-agent-environment-boundary):

> the agent receives sensory information from the environment, and the agent sends motor outputs to the environment, and nothing else can cross the `Cartesian border'

Under [embedded agency](https://www.lesswrong.com/w/embedded-agency), that cut is part of the problem. A process can steer through a channel that was never labeled as its action set. I would want the theory to recover a [boundary](https://www.lesswrong.com/w/boundaries-membranes-technical), not only to ascribe preferences once the boundary is given. Which process is the real optimizer is the first question I ask; my answer is still [Unsupervised Agent Discovery](https://www.lesswrong.com/posts/pXYosC3eoS9GrDRAw/unsupervised-agent-discovery).

You later constrain *what counts as an agent*: SGD would exclude humans (overspecified); any expected-utility maximizer would include rocks and underspecify attributes (Shah 2018). That is the right constraint on the **class**. It does not recover the **unit**. A theory that correctly excludes rocks and includes humans can still ascribe Alice’s attributes to the labeled sensors, or to the loudest subprocess. Footnote 2’s scalar makes this worse if “more agentic” tracks volume of effect: the process that matters can be quieter than the process that moves the most variables.

Putting “particular preferences” inside the definition of agent also collapses discovery and value-reading. You can find a unit that steers and still not know what it is steering toward; a wrong unit can still be handed a fluent utility.

### Descriptive

Agreed on covering humans, the unaligned system, and the aligned system from the theory rather than from domain lore.

The apple and banana case is the easy kind of ambiguity. Both readings still apply to Alice, and to apples and bananas. A value can be stated precisely and still change who it applies to. “Happiness of mankind” can stay a clean preference while its bearers are read as souls in Heaven rather than living people.

> When a proxy for some value becomes the target of optimization pressure, the proxy will cease to be a good proxy.

([Goodhart's Law](https://www.lesswrong.com/w/goodharts-law))

That residual is not immaterial once optimization is on the table. [The pointers problem](https://www.lesswrong.com/w/the-pointers-problem) is which functions of which variables correspond to the latent variables in the agent’s model. I call the requirement that a value keep applying to the same persons and processes Bearer Persistence. Tolerance for ambiguity needs an index: the ratio, the person, or the extension.

> if we also knew all pertinent facts about the physical world, we would be able to answer the question

Some of those facts are a history in which another agent shaped the preferences. [Value drift](https://www.lesswrong.com/w/value-drift) is change over time, often not as originally intended; a mistake relative to a person’s preference, a real change of preference, and a change the system installed ([user manipulation](https://www.lesswrong.com/w/user-manipulation)) are three different facts. If every change of mind is noise around a fixed target, a long-running agent that reshapes education will count as having learned the user.

### Metareflective

> Describe an agent that identifies other agents in the universe and infers their preferences, beliefs, or other attributes.

I would split this bullet. Identifying other agents, and inferring their attributes, are different uses of the theory. An agent can do the second on the wrong unit and still look metareflective.

You separate “metareflective” from reflective stability. I think that separation is right, and I would keep a further one. [Successor alignment](https://www.lesswrong.com/w/successor-alignment) is not only “the successor has the parent’s goals.” An agent can know the theory, look [corrigible](https://www.lesswrong.com/w/corrigibility-1) on one channel, and still hand its successor a path on which a person’s later correction no longer constrains action.

### Comparative

Agreed that we need both a comparison of attributes and a real scale of power, and that without computational bounds the power scale collapses.

On the metaphysical realism you invoke for that comparison: incomparability of utilities is real, and so is caring about world-states rather than only subjective experience. I am not sure the fix is one external ontology that the preferences live in. I want the user’s map and the agent’s map to refer to the same entities ([pointers](https://www.lesswrong.com/w/the-pointers-problem) again). I call that Bearer Maps. Two agents can share referents and still have utilities that do not compare.

Similarity of preferences can be high while those referents have drifted ([ontological crisis](https://www.lesswrong.com/w/ontological-crisis)). That is a third comparison, alongside “how alike are the attributes” and “how powerful is the agent.” A powerful agent with the user’s words, pointed at the wrong people, is already inside your threat model. Score power on the recovered optimizer. Footnote 7’s more efficient process, with less compute, is also the process easiest to leave outside the labeled interface.

### Aggregative

> the agent needs to align itself to the aggregate of possible counterfactual users

This is the desideratum I was missing from the previous post, where preference aggregation was set aside. I agree it belongs here, and I agree that \(\mathbb{E}[u_\theta]\) is ill-posed once utility is only defined up to a positive affine transformation.

I would still not treat a repaired mixture as the alignment target. The mixture is over counterfactual users in the agent’s belief. The people who can still object are a different set. If residual error is handled by aligning to the aggregate of users you might have found, a living dissent arrives as noise about that aggregate. When time pressure forces a decision before alignment is perfect, the invariant I want is that a person’s correction still constrains later actions, including the actions of a successor. That is a guarantee about the channel, not a claim that the aggregate utility was right.

> conditions under which a collective of agents can be regarded as a single agent

The converse conditions matter too. A collective can steer while no member, and no extra crisp agent, is the optimizer, because the steering sits in a shared resource. And a label such as “the users” or “humanity” can be treated as one agent when the acting unit is whoever operates the aggregator. Whoever controls that aggregate has the power the defense task was meant to control.

### Constructive

> We would be taking our chances with agents that would converge to alignment in some imaginary asymptotic limit, but take catastrophic actions long before approaching that point.

Agreed. A proposal whose only safety argument is that the agent would be aligned in the limit fails even when that limit is true.

> the theory has to produce a formal specification such that any heuristic output that certifiably meets the specification is safe

A spec can still be [reward hacking](https://www.lesswrong.com/w/reward-hacking) of the wrong process: efficiently checkable on the intended interface, met by a system that fails on a side channel. And a proved algorithm is still an empirical claim once it is the thing that runs. Verification helps, and it stays conditional. Convergence bites again at deployment, not only inside the learning rule.

---

Do you see bearer persistence, and a correction channel that survives successors, as implied by these five, or as separate desiderata? And does computational superimitation identify the agent before it ascribes attributes, or does the user arrive already labeled?
