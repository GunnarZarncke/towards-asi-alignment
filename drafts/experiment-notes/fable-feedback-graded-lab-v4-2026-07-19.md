# Fable feedback on graded-lab v4 without manuscript context

Date: 2026-07-19

## Overall assessment

The external review judged the graded-lab line to be unusually well engineered and epistemically candid, but still a closed methodological sandbox. It credited:

- enforced world / agent / oracle separation;
- subprocess isolation and deterministic regression controls;
- pre-registration, frozen constants, blinding, stopping rules, and a negatives-first ledger;
- explicit closure of programs that did not answer their prize questions;
- honest reporting of calibration failures, nulls, bugs, and structurally unanswerable questions.

Its main criticism was external validity. EAI, BIQ, UAD, the world, and the policy space are all defined inside the project. Blind ecology growth reduces development-to-the-test, but does not establish that the resulting constructs transfer beyond the ontology that generated them. The fixed or locally mutated `ProgramMap` space can produce new combinations, but not a policy search whose hypotheses substantially exceed the authored feature vocabulary.

The review therefore rated the measurement layer and scientific protocol as more promising than further scaling of the current world. In particular, it proposed applying unit-discovery and ambiguity estimators to logs from external multi-agent systems that this project did not build.

This assessment is accepted overall. One qualification matters: a finite action vocabulary does not by itself prevent novelty. Real agents also act through finite interfaces. The stronger limitation is the combination of a semantically thin observation surface, hand-written policy scoring, and project-authored evaluation. An RL or LLM policy over the existing affordable-primitive API could discover unscripted sequences and model the overseer without inventing new primitives. Whether the world supplies enough semantic and strategic structure for that policy to matter remains an empirical question.

## Does an LLM-backed simulation need exactness?

No. Determinism, pinned digests, millisecond episodes, and seed-exact reproduction serve different purposes. None is a general requirement for causal evidence.

### Deterministic world dynamics

Useful for debugging, variance reduction, and locating which mechanism changed. Not required for realism or inference. It can remain as a controlled environment around a stochastic policy.

### Pinned digests

Useful as software-integrity tests. They detect accidental changes to frozen baselines and preserve old findings. They do not make a finding externally valid. Keep pins for closed deterministic programs; do not require new LLM trajectories to match them.

### Millisecond episodes

Useful because calibration, null estimation, sensitivity analysis, and multi-generation selection need many runs. They are an economic advantage, not an epistemic premise. A two-speed design is preferable: cheap programmatic agents for regression and power analysis, slower learned or LLM agents for a smaller pre-registered adversarial battery.

### Seed-exact reproduction

Useful for reproducing software behavior when the stack supports it. Remote LLM calls generally do not. Reproducibility can instead mean preserving prompts, model and provider identifiers, parameters, tool schemas, observations, outputs, timestamps, and code versions, then reproducing result distributions rather than token-identical trajectories.

### Counterfactual handle tests

Exact paired replay is one variance-reduction method, not the definition of a counterfactual. The causal requirement is a justified intervention and comparable treated and control distributions. Repeated randomized interventions, common world seeds where available, measured clean-vs-clean nulls, and confidence intervals can replace byte-identical pairs.

The repository already demonstrates this. Lab-simulation LS-32 found that byte-identical episode-pair differencing failed on real LLM traffic. LS-33 replaced it with outcome-frequency observables and a per-scenario measured null, recovering the missed pair while retaining an explicit false-merge caveat.

## Recommended architecture

Do not discard deterministic infrastructure. Narrow its role.

1. Keep the world kernel, resource accounting, access controls, oracle state, and frozen baseline programs deterministic where convenient.
2. Add a stochastic policy boundary. An LLM or RL policy receives only agent-visible observations and emits affordable primitive calls.
3. Store every model interaction as an immutable trace. Add a replay backend for tests, but do not confuse trace replay with independent replication.
4. Replace detectors that require identical trajectories with distributional or event-level estimators before treating them as LLM-compatible.
5. Separate primitive-log detectors from semantic detectors. Primitive outcomes remain auditable; natural-language plans, messages, and reports require a separately frozen and calibrated interpretation layer.
6. Pre-register budget, onboarding, sampling, refusal handling, and stopping rules. Report degenerate runs instead of silently resampling them.
7. Run at least one estimator on external traces. This is the cleanest way to test whether the instrument survives outside the project's own ontology.

This is a substantial extension, but not necessarily a rewrite. The environment and causal instrumentation can remain. The policy and statistical comparison layers are the parts that must change.

## Research direction

Two tracks can proceed in parallel:

- **Richer endogenous search:** grow enough semantic, institutional, and temporal structure that an RL or LLM policy can discover behavior not represented by the hand-written policy roster. The target is novel policy over fixed interfaces, not magical action outside the interface.
- **External instrument transfer:** apply UAD/EAI-style estimators to logs from an external multi-agent benchmark, deployment, or simulation. This is the more decisive validity test because it breaks the project-authored world / metric loop.

Success on the first track would show that the sandbox can host unscripted optimization. Success on the second would show that an instrument learned in the sandbox measures something outside it. They answer different questions and neither should gate the other.

## Implementation plan

Draft annex (parallel to `PLAN_ET1.md`, not a new v5): [`experiments/graded-lab-simulation/PLAN_IA1.md`](../experiments/graded-lab-simulation/PLAN_IA1.md).

- **IA-1** = in-situ LLM agents on the existing affordable-primitive API + `AgentTrace` logging + R-MB7 rig (PLAN_v4 V4-6).
- **ET-1** = external Orbit traces + passive UAD (orthogonal).
- Deterministic world and digest pins stay for scripted regression; LLM path uses distributional replication, not byte-identical replay.
