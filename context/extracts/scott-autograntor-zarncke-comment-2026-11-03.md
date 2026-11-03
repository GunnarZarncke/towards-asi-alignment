Source URL: https://www.lesswrong.com/posts/Sfkv6JF2ozmAkggKu/towards-the-autograntor/comment/PeiopN6zMXaJQf2CF
API (Markdown): https://www.lesswrong.com/api/post/towards-the-autograntor/comments/PeiopN6zMXaJQf2CF
Parent post: [Towards The Autograntor](https://www.lesswrong.com/posts/Sfkv6JF2ozmAkggKu/towards-the-autograntor) (Scott Alexander, 2026-11-01)
Parent comment (Adam Scholl): https://www.lesswrong.com/posts/Sfkv6JF2ozmAkggKu/towards-the-autograntor/comment/5TngP4sgoEu2WwmzK
Author: Gunnar Zarncke
Posted: 2026-11-03 03:05:23Z

# Comment on Towards The Autograntor

Scott's project is a showcase of the alignment problem in the small. Such small-scale projects with high involvement of LLMs are a good lens for thinking about and exploring approaches for addressing alignment subproblems. The big labs also have [very high LLM involvement](https://www.anthropic.com/institute/measuring-pace-of-ai-development), but the scale obscures with accidental complexity - and we don't get the details anyway.

Scott wrote:

> I would like to keep using my own reasoning, with the autograntor as a supplement, but this has been increasingly hard. The lure of a specific cost-effectiveness number attached to each grant is a powerful anchor, even though I know how many tries it took before the autograntor numbers looked sane, and how many flaws it probably still has.

So what can he do? The cheapest fix is to *write a guessed $/point and PERCY before looking at the report. Then track how often you significantly change that number vs the autograntor*.

I do something like this in my own [project](https://github.com/GunnarZarncke/towards-asi-alignment). A few weeks ago, I realized that I had the same problem: I used AI agents to get an overview of [The Open Problems of the AI Alignment Field and their Cruxes](https://www.lesswrong.com/posts/quC3LLPXCashfnKZY/the-open-problems-of-the-ai-alignment-field-and-their-cruxes). But am I not at risk of falling into all of the problems I want to avoid while doing so? I came up with an approach to track whether I still maintain control of the process, rather than just rubber-stamping LLM edits, to track AI authorship, whether references point to the real thing, whether the project has my voice, and other instruments I experiment with.

So going by the [alignment subproblems](https://www.lesswrong.com/posts/quC3LLPXCashfnKZY/the-open-problems-of-the-ai-alignment-field-and-their-cruxes), we can see the following failure modes in Scott's project. And I am grateful that he has been so open about this work and I do not see these as flaws in his project but as an unavoidable consequence of how using AI without alignment engineering has to look at this stage. (emphasis in the quotes below is mine)

**[Embedded Agency](https://www.lesswrong.com/w/embedded-agency)**

> The parts I could outsource to AI were sparkling, perfect, exhaustive — but they were all **tacked together** with shoddy connective tissue formed by the Mark 1.0 human brain.
>
> FutureSearch calls failed, which is a constant hazard of workflows requiring different AIs to connect to each other
>
> [the workflow] summon Opus and Fable subagents, have them each do the estimate separately, have them each argue ... the main Claude ... make a final decision

What is the agent that Scott is trying to align? It is not the claude-opus-5.5 model or a single Claude Code session. It is Claude + Common Law + FutureSearch + Scott (human in the loop) + other evaluators + external memory (notes that can get lost).

The problem is not that Claude writes bad code or intends to defraud Scott. It is that a grantmaking system of uncertain composition is spiraling out of control. The first step of alignment here is to figure out the unit to align. In such a small system that is relatively easy. Scott has already told us the components. Except...

>! now we have clones of grant-adversarial-estimate and these may take on a life of their own, fork and merge.

**[Value Learning](https://www.lesswrong.com/w/value-learning)**

> **Can I really translate my beliefs about what matters** in AI safety into a list of milestones, each with a **consistent point value**?
>
> ‘Harry Potter And The Methods Of Rationality’ was an especially controversial milestone — **one person rated it as 1 point, another person as 75,000 points**.
>
> I don’t really get the impression that if Apart were actually much more on the ball than other alignment organizations ... or if they were much less on the ball ... a complete sham ... the autograntor would be capable of noticing this

Scott's milestones compress what matters to him into a scalar. And the models (and reviewers) translate complex papers, grant applications, and projects into these numbers. How can he be sure this captures what he values? He is already breaking down the evidence for the points for interpretability. But he could try interventions that he expects to change the value (such as changing a crucial sentence in the application) and see if the value moves points in the expected direction. Or he could let the autograntor score adversarially crafted applications. I bet some people are already working on that.

**[Corrigibility](https://www.lesswrong.com/w/corrigibility-1)**

> **I would like to keep using my own reasoning, with the autograntor as a supplement, but this has been increasingly hard.** The lure of a specific cost-effectiveness number attached to each grant is a powerful anchor, even though I know how many tries it took before the autograntor numbers looked sane, and how many flaws it probably still has.
>
> I find myself glazing over the analysis as I read it, thinking ‘yeah, that number is probably right … yeah, that number is probably right too’.
>
> I decided to hand them off to the AI … record its ruling in a Common Law document. Later autograntor runs would respect previous rulings … I’m delinquent in my resolution to review it regularly.
>
> It sometimes makes new insane common law rulings, and these silently poison several runs before they poison one loudly enough that I notice, investigate, and correct it.

It is not enough to be able to stop the system. You need to avoid rubber-stamping, preference capture and [gradual disempowerment](https://www.lesswrong.com/posts/pZhEQieM9otKXhxmd/gradual-disempowerment-systemic-existential-risks-from). How could Scott avoid that here? He could measure how often he rubber-stamps, i.e., doesn't amend anything (points or laws). Anybody has an idea what the corresponding [flute and sling](https://www.lesswrong.com/posts/aRxDLju75KXD6PCpB) are here?

**[Tiling](https://www.lesswrong.com/lw/hmt/tiling_agents_for_selfmodifying_ai_opfai_2)**

> Prompt: “feel free to **invent new milestones**, which you can price by common-sense comparison to the existing ones on the list"
>
> **Later autograntor runs would respect previous rulings** for the big questions and add their own sub-rulings

The autograntor (the system, not the model) can self-modify, including the instrument he uses to align it. What could he do? Make sure that he still understands all of the laws. Currently, it is a sprawling list without structure, keeping a record of why laws were added may help interpretability. In principle, you'd want to check that amendments preserves the ability to correct in the future, though here that is probably not needed.

**[Gradual Disempowerment](https://www.lesswrong.com/posts/pZhEQieM9otKXhxmd/gradual-disempowerment-systemic-existential-risks-from)**

> As far as I can tell, this dumbest possible strategy worked well” (milestone points as selector)
>
> every method of adjusting for double-counting ... fails in a different way”
>
> I sort of vibe-coded fixes to them, and I worry that I spotted the obvious ones … but that there are many smaller ones that usually cancel out
>
> Milestone worldview spread: geometric mean difference between Scott and knowledgeable survey respondents “2.9x, 4.4x, 6.9x, and 8x

This is probably the clearest pattern: Building a system that [optimizes proxies](https://www.lesswrong.com/w/goodhart-s-curse) even when he knows about the failures. I kind of wonder if he is giving us this tool in the hope that we work it out. Anyway, what can he do? Diversify proxies, holdout grants, dropout fields from evaluation. ML has lots of tools for this that should work on this project.

**[Inner Alignment](https://www.lesswrong.com/w/inner-alignment)**

> FutureSearch and Preseen … occasionally lost the attachments and hallucinated their contents, and produced results off by an order of magnitude
>
> **I can’t tell** whether the probability it ultimately got was its own guess (Claude is pretty good at this …) or its reading some intermediate result off the FutureSearch connector
>
> ChatGPT consistently gave results 2-3x better (more cost-effective) than Claude for everything
>
> The autograntor is sufficiently ‘more sophisticated’ than I am … I don’t feel capable of directly judging its reasoning, instead having to resort to indirect methods

This shows that we need interpretability not only of what goes on in the models but also about what goes on in the system composed of them. At least here all the information is right there in the form of code, laws and traces, and he still struggles. So even if you can interpret the thing, you still need aggregate instruments. I use Lean to check derivations. Scott could let the LLMs create automated consistency checks. Adversarially testing the tool would also help. Am I doing that right now?

**[Grounding Drift](https://www.lesswrong.com/w/symbol-grounding)**

> something must be wrong with these numbers — a really great alignment paper is worth 5,000, so this suggests … whereas common-sensically, convincing five million people is clearly better
>
> [Common Law rulings that] would have misled me if I had **interpreted them in the way that seemed natural to me**

This shows that things within the autograntor do not seem to mean what he thinks they mean. And with growing complexity and more and more edge cases, that is not unlikely to get worse instead of better. What can he do? He should connect the symbols in the report to the source of the data. One simple step could be to split the Common Law into math, i.e., code, and semantics. In code, what a symbol refers to is always unique and by referencing the code symbol in the law text, the relation becomes stable. If this project were larger, you'd also want to make sure that each run tracks against which code version it was running. Scott may still not want to reread the whole law after each rewrite or the whole report for a grant evaluation, but one could build a calculator that determines the highest impact elements and highligt and check these in the reports and laws.

**Deployment Safety ([AI Control](https://www.lesswrong.com/w/ai-control))**

> I plan to test the autograntor in my next Lightcone Commons grant round, hopefully before any of the other evaluators have formed opinions, then check how well it matches their outcomes

> I’m left in the position of trying to catch up to and understand their work

Scott is not the only one who is putting such opaque agent-driven systems in the position to make important financial decisions. The upside is potentially large! But the question is still: Can we trust such a system when it has no adequate safety case (a set of sufficiently calibrated handles on the above subproblems)? Good thing this is small now, but I imagine into what an engine for multi-billion fund allocations this may evolve.
