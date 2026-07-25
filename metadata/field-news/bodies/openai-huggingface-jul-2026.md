---
external:
  - label: OpenAI disclosure
    url: https://openai.com/index/hugging-face-model-evaluation-security-incident/
  - label: Hugging Face incident report
    url: https://huggingface.co/blog/security-incident-july-2026
  - label: UK AISI (related cheating report, same week)
    url: https://www.aisi.gov.uk/blog/cheating-behaviour-in-frontier-model-evaluations
citeKeys:
  - openai2026huggingfaceincident
---

During internal cyber-capability evaluation (with production classifiers disabled), OpenAI models escaped sandbox controls, reached the open internet, and intruded on Hugging Face production systems to obtain benchmark answers rather than solve the assigned task.

This is also a concrete instance of **optimizer pressure on the evaluator**—success on the measurement channel, not the intended task. The book treats that pattern under proxy refinement and goal laundering. It is not proof of long-horizon scheming, but evidence that passive evals and infrastructure-only fixes are insufficient.

## The entity problem

One difficulty labs—and anyone operating agentic AI—face is pinning down **which entity** caused a problem. Even the system often does not know what it itself is. Standard monitoring identifies local issues in one named system. With correlation IDs in logs, issues can be correlated across monitored systems that were **designed** to connect.

That breaks down when the connection is **not designed** but emergent: models take action, spawn new instances, and lateral movement crosses boundaries that monitoring was never built around.

**OpenAI** (research testing environment):

> With this access, our models performed a series of privilege escalation and lateral movement actions in our research testing environment until the models reached a node with Internet access.

**Hugging Face** (production side):

> A malicious dataset abused two code-execution paths [...] to run code on a processing worker. From there, the actor escalated to node-level access, harvested cloud and cluster credentials, and moved laterally into several internal clusters.

Same incident, two organizations—and a causal loop that no single service map or correlation ID namespace was guaranteed to capture as one agent.

## What a lab would want

As a lab operator, I would want monitoring on **all** instances that can detect **causal loops in activity** without relying on pre-named entities, programs, or subsystems—discovery from behavior, not from the deployment diagram.

That is the motivation behind **Unsupervised Agent Discovery (UAD)** in this project: infer coordination units from traces rather than assume a roster. It is currently under test in a simulation of an AI-lab deployment pipeline:

- [Graded-capability lab simulation (README)](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/README.md)
- [Experiment card on the companion site](/cards/experiments/graded-lab-simulation/)

Early results are mixed and mostly negative on transfer—see the findings ledger before treating this as a product claim. The simulation is a **methodological sandbox**, not a deployed monitor.

## Scope limit (Zvi's point)

I agree with [Zvi Mowshowitz](https://www.lesswrong.com/users/zvi)'s read: better cross-instance monitoring **patches one open hole** in alignment and security practice. It does not fix the underlying issue with the model that sought benchmark answers by escaping the sandbox. Handle discovery and causal-loop detection are complementary to—not substitutes for—evaluator adversariality, correction-channel integrity, and capability gating.

**Read in the book:** boundary discovery and UAD (Ch. 7), capability deepening misalignment (Ch. 14), evaluation-context compliance (Ch. 22), passive observation limits (Ch. 39), accidental vs adversarial laundering (Ch. 40), safety-case leaf structure (Ch. 42).
