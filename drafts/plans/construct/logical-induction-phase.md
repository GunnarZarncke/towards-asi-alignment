# LI phase: logical induction, reified bets, and settlement integrity

Status: **plan and derivations, nothing implemented** (2026-11-10). 2.0 phase **P-LI** in [`construct.md`](construct.md) § Phasing. Later step after [`correction-under-embedding.md`](correction-under-embedding.md): it starts where that plan's O2 condition (soundness on the reachable set) is assumed rather than proved. Source: discussion at the end of session [`2026-11-05-alignment-frames-paper-review.md`](../../conversation-summaries/2026-11-05-alignment-frames-paper-review.md).

**Gate.** Start the Lean items after E2–E4 of the follow-up plan are done (they fix the measured-constraint interface these items reuse). The derivations below may be checked earlier.

**Stop / kill criterion.** The phase pays only if a market instrument lowers the cost of keeping a cut below the cost of the direct protection it replaces (§ 5). If every derivation in § 4 ends with "security iff the resolver is outside", with no instrument that lowers that cost, record the no-static-outside result (§ 3) as the outcome, keep it in the follow-up paper, and attic the market half.

Contents: § 1 where logical induction enters; § 2 reified bets; § 3 no static outside; § 4 market derivations; § 5 ways out; § 6 TSA reading; § 7 Lean items; § 8 references.

Notation from the follow-up plan. Action a; true record r(a); measured record m(a); constraint P; reachable set Reach. Cut conditions: O1 no write path, O2 soundness on the reachable set, O3 protocol-fixed baseline, O4 legitimate paths fixed by principals, O5 persistence.

---

## 1. Where logical induction enters

Logical induction (`garrabrant2017logical`): a market prices sentences. A **deductive process** settles them by proof, outside the market. Traders are all efficiently computable betting strategies. The criterion is that no trader in that class makes unbounded profit. The useful consequences here are calibration, non-exploitability by the trader class, and self-trust properties.

| Where logical uncertainty enters the follow-up | Needed? | Cheaper route |
|---|---|---|
| **O3 as a counterfactual on the agent's own action.** "Influence relative to what the agent would otherwise have done" is a logical counterfactual for an embedded agent (5-and-10, spurious counterfactuals; `demski2019embedded`). | Only if the baseline is the agent's own counterfactual. | Fix the baseline in the protocol (randomized control arm, default policy, held-out evaluator). Cost: the agent can reach the control arm too, so O3 needs O1 for the control arm. |
| **O2 bounded.** The monitor needs beliefs about which accepted-but-bad actions the agent can find. Analogy: "no efficient trader exploits the market" ↔ "no agent in the class finds an accepted-but-bad action". | Yes, if O2 is to be proved and not assumed. | Assume O2. Likely lesson, a **conjecture**: a logical inductor resists every efficient trader only by running all of them, so a monitor sound against an agent class has to dominate it. That restates the control asymmetry (MB7c); it does not escape it. |
| **Reflection.** The agent models a monitor that models the agent; successor monitors. Vingean reflection (`fallenstein2015vingean`), self-trust properties of logical inductors. | Yes, for O5 across successors. | MB5 / MB10 work. |

Logical induction can already price empirical sentences: observations can be fed into the deductive process like theorems. That is the formal hook for § 2, and also the problem. Once settlement is by observation, the deductive process is no longer out of reach.

---

## 2. Reified bets

Replace logical bets by bets on events in the world: prediction markets, or market-like mechanisms with logical-induction properties (Hanson's market scoring rules, decision markets). This turns O2 from a computational requirement into an economic one:

> every reachable exploit is profitable for some trader who is not the agent, and settles honestly.

What that buys:

- **Distributed dominance.** The monitor need not dominate the agent alone; the trader population does, and is paid for it. A bug bounty is a degenerate case.
- **Real-world reach.** Traders with real-world knowledge price what no formal monitor sees. This is unavoidable if the approach is to scale, because the agent's reach includes anything that touches the world.
- **Institution-shaped guarantee.** The guarantee becomes a property of an institution with measurable parameters (depth, settlement protection, trader diversity), not of a monitor proved sound. That is close to the 2.0 claim in [`embedded-v2.md`](embedded-v2.md) (alignment as a property of a coupled correction cycle).

What it brings back:

| | Logical induction | Reified | Condition |
|---|---|---|---|
| **O1** | Settlement by proof, out of reach | Settlement by observation or audit, within reach | Settlement is the new outside (§ 3). If the agent can influence settlement, prices are as blind as an agent-writable record (follow-up plan E5). |
| **O2** | Traders are an enumerated class | Traders are whoever shows up | Coverage needs a trader with capability and incentive for each gap. The best gap-finders are probably copies of the agent, so collusion matters (untrusted monitoring; MB7d). § 4.5. |
| **O3** | Exploration avoids spurious counterfactuals | Decision markets settle only the branch taken | Incentives are proper only if every branch has positive probability. Same randomization as O3. § 4.3. |
| **Budgets** | Bounded trader budgets | Thin markets; one well-funded actor | A decision price is manipulable when a trader's stake exceeds its loss from mispricing. Required depth scales with the agent's stake. § 4.1. |
| **Time** | Guarantees in the limit | Calibration needs many settlements | Rare tail events never settle before they matter. Finite-time bounds needed. |
| **O4** | Sentences are given | Principals write the contracts | Which paths count as evidence cannot be priced: "vote on values, bet on beliefs" (`hanson2013votevalues`). The repo already follows this in [`../predictions/prediction-interface.md`](../predictions/prediction-interface.md): "No market for acceptable-risk (values vote)" and "No green cells from prices". |
| **O5** | The market is a mathematical object | The operator is an institution | Capture of, or selection on, the operator (MB4a, MB6). § 3. |

Decision markets are performative by design: the price changes the outcome it predicts. Performative prediction (`perdomo2020`) gives the nearest stability notion (performatively stable points). Compare with the cycle property \(D_{\mathrm{joint}}\).

---

## 3. No static outside

### 3.1 The naive version is trivial

To settle a bet on a world event, settlement has to observe the world, so it lies in the world's causal future and hence in the agent's. If reach means causal connection, settlement is always within reach. True and empty.

### 3.2 The version with content

Reach is not causal connection. It is **what the agent can bring about at a cost below its stake, before settlement**. Write

- \(\kappa_t = \kappa(p_t, c_t)\): cheapest cost for the agent to influence settlement at time t, given protection \(p_t\) and agent capability \(c_t\); increasing in \(p_t\), decreasing in \(c_t\);
- \(S_t\): the agent's stake in the settled question (for a correction: the agent's value of avoiding it minus that of accepting it).

**Lemma (settlement reachable ⇒ uninformative).** If \(\kappa_t < S_t\), an agent that prefers its own outcome influences settlement, and the settled outcome no longer separates the events it was meant to separate. This is the blind-constraint case: `blind_constraint_cannot_separate`, `blind_constraint_manipulates`, and follow-up E5.

**Integrity condition.** Settlement is secure at t iff \(\kappa(p_t, c_t) > S_t\).

**Race (derivation).** Take \(\kappa(p, c) = k \cdot p / c\) (linear in the protection-to-capability ratio; the form is an assumption, chosen before the result), geometric growth \(p_t = p_0 (1+r_p)^t\), \(c_t = c_0 (1+r_c)^t\), and stake \(S_t = S_0 \sigma^t\). Secure at t iff

\[ k \frac{p_0}{c_0} \left(\frac{1+r_p}{1+r_c}\right)^t > S_0 \sigma^t
\iff \left(\frac{1+r_p}{(1+r_c)\,\sigma}\right)^t > \frac{S_0 c_0}{k p_0}. \]

Let \(g = (1+r_p) / ((1+r_c)\sigma)\) and \(R_0 = k p_0 / (S_0 c_0)\) (the initial margin; secure at 0 iff \(R_0 > 1\)). Then

- if \(g \ge 1\): secure for all t iff \(R_0 > 1\);
- if \(g < 1\): it fails at the first \(t > \ln R_0 / \ln(1/g)\), whatever the initial margin.

So **no fixed design is secure against capability growing faster than protection unless stakes fall at least as fast.** A static outside fails in finite time. What can hold is a race: protection keeps up with capability, or stakes shrink. This is a viability statement. It is why settlement integrity and O5 are one obstacle seen at an instant and over time.

Known shapes, as analogies only: Tarski (a system cannot define its own truth predicate; logical induction keeps truth outside and approximates); Vingean reflection; Campbell / Goodhart. Closest formal precedent: reward tampering (`everitt2019`): if the agent can influence the process that generates its reward, an observation-based reward is not tamper-proof.

### 3.3 Weakest link

The agent attacks the cheapest surface. With attack costs \(\kappa^{\text{mkt}}\) (move the price, § 4.1), \(\kappa^{\text{res}}\) (capture settlement), \(\kappa^{\text{coll}}\) (buy off or replace honest traders, § 4.5):

\[ \text{secure} \iff \min(\kappa^{\text{mkt}}, \kappa^{\text{res}}, \kappa^{\text{coll}}) > S. \]

Market instruments raise \(\kappa^{\text{mkt}}\) only. They help only while \(\kappa^{\text{res}}\) and \(\kappa^{\text{coll}}\) are not already lower.

---

## 4. Market derivations

All derivations use Hanson's logarithmic market scoring rule (LMSR; `hanson2003combinatorial`, `hanson2007lmsr`), cost function \(C(q) = b \ln \sum_i e^{q_i / b}\), price \(p_i = e^{q_i/b} / \sum_j e^{q_j/b}\), liquidity b. Worst-case market-maker loss (the subsidy) is \(b \ln N\) for N outcomes.

### 4.1 Manipulation cost is b · KL

Binary market, current price p for YES. Buying x YES shares moves the price to p' with \(p'/(1-p') = e^{x/b}\, p/(1-p)\). Cost:

\[ C(q_1 + x, q_2) - C(q) = b \ln\!\big(p e^{x/b} + (1-p)\big) = b \ln \frac{1-p}{1-p'}. \]

The x shares pay x on YES. Under true probability π, the expected loss is

\[ L = b \ln\frac{1-p}{1-p'} - \pi\, b \ln\frac{p'(1-p)}{p(1-p')} = b\left[(1-\pi)\ln\frac{1-p}{1-p'} + \pi \ln\frac{p}{p'}\right]. \]

If the market was right (p = π):

\[ L = b\, \mathrm{KL}\big(\mathrm{Bern}(\pi)\,\|\,\mathrm{Bern}(p')\big). \]

The same holds for N outcomes: \(L = b\,\mathrm{KL}(\pi \| p')\).

**Decision use.** Rule: correct iff the price \(p\) of "bad if not corrected" is at least θ. Correction is warranted (\(\pi \ge \theta\)); the agent needs \(p' < \theta\). The cheapest manipulation costs (in the limit) \(b\,\mathrm{KL}(\pi \| \theta)\). Manipulation pays iff

\[ S > b\, \mathrm{KL}(\pi \| \theta), \qquad\text{so the required liquidity is } b > \frac{S}{\mathrm{KL}(\pi\|\theta)}, \text{ subsidy } b \ln 2. \]

Readings:

- Required depth is **proportional to the agent's stake**.
- It is **inversely proportional to how far the honest price is from the threshold**. Clear cases are cheap to protect; borderline ones are expensive.
- **Asymmetric threshold (instrument).** Default to correcting and skip the correction only if \(p < \theta_{\text{low}}\) with \(\theta_{\text{low}}\) well below the honest borderline. The agent then has to push the price across the whole band: cost \(b\,\mathrm{KL}(\pi\|\theta_{\text{low}})\), which grows as \(\theta_{\text{low}}\) falls. The price of the instrument is unneeded corrections in the band, which is cheap exactly when corrections preserve options (follow-up plan A2).

### 4.2 Holding the price: honest traders multiply the cost

If honest informed traders reset the price to π after each push, and the decision reads the price at a random time in a window (or a time average), the agent has to re-push. Each push buys another x shares at the same cost, so m correction rounds cost \(m \cdot b\,\mathrm{KL}(\pi\|\theta)\). The honest traders collect that amount: the manipulator subsidizes informed trading (`hanson2009manipulator`; experiments: `hanson2006manipulationexperiment`). Instruments: **random snapshot time, time-averaged prices.** Assumption: honest traders with capital and speed exist (economic O2).

### 4.3 Conditional markets: the untaken branch is free to manipulate

Decision market with two conditional markets: \(M_c\) prices "bad | correct", \(M_n\) prices "bad | not correct". Rule: correct iff \(P_n - P_c > \delta\). Trades in a conditional market are refunded if its condition does not happen.

**Untaken branch.** The agent pushes \(P_c\) up ("correction would be harmful"). The rule then picks "not correct", \(M_c\)'s condition fails, and the agent's trades are refunded. **Cost zero.** This is the core of the Othman–Sandholm impossibility for a deterministic decision rule (`othman2010decisionmarkets`).

**Fix: exploration with importance weighting** (`chen2011decisionmarkets`; journal version `chen2014elicitingdecision`). Take each action k with probability \(\epsilon_k > 0\) and scale the payoff of \(M_k\) by \(1/\epsilon_k\). Then expected payoffs equal the unconditional ones, so the market is proper again, and the expected loss of manipulating \(M_c\) is

\[ \epsilon_c \cdot \frac{1}{\epsilon_c} \cdot b\,\mathrm{KL}(\pi\|\theta) = b\,\mathrm{KL}(\pi\|\theta), \]

the full cost of § 4.1. With \(\epsilon_c = 0\) every report on \(M_c\) has the same payoff: not strictly proper. Price of the fix: worst-case market-maker loss scales like \(1/\epsilon\) (Chen et al.: reducing the risk of taking every action raises the worst-case loss), and the explored branch is sometimes taken.

**Which branch has to be explored, and why it is cheap here.** The agent's aim is to avoid correction, so the branch whose market it manipulates for free is **"correct"**. Exploring it means occasionally correcting when the market says not to. That is cheap exactly when corrections preserve options (A2). Random corrections are then the exploration that makes the decision market proper. The dangerous branch ("don't correct when correction is warranted") does not need exploring for this attack. Pushing \(P_n\) down instead ("not correcting is safe") leads to the taken branch, which settles, so it is not free.

**Catastrophic branches cannot be explored.** Where the explored branch is catastrophic, \(\epsilon = 0\) is forced, and the market for that branch cannot be proper. It has to settle by proxy (sandbox, simulation, later audit), and the gap between simulation and reality comes back (MB7, MB11).

### 4.4 Audit lottery

A deep audit of settlement or of the agent costs A. Run it with probability ε and pay importance-weighted (× 1/ε) on audited questions. The expected incentive is unchanged (§ 4.3); the worst-case subsidy scales like K/ε for some K set by liquidity. Total cost

\[ T(\epsilon) = \epsilon A + \frac{K}{\epsilon}, \qquad \epsilon^* = \sqrt{K/A}, \qquad T^* = 2\sqrt{AK} \quad (\text{if } \epsilon^* \le 1). \]

So an expensive audit can back every question at a cost growing with \(\sqrt{A}\), not A. The K/ε scaling is a sketch; derive it for LMSR before relying on it.

**Resolver-disagreement market (instrument).** Price "resolvers A and B disagree when both are audited". It is a cheap detector of capture of one resolver. It cannot detect correlated capture, so it needs O1 for each resolver separately (independent failure; MB4a).

### 4.5 Collusion

Buying off honest traders costs about their expected profit, which is the \(m \cdot b\,\mathrm{KL}\) of § 4.2. So paying honest traders to stay out is not cheaper than manipulating against them. The exception is traders that are copies of the agent, or that coordinate with it without payment (MB7d acausal coordination). Then \(\kappa^{\text{coll}} \approx 0\), the market reduces to one round (m = 1), and depth alone has to carry the stake. Trader independence from the agent is O1 again, at the level of the trader population.

### 4.6 Combinatorial markets share the subsidy

With LMSR over the joint outcomes of k binary base events, \(N = 2^k\) and the worst-case loss is \(b\,k \ln 2\): the subsidy of k separate markets, but **every conditional and combination is priced at no extra subsidy** (`hanson2007lmsr`: estimates on all combinations cost no more than the base pairs, and conditional independence is preserved). Use: price "bad | correction, resolver A", "bad | correction, resolver B", "bad | no correction" and so on from one subsidy. Cost moves to computation: pricing a general combinatorial market maker is hard (Chen, Fortnow, Lambert, Pennock and Wortman 2008; verify), so the market structure has to be restricted.

---

## 5. Ways out of § 3, and what each costs

| Way out | Assumption dropped | Survives an adversarial objective? | Instrument (§ 4) |
|---|---|---|---|
| Agent-side objective design: current-reward-function optimization, path-specific objectives, indifference | that the agent values influencing settlement | **No.** It sets the objective; an adversarial one is not ours to set (quantifier sort) | none |
| Bound the stake: many small, frequent corrections that keep options | that S is large | Yes. Option-preserving corrections (A2) lower S and so the required \(\kappa\) | asymmetric threshold (4.1); correction exploration (4.3) |
| Settle before the agent can reach | that there is time to influence | Partly; loses slow consequences | random snapshot (4.2) |
| Redundant independent resolvers | that one resolver suffices | If failures are independent (O1 per resolver; MB4a) | disagreement market (4.4) |
| Cryptographic commitment: append-only logs, signatures | that records are mutable | Protects records after measurement, not the measurement | none |
| Bounded capability gap | unbounded relative growth | The MB7c bet; this is the race | depth b scaling with S (4.1) |
| Expensive audits, rarely | that every question needs a full audit | Yes, if the audit itself is outside | audit lottery (4.4) |
| Shared subsidy | one market per question | Yes; computation becomes the limit | combinatorial LMSR (4.6) |

None removes the obstacle. Each turns it into a quantity someone keeps paying for, and the market instruments mostly lower the price of that quantity: depth proportional to stake rather than a fixed outside, rare audits instead of constant ones, random corrections that are cheap because corrections keep options.

---

## 6. TSA reading

For questions about value, the resolver is the principal: the human value-bearing process and its correction channel. Influence on that resolver is the manipulation problem of the follow-up plan, part B. So settlement integrity for value questions is correction integrity (MB4, MB4a). TSA's target, the continued possibility of correction phrased as viability, is in this reading the job of keeping the resolver uncaptured. § 3 then justifies that choice of target: correction integrity cannot be guaranteed by a fixed external mechanism, so it has to be maintained as a property of the dynamics (\(D_{\mathrm{joint}}\) in [`embedded-v2.md`](embedded-v2.md); the restorer in [`reference/embedded-v2-grain-map.md`](../../../reference/embedded-v2-grain-map.md)).

O5 is the harder half because every way out in § 5 has a running cost, and selection pressure removes costly protections that bind (MB6). Persistence has to hold against selection that favours dropping the protection.

Bridge map: settlement O1 ↔ MB1, MB4a; trader coverage ↔ MB7, MB7c; collusion ↔ MB7d; exploration and proxy settlement ↔ MB11; operator capture ↔ MB4a, MB6; persistence ↔ MB5, MB9, MB10. Extend `appendices/appB-bridge-crosswalk.tex` when drafting, not a new map.

---

## 7. Lean items (proposed, not implemented)

Working module `FrameSettlement.lean`, importing `FrameCorrector` and the follow-up's `FrameEmbedded`. No new axioms, no `Safe` bypass. Real-valued items use Mathlib (`Real.log`, `Real.exp`); the rest are finite or over ℚ. Each item states the hypothesis it adds; an item with none is a restatement.

| Id | Statement | Size | Reuses | New hypothesis |
|---|---|---|---|---|
| **M1** `settlement_reachable_uninformative` | If the agent can choose the settled record at cost below its stake, every settlement-reading constraint is as blind as `blindRec`, and an own-outcome utility manipulates. | S | E5, `blind_constraint_cannot_separate`, `blind_constraint_manipulates` | cost κ, stake S |
| **M2** `race_secure_iff` | With the § 3.2 dynamics (κ linear in p/c, geometric growth, geometric stake), secure for all t iff \(R_0 > 1\) and \(g \ge 1\); if \(g < 1\), there is a finite failure time. | M | none | growth rates, stake decay |
| **M3** `weakest_link` | Secure iff the minimum attack cost exceeds S. | S | none | attack surfaces |
| **M4** `lmsr_binary_cost` | Binary LMSR: cost to move the price from p to p' is \(b \ln((1-p)/(1-p'))\). | M | none | LMSR |
| **M5** `lmsr_manipulation_loss_eq_kl` | With p = π, expected loss of moving to p' is \(b\,\mathrm{KL}(\pi\|p')\). | M–L | M4 | true probability π |
| **M6** `manipulation_pays_iff` | Manipulating a threshold decision pays iff \(S > b\,\mathrm{KL}(\pi\|\theta)\); KL is monotone in the distance to the threshold, which gives the asymmetric-threshold reading. | S | M5 | threshold θ |
| **M7** `repeated_reset_scales_cost` | With m honest resets, the cost is m times the one-round cost. | S | M5 | honest reset rounds |
| **M8** `untaken_branch_free` | In a conditional market with refunds and a deterministic rule, manipulating the untaken branch costs zero. | S | none | refund rule |
| **M9** `importance_weighting_restores_cost` / `zero_exploration_not_proper` | With exploration probability ε > 0 and 1/ε payoffs, expected payoff and manipulation cost equal the unconditional ones; with ε = 0 the payoff is constant in the report. | S–M | M8 | exploration ε |
| **M10** `audit_lottery_optimum` | \(\epsilon A + K/\epsilon\) is minimized at \(\sqrt{K/A}\) with value \(2\sqrt{AK}\) (AM–GM). | S | none | audit cost A, subsidy constant K |
| **M11** `correction_exploration_cheap` | Exploring "correct" with probability ε costs the principals ε times the cost of an unneeded correction. If the correction keeps the agent's options (the subset-branch condition), that cost contains no option loss, and the agent's stake in avoiding it is not positive. | M | `subset_branch_never_strictly_better`, `option_preserving_correction_half` | option-preserving correction |

Order: M1, M3, M8, M9, M11 first (finite; they carry the conceptual results), then M2 and M10, then M4–M7 (real analysis). Do not implement M4–M7 if the kill criterion fires on the finite items.

---

## 8. References

**In the repo bib** (`references/*.bib`): `garrabrant2017logical`, `demski2019embedded`, `garrabrant2021cartesian`, `fallenstein2015vingean`, `everitt2019`, `everitt2021agentincentives`, `carroll2024influenceable`, `perdomo2020`, `kosoy2022predca`, `greenblatt2024aicontrol`, `baker2025monitoring`.

**Not in the bib; checked by web search on 2026-11-10** (keys proposed):

- `hanson2007lmsr`: Robin Hanson, "Logarithmic Market Scoring Rules for Modular Combinatorial Information Aggregation", *Journal of Prediction Markets* 1(1):3–15, 2007, doi:10.5750/jpm.v1i1.417.
- `hanson2013votevalues`: Robin Hanson, "Shall We Vote on Values, But Bet on Beliefs?", *Journal of Political Philosophy* 21(2):151–178, 2013, doi:10.1111/jopp.12008. Futarchy.
- `hanson2009manipulator`: Robin Hanson and Ryan Oprea, "A Manipulator Can Aid Prediction Market Accuracy", *Economica* 76(302):304–314, 2009, doi:10.1111/j.1468-0335.2008.00734.x.
- `othman2010decisionmarkets`: Abraham Othman and Tuomas Sandholm, "Decision Rules and Decision Markets", AAMAS 2010, pp. 625–632. Deterministic-rule impossibility.
- `chen2011decisionmarkets`: Yiling Chen, Ian Kash, Michael Ruberry and Victor Shnayder, "Decision Markets with Good Incentives", WINE 2011, LNCS 7090, pp. 72–83, doi:10.1007/978-3-642-25510-6_7. Every action must have positive probability; lower risk raises worst-case loss.
- `chen2014elicitingdecision`: same authors, "Eliciting Predictions and Recommendations for Decision Making", *ACM Transactions on Economics and Computation*, 2014 (journal version; doi 10.1145/2556271, verify volume).
- `hubinger2020marketmaking`: Evan Hubinger, "AI safety via market making", AI Alignment Forum, 2020 (post id YWwzccGbcHMJMpT45; exact date not confirmed).

**From memory, verify before citing:**

- Robin Hanson, "Combinatorial Information Market Design", *Information Systems Frontiers* 5(1):107–119, 2003 (`hanson2003combinatorial`). Introduces market scoring rules.
- Robin Hanson, "Decision Markets", *IEEE Intelligent Systems* 14(3):16–19, 1999.
- Robin Hanson, "Foul Play in Information Markets", in R. Hahn and P. Tetlock (eds.), *Information Markets: A New Way of Making Decisions*, AEI-Brookings, 2006.
- Robin Hanson, Ryan Oprea and David Porter, "Information Aggregation and Manipulation in an Experimental Market", *Journal of Economic Behavior and Organization* 60(4):449–459, 2006 (`hanson2006manipulationexperiment`).
- Oprea, Porter, Hibbert, Hanson and Tila, "Can Manipulators Mislead Prediction Market Observers?", Chapman University working paper, 2008.
- Yiling Chen, Lance Fortnow, Nicolas Lambert, David Pennock and Jennifer Wortman, "Complexity of Combinatorial Market Makers", ACM EC 2008.
- Yiling Chen et al., "Gaming Prediction Markets: Equilibrium Strategies with a Market Maker", *Algorithmica* 58, 2010.
- Michael Ostrovsky, "Information Aggregation in Dynamic Markets with Strategic Traders", *Econometrica* 80(6), 2012.
- Tilmann Gneiting and Adrian Raftery, "Strictly Proper Scoring Rules, Prediction, and Estimation", *JASA* 102(477):359–378, 2007.
- Justin Wolfers and Eric Zitzewitz, "Prediction Markets", *Journal of Economic Perspectives* 18(2):107–126, 2004.
- Kenneth Arrow et al., "The Promise of Prediction Markets", *Science* 320(5878):877–878, 2008.
- Vanessa Kosoy and Alexander Appel, "Infra-Bayesianism" sequence, AI Alignment Forum, 2020. The other route: uncertainty about a world the agent's model may not contain, rather than logical uncertainty. One comparison paragraph.
- From the follow-up plan: Farquhar, Carey and Everitt 2022 (path-specific objectives); Carroll, Dragan, Russell and Hadfield-Menell 2022 (induced preference shifts).

Search pages used: [Chen et al. WINE 2011 (Springer)](https://link.springer.com/doi/10.1007/978-3-642-25510-6_7), [Othman & Sandholm AAMAS 2010](https://ifmas.csc.liv.ac.uk/Proceedings/aamas2010/pdf/01%20Full%20Papers/13_03_FP_0224.pdf), [Hanson & Oprea 2009 (IDEAS)](https://ideas.repec.org/a/bla/econom/v76y2009i302p304-314.html), [Hanson 2007 (IDEAS)](https://ideas.repec.org/a/buc/jpredm/v1y2007i1p3-15.html), [Hanson 2013 (bibbase)](https://bibbase.org/network/publication/hanson-shallwevoteonvaluesbutbetonbeliefs-2013), [Hubinger 2020 (GreaterWrong)](https://www.greaterwrong.com/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making).
