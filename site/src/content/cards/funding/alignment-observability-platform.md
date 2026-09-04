---
title: "Shared alignment observability platform"
type: funding
status: framework
summary: "Shared observability infrastructure for the research community — trace schema, ingestion, plugin-based analysis, and baseline unsupervised agency analysis — so analysis tools are comparable and applicable to a wide range of datasets."
fundingState: open
doneState: not_started
costUsd: 100000
costUsdMax: 500000
durationMonths: 12
fte: 1
fteMax: 5
dependsOn:
  - funding/unsupervised-agent-discovery
bookChapters: ["ch07", "ch09", "ch37", "ch38", "ch39", "ch41"]
roles:
  - Lead investigator
  - AI researcher
  - Software engineer (platform)
  - Data-science lead
related:
  - boundary-discovery
  - deployment-gate
---

## Problem

Our main impact target is a neglected bottleneck: **observability of alignment-relevant structure** in multi-agent systems and perspectively heterogenous human-AI systems.

Our working assumption is that risks from individual AI (e.g. models deployed by a single AI lab) can be made sufficiently safe (and if not that is not our core strength). We address the remaining and possibly bigger risk from optimization processes that are not clearly seen, e.g., because they are not designed but accidental. It is a risk where regulators cannot or don't want to trust the developer of the system(s).

## Approach

Our plan is to first build observability infrastructure for the research community and start bringing analysis tools together and make them comparable and applicable to a wide range of datasets.

The next step, maybe in year two, is to grow the community both at the trace data side (potential users of system in need of observation) as well as on the analysis side. The latter includes growing support for distributed, heterogenous, hybrid and other AI systems.

The ultimate goal is to establish reliable criteria for detecting agency and dangerous capability in real-world observation data collected by standardized tooling and provide the platform as an instrument for regulators for monitoring systems for compliance.

### ~20% funding (~$100k) — Core platform

Focus: demonstrate feasibility.

- 1 developer
- Build minimal platform: trace schema; ingestion pipeline (2 trace types); plugin-based analysis runner; baseline unsupervised agency analysis; simple reporting (including change over time)
- At least one external user (e.g. tester at another non-aintelope AI org)
- Demo and technical writeup

**Output:** a working platform showing that agent-like structure and changes can be detected from simple ingested data and monitored.

### ~75% funding (~$200k–$300k) — MVP + pilots

Focus: make the system usable by external collaborators.

- 2–3 staff (core team)
- Platform MVP: multiple plugin-based analyses; multiple trace sources (simulation, LLM workflows, cooperative AI simulations); 4 baseline analyses (clustering, time horizon, capability proxy, interaction graph); versioned reports and comparisons
- 2–3 pilot partners or serious letters of interest
- 2 case studies
- conference publications

**Output:** a usable system with external validation and first evidence of generality.

### ~75–100% funding (~$300k–$500k) — Early network + robustness

Focus: move from tool to shared infrastructure.

- 5+ staff (full team)
- Platform extensions: stable production ingestion API; multiple independent analyses; comparison across methods; richer reporting (interaction graphs, trends)
- 3–5 pilot partners including one dataset with deployment pipeline data; experiments with other real-world datasets
- External contributed analyses (plugin ecosystem)
- Work with policy/governance / sharing model for traces
- Public positioning writeup and dataset release

**Output:** early-stage shared observability with multiple users and methods.

## Milestones

- Core platform: trace schema, ingestion, plugin runner, baseline UAD analysis, external user demo.
- MVP: multiple analyses and trace sources, pilot partners, case studies, publications.
- Network: production API, plugin ecosystem, regulator-facing instrumentation.

## If it works

A shared observability layer where agent-like structure and changes can be detected from ingested traces, monitored over time, and compared across methods — infrastructure regulators and researchers can use without trusting a single lab's self-report.
