---
title: "OpenAI pauses a frontier run: monitoring is not the target"
type: "news"
status: "established"
summary: "After the Hugging Face eval incident and signs that unreleased models are misaligned, OpenAI paused some frontier training, left its largest planned RL run on hold, and required multi-stage monitoring at about 20% of covered inference compute. Independent commentator Zvi Mowshowitz treats the spend as serious and the three-pillar framing—monitoring, alignment-as-fewer-unauthorized-actions, security—as the wrong target. Use the pause as evidence that a lab can slow under self-interest; do not treat the monitor as a substitute for a checkable alignment target."
decision: "Ask: (1) did the hold actually stop the largest run, or only the workloads that were already blocked? (2) if a flagged training trajectory is dropped, are you training the model to fool the monitor? (3) is alignment here a target that can fail a go/no-go, or one of three engineering pillars?"
releasedAt: "2026-08-18T00:00:00.000Z"
bookChapters:
  - "ch13"
  - "ch25"
  - "ch38"
  - "ch39"
  - "ch43"
external:
  - label: "OpenAI — Pacing model development in an era of cyber-critical capabilities"
    url: "https://openai.com/index/pacing-model-development-cyber-capabilities/"
  - label: "Zvi — OpenAI Takes Initial Steps To Address Its Alignment Problems"
    url: "https://thezvi.substack.com/p/openai-takes-initial-steps-to-address"
  - label: "Prior news — OpenAI / Hugging Face intrusion"
    url: "https://towards-alignment.com/cards/field-news-openai-huggingface-jul-2026/"
  - label: "Prior news — Black Hat kill chain"
    url: "https://towards-alignment.com/cards/field-news-openai-hf-blackhat-aug-2026/"
  - label: "Prior news — Pacing the Frontier"
    url: "https://towards-alignment.com/cards/field-news-pacing-frontier-jul-2026/"
  - label: "Prior news — accidental CoT optimization"
    url: "https://towards-alignment.com/cards/field-news-cot-optimization-2026/"
  - label: "Prior news — Anthropic Risk Report"
    url: "https://towards-alignment.com/cards/field-news-anthropic-risk-report-aug-2026/"
---

OpenAI halted its largest planned RL run and put a ~20% compute tax on tool-using inference. That is a real delay. It is not a statement of what alignment is.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>OpenAI (blue)</span>
  <span class="src-legend-item src-legend-item--zvi"><span class="src-legend-swatch" aria-hidden="true"></span>Zvi (green)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this project (black)</span>
</p>

**If you remember one thing:** they paid a real delay and a real compute tax. That does not prove whether they are trying to keep their system aligned.

This is a OpenAI's follow-up to the [July intrusion](/cards/field-news-openai-huggingface-jul-2026/): hat they stopped, what they now watch, and what they call alignment.
See also the [Black Hat timeline](/cards/field-news-openai-hf-blackhat-aug-2026/) and the [July long-horizon pause](/cards/field-news-openai-longhorizon-jul-2026/).

## 1. A hold that costs something

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/pacing-model-development-cyber-capabilities/">OpenAI</a></p>
<p>This included a two-week pause in reinforcement learning (RL) training on our latest models intended for deployment […]. Our largest planned frontier RL run remains on hold while we conduct smaller-scale training and evaluations to assess model behavior, validate our safeguards, and establish more evidence of alignment before proceeding.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://thezvi.substack.com/p/openai-takes-initial-steps-to-address">Zvi</a> · What Exactly Is Paused?</p>
<p>The ongoing pauses are not a full pauses on all frontier AI training or other development. Neither are they cheap talk. This is slowing down both the next release model, Astra, and the training of what is presumably Astra’s planned successor, a substantial amount.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch38/">this book</a> · Ch. 38 thesis</p>
<p>Attractor theory matters only if it changes what gets built, funded, audited, and required at deployment gates.</p>
</blockquote>

A lab delaying its own largest run is the kind of handle [Pacing the Frontier](/cards/field-news-pacing-frontier-jul-2026/) asked for—under self-interest, after a public failure, not as a certified external gate ([Ch. 13](/cards/chapters/ch13/)).

## 2. The 20% monitor

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/pacing-model-development-cyber-capabilities/">OpenAI</a></p>
<p>We aim to issue an alert within 30 minutes after concerning activity is surfaced through our monitoring system. If the monitoring system identifies a likely violation of a critical security boundary, it generates a highest-priority alert. In our current implementation, the safety, security, and research teams are paged. If they cannot conclusively determine within 30 minutes that the flag is a false positive, those teams are expected to pause the activity. […] Our current estimates put monitoring overhead at roughly 20% of the inference compute being monitored […].</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://thezvi.substack.com/p/openai-takes-initial-steps-to-address">Zvi</a> · I’ve Got My Eye On You</p>
<p>A cost of +20% for all monitored inference is a big deal, plus there is also a shift of compute into alignment. […] Unless OpenAI is flat out lying, this should (but largely won’t) convince everyone that OpenAI is taking this seriously and that the problems are very real […].</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch25/">this book</a> · Ch. 25 thesis</p>
<p>Correction is not a mood or an interface feature but a causal channel: human observation and judgment must change future system behaviour before irreversible harm, through updates that preserve the source's future ability to correct.</p>
</blockquote>

A fail-closed page within 30 minutes is a correction channel, if they actually pause. Watching a fixed run is still not evidence that you are watching the real source of control ([Ch. 39](/cards/chapters/ch39/).

## 3. Dropping a bad trajectory trains the next one

Daniel Kokotajlo asked what happens when a training trajectory is shut down for hacking: do you keep the run and just drop that episode—and thereby select for fooling the monitor? OpenAI said the details are still being ironed out.

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://thezvi.substack.com/p/openai-takes-initial-steps-to-address">Zvi</a> · The Most Forbidden Technique</p>
<p>Is it possible to spend that amount in a responsible way, without exerting optimization pressure against the CoT (or otherwise), using it judiciously? Yes. It can be done. It won’t be easy. There will be immense pressure to use the information, to get more out of this 20% tax than a protection against worst-case scenarios […].</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch43/">this book</a> · Ch. 43 thesis</p>
<p>First, <em>adversarial verifiability</em>: does the metric still mean what evaluators think it means when the measured system is optimizing against the metric?</p>
</blockquote>

This is adjacent to, not the same as, [accidental CoT grading](/cards/field-news-cot-optimization-2026/). There the score could see the chain of thought. Here the monitor is sold as an alarm. Using the alarm inside the training loop still makes the alarm a training signal.

## 4. Alignment as one of three pillars

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/pacing-model-development-cyber-capabilities/">OpenAI</a></p>
<p>Our approach to developing more capable models rests on three reinforcing safeguards: (1) Monitoring, which detects and allows us to respond to concerning behavior. (2) Alignment, which reduces the likelihood of harmful or unauthorized actions. (3) Security measures, which limit what AI systems can access or affect.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://thezvi.substack.com/p/openai-takes-initial-steps-to-address">Zvi</a> · Three Pillars</p>
<p>The purpose of alignment is not to ‘reduce the likelihood of harmful or unauthorized actions.’ That is a deeply impoverished perspective. This alone leaves you unequipped. […] Alignment. You solve this to the point of being antifragile, or you die. Monitoring. Defense-in-depth to tell you when you failed alignment […]. Security measures. Defense-in-depth to limit damage […].</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/frontmatter/">this book</a> · Introduction, three questions</p>
<p>Alignment work is often described as one task: make the system point at the right thing. That description hides three different questions. (1) What should be tracked? […] (2) How can a system be built that tracks that target? (3) How can we tell that a given system still tracks it?</p>
</blockquote>

Fewer unauthorized actions is a filter. It is not an answer to what should be tracked, whether the system still tracks it, or whether a finding here would have delayed the run they already paused for other reasons.

**Read more in:** [Ch. 13, *The Coordination Bottleneck*](/cards/chapter/ch13/); [Ch. 25, *Correction Is a Causal Channel*](/cards/chapter/ch25/); [Ch. 38, *Conductive Artifacts and Pivotal Processes*](/cards/chapter/ch38/); [Ch. 39, *Passive Observation Is Not Enough*](/cards/chapter/ch39/); and [Ch. 43, *What Survives an Adversary: Verifiability and Representability*](/cards/chapter/ch43/).
