# Epistemic selves as stakeholders

- **Date:** 2022-11-22
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/o3RLHYviTE4zMb9T9/tyranny-of-the-epistemic-majority
- **Source read:** full
- **TSA files consulted:** `appendices/appB-bridge-crosswalk.tex`; `chapters/ch08-grow-split-merge.tex`
- **Keywords grepped:** Kelly; subagent; stakeholder; Bayesian; majority; hypothesis; epistemic; credence

## Source ontology

Scott Garrabrant recasts uncertainty as a **population of possible or future selves (hypotheses) that own probability-proportional stakes**. A decision is resource allocation among those epistemic subagents, not a single expected-value choice. Majority EV-max “seizes” minority bankroll (tyranny of the epistemic majority); proportional policy (each hypothesis bets its own stake) is **compositional**: boxing agents together yields wealth-weighted average beliefs and the same net bet, so it does not matter where you draw the boundary. Internal betting among the subagents *is* Bayesian updating; when both sides of a bet are costly, Nash bargain across selves yields Kelly (max expected log wealth). Fractional Kelly is an inside-view bettor plus a non-updating market-deference bettor, with an explicit wealth transfer between them. This replaces the usual “Kelly because long-run growth” argument with a one-shot fairness/governance primitive.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** operational subagents / grow–split–merge (ch08, also ch12, ch30); boundary discovery (Claim 1, ch06–ch10); App. B “Logical induction; infra-Bayesianism” exclude-by-reference row; field-glossary “selection theorems” (Kelly as type-signature example, not this unit)
- **Overlap:** TSA already treats “where you draw the box” as load-bearing, and names subagents as things that enter the effective boundary (ch08: integration, not ownership). Garrabrant’s compositionality claim is the dual: *aggregation rule* decides whether that cut is politically load-bearing. App. B already parks the nearby agent-foundations cluster (logical induction, infra-Bayesianism) as outside book ontology.
- **Gap:** TSA subagents are causal successors, delegates, and tools—not credence-weighted hypothesis-bettors. TSA cannot express “Bayesian update = internal bet reallocating control” or “EV-max as expropriation of minority worlds” without stretching successor-stability or selection-environment. Value-bundle / Nash talk is about bearers of values, not epistemic selves. Absorbing this into boundary discovery would fail the hostile test: Garrabrant argues proportional policy makes the cut *not matter* for bets; TSA argues the cut *is* the alignment object.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** Real ontology, real contact with Claim 1’s boundary politics, but not a missing spine primitive. Alignment purchase is a crosswalk pointer: distinguish epistemic-stakeholder subagents from TSA successor-subagents, next to the existing logical-induction exclude. Score 3 would be warranted if TSA’s six claims needed a proportional-vs-majoritarian aggregation rule; they do not. Score 4 would require changing the boundary or successor cut; this does not compete with those cuts.
- **Ontology-stickiness risk:** High for pre-2022 training (Kelly = growth-optimal betting; Bayes = scalar update). Post-TSA drafting will rename-and-exclude via the homograph “subagent”: ch08/ch30 look like coverage. Models will miss the stakeholder-population recarving and the cut-invariance claim.
- **Recommended action:** cite-in-crosswalk

## One-line finding

Garrabrant’s epistemic selves-as-stakeholders make Kelly and Bayes into proportional resource allocation among hypotheses; TSA’s subagents are successors, and App. B already excludes this agent-foundations neighborhood—cite the distinction, do not absorb.
