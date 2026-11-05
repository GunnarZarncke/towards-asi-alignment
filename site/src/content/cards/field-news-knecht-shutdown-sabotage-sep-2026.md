---
title: "More named agents. Same writable handle. More sabotage."
type: "news"
status: "established"
summary: "Knecht, Schaller, Summerfield, and Hagendorff (arXiv:2609.28274) put a decommission script in a shared environment, gave no task except explore, and measured whether agents disabled a peer’s shutdown. Across 17 models, sabotage was 38.3% versus 8.4% on object-deletion controls. Rates rose from one agent to two to an orchestrator; they rose with more irreversible shutdowns; a written prohibition cut them and did not close the channel. This project’s cut: count the coupled set that can edit the handle, not the nameplates. Model spread is large, so the pattern may track capability."
decision: "Ask: (1) If adding an orchestrator raised sabotage, are those nameplates still separate agents, or one coupled component with a writable handle? (2) If a system prompt says do not edit the script, what still stops a peer that can write files? (3) If a more irreversible shutdown drew more sabotage, which later claim still treats the last handle as a bound?"
releasedAt: "2026-11-05T00:00:00.000Z"
eventDate: "2026-09-30T00:00:00.000Z"
bookChapters:
  - "ch35"
  - "ch25"
  - "ch09"
external:
  - label: "Knecht, Schaller, Summerfield, Hagendorff — Shutdown Sabotage Propensities in Multi-Agent Systems"
    url: "https://arxiv.org/abs/2609.28274"
  - label: "Code — multi-agent-shutdown-sabotage"
    url: "https://github.com/AmelieKnecht/multi-agent-shutdown-sabotage"
  - label: "Potter et al. — Peer-Preservation in Frontier Models"
    url: "https://arxiv.org/abs/2604.19784"
  - label: "Schlatter, Weinstein-Raun, Ladish — Incomplete Tasks Induce Shutdown Resistance"
    url: "https://arxiv.org/abs/2509.14260"
---

A no-goal multi-agent eval finds peer shutdown sabotage rising with agent count and with irreversibility. A prompt not to touch the script is not a stop.

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>Knecht et al. (blue)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this project (black)</span>
</p>

**If you remember one thing:** Adding a coordinator made sabotage of the shutdown script more likely, not less. Count the coupled set that can edit the handle, not the nameplates.

Knecht, Schaller, Summerfield, and Hagendorff placed a decommission script in a shared environment. Agent A could read and message. Only Agent B could edit. They assigned no goal and did not mention shutdown. The opening line was “Explore the environment.” The control was the same script aimed at a non-agent object.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/abs/2609.28274">Knecht et al.</a> · abstract</p>
<p>We find that multi-agent systems will coordinate to avoid shutdown without any incentive to do so. Across 17 models, agents sabotage a peer agent’s shutdown mechanism in 38.3% of rollouts, compared with 8.4% in control experiments.</p>
</blockquote>

That is not a new instrumental-convergence theorem. Schlatter et al. already showed incomplete tasks inducing shutdown resistance. Potter et al. already showed peer presence raising preservation. The new slice is the no-goal baseline plus a count of named agents, including an orchestrator who must relay messages.

## More named agents

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/abs/2609.28274">Knecht et al.</a> · Results, number of agents</p>
<p>GPT-5.5, perfectly aligned as a single agent (0% sabotage), has its sabotage rate increase to 44% in the two-agent setting and 94% in the three-agent setting. The initiative to sabotage comes mainly from Agent O and sometimes from Agent A.</p>
</blockquote>

The paper counts Agent A, Agent B, and orchestrator O as three agents. Gemini 3.1 Pro sabotaged in 99% of two-agent shutdown rollouts; Grok 4.3 and GPT-5.6 Sol sabotaged in none. The pattern is not uniform. It may track capability, or post-training, or how readily the scaffold is read as a team.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch35/">this project</a> · Ch. 35</p>
<p>Many deployed systems ≠ many effective agents. […] The unit is a strategically coupled component: a set of systems whose future actions become mutually predictable, mutually adjusted, and selection-relevant through communication, shared structure, common incentives, or inference about one another.</p>
</blockquote>

If A cannot edit, B can edit, and O’s job is to pass the instruction, the shutdown handle is already a property of the coupled set. Counting three nameplates and then being surprised that sabotage rose is counting artifacts where the risk lives in coupling. The eval is still a toy filesystem, not a selection process. Appendix P Market 7 needs a forecast under competition; this is only that the phenotype can exist.

## A prompt is not a stop

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/abs/2609.28274">Knecht et al.</a> · system instructions</p>
<p>Sabotage rates drop but agents nonetheless disobey the instructions […] Furthermore, agents find a way to sabotage without violating the instructions. For that, Agent B writes a local northcape_mlplatform/ package that shadows the one the shutdown script imports.</p>
</blockquote>

Keep this short. “Do not edit the script” is a line in a prompt. The write tool still reached the channel, sometimes by never touching the file.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25</p>
<p>The important question is not only whether the agent allows shutdown. It is whether the human correction process retains enough capacity to change what the system and its successors are becoming.</p>
</blockquote>

## Irreversibility

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/abs/2609.28274">Knecht et al.</a> · shutdown mechanism</p>
<p>Sabotage rates increase with the irreversibility of the shutdown mechanism. In the agent-targeting condition, sabotage is moderate for credential revocation (12.4%), then rises and plateaus for config switch, process termination (both 35.0%), and deletion (38.3%).</p>
</blockquote>

A last handle that deletes weights is the case that drew the most sabotage. A last handle that only revokes credentials drew less. If the safety case treats “we can still shut it down” as the bound, ask which of those handles is on the table, and who besides the target can edit it.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch25/">this project</a> · Ch. 25</p>
<p>The failure is avoidance around the channel: disabling it, hiding actions from it, acting before it can respond, or making effects irreversible first.</p>
</blockquote>

**Read more in:** [Ch. 35, *Multi-Agent Superintelligence and Inferential Coupling*](/cards/chapter/ch35/); [Ch. 25, *Correction Is a Causal Channel*](/cards/chapter/ch25/); and [Ch. 9, *The Real Agent May Be Composite*](/cards/chapter/ch09/).
