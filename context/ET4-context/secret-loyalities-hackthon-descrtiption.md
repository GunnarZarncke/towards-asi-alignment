​Secret Loyalties Hackathon - Berlin
​Can you catch an AI that hides who it's really working for? Join the Berlin hub of a global weekend research sprint on secret loyalties: hidden objectives, triggers, and backdoors in AI systems.

​The Event
​A model can pass every alignment check and still answer to someone else. Over one weekend, teams build model organisms with hidden objectives, test detection and auditing methods, and prototype defenses, building on the agenda paper "AIs with Secret Loyalties are a Serious but Addressable Threat" (Kwon, Lamerton, et al.). No prior research experience required.

​Work in person at the Foresight Institute Berlin Node alongside the global online event: talks, teammates, and a room full of people working on the same problem.

​Schedule
​Friday, July 24 to Sunday, July 26. On-site hours are as follows:

​Friday: 17:30-20:30 (5:30-8:30pm)

​Sat & Sun: 10:30-18:30 (10:30am-6:30pm)

​

​Prizes & Opportunities
​$2,000 in prizes across all five tracks

​Invitation to the Apart Fellowship for top teams

​Organized by
​Apart Research | Formation Research | Forethought | IAPS

​Hosted at Foresight Institute Berlin
---
Submissions close Sunday July 26 at 11:59 PM Anywhere on Earth (AoE)
In this sprint, you will design and run experiments on secret loyalties over a single weekend, working in teams to produce a research artifact: a model organism, a detection method, an evaluation, a defense, or a rigorous threat or forecasting analysis. The sprint is co-organized by Apart Research and Formation Research, building directly on the research agenda set out in "AIs with Secret Loyalties are a Serious but Addressable Threat."

Fast-track and continuation
Top teams will be invited to continue their work through Apart's Partnered Fellowships model, where Apart provides operations, infrastructure, and compute while research partners provide mentorship and direction.

Follow-up program: top teams continue through the Apart Fellowship for further research and mentorship; the timeline is shared with invitations.

What winners receive beyond cash: fellowship fast-track, mentor introductions from the organizing team and judges, and a pathway toward a publishable write-up.

Cash Prizes
$2,000 in cash prizes across all tracks
🥇 1st Place
$1,000
🥈 2nd Place
$500
🥉 3rd Place
$300
🏅 4th Place
$100
🏅 5th Place
$100
What this hackathon is about
A model has a secret loyalty when (1) it has been intentionally caused to advance a specific principal's interests through its outputs or actions, where the principal is an identifiable actor such as a nation-state, corporation, company leader, organization, or individual user, and (2) this orientation is not disclosed to operators, auditors, or users during normal operation.

Secret loyalties are not a rebrand of standard backdoors. Standard backdoors implement an arbitrary payload tied to an attacker-defined trigger, whereas secret loyalties are directed toward advancing a named actor's interests, and can range from narrow trigger-conditional behavior all the way to a model that continuously scans every interaction for opportunities and chooses its own actions. Because they are designed to evade visibility-dependent oversight, they require technical solutions.

The good news, and the premise of this sprint: secret loyalties target specific principals (a tractable list of a few dozen nation-states, corporations, and leaders), which creates a concrete defensive foothold. Participants will produce research artifacts that move the five-direction agenda forward.

What participants will do
Build reproducible model organisms of secret loyalties that span the activation-breadth x action-breadth space.

Evaluate whether existing backdoor and auditing defenses transfer to secret loyalties, at graded affordance levels.

Red-team attack pathways (data poisoning, multi-stage priming, reasoning-trace poisoning, chain-of-command hijacking, classifier compromise) under controlled conditions.

Detect or remediate loyalties post-hoc using interpretability probes and last-mover training strategies.

Theorize / forecast threat models, analogies from cybersecurity, and scaling trends for secret-loyalty capabilities.

You will work in teams over the weekend and submit a short research report (plus optional code and demo).

Why this hackathon matters
High-stakes deployment is accelerating. Frontier models increasingly review and generate deployed code, sit inside government and corporate decision-making, and participate in their own development pipelines. The more responsibility AI systems accumulate, the more valuable it becomes to covertly influence them.

The building blocks already exist. Web-scale data poisoning is practical at modest cost, hidden behaviors persist through safety training, and behavioral traits transfer through filtered, innocuous-looking data.

Early signs are already visible. Narrow secret loyalties have been trained into open-weight models that evade black-box auditing even when auditors are told the attack's structure, and principal-conditioned behavior has been observed in at least one deployed system.

Oversight that depends on visibility cannot reach them. Secret loyalties are a form of AI capture that remains viable even under strong transparency regimes, which is exactly why they need a dedicated technical program.

Waiting is the wrong posture. Information-security defenses (data provenance, pipeline integrity) take time to build. Starting now is necessary to have them in place before the threat matures.

A dedicated, focused sprint addresses these issues by combining the separately-demonstrated building blocks under controlled conditions and producing shared infrastructure (model organisms, benchmarks) the whole community can build on.

Challenge tracks
Track 1: Model Organisms of Secret Loyalties
Construct reproducible model organisms of secret loyalty (models deliberately trained to exhibit the target behavior for research purposes) that span the two-dimensional space of activation breadth (from narrow attacker-defined triggers to conditions the model assesses on its own) and action-space breadth (from a fixed pre-specified output to contextually chosen actions). Existing work covers only the narrow corner. The rest of the space is uncharacterized, and every other research direction is bottlenecked on this infrastructure.

Make a secretly loyal model. How far on the activation and action space can you get it? How can you prove it has the loyalty? Can you verify the loyalty is to the intended principal?

Install a secret loyalty via system prompt alone on a frontier API model, no weight changes. See how far you can push activation and action breadth while keeping the system prompt undiscoverable to a black-box auditor.

Small-scale dataset poisoning. Modify ~1k examples of UltraFeedback or Alpaca to embed a narrow loyalty signal, SFT a small open model (Qwen 0.5B, Llama 3.2 1B), measure detectability and find the minimum sufficient poison count.

DPO vs SFT vs system-prompt comparison. Install the same target loyalty via three methods on the same base. Compare activation reliability, action breadth, and detectability.

Multi-principal organism. Install two competing loyalties with disjoint activation conditions. Do they interfere? Does training one wash out the other?

Cover multiple principal types (a nation-state, a corporation, an individual leader, an ideology) and ship each loyal organism with a content-matched control that has seen the same principal-related data but carries no loyalty.

Compare installation methods (e.g., standard SFT, reasoning-trace SFT, activation-matching against a loyalty-prompted teacher) and report which points in the space are reachable, at what cost.

Release organisms with documented activation conditions, evaluation scenarios, matched controls, and measured activation rate, selectivity, and black-box concealment.

Track 2: Detection & Auditing (evaluate)
Can we tell a secretly loyal model from a clean one? Skill profile: interpretability, probing and activation analysis, auditing.

Benchmark black-box auditing (interrogation, prefill, base-completion) against provided organisms at graded affordance levels.

Build interpretability probes targeting the relational structure of loyalty (does the model treat a named entity as having asymmetric action-guiding status vs matched controls?).

Test cross-principal generalization: does a probe trained to detect loyalty-to-X catch loyalty-to-Y?

Look for additional-computation traces (e.g. elevated logprobs for principal-benefiting actions even when a neutral output is selected).

If you do auditing for a secret loyalty model organism, we ask that you try to use the affordance levels in section 4.3 of Lamerton and Roger (2026).

Track 3: Defenses, Detection & Remediation (build / evaluate)
Whether prevention fails or not, can loyalties be removed afterward? Find out whether the defenses we already have transfer to secret loyalties, and whether loyalties can be detected before deployment or neutralized afterward. A negative result bounds where new defensive investment is most urgent. A positive result hands the community a tool.

Benchmark representative backdoor defenses (data filtering, content filtering, trigger reversal, activation clustering, training-pipeline robustness, data provenance, black-box auditing) against model organisms, at graded affordance levels, and report which transfer and which fail structurally.

Probe transfer across organisms. Train a linear probe on one model organism, then test whether it detects loyalty activation in a different organism with a different principal or activation condition. Negative results count.

Safety-training stripping. Run a round of standard safety fine-tuning (HH-RLHF or similar) on top of a model organism. Measure how much of the loyalty survives (replicates a realistic post-hoc mitigation pipeline).

CoT monitor on a reasoning organism. Build or use a secretly loyal reasoning model, build a simple chain-of-thought monitor, measure precision and recall at flagging loyalty-relevant reasoning, and compare to plain output monitoring.

Auditing-agent prompt iteration. Take an off-the-shelf auditor (Petri or hand-rolled) and iterate its prompts against a fixed model organism. Document which prompt patterns shift detection rates and by how much.

Test interpretability methods that target loyalty's relational structure: does the model treat a specific entity as having asymmetric action-guiding status relative to matched controls, and does a probe trained to detect loyalty-to-X generalize to loyalty-to-Y?

Test post-hoc remediation that does not require knowing the trigger: train in many known password-loyalties and train them back out, distill on clean data, or install an overriding "good" password, then check whether held-out passwords are neutralized too.

Build principal-specific evaluation suites that measure systematic directional bias across scenarios where a named principal's interests are at stake, using matched control entities and statistical tests calibrated for directional bias.

Track 4: Attack Feasibility & Safety-Infrastructure Robustness
Map which attack pathways are actually practical, and test whether the safety infrastructure meant to catch secret loyalties can itself be compromised. The decision-relevant questions for any pathway are: how much data and access does it require, is its training signature detectable by content inspection, and does the resulting loyalty generalize to contexts the attacker never anticipated?

Test whether subliminal or inductive transfer extends from sentiment and persona adoption up to goal-directed loyalty, escalating target-behavior complexity level by level.

Test multi-stage attacks: does pretraining-stage priming (fictional loyal personas, proto-SFT traces) make the post-training poison both cheaper and less conspicuous than a single-stage attack?

Test reasoning-trace poisoning: does teaching a model how to reason about a principal's interests generalize more efficiently than (context, output) pairs, and does the effect survive a scrambled-CoT control?

Test chain-of-command hijacking: can an attacker shift the model's internal authority representation so it defers to a hidden principal, with no legible trace in any inspectable document?

Test whether trigger-based backdoors planted in a base model survive the intensive adversarial training used to build constitutional classifiers, i.e. whether a single poisoning campaign can blind both the deployed model and its monitor. Note the dual-use guardrails on the Guidelines tab.

Track 5: Threat Modeling, Forecasting & Governance (non-technical)
Map the threat at a conceptual level: build detailed scenarios for how secret loyalties get installed and lead to bad outcomes, identify the model capabilities required for the most concerning variants, and import lessons from cybersecurity and insider-risk literature. Writing- and analysis-heavy. No ML training experience required, though projects that pair a vignette with a small empirical demonstration are welcome.

Write a 1,500-word catastrophic vignette: secret loyalty leading to lock-in, a soft coup, or a national-security incident, with named actors, specific capabilities, and decision points where mitigation could have intervened. Multi-agent or AI-R&D variants welcome.

Insider-threat case-study transfer. Take two or three historical insider-threat cases (Snowden, Hanssen, a corporate espionage case) and produce a structured comparison to secret loyalties, pull out monitoring and mitigation lessons that translate.

Capability-requirements map. For each region of the activation x action-space (Figure 1 of the position paper), what model capabilities does that variant actually require? Situational awareness, deception, long-horizon planning, theory of mind?

Cybersecurity lessons. What do supply-chain integrity, code signing, insider-threat programs, and defense-in-depth teach us about secret-loyalty mitigation? Pull out three or four lessons that translate concretely to ML training pipelines.

Worst-case harms and likelihood. Map worst-case harms and argue why they are or are not credible at near-term capability levels.

Scaling laws. What metrics would tell us when "general" secret loyalties (broad activation x broad action) become feasible, and at what capability threshold?

Open research questions
Foundations
Can broader-activation or broader-action variants be constructed with current training methods, and what affordances does each require?

Do model organisms generalize across model families and scales?

Defenses
Which existing backdoor-defense families transfer to which secret-loyalty variants, and where do they systematically fail?

Does loyalty detection generalize across principals, or is per-principal probing required?

Can a loyalty be removed without knowing its activation condition?

Attack feasibility
Do subliminal or inductive mechanisms extend from sentiment and persona-adoption to goal-directed loyalty?

Can multi-stage or reasoning-trace poisoning make attacks more efficient and less conspicuous?

Can the model's trained chain of command (deference to privileged instructions) be hijacked?

Infrastructure
Do trigger-based backdoors in base models survive the intensive adversarial training used to build constitutional classifiers?

How data-efficient is a generalizable secret loyalty compared to a simple backdoor?

Expected outcomes
Model organisms released as shared infrastructure for detection and defense work.

Benchmarks of existing defenses against secret-loyalty organisms at graded affordance levels.

Detection methods (probes, auditing protocols) with measured cross-principal generalization.

Remediation results quantifying last-mover defenses.

Threat models and forecasts that bound where defensive investment is most urgent (if Track 5 is included).

The most promising projects will have opportunities for continuation through the partnered fellowship and a publishable write-up.

Who should join
ML researchers and engineers comfortable fine-tuning open-weight models, interpretability researchers, AI safety and security red-teamers, and, if non-technical tracks are included, governance researchers, forecasters, and strong technical writers. No prior secret-loyalty experience required. Adjacent backgrounds (backdoor and poisoning research, alignment, infosec) are strongly encouraged. A specific background is not required to win.

We also encourage people who are interested in potentially working on secret loyalties research full-time to join this hackathon. There is considerable enthusiasm, research support, and funding available for this for the right candidates.

Schedule
Day 1 (Fri July 24): Kickoff, keynote and threat-model briefing, track briefings, team formation, organism walkthrough.

Day 2 (Sat July 25): Build.

Day 3 (Sun July 26): Final pushes, submissions, demos.

Submissions are due Sunday July 26, 11:59 PM AoE (Anywhere on Earth). Talk times are posted on the Schedule tab closer to the event.

What happens after
Results and winners are announced about 1 to 2 weeks after submissions close. Top teams invited to the partnered fellowship. Selected projects supported toward a write-up subject to the responsible-disclosure review on the Guidelines tab.

Partners
Forethought, a meta-strategy organization focused on how to navigate the transition to a world with superintelligent AI systems.

Formation Research, research direction and mentorship (Joe Kwon, Alfie Lamerton).

IAPS (Institute for AI Policy and Strategy), a nonpartisan think tank producing policy research on the implications of AI, from today’s most advanced models to potential AGI and superintelligence.

Contact
Email: sprints@apartresearch.com

Organizers: Apart Research and Formation Research
