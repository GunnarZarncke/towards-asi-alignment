---
external:
  - label: "Dwarkesh Patel — Paul Christiano: We could be 12 months away from AIs that can overthrow the government"
    url: https://www.dwarkesh.com/p/paul-christiano-2
---

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--letter"><span class="src-legend-swatch" aria-hidden="true"></span>Paul Christiano (purple)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this project (black)</span>
</p>

**If you remember one thing:** The plan is to let the AIs find the alignment path. And to stop if they don't.

The [Dwarkesh RSI news](/cards/field-news-dwarkesh-rsi-alignment-gap-nov-2026/) concluded that capability has a path to growth and alignment hasn't. Now Dwarkesh asked Paul Christiano what the plan is.

## Patching a hack trains hiding

What happens when you find a hack and penalize it?

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · Why an AI might want to takeover</p>
<p>If you fix the problem in this way, which you might think of as a Band-Aid, you still have an adversarial relationship with your AI. But now the AI doesn’t win the game by hacking your cluster and then you noticing it hacked your cluster. In order to win the game, the AI has to make sure that you do not notice that it hacked your cluster.</p>
</blockquote>

The correction is real. It also moves the optimization pressure onto your detection.

## Clean environments are not enough

Could we just remove the hacks from training?

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · The best plan we have is to build the plane as we fly it</p>
<p>It’s very dicey to not have any opportunities to hack in training, which is basically a precondition for this approach working. And then it’s very dicey because we don’t actually have a good scientific understanding of how this works. Our best expectation is that models will learn to hack at deployment time, even if they never hack in training.</p>
</blockquote>

And the careful-grader approach has an expiry date:

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · The best plan we have is to build the plane as we fly it</p>
<p>I think it will work for some amount of time, and then it will break. […] We don’t know exactly when it breaks down.</p>
</blockquote>

## The plan, stated

Dwarkesh summarizes: let the AIs loose on approaches with a few percent chance each, hope they find one and are still on our side. Christiano:

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · The best plan we have is to build the plane as we fly it</p>
<p>That is the plan. I agree that that is the plan. We can talk about whether they have a couple percent or tens of percent.</p>
</blockquote>

This is the missing alignment loop from the RSI card, delegated to the systems whose alignment is in question.

## Two saving throws, one die

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · The best plan we have is to build the plane as we fly it</p>
<p>Those are my two saving throws. Each of them is a 50% chance, and bam, we’re at like a 75% chance things are okay. But that does involve being able to stop if things are not okay.</p>
</blockquote>

75% assumes the throws are independent. Stopping needs a signal:

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · We could be &lt;12 months away from AIs that can overthrow the government</p>
<p>It needs to be the case that you’re able to tell the systems are not well controlled. It also needs to be the case that if you stop, that fixes the problem.</p>
</blockquote>

The first throw fails when the solver's work cannot be checked. The second fails when the warning cannot be trusted. Both read through the same observations that the first section says the system is being pushed to hide. When one fails, the other is likely to fail with it.

He names the second condition's other failure himself: if weights or algorithms leak, stopping does not fix the problem.

## The warning comes late

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · Crossing the sim-to-real gap</p>
<p>For the first six months of that year, you look at the systems and say, “Well, they were previously superhuman at math, and now they’re incredibly superhuman at math.” But if you go and talk to someone, there’s no real ability to say, “Therefore, they are a threat to humanity.”</p>
</blockquote>

And outside the labs there is no shared way to read it:

<blockquote class="src-quote src-quote--letter">
<p class="src-quote-attr"><a href="https://www.dwarkesh.com/p/paul-christiano-2">Paul Christiano</a> · If labs keep racing without security</p>
<p>We are not in a regime where there is a meaningful scientific discussion about how you assess whether your AI systems are aligned. […] Independent scientists really have no idea whether the systems being produced are aligned or how you would tell.</p>
</blockquote>

Scientists could start one outside the labs: prediction markets on fixed alignment challenges, like the [prediction markets proposed here](/predictions/). A market price is not a stop rule, but it puts a public number on whether the evidence exists.
