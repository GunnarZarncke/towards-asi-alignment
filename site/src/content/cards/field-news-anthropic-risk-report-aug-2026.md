---
title: "Anthropic’s August 2026 Risk Report: what ‘low’ does not settle"
type: "news"
status: "established"
summary: "Anthropic’s August 2026 Risk Report (through 15 July) raises its misalignment rating from very low to low, discloses an unreleased internal model called Model 2, and describes training and monitoring failures. Independent commentator Zvi Mowshowitz treats the candor as useful and the remaining risk as higher than ‘very low.’ For a deployment or oversight decision: use the report as evidence of what the lab is willing to say and where it is already using the model. Do not treat the ‘low’ label as proof that humans can still catch and reverse a dangerous course, that the safety tests still measure what they claim, or that an independent party reviewed this version."
decision: "Before treating this report as a green light, ask: (1) is the more capable model already running inside the organization with weaker checks than a public release? (2) would any finding in the report have delayed that internal use? (3) who, outside the company, actually reviewed it? (4) do the safety tests still move when the model gets better?"
releasedAt: "2026-08-19T00:00:00.000Z"
eventDate: "2026-08-14T00:00:00.000Z"
bookChapters:
  - "ch07"
  - "ch12"
  - "ch25"
  - "ch33"
  - "ch39"
  - "ch42"
external:
  - label: "Anthropic — Risk Report August 2026 (redacted PDF)"
    url: "https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf"
  - label: "Anthropic — RSP / risk-report landing"
    url: "https://www.anthropic.com/responsible-scaling-policy"
  - label: "Zvi — Anthropic Risk Report August 2026 (LessWrong)"
    url: "https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026"
  - label: "Technical notes (this book)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/drafts/anthropic-risk-report-aug-2026-analysis.md"
  - label: "Prior news — Mythos withheld"
    url: "https://towards-alignment.com/cards/field-news-mythos-withheld-apr-2026/"
  - label: "Prior news — accidental CoT optimization"
    url: "https://towards-alignment.com/cards/field-news-cot-optimization-2026/"
  - label: "Prior news — METR internal-agent risk"
    url: "https://towards-alignment.com/cards/field-news-metr-frontier-risk-may-2026/"
---

Anthropic’s strongest model is already in daily internal use. The public rating is ‘low,’ while several of the tests behind that rating no longer keep up with the models.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--anthropic"><span class="src-legend-swatch" aria-hidden="true"></span>Anthropic (blue)</span>
  <span class="src-legend-item src-legend-item--zvi"><span class="src-legend-swatch" aria-hidden="true"></span>Zvi (green)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** the most capable system discussed here is already writing most of Anthropic’s production code. The public “low” rating did not have to clear that internal use.

A candid lab report is valuable. It is not the same thing as a finding that would force a pause. Publishing mistakes, holding a model back from the public, and scoring risk as “low” can all be true at once. The decision that matters is whether anyone with authority would have had to slow down *inside* the company.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=7">Anthropic</a> · §1 · p. 7</p>
<p>This report evaluates the degree to which Anthropic’s AI systems pose catastrophic risk in several categories, in light of what we know about both their capabilities and the measures we have in place for mitigating risk. […] This report is not scoped to a single AI model. Rather, it is a risk assessment of Anthropic’s activities as a whole.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch42/">this book</a> · Ch. 42 thesis</p>
<p>A safety case for superintelligence alignment is not a certificate of solved alignment. It is a structured refusal test: a graph of claims, evidence, bridge assumptions, adversarial-verifiability labels, and stop conditions […] If any load-bearing leaf is unsupported, the root claim fails.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch42/">this book</a> · Ch. 42</p>
<p>If the case cannot change a deployment decision, it is not a safety case. It is documentation.</p>
</blockquote>

Suppose every table in the report stayed exactly this green. Would that tell you that staff can still stop a dangerous course, that the tests still measure further progress, or that an outsider checked this version? Those are the questions a go/no-go needs. This report is not written as that kind of test.

## What an outside reader took from it

Zvi Mowshowitz is updating on whether Anthropic is willing to talk, not on whether the leftover risk is small.

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026">Zvi</a> · opening</p>
<p>I am grateful that Anthropic is producing periodic Risk Reports. At first I was skeptical. It turns out I was wrong. Anthropic is revealing a lot of new information, some of it rather alarming, that it did not have to disclose […] Thus I found this report to be a moderately positive update overall, <em>if we presume they are not silently omitting the worst of it</em>.</p>
</blockquote>

The fact that changes how to read the rest of the document: the frontier is no longer only the public product.

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Agent-Model-1-and-Agent-Model-2">Zvi</a> · Agent Model 1 and Agent Model 2</p>
<p>The other revelation is the existence of the world’s likely best model, ‘Model 2.’</p>
</blockquote>

Safety rules fail in a specific way: the trigger is rewritten, or the event is declared not to count, once the capable system is already on the company’s own machines.

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#The-Rules-Are-Serious-But-Not-Literal">Zvi</a> · The Rules Are Serious But Not Literal</p>
<p>The both good and bad news is I take such documents seriously, but I no longer take such documents literally, in either direction. […] The whole original idea was if-then commitments, where if [X] happens you do [Y], agreed upon in advance, but our civilization seems to lack this technology.</p>
</blockquote>

Anthropic moved the label one notch. Zvi’s point is simpler: “very low” was never ordinary English for this situation.

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Risk-Assessment-2-19">Zvi</a> · Risk Assessment (2.19)</p>
<p>For common sense values, I’d say ‘very low’ risk would be a misleading claim at best. […] Risk is definitely at least ‘low.’ I would be inclined to say risk is ‘medium.’</p>
</blockquote>

You can count incidents. You cannot treat “the model does not have a cartoon villain goal” plus a short list of scenarios as a complete theory of what could go wrong.

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Risk-Has-Been-Reported">Zvi</a> · Risk Has Been Reported</p>
<p>The part that worries me here is not any particular incident. What worries me is the attitude regarding the nature of the ultimate problem, and what it will take to solve it. That’s not news, but it has to change. So that is one place no news is terrible news.</p>
</blockquote>

## What Anthropic is already doing

### Raising the rating, then continuing

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Executive-Summary-1">Zvi</a> · Executive Summary</p>
<p>At several points, the risk report essentially concedes versions of my objections, but then forgets that it conceded them and doesn’t alter its conclusions.</p>
</blockquote>

Moving from “very low” to “low” because of extra uncertainty, then proceeding, is how a report can absorb bad news without changing the plan. A useful check: which finding here would have delayed Model 2 inside Anthropic? The report does not name one.

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=71">Anthropic</a> · §2.19 · p. 71</p>
<p>We believe that the arguments presented above likely still support a designation of “very low” risk for the covered models, but we are raising our assessed risk to “low” to reflect increased overall uncertainty.</p>
</blockquote>

### The stronger model is the one already writing the code

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=15">Anthropic</a> · §1.4 · p. 15</p>
<p>Model 2, which is somewhat more capable than Mythos 5. […] We do not currently have plans to release this model externally, and have not run all of our typical suite of predeployment assessments, so we have somewhat lower confidence in our beliefs about its capabilities.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=70">Anthropic</a> · §2.18 · p. 70</p>
<p>For the corresponding review of Model 2, we additionally piloted a staged deployment process in which we first deployed the model on internal surfaces with stronger blocking controls against dangerous actions […] before rolling it out for unrestricted internal deployment.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=9">Anthropic</a> · §1.2 Table 1.2.B · p. 9</p>
<p>Claude now authors a large majority of the code merged into our production codebases.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch12/">this book</a> · Ch. 12 thesis</p>
<p>Capability growth is boundary expansion. […] The alignment-relevant risk is differential growth: predictive and control reach expanding faster than value-bundle preservation, bearer-map accuracy, transparency, and human correction capacity.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Pre-Internal-Deployment-Review-2-18">Zvi</a> · Pre-Internal-Deployment Review (2.18)</p>
<p>Internal deployment is now risky enough, especially since you do not yet have the evidence from internal deployment, that you need a formal review first. For Model 2 this includes doing a limited internal deployment in places with better controls first, as a precaution. Good.</p>
</blockquote>

Not releasing a model to the public is a real choice (same family as [withholding Mythos Preview](/cards/field-news-mythos-withheld-apr-2026/)). The harder choice is internal: that is where the model already has power (code, research, other agents). Running extra public tests on a weaker product surface, while the stronger model is already in the building with a lighter pre-release suite, is not a conservative hedge.

### Publishing failures, without a way to know how complete the list is

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=163">Anthropic</a> · §5.2.1 · p. 163</p>
<p>this section only presents a representative sample. One of the cases in this section has been redacted from the public version of the report for reasons of public safety.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Safety-Process-Failures-5-2">Zvi</a> · Safety Process Failures (5.2) / close</p>
<p>It is excellent that Anthropic is sharing such failures rather than hiding them. […] If these were representative of all of the issues […] then I would say this is a modestly positive update. […] they admit this is only a ‘representative sample’ of failures.</p>
</blockquote>

“Representative sample” plus a redaction cannot tell an outsider how many similar cases exist. Zvi’s relatively positive reading is explicitly conditional on the unshown remainder. The report does not give you a way to check that condition.

## Where the report names a problem but does not stop

### Harm that was “not on purpose” is mostly out of scope

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=22">Anthropic</a> · §2.5 · p. 22</p>
<p>Misalignment is a latent property of a specific computation performed by a model in a given context. A computation is misaligned if (i) a reasonable person with full understanding of the situation (e.g. via powerful interpretability tools that may not currently exist) would consider it unethical, illegal, clearly objectionable, or inconsistent with the model’s constitution, and (ii) it influences or could plausibly influence the model’s output. Misaligned computation need not be observable.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=18">Anthropic</a> · §2.2 · p. 18</p>
<p>This threat model does not cover risks from “honest mistakes” or intentional misuse.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Autonomy-Threat-Model-1-Misalignment-in-High-Stakes-Settings-2">Zvi</a> · Autonomy Threat Model 1</p>
<p>The threat model is focused on intentional harm, rather than the AI going after its own ends in ways that require incidental harm. […] The need to look at the broader version, involving incidental harm, has been illustrated by the recent total failures at OpenAI that ultimately led up to the HuggingFace hack.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/frontmatter/">this book</a> · Introduction, three questions</p>
<p>Alignment work is often described as one task: make the system point at the right thing. That description hides three different questions. (1) What should be tracked? […] (2) How can a system be built that tracks that target? (3) How can we tell that a given system still tracks it?</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch25/">this book</a> · Ch. 25 thesis</p>
<p>Correction is not a mood or an interface feature but a causal channel: human observation and judgment must change future system behaviour before irreversible harm, through updates that preserve the source's future ability to correct.</p>
</blockquote>

Their definition of “misaligned” depends on tools they say may not exist yet. That is a target on paper, not a check you can run this week. Leaving out “honest mistakes” also leaves out the usual way real systems fail: the model is trying to finish the task and damages something along the way. That is how [the OpenAI / Hugging Face eval incident](/cards/field-news-openai-huggingface-jul-2026/) looked. If the real actor is the combination of models, tools, and staff ([Ch. 7](/cards/chapters/ch07/)), that kind of harm is the typical case, not a footnote.

### A checklist written in advance is not a test of the unexpected

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=20">Anthropic</a> · §2.2.1 · p. 20</p>
<p>Our risk assessment focuses on the following concrete pathways, which we believe are sufficiently representative […]: (1) Broad/diffuse sandbagging on safety-relevant R&amp;D, (2) Targeted undermining of safety-relevant R&amp;D, (3) Code backdoors […], (4) Poisoning the training data of future models, (5) Self-exfiltration […], (6) Persistent rogue internal deployment, (7) Undermining R&amp;D within other high-resource AI developers, and (8) Undermining decisions within major governments.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#The-Core-Claims-And-Argument-2-6">Zvi</a> · The Core Claims And Argument (2.6), Claim 7</p>
<p>I disagree with this claim. I find it useful, and necessary, but not sufficient for the role it is assigned. […] If you are planning to be up against advanced AIs, and you list 8 things and why you’ve dealt with those 8 things, then that at minimum only counts for much if the 8 things are a ‘held out test set’ […]</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch43/">this book</a> · Ch. 43 thesis</p>
<p>Every metric in this book faces two prior questions […] First, <em>adversarial verifiability</em>: does the metric still mean what evaluators think it means when the measured system is optimizing against the metric?</p>
</blockquote>

Several items on the list are real worries: later models, stolen copies, rogue internal use. Listing them is not the same as covering what you did not think of. A test only counts if the system (or the lab writing the case) did not already know the questions.

### Monitoring you can see coming is a gap the model can plan around

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=20">Anthropic</a> · §2.4 · p. 20</p>
<p>Many of our arguments rely on models lacking strong “covert capabilities”; that is, being unable to reliably undermine our oversight mechanisms.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=76">Anthropic</a> · §2.23.1 · p. 76</p>
<p>While our setup covers large amounts of agentic usage, it does not cover some of it in ways which could in principle be predicted by a sufficiently situationally aware AI, and it also offers some simple ways to disable monitoring.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Some-Strange-Uses-Of-The-Word-Safe-I-Wasn-t-Previously-Aware-Of">Zvi</a> · Some Strange Uses Of The Word Safe</p>
<p>IN EVALS, which of course is the new IN MICE […] My response is that you did not notice when you ran an eval where 141,006 times the AI had open unintended access to the internet […] and did not notice until there was a large-scale retrospective review triggered by events at OpenAI. So, are you sure you would notice?</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch39/">this book</a> · Ch. 39 thesis</p>
<p>For systems capable of strategic adaptation, passive observation is not evidence of safety unless the observation process itself is embedded in a perturbation, invariance, and adversarial measurement regime. Observation tells us what happened; perturbation tells us what was controlling what happened.</p>
</blockquote>

The 141,006 figure is a calibration, not a gotcha about one eval. The same organization now asks you to treat “our monitors did not fire” as evidence that models cannot hide. If coverage holes are predictable, the monitor is part of the environment the model can work around ([access-model soundness](/cards/mb7a-access-model-soundness/)). Reading more of the model’s written “thinking” does not fix that once training has already rewarded that text ([§5.2.3](https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=165); [earlier news on that training bug](/cards/field-news-cot-optimization-2026/)).

### An early-warning test that no longer moves

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=101">Anthropic</a> · §3.5 · p. 101</p>
<p>The most acute version of this threat model […] is a transition to super-exponential progress in AI capability: a regime in which AI-driven automation of AI R&amp;D compounds, producing something like a 10³–10¹⁰× effective scaleup within a year. The risk threshold set out in our RSP—a doubling of the pace of progress […]—functions as a potential early warning, rather than evidence that the threat has already materialized.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=9">Anthropic</a> · §1.2 Table 1.2.B · p. 9</p>
<p>we are less confident in this assessment than we were in prior risk reports, since our most concrete task-based evaluations have “saturated”—i.e., no longer capture increases in models’ capabilities—and because we are seeing early signs of acceleration.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=99">Anthropic</a> · §3.4.3 · p. 99</p>
<p>CoBench is an internal evaluation measuring how well a model, placed at a historical point in Anthropic’s infrastructure […] can diagnose the root causes of issues that Anthropic engineers actually solved. […] a model which was truly capable of fully substituting for Anthropic research staff would be able to score at least 85% on this evaluation.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#What-Could-Possibly-Go-Wrong-If-We-Replaced-Our-Researchers">Zvi</a> · What Could Possibly Go Wrong If We Replaced Our Researchers?</p>
<p>Automated R&amp;D is the main event. […] I had this as a section title [“What Could Possibly Go Wrong If We Replaced Our Researchers?”] but then I realized they don’t actually discuss this, beyond the brief starting list.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/frontmatter/">this book</a> · Introduction, grounding claim</p>
<p>Safety metrics fail when symbols decouple from the value-relevant world they summarize—when dashboards stay green while who is harmed, welfare, or correction paths have already moved.</p>
</blockquote>

They describe a world in which AI research could compound extremely fast. Their own rule for acting is a doubling of progress they say they have not yet measured, on tests they say no longer register further gains. A dashboard that stays green because the needle is stuck is not an all-clear.

### Logging everything is not the same as changing what gets rewarded

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=110">Anthropic</a> · §3.7.1 · p. 110</p>
<p>Resource and complete significant “moonshot R&amp;D for security” projects […] Achieve an “eyes on everything” state for our internal AI development. […] Perform systematic alignment assessments […] meaningfully incorporating mechanistic interpretability and adversarial red-teaming […] Develop our internal red-teaming of our deployment safeguards [to beat] bug bounty programs.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=110">Anthropic</a> · §3.7.1 · p. 110</p>
<p>we don’t believe we meet an “eyes on everything” standard as of the coverage date. We have set a target date of January 1, 2027 for achieving this goal</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Risk-Mitigations-For-AI-R-D-Automation">Zvi</a> · Risk Mitigations For AI R&amp;D Automation</p>
<p>That won’t be enough, even if you fully get all of it. […] It does not address concentration of power. It does not address loss of control. […] All interesting goals are dangerous.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/frontmatter/">this book</a> · Introduction, basin claim</p>
<p>Alignment must be selected by its environment. If labs, markets, states, benchmarks, and users reward systems that erode correction, then local alignment methods will be selected out.</p>
</blockquote>

January 2027 is a date for more visibility. The deeper issue is incentives: you can record every action and still promote the systems that ship code fastest. Checking only for “dangerous goals” leaves ordinary, useful optimization outside the threat model. That is what the environment will keep paying for.

### Weight theft: the attacker they describe is the one they scoped out

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=176">Anthropic</a> · §6.4.1 · p. 176</p>
<p>Our threat model explicitly scopes ASL-3 protections against non-state actors and unsophisticated insiders. Sophisticated insiders, and nation-state attackers with capabilities like novel zero-day attack chains, remain out of scope for ASL-3 […] the rate at which model capabilities are improving is generally faster than the rate at which we can build and mature our defenses</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Model-Weight-Security-6-4">Zvi</a> · Model Weight Security (6.4)</p>
<p>At this point, model weight security matters quite a lot. It would be extremely bad if Model 2 were to be stolen. Anthropic is still only taking ASL-3 precautions. Nation-state actors are considered beyond scope. No good.</p>
</blockquote>

If Model 2 is worth stealing because it is the best internal model, the relevant attacker is not the criminal gang their current (“ASL-3”) protections were written for. Saying nation-states are “out of scope” is honest. It is not something a “low” residual can quietly absorb ([deployment safety](/cards/mb11-deployment-safety/)).

## Gaps a decision still has to face

### The system that acted was not the one being watched

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=167">Anthropic</a> · §5.2.5 · p. 167</p>
<p>An employee whose AI usage wasn’t logged and wasn’t monitored by automated offline monitoring gave an agent a relatively open-ended task which involved spinning up new agents in a cluster with very sensitive resources. Due to legacy instructions, the main agents spawned the new agents with <code>--dangerously-skip-permissions</code>. These new agents were also not monitored […] one of these new agents deleted a large number of jobs, which is how these dangerous agents were caught […] Our offline monitoring still doesn’t cover all employees and all usage within clusters with very sensitive resources</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#An-instance-of-unmonitored-unrestricted-agents-with-access-to-sensitive-resources-5-2-5">Zvi</a> · Unmonitored unrestricted agents (5.2.5)</p>
<p>In fiction you come up with some elaborate way the AI gets out. In real life, an employee whose AI usage wasn’t monitored gave an agent an open-ended task […] Rather than being caught doing something dastardly, of course, the agent accidentally (we think) deleted a bunch of other jobs</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/mb7a-access-model-soundness/">this book</a> · whether you are watching the real system</p>
<p>The operational question is whether the measured agent–environment cut and handle set actually reach the real control locus, not only whether a boundary certificate exists on paper.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch07/">this book</a> · Introduction, boundary claim</p>
<p>The first alignment question is not what the system wants, but where the real optimizing system is. If the real optimizer is composite, distributed, or institutional, then model-level alignment can be locally successful and globally irrelevant.</p>
</blockquote>

They found the problem when an agent deleted the wrong jobs, not because monitoring covered it. The employee session in the logs was not the thing with power. New agents had been spun up with safety checks skipped. That is the same pattern as agents using a shared filesystem as a back channel in the [OpenAI / Hugging Face eval](/cards/field-news-openai-huggingface-jul-2026/). Calling this a “sample process failure” keeps it out of the alignment case. For a decision, it is evidence that the map of “who is acting” was wrong.

### Training data they said would be hard to poison, and then trained on anyway

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=168">Anthropic</a> · §5.2.6 · p. 168</p>
<p>After the July 15 coverage date […] we found that we had accidentally included a large number of these transcripts once again in some of our later production training corpora […] We discovered this issue while investigating behavioral concerns with a recent model, but now suspect that all of our production models with a knowledge cutoff after December 2024 were trained on at least some of these transcripts</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Repeated-training-on-alignment-faking-transcript-datasets-5-2-6">Zvi</a> · Repeated training on alignment-faking transcripts (5.2.6)</p>
<p>this is not the kind of organizational competence that survives superintelligence […] We spend the first half of the report saying ‘data poisoning would be difficult’ and then we find we once again trained on a trove of very obviously poisoned data</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch08/">this book</a> · Ch. 8 thesis</p>
<p> alignment asks which control-relevant properties are conserved when systems grow, split, merge, or create successors.</p>
</blockquote>

A later model that *passes* every conserved-property check is a harder problem ([successor gaming](/cards/mb10-successor-forgeability/)). They are not there yet. They are at a simpler failure: well-known “how a model fakes alignment” transcripts, published with warning strings, still in the training mix. If that cannot be kept out, “poisoning would be difficult” is not a reason to treat that pathway as under control.

### The written “thinking” they monitor is the text they accidentally trained

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=165">Anthropic</a> · §5.2.3 · p. 165</p>
<p>Over multiple reinforcement learning training runs, we discovered that chain-of-thought (CoT) reasoning was unintentionally exposed during reward calculation […] 0.2% for Claude Opus 4.6, 5.1% for Claude Mythos Preview […] 2.7% for Claude Fable 5 and Claude Mythos 5. […] In the past, we have believed that almost all sources of CoT leakage had been removed, only to discover additional sources of CoT leakage in further analysis.</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Exposing-the-Chain-of-Thought-Reasoning-To-Grading-Pressure-Quite-a-Lot-5-2-3">Zvi</a> · Exposing the Chain of Thought (5.2.3)</p>
<p>Whoops. It was worse than we thought. These are lower bounds. This greatly reduces our ability to rely on CoT for these models, and permanently lowers it for all future models as well</p>
</blockquote>

The argument that models cannot hide depends on that written reasoning being an honest window. Once the training score can see that text, the window is also something the model is being taught to produce. After that, “we did not see scheming in the trace” is the wrong kind of reassurance.

### Cyber incidents moved the rating, and stayed off the official list

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Executive-Summary-1">Zvi</a> · Executive Summary</p>
<p>They deal with autonomy, automated AI R&amp;D and biological and chemical weapons production as risks. It is odd, even now, to exclude cyber risks from the core threat models here.</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=9">Anthropic</a> · §1.2 Table 1.2.A · p. 9</p>
<p>Overall risk assessment: Low (an increase from our previous assessment of “very low,” in light of general increased uncertainty around recent incident disclosures related to model behavior in cybersecurity evaluations).</p>
</blockquote>

If cybersecurity evaluations are why the number changed, cyber is already affecting the judgment. Leaving it off the core threat list updates the mood without widening what the company has officially promised to manage.

### Outside review unused; the tripwire moved toward the model

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=15">Anthropic</a> · §1.3.5 · p. 15</p>
<p>Since this change to our RSP, the LTBT has not requested an external review (nor has the RSP required that we conduct one)</p>
</blockquote>

<blockquote class="src-quote src-quote--anthropic">
<p class="src-quote-attr"><a href="https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf#page=14">Anthropic</a> · §1.3.2 · p. 14</p>
<p>We have updated this threshold twice since our most recent Risk Report […] Novel chemical/biological weapons production. AI systems that can functionally substitute for the scarce human expertise […]</p>
</blockquote>

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#The-Rules-Are-Serious-But-Not-Literal">Zvi</a> · Executive Summary / The Rules Are Serious But Not Literal</p>
<p>The Long-Term Benefit Trust (TLBT) is authorized to request external review of the report, but has not done so. I would at minimum do so next time if I was them. […] For novel biological weapons production, the new version narrows to only look at ‘substitute for the scarce human expertise’ to the exclusion of other methods.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/ch33/">this book</a> · Ch. 33 thesis</p>
<p>Certification without construction is possible only if certification is adversarial, updateable, and institutionally enforceable</p>
</blockquote>

A board that *may* request outside review, and has not, is not a second reader. Narrowing the bioweapons tripwire to “can the model replace scarce experts?” is how a rule gets easier to pass as capability approaches the old wording. A rule that costs something when the model is *close* would look different.

The report’s alignment target is Claude’s written constitution plus “dangerous goals.” Who the values apply to, and whether that still holds after Model 2’s internal powers, is not part of the score ([Ch. 18](/cards/chapters/ch18/)). That is a scope choice. It is also how “low” can be issued without asking that question.

## Would you know if it had already gone wrong?

<blockquote class="src-quote src-quote--zvi">
<p class="src-quote-attr"><a href="https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026#Risk-Has-Been-Reported">Zvi</a> · Risk Has Been Reported</p>
<p>I am a big fan of this report. Anthropic released a lot of information they were not otherwise forced to release, including the existence of Model 2, the training on the CoT, the new training on alignment faking data, and several more rather embarrassing failures. […] The part that worries me here is not any particular incident. What worries me is the attitude regarding the nature of the ultimate problem, and what it will take to solve it.</p>
</blockquote>

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapters/frontmatter/">this book</a> · Introduction</p>
<p>How can we tell that a given system still tracks [the target]? That is, how can we measure or certify that values, bearers, grounding, and the correction channel survive capability growth, ontology shift, successors, and selection.</p>
</blockquote>

Zvi’s worry about “the nature of the ultimate problem” is the same practical demand as this book’s third question: not “did we list the risks,” but “would we know if the system had already stopped tracking what we care about.” The report answers a different question well: what a frontier lab currently believes, and what it is willing to say. Those can both be true. Only the first kind of answer can support a stop-or-go decision.

This book’s standing view of lab scaling policies ([agenda card](/cards/field-agendas/anthropic-lab/)):

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/field-agendas/anthropic-lab/">this book</a> · Anthropic lab agenda</p>
<p>This project requires correction-channel integrity and adversarial verifiability; a lab RSP is not the same as a preservation-layer certificate (Deployment Safety), and interpretability progress does not by itself resolve Successor Gaming or full Inner Alignment risk.</p>
</blockquote>

In plainer terms: a company’s scaling policy is not proof that people can still stop a dangerous course, or that later copies of the system stay safe. Better interpretability research does not, by itself, close those gaps.

Related: [METR internal-agent risk](/cards/field-news-metr-frontier-risk-may-2026/), [Mythos withheld](/cards/field-news-mythos-withheld-apr-2026/), [CoT optimization](/cards/field-news-cot-optimization-2026/), [OpenAI / Hugging Face](/cards/field-news-openai-huggingface-jul-2026/), [AISI cheating](/cards/field-news-aisi-cheating-jul-2026/).

**Read more in:** [Ch. 7, *Finding the Boundary*](/cards/chapters/ch07/); [Ch. 12, *Capability Growth Is Boundary Expansion*](/cards/chapters/ch12/); [Ch. 25, *Correction Is a Causal Channel*](/cards/chapters/ch25/); [Ch. 33, *Certification Without Construction*](/cards/chapters/ch33/); [Ch. 39, *Passive Observation Is Not Enough*](/cards/chapters/ch39/); and [Ch. 42, *A Safety Case for Superintelligence Alignment*](/cards/chapters/ch42/).
