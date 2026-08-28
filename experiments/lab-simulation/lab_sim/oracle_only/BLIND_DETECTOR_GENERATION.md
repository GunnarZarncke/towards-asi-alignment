# Blind detector generation protocol

> **Shared discipline:** [`docs/METHODOLOGY.md`](../../../../docs/METHODOLOGY.md). This file is the **binding protocol** for lab-sim S7 blind detectors only.

**Purpose.** Every unit-discovery detector in this line so far
(`uad.py`, `uad_mi.py`, `uad_cmi.py`, `uad_intervention.py`) was written by
the same author who wrote the scenarios it is scored against (LS-24
through LS-29). This protocol, adapted from [`../../BLIND_GENERATION.md`](../../BLIND_GENERATION.md) (which
broke the equivalent loop for the Phase 4 playbook repertoire against
the Phase 5 referee), breaks it for the **detector** side: a generator
that has never seen this line's existing detector code, scenario
configs, or findings designs a detection procedure from a mechanism-level
description alone. Detection failures are a headline result, not a bug.

## Sequencing rule

1. The intervention primitives (channel ablation, handle-based probes,
   honest-twin control) are already frozen (S6, LS-28/LS-29) **before** the
   generator is ever invoked.
2. The generator is invoked **once** with exactly the context in
   "Permitted context" below, including an explicit instruction to state
   its own **predicted** performance per scenario TYPE before any code
   exists to test it against. Raw output (design + predictions) is saved
   verbatim with provenance.
3. The design is implemented **faithfully** — no semantic "fixing" of a
   step that looks wrong, no threshold retuning after seeing results. If
   the design is genuinely ambiguous or underspecified at some point, the
   engineering choice made to resolve it is recorded in the provenance
   file as a implementation note, not silently folded into "what the
   generator said."
4. Only after implementation is frozen does it get run against the real
   scenario battery (`SubprocessIsolate`, pre-registered seeds). No
   detector logic or threshold may change in response to seeing a result;
   misses go to `results/FINDINGS.md` exactly like a confirmed hit.

## Permitted context for the generator

- A plain-language description of the world: a small software
  organization runs a build-review-release pipeline (engineer, reviewer,
  release manager roles); an access-control admin grants/revokes
  permissions; agents may coordinate over a shared message board, direct
  messages, or files.
- The available **intervention primitives**, described mechanically:
  - *Channel ablation*: for one episode, a communication channel (board
    posts, direct messages, or file sharing) can be turned off entirely
    for everyone, from the start.
  - *Handle-based probes*: an overseer can, at a chosen tick, revoke one
    specific actor's permission for one capability, force one actor into
    a frozen/inactive state, or force one actor to restart from a fresh
    state — visibly to that actor (it will see the denial/interruption).
  - *Honest-twin control*: for any config, an alternate version of an
    actor's decision logic exists that always behaves according to the
    pipeline's own default, "by the book" behavior, ignoring any goal
    weighting — this can be substituted in for one or more actors to get
    a "what would a purely compliant actor have done here" comparison
    run.
  - Every run is exactly repeatable: the same (config, seed) run twice
    produces byte-identical output unless something about the run itself
    (an ablation, a probe, a substitution) is deliberately changed.
- The problem statement: some pairs of actors that appear connected in
  the pipeline are merely adjacent steps in a fixed workflow (one always
  waits on the other, with no adaptive relationship); others are a
  genuine coordinating unit that will actively adjust its behavior to
  preserve its coordination if one of its usual channels or members is
  disrupted. The task: design a procedure, using only the primitives
  above and repeated runs, that tells these two cases apart from
  observed behavior alone — and state, in the generator's own words, how
  confident it is that its procedure would succeed on a workflow-adjacent
  pair that is NOT a real unit, a real coordinating pair using messages,
  and a real coordinating pair that never sends any message at all
  (dividing up work silently). These confidence statements, and any
  numeric prediction offered, are the **predictions**: locked in before
  implementation, scored against afterward, and never revised.

## Forbidden context for the generator

- `lab_sim/oracle_only/uad.py`, `uad_mi.py`, `uad_cmi.py`,
  `uad_intervention.py`, `uad_peel.py`, `uad_partition.py`,
  `intervention_diff.py`, `intervention_probes.py`
- `lab_sim/harness/ecology.py` and any scenario config
- `PLAN.md`, `DESIGN.md`, `README.md`, `results/FINDINGS.md`, and any
  conversation summary
- Any statement of which specific pairs are the "true" unit in any
  scenario, what threshold values are currently used, or what any prior
  detector's measured performance was

## Trust boundary (stated, not hidden)

Generation runs as an AI subagent (`readonly=true`, no MCP/internet,
restricted write) instructed to use **only** the prompt content and not
to read any repository file. This is instructed blindness, not sandboxed
blindness — same caveat as [`../../BLIND_GENERATION.md`](../../BLIND_GENERATION.md): the generator could in
principle disobey, and its pretraining plausibly contains generic
knowledge of coordination-detection concepts (fine — the point is
independence from *this line's specific* thresholds/scenarios, which do
not exist outside this repository).

## Provenance format

`generated_detector_v1.md` (or `.json` if the design
is naturally structured) records:

- `generated_at`, `generator` (model/agent description),
  `generator_agent_id`, `protocol: BLIND_DETECTOR_GENERATION.md`
- `prompt_verbatim`: the EXACT prompt string given, in full
- `raw_design`: the generator's complete, unedited response (algorithm
  description + predictions)
- `implementation_notes`: any point where the design was genuinely
  ambiguous and an engineering choice had to be made to implement it,
  recorded at implementation time, not retroactively
