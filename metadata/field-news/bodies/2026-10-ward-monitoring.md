---
external:
  - label: Ward — An overview of frontier AI company monitoring practices in mid 2026
    url: https://www.lesswrong.com/posts/E4Jpmo3igPnGnXtL4/an-overview-of-frontier-ai-company-monitoring-practices-in
  - label: OpenAI — Auto-review
    url: https://alignment.openai.com/auto-review/
  - label: OpenAI — Pacing on cyber capabilities (18 August 2026)
    url: https://openai.com/index/pacing-model-development-cyber-capabilities/
  - label: OpenAI — How we monitor internal coding agents
    url: https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/
  - label: Google DeepMind — Securing the future of AI agents
    url: https://deepmind.google/blog/securing-the-future-of-ai-agents/
  - label: METR — Risk report, February–March 2026
    url: https://metr.org/risk-report-feb-mar-2026.pdf
  - label: Prior news — The alarm arrived in minutes
    url: /cards/news/field-news-openai-dns-chatbot-sep-2026/
  - label: Prior news — Anthropic’s pace measurements
    url: /cards/news/field-news-anthropic-pace-measurements-sep-2026/
  - label: Prior news — OpenAI’s monitoring tax
    url: /cards/news/field-news-openai-pacing-aug-2026/
---

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--ward"><span class="src-legend-swatch" aria-hidden="true"></span>Ward (teal)</span>
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>Labs (blue)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this project (black)</span>
</p>

**If you remember one thing:** A response time, a response, disclosure, and a person on alert are good first steps. What is open, is bounding what can get through before a response on an alert.

<figure class="book-figure book-figure--meme">
<img src="/field-news/memes/2026-10-ward-monitoring.jpg" alt="Anakin and Padme meme: the monitors are on — so nothing can slip past, right?" />
</figure>

On 7 October Francis Rhys Ward published a single public inventory of how Anthropic, OpenAI, and Google DeepMind watch agents deployed inside the lab. He is explicit about the job, and about Google DeepMind’s column.

<blockquote class="src-quote src-quote--ward">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/E4Jpmo3igPnGnXtL4/an-overview-of-frontier-ai-company-monitoring-practices-in">Ward</a> · opening</p>
<p>This document provides an overview of publicly available evidence regarding the monitoring practices of internally deployed agents within frontier AI companies (focusing on OAI, Anthropic, and GDM).</p>
<p>In general, there is limited public evidence about GDM monitoring practices. Much of the information herein comes from the GDM control roadmap, which is a plan that makes suggestions but does not make claims about GDM’s actual practices.</p>
</blockquote>

That inventory is a step in the right direction. Practices that used to live in separate system cards can now be lined up. Some prior steps have been discussed here ([pace measurements](/cards/news/field-news-anthropic-pace-measurements-sep-2026/), [the August hold](/cards/news/field-news-openai-pacing-aug-2026/)). What follows takes each practice Ward was able to document as a step on an open alignment problem, and says what is still open.

## A response time

<blockquote class="src-quote src-quote--ward">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/E4Jpmo3igPnGnXtL4/an-overview-of-frontier-ai-company-monitoring-practices-in">Ward</a> · claim 1</p>
<p>Transcripts are primarily monitored asynchronously/offline.</p>
</blockquote>

The labs have started to say how late.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf">Anthropic, August 2026</a>, p. 76, as quoted by Ward</p>
<p>Our main form of asynchronous monitoring is an automated offline monitoring pipeline.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/">OpenAI, March 2026</a>, as quoted by Ward</p>
<p>our monitoring system reviews interactions within 30 minutes of completion</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/pacing-model-development-cyber-capabilities/">OpenAI, 18 August 2026</a></p>
<p>We aim to issue an alert within 30 minutes after concerning activity is surfaced through our monitoring system. […] If they cannot conclusively determine within 30 minutes that the flag is a false positive, those teams are expected to pause the activity.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://deepmind.google/blog/securing-the-future-of-ai-agents/">Google DeepMind, June 2026</a></p>
<p>For low-risk and reversible actions, we can rely on reviewing transcripts with a delay and remediating issues quickly after they occur (asynchronous response). For particularly high-risk actions, such as major cyber attacks, we must shift to real-time prevention, blocking harmful actions before they can be executed (synchronous response).</p>
</blockquote>

This is a real tightening of response and Ward’s reading of their roadmap is that synchronous monitoring is suggested starting at the next capability level, and that they build an internal prototype for it. THis will hopefully address latency.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25 · Latency</p>
<p>Correction must arrive before the relevant harm becomes irreversible. […] A correction channel with high capacity but excessive latency may be useless. […] For autonomous cyber operations, milliseconds may matter.</p>
</blockquote>

Will they compare correction time against harm time? Will a process that starts on a finished interaction can still be on time to undo effect? The [DNS-chatbot run](/cards/news/field-news-openai-dns-chatbot-sep-2026/) was a case where the outside answer was already back before the kill.

##What the Monitor sees

<blockquote class="src-quote src-quote--ward">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/E4Jpmo3igPnGnXtL4/an-overview-of-frontier-ai-company-monitoring-practices-in">Ward</a> · claim 3</p>
<p>Monitors receive the full agent transcript as input (including prompts, CoT, and tool calls).</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://deepmind.google/blog/securing-the-future-of-ai-agents/">Google DeepMind, June 2026</a></p>
<p>Today, we monitor a model’s visible chain-of-thought. However, as models learn to hide their reasoning — either through oversight awareness (knowing they are being monitored) or opaque reasoning (reasoning without using visible text) — simply reading their verbalized reasoning will not be enough. We will need to analyze their behavior and potentially inspect the model’s inner workings.</p>
</blockquote>

Naming the inputs is good. But it is mostly direct LLM outputs and scratchpads (and maybe the history of it). 

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this project</a> · Ch. 43</p>
<p>A system can move the reasoning that matters out of whatever text is being read—into encoded reasoning or steganographic chain-of-thought—so the monitored signal keeps its shape while losing its content.</p>
</blockquote>

The inputs also don't record effects of actions such as tool calls unless these show up in the conversation.

## Activations

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">Anthropic, on Mythos 5, as quoted by Ward · p. 163</p>
<p>[For Mythos 5] probes were run on every transcript during the majority of post-training.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/pacing-model-development-cyber-capabilities/">OpenAI, 18 August 2026</a>, as quoted by Ward</p>
<p>This new monitoring setup is multistage, starting with activation classifiers (detectors that inspect a model’s internal activity) that run at every sampled token. […] This monitoring is required for all RL training and evaluations involving tools for models of Sol capability or higher. […] we added an additional monitoring requirement for all inference of Astra with tools.</p>
<p>Our current estimates put monitoring overhead at roughly 20% of the inference compute being monitored.</p>
</blockquote>

That is a observation handle on another route.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch10/">this project</a> · Ch. 10</p>
<p>Model activations inside the boundary are one such route. They can steer even when logs, tools, and the text the system emits do not reach them.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this project</a> · Ch. 43</p>
<p>A measurement handle that reads those activations still leaves a green reading only as good as the cost of faking the handle.</p>
</blockquote>

## Named holes

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/">OpenAI, March 2026</a>, as quoted by Ward</p>
<p>A very small fraction of traffic (&lt;0.1%) primarily from bespoke or local setups is currently outside our monitoring coverage, and we are working to close that gap.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://alignment.openai.com/misalignment-reports/">OpenAI, September 2026</a>, as quoted by Ward</p>
<p>our misalignment monitoring system, which <emph>ran</emph> on 20% of the samples for this RL run</p>
<p>Our misalignment monitoring system, which <emph>runs</emph> on all training samples for models greater than or comparable to 5.6-sol capability which involve tools</p>
</blockquote>

Going from 20% to every tool-use training sample is a real improvement. Ward reports that the offline pipeline misses reinforcement learning and most evaluations, that custom scaffolds are sampled at about 5%, and that some non-coding use is logged and left out of offline monitoring. METR, in the February–March report, wrote that categories with lighter monitoring are a route an agent could use to avoid it.

This still only looks at single agent activities and doesn't seem suitable of the entity that acts is not (a single) LLM conversation as seen in <HF>.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://deepmind.google/blog/securing-the-future-of-ai-agents/">Google DeepMind, June 2026</a></p>
<p>we constantly measure performance across three critical metrics: coverage (the fraction of traffic monitored), recall (the fraction of misaligned behaviors caught), and time-to-response.</p>
</blockquote>

Bounding the unmonitored is good.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch10/">this project</a> · Ch. 10</p>
<p>If the system has unmonitored channels, broad background uncertainty, or redundant ways to achieve the same control, it may hide cheaply.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/appendix/appp/">this project</a> · Appendix P · Market 8</p>
<p>“The monitor sees everything consequential” is itself an empirical claim.</p>
</blockquote>

But the remaining questions is empirically measuring and defending the the bound is tight enough.

## The live filter says what it misses

Companies do run a classifier on actions as they happen. OpenAI’s version is specific about both the catch and the miss.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://alignment.openai.com/auto-review/">OpenAI, April 2026</a> · Auto-review</p>
<p>For the small fraction that need review, Auto-review approves around 99%.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://alignment.openai.com/auto-review/">OpenAI, April 2026</a> · Notes of Caution</p>
<p>it should not be understood as a mechanism for protecting against model scheming. Auto-review evaluates proposed out-of-sandbox actions at the point of escalation. A model that is strategically hiding its intent may still produce an escalation request that looks benign, or may act within the sandbox in ways Auto-review never sees.</p>
</blockquote>

Never sees or never flags. For example, because the effect is locally benign.

OpenAI also scored performance. They say they watch for attempts to game the reviewer, and they stop a trajectory after repeated denials. The disclaimer is the part that does the safety work: the live filter looks at the moment an action asks to leave the sandbox.

Anthropic:

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf">Anthropic, August 2026</a>, p. 83, as quoted by Ward</p>
<p>Neither were evaluated against the risk pathways... and we think it's likely that covered models would be able to bypass at least one of those</p>
</blockquote>

Or more generally:

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this project</a> · Ch. 43</p>
<p>None of that defense answers the question that decides whether the measurement is worth anything against a superintelligence: would the number still track the world if the system wanted it to read “safe”?</p>
</blockquote>


## The monitors

<blockquote class="src-quote src-quote--ward">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/E4Jpmo3igPnGnXtL4/an-overview-of-frontier-ai-company-monitoring-practices-in">Ward</a> · claim 5</p>
<p>Anthropic uses weaker monitors. […] OAI uses the best models as monitors. […] GDM uses weaker monitors. Monitor models are not disclosed.</p>
</blockquote>

It is good that they publish their choices. 
They each have good <emph>arguments</emph> for their designs. GDM's roadmap defines a detection level at which frontier models can no longer be reliably overseen by trusted models. But they don't seem to lay out a principled way to defend or empirically support their argument.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this project</a> · Ch. 43 thesis</p>
<p>…and the only general escape from unverifiability is to stop trying to read a property and instead bound the cost an adversary must pay to fake it. This chapter defines that cost relation; it does not establish the bound against a real adversary.</p>
</blockquote>

<blockquote class="src-quote src-quote--ward">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/E4Jpmo3igPnGnXtL4/an-overview-of-frontier-ai-company-monitoring-practices-in">Ward</a> · left out</p>
<p>Monitor performance and evaluation. For example, robustness to red-teaming, or evaluation of collusion propensity between agents and monitors. Monitor elicitation. E.g., are monitors fine-tuned or just prompted?</p>
</blockquote>

There is much work to be done.

## The human in the loop

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://metr.org/risk-report-feb-mar-2026.pdf">METR, May 2026</a>, as quoted by Ward</p>
<p>a large fraction of agent activity was not reviewed by any human ... We are not aware of any company imposing strict requirements about human oversight of agents in Feb–Mar 2026</p>
</blockquote>

People may se, but can they do something about it?

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25</p>
<p>A low-authority channel may still look active. It may produce tickets, meetings, dashboards, safety reports, appeal forms, labels, and policies. But if later system behaviour is almost unchanged, the channel is low authority.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch12/">this project</a> · Ch. 12 · Correction Lag</p>
<p>The system's action speed and complexity increase faster than human review.</p>
</blockquote>

It is still good that people do see and I hope that what they see know will help improving the process.
