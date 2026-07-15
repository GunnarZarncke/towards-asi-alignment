# Experiments

Reproducible research artifacts live here. Each experiment should have its own
subfolder so results, logs, and local TODOs stay scoped.

Narrative map: [`docs/EXPERIMENTS.md`](../docs/EXPERIMENTS.md). Structured index for the companion site: [`metadata/experiments.yml`](../metadata/experiments.yml). Cross-line lessons on blind generation/growth protocols: [`BLIND_GENERATION_METHODOLOGY.md`](BLIND_GENERATION_METHODOLOGY.md).

## Current Experiments

- [`toy-simulation/`](toy-simulation/) — multiresolution alignment toy simulation,
  bridge stress scenarios, and LLM red-team harness.
- [`embedded-simulation/`](embedded-simulation/) — embedded auditor on simulated
  machines: VFS artifacts, scripted MB scenarios, handle-mediated access tiers,
  red team, outer oracle evaluation.
- [`goal-agent-simulation/`](goal-agent-simulation/) — goal-driven agents (utility
  softmax over weights × tool access) replace scripted scenarios; mechanism-derived
  labels; held-out goal-space region protocol. Kept separate to preserve
  comparability of the embedded line's recorded results.
- [`lab-simulation/`](lab-simulation/) — lab-layer sim: JSON-RPC subprocess
  isolates, graded access tiers, playbook agents, referee batteries, and blind
  generation rounds (G-1 through G-8+).
