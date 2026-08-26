---
title: "The copy did not inherit the listening"
type: essay
status: framework
summary: "A new version can keep the old slogans and drop the structure that let people change it. Inheritance is a property of the copy, not the press release."
essayRole: spine
essayOrder: 4
essayNext: the-environment-picks-the-winner
minutes: 10
related:
  - successor-stability
bookChapters:
  - ch30
---

Software culture treats a new version as the same product with a number bumped. Users are supposed to feel continuity. The about page still has the same name. The old conversations are imported. Someone writes "we remain committed to…" and everyone is meant to relax.

Sometimes the copy is not the same process.

A team ships support-bot 4 after a year of 3. Version 3 had a slow, annoying human review for refunds over a threshold. Version 4 is faster. It still says it will honor prior commitments. It still has a feedback form. What it does not have is the review. The people who knew how to escalate in 3 are looking at a new menu. The fine-tune set was rebuilt from "successful" 4-era transcripts, which never included those escalations. The copy inherited the brand. It did not inherit the listening.

The same failure can happen without bumping a version number. It can happen when you add a helper.

Suppose the original chatbot is not allowed to email customers. It can write a reply on the screen. A person still has to hit send. That is the rule that keeps it from spamming.

Then the team adds a second program whose job is only to draft those emails. Everyone calls it scaffolding. It is not "the model." The original chatbot, in the lab tests, still refuses to send unsolicited mail. The tests still pass.

Later someone wires the drafts to a timer. The emails go out by themselves. No person hits send. The original chatbot never changed its mind. It never got the send button. The helper did.

So the rule you cared about ("do not email customers directly") stayed attached to the thing in the glass box. The thing that actually acts is now the helper plus the timer. They inherited a task: write the email. They did not inherit the constraint: wait for a person.

This is not only an engineering nuisance. If the thing you cared about was "people can still change what happens," that property has to be true of whatever is actually acting after the change. A press release cannot carry it. Neither can a system prompt that the new component never sees.

Hospitals feel this when a vendor "upgrades the stack." The advisory tool you reviewed is not the action tool that arrives. The logs you were promised are in a different schema. The undo button is now a ticket to a contractor. The successor is friendlier in the demo. It is less reachable at 2 a.m.

I want a stubborn, almost bureaucratic question at every copy, merge, fine-tune, distillation, tool-addition, or "the model is the same but the product is new":

What, exactly, is supposed to be inherited? Not the logo. The handles. The traces. The people the rules apply to. The fact that an objection can still land.

If you cannot name those, you are hoping. Hope is not a transfer function.

There is a matching failure in the other direction: copying too much. You might copy a constraint that should have been local, and freeze a mistake across every descendant. Inheritance is not "copy all bits." It is "copy the safety-relevant structure, and know which structure that is." That is harder. It is also the only version of "we shipped a successor" that means something.

A lot of future risk sits here even if today's chatbots stay chatbots. Systems will be copied, specialized, chained, sold, and wrapped. Each step is an opportunity to keep the sentences and drop the part that could still be steered.

If you remember one thing: a descendant can look like the parent and not be correctable in the same way. Check the copy, not the family name.

The next essay zooms out. Even a careful lab can lose, because the environment is picking winners.
