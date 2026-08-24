# Measurement as latent-variable discovery

- **Date:** 2022-09-20
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/9kNxhKWvixtKW5anS/you-are-not-measuring-what-you-think-you-are-measuring
- **Source read:** full
- **TSA files consulted:** `chapters/ch07-finding-boundary.tex`, `chapters/ch11-capability-without-task-ontology.tex`
- **Keywords grepped:** confounder; firehose; one-bit; latent variable; task ontology; ontology trap; adversarial measurement; intended measur

## Source ontology

John Wentworth’s First Law: an experiment’s intended variable is only a hypothesis about what the apparatus measures; in practice one almost always measures unknown mediators or confounders (latency instead of button design; floor sound instead of maze geometry). A corollary: if you are sure you are measuring the intended thing, you usually already know the result and so measure nothing. The Second Law: with enough distinct high-bandwidth observations (a “firehose of bits,” not a one-bit yes/no trial) one can sometimes recover the actual latents and their causal links (Pearl-style, many variables). High-bit instruments, not single controlled trials, are treated as the bottleneck of science. The intended measurand is demoted from given to recoverable object.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** ontology trap (ch07); task ontology / slice ≠ intended target (ch11, GL-13); alignment-as-measurement; adversarial measurement (C-010, ch39, appB MB7a–c); measurement-handle blur (ch07 P34K/P35M).
- **Overlap:** TSA already refuses to treat pre-existing labels as discovered objects (ch07 ontology trap) and treats capability scores as ontology-importing (ch11). GL-13 is the First Law inside TSA’s own stack: a correctly stated \(I_{\mathrm{ctrl}}^X\) implementation measured a one-event completion slice and equated a contention confounder with the true driver. Ch07’s handle-blur margin (“certifying the measurement setup, not the underlying system”) is the same failure in boundary language. Pearl is already in the ch07 source list.
- **Gap:** TSA’s measurement failures are typed as (a) wrong chosen ontology/boundary and (b) adversarial gaming. Wentworth’s cut is prior and non-adversarial: even a well-chosen, non-strategic experiment typically measures an unknown mediator; the named measurand is a hypothesis. TSA has no “one-bit experiment” class and no Second Law (firehose recovery of what you actually measured) distinct from interventional/adversarial protocols. GL-13 is filed as an implementation hazard, not as a general law applying to TSA’s own typed measurands and bridge checks.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The source does not force a new TSA cut: ontology trap, task-ontology, and handle-blur already cover the nearby object. It does add a split TSA underspecifies—non-adversarial confounder discovery vs adversarial measurement, and intended-variable-as-hypothesis vs “choose the right ontology.” That split bites TSA’s own program, which is a battery of named measurands (boundary, bundle, CCI, successor, basin) at risk of being one-bit tests. Worth a reverse-gap note, not a rewrite.
- **Ontology-stickiness risk:** Generic “confounders / wrong DV” is old stats advice a pre-2022 model already has. The load-bearing primitive—intended variable as hypothesis, unknown mediators as the actual scientific objects, firehose vs one-bit—is easy to collapse into TSA’s existing “ontology trap” and “adversarial measurement,” which miss the non-adversarial, high-bandwidth discovery cut and would not apply the First Law to TSA’s own named checks.
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already has ontology trap, task-ontology reimport, and handle-blur, but not Wentworth’s non-adversarial law that named measurands are hypotheses and that only a high-bit firehose recovers what was actually measured.
