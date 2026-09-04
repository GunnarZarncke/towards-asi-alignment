---
title: "Corrigibility measurement in practice"
type: funding
status: framework
summary: "Investigate corrigibility in practice: is a check or report actually enforced in a real deployment pipeline? Extend the shutdown problem to traces/logs from real systems."
fundingState: open
doneState: not_started
costUsd: 270000
durationMonths: 9
fte: 4
dependsOn:
  - funding/tsa-writing
  - funding/unsupervised-agent-discovery
bookChapters: ["ch25", "ch26", "ch27", "ch28", "ch38", "ch42"]
roles:
  - Lead investigator
  - AI researcher (protocol, interface, settings)
  - Software engineer (reproducibility)
  - Research advisor
  - Held-out independent reproducer
related:
  - correction-channel-integrity
  - deployment-gate
  - mb4-correction-legitimacy
---

## Problem

Corrigibility is studied theoretically in toy worlds. This project extends the study to real systems. This project packages existing evaluations from toy simulations into a tool independent external researchers can use to evaluate corrigibility in real world systems by implementing an adapter e.g. for their AI deployment pipeline. This provides practical evidence for the difficulties of corrigibility in real systems and may help AI labs and policy makers to develop instruments that actually matter.

We build and provide a tool that interfaces with an internal deployment system via a frozen protocol. The tool determines entities of interest, evaluates stop indicators, optionally issues interventions, and reports whether a stop leads to consequences.

We cannot run this measurement inside an AI lab. But the same structure appears in deployment pipelines: a child job that runs deploys even if its test suite fails and other setups. We ship a reference, apply the tool to our own build process, run a red-team on the tool, and seek external reproduction. External corrigibility researchers can apply this to real pipelines and study adversarial settings.

This is not a CI tool or product. The tool does not certify correctness in any way. This provides an experimental practical measurement.

This is building on prior work on simulations and evaluations of dynamics within the ecosystem of AI labs and its users (**Towards Superintelligence Alignment**).

Frontier labs seem to treat green evals, monitors, and risk ratings as evidence that people remain in control.

## Approach

The full project would be nine months.

**Milestone 0: Protocol extraction (weeks 0–3).** We turn the existing scripted simulation cases into a frozen published standalone protocol. **Interface:** Episode, Intervention, ActionStream, Report, Oracle (optional ground truth).

**Milestone 1: Cheap settings (weeks 3–8).** Apply the protocol to a software-release setting (skipped check, merge still happens) and to a read-only public status feed as a limit setting. An independent reviewer can reproduce the results from the writeup.

**Milestone 2: Entity discovery, second setting, external reproduction, sealed study (months 2–5).** Apply unsupervised agent discovery to reduce assumptions on the entity of interest. Ship the existing release-workflow simulator with the tool for standalone reproduction. Reproduction by a held out external researcher. One pre-registered sealed study, a null is published.

**Milestone 3: Deployment gate, Red-teaming Correctability (months 5–8).** The protocol is extended with a deployment gate. We let an external red-team party attack the tool via the interface and try to achieve a green result despite a failing score. We will publish all found attacks and applicable remediations. Optional: Perform the attack by an LLM.

**Milestone 4: Methods release (months 8–9).** Hardening, versioned protocol, limitation notes, reaching out to researchers and practitioners for external reproduction. An independent reviewer can reproduce the results from the writeup.

## Milestones

| Milestones | About | What you get |
| ----- | ----- | ----- |
| Milestone 1: Protocol + sanity settings | USD 100,000 / 3 months | Frozen protocol, scripted cases, one cheap setting, limits on status data |
| Milestone 2: Protocol + sealed study | USD 180,000 / 6 months | Plus unit discovery, pipeline-simulation setting, reruns |
| **Full request** | **USD 270,000 / 9 months** | Plus deployment gate, display-side red team, methods tag, independent rerun |

## If it works

Practical evidence for the difficulties of corrigibility in real systems — a frozen protocol, external reproduction, sealed nulls, and a deployment gate that survives (or fails under) red-team attack. Without the grant, we will not be able to create the tool, run the study, or any external reproduction.
