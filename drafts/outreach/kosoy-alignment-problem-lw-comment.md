# LessWrong comment on Kosoy — *The Alignment Problem* (Oct 2026)

**Thread:** [The Alignment Problem: Computer Science Meets Analytic Philosophy](https://www.lesswrong.com/s/iKtxSpGeRSwdyNZd6/p/Emp7awtxsYn8MusNq) — Vanessa Kosoy, 18 October 2026.

**Anchor:** `#sSBMjNcuu9CoTKhZ8` (section linked from the original draft).

**Status:** Archived reply text (Gunnar Zarncke). Point-by-point response to Kosoy’s post, mapping disagreements and extensions to TSA vocabulary.

## Comment (as posted or final draft)

Thanks for working on alignment. I want to add to it with points around the entity that gets aligned, what your approach can actually guarantee, and whose values count.

Going in order of your post.

we can run any AI inside a homomorphic encryption box and never decrypt the output. This is probably perfectly safe, but also perfectly useless.

Useless, yes. On "perfectly safe" I'm not sure. Footnote 1 assumes the ciphertext is physically indistinguishable from a random program. Your side-channel section doesn't allow to ignore that your box is embedded in the real world and radiates away information. Side-channels are part of the entity we need to model.

the *minimal* task that safe AI must be able to solve is "create a reliable global defense system against dangerous AI" (GDS).

Let's apply your argument one step further: Whoever (even if distributed) controls the defense system has the power you were trying to control. Your footnote 6 sets puts preference aggregation out of scope, but for this task you need to consider which entity (even if a group, which might also be influenced) can exercise control.

designing an AI system that can bring scalable (and ultimately superhuman) capability to bear on problems that require multi-domain reasoning and open-world long-term planning with far-reaching consequences, all the while staying aligned with the intentions and preferences of its human users.

"Its human users" does a lot of work here. Those users are fallible and this is fully compatible with a catastrophe.

The nature of the incremental approach is as follows: we build a system, then we find problems ... This approach utterly fails if the "problems" result in AI takeover and possibly human extinction: there is nobody left to fix them.

Agreed. But a nitpick. Even if you don't intend to build a system incrementally but from a theory strong enough to get it right on the first try, you still have one area where your argument bites yourself and that is when you go from theory to practice. Even a theory that proves the intended algorithm safe can not on its own prove that an implementation of it realizes that algorithm under the assumptions made. Constructing a system that implements a theory is an empirical claim in the end and the problem of irreversible mistakes reappears during implementation. Verification helps, but it is still conditional.

"Alignment" is meaningless outside the full context of epistemic and instrumental rationality.

Agreed, including the part where aligned beliefs means beliefs the user can trust, not beliefs the user already has.

Such an AI would be motivated to kill all humans, even though its preferences are arguably "aligned".

I would phrase it differently. "happiness of mankind" did not fail. The entities it applies to were reinterpreted: souls in Heaven instead of living people. We want to ensure that a value still applies to the same persons and processes (what I call Bearer Persistence).

One approach to avoiding Goodhart's Curse is somehow restricting the domain within which the agent operates or its overall impact. But this is incompatible with the GDS task.

It is incompatible with an unrestricted GDS agent. But I think it is compatible with keeping uncertified deployment channels narrow while the defense layer stays large enough. And there may be other options that I discuss in adversarial pressure on correction.

we cannot just delegate the task to a heuristic, since that would preclude any strong guarantee about the outcome.

This holds if the guarantee has to be about each decision. But a guarantee could maintain invariants over decisions and successors, for example that a person's correction still constrains later actions (integrity of the correction channel).

none of this data is a direct and accurate representation of human preferences. Humans make mistakes. Humans change their mind.

Yes, but let's be clear that these are indeed two different things.

A mistake relative to a person's preference,
A real change of preference.
If every change of mind is noise around a fixed target, a long-running agent that reshapes education will learn a preference it created. I discuss this in manipulation and false consent.

such utility functions cannot be compared between different agents ... humans have preferences about the physical reality itself, rather than merely their subjective experience.

Agreed to both incomparability as well as using value about world-states as criteria. But I'm not sure we need metaphysical realism. I'd say we need that the user's map and the agent's map refer to the same entities as suggested in Bearer Maps.

some humans are smart enough to build ASI but not smart enough to either make sure it's aligned or not to build it. As a user, I would not like my agent to inhabit a similar epistemic state, even if the agent *would* be fully aligned with more scaling.

Yeah. A proposal whose only safety argument is "at sufficient scale it would be aligned" fails even if the claim is true in the limit.

Any guarantee about the preferences, beliefs and decisions of the agent would reference only the actions that the agent takes through its intended interface. ... a robot that never takes a malign action with its actuators, but runs an internal computation which causes an unaligned successor agent to be copied into a different system.

You need to treat the side channel as part of the agent. Which process is the real optimizer is the first question to ask, and my answer is Unsupervised Agent Discovery.

If we had a guarantee that the agent's attributes are aligned, then, in particular, it wouldn't be controlled by a misaligned mesa-optimizer.

This seems to follows trivially from the way you stated the guarantee. The question is whether any feasible algorithm supplies that guarantee.

It is intended as a set of lenses that must be applied to any proposed solution in order to validate its viability.

I will use the lenses that way in my summary of your agenda.

I am not sure if superimitation can establish

that human values continue to refer to what they used to as the system and its ontology change, and
that humans continue to exert effective control even as they and the system (self-)modify and develop.
Do you see these as implied by superimitation or as separate problems?

---

## Uptake in this repo

| Topic in comment | Where it lives (partial) |
|------------------|---------------------------|
| Four lenses (side channel, convergence, grounding, hypercomplexity) | `review/claim-checklist.md`; Ch. 10, Ch. 44; bib `kosoy2026alignmentproblem` |
| Side-channel / successor robot case | `chapters/ch10-strategic-opacity.tex`, `chapters/ch44-lethality-stress-test-open-issues.tex` |
| Bearer Persistence, Bearer Maps, UAD, correction channel, manipulation | Book concepts / chapters (e.g. ch18, ch25–29, ch7); field card + `drafts/outer-alignment-peer-ratings/predca-psi.md` |
| Superimitation vs bearer + correction (closing questions) | Named as separate checks on Kosoy/LTA in field hub; not settled in manuscript |

**Not yet in manuscript** (logged in [`drafts/conversation-summaries/archive/2026-10/2026-10-19-kosoy-lenses.md`](../conversation-summaries/archive/2026-10/2026-10-19-kosoy-lenses.md)): GDS / who controls the defense layer; invariant-over-successors guarantees vs per-decision regret; homomorphic-box side-channel nuance; theory→implementation gap as its own convergence bite.

**Session:** lens integration — [`2026-10-19-kosoy-lenses.md`](../conversation-summaries/archive/2026-10/2026-10-19-kosoy-lenses.md).
