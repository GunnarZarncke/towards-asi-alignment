# Chapter 35 — κ-Edge Percolation Toy

Deterministic synthetic experiment for the "Percolation and Inferential Coupling"
subsection of `chapters/ch35-multi-agent-strategic-coupling.tex`.

Social (causal) edges exist first, generated from a stochastic block model over
communities with configurable degree distribution. A social edge only becomes
*cooperative* when the cooperativity index κ = (b/c) · p · ρ exceeds 1, where:

- `b/c` is the benefit/cost ratio slider,
- `p` (`pReach`) is the conditional probability a cooperative act actually
  reaches the other side, derived from tie strength,
- `ρ` is strategic/value correlation, also derived from tie strength but with
  a steeper exponent so weak bridge ties can exist and reach while still
  having low correlation.

The demo reports the giant-component fraction of the social graph and of the
κ-open ("cooperative") subgraph separately, plus the branching-process
critical threshold φ_critical = ⟨k⟩ / (⟨k²⟩ − ⟨k⟩) for comparison against the
observed open-edge share φ.

The key failure mode the chapter warns about is visible when the social graph
has a giant component but the κ-open graph does not: communication exists,
but cooperative correction does not conduct. This is a toy illustration of
the qualitative claim, not an empirical estimate of real deployment κ values.
