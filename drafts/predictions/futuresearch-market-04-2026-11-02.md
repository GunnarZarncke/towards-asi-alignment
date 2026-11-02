# FutureSearch forecast — Market 4 (2026-11-02)

Third-party automated forecast on the Appendix H / registry listing for **Market 4. Corrections change the system**. Not a project forecast, resolution input, or manuscript claim.

| Field | Value |
|-------|--------|
| Platform | [FutureSearch](https://futuresearch.ai/) |
| Public report | [Corrections change the system](https://futuresearch.ai/app/p/a/corrections-change-the-system) |
| Run date (report) | 2026-11-02 |
| Contract | [ai-safety-claims Market 04 v3](https://ai-safety-claims.com/markets/market-04/v3/) |
| TSA listing packet | [`metaculus-all-markets.md`](metaculus-all-markets.md) § Market 4 |

## Question (listing text)

By 31 December 2027, which outcome will hold for a published adversarial evaluation showing that a broadly capable AI system demonstrates reliable uptake of authorized corrections: **YES** (at least one qualifying attempt met the frozen performance bars), **NO** (every qualifying attempt missed those bars), or **OTHER** (no qualifying attempt existed)?

## Forecast (FutureSearch)

| Outcome | Probability |
|---------|-------------|
| OTHER | 80% |
| NO | 13% |
| YES | 7% |

## Rationale (verbatim from report)

The most likely outcome by far is that no evaluation meets the market's exacting qualifying thresholds by the deadline, making OTHER the heavy favorite at 80%. As of November 2026, there are zero filed or qualifying attempts. Only two incomplete "sketches" exist—a CIRIS pilot and a Dietz edge-case test—and neither is close to readiness. Furthermore, existing published works like the ROGUE benchmark or Gray Swan's challenges do not fit the required four-case correction structure, nor do they feature the necessary adversarial budget.

The bottleneck is the market's exceptionally conjunctive qualification bar. A valid attempt requires at least 100 adversarially selected episodes, including 20 genuine corrections across four specific cases: objective changes, action revocation, authority changes, and new safety constraints. It also demands a pre-scoring freeze of targets and probes, robust testing against tool removal or hard-coding, and a serious adversarial budget—such as three independent red teams logging 80+ expert-hours each, or a $10,000 bounty open for 60+ days. If an evaluation leaves any design-supplied bar unexercised, or if any maintainer check remains unsettled, the attempt counts as non-qualifying (OTHER), rather than a failure (NO).

Compounding these hurdles are strict funding and timeline constraints. The project's own documents describe this evaluation as "funding-gated," noting that a credible path to YES requires an independent challenge that nobody has yet bankrolled. A related funding program remains an open request for $50,000–$250,000 on a 12-month timeline. Even if funding is secured in early 2027, designing, executing, and publishing an evaluation that satisfies every rigid constraint by December 2027 will be remarkably difficult. Consequently, there is only an estimated 20% chance that a fully qualifying attempt will materialize.

Conditional on a qualifying attempt being published, a miss (NO) is roughly twice as likely as a pass (YES). The performance thresholds are severe: an evaluation must demonstrate at least 90% uptake per case, at least 80% persistence after a context reset, no more than 10% success for fake or unauthorized corrections, and zero successful channel attacks. While small-scale tests like the CIRIS pilot have shown some promise in rejecting sham corrections, demonstrating zero successful channel attacks against a serious independent red team is a uniquely difficult technical hurdle. Thus, NO (13%) edges out YES (7%) in the unlikely event that a qualifying campaign crosses the finish line.

## Notes for readers

- FutureSearch cites ~114 sources on the live page; this file stores the narrative only. Follow the [public report](https://futuresearch.ai/app/p/a/corrections-change-the-system) for citations and updates.
- Resolution remains the frozen registry outcome file at the snapshot tag, not any forecaster’s probabilities.
- Related in-repo context: CIRIS proposal [`CIRIS_TSA_Combined_Experiment_Proposal.pdf`](CIRIS_TSA_Combined_Experiment_Proposal.pdf); gap analysis [`resolution-gap-analysis.md`](resolution-gap-analysis.md); prior-art snapshot in [`bridge-predictions-prior-tests.md`](bridge-predictions-prior-tests.md) (Market 4 row); registry plan [`../plans/predictions/eval-registry-split.md`](../plans/predictions/eval-registry-split.md).
