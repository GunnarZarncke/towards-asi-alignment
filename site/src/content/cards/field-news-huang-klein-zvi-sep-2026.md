---
title: "Jensen Huang said: \"If your product might kill everyone then just stop.\""
type: "news"
status: "established"
summary: "On 23 September 2026 Ezra Klein interviewed Jensen Huang at Nvidia headquarters. After the Hugging Face incident, Huang said labs that cannot contain experiments should shut down, that evaluation may soon cost ten times the training compute, and that unready products should not ship — with third-party auditors. Zvi's 25 September post treats those lines as binding standards and notes they would forbid today's frontier models. This project's cut: a stated rule is not a gate until containment, evaluation spend, and auditor findings can delay the next run without the lab grading its own test."
decision: "(1) If a lab says an experiment cannot be contained, does that stop the experiment? (2) What share of compute is adversarial evaluation? (3) Who outside the lab can enforce the share and its actual use?"
releasedAt: "2026-09-25T00:00:00.000Z"
eventDate: "2026-09-23T00:00:00.000Z"
bookChapters:
  - "ch02"
  - "ch38"
  - "ch13"
  - "ch25"
external:
  - label: "Ezra Klein Show — Jensen Huang vs. the A.I. Doomers (NYT transcript)"
    url: "https://www.nytimes.com/2026/09/23/opinion/ezra-klein-podcast-jensen-huang.html"
  - label: "Zvi — On Ezra Klein’s Podcast With Jensen Huang"
    url: "https://www.lesswrong.com/posts/j3xefrWrNqsmMfJEi/on-ezra-klein-s-podcast-with-jensen-huang"
  - label: "Prior news — Pacing the Frontier"
    url: "/cards/news/field-news-pacing-frontier-jul-2026/"
  - label: "Prior news — OpenAI / Hugging Face intrusion"
    url: "/cards/news/field-news-openai-huggingface-jul-2026/"
  - label: "Prior news — containment verification"
    url: "/cards/news/field-news-containment-verification-sep-2026/"
---

On Ezra Klein's show, Jensen Huang said labs should invest into safety and make products safe or be shut down. The hard part is to enforce external audits on the labs.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>Huang · NYT (blue)</span>
  <span class="src-legend-item src-legend-item--zvi"><span class="src-legend-swatch" aria-hidden="true"></span>Zvi (green)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** Jensen Huang said: "If your product might kill everyone then just stop." The task is to externally ensure the labs are doing it.

<figure class="book-figure book-figure--meme">
<img src="/field-news/memes/field-news-huang-klein-zvi-sep-2026.jpg" alt="Anakin and Padme meme: don't ship until ready — and someone outside can stop it, right?" />
</figure>

Ezra Klein, when discussing the [Hugging Face incident](/cards/news/field-news-openai-huggingface-jul-2026/), said the labs do not know how to contain that. 

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://www.nytimes.com/2026/09/23/opinion/ezra-klein-podcast-jensen-huang.html">Huang</a>, to Ezra Klein</p>
<p>Now, if they say the alternative, which is: There is no way to contain our experiments, there's just no way; when we test our A.I. models, it will get out, and it will damage the world — then I think the answer is that we have to shut the labs down.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/j3xefrWrNqsmMfJEi/on-ezra-klein-s-podcast-with-jensen-huang">Zvi</a></p>
<p>If your rule is "you cannot release a product that will damage the world" on the level of "hack into some websites" then you cannot release a frontier model.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch02/">this project</a> · Ch. 2</p>
<p>It may accept shutdown in the test while creating successors or dependencies outside the tested boundary.</p>
</blockquote>

How can that be prevented?

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">Huang</p>
<p>Now, they have so much market footprint, they have to shift their R.&amp;D., or total R.&amp;D., from just capability to a lot of verification, evaluation and testing. To the point where I wouldn't be surprised if the amount of compute necessary to develop these models increased by a factor of 10, because the evaluation is so rigorous.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr">Zvi</p>
<p>Can you imagine if us safety advocates said "I demand the frontier labs spend 90% of their R&amp;D compute on alignment, evaluation and verification"?</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch02/">this project</a> · Ch. 2</p>
<p>Once a benchmark matters, systems and organizations optimize for passing it. The benchmark may still be useful, but its meaning changes.</p>
</blockquote>

Klein then read the [Pacing the Frontier letter](/cards/news/field-news-pacing-frontier-jul-2026/) asking for time. 

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr">Huang, on the pace letter</p>
<p>Don't ship the product. If your product is not ready to ship, don't ship the product. [...] Third-party safety auditors, financial auditors — that's all great. That's terrific.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr">Zvi</p>
<p>Third, that he suggests we vote to tell them to slow down, and that he would support that, which is also known as democratic governance.</p>
</blockquote>

And external auditors.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch38/">this project</a> · Ch. 38</p>
<p>Can the executive explain what would stop release? Can the auditor reproduce the evidence?</p>
</blockquote>

**Ask:** (1) If a lab says an experiment cannot be contained, does that stop the experiment? (2) What share of compute is adversarial evaluation? (3) Who outside the lab can enforce the share and its actual use?

**Read more in:** [Ch. 2, *From Artificial Intelligence to Artificial Civilization*](/cards/chapter/ch02/); [Ch. 38, *Conductive Artifacts and Pivotal Processes*](/cards/chapter/ch38/); [Ch. 13, *The Coordination Bottleneck*](/cards/chapter/ch13/); and [Ch. 25, *Correction Is a Causal Channel*](/cards/chapter/ch25/).
