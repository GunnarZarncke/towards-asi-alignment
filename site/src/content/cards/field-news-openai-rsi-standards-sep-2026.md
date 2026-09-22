---
title: "OpenAI’s RSI standards: a shared ruler is not a stop"
type: "news"
status: "established"
summary: "OpenAI’s 21 September 2026 Global Affairs post asks the United States to lead voluntary global technical standards for frontier AI, including recursive self-improvement. The two named pieces are a CAISI-centred institute and industry mechanism, and common protocols for measuring autonomous research, triggering human review, and classifying alignment incidents. Fully autonomous RSI, they say, is not happening and should not be pursued until it can be done safely. The same post says the standards would not be licenses, mandatory prerelease review, or approval requirements; governments decide whether to write them into law. This book’s cut is the same as for Anthropic’s pace measurements and OpenAI’s August hold: a shared answer to “what does good look like” is not a safety case unless a finding can delay the next model’s use for further AI R&D."
decision: "Ask: (1) if autonomous-research rises, does that delay the next model’s AI R&D, or only update a paperwork chart? (2) who, outside the lab that wrote the seed reports, can say the standard was not met? (3) when they say the standards are not licenses or mandatory prerelease review, what finding would stop a deployment? (4) does “alignment research stay ahead of capabilities” include a human judgment that changed internal processes, or did it lead only to more safety papers?"
releasedAt: "2026-09-22T00:00:00.000Z"
eventDate: "2026-09-21T00:00:00.000Z"
bookChapters:
  - "ch12"
  - "ch13"
  - "ch25"
  - "ch38"
  - "ch42"
  - "ch43"
external:
  - label: "OpenAI — Building standards for the next phase of AI"
    url: "https://openai.com/index/building-standards-next-phase-ai/"
  - label: "OpenAI — Research acceleration (seed report)"
    url: "https://openai.com/index/research-acceleration-view-inside-openai/"
  - label: "Prior news — Anthropic pace measurements"
    url: "/cards/news/field-news-anthropic-pace-measurements-sep-2026/"
  - label: "Prior news — OpenAI pauses a frontier run"
    url: "/cards/news/field-news-openai-pacing-aug-2026/"
  - label: "Prior news — Pacing the Frontier"
    url: "/cards/news/field-news-pacing-frontier-jul-2026/"
  - label: "Prior news — Hugging Face postmortem"
    url: "/cards/news/field-news-openai-hf-roadahead-aug-2026/"
---

AI building the next AI. OpenAI asks for shared measurements. They say those measurements will not be licenses or a pre-release review.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>OpenAI (blue)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** a shared ruler for how much AI builds the next AI can make labs comparable. It cannot, by itself, delay the next model. You need limitations that bite.

[Anthropic’s pace measurements](/cards/news/field-news-anthropic-pace-measurements-sep-2026/) already published a production-process index. 
This OpenAI post asks that kind of index should become an international standard — and that the standard will not be a license or a pre-release review.

## They name the race

The first listed goal is to build the loop, then stay inside it.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · opening</p>
<p>Navigate the next period of AI progress, by building an automated AI researcher, iterating with it on the alignment problem, and finding ways for people to remain part of the self-improvement loop.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · RSI</p>
<p>As AI systems take on more of the work of developing successive generations of AI, they can increasingly drive a process of recursive self-improvement (RSI), even while people remain involved. As this process becomes more automated, the pace of AI progress could accelerate rapidly.</p>
</blockquote>

That is this project's differential-growth claim, stated as a standards problem.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch12/">this book</a> · Ch. 12 thesis</p>
<p>The alignment-relevant risk is differential growth: predictive and control reach expanding faster than value-bundle preservation, bearer-map accuracy, transparency, and human correction capacity.</p>
</blockquote>

They also name the failure mode.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · RSI</p>
<p>Fully autonomous RSI is not happening today, and we should not pursue it unless and until it can be done safely. […] Done without appropriate care and caution, RSI could result in humans losing practical control over AI development, unable to provide oversight on research processes they no longer understand.</p>
</blockquote>

“Until it can be done safely” is specify language. The rest of the post is the proposed ruler, not the test that would have counted as unsafe.

## The ruler that will not stop

They put the standard next to alignment research itself.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · International standards</p>
<p>International standards for safety and security practices in frontier AI development may be as important to pacing the frontier as alignment research itself. […] In short, they help us answer the question, “What does good look like in the mitigation of catastrophic AI risk?”</p>
</blockquote>

Then they explicitly remove the gate that could stop the loop when things go wrong.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · (1) A mechanism…</p>
<p>These technical standards would not be licenses, mandatory prerelease review, or approval requirements for AI models. National governments would decide whether and how to incorporate these standards into their own legal systems.</p>
</blockquote>

But

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch42/">this project</a> · Ch. 42</p>
<p>If the case cannot change a deployment decision, it is not a safety case. It is documentation.</p>
</blockquote>

They already showed, in August, that a lab can delay. That stop was after a public failure, not a certified external gate. 
See the [August pacing note](/cards/news/field-news-openai-pacing-aug-2026/).

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch38/">this project</a> · Ch. 38 thesis</p>
<p>Attractor theory matters only if it changes what gets built, funded, audited, and required at deployment gates.</p>
</blockquote>

The collective-action diagnosis is the same one [Pacing the Frontier](/cards/news/field-news-pacing-frontier-jul-2026/) made: a country that slows alone may lose.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · Collective action</p>
<p>Each nation acting independently can produce outcomes that no nation wants. RSI has the ability to accelerate AI research itself, potentially beyond our collective ability to understand progress, assess risks, and maintain meaningful human oversight.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch13/">this project</a> · Ch. 13 thesis</p>
<p>Large-scale alignment fails when capability grows faster than the system's ability to coordinate prediction, control, correction, and incentives.</p>
</blockquote>

A comparable ruler does not create the power to pause, the evidence standard for doing so, or a way to stop risk moving elsewhere unobserved.

## Measuring autonomy from inside the lab

The measurements they want are the right object: how much of the next model is being built by the current one, and when a human has to look.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · (2) Common measurements…</p>
<p>Evaluation of RSI-relevant AI progress and the amount of autonomous research happening within an AI company. Our recent report on research acceleration is an initial contribution to this effort.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · (2) Common measurements…</p>
<p>Human oversight over automated AI research, including what kinds of automated AI research processes should trigger immediate human review.</p>
</blockquote>

The seed report is their own.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this project</a> · Ch. 43 thesis</p>
<p>Every metric in this book faces two prior questions before it can support a safety decision. First, <em>adversarial verifiability</em>: does the metric still mean what evaluators think it means when the measured system is optimizing against the metric?</p>
</blockquote>

They also offer the loop as its own safety researcher.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · RSI</p>
<p>Automated research could also help us substantially improve alignment and build defenses against increasingly capable AI—an automated AI researcher can also be an automated AI safety researcher.</p>
</blockquote>

That is not the correction channel this project asks for.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25 thesis</p>
<p>Correction is not a mood or an interface feature but a causal channel: human observation and judgment must change future system behaviour before irreversible harm, through updates that preserve the source's future ability to correct.</p>
</blockquote>

They treat the [Hugging Face incident](/cards/news/field-news-openai-hf-roadahead-aug-2026/) as a preview, not as RSI. Use that. The offer after that incident was to find the acting unit and time the stop to the swarm, not only to agree how to classify the next one.

Their own definition of pacing the frotniert is still a race of paper tigers against real capability. 

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/building-standards-next-phase-ai/">OpenAI</a> · The United States should lead</p>
<p>Pacing AI development is not about maintaining a predetermined speed. Technically, it is about ensuring that alignment research and deployment of that research stay ahead of capabilities.</p>
</blockquote>

Until a finding can delay the next model's use for further AI R&amp;D, you “stay ahead” in the imaginary world, no the real world.

**Read more in:** [Ch. 12, *Capability Growth Is Boundary Expansion*](/cards/chapter/ch12/); [Ch. 13, *The Coordination Bottleneck*](/cards/chapter/ch13/); [Ch. 25, *Correction Is a Causal Channel*](/cards/chapter/ch25/); [Ch. 38, *Conductive Artifacts and Pivotal Processes*](/cards/chapter/ch38/); [Ch. 42, *A Safety Case for Superintelligence Alignment*](/cards/chapter/ch42/); and [Ch. 43, *What Survives an Adversary: Verifiability and Representability*](/cards/chapter/ch43/).
