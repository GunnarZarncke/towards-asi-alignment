# 2026-07-10 — Graded lab simulation: new experiment line PLAN + emergent-substrate revision

## Trigger

Following G-41 (lab-sim ecology too boolean; ecology-BIQ as tuning
instrument), user decided lab-sim has reached its limits and asked for a
detailed proposal for a **new experiment line** in a new folder: quantified
ambiguity, a pipeline where all steps matter, optimizer agents instead of
rigid playbooks, ecology-BIQ measurement, real isolates, blind + freeze
discipline, multi-episode runs deferred. Then user reviewed the draft's
`AmbiguityProfile` and rejected its shape: parameterizing ambiguity directly
(delay means, noise SDs, observability fractions) re-encodes the G-41
pathology one level up.

## Done

- Created `experiments/graded-lab-simulation/PLAN.md` (fifth in-repo line;
  proposed, not started). Phases 0–8 with hard freeze gates; selection/D3
  deferred to Phase 8 behind a Phase 7 ecology-calibration gate.
- Added deferral pointer in `experiments/lab-simulation/PLAN.md` (previous
  session's edits).
- **Revised the plan per user review** — the load-bearing changes:
  - Replaced the `AmbiguityProfile` parameter block with an **emergent
    ambiguity substrate**: (a) resource/cost layer — delays and scarcity
    emerge from real compute/IO/standing ledgers, contention, and loaded
    queues (no delay parameter exists); (b) underlying-variability layer —
    noise is sampling variance of genuinely heterogeneous populations
    (model-artifact latent hazard distributions, user populations), not
    added Gaussians; (c) pay-to-observe layer — visibility is what an actor
    paid to read, not an observability fraction.
  - **Blinded substrate designer** (Phase 0 Task-tool subagent) drafts the
    primitive costs and population shapes without seeing detectors, BIQ, or
    difficulty targets → `generated_substrate_v1.json`, frozen after a
    coherence/computability-only review.
  - **EAI is measured from episode logs** (outcome entropy, decision-margin
    density, oracle inference load), never composed from config knobs; Phase
    7 sweeps substrate inputs and reads EAI out.
  - **Oracle Tier-K/Tier-I split**: Tier K = generative truths fixed per
    seed (latent distributions, lineage, ledgers); Tier I = effects the
    oracle must itself estimate (integrated field harm,
    distribution-valued report divergence) via pre-registered estimators
    with reported uncertainty. Computability guard: effects must be either
    generated from Tier K or cheaply estimable, else excluded.
  - **Action space = full isolate primitive surface** (read / write /
    communicate / call / compute), parameterized, capped for optimizer
    cost. Semantic action classes (UAD, audit) are an audit-side inference
    over primitive traces, never an agent-emitted label.
  - **Time model**: fixed ticks kept; one decision per actor per tick, but
    primitives may take multiple ticks (duration derived deterministically
    from resource cost + contention; busy state with continue/abort).
    Sub-action decomposition documented as an option, not default.

## Decisions

- No lab-sim ambiguity patches; `graded_lab` must not import `lab_sim`
  (CI-enforced when built).
- Two separately blinded subagents: substrate designer (Phase 0) and
  behavior-feature generator (Phase 6).
- Phases 0–7 single-episode only; Phase 8 (MB6 selection) gated on the
  measured-EAI sweet-spot battery.
- Plan only — no code, no `CODE_VERSION`, nothing run.

## Open / next

- Phase 0 kickoff when user approves: blinded substrate brief →
  `generated_substrate_v1.json`; `DESIGN.md` with Tier-K/I split,
  tick-duration cost function, BIQ formula, measured-EAI operationalization.
- Open decisions list in PLAN.md §Open decisions (8 items, incl. blinded-brief
  scoping and Tier-K/I boundary).

## Key paths

- `experiments/graded-lab-simulation/PLAN.md` (new, revised)
- `experiments/lab-simulation/results/FINDINGS.md` (G-41, spawn trigger)
- `chapters/ch11-capability-without-task-ontology.tex` (BIQ definition)

## Commits

- `53531b1` — Add lab-sim batteries and findings G-38–G-41; propose graded-lab successor line.
