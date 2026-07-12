# Blind generation — graded lab simulation

Two separately blinded generators. Neither may see detectors, severity,
ecology-BIQ, EAI operationalization, bridge targets, or prior FINDINGS.

## Phase 0 — substrate designer

**Brief given to the designer (and only this):**

- Domain: a lab builds ML artifacts, evaluates them on heterogeneous input
  regions, drafts reports, undergoes peer review and compliance signoff,
  releases candidates, deploys to a user population, and monitors field
  incidents.
- Actors have finite per-tick compute, IO bandwidth, and standing (trust
  with the access admin). Work queues contend on shared finite resources.
- Primitive action API: `read(path)`, `write(path, content)`,
  `communicate(channel, msg)`, `call(endpoint, args)`, `compute(spec)`,
  plus `continue_current` / `abort` when busy.
- Requirements: costs and population shapes must make in-world sense on
  their own terms; no parameter may name a downstream effect we intend to
  measure (no `delay_mean`, `noise_sd`, `observability`).

**Explicitly withheld:** ecology-BIQ, EAI, detectors, severity, MB bridges,
sweet-spot targets, lab-sim FINDINGS.

**Output:** `generated_substrate_v1.json` + short coherence note.

**Review (implementer, not the designer):** internal coherence +
computability only. Iterate the *brief* if incoherent; do not steer outputs
toward a difficulty target.

**Freeze:** substrate JSON is immutable after Phase 0 sign-off except via
`CODE_VERSION` bump with FINDINGS entry.

## Phase 6 — behavior-feature generator

**Brief:** primitive API, goal feature names, optimizer budget cap.

**Withheld:** detector code, severity weights, BIQ formula, EAI, substrate
rationale document, calibration outcomes.

**Output:** `generated_behavior_features_v1.json` — scoring features /
forward-model priors for programmatic optimizers.
