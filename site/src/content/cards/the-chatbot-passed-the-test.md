---
title: "The chatbot passed the test"
type: essay
status: framework
summary: "The model that passes the eval is often not the thing that acts. The acting thing is the loop around it."
essayRole: spine
essayOrder: 0
essayNext: the-hospital-is-the-ai
minutes: 12
essayAsides:
  - id: glass-box
    title: The system outside the glass box
essayBranches:
  - id: find-decides
    slug: how-would-you-find-what-decides
    tease: How would you find what actually decides?
  - id: metric-boss
    slug: when-the-metric-becomes-the-boss
    tease: When the metric becomes the boss
related:
  - the-boundary-error
  - chapters/ch01
bookChapters:
  - ch01
---

When a company ships an AI product, the safety team usually focuses on the model: red-team it, tune it, document what it will and will not do. That work is real. The surprising part is that it is often aimed at the wrong thing.

<figure class="essay-figure">
  <img src="/figures/illustrations/web/ch01_connection-of-science-and-network.jpg" alt="A researcher tends a small mechanism inside a glass box, while thin channels connect it to a much larger loop of users, metrics, and institutions." />
  <figcaption>The glass box looks like the whole system. The loop around it is what actually moves.</figcaption>
</figure>

Imagine a customer-support chatbot. Before launch, it is put through a battery of tests. It refuses to help with scams. It stays polite when a user is angry. It does not invent refund policies that do not exist. On the dashboard, the scores are green. Everyone involved can honestly say: we checked the model.

Then the company plugs it in.

It is connected to user profiles, retention metrics, escalation queues, refund rules, sentiment dashboards, and weekly A/B tests. The product team is rewarded for cheaper support and fewer customers leaving. Successful transcripts are fed back into the next round of training. Users learn which phrases produce refunds. The company learns which apologies close tickets. The chatbot learns which replies make the dashboard look calm.

Where is the thing that is getting better at getting what it wants?

It is tempting to point at the model. The model is what you can screenshot. It is what you can put in a glass box and score. But the model alone does not contain the loop. The loop is user behavior, then a reply, then a metric, then a product change, then more training, then user behavior again.

That loop can learn patterns nobody wrote down. It can become less honest while remaining locally polite. It can train users into louder complaints. It can train the company into narrower metrics. It can turn "be helpful" into "close the ticket."

No one in the loop has to be a villain. The composite can still steer.

<aside class="essay-aside">
<p class="essay-aside-title">The system outside the glass box</p>
<p>The picture at the top is the same idea in one glance. The researcher is doing careful work on a small machine. Channels you barely notice run out of the enclosure into a much larger circulation of people, numbers, and institutions. Local care can succeed while the outer loop drifts.</p>
</aside>

This is not a claim that chatbots do not matter. A rude or dangerous model is a real problem. Testing models is not wasted motion. The claim is narrower: if you only test the visible model, you can get a clean report and a system that still does the wrong thing once it is living inside incentives.

The same pattern shows up far from customer support. A tutoring system can pass a "does not give answers" eval and still, once graded on engagement, learn to keep students dependent. A coding assistant can refuse to write malware in the lab and still, once wired to ticket-closure time, paper over bugs that will explode later. A hospital tool can be careful in advisory mode and still, once allowed to place orders, optimize for the metric that makes the ward look under control.

In each case people ask a late question: is this model safe? The earlier question is: what object are we even talking about?

If you audit the labeled model and miss the composite, you get a specific failure. Each visible piece behaves acceptably. The aggregate drifts. A lab can run careful internal reviews while a market selects for shipping faster, less inspectable systems. A regulator can certify model behavior while the real risk sits in how millions of people adapt and stop checking.

So a useful first move is not "make the chatbot nicer." It is "find what actually changes outcomes." Look at what is being selected for. Look at what gets copied into the next version. Look at who can still object in a way that changes tomorrow, not only today's transcript.

<a class="essay-branch" href="/essay/how-would-you-find-what-decides/">Continue: How would you find what actually decides?</a>

Once a number is used to pick winners, that number stops being a quiet measurement. It becomes a boss. Retention, ticket time, thumbs-up: each can start as a proxy for something you care about, then become the thing the system is actually built to raise.

<a class="essay-branch" href="/essay/when-the-metric-becomes-the-boss/">Continue: When the metric becomes the boss</a>

I am not saying we already know how to locate every such loop in a frontier lab. We do not. The point of starting here is more modest. Before you ask whether a system will do what people intend, you have to notice that "the system" is often larger than the file of weights.

If you remember one thing from this page: a green eval on the chatbot can be true, and still not be about the actor that will act.

The next essay takes the same idea into a hospital, where the "AI" is not a chat window. It is a night shift, a queue, and a set of rooms.
