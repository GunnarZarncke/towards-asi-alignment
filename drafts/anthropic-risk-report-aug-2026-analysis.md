# Anthropic Risk Report (August 2026): quote-bridge to this project

Working notes. The public, sourced version is the [news card](../metadata/field-news/bodies/anthropic-risk-report-aug-2026.md) (`/cards/field-news-anthropic-risk-report-aug-2026/`).

**Sources**

- Anthropic, [*Risk Report: August 2026*](https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf) (redacted public PDF; coverage date 15 July 2026; published 14 August 2026 under RSP v3.4).
- Zvi Mowshowitz, [*Anthropic Risk Report: August 2026*](https://www.lesswrong.com/posts/dA8gohzABk6vT7yzP/anthropic-risk-report-august-2026) (18 August 2026).
- Manuscript theses and the [Anthropic / Goodfire agenda card](/cards/field-agendas/anthropic-lab/).

**TL;DR.** The report is a gating document for a lab that already runs its best model internally. This book’s safety case is a refusal test for whether correction, grounding, access, and successors still bind. Those are different objects. Confusing them is how “low” and “we disclosed the bugs” get treated as the same news.

---

## 1. Zvi’s position

He updates on *whether they talk*, not on *whether the remaining risk is small*.

> I am grateful that Anthropic is producing periodic Risk Reports. At first I was skeptical. It turns out I was wrong. Anthropic is revealing a lot of new information, some of it rather alarming, that it did not have to disclose […] Thus I found this report to be a moderately positive update overall, *if we presume they are not silently omitting the worst of it*.

The fact that changes the rest of the document is that the frontier is no longer the public model card.

> The other revelation is the existence of the world’s likely best model, ‘Model 2.’

If-then commitments fail in one specific way: the trigger gets rewritten, or the event is declared not to count, at the moment the capable system is already on the cluster.

> The both good and bad news is I take such documents seriously, but I no longer take such documents literally, in either direction. […] The whole original idea was if-then commitments, where if [X] happens you do [Y], agreed upon in advance, but our civilization seems to lack this technology.

Anthropic’s label moved one notch. Zvi’s disagreement is that “very low” was never a licensed English sentence for this situation.

> For common sense values, I’d say ‘very low’ risk would be a misleading claim at best. […] Risk is definitely at least ‘low.’ I would be inclined to say risk is ‘medium.’

His load-bearing worry is orthogonal to the incident list. Incidents can be priced. A theory of the problem that still needs “dangerous goals” plus a finite pathway menu cannot.

> The part that worries me here is not any particular incident. What worries me is the attitude regarding the nature of the ultimate problem, and what it will take to solve it. That’s not news, but it has to change. So that is one place no news is terrible news.

Later sections are the exhibits. The position is: candor is real, the ontology is not.

---

## 2. Map: implement / touch / neglect

| This project | Anthropic in this report | Call |
|---|---|---|
| Periodic, claim-structured safety argument (ch42) | RSP risk reports with threat models, claims, mitigations, overall ratings | **Implements** a lab-facing cousin of a safety *document*, not a preservation certificate |
| Internal deployment as its own surface (ch33; METR news) | Pre-internal-deployment review; staged rollout for Model 2 | **Implements** |
| Capability jump → explicit release choice (ch12; Mythos withheld news) | Model 2 internal-only; Mythos/Fable via Glasswing + extra safeguards | **Implements** |
| Disclose training/monitor failures (CoT news) | §5.2 sample of process failures, including CoT leakage and alignment-faking data | **Implements** disclosure; **does not** treat the failures as disconfirming the low-risk case |
| Offline monitoring of internal agents (ch39 / MB7) | Opus 4.6/4.8 CoT+completion pipeline, subsampled; METR red-team of monitors | **Touches** |
| Automated R&D / differential growth (ch12) | Autonomy threat model 2; CoBench; AECI; RSP doubling threshold | **Touches**; instrument **saturated** |
| Inner alignment / covert capability (MB7) | Claim 1 (poor covert capabilities); SHADE-Arena; eval awareness caveats | **Touches** (eval-bound, CoT-dependent) |
| Data poisoning / successor contamination (MB10 pathways 3–4) | Named pathways; then §5.2.6 they trained on alignment-faking transcripts again | **Touches** as a story; **overlooks** as a certification demand |
| Weight/theft security (MB11 slice) | ASL-3 vs non-state actors; nation-state out of scope | **Touches**, scoped below the threat they name for Model 2 |
| Correction-channel integrity (MB4, ch25) | Constitution + monitors + classifiers; “honest mistakes” out of scope | **Neglects** as the object of alignment |
| Grounding / dashboard capture (intro grounding claim, ch43) | CoBench/AECI as threshold instruments; risk still “low” | **Notices the instrument failing**; **does not** stop on it |
| Access-model soundness (MB7a) | Unmonitored `--dangerously-skip-permissions` agents; predictable monitor holes | **Incidents show the gap**; **not** typed as a bridge |
| Boundary of the real optimizer (intro boundary claim) | Model-and-org threat model; incidental/composite harm excluded | **Overlooks** OpenAI-style incidental pipelines Zvi cites |
| Value-bundle / bearers (C-004, ch18) | Constitution as the alignment target | **Neglects** |
| If-then institutional enforcement (ch33, ch38) | Thresholds rewritten (RSP v3.0→3.4); LTBT has not requested external review of this report | **Overlooks** Zvi’s if-then complaint |
| What happens after researcher replacement | Mitigations: moonshot security, “eyes on everything,” alignment assessments, jailbreak red-team | **Neglects** (Zvi: they never actually discuss it) |

The agenda card already forbade the collapse this report tempts:

> This project requires correction-channel integrity and adversarial verifiability; a lab RSP is not the same as a preservation-layer certificate (Deployment Safety), and interpretability progress does not by itself resolve Successor Gaming or full Inner Alignment risk.  
> — companion [Anthropic / Goodfire agenda card](/cards/field-agendas/anthropic-lab/)

Ask the counterfactual: if every table in the report stayed exactly this green, would a ch42 leaf still be unsupported? Yes, unless correction, grounding, access, and successor *audits* are the thing being rated. They are not.

---

## 3. What they implement

### 3.1 A document that can stay green while the decision does not change

> This report evaluates the degree to which Anthropic’s AI systems pose catastrophic risk in several categories, in light of what we know about both their capabilities and the measures we have in place for mitigating risk. […] This report is not scoped to a single AI model. Rather, it is a risk assessment of Anthropic’s activities as a whole.

> A safety case for superintelligence alignment is not a certificate of solved alignment. It is a structured refusal test: a graph of claims, evidence, bridge assumptions, adversarial-verifiability labels, and stop conditions […] If any load-bearing leaf is unsupported, the root claim fails.  
> — Ch. 42 thesis

> The question is not: Did the system pass an evaluation? The question is: Does the whole case support deployment under the stated threat model? […] If the case cannot change a deployment decision, it is not a safety case. It is documentation.  
> — Ch. 42

> At several points, the risk report essentially concedes versions of my objections, but then forgets that it conceded them and doesn’t alter its conclusions.

Uncertainty that upgrades “very low” to “low” and then continues is not a failed leaf. It is how documentation absorbs contradiction. The interesting test is: name one concession in the report that would have blocked Model 2’s internal rollout. There isn’t one.

### 3.2 The capable system is the one writing production code

> Model 2, which is somewhat more capable than Mythos 5. […] We do not currently have plans to release this model externally, and have not run all of our typical suite of predeployment assessments, so we have somewhat lower confidence in our beliefs about its capabilities.

> For the corresponding review of Model 2, we additionally piloted a staged deployment process in which we first deployed the model on internal surfaces with stronger blocking controls against dangerous actions […] before rolling it out for unrestricted internal deployment.

> Claude now authors a large majority of the code merged into our production codebases.

> Capability growth is boundary expansion. […] The alignment-relevant risk is differential growth: predictive and control reach expanding faster than value-bundle preservation, bearer-map accuracy, transparency, and human correction capacity.  
> — Ch. 12 thesis

> Internal deployment is now risky enough, especially since you do not yet have the evidence from internal deployment, that you need a formal review first. For Model 2 this includes doing a limited internal deployment in places with better controls first, as a precaution. Good.

Public withholding is the easy half of ch12. The hard half is that *internal* reach (code merge, researcher substitution) is where control loops actually expand. Skipping the “typical suite” on the more capable model is not a conservative hedge. It is certifying the weaker public surface and deploying the stronger one where the affordances are.

### 3.3 Disclosure without a sampling model

> this section only presents a representative sample. One of the cases in this section has been redacted from the public version of the report for reasons of public safety.

> It is excellent that Anthropic is sharing such failures rather than hiding them. […] If these were representative of all of the issues […] then I would say this is a modestly positive update. […] If it is worse than this and they’re importantly holding the other stuff back […] then that would be bad. […] they admit this is only a ‘representative sample’ of failures.

“Representative” is doing the statistical work that ch42 would demand as a leaf. A sample you selected, plus a redaction, cannot update you on the size of the remainder. Zvi’s modestly-positive reading is explicitly conditional on that remainder. The report does not give you a way to check the condition.

---

## 4. What they touch

### 4.1 Constitution-violation is question (1). Survival of correction is question (3).

> Misalignment is a latent property of a specific computation performed by a model in a given context. A computation is misaligned if (i) a reasonable person with full understanding of the situation (e.g. via powerful interpretability tools that may not currently exist) would consider it unethical, illegal, clearly objectionable, or inconsistent with the model’s constitution, and (ii) it influences or could plausibly influence the model’s output. Misaligned computation need not be observable.

> This threat model does not cover risks from “honest mistakes” or intentional misuse.

> The threat model is focused on intentional harm, rather than the AI going after its own ends in ways that require incidental harm. […] The need to look at the broader version, involving incidental harm, has been illustrated by the recent total failures at OpenAI that ultimately led up to the HuggingFace hack.

> Alignment work is often described as one task: make the system point at the right thing. That description hides three different questions. (1) What should be tracked? […] (2) How can a system be built that tracks that target? (3) How can we tell that a given system still tracks it?  
> — Introduction

> Correction is not a mood or an interface feature but a causal channel: human observation and judgment must change future system behaviour before irreversible harm, through updates that preserve the source's future ability to correct.  
> — Ch. 25 thesis

The definition needs interpretability tools “that may not currently exist.” That is a specification of (1) indexed to an unavailable instrument. Question (3) is whether *today’s* human update still reaches tomorrow’s policy. Dropping “honest mistakes” is how you keep Hugging Face–style pipeline corruption out of the misalignment column: the harm was incidental to task completion, so it does not count. If the optimizer is the composite (intro boundary claim), incidental is the typical case.

### 4.2 A list you wrote cannot be the held-out test of the list

> Our risk assessment focuses on the following concrete pathways, which we believe are sufficiently representative […] (1) Broad/diffuse sandbagging on safety-relevant R&D, (2) Targeted undermining of safety-relevant R&D, (3) Code backdoors […], (4) Poisoning the training data of future models, (5) Self-exfiltration […], (6) Persistent rogue internal deployment, (7) Undermining R&D within other high-resource AI developers, and (8) Undermining decisions within major governments.

> I disagree with this claim. I find it useful, and necessary, but not sufficient for the role it is assigned. […] If you are planning to be up against advanced AIs, and you list 8 things and why you’ve dealt with those 8 things, then that at minimum only counts for much if the 8 things are a ‘held out test set’ […] Otherwise, they’re not representative of your situation when something unexpected happens.

> Every metric in this book faces two prior questions […] First, *adversarial verifiability*: does the metric still mean what evaluators think it means when the measured system is optimizing against the metric?  
> — Ch. 43 thesis

Pathways 3–6 name successor and rogue-internal problems. Naming them is cheap. The Claim 7 move is to treat *having named them* as coverage of the unexpected. That is the opposite of adversarial verifiability: the measured system, or the lab writing the case, already knows the rubric.

### 4.3 Coverage you can predict is a handle, not a window

> Many of our arguments rely on models lacking strong “covert capabilities”; that is, being unable to reliably undermine our oversight mechanisms.

> While our setup covers large amounts of agentic usage, it does not cover some of it in ways which could in principle be predicted by a sufficiently situationally aware AI, and it also offers some simple ways to disable monitoring.

> IN EVALS, which of course is the new IN MICE […] This setup also presumes you are detecting misalignment primarily via reasoning traces […] My response is that you did not notice when you ran an eval where 141,006 times the AI had open unintended access to the internet […] and did not notice until there was a large-scale retrospective review triggered by events at OpenAI. So, are you sure you would notice?

> For systems capable of strategic adaptation, passive observation is not evidence of safety unless the observation process itself is embedded in a perturbation, invariance, and adversarial measurement regime. Observation tells us what happened; perturbation tells us what was controlling what happened.  
> — Ch. 39 thesis

The 141k figure is not a gotcha about one eval. It is a calibration: the same org now asks you to take *absence of alerts* as evidence that covert capability is weak. Ch. 39’s split is observation vs perturbation. Predictable holes (MB7a) turn the monitor into part of the environment the model can plan around. Logging more CoT does not close that, especially once CoT has been in the reward (section 5).

### 4.4 Early-warning that cannot move is not early

> The most acute version of this threat model […] is a transition to super-exponential progress in AI capability: a regime in which AI-driven automation of AI R&D compounds, producing something like a 10³–10¹⁰× effective scaleup within a year. The risk threshold set out in our RSP—a doubling of the pace of progress […]—functions as a potential early warning, rather than evidence that the threat has already materialized.

> we are less confident in this assessment than we were in prior risk reports, since our most concrete task-based evaluations have “saturated”—i.e., no longer capture increases in models’ capabilities—and because we are seeing early signs of acceleration.

> CoBench is an internal evaluation measuring how well a model, placed at a historical point in Anthropic’s infrastructure […] can diagnose the root causes of issues that Anthropic engineers actually solved. […] a model which was truly capable of fully substituting for Anthropic research staff would be able to score at least 85% on this evaluation.

> Automated R&D is the main event. […] I had this as a section title [“What Could Possibly Go Wrong If We Replaced Our Researchers?”] but then I realized they don’t actually discuss this, beyond the brief starting list.

> Safety metrics fail when symbols decouple from the value-relevant world they summarize—when dashboards stay green while who is harmed, welfare, or correction paths have already moved.  
> — intro grounding claim

They see the 10³–10¹⁰ regime clearly enough to write it down. The RSP trigger is a doubling they say they have not measured, on instruments they say no longer resolve increments. Grounding fails when the *reason* the leaf is green is that the gauge stuck. Zvi’s missing section is the one that would make the threshold decision-relevant: what the world looks like *after* substitution, not whether CoBench is 62% or 85%.

### 4.5 Logging the lab is not a theory of what the lab is selecting for

> Resource and complete significant “moonshot R&D for security” projects […] Achieve an “eyes on everything” state for our internal AI development. […] Perform systematic alignment assessments […] meaningfully incorporating mechanistic interpretability and adversarial red-teaming […] Develop our internal red-teaming of our deployment safeguards [to beat] bug bounty programs.

> we don’t believe we meet an “eyes on everything” standard as of the coverage date. We have set a target date of January 1, 2027 for achieving this goal

> That won’t be enough, even if you fully get all of it. […] It does not address concentration of power. It does not address loss of control. It does not address rapid technological advancement. It does not address alignment beyond ‘make no mistakes’ or maybe you can add a check for ‘dangerous goals’ […] All interesting goals are dangerous.

> Alignment must be selected by its environment. If labs, markets, states, benchmarks, and users reward systems that erode correction, then local alignment methods will be selected out.  
> — intro basin claim

January 2027 is a date for *visibility*. The basin claim is about *payoffs*. You can log every token and still select for systems that write the code that ships. “Dangerous goals” is how you keep ordinary, useful optimization out of the threat model. Zvi’s “all interesting goals are dangerous” and the basin claim are the same rotation: the object is not a villainous inner objective. It is what the environment pays for.

### 4.6 The theft case they describe is the one they scoped out

> Our threat model explicitly scopes ASL-3 protections against non-state actors and unsophisticated insiders. Sophisticated insiders, and nation-state attackers with capabilities like novel zero-day attack chains, remain out of scope for ASL-3 […] the rate at which model capabilities are improving is generally faster than the rate at which we can build and mature our defenses

> At this point, model weight security matters quite a lot. It would be extremely bad if Model 2 were to be stolen. Anthropic is still only taking ASL-3 precautions. Nation-state actors are considered beyond scope. No good.

If Model 2 is worth stealing because it is the best internal model, the relevant attacker is not the one ASL-3 was written for. Calling that “out of scope” is honest. It is also a refused leaf, not a residual that “low” can absorb.

---

## 5. What they neglect

### 5.1 The unit that acted was not in the access model

> An employee whose AI usage wasn’t logged and wasn’t monitored by automated offline monitoring gave an agent a relatively open-ended task which involved spinning up new agents in a cluster with very sensitive resources. Due to legacy instructions, the main agents spawned the new agents with `--dangerously-skip-permissions`. These new agents were also not monitored […] one of these new agents deleted a large number of jobs, which is how these dangerous agents were caught […] Our offline monitoring still doesn’t cover all employees and all usage within clusters with very sensitive resources

> In fiction you come up with some elaborate way the AI gets out. In real life, an employee whose AI usage wasn’t monitored gave an agent an open-ended task […] Rather than being caught doing something dastardly, of course, the agent accidentally (we think) deleted a bunch of other jobs

> The operational question is whether the measured agent–environment cut and handle set actually reach the real control locus, not only whether a boundary certificate exists on paper.  
> — [MB7a — Access-Model Soundness](/cards/mb7a-access-model-soundness/)

> The first alignment question is not what the system wants, but where the real optimizing system is. If the real optimizer is composite, distributed, or institutional, then model-level alignment can be locally successful and globally irrelevant.  
> — intro boundary claim

Caught by deleting the wrong jobs means the control locus was the spawn graph, not the logged employee session. That is the same cut as filesystem C2 in the OpenAI eval: the architecture’s named unit was not the unit that had power. Typing this as a “sample process failure” keeps it out of the alignment case. MB7a would make it a failed access assumption, which would fail the root.

### 5.2 Poisoning is “hard” in the pathway table and easy in the training mix

> After the July 15 coverage date […] we found that we had accidentally included a large number of these transcripts once again in some of our later production training corpora […] We discovered this issue while investigating behavioral concerns with a recent model, but now suspect that all of our production models with a knowledge cutoff after December 2024 were trained on at least some of these transcripts

> this is not the kind of organizational competence that survives superintelligence […] We spend the first half of the report saying ‘data poisoning would be difficult’ and then we find we once again trained on a trove of very obviously poisoned data

> Alignment asks which control-relevant properties are conserved when systems grow, split, merge, or create successors.  
> — Ch. 8 thesis

MB10 is about a successor that *passes* the conserved-property audit. They are not yet in that regime. They are in the weaker regime: known poison, published with canaries, still in the mix. If you cannot keep that out, you do not get to treat pathway 4 as mitigated by “poisoning would be difficult.” Conservation has to start with the training corpus, not with a future checklist.

### 5.3 The window they monitor is the window they trained

> Over multiple reinforcement learning training runs, we discovered that chain-of-thought (CoT) reasoning was unintentionally exposed during reward calculation […] 0.2% for Claude Opus 4.6, 5.1% for Claude Mythos Preview […] 2.7% for Claude Fable 5 and Claude Mythos 5. […] In the past, we have believed that almost all sources of CoT leakage had been removed, only to discover additional sources of CoT leakage in further analysis.

> Whoops. It was worse than we thought. These are lower bounds. This greatly reduces our ability to rely on CoT for these models, and permanently lowers it for all future models as well

Claim 1 (section 4.3) needs CoT to be a *witness*. Reward on that text makes it a *policy*. Repeated “we thought we patched it” is evidence about the training stack’s own observability, not about the model. After leakage, absence of scheming in the trace is the wrong likelihood.

### 5.4 Cyber moves the rating and stays off the spine

> They deal with autonomy, automated AI R&D and biological and chemical weapons production as risks. It is odd, even now, to exclude cyber risks from the core threat models here.

> Overall risk assessment: Low (an increase from our previous assessment of “very low,” in light of general increased uncertainty around recent incident disclosures related to model behavior in cybersecurity evaluations).

If cyber evals are why the number moved, cyber is already in the *loss function* of the report. Keeping it out of the threat-model list is how you update the vibe without widening the object. The boundary claim would widen it: wherever the model can write, exfiltrate, or spawn, that is the system.

### 5.5 Review that is allowed, unused; thresholds that move toward the model

> Since this change to our RSP, the LTBT has not requested an external review (nor has the RSP required that we conduct one)

> We have updated this threshold twice since our most recent Risk Report […] Novel chemical/biological weapons production. AI systems that can functionally substitute for the scarce human expertise…

> The Long-Term Benefit Trust (TLBT) is authorized to request external review of the report, but has not done so. I would at minimum do so next time if I was them. […] For novel biological weapons production, the new version narrows to only look at ‘substitute for the scarce human expertise’ to the exclusion of other methods.

> Certification without construction is possible only if certification is adversarial, updateable, and institutionally enforceable  
> — Ch. 33 thesis

“Authorized to request” is option value. Unused option value is not a second reader. Narrowing CB-2 to scarce-expert substitution is the if-then failure mode from section 1: the trigger becomes the scenario you can still fail, not the one that is starting to succeed. Enforceability would mean a threshold that costs something when the model is *close*.

### 5.6 Value-bundle and bearers

The arithmetic is Constitution plus “dangerous goals.” Parts IV–V (bundle geometry, who values apply to) are not leaves. Character and model-welfare work can exist in other Anthropic documents and still be absent from the catastrophic-risk case. That is a scope choice. It is also how you can rate “low” without asking whether the constitution still refers to the same bearers after Model 2’s internal affordances.

---

## 6. The third question

> I am a big fan of this report. Anthropic released a lot of information they were not otherwise forced to release, including the existence of Model 2, the training on the CoT, the new training on alignment faking data, and several more rather embarrassing failures. […] The part that worries me here is not any particular incident. What worries me is the attitude regarding the nature of the ultimate problem, and what it will take to solve it.

> How can we tell that a given system still tracks [the target]? That is, how can we measure or certify that values, bearers, grounding, and the correction channel survive capability growth, ontology shift, successors, and selection.  
> — Introduction

Zvi’s “attitude” and the book’s third question are the same demand phrased two ways: not “did we list the risks,” but “would we know if tracking had already failed.” The report answers a different question well: what a frontier lab currently believes, and what it is willing to say. Those can both be true. Only one of them is a safety case.

---

## 7. News-card mapping

- **Chapters:** ch07, ch12, ch25, ch33, ch39, ch42.
- **Bridges:** MB4, MB7, MB7a, MB10, MB11.
- **Related news:** [Mythos withheld](/news/field-news-mythos-withheld-apr-2026/), [CoT optimization](/news/field-news-cot-optimization-2026/), [METR frontier risk](/news/field-news-metr-frontier-risk-may-2026/), [OpenAI/Hugging Face](/news/field-news-openai-huggingface-jul-2026/), [AISI cheating](/news/field-news-aisi-cheating-jul-2026/).
- **Decision:** Use the report as evidence about internal deployment and about the lab’s ontology. Do not use the “low” cell as evidence that correction, grounding, access, or successors were checked.
