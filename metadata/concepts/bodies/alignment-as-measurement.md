---
related:
  - the-boundary-error
  - boundary-discovery
---

Many alignment arguments begin too late. They ask whether a model's objective is safe, whether a policy is corrigible, or whether a trained network contains a mesa-optimizer — all of which assume we already know what object is being aligned. Often we do not.

The book reframes the opening question as operational: which subset of the world, modeled as a bounded process with internal state, interface channels, and control capacity, best predicts the future changes that matter? That is a measurement question before it is an evaluation question.

This reframing carries through the rest of the manuscript. Boundary discovery, capability measurement, and correction-channel integrity are all downstream of first locating the right object — a step skipped by approaches that start from "is this policy's behavior acceptable?"
