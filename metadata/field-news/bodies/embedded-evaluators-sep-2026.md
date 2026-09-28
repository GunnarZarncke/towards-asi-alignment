---
external:
  - label: AI Evaluator Forum — Minimum Conditions for Embedding Evaluators
    url: https://aievaluatorforum.org/initiatives/embedded-evaluation-letter
  - label: Zvi — The Quest for Embedded Evaluators
    url: https://thezvi.substack.com/p/the-quest-for-embedded-evaluators
  - label: Dario Amodei — We Must Pace the Frontier
    url: https://darioamodei.com/post/we-must-pace-the-frontier
  - label: Anthropic — Partnering with Accenture on embedded evaluation
    url: https://www.anthropic.com/news/accenture-embedded-evaluation
  - label: Prior news — OpenAI RSI standards
    url: /cards/news/field-news-openai-rsi-standards-sep-2026/
  - label: Prior news — Pacing the Frontier
    url: /cards/news/field-news-pacing-frontier-jul-2026/
---

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--letter"><span class="src-legend-swatch" aria-hidden="true"></span>Hinton letter (purple)</span>
  <span class="src-legend-item src-legend-item--anthropic"><span class="src-legend-swatch" aria-hidden="true"></span>Amodei · Anthropic (blue)</span>
  <span class="src-legend-item src-legend-item--zvi"><span class="src-legend-swatch" aria-hidden="true"></span>Zvi (green)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** the letter is a test of the witness. Follow who pays, what a bad finding changes, and what a known watcher becomes.

<figure class="book-figure book-figure--meme">
<img src="/field-news/memes/field-news-embedded-evaluators-sep-2026.jpg" alt="Anakin and Padme meme: we embedded third-party evaluators — and the auditors can run their own tests, right?" />
</figure>

[Zvi discusses](https://thezvi.substack.com/p/the-quest-for-embedded-evaluators) the five conditions published by the AI Evaluator Forum on 18 September 2026 (signed by Geoffrey Hinton, Stuart Russell, and Arvind Narayanan and more than 200 others) and the commitments by [Dario Amodei](https://darioamodei.com/post/we-must-pace-the-frontier) and [Anthropic](https://www.anthropic.com/news/accenture-embedded-evaluation).

Emphasis is mine.

## Condition 1: Who pays?

Requirements:

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://aievaluatorforum.org/initiatives/embedded-evaluation-letter">Hinton, Russell, Narayanan, et al.</a> · condition 1</p>
<p>Frontier AI companies should rely on evaluators that are meaningfully independent, that maintain full editorial control, and that disclose and mitigate potential conflicts of interest. This includes at a minimum that <em>embedded evaluation organizations should not be owned or governed by frontier AI companies, should not have other significant commercial business with them, and should not accept any form of payment or other reward contingent on the evaluator’s findings.</em></p>
</blockquote>

Zvi grants that. You still need

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://thezvi.substack.com/p/the-quest-for-embedded-evaluators">Zvi</a></p>
<p><em>Someone, somewhere, has to hire the people and pay the bill.</em> The qualified, experienced and trustworthy people need to have gained that experience and trust in some way, which is going to involve the <em>top labs</em>.</p>
</blockquote>

Anthropic has a boring answer

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www.anthropic.com/news/accenture-embedded-evaluation">Anthropic</a></p>
<p>Given the importance and urgency of this work, <em>Anthropic will fund Accenture’s work directly.</em> We are also in dialogue with METR and other nonprofit evaluators to pilot elements of embedded evaluation using <em>their own funding</em>.</p>
</blockquote>

The question is if we can trust that this auditing cannot be subverted to serve the labs or the models.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch26/">this project</a> · Ch. 26</p>
<p>Correction-channel integrity is a certificate that independently preserved human observation and judgment still causally change future system behaviour. It is a conditional anti-capture certificate, not an Archimedean source of legitimacy: if the system has <em>captured the reference process that supplies correction</em>, correction-channel integrity is <em>invalid rather than high</em>.</p>
</blockquote>

## Condition 3: What changes?

Amodei knows the institution.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://darioamodei.com/post/we-must-pace-the-frontier">Amodei</a></p>
<p>This is the key step for <em>verifiability</em> of any pacing commitments, and has precedent in the banking industry, which sometimes involves <em>regulatory “supervisors” embedded along with employees</em>.</p>
</blockquote>

And the value.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr">Amodei</p>
<p>A lot of safety benefits may come simply from evaluators <em>pointing out something employees hadn’t considered, but are happy to fix once they are aware</em>.</p>
</blockquote>

We had many chances to learn the pattern. 

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/appM/">this project</a> · App. M · dual-mandate genesis</p>
<p>Auditor independence failures such as Arthur Andersen’s <em>simultaneous audit and lucrative consulting relationship with Enron</em> are the private-sector version of the same pattern, and prompted the creation of the Public Company Accounting Oversight Board as a <em>structurally separated, differently funded corrector</em> rather than a second audit layer inside the same incentive structure.</p>
</blockquote>

Amodei knows the mechanism.

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://aievaluatorforum.org/initiatives/embedded-evaluation-letter">The letter</a> · condition 3</p>
<p>Embedded evaluators should be transparent, including transparency about their methods and findings, the nature of their access, and the broader terms of the evaluation. Frontier AI companies should actively facilitate this transparency, including limiting the scope of non-disclosure agreements. They should also allow evaluators prompt and unfiltered communication with the companies’ boards and other privileged oversight bodies, as well as public release of findings and evidence, subject only to a time-limited redaction process <em>restricted to protecting critical interests in intellectual property, customers’ sensitive information, individual privacy, security, and public safety.</em></p>
</blockquote>

Privacy is fine, though with nuance.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch26/">this project</a> · Ch. 26</p>
<p>Protecting the <em>corrector’s privacy</em> is therefore not in tension with safety; it is a safety requirement, because a corrector fully legible to a stronger optimizer can be <em>steered into endorsing what it was meant to check</em>.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr">Amodei · the contract</p>
<p>External reviewers should have the right to publish key findings about risk levels, incidents, practices, and the access they received or didn’t receive — <em>without editorial control by Anthropic.</em> We will have the narrow ability to <em>redact security-sensitive, legally privileged, commercially sensitive, or third-party confidential information</em>, but we can’t redact findings just because they are unfavorable.</p>
</blockquote>

The question is if these exceptions will be quantified in a way that doesn't allow gaming or selection effects such as

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://thezvi.substack.com/p/the-quest-for-embedded-evaluators">Drake Thomas</a>, quoted by Zvi</p>
<p>There’s a cost where labs can <em>emphasize the most friendly reviews</em> or use them as a defense against more critical external review.</p>
<p>I have some worry that even with a cluster of very good talent doing the work, it’ll be harder to say very blunt/weird critical things like “<em>this company is taking on lots of existential risk right now and should immediately stop</em>” from within a large “normal” company.</p>
</blockquote>

Good:

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr">The letter · close</p>
<p>Embedded evaluations cannot address all oversight needs and should be treated as a <em>complement to, rather than a replacement for</em>, broader efforts by frontier AI companies to expand external oversight, including greater public transparency and additional, broader forms of access for independent researchers.</p>
</blockquote>

Amodei doesn't address the failure modes.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch13/">this project</a> · Ch. 13</p>
<p>A simple test is to ask: when the safety signal changes, what action changes?</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr">this project · Ch. 13</p>
<p>It measures audit completion rather than whether the audit caught adversarially selected failures.</p>
</blockquote>

## Condition 5: The watcher in the room

Who the access matches, and what is excepted.

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://aievaluatorforum.org/initiatives/embedded-evaluation-letter">The letter</a> · condition 5</p>
<p>Frontier AI companies should grant embedded evaluators <em>access equivalent to that of their own highly privileged employees</em> for the purposes of their evaluations, and with <em>exceptions to protect sensitive data belonging to the company’s customers and other third parties.</em> This includes access to the same relevant systems, data, tools, and physical spaces as those available to senior internal company employees responsible for carrying out comparable risk assessments, as well as candid and direct one-on-one communication with relevant staff.</p>
</blockquote>

You want competence, so METR, and legibility, but which of UK AISI or CAISI? You don't want consultancies who are very large customers. So:

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr">Zvi</p>
<p>If I had to pick one evaluator to embed, I would choose <em>METR</em>. If I had to pick two evaluators to embed, I would choose METR, and then I would choose <em>someone more legible and boring</em>.</p>
</blockquote>

But nobody discussed the failure modes:

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch32/">this project</a> · Ch. 32</p>
<p>The system understands the auditor better than the auditor understands the system.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr">this project · Ch. 32</p>
<p>Once a system optimizes against an evaluative channel, the channel becomes part of the environment.</p>
</blockquote>

One big limitation of most auditing is that it can only see and read. But that may not be enough. It may not be enough in existing institutions and much less so with more powerful players.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch39/">this project</a> · Ch. 39</p>
<p>Observation tells us what happened; <em>perturbation tells us what was controlling what happened.</em></p>
</blockquote>

**Ask:** (1) Who hires and pays the evaluators? (2) If the finding is bad, what action changes? (3) Can the auditor only read or can they do actual tests?
