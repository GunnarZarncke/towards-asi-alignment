# Social dark matter

- **Date:** 2023-11-16
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/KpMNqA5BiCRozCwM3/social-dark-matter
- **Source read:** full
- **TSA files consulted:** `metadata/concepts/bodies/strategic-opacity.md`, `chapters/ch39-passive-observation-not-enough.tex`
- **Keywords grepped:** dark matter, conceal, latent population, selection environment, cost of faking, goal laundering, adversarial measurement, prevalence

## Source ontology

Duncan Sabien treats socially hidden traits and acts not as rare exceptions but as a **latent population** whose observed frequency is a distorted sample. Two laws: **Prevalence** — anything people have a strong incentive to hide is many times more common than it seems; **Extremity** — if stigma paints the thing as damning or debilitating, the median/modal instance is much milder than the cultural narrative, which is calibrated on the un-hideable tail. Destigmatization therefore looks like a prevalence explosion that is mostly visibility, not incidence. The unit is a *class of people under concealment pressure*, not a single agent gaming a test. It replaces “I never see X, so X is rare / the X I see is typical.”

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** strategic opacity (ch10); hidden productive BIQ / MB7a–c; passive observation (ch39); cost of faking and adversarial measurement (ch39, ch43); goal laundering (ch40); selection environment (ch34)
- **Overlap:** TSA already rejects “we would have seen it.” Strategic opacity is incentive-compatible concealment of the control locus; ch39 treats passive traces as fragile because a capable system can produce behavior *for the observer*; MB7 prices how much productive control can stay offline while monitors read green. That is the same concealment-incentive move as Prevalence, applied to one optimizer rather than a social class.
- **Gap:** TSA’s unit is a *system/control locus* under measurement, not a *latent population* with two estimator biases. It has no Extremity law (caught instances are the un-hideable tail, so eval-caught schemers are caricatures of the hidden class) and no destigmatization-as-visibility corollary (incident-reporting spikes are not incidence spikes). Stretching “selection environment” or “adversarial measurement” to cover this collapses population-sampling bias into per-system metric-faking.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** Load-bearing for how TSA reads “no one has seen it” and “the caught case looks terrifying,” without competing with boundary, bundle, CCI, successor, or basin cuts. A reverse-gap note would stop renaming Prevalence into MB7 and dropping Extremity. Score 4 would require changing a TSA cut; this does not. Score 2 would underweight that TSA already *talks* concealment and can silently treat the two-law object as already covered.
- **Ontology-stickiness risk:** High for pre-2023 training (deceptive alignment, scheming, “if it were common we’d know”). TSA already includes strategic opacity, so the failure mode is rename-and-exclude: treating social dark matter as MB7, and losing “visible ≠ typical” plus destigmatization-as-visibility. LLM-drafted TSA prose is likely to keep writing about one system hiding rather than a biased census of a hidden class.
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already prices concealment of a control locus; it still lacks Sabien’s two-law sampling object — a latent hidden class looks both rarer and more extreme than it is.
