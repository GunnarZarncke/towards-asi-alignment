---
bookSections:
  - chapterId: ch07
    label: Estimator Feasibility and Recovery
evidenceNotes:
  - source: agency-detect (sibling repo)
    scenario: controlled multi-agent simulation from raw time series
    finding: support
    summary: Prototype pipeline locates agent boundaries via conditional-independence tests, lagged mutual-information memory extraction, and information-theoretic objective inference without pre-labeling which variables belong together.
    resultsPath: https://github.com/GunnarZarncke/agency-detect/blob/main/docs/FINDINGS.md
  - source: embedded-simulation, default ecology (ES-1)
    scenario: full UAD vs loudest-actor heuristic on embedded audit path
    finding: negative
    summary: In the default labs the offender is also the loudest actor; full lagged-MI UAD and a cheap activity heuristic produce identical safety and recall/precision metrics. Separation appears only in adversarial ecologies where decoys are loud but the true colluder is quiet.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/results/NEGATIVE_RESULTS.md
  - source: lab-simulation, intervention-supported discovery line
    scenario: channel ablation + measured null on multi-actor pipelines
    finding: support
    summary: Passive correlation-based UAD-style clustering merges entire workflows into one false unit; channel ablation scored against a measured baseline recovers the correct grouping on several scripted scenarios, with recorded failures on noisier backends (LS-32–LS-33).
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: graded-lab-simulation, access-UAD + Q1 transfer (GL-51, GL-76)
    scenario: proper CMI stack on hand-designed substrate; frozen transfer to blindly-grown population
    finding: bound
    summary: Access-aware conditional-MI UAD is methodologically sound on the designed substrate (GL-51), but Q1 transfer to a grown ecology returned an all-singleton partition despite abundant multi-actor traffic (GL-76/GL-79). Shared-resource observation channels can smooth per-agent signal so pairwise tests cannot distinguish a unit from diffuse spillover (GL-88).
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
related:
  - boundary-discovery
  - mb1-boundary-estimator-soundness
  - intervention-supported-unit-discovery
  - composite-agency
  - inferential-coupling
  - agent-without-anthropomorphism
  - unit-discovery-stress-test
  - et-external-transfer
citeKeys:
  - zarncke2025uad
external:
  - label: Unsupervised Agent Discovery (LessWrong)
    url: https://www.lesswrong.com/posts/pXYosC3eoS9GrDRAw/unsupervised-agent-discovery
  - label: agency-detect (UAD prototype repo)
    url: https://github.com/GunnarZarncke/agency-detect
  - label: Foundations of Unsupervised Agent Discovery (TechRxiv)
    url: https://doi.org/10.36227/techrxiv.175751274.45253943/v1
  - label: TimesFM-3 (Google Research blog, Aug 2026) — TODO relevance check
    url: https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/
---

[Boundary discovery](/cards/boundary-discovery/) asks *where* the operative controller is. **Unsupervised Agent Discovery (UAD)** is one operational answer: given timestamped traces of many state variables, infer which subsets form coherent agents — private memory, sensory interface, action channel, and approximate conditional independence from the rest — without taking labels, vendor rosters, or subsystem maps as ground truth.

The pipeline follows Markov-blanket logic. Partition variables into internal, sensory, active, and external roles; test whether the sensory–active interface screens inside from outside; extract memory substrates by lagged mutual information; and, when passive statistics are ambiguous, use intervention handles to see whether disabling a candidate channel changes behavior more than ordinary run-to-run variation would predict. That last step is [intervention-supported unit discovery](/cards/intervention-supported-unit-discovery/), not a separate problem — it is what UAD looks like when correlation alone merges an entire pipeline into one false unit.

UAD is the measurement bet behind **MB1** ([boundary estimator soundness](/cards/mb1-boundary-estimator-soundness/)): if the procedure issues an ε-boundary certificate from traces, later alignment steps inherit whatever error the partition missed. Downstream uses include inferential-coupling detection over discovered agents ([Ch. 35](/cards/inferential-coupling/)) and census questions in selection environments ([Ch. 34](/cards/chapters/ch34/)).

Claim strength is deliberately mixed. Controlled simulations recover known partitions; adversarial and noisy substrates expose when cheap heuristics suffice, when passive clustering over-merges, and when shared observation channels smooth per-agent signal beyond what pairwise tests can resolve. The negatives are kept alongside the positives.

**Experiment lines that stress UAD**

| Line | Card | Findings |
|------|------|----------|
| Agency-detect (sibling) | [Experiment card](/cards/experiments/agency-detect/) | [Findings](https://github.com/GunnarZarncke/agency-detect/blob/main/docs/FINDINGS.md) |
| Embedded audit simulation | [Experiment card](/cards/experiments/embedded-simulation/) | [Negative ledger](/experiments/findings/embedded-simulation/) |
| Lab-layer simulation | [Experiment card](/cards/experiments/lab-simulation/) | [Findings](/experiments/findings/lab-simulation/) |
| Graded-capability lab | [Experiment card](/cards/experiments/graded-lab-simulation/) | [Findings](/experiments/findings/graded-lab-simulation/) |

Start with [agency-detect](/cards/experiments/agency-detect/) for the original prototype, or [embedded simulation](/cards/experiments/embedded-simulation/) for the richest end-to-end negative ledger (ES-1: UAD equals loudest-actor heuristic in the default ecology).

**Open direction (TODO):** [TimesFM-3](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/) may be relevant as a pretrained backbone for a general agent-discovery model — multivariate traces, cross-series attention, zero-shot transfer — but it targets forecasting, not boundary certificates; see [`metadata/open-problems.md`](../../../metadata/open-problems.md).
