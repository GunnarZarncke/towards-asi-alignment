---
title: "Unsupervised Agent Discovery"
type: funding
status: framework
summary: "Develop a method that finds agents directly inside complex systems without assuming them in advance. This lets us see what parts of a system are actually acting, what they want, and how they influence each other, so we can steer or incentivise AI systems and give regulators tools to detect agentic entities independent of their designers words."
fundingState: partial
doneState: partial
costUsd: 60000
fundedUsd: 10000
remainingUsd: 30000
durationMonths: 5
fte: 1
bookChapters: ["ch06", "ch07", "ch08", "ch09", "ch11", "ch12", "appI"]
roles:
  - Lead investigator
related:
  - experiments/agency-detect
  - boundary-discovery
---

## Problem

Current safety work assumes we already know where the agents are, what their boundaries are, and how they interact. But large AI systems blend components in ways that hide real goals and internal models. We infer these structures directly from recordings of raw system behavior.

Finding agents is important for deployed AI systems because feedback loops in these systems are bigger than the LLMs themselves or even the labs building them. The model may pass all the evals but when working thru users, tools, and institutional or financial incentives, it can destabilize the systems it is interacting with, especially if its loops are fast and applied in parallel. The same way well-intentioned humans in bad organizations can do a lot of harm.

To cause harm, generally to do anything, an entity needs relevant inputs and outputs whose effects come back to it, including effects on its continued existence. For deployed AI systems, we do not measure which outputs affect the existence of the deployed agent, the model, or its weights nor the optimization pressure and then we get surprised by effects like people pushing for continuation of ChatGPT-4o.

Talking only about what the text output of a model say or even what the mechinterp says about the intentions behind the output is not enough. We need tools that detect, anticipate or quantify such patterns.

## Approach

The most safety-relevant pieces: boundary detection, memory extraction, goal inference and clustering can be developed and validated without building more capable agents. These tools act as microscopes rather than amplifiers.

We infer agent structures directly from recordings of raw system behavior using ε-blanket-based boundary detection, memory-slice extraction, and multi-agent simulation validation.

## Milestones

- Month 1 — Robust implementation of ε-blanket-based boundary detection on synthetic data. **Done** (core detector hardened; calendar work largely before grant window, May 2026).
- Month 2 — Memory-slice extraction; automated detection of internal models of other components. **Partial** (lagged memory and S/A/I roles exist; ToM-style internal models of other components not shipped).
- Month 3 — Metrics for cooperation, opacity, and parasitic persistence. **Not done** as specified.
- Month 4 — Validation in multi-agent simulations. **Done** (learn_agents E0–E16, May–June 2026).
- Month 5 — Benchmarks on real-world AI systems (LLMs, model-mixtures, toolchains). **Not done** (real-data probes were adjacent host-machine and worm calcium work, not the promised AI-system suite).

**Grant completion note:** $10,000 bought a working synthetic detector and simulation validation, not the real-world AI benchmarks or the named cooperation/opacity/parasite metrics. Remaining ~$30,000 covers Month 2 remainder + Month 3 + Month 5 toward the moderate outcome: full implementation of unsupervised agent detection in real-world data in limited settings, with validation experiments and published paper.

## If it works

Success is the ability to:

- detect when new (sub) agents form inside AI systems,
- measure their goals and coupling,
- map when cooperation, deception, or parasitic dynamics arise, and
- intervene before unsafe structures stabilize.

If development goes well, the project scales into continuous agent-monitoring infrastructure for large deployments, red-team tools for detecting covert sub-agents, emergent hierarchies, and unintended cooperation patterns (collusion), and policy compliance tooling for collecting data to measure “agentic load” in distributed deployments.
