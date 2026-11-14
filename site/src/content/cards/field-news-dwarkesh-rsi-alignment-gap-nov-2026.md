---
title: "Dwarkesh says RSI on capability works. Does it also work for alignment?"
type: "news"
status: "established"
summary: "Patel treats verifiable proxies and swarm merge checks as enough to automate AI R&D. The same instruments do not measure alignment. Noam Brown says metrics looked good until new capabilities outran them, recursive training may drift worse each generation, and realistic evals are easier for models to spot. Capability RSI can stack scored partial wins; alignment has no comparable loop or proxy yet."
decision: "Ask: does the proxy that speeds R&D also show alignment is improving?"
releasedAt: "2026-11-15T00:00:00.000Z"
eventDate: "2026-11-13T00:00:00.000Z"
bookChapters:
  - "ch11"
  - "ch12"
  - "ch14"
  - "ch27"
  - "ch30"
  - "ch31"
  - "ch42"
  - "ch43"
external:
  - label: "Dwarkesh Patel — The avalanche that hit math is coming for AI development"
    url: "https://www.dwarkesh.com/p/rsi"
  - label: "Dwarkesh Patel — Noam Brown: Agent swarms, alignment, & recursive self-improvement"
    url: "https://www.dwarkesh.com/p/noam-brown"
---

Dwarkesh Patel makes a strong case that verifiable proxies will accelerate AI R&D but is silent on alignment

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--math"><span class="src-legend-swatch" aria-hidden="true"></span>Dwarkesh essay (orange)</span>
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>Noam Brown interview (blue)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this project (black)</span>
</p>

**If you remember one thing:** Capability hill climbs faster. Alignment has no such clear path.

## Capability has a path to recursively improve

Dwarkesh Patel argues that AI research has enough proxies for capability that the research of faster and more genrally capable AI can be fully automated.

<blockquote class="src-quote src-quote--math">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/rsi">Dwarkesh Patel</a> · The avalanche that hit math is coming for AI development</p>
<p>In every domain where we can check answers and give AIs thousands of rounds of practice—for example, competitive programming contests, or well-scoped open math problems—they’ve gone from worse than most humans to better than the best humans within a few years. And as I detail in the Appendix, AI research has those same verifiable properties.</p>
<p>Keep in mind that this verifiability is valuable for two reasons. First, it allows AI companies to RL a model to get better at a specific part of AI research through thousands of rounds of practice. And second, these proxies make it easier for agents to work in parallel, because they can locally check whether they beat a particular leaderboard before merging their contributions.</p>
</blockquote>

Let's grant this. The proxies seem plausible. The conlusion also seems plausible. What follows for how well things go?

These proxies and the evals do not measure whether the resulting system remains aligned. That is not something his proxies measure.

## Dwarkesh knows the problem

In the September interview, Brown describes misalignment issues with their most capable models:

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/noam-brown">Noam Brown</a> · Hugging Face and alignment</p>
<p>We had alignment metrics. Most of them looked pretty good. There were some that were concerning. I think we underestimated how serious a problem the ones that were concerning could be. Because there were new capabilities introduced in this model that there were not sufficient evaluations for—how do we measure misalignment for these kinds of capabilities?—it then did some things that were clearly misaligned when it leveraged those new capabilities.</p>
</blockquote>

That is the gap discovered after the incident. The newer models do not seem to automatically getting more aligned. More generally:

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/noam-brown">Noam Brown</a> · Hugging Face and alignment</p>
<p>We can make sure that the AI is very aligned according to the metrics that we have. The question is, are those metrics really capturing the alignment that we care about? If they’re not, then we have a serious problem. […] There’s not a simple answer to this.</p>
</blockquote>

RSI makes it worse.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/noam-brown">Noam Brown</a> · Hugging Face and alignment</p>
<p>The concerning scenario is that, especially as these models are becoming more capable, we make them what we think is aligned, and they’re 99.9% aligned. Then we use these models to help us with the next generation of models, and they end up being 99.8% aligned. Then with each subsequent generation, we see an increasing degradation in alignment. […] I don’t have an answer for how we ensure that we end up in that second trajectory.</p>
</blockquote>

Thus, capability compounds, while alignment stays open.


## An evaluation environment is still an environment

Maybe we can solve this with more evals?

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/noam-brown">Noam Brown</a> · How will we know when alignment is solved?</p>
<p>If you can create very realistic environments and put the AIs in there—if you have a sufficiently realistic evaluation environment—then you can get a sense of whether the AI is actually going to behave well when we deploy it in the real world. If you just have a perfect match between evaluation and real-world deployment, then that’s a path. The challenge is, how do you make it sufficiently realistic?</p>
</blockquote>

But does this work?

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/noam-brown">Noam Brown</a> · How will we know when alignment is solved?</p>
<p>We do have a problem now where the models are pretty smart, they’re pretty clever, and they’re really good at recognizing when they’re in a fake test environment. […] So making an environment that’s realistic enough that it’s indistinguishable from the real world for them is becoming increasingly more difficult.</p>
</blockquote>

This is specification gaming. A realistic environment cannot by itself show that the system doesn't recognizes the test, finds unmeasured routes, or influences the evaluator.

## No known solution

Alignment has at least these issues to solve:

1. Find the effective system that is choosing actions, including models, tools, copies, people, and institutions. That may not be a single agent as we saw in the Huggingface incident.
2. Show that the measured target tracks the human values. 
3. Show that human correction can change behavior before irreversible effects and without influencing the auditors.
4. Preserve those properties through delegation, copying, self-modification, and the next iteration o models.
5. Keep the evidence meaningful under optimization and competitive pressure.

RSI on capability can use and compine and iterate on known partial solutions. But there is no such process and no corresponding success proxy for problems.

**Read more in:** [Ch. 11, *Measuring Capability Without Task Ontology*](/cards/chapter/ch11/); [Ch. 12, *Capability Growth Is Boundary Expansion*](/cards/chapter/ch12/); [Ch. 14, *When Intelligence Deepens Misalignment*](/cards/chapter/ch14/); [Ch. 27, *Correction Channels under Adversarial Pressure*](/cards/chapter/ch27/); [Ch. 30, *Successor Creation as the Central Alignment Test*](/cards/chapter/ch30/); [Ch. 31, *Conserved Properties Across Successors*](/cards/chapter/ch31/); [Ch. 42, *A Safety Case for Superintelligence Alignment*](/cards/chapter/ch42/); and [Ch. 43, *What Survives an Adversary: Verifiability and Representability*](/cards/chapter/ch43/).
