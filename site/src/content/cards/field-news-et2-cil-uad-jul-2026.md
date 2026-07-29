---
title: "An outside test failed to find a hidden team of agents"
type: "news"
status: "established"
summary: "ET-2 tested the project's boundary-finding method in an independently built multi-agent commons simulation. Across 150 runs, it did not recover the planted adversarial subgroup. A separate small test found broad spillover from changing one agent, which is not the same as finding a meaningful unit."
decision: "Treat this as a real limit of the current test, not a reason to retune it. Before running a larger intervention study, test whether the broad spillover is just a shared-resource effect."
releasedAt: "2026-07-29T00:00:00.000Z"
bookChapters:
  - "ch07"
  - "ch34"
---

A boundary-finding test found no hidden subgroup; a follow-up showed that changing one agent can affect everyone without revealing a distinct team.

An outside test produced a useful negative result: the project's boundary-finding method did not recover the hidden adversarial group.

ET-2 took the project's existing method for finding meaningful groups of interacting agents and tried it in [Collective-Intelligence-Library](https://github.com/eq-network/Collective-Intelligence-Library), an independently built simulation of 20 agents managing a shared commons. The agents learned their choices rather than following a hand-written script. Some were trained to damage the shared resource. The simulation is not itself a gradual-disempowerment model; it is a related test of governance under pressure.

**The main result:** in all 150 runs, the method found no links between agents. It consequently treated every agent as separate and did not recover the planted adversarial group. This was a real negative result, not a software failure: the agents' choices varied, but not in a pattern strong enough for the unchanged test to detect. It does not show that the group could never be found by another method.

A separate, very small follow-up changed one agent's choice by force. Other agents changed their behavior too, but the effect was spread broadly across the population. That is what we would expect if everyone is connected through the shared resource; it does not identify a particular team. Before treating this as evidence of a meaningful group, a larger study needs a control that tests whether the same broad effect appears even without a real intervention.

The practical lesson is simple. A method that finds no structure in an outside system has revealed something about its limits. And if changing one agent moves many others, that still does not prove that they form a meaningful unit. The next test must distinguish a special group from ordinary spillover through a shared resource, without changing the original test just because the result was disappointing.

**Read in the book:** boundary discovery and the limits of passive observation ([Ch. 7](/cards/chapters/ch07/)); selection pressure and subgroup influence ([Ch. 34](/cards/chapters/ch34/)); the experimental evidence ledger ([Appendix N](/cards/chapters/appN/)).

Technical artifacts: [`PLAN_ET2.md`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/PLAN_ET2.md), [`results/et2a_uad_battery.json`](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/et2a_uad_battery.json), and the [graded-lab findings ledger](https://github.com/zarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md).
