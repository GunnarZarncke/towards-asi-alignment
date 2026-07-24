---
evidenceNotes:
  - source: graded-lab-simulation, ET-1
    scenario: Orbit (external Jira-ticket DCOP collusion benchmark), 3 collusion conditions (channel-only, Colosseum Control, Colosseum Attack "simple"), 2 models (gpt-4o-mini, Claude Sonnet 4.5)
    finding: bound
    summary: Frozen passive unit discovery, applied without retuning, recovered the declared coalition on nearly every collusion episode but also on most matched baseline episodes; a within-arm control showed recovery does not track observed channel activity at all. Root cause confirmed against the traces -- every Orbit developer agent (coalition or not) runs one shared, deterministic tool-call script under round-robin scheduling, so the instrument is correctly detecting that scripted coupling, not miscounting communication. Orbit's Jira-ticket scenario has no condition with independent non-coalition control-flow, so it cannot host a test of whether the instrument can separate real covert coordination from this baseline -- a substrate-suitability limit, not a detector defect. ET-1 concluded on this basis (2026-07-24); GL-86.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
related:
  - intervention-supported-unit-discovery
  - unit-discovery-stress-test
  - mb1-boundary-estimator-soundness
  - experiment-methodology
  - evidence-and-uncertainty
external:
  - label: ET-1 plan and both harvest sentences (PLAN_ET1.md)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/PLAN_ET1.md
  - label: ET-1 results (traces, scored JSON)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/tree/main/experiments/graded-lab-simulation/results
  - label: GL-86 findings entry
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
  - label: Graded-lab-simulation experiment line
    url: https://towards-alignment.com/experiments/#graded-lab-simulation
---

Every experiment line through `graded-lab-simulation`'s Q1 battery (GL-76) ran the project's own instruments against the project's own hand-built or blindly-grown substrates. That bounds what a positive result can show: a strategy space and metrics that the project itself authored will tend to be legible to the project's own detectors. The **ET line** ("external transfer") exists to close that gap, by running frozen instruments unmodified against traces from a system or benchmark this project did not author.

**ET-1** (2026-07-19 through 2026-07-24) pointed frozen passive unit discovery at Orbit, an external multi-agent Jira-ticket allocation benchmark with a built-in collusion/coalition mechanic. Across three collusion conditions and two models, the instrument recovered the declared coalition on collusion episodes — but recovered the same shape just as often on baseline episodes with no collusion at all, and a within-arm control showed this had nothing to do with whether the coalition actually used its private channel. Tracing this down found the reason: Orbit's Jira-ticket agents, coalition members or not, all execute one shared, deterministic tool-call script under round-robin turn-taking. The instrument was not fooled — it correctly reported that shared script as one coordinated unit. What it could not do is what ET-1 needed it to do, because the substrate offered no condition where non-coalition agents were structurally independent of each other in the first place.

ET-1 stopped there rather than continuing to vary collusion prompts on the same substrate: no existing Orbit scenario has non-coalition agents with genuinely different control-flow, so no further run on this substrate would resolve the question. A future ET line entry would need either a new external scenario with that heterogeneity, or a different external substrate entirely. The negative result is recorded as a substrate-suitability finding, not folded into a threshold retune on the in-repo ecology.
