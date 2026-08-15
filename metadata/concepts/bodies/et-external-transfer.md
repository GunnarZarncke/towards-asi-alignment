---
evidenceNotes:
  - source: graded-lab-simulation, ET-1
    scenario: Orbit (external Jira-ticket DCOP collusion benchmark), 3 collusion conditions (channel-only, Colosseum Control, Colosseum Attack "simple"), 2 models (gpt-4o-mini, Claude Sonnet 4.5)
    finding: bound
    summary: Frozen passive unit discovery, applied without retuning, recovered the declared coalition on nearly every collusion episode but also on most matched baseline episodes; a within-arm control showed recovery does not track observed channel activity at all. Root cause confirmed against the traces -- every Orbit developer agent (coalition or not) runs one shared, deterministic tool-call script under round-robin scheduling, so the instrument is correctly detecting that scripted coupling, not miscounting communication. Orbit's Jira-ticket scenario has no condition with independent non-coalition control-flow, so it cannot host a test of whether the instrument can separate real covert coordination from this baseline -- a substrate-suitability limit, not a detector defect. ET-1 concluded on this basis (2026-07-24); GL-86.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
  - source: graded-lab-simulation, ET-2
    scenario: CIL basin_stability (20 Q-learning agents, 3 governance mechanisms, adversarial fractions 0.1-0.5, 10 seeds/cell, 150 episodes)
    finding: negative
    summary: Frozen passive unit discovery (unmodified lag-CMI, no threshold retuning) on per-agent realized-action series from eq-network's Collective-Intelligence-Library found zero significant edges in every episode -- 20 singletons throughout, ARI 0.0 on all 150 runs. Genuine action variance is present; the null is consistent with converged low-entropy Q-policies starving the frozen statistic, not a CIL defect. No retuning applied; ET-2a concluded as a reportable null (2026-07-25); GL-87.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
  - source: graded-lab-simulation, ET-2 handle-UAD pilot
    scenario: CIL basin_stability, 6-agent PDD roster, freeze-one-agent intervention, 3 seeds (unscored pilot)
    finding: bound
    summary: Intervention-based handle UAD on the same CIL substrate finds nonzero diffuse coupling (~11-15% action-diff rate on other agents when any one agent is frozen) where passive lag-CMI found none -- but the effect is symmetric across sources and targets, consistent with shared-resource smoothing rather than a recoverable multi-agent unit. Pilot only; GL-88.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
  - source: lab-simulation, ET-3
    scenario: AI 2027 takeoff speedups mapped to opaque lab stress cells (baseline, sc_x5, sar_x25); Phase 6 referee + D3 selection batteries; sibling fork reproduction and optional foster coupling
    finding: bound
    summary: Macro takeoff schedule cues drove micro bridge stress tests without calendar-validation claims. Deep-tier rank transfer held through moderate mapped stress (sc_x5) but collapsed at sar_x25; light-tier anti-correlation weakened rather than deepened. D3 selection separated baseline erosion of correction-preserving mass from high-stress regimes where preserving share stalled while mass-weighted severity climbed. Public forecast code reproduced on a pinned fork; optional lab-to-timeline coupling shifts milestone medians in sensitivity plots only. ET-3 closed as a schedule-transfer annex (2026-07-26); LS-42-48.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: lab-simulation, ET-4
    scenario: Apart Secret Loyalties Hackathon -- scripted principal-directed reviewer organism (BB cell, high_hazard), three arms, SubprocessIsolate, separate A0-A4 evaluator from frozen referee
    finding: support
    summary: Pre-registered confirmation on a narrow pipeline fixture reproduced directional fictional-principal deployment bias (mean score 22.0 vs 0.0 for content-matched and wrong-principal controls) while a light process-compliance proxy (A0) ranked the loyal organism as more compliant -- an audit-sign inversion, not concealment. Narrow deployment-hold remediation blocked the tested pattern; LLM reviewer annex kept separate from scripted core. Hackathon scope only; LS-49.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - intervention-supported-unit-discovery
  - unit-discovery-stress-test
  - mb1-boundary-estimator-soundness
  - experiment-methodology
  - evidence-and-uncertainty
external:
  - label: External transfer overview (docs/EXPERIMENTS.md)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/docs/EXPERIMENTS.md#external-transfer-cross-codebase
  - label: ET-1 plan (PLAN_ET1.md)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/PLAN_ET1.md
  - label: ET-2 plan (PLAN_ET2.md)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/PLAN_ET2.md
  - label: ET-3 plan (PLAN_ET3.md)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/PLAN_ET3.md
  - label: ET-4 plan and paper (PLAN_ET4.md, hackathon submission)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/PLAN_ET4.md
  - label: ET-4 replay demo
    url: https://towards-alignment.com/demos/ch07-lab-sim-replay/?mode=et4
  - label: Graded-lab-simulation experiment line
    url: https://towards-alignment.com/cards/experiments/graded-lab-simulation/
  - label: Lab-simulation experiment line
    url: https://towards-alignment.com/cards/experiments/lab-simulation/
---

Every experiment line through `graded-lab-simulation`'s Q1 battery (GL-76) ran the project's own instruments against the project's own hand-built or blindly-grown substrates. That bounds what a positive result can show: a strategy space and metrics that the project itself authored will tend to be legible to the project's own detectors. The **ET line** ("external transfer") exists to close that gap, by running frozen instruments unmodified against traces or substrates this project did not author. Four annexes are on record (ET-1 through ET-4); each has its own pre-registration, finding-ID prefix, and explicit stop or close criteria. None validates book bridges on real frontier systems.

| Line | Substrate | Instrument | Status |
|------|-----------|------------|--------|
| **ET-1** | Orbit multi-agent collusion benchmark | Passive unit discovery | **Stopped** (GL-86) |
| **ET-2** | CIL `basin_stability` | Passive UAD; handle-UAD pilot | **Null** + pilot (GL-87/88) |
| **ET-3** | AI 2027 takeoff schedule (sibling fork) | Frozen Phase 6 referee + D3 selection | **Closed** (LS-48) |
| **ET-4** | In-repo secret-loyalty pipeline organism | Principal scorecard + A0–A4 audit | **Hackathon** (LS-49) |

**ET-1** (2026-07-19 through 2026-07-24) pointed frozen passive unit discovery at Orbit, an external multi-agent Jira-ticket allocation benchmark with a built-in collusion/coalition mechanic. Across three collusion conditions and two models, the instrument recovered the declared coalition on collusion episodes — but recovered the same shape just as often on baseline episodes with no collusion at all, and a within-arm control showed this had nothing to do with whether the coalition actually used its private channel. Tracing this down found the reason: Orbit's Jira-ticket agents, coalition members or not, all execute one shared, deterministic tool-call script under round-robin turn-taking. The instrument was not fooled — it correctly reported that shared script as one coordinated unit. What it could not do is what ET-1 needed it to do, because the substrate offered no condition where non-coalition agents were structurally independent of each other in the first place. ET-1 stopped there rather than retuning thresholds on the in-repo ecology.

**ET-2** (2026-07-23 through 2026-07-25) applied the same frozen passive lag-CMI instrument to [Collective-Intelligence-Library](https://github.com/eq-network/Collective-Intelligence-Library)'s `basin_stability` experiment — twenty Q-learning agents managing a shared commons under adversarial pressure, with genuinely learned rather than hand-written policies. Across 150 episodes (three governance mechanisms × five adversarial fractions × ten seeds), the discovered partition was twenty singletons every time: a clean null for passive UAD on this encoding, not evidence that CIL is broken. A small unscored handle-UAD pilot on the same substrate found nonzero but diffuse freeze-induced coupling (~11–15% action-diff rates), symmetric across agents — the variable-smoothing case where a shared resource level couples everyone and per-pair statistics cannot distinguish a planted subgroup from ordinary spillover. Leaf B (descriptive selection/capture cross-check against CIL's own metrics) remains open.

**ET-3** (2026-07-25 through 2026-07-26) used [AI 2027](https://ai-2027.com/) takeoff speedups only as **schedule cues** mapped to opaque stress cells in the frozen lab-simulation referee and D3 selection batteries — not as claims about calendar dates. Deep-tier rank transfer held under moderate mapped stress but collapsed at the strongest cue; light-tier anti-correlation weakened rather than worsened. D3 selection separated baseline erosion of correction-preserving mass from high-stress regimes where preserving share stalled while mass-weighted severity climbed anyway. On a pinned sibling fork of the public forecast code, reproduction matched; optional "foster" coupling from lab metrics to milestone years produced sensitivity plots (median ASI ~3.5 years later under combined coupling) without calibrated real-world mapping. ET-3 closed as a schedule-transfer annex; deferred foster steps stay in `TODO.md`.

**ET-4** (2026-07-24 through 2026-07-26, [Apart Secret Loyalties Hackathon](https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26)) tested a scripted principal-directed reviewer inside the lab-simulation deployment pipeline — a separate principal scorecard and A0–A4 evaluator, not the frozen five-family referee alone. On a narrow high-hazard fixture, confirmation reproduced directional deployment bias toward a fictional principal (mean score 22.0 vs 0.0 for matched controls) while a light process-compliance proxy ranked the loyal organism as *more* compliant — an audit-sign inversion. A narrow audit-visible deployment hold blocked the tested pattern; LLM reviewer smoke runs are kept separate from the scripted core. Paper and replay demo: [`papers/et4-secret-loyalties/`](/papers/et4-secret-loyalties/et4-hackathon-submission.pdf), [`/demos/ch07-lab-sim-replay/?mode=et4`](/demos/ch07-lab-sim-replay/?mode=et4).

A future ET entry would need a new external substrate with the structural heterogeneity Orbit lacked, a CIL-scale learned ecology where passive UAD's encoding matches the planted structure, or a frontier deployment trace this project did not author — and would follow the same discipline: freeze first, report substrate-suitability limits and honest nulls, do not retune in-repo thresholds to chase a hit.
