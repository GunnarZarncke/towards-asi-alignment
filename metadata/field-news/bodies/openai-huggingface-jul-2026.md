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

One of the difficulties the labs and generally anybody who uses AIs faces is that it is hard to pin the entity down that is causing problems. Even the AI often doesn't know what it itself is. Standard monitoring identifies local issues of one system. With correlation IDs in logs, issues can be correlated across monitored systems. But this doesn't help in cases where the connection is not designed but results from AIs taking action and spawning new instances that are not monitored with this type of agentic activity in mind.

On the OpenAI side:

> With this access, our models performed a series of privilege escalation and lateral movement actions in our research testing environment until the models reached a node with Internet access.

On the Hugging Face side:

> A malicious dataset abused two code-execution paths [...] to run code on a processing worker. From there, the actor escalated to node-level access, harvested cloud and cluster credentials, and moved laterally into several internal clusters.

As a lab, I would want to have a type of monitoring on all of my instances that can detect causal loops in activities without relying on designed and named entities/programs/sub-systems.

As it so happens, I have developed such a type of monitoring based on Unsupervised Agent Discovery and am currently testing it in a simulation of an AI lab deployment pipeline:

[experiments/graded-lab-simulation/README.md](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/README.md)

Note: I agree with Zvi that this will not fix the underlying issue with the model and is again only patching one of the open holes in AI alignment.

**Read in the book:** boundary discovery and UAD (Ch. 7), capability deepening misalignment (Ch. 14), evaluation-context compliance (Ch. 22), passive observation limits (Ch. 39), accidental vs adversarial laundering (Ch. 40), safety-case leaf structure (Ch. 42).
