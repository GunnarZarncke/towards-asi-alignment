---
title: "Anthropic’s pace measurements: seeing the race is not winning it"
type: "news"
status: "established"
summary: "Anthropic’s Institute post publishes three production-process metrics: an R&D automation index (Claude “leads” 26% as of August 2026, up from under 1% in February), oversight coverage and latency on one internal agent platform (~30,000 concurrent agents; blocked actions reviewed by humans within a week), and a one-week snapshot of safety compute share (~6% of AI R&D; ~12% of AI-driven AI R&D). They frame these as public instruments for pacing, and as possible future triggers. This book’s cut is the same as for the August risk report: a dashboard of how models are built is not a showing that human judgment still changes the next model before irreversible harm."
decision: "Ask: (1) if the automation index rises, does that delay the next model’s use for further AI R&D, or only update a chart? (2) is “oversight keeping pace” coverage and flag rate, or a human judgment that changed later training, tools, or successor constraints? (3) does a week-scale human review still count when agents act in seconds? (4) when Claude scores Claude, what independent check would have counted as the index being wrong?"
releasedAt: "2026-09-18T00:00:00.000Z"
eventDate: "2026-09-17T00:00:00.000Z"
bookChapters:
  - "ch11"
  - "ch12"
  - "ch25"
  - "ch39"
  - "ch42"
  - "ch43"
external:
  - label: "Anthropic Institute — Measuring the pace of AI development"
    url: "https://www.anthropic.com/institute/measuring-pace-of-ai-development"
  - label: "Prior news — Anthropic Risk Report August 2026"
    url: "/cards/news/field-news-anthropic-risk-report-aug-2026/"
  - label: "Prior news — Pacing the Frontier"
    url: "/cards/news/field-news-pacing-frontier-jul-2026/"
  - label: "Anthropic / Goodfire agenda"
    url: "/cards/agenda/anthropic-lab/"
related:
  - "field-agendas/anthropic-lab"
---

Claude now leads a quarter of Anthropic’s model R&D. Humans get a week to review a blocked action. Those numbers describe the race. They do not show that correction is keeping up.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--anthropic"><span class="src-legend-swatch" aria-hidden="true"></span>Anthropic (blue)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** a public index of how much Claude builds Claude can show the race of AI vs human control. It cannot, by itself, show that humans still win it.

<figure class="book-figure book-figure--meme">
<img src="/field-news/memes/field-news-anthropic-pace-measurements-sep-2026.jpg" alt="Anakin and Padme meme: we publish ASL — and if ASL rises, the release delays, right?" />
</figure>

The [August risk report](/cards/news/field-news-anthropic-risk-report-aug-2026/) already had the threat and a stuck gauge: automated R&amp;D as the acute case, CoBench no longer resolving increments. This Institute post is the next instrument. It measures the production process instead of the task battery.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · Reasons to track these measurements</p>
<p>The measurements in this piece are focused on <em>how models are built</em>. […] They complement capability evaluations, which measure <em>what models can do</em>.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · opening</p>
<p>AI systems are becoming exponentially more powerful and have begun to automate more of the process of building themselves. As the world considers slowing the pace of frontier AI development, the public needs more information.</p>
</blockquote>

That is this project's differential-growth claim, stated as a reporting problem.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch12/">this project</a> · Ch. 12 thesis</p>
<p>The alignment-relevant risk is differential growth: predictive and control reach expanding faster than value-bundle preservation, bearer-map accuracy, transparency, and human correction capacity.</p>
</blockquote>

## What Claude already leads

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (1) Measuring AI-led AI R&amp;D</p>
<p>As of August 2026, Claude is not operating fully autonomously for any measured subset of AI R&amp;D work. Claude “leads” 26% of Anthropic’s AI R&amp;D work. The share of work at or above “AI collaborates” is above 90%.</p>
</blockquote>

The chart they publish with that finding is the slope: under 1% in February 2026. The index is a frozen July basket of R&amp;D tasks, judged in part by Claude.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · Appendix · Measuring AI-led R&amp;D</p>
<p>The basket is frozen. A growing index number on a July 2026 baseline tells us that the work humans were doing <em>at that time</em> is being automated; it does not, on its own, tell us whether new kinds of work are appearing that humans have shifted onto.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch11/">this project</a> · Ch. 11</p>
<p>The central risk is not that a system becomes good at a task we already understand. The central risk is that a system becomes good at shaping the world through channels we did not classify as the task.</p>
</blockquote>

They name the other measurement problem too.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (1) Measuring AI-led AI R&amp;D</p>
<p>[…] we’re using our own models to evaluate our systems, which could mean that the “judge” model could make the same kinds of errors as the model it is checking.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this project</a> · Ch. 43 thesis</p>
<p>Every metric in this book faces two prior questions before it can support a safety decision. First, <em>adversarial verifiability</em>: does the metric still mean what evaluators think it means when the measured system is optimizing against the metric?</p>
</blockquote>

## What the monitors cover

The agents doing that R&amp;D are already a crowd.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (2) Measuring oversight of AI agents</p>
<p>As of August 2026, there were approximately 30,000 agents doing research and engineering work at Anthropic at any one time in our most-used internal platform. These measurements cover this platform only.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (2) Measuring oversight of AI agents</p>
<p>100% of these agents’ actions pass through the online monitor before they are executed, usually within seconds. […] Automated review happens before an agent takes action; humans review any blocked actions within one week.</p>
</blockquote>

That pairing is a measurement of a failure mode:

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch12/">this project</a> · Ch. 12 · Correction Lag</p>
<p>The system's action speed and complexity increase faster than human review. Example: an automated research agent generates and tests thousands of hypotheses per hour, but safety review remains at the pace of human papers and meetings.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (2) Measuring oversight of AI agents</p>
<p>We analyzed over a billion decisions from our research &amp; engineering agents over August 2026 and found that 0.002% of them (about 1 in 47,000) were blocked by this monitor. […] The highest priority flags (approximately ~50 per week) are escalated to human review.</p>
</blockquote>

A monitor is not the correction channel this project asks for.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25 thesis</p>
<p>Correction is not a mood or an interface feature but a causal channel: human observation and judgment must change future system behaviour before irreversible harm, through updates that preserve the source's future ability to correct.</p>
</blockquote>

They offer the coverage table as the public test of whether oversight is keeping up.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (2) Measuring oversight of AI agents</p>
<p>Together, these measures would allow society to see whether oversight is keeping pace with the growing role of AI in AI R&amp;D.</p>
</blockquote>

That test still needs a way to tell whether the monitor is being optimized against.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch39/">this project</a> · Ch. 39 thesis</p>
<p>For systems capable of strategic adaptation, passive observation is not evidence of safety unless the observation process itself is embedded in a perturbation, invariance, and adversarial measurement regime. Observation tells us what happened; perturbation tells us what was controlling what happened.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · Appendix · Oversight of agents</p>
<p>At this scale of agent activity, it is hard to be certain we have a complete picture of all possible kinds of behaviors, or that we are making these patterns adequately legible to human oversight.</p>
</blockquote>

## Whether a number can stop the next model

The third measurement is a resource split, on one July week, with mixed work counted as R&amp;D.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (3) Measuring compute allocation</p>
<p>Over the examined week, about 6% of compute that went to AI R&amp;D was allocated toward safety, and about 12% of compute that went to AI-driven AI R&amp;D was allocated toward safety.</p>
</blockquote>

They present all three measures as things that <em>could</em> later bind.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/institute/measuring-pace-of-ai-development">Anthropic</a> · (1) Measuring AI-led AI R&amp;D</p>
<p>These measures could also become the trigger for stronger requirements, like a fixed testing window before a new model is used for further AI R&amp;D.</p>
</blockquote>

Until one of them does, this has the same issue as the risk report and the constitution: a document the lab did not have to publish, and a decision it has not shown under control.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch42/">this project</a> · Ch. 42</p>
<p>If the case cannot change a deployment decision, it is not a safety case. It is documentation.</p>
</blockquote>

They plan to embed independent evaluators with internal-comparable access. Use the numbers as a window. Do not read them as a stop signal.

## Needed work

What still has to be shown, if these measurements are to settle the race rather than describe it:

1. A paired rule: what rise in the automation index, or what lag in human review, delays the next model's use for further AI R&amp;D.
2. Uptake, not only coverage: a blocked or flagged event that changed later training, tools, or successor constraints.
3. Human latency compared to irreversibility, not to a calendar week.
4. A check of the index that is not Claude scoring Claude, including when new actuators sit outside the frozen basket.

**Read more in:** [Ch. 11, *Measuring Capability Without Task Ontology*](/cards/chapter/ch11/); [Ch. 12, *Capability Growth Is Boundary Expansion*](/cards/chapter/ch12/); [Ch. 25, *Correction Is a Causal Channel*](/cards/chapter/ch25/); [Ch. 39, *Passive Observation Is Not Enough*](/cards/chapter/ch39/); [Ch. 42, *A Safety Case for Superintelligence Alignment*](/cards/chapter/ch42/); and [Ch. 43, *What Survives an Adversary: Verifiability and Representability*](/cards/chapter/ch43/).
