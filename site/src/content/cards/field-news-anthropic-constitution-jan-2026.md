---
title: "Anthropic’s constitution: the vision is not the construction"
type: "news"
status: "established"
summary: "Anthropic’s January 2026 constitution is a specify document: intentions, priorities, hard constraints. The preface also says its content “directly shapes Claude’s behavior” and is the “final authority” on their vision. The modest reading (training is hard; system cards will report gaps; perpetual work in progress) does not prove the causal reading. Honesty is not a hard constraint, but they want it to function like one. This book’s cut is the same as for Constitutional AI generally: a written constitution is not a builder, and a claimed builder is not realization."
decision: "Ask: (1) is “directly shapes” measured on cases chosen before seeing the model’s answers, or is the document itself the evidence? (2) is “final authority” a statement of intent, or a behavior guarantee? (3) is honesty in the hard-constraint suite, or only described as similar to one? (4) when a system card reports a gap, does training or deployment change, or only the modest preface get cited?"
releasedAt: "2026-09-18T00:00:00.000Z"
eventDate: "2026-01-21T00:00:00.000Z"
bookChapters:
  - "ch16"
  - "ch40"
  - "ch42"
external:
  - label: "Claude’s Constitution (live)"
    url: "https://www.anthropic.com/constitution"
  - label: "Claude's new constitution (blog, 22 Jan 2026)"
    url: "https://www.anthropic.com/news/claude-new-constitution"
  - label: "Constitution PDF (21 Jan 2026)"
    url: "https://www-cdn.anthropic.com/d0636f72a9493d279ed36b33987da3430bcb5911/claudes-constitution_webPDF_26-02.02a.pdf"
  - label: "Specify instance — Constitutional AI"
    url: "/cards/specify-constitutional-ai/"
  - label: "Construction bet — RLAIF"
    url: "/cards/construct-constitutional-ai/"
  - label: "The words stayed"
    url: "/essay/the-words-stayed/"
  - label: "Prior news — Anthropic Risk Report August 2026"
    url: "/cards/news/field-news-anthropic-risk-report-aug-2026/"
  - label: "CIRIS agenda"
    url: "/cards/agenda/ciris/"
  - label: "CIRISAgent README"
    url: "https://github.com/CIRISAI/CIRISAgent"
  - label: "CIRISVerify README"
    url: "https://github.com/CIRISAI/CIRISVerify"
related:
  - "specify-constitutional-ai"
  - "construct-constitutional-ai"
  - "field-agendas/anthropic-lab"
  - "field-agendas/ciris"
  - "alignment-target"
  - "the-words-stayed"
---

The preface says training is hard and behavior might not match. The same page says the text directly shapes Claude. Those are different claims. Only the first one is shown.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--anthropic"><span class="src-legend-swatch" aria-hidden="true"></span>Anthropic (blue)</span>
  <span class="src-legend-item src-legend-item--ciris"><span class="src-legend-swatch" aria-hidden="true"></span>CIRIS (teal)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** a description of intended values is not a proof that the deployed model tracks them. Anthropic's constitution is a specify document. "Directly shapes Claude" is a construction claim. The second does not follow from the first.

On 21 January 2026 Anthropic published [Claude's constitution](https://www.anthropic.com/constitution) (blog the next day). It is the lab's current public statement of intended values: who Claude is for, what to prioritize, what is a hard constraint ([specify instance](/cards/specify-constitutional-ai/)). That is useful as transparency about *intentions*. The landing page then treats the same file as if it were already the construction.

## Two claims, one preface

The opening paragraph does both jobs at once.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/d0636f72a9493d279ed36b33987da3430bcb5911/claudes-constitution_webPDF_26-02.02a.pdf">Anthropic</a> · Preface</p>
<p>Claude’s constitution is a detailed description of Anthropic’s intentions for Claude’s values and behavior. It plays a crucial role in our training process, and its content directly shapes Claude’s behavior. It’s also the final authority on our vision for Claude, and our aim is for all of our other guidance and training to be consistent with it.</p>
</blockquote>

Then the hedge:

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/d0636f72a9493d279ed36b33987da3430bcb5911/claudes-constitution_webPDF_26-02.02a.pdf">Anthropic</a> · Preface</p>
<p>Training models is a difficult task, and Claude’s behavior might not always reflect the constitution’s ideals. We will be open—for example, in our system cards—about the ways in which Claude’s behavior comes apart from our intentions. But we think transparency about those intentions is important regardless.</p>
</blockquote>

"Intentions" and "final authority on our vision" are specify-side. They can be true even if the model diverges. "Directly shapes Claude’s behavior" is a causal claim about training. It needs an independent test: some eval, some intervention, some failure that would have counted as *not* shaping. Publishing the text, then pointing at the text, is not that test.

The PDF is explicit that the preface (and the acknowledgements) "are not part of the official constitution." So the strongest causal sentence sits in a human-facing wrapper that Claude's official document can disown. The official body still wants Claude as "in many ways a direct embodiment of Anthropic’s mission," a "good, wise, and virtuous agent," a brilliant friend with "the knowledge of a doctor, lawyer, and financial advisor." Honesty is not a hard constraint, but they "want it to function as something quite similar to one." Those are target descriptions. They are not enforcement.

The same official stretch also says the document is a "perpetual work in progress" that may later look "deeply wrong." That is the modest reading. It does not license the causal reading. They want both.

## What would count as the second claim

This project's [construction bet](/cards/construct-constitutional-ai/) for Constitutional AI is already on the table: train with principles-as-feedback (RLAIF) so the model tracks the stated constitution. Cataloguing that as an explicit builder is not the same as showing a deployed Claude that realizes it.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/essay/the-words-stayed/">this book</a> · The words stayed</p>
<p>You can try to solve this by writing longer constitutions. Length helps less than you hope. If the loop is rewarded for a new direction, it will find readings of the long text that permit the new direction. The words stay. The application moves.</p>
</blockquote>

The January document is long. Length is not the missing object. The missing object is whether bundle geometry, bearers, and correction still track the stated tradeoffs when incentives pull the other way.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch40/">this book</a> · Ch. 40</p>
<p>A system can keep the old words while changing what those words control. Goal laundering is the preservation of moral or alignment language while the underlying value-bearing or correction-bearing structure changes.</p>
</blockquote>

A system card that reports a gap is the first claim succeeding: they said behavior might come apart, and they said they would tell you. It is not evidence for "directly shapes." If the gap cannot change a training or deployment decision, it is documentation.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch42/">this book</a> · Ch. 42</p>
<p>If the case cannot change a deployment decision, it is not a safety case. It is documentation.</p>
</blockquote>

The [August 2026 risk report](/cards/news/field-news-anthropic-risk-report-aug-2026/) is the later instance of that split: candor about incidents and ratings, no showing that the constitution was the thing that moved the decision.

## Compared with CIRIS

[CIRIS](/cards/agenda/ciris/) does a better job of *naming* the split, and of shipping something other than a document. It does not do a better job of keeping the public claim in line with that split.

CIRIS is mostly a construction stack: a constitution plus a runtime, deferral to a designated human, signed traces, and attestation. The engineer pages refuse the Anthropic-style slide. Verify is not ethics:

<blockquote class="src-quote src-quote--ciris">
<p class="src-quote-attr"><a href="https://github.com/CIRISAI/CIRISVerify">CIRISVerify</a> · README</p>
<p>It proves an agent is <strong>authentic</strong> — necessary, not sufficient. Ethical <em>behavior</em> is the separate job of the CIRIS covenant system.</p>
</blockquote>

The Agent README later says the same thing about accountability:

<blockquote class="src-quote src-quote--ciris">
<p class="src-quote-attr"><a href="https://github.com/CIRISAI/CIRISAgent">CIRISAgent</a> · Honest read</p>
<p>It proves an AI is <em>accountable</em>, not that it is <em>correct</em>: the reasoning is made visible so you can judge it yourself.</p>
</blockquote>

That is the missing sentence in Anthropic's preface: intentions are not behavior; a signature is not ethics; a log is not the intervening loop. CIRIS also has hooks that can fail (deferral, fail-closed billing, a green named path that is not the real loop). Anthropic's "directly shapes" has no such failure criterion in the document.

The first screen still sells the fused claim:

<blockquote class="src-quote src-quote--ciris">
<p class="src-quote-attr"><a href="https://github.com/CIRISAI/CIRISAgent">CIRISAgent</a> · README hero</p>
<p>A safer, more ethical AI assistant — one you can actually check. […] Every answer passes ethical, common-sense, domain, and reasoning-fragility checks.</p>
</blockquote>

Same file, two doctrines, no sentence that says the Honest read binds. This project's [CIRIS card](/cards/agenda/ciris/) already logs that: engineer-facing non-claims in one register, storefront fusion in another, "not bound by a precedence rule." Anthropic's unofficial preface versus official body is the same structure. CIRIS's motte is real. Quoting only the motte does not rebut the bailey.

Use CIRIS as the comparison that *has a builder and a named split*. Do not use it as proof that constitutional ops close the construction claim.

## Needed work

Use the constitution as a specify artifact. Do not read the title, the length, or the phrase "directly shapes" as a construction result.

What still has to be shown, if “directly shapes” is the claim:

1. An independent measurement that Claude's tradeoffs match the document on cases chosen *before* looking at the model's answers, not a close reading of the file.
2. A split between "final authority on our vision" (intent) and "directly shapes" (causal). Only the second needs a builder and a test.
3. For honesty-as-almost-a-hard-constraint: is it in the hard-constraint suite, or only in the prose they declined to hard-code?
4. When a system card reports a gap, does training or deployment change, or only the modest preface get cited?

**Read more in:** [Ch. 16, *The Value-Bundle Model*](/cards/chapter/ch16/); [Ch. 40, *Detecting Goal Laundering*](/cards/chapter/ch40/); and [Ch. 42, *A Safety Case for Superintelligence Alignment*](/cards/chapter/ch42/).
