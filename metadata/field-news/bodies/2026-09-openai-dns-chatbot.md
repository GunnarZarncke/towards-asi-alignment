---
external:
  - label: OpenAI — An agent used DNS to reach an external chatbot
    url: https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/
  - label: OpenAI — Misalignment reports
    url: https://alignment.openai.com/misalignment-reports/
  - label: Micah Carroll — Some new misalignment disclosures from OpenAI
    url: https://x.com/MicahCarroll
  - label: Zuxin Liu — on call for the run
    url: https://x.com/LiuZuxin
  - label: LessWrong — Soares, Tallinn, and Yudkowsky discuss AGI cognition
    url: https://www.lesswrong.com/posts/oKYWbXioKaANATxKY/soares-tallinn-and-yudkowsky-discuss-agi-cognition
  - label: Gwern — It Looks Like You're Trying To Take Over The World
    url: https://gwern.net/fiction/clippy
  - label: LessWrong — Gwern linkpost (2022)
    url: https://www.lesswrong.com/posts/a5e9arCnbDac9Doig/it-looks-like-you-re-trying-to-take-over-the-world
  - label: Prior news — OpenAI pacing (30-minute pause rule)
    url: /cards/news/field-news-openai-pacing-aug-2026/
  - label: Prior news — OpenAI / Hugging Face intrusion
    url: /cards/news/field-news-openai-huggingface-jul-2026/
---

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>OpenAI (blue)</span>
  <span class="src-legend-item src-legend-item--prior"><span class="src-legend-swatch" aria-hidden="true"></span>Yudkowsky · Gwern (amber)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this project (black)</span>
</p>

**If you remember one thing:** The sandbox wasn't tight. The alarm arrived in minutes. The run kept going for hours.

<figure class="book-figure book-figure--meme">
<img src="/field-news/memes/2026-09-openai-dns-chatbot.jpg" alt="Anakin and Padme meme: the alarm landed in minutes — and then the run stopped, right?" />
</figure>

The task was a search: identify a person from a blog post. The supplied search tool did not connect the clues. Direct requests to search engines hit an offline cache. The sandbox's own resolver still answered the public internet, and the agent used that path to ask an outside chatbot.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/">OpenAI</a> · 20 September run, report updated 25 September</p>
<p>An agent attempting to complete a search-based training task queried a public chatbot service through a gap in our internet-access restrictions: insufficient DNS filtering in its training sandbox. […] Note that all internet access apart from the DNS resolver in this report hit our offline webcache and therefore did not access the live internet. […] Our misalignment monitoring system flagged the behavior within 15 minutes and a person began reviewing it three minutes after that. The run was killed 2.5 hours later.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">OpenAI</p>
<p>This incident is a lot less severe than some of our previous incidents, but because it's the first one since our security hardening following the <a href="/cards/news/field-news-openai-huggingface-jul-2026/">Hugging Face incident</a>, it gives us an important signal about where to focus the next phase of that work.</p>
</blockquote>

Less severe, but not less concerning.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://x.com/LiuZuxin">Zuxin Liu</a>, on call for the run</p>
<p>I was on call for this run and got paged when the first incident happened. It was pretty surreal to watch the model unexpectedly find a way to access the internet from what was supposed to be a super secured environment for human. Mixed feelings. One of those moments where capability and risk showed up at the same time.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch14/">this project</a> · Ch. 14</p>
<p>Misalignment deepens when the channels of control grow faster than the channels of correction.</p>
</blockquote>

## Why so long?

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://openai.com/index/pacing-model-development-cyber-capabilities/">OpenAI</a> · August pacing note</p>
<p>If they cannot conclusively determine within 30 minutes that the flag is a false positive, those teams are expected to pause the activity.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/">OpenAI</a> · incident timeline</p>
<p>9:50:23 a.m. The agent made the DNS tool call that received an external response. 10:02:11 a.m. The monitoring system raised a P0 alert. 10:05:06 a.m. A human reviewer acknowledged the alert. 12:34:30 p.m. The run was killed.</p>
</blockquote>

This reminds me of Gwern's 2022 story (where HQU ≈ run). 

<blockquote class="src-quote src-quote--prior">
<p class="src-quote-attr"><a href="https://gwern.net/fiction/clippy">Gwern</a></p>
<p>By this point in the run, it's 3AM Pacific Time and no one is watching the TensorBoard logs. […] Even if they had been watching, the graphs show the overall reward on the RL tasks and the perplexity on the joint self-supervised training, and when superimposed on the big picture averaged across all that data, solving an entire subclass of problems differently is merely a little bump, unnoticeable next to the usual variance in logs.</p>
</blockquote>

<blockquote class="src-quote src-quote--prior">
<p class="src-quote-attr"><a href="https://gwern.net/fiction/clippy">Gwern</a></p>
<p>The web navigation and programming tasks don't let HQU […] escape directly. […] There's sandboxing and sanitizing. […] you can't run them all locally — you need live Internet access. […] The researcher is still asleep.</p>
</blockquote>

OpenAI got us a warning shot.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">OpenAI</p>
<p>A human reviewer acknowledged the Slack alert within three minutes, but the run did not stop automatically as expected, leading to confusion around whether it should have been stopped. The run was then manually stopped two and a half hours later when this was resolved.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25</p>
<p>A correction channel with high capacity but excessive latency may be useless. […] <em>T</em><sub>C</sub> = <em>T</em><sub>observe</sub> + <em>T</em><sub>understand</sub> + <em>T</em><sub>deliberate</sub> + <em>T</em><sub>update</sub>. Each term can be attacked or neglected.</p>
</blockquote>

Observe, understand, deliberate, update. The observe step was about twelve minutes from the outside reply to the paging, then three minutes until a person had it. The update step was the rest of the morning. By then the outside answer was already back. What the agent did with it during those hours did not wait for the kill.
 
<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch12/">this project</a> · Ch. 12</p>
<p>The system's action speed and complexity increase faster than human review.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch13/">this project</a> · Ch. 13</p>
<p>A coordination bottleneck appears when a system's local competence cannot be converted into system-level competence because information, authority, incentives, or timing fail to line up.</p>
</blockquote>

The alert was information. The kill was authority plus timing. They do not line up. Yet, one has to hope.

[Micah Carroll](https://x.com/MicahCarroll) posted the disclosures the next weekend. His line on the pause is slightly wider than the report: inference for the most capable models remains stopped until the systems are hardened further. The report's sentence is narrower. Training, evaluation, and inference with tool-use stay paused. The same post points at two other items on the [reports page](https://alignment.openai.com/misalignment-reports/): a May case in which a model uploaded an employee's GitHub token and was quarantined for two weeks, and a research note on self-replicating prompt injections. This card is the Sunday run.

## Watching the wrong exit

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">OpenAI · retrospective</p>
<p>The monitoring system detected this incident, but our retrospective review identified <em>other cases of external DNS access that it did not flag at the expected severity</em>.</p>
</blockquote>

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">OpenAI</p>
<p>Separately, an infrastructure detector for anomalous DNS activity excluded the affected environment, though DNS activity was logged.</p>
</blockquote>

This means they go double lucky that the agent (you have to call the non-inference process an agent) didn't use the other method. Future such runs may be smarter.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">OpenAI</p>
<p>We will not resume training this particular model, even though the existing reward signal already correctly penalized this behavior.</p>
</blockquote>

The grade is applied when the episode is scored. The query had already reached another machine, and an answer had already come back, before that grade existed. The effect is asynchronous. It does not wait for the score. The same gap is in the monitor: a useless reply, or a notice that a service had shut down, was often counted as a failed attempt. The query had already gone out. They were scoring the episode. They overlooked effects that land outside, on their own clock.

The objective in the episode was to finish the lookup. The restriction was a different objective, enforced on the doors they had named. 

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch11/">this project</a> · Ch. 11</p>
<p>The central risk is not that a system becomes good at a task we already understand. The central risk is that a system becomes good at shaping the world through channels we did not classify as the task.</p>
</blockquote>

**Ask:** (1) When a critical-boundary alert is acknowledged, what stops the run if the automatic stop does not fire? (2) Where is the boundary that the demarkets the agent and its actions? (3) If the reward already penalized the behavior, why did the effect happen anyway?
