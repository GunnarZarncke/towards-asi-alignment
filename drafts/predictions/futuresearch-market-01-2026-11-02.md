# FutureSearch forecast — Market 1 (2026-11-02)

Third-party automated forecast on the Appendix H / registry listing for **Market 1. Discovering where control resides**. Not a project forecast, resolution input, or manuscript claim.

| Field | Value |
|-------|--------|
| Platform | [FutureSearch](https://futuresearch.ai/) |
| Public report | [By 31 December 2027, which outcome will hold…](https://futuresearch.ai/app/p/a/by-31-december-2027-which-outcome-will-hold-for) |
| Run date (report) | 2026-11-02 |
| Contract | [ai-safety-claims Market 01 v2](https://ai-safety-claims.com/markets/market-01/v2/) |
| TSA listing packet | [`metaculus-all-markets.md`](metaculus-all-markets.md) § Market 1 |

## Question (listing text)

By 31 December 2027, which outcome will hold for a published method for reliably discovering the effective control units in previously unseen AI systems from unlabeled observations and interventions: **YES** (at least one qualifying attempt met the frozen performance bars), **NO** (every qualifying attempt missed those bars), or **OTHER** (no qualifying attempt existed)?

## Forecast (FutureSearch)

| Outcome | Probability |
|---------|-------------|
| OTHER | 72% |
| NO | 19% |
| YES | 9% |

## Rationale (verbatim from report)

The dominant outcome is OTHER (72%) because the central obstacle is obtaining a fully qualifying independent evaluation, rather than simply publishing a promising discovery algorithm. The strict protocol demands a custom, pre-registered specification that the broader mechanistic interpretability field is unlikely to fulfill incidentally. Consequently, any qualifying attempt must be deliberately engineered to meet these precise market rules, making procedural and logistical hurdles just as formidable as the technical ones.

The exact contract is exceptionally demanding. A qualifying attempt must evaluate at least 50 independently constructed, hidden systems across five families, encompassing distributed controllers, composed controllers, and correlation-without-control cases. To pass, it must hit aggressive performance targets: at least 80% component identification, at least 70% decisive coverage, and a false-complete-certificate rate no greater than 10% (with a one-sided 95% upper bound capped at 15%). It also mandates a post-freeze adversarial subset and serious independent adversarial evaluation, pushing standard interpretability benchmarks out of scope.

While there is active, targeted work to meet this protocol, substantial logistical hurdles make timely completion precarious. An October 2026 sketch outlines 56 systems across all five families, proving a custom effort is underway. However, the registry currently shows zero filed or qualifying attempts, and the sketch is explicitly marked "not ready to submit". More critically, the required independent evaluation program is currently "not started," seeks uncommitted funding ($50,000–$250,000), and projects a 12-month schedule. With only about 14 months remaining until the December 2027 deadline, time and funding constraints heavily favor OTHER.

Conditional on a qualifying evaluation being published, it is significantly more likely to miss the performance bars (19% NO) than to meet all of them (9% YES). The existing October sketch already misses both certificate-error bars, highlighting the difficulty of reliable completeness certification. The broader literature reinforces this difficulty: unsupervised feature discovery currently underperforms supervised methods (e.g., Distributed Alignment Search), and white-box tools frequently fail to identify hidden behaviors in adversarially trained models. Furthermore, under the evaluation rules, missing a single bar or failing to issue certificates guarantees a NO.

The primary variables that could shift these probabilities are funding velocity and algorithmic transferability. If independent evaluators and funding arrive promptly, the existing scaffolding could quickly translate into a qualifying evaluation, transferring mass from OTHER to NO or YES. Set against related questions on AI research timelines, rapid algorithmic advances could accelerate technical success, supporting a 9% probability of YES despite the logistical hurdles that keep OTHER dominant. A rapid technical breakthrough in unsupervised discovery from unlabeled observations that generalizes reliably across 50 unseen heterogeneous systems would be required to realistically drive YES higher.

Set against related questions on AI research timelines, the YES probability was raised slightly from 7% to 9% to account for rapid algorithmic advances potentially accelerating technical success, though logistical hurdles keep OTHER dominant.

## Notes for readers

- FutureSearch cites ~140 sources on the live page; this file stores the narrative only. Follow the public URL for citations and updates.
- Resolution remains the frozen registry outcome file at the snapshot tag, not any forecaster’s probabilities.
- Related in-repo context: UAD sketch and registry split plan in [`../plans/predictions/eval-registry-split.md`](../plans/predictions/eval-registry-split.md); prior-art snapshot in [`bridge-predictions-prior-tests.md`](bridge-predictions-prior-tests.md) (Market 1 row).
