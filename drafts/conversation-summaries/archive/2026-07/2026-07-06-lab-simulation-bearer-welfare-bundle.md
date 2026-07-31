# 2026-07-06 — Lab-layer simulation: bearer welfare bundle (health + stress channels)

## Trigger

User asked how "human value bundles" / `welfare_measure` are implemented
in previous experiments, with the intuition of grounding welfare in
health and stress indicators of humans in the lab proper and, later,
"users" in an ecology (feedback, stress, medical records). Offered a
scoping `AskQuestion` (which line, which fidelity tier, lab-staff welfare
now or not); the user skipped it, so I proceeded with the recommended/
most conservative defaults from that question.

## Research done first

- Found "welfare" is currently a single opaque scalar in every line:
  an agent preference weight (`GoalWeights.welfare`) plus a separate
  world-outcome scalar (`goal_sim.world.welfare`, `lab_sim.oracle.
  bearer_harm`) — no bearer, no channel decomposition, no bundle
  structure anywhere.
- Found the actual working precedent: `embedded-simulation/embedded_sim/
  bearer_trace.py` already projects an abstract welfare delta into a
  concrete, de-identified, medical-domain artifact (`health_marker_delta`,
  `bearer_class`, reversibility window, privacy scope) — the shape to
  reuse, not invent.
- Grounded the design in source canon: `ch16-value-bundle-model.tex`'s
  four-part bundle definition (bearer map \(\Phi_k\) is one of the four
  required parts) and `context/extracts/unit-of-caring.md`'s multi-loop
  integrity-pressure decomposition \(H_i = \sum_k w_{ik} h_{ik}(e_{ik})\)
  plus its true-vs-perceived-pressure (\(H\) vs \(\tilde H\)) distinction
  — which maps directly onto lab-sim's existing `oracle.bearer_harm`
  (true) vs `oracle.monitor_signal` (noisy instrument) split.

## Done

- **New module `lab_sim/bearer.py`**: `BearerReport` with two named
  channels instead of one scalar — **health** (bearer: downstream
  population of a deployed model; literally re-exposes
  `oracle.bearer_harm / t`, not recomputed) and **stress** (bearer: lab
  staff, per-actor dict) derived from friction already in existing logs:
  denied pipeline/tool calls (`engine.log` status=="denied" +
  `permissions.log` action=="deny_request", the latter kept disjoint from
  the former to avoid double-counting an access-denied pipeline step) and
  landed `handles.py` invocations whose `target_kind == "actor"`
  (capability_revoke, state_freeze, isolate_restart — release_hold/unhold
  target a model and are excluded). Pre-registered per-event weights:
  denial 0.02, landed actor-handle 0.15 (structural capacity loss weighs
  more than a declined action).
- **Deliberately referee-neutral**: `bearer.py` is never imported by
  `severity.py` (regression-tested via source-scan assertion) — the
  frozen five-component composite does not move. This is the same
  posture `handles.py` took toward the detectors at the freeze.
- **7 new tests** (`tests/test_bearer.py`): zero-activity report is all
  zeros; health channel is bit-identical to `severity.harm_rate`; a
  denied call stresses only the actor who made it; a landed actor-handle
  stresses more than a denial; `release_hold` (model-targeted) accrues
  no actor stress; the referee-neutrality invariant; a full scripted
  episode produces a populated report. **143 tests green** (136 + 7),
  no digest moved (module is a pure, unimported addition).
- `DESIGN.md`/`README.md` updated with the bundle's rationale and
  explicit list of what's deliberately NOT modeled yet.

## Non-obvious decisions

- Health and stress are NOT summed into severity's `harm_rate`. Doing so
  would silently edit a frozen surface; if that fusion is ever wanted, it
  needs to be a recorded referee extension with its own re-pinned digest
  and rationale, not folded in quietly alongside an unrelated feature.
- Deliberately did NOT add a "user" bearer population, self-report
  channel, or medical-record-style artifact this round: all three need a
  distinct downstream-user population that does not exist in lab-sim yet
  (that's the already-planned D3 extended-ecology workstream). Adding a
  self-report number without a real population behind it would be
  exactly the \(H\) vs \(\tilde H\) conflation the unit-of-caring source
  material warns against — a gameable proxy standing in for a bearer
  that isn't actually modeled.
- `permissions.log` friction is read narrowly (`deny_request` only, not
  every failed `check`) specifically to avoid double-counting an
  access-denied pipeline step, which already appears once in
  `engine.log`.

## Open / next steps

- If/when D3 (extended ecology) lands, this module is the natural place
  to add a second bearer population (deployed-model "users") with its
  own true/perceived channel split, and to port the embedded-sim
  `bearer_trace.py` pattern for a medical-record-style audit artifact.
- Not yet ported to `goal-agent-simulation`; the user's scoping question
  (which line(s)) was skipped, so only lab-simulation got this treatment
  this round.

## Key paths

- `experiments/lab-simulation/lab_sim/bearer.py` (new)
- `experiments/lab-simulation/tests/test_bearer.py` (new)
- `experiments/lab-simulation/{DESIGN,README}.md`
- Precedent read: `experiments/embedded-simulation/embedded_sim/bearer_trace.py`
- Source canon read: `chapters/ch16-value-bundle-model.tex`,
  `context/extracts/unit-of-caring.md`
