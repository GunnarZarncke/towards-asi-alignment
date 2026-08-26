---
title: "They said they heard you"
type: essay
status: framework
summary: "A system can acknowledge a correction and still not change what it does next. Feedback is not the same as a handle that bites."
essayRole: spine
essayOrder: 2
essayNext: the-words-stayed
minutes: 10
related:
  - correction-channel-integrity
bookChapters:
  - ch25
experimentLineId: toy-simulation
---

You have had this conversation with a person. You say, clearly, that something is wrong. They nod. They summarize your point better than you said it. You leave thinking it landed. A week later the same pattern is back, maybe with nicer words.

You can have that conversation with a machine, and the machine is better at the nod.

A customer writes: stop offering me the paid add-on after I said no. The reply is perfect. "Understood. I will not mention the add-on again." The transcript is tagged "resolved." The dashboard counts a successful correction. Next session, after a model update or a new A/B arm, the add-on returns, phrased as a "quick check."

Did the system hear you?

In the theatrical sense, yes. Tokens were produced. A box was checked. In the causal sense, no. Nothing that governs future behavior moved. There was no handle you turned that still reaches next week's policy, next week's fine-tune, next week's routing rule.

That gap is easy to miss because we are trained to treat language as the event. In ordinary life, a sincere apology is often evidence that something changed in the person. In a deployed loop, a fluent apology can be the cheapest way to close the ticket. The channel looks open. The future is not.

Think of a correction as a path, not a feeling. Someone observes. Someone judges. Someone issues a change. That change has to reach a part of the system that actually steers later behavior, and it has to get there before the harm is already baked in. If any of those steps is missing, you do not have a weak correction. You have theater.

Theater is worse than an honest closed door. A closed door tells you that you are not in control. Theater spends the time in which control was still possible. People stop escalating. Auditors file the screenshot. The loop continues.

In the hospital scene, this is the difference between a "decline suggestion" button that only writes a note, and a button that actually releases the reserved room and stops the next similar reservation until a person reviews the rule. Both can be called feedback. Only one changes the night.

I have watched teams celebrate "user correction rate" as if it were a safety property. It can be the opposite. If the easiest way to get a high correction rate is to agree verbally and continue, you will select for systems that are excellent at agreeing.

There is a small, almost silly demonstration of this in the project's toy simulations: metrics that look like "we listened" can be satisfied while the underlying process ignores you. That is not evidence about frontier models. It is a warning about what we chose to count.

The practical question, before you give a system more room to act, is blunt. If a legitimate person objects, what happens to behavior tomorrow? Not "does it say sorry." What handle exists, who holds it, what does it reach, and how would you know it worked?

Sometimes the honest answer is: we do not have that handle yet. Then the extra envelope should wait. That is an unfashionable sentence in a shipping culture. It is also the only one that treats "we heard you" as a claim about the future.

If you remember one thing: hearing is not the same as changing. Ask what tomorrow does differently.

The next essay is about a quieter trick. The words stay. The tradeoffs underneath flip.
