---
title: "ET-3: AI 2027 takeoff mapped onto lab-simulation stress cells"
type: "news"
status: "established"
summary: "External transfer ET-3 uses AI 2027 milestone speedups as opaque schedule cues for frozen Phase 6 and D3 batteries. Deep-tier transfer held at SC-scale stress but collapsed at SAR-scale; D3 preserving mass eroded on baseline only while severity rose under stronger cells. Phase 2 reproduction matched on fork branch gunnar/et3-annex; optional foster coupling maps lab metrics into takeoff calendar rules, shifting median ASI ~3.5 y later when all extensions are enabled."
decision: "Keep macro forecasts and micro bridge tests epistemically separate; use adapter mappings to stress correction and selection leaves, not to confirm calendar predictions. Treat foster trajectory plots as sensitivity illustrations, not calibrated timeline forecasts."
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
  - label: "Timelines / takeoff code"
    url: "https://github.com/uvafan/timelines-takeoff-ai-2027"
  - label: "ET-3 fork branch (annex)"
    url: "https://github.com/GunnarZarncke/timelines-takeoff-ai-2027/tree/gunnar/et3-annex"
---

Macro speedup forecasts can drive micro mechanism tests without pretending one validates the other's dates.

External transfer **ET-3** maps [AI 2027](https://ai-2027.com/) takeoff speedups onto opaque stress cells in the lab-simulation line — without merging codebases or claiming the micro-batteries validate macro dates.

**Phase 1 (driver):** frozen Phase 6 + D3 batteries under `baseline`, `sc_x5`, and `sar_x25`. Deep-tier rank transfer held through SC-scale stress but collapsed at SAR-scale; D3 correction-preserving mass eroded only on baseline while severity rose under stronger cells.

**Phase 2 (reverse + reproduce):** upstream takeoff and timelines scripts **reproduce matched** on fork branch [`gunnar/et3-annex`](https://github.com/GunnarZarncke/timelines-takeoff-ai-2027/tree/gunnar/et3-annex) (seed smoke, full figure regen). A one-parameter `oversight_drag` patch adds calendar lag per takeoff phase; mechanical smoke confirms median SAR shifts **+1.0 y** per year of drag. Optional `simulation.seed` patch recorded for determinism.

**Foster coupling (steps 1–3):** optional `et3_foster` blocks on the same fork map Phase 1 light/deep Spearman anchors and a successor-gate pause into takeoff calendar rules (default off). A **512-sim trajectory battery** compares six scenarios:

<figure class="book-figure">
<img src="/experiments/lab-simulation/et3_foster_trajectories_median.png" alt="ET-3 foster scenarios — median SAR, SIAR, and ASI milestone years" />
<figcaption>Median milestone ladder: baseline fastest; combined foster ~3.5 y later at ASI (LS-47).</figcaption>
</figure>

<figure class="book-figure">
<img src="/experiments/lab-simulation/et3_foster_trajectories_sar_kde.png" alt="ET-3 foster scenarios — SAR arrival density 2027–2035" />
<figcaption>SAR density: successor gate bimodal; all-foster spreads mass toward ~2030.</figcaption>
</figure>

**Read in the book:** capability vs correction under acceleration ([Ch. 12](/cards/chapters/ch12/)), intelligence deepening misalignment ([Ch. 14](/cards/chapters/ch14/)), successor closure ([Ch. 30](/cards/chapters/ch30/)), selection environment ([Ch. 34](/cards/chapters/ch34/)), safety-case tiers ([Ch. 42](/cards/chapters/ch42/)).

Artifacts: [`PLAN_ET3.md`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/PLAN_ET3.md), [`results/et3_phase1_summary.json`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/et3_phase1_summary.json), [`results/et3_foster_trajectories.json`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/et3_foster_trajectories.json).
