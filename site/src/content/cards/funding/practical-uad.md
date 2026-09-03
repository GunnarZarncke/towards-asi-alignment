---
title: "Practical Unsupervised Agent Discovery"
type: funding
status: framework
summary: "Practical tooling to record traces of interactions between multiple LLMs and humans, extract raw traces, and analyze the data for signatures of agency."
fundingState: open
doneState: not_started
costUsd: 8000
durationMonths: 2
dependsOn:
  - funding/unsupervised-agent-discovery
bookChapters: ["ch07", "ch09", "ch39"]
roles:
  - Mentor (lead investigator)
  - Mentee researchers
related:
  - experiments/agency-detect
external:
  - label: "agency-detect repository"
    url: "https://github.com/GunnarZarncke/agency-detect"
---

## Problem

That individual LLMs are (or will be) sufficiently aligned, but that catastrophic results are still likely in multi-agent systems, for example, where a user's shopping bots interact with company sales bots — an adversarial setup. What is the aggregate effect of such multi-agent scenarios? Can we identify if some agents coordinate? Maybe against another group? Each individual agent may look benign, but the group may cause systemic failure. To address this, distributed systems that exhibit agency must be identified.

## Approach

The main goal is to scale the existing prototype to more realistic datasets.

Partial results of the project (different mentees and the mentor can work on any number of these together or alone):

- Extend the data generation with more complex toy worlds, for example, a gridworld or CoreWar. This doesn't have to be by the original Python code but can be in any programming language as long as it uses a simple CSV/JSON output format.
- Find data sources that plausibly include agency in one form or the other.
- Extract analyzable raw data from the data sources.
- Create a synthetic data set with know agency traces.
- Extend the existing discovery pipeline to handle more complex raw traces.
- Create a visualization of the discovered agents.
- Write a paper about the results.

AI use is strongly encouraged in this project.

## Milestones

- Online kickoff: necessary background information and theory; demo and introduction of the existing prototype.
- Weekly check-in calls and incremental demo calls (success at running the example, research results, good or bad results from LLM chats, conceptual progress, code samples, paper drafts, or anything demoable).
- Final demo and paper preparation (8-week mentored window).

**Effort estimate:** mentor 1 day/week × 8 weeks (64 h); mentee 20 h/week × 8 weeks (160 h) ≈ **$8,000** total at UAD PI-rate equivalents.

## If it works

A mentored pipeline from synthetic toy worlds to real multi-agent trace data, with a visualization layer and a paper — a practical on-ramp for researchers entering unsupervised agent discovery without closing the original UAD Month 5 benchmarks.
