---
title: "AI 2027 speed assumptions stress-tested in a lab simulation (without confirming dates)"
type: "news"
status: "established"
summary: "AI 2027-style takeoff speedups were used only as schedule cues in a separate lab simulation with frozen safety batteries. Hard safety ranking held under moderate mapped stress but broke down under the strongest cue; selection dynamics differed by regime without validating calendar predictions. The public forecast code reproduced on a pinned fork; optional coupling from lab metrics to milestone years shifts medians in sensitivity plots, not as new timeline claims."
decision: "Treat macro forecasts and micro lab tests as separate evidence. Use scenario speedups to stress correction and selection mechanisms — not to confirm when SC, SAR, or ASI will arrive."
releasedAt: "2026-07-25T00:00:00.000Z"
bookChapters:
  - "ch12"
  - "ch14"
  - "ch30"
  - "ch34"
  - "ch42"
external:
  - label: "AI 2027 research"
    url: "https://ai-2027.com/"
  - label: "Takeoff forecast code (upstream)"
    url: "https://github.com/uvafan/timelines-takeoff-ai-2027"
---

A famous timeline forecast can drive lab safety tests — without the lab proving the forecast right.

[AI 2027](https://ai-2027.com/) is a well-known scenario about very fast AI progress — with milestone labels like **superhuman coder (SC)**, **superhuman AI researcher (SAR)**, and paths toward **superintelligence (ASI)**. It is a *forecast*, not a measurement of what happened in a real lab.

This project ran a paired experiment: use AI 2027’s *speed* assumptions as a **schedule cue** in a separate **lab simulation** — a toy AI lab with real subprocess isolates and frozen safety tests — and ask what breaks under that pressure. The two tracks stay separate on purpose: the forecast does not prove the lab results, and the lab results do not confirm or refute AI 2027’s calendar dates.

**What the lab tests showed (under mapped stress):**

- **Harder safety ranking held** when stress looked like a moderate speedup; it **fell apart** under the strongest speedup cue — the referee’s ranking surface thinned, not because anyone retuned the detectors.
- **Selection pressure** behaved differently by regime: on a baseline schedule, the share of “correction-preserving” programs **eroded**; under stronger cues that share **stalled** while measured harm **rose** anyway.
- None of this validates “AI 2027 will happen on schedule.” It stress-tests mechanisms this project cares about under acceleration-shaped load.

**What we did with the forecast code (separate checkout, not merged into the lab):**

- Re-ran the public takeoff/timelines scripts on a pinned fork and got a **matched reproduction** (same ballpark milestone years as the published model).
- Added a simple knob — **oversight drag** — that adds calendar delay after each takeoff phase. In a smoke test, **+1 year of drag per phase** shifts the median SAR milestone about **one year later**. That is a mechanical check, not a calibrated map from lab metrics to real-world delay.
- Optionally linked lab-test statistics into the timeline model (“foster” coupling). A **512-run comparison** shows how different coupling rules shift median milestone years — again **sensitivity illustrations**, not new timeline predictions.

<figure class="book-figure">
<img src="/experiments/lab-simulation/et3_foster_trajectories_median.png" alt="Median milestone years under six coupling scenarios compared to the baseline AI 2027-style forecast" />
<figcaption>Median paths through milestone years: baseline forecast is earliest; combining all optional coupling rules pushes the median ASI milestone about 3.5 years later in this exercise.</figcaption>
</figure>

<figure class="book-figure">
<img src="/experiments/lab-simulation/et3_foster_trajectories_sar_kde.png" alt="Distribution of when the SAR milestone arrives, 2027–2035, under different coupling rules" />
<figcaption>When SAR arrives: some rules keep mass near 2027; combined coupling spreads probability toward ~2030.</figcaption>
</figure>

Those chapters were **not rewritten** from this experiment; the card links related ideas. Full methods and numbered findings (LS-42–48) are in the [lab findings ledger](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md).

Technical artifacts: [`PLAN_ET3.md`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/PLAN_ET3.md), [`results/et3_phase1_summary.json`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/et3_phase1_summary.json).

**Read more in:** [Ch. 12, *Capability Growth Is Boundary Expansion*](/cards/chapter/ch12/); [Ch. 14, *When Intelligence Deepens Misalignment*](/cards/chapter/ch14/); [Ch. 30, *Successor Creation as the Central Alignment Test*](/cards/chapter/ch30/); [Ch. 34, *Alignment Is Selected or Destroyed by Its Environment*](/cards/chapter/ch34/); and [Ch. 42, *A Safety Case for Superintelligence Alignment*](/cards/chapter/ch42/).
