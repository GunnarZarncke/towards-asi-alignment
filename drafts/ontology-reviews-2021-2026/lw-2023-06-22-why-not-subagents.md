# Subagent → consolidated-agent dynamics

- **Date:** 2023-06-22
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/bzmLC3J8PsknwRZbr/why-not-subagents
- **Source read:** full
- **TSA files consulted:** `chapters/ch09-composite-agent.tex`, `chapters/ch08-grow-split-merge.tex`
- **Keywords grepped:** subagent, incomplete preference, coherence, composite agent, contract, utility maximizer, veto, money-pump

## Source ontology

Wentworth and Lorell replace the 2019 picture (an inexploitable veto-committee with incomplete preferences need not be a utility maximizer) with a **contracting-completion** relation. Strong incompleteness—states A ≺ B with a third state C incomparable to both—admits a (possibly randomized) contract or precommitment that holds C’s frequency fixed while shifting mass from less- to more-preferred states; non-strongly-incomplete preferences already encode a utility maximizer. The new state variable is therefore not “has subagents” but whether the plurality’s implied preferences are **stable under internal contracting**. If they are not, the system is incentivized to complete them; the only non-dominated equilibria are unitary expected-utility maximizers. The alignment bite is that incomplete-preference designs (e.g. shutdownability loopholes) are claimed to be dynamically unstable, not merely philosophically incomplete.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** composite agent / boundary discovery (ch09); merge by shared incentives and shared control (ch08); nearby greps: EU coherence / CCC (ch14), successor self-modification, CCI/shutdown as a one-bit correction projection
- **Overlap:** TSA already treats a plurality of named parts as a single alignment object when joint dynamics are more agentic than the parts (ch09: boundary closure, control reach, intentional compression). ch08’s merger tests (shared memory, correlated rewards, closed control loops) are the same family of “when does the committee become one optimizer?” questions, including markets and bureaucracies that optimize without any participant intending the market-level result.
- **Gap:** TSA’s composite tests do not carry **strong incompleteness** or **randomized preference-completion by contract**. Merge is diagnosed by compression and incentive correlation, not by Pareto-improving completion of vetoes. TSA therefore cannot say, except by stretching CCC or “the composite is the real agent,” that a remaining veto-structure is an unstable strategy rather than a durable form of plurality. The source’s claim that non-dominated composites tend to a representative utility function also sits next to TSA’s later refusal of a single utility as the value object, without TSA distinguishing “optimizer coherence” from “value-bundle geometry.”

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The primitive is a selection pressure on preference *structure* of composites, not a new alignment target. It matters for two TSA cuts: (1) when a market/committee should be treated as a unitary maximizer for boundary discovery, and (2) whether “keep preferences incomplete” can underwrite corrigibility or shutdown. TSA already routes shutdown into correction-channel integrity rather than incompleteness, but it does not record this specific instability. That is a reverse-crosswalk gap, not a reason to replace the composite or value-bundle cuts.
- **Ontology-stickiness risk:** High for the pre-2023 default that incomplete preferences are a safe alternative to EU agents, and that efficient markets need not have a representative agent. A model trained on that default, or on TSA’s composite/merge language alone, can *rename* plurality as “the real optimizer” while missing that internal contracting is the mechanism that completes it. TSA includes the nearby objects (composite, merge, CCC) and would not see this relation unless the reverse gap is named.
- **Recommended action:** add-reverse-gap

## One-line finding

Contracting-completion is a missing relation on TSA’s composite/merge cut: veto-plurality is not a stable alternative to a utility maximizer once internal contracts are allowed.
