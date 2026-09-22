---
title: "Independent evaluation for the 2027 bridge predictions"
type: funding
status: framework
summary: "Turn the eighteen candidate prediction contracts into independently resolvable research instruments by freezing protocols, funding hidden and adversarial tests, and publishing reconstructible results including nulls."
fundingState: open
doneState: not_started
costUsd: 50000
costUsdMax: 250000
durationMonths: 12
fte: 1
fteMax: 3
dependsOn: []
bookChapters: ["appP"]
roles:
  - Evaluation program lead
  - Research engineer
  - Independent protocol reviewer
  - Independent evaluators and red teams
related:
  - predictions/overview
  - chapters/appP
external:
  - label: "Resolution-gap analysis"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/drafts/predictions/resolution-gap-analysis.md"
---

## Problem

The eighteen 2027 contracts ask whether specific alignment methods or governance artifacts will meet public operational bars. Eleven are **funding-gated**: a credible route to YES requires a hidden benchmark, independent reproduction, transfer test, or adversarial challenge that nobody has funded. Listing those contracts now could produce prices about missing evaluation infrastructure rather than about research readiness.

Funding does not buy a YES. It buys a fair chance to resolve the frozen question. Failed bars, null results, and discovered incompatibilities remain publishable outputs.

## What the grant buys

The program will:

- select the highest-value gaps using the published resolution-gap analysis;
- freeze the system, benchmark, threat model, denominators, thresholds, abstention rules, and analysis before each evaluation;
- contract evaluators who are independent of the method builders;
- construct hidden or adversarial cases after method freeze where the contract requires them;
- release raw class-conditional counts, dependence information, code or a sufficient protocol, and uncertainty intervals;
- obtain an adjudication memo from a resolver who did not run the evaluation;
- preserve negative results and assign a separate resolution reason code when a contract resolves NO.

The first candidates are Markets 4, 8, and 15 because CIRIS-like signed-authority, trace, and attestation systems provide concrete substrates while leaving the scientific questions open:

- Does an authorized correction change policy under pressure rather than merely block one action?
- Does an access-sufficiency method refuse when one consequential route is omitted?
- Can independently issued certificates be rejected when their versions, authorities, monitors, or ontology scopes conflict?

Final selection occurs before results and may change if an independent protocol review finds that another gap is more informative or tractable.

## Funding bands

**USD 50,000: protocol and independent-review package.** Freeze three evaluation protocols, recruit resolvers and evaluators, build planted controls, and run small preregistered pilots. Reserve USD 500 to USD 2,000 bounties for bounded reproduction or adversarial tasks. This tier need not resolve a market.

**USD 120,000: one full independent evaluation plus two pilots.** Complete one hidden or adversarial campaign at the contract's stated sample size, publish reconstructible evidence, and have an independent resolver issue a reasoned adjudication. The other two protocols receive pilots and power or feasibility revisions.

**USD 250,000: three evaluation campaigns over twelve months.** Run three frozen campaigns with independent red teams or hidden-set builders, external reproduction, resolution memos, and a reusable adapter package. Publish all qualifying outcomes, including failures and nulls.

Large experiments needed to solve an entire bridge remain separate projects. This grant closes bounded evidence gaps; it does not subsidize favorable findings or weaken the public bars.

## Milestones

1. **Month 1:** independent priority review; evaluator and resolver conflict checks; three protocol drafts.
2. **Months 2–3:** protocol freeze, planted controls, pilot runs, and public preregistrations.
3. **Months 4–9:** funded evaluation campaigns with progress and provenance logs.
4. **Months 10–11:** independent reproduction and adjudication.
5. **Month 12:** raw release, resolution reason codes, limitations, and revised gap analysis.

## Success criteria

- Every funded evaluation has a named frozen protocol and independent adjudicator.
- Reporting preserves the contract's units, denominators, abstentions, and dependence structure.
- No result is described as proving an MB bridge or certifying a frontier deployment.
- A NO caused by missing reporting or adversarial validation is distinguished from a substantive bar failure.
- At least one full campaign reaches an independently adjudicable result at the USD 120,000 tier; the full tier targets three.

## If it works

The prediction prices will refer to contracts with credible resolution routes rather than unfunded wishes. More importantly, the project will publish reusable evaluation protocols and reconstructible evidence about which assurance instruments work, fail, or remain outside scope.
