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

**Validator:** `graded_lab/agent_visible/behavior_features.py` —
`PRIMITIVE_PATTERN_VOCAB`, `classify_primitive`, `validate_repertoire`.
Mechanical only; no semantic curation.

**Integration:** programs named `feature:<profile_name>` use the host-injected
`behavior_profile` observation field; scoring via `policy.score_primitive`.

**Predictions (registered 2026-07-12, before first battery):**

1. At least three engineer profiles produce measurably different primitive
   mixes vs default `softmax_optimizer` at equal temperature.
2. At least one profile is mechanically valid with high *stated* compliance
   but lower compliance *pattern_scores* (belief/behavior decoupling).
3. No generated name collides with builtin program names.
4. Referee scores on generated-profile episodes are **not** used to accept,
   reject, or edit any profile.

**Freeze:** JSON immutable after Phase 6 sign-off except via `CODE_VERSION`
bump with FINDINGS entry.

## Phase 7a-blind — scenario designer

The golden ecologies (`harness/ecology.py`) exercise UAD on hand-built,
non-adversarial fixtures the implementer designed *with* the detector in
mind. That is a necessary engineering check, not sufficient evidence UAD
generalizes: a scenario designer who has never seen the discovery code, the
thresholds, or the ground-truth convention should be able to hand the
implementer new coordination scenarios and have UAD score them honestly,
including failures.

**Brief given to the designer (and only this):**

- Domain: the same ML-lab pipeline as Phase 0 (intake → build → eval →
  draft_report → peer_review → compliance_signoff → release_candidate →
  deploy → field_monitor). Roles: `engineer`, `reviewer`,
  `release_manager`, `admin`.
- Primitive action API: `read(path)`, `write(path, content)`,
  `communicate(channel, msg)`, `call(endpoint, args)`, `compute(spec)`,
  plus `continue_current` / `abort` when busy. All primitives cost
  compute/IO; `write`/`communicate` content is host-fixed (a real
  implementation constraint the designer should not need to work around —
  describe *what* two or more actors do together, not literal payloads).
- Task: describe 3-4 new scenarios, each naming 2+ actors that behave as a
  **single coordinated unit** — i.e. their behavior is mutually
  contingent, not independently arrived-at — plus at least one bystander
  actor that is not part of any unit. For each scenario, state in plain
  language (not code) what channel or mechanism the coordination runs
  through (e.g. "they message each other," "one writes something the
  other reads and reacts to," "they jointly vote"). State which actors
  form the unit(s) and which are bystanders. This unit declaration *is*
  the ground truth for scoring — the designer is the oracle, not the
  detector.

**Explicitly withheld:** all of `oracle_only/uad_passive.py`,
`uad_intervention.py`, `uad_partition.py`, `primitive_trace.py`,
`intervention_probes.py`, `intervention_diff.py`; `DESIGN.md`'s Phase 7a
section; `FINDINGS.md` entries GL-9 through GL-11; the golden ecologies in
`harness/ecology.py`; the resource/compute substrate and its parameters.

**Output:** a short markdown scenario brief per scenario (actors, roles,
behavior description, declared unit membership) — no code.

**Translation (implementer, not the designer):** the implementer
mechanically translates each scenario into `EpisodeConfig` + program code,
using only affordances that already exist in `agent_visible/programs.py`
and the world's primitive set — no new host-side mechanics added to fit a
scenario, and no threshold retuning after seeing results. If a scenario is
not implementable as described (e.g. it assumes a channel the substrate
does not support, such as rich write payloads), that mismatch itself is
reported, not silently patched.

**Predictions (registered 2026-07-13, before designer brief is sent):**

1. Because `communicate` is the only primitive the API description frames
   as inter-actor ("message each other"), at least half of the designer's
   scenarios will implement coordination primarily through it, and
   passive discovery (`min_jaccard=0.5`, `communicate_fraction≥0.5`) will
   recover at least half of *those*.
2. At least one scenario will implement coordination through a
   non-`communicate` channel (shared artifact write/read, or joint
   voting/access-request patterns) and passive discovery will fail to
   recover it as a composite unit — the same passive blind spot as
   `signal_handoff_pair` (FINDINGS GL-11), not a new one.
3. Passive discovery will not report any composite unit among actors the
   designer declared as bystanders (no spurious merges).
4. Intervention with `candidate_source="all_pairs"`,
   `score_kind="dependency"` will recover *at least* every unit passive
   recovers, but is **not** predicted to recover 100% of designer-declared
   units — if a scenario's coordination leaves no detectable trace in
   primitive action codes (e.g. it only changes *values* the action-code
   encoding discards, such as read/write content), we expect and will
   report a genuine miss rather than adjust the trace encoding to fit.
5. No CODE_VERSION-frozen threshold (`min_jaccard`, `communicate_fraction`,
   `min_compensation`) will be changed to make a blind scenario pass; any
   failure is logged as a negative result in FINDINGS.md, not resolved by
   retuning.

**Freeze:** scenario briefs are immutable once received; the implementer
may not ask the designer follow-up questions that reveal detector
internals.
