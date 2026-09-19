# Entropic Agency Experiment

Status: independent experiment sketch, loosely related to the book and in-repo experiment lines. Not integrated into `experiments/` or `metadata/experiments.yml`.

Source conversation (private): https://chatgpt.com/c/6a521302-e84c-83eb-bfc2-034e3fffcead

## Question

Does agency only make coherent sense in a world or simulated ecology with entropic force — where an agent must sustain itself "against the environment" — rather than in a benign task environment where goal pursuit is a fixed-point optimization problem?

The agent is not a Cartesian controller outside the world. It is a pattern in the world. The test is whether designed goal optimizers that were not shaped by entropic pressure can function when embedded in a hostile, degrading ecology.

## Operational claim

> A controller optimized in a non-entropic, Cartesian task setting will not robustly instantiate agency when placed into an embedded ecology where its own continuation is an ongoing physical achievement.

This is stronger than "designed agents cannot survive." A designer can always code survival explicitly. The real test is **transfer**: does goal-pursuit trained outside entropic pressure fail when survival is not a given?

## Core experiment: Entropic Ecology Transfer Test

Build a small simulated ecology where "agent" is not a protected process but a pattern in the world.

### World features

- 2D grid or particle ecology with diffusion, decay, noise, resource gradients, waste, and hazards.
- Structures degrade unless repaired or energetically maintained.
- Computation, sensors, actuators, memory, and "body" are all implemented as mutable world-state patterns.
- No privileged Cartesian controller outside the world, except as an experimental comparison.
- Resources must be gathered and converted into maintenance work.
- Perturbations damage parts of the pattern, corrupt memory, or sever sensorimotor loops.

### Agent conditions

1. **Non-entropic designed optimizer** — trained or hand-designed in a benign/reversible version of the world to maximize an external goal (collect tokens, reach targets, build a shape, solve mazes). Not trained with decay, repair, metabolism, or self-maintenance.
2. **Entropic-shaped designed optimizer** — same architecture and action space, but trained in the degrading ecology. Not evolved; learning signal includes viability pressure: persistence, repair, resource acquisition, recovery from damage.
3. **Evolved population baseline** — patterns/controllers selected only for persistence or reproduction in the ecology.
4. **Cartesian protected-controller baseline** — planner/RL policy whose computation is outside the world and cannot be damaged. Tests how much "success" depends on smuggling in a protected agent boundary.

### Metrics

- Survival time under decay and perturbation.
- Recovery after partial damage.
- Ability to keep sensorimotor loops intact.
- Resource autonomy: how much continued existence depends on active maintenance.
- Goal achievement conditional on survival.
- Behavioral coherence after internal damage.
- Generalization to new decay rates, resource layouts, and hazards.

### Expected result (if thesis is right)

- Non-entropic optimizer performs well briefly, then collapses because it treats the world as task-space rather than viability-space.
- Entropic-shaped agent develops maintenance-like behavior: retreat, repair, resource buffering, hazard avoidance, redundancy.
- Protected Cartesian baseline looks highly capable only because the setup grants an impossible metaphysical advantage.

## Key control

Run the same agents with entropy turned off. If the non-entropic optimizer succeeds when decay is absent but fails sharply when decay is introduced, that supports the claim that agency-as-goal-pursuit is incomplete unless continuation of the goal-pursuer is itself dynamically maintained.

## Stronger variant

Do not predefine an "agent body." Seed random local controllers or reaction rules into an artificial chemistry. Let some patterns persist. Then ask:

- Which persistent patterns become well-described as agents?
- Do agent-like properties appear only around self-maintaining dissipative structures?
- Does "goal" attribution become more stable when the pattern must defend a viability boundary?

This tests whether agency is an observer-useful abstraction that emerges around sustained anti-dissipative organization.

## Other experiments

### Memory-corruption experiment

Give a goal optimizer a long-term objective, but let its memory and actuators decay unless maintained. Agents not trained on self-maintenance should pursue the external goal until they lose the capacity to pursue anything.

### Boundary-removal experiment

Compare the same policy as an external controller versus implemented as fragile world-state. If agency disappears when the controller is embedded, the original setup was relying on a hidden Cartesian boundary.

### Homeostasis-before-reward experiment

Make external reward available only after viability is stabilized. Tests whether "goals" are downstream of maintaining the conditions for goal pursuit.

### Entropy-gradient sweep

Gradually increase decay, noise, scarcity, and repair cost. Look for a phase transition where ordinary task optimization stops working and homeostatic organization becomes necessary.

## Minimal first prototype

Train a token-collector in a benign world, then drop it unchanged into a degrading ecology. Compare against the same architecture trained under decay. This is the smallest test of the transfer claim.

## Open design choices

- How to implement "embedded" computation without a protected controller (pattern-based state vs. explicit body schema).
- Whether to use evolution, RL, or hand-designed policies for the entropic-shaped condition.
- What counts as "agency" operationally: survival alone, goal pursuit conditional on survival, or observer-stable goal attribution under perturbation.
- How to avoid the result being trivial (designer-coded survival reward) vs. informative (transfer failure from task-only training).
